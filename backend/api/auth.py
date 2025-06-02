from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import timedelta, datetime
from typing import Annotated
import json

from database import get_session
from schemas.auth import UserCreate, UserLogin, UserResponse, Token, Setup2FA, Verify2FA, PasswordReset
from services.auth_service import AuthService
from models.user import User

router = APIRouter()
auth_service = AuthService()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: AsyncSession = Depends(get_session)
) -> User:
    token = credentials.credentials
    payload = auth_service.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await auth_service.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(status_code=423, detail="Account temporarily locked")
    
    return user

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.post("/register", response_model=UserResponse)
@limiter.limit("3/minute")
async def register(
    request: Request,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="An account with this email already exists"
        )
    
    # Validate password strength
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )
    
    # Create user
    user = await auth_service.create_user(db, user_data.email, user_data.password)
    return UserResponse.model_validate(user)

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    user_data: UserLogin,
    db: AsyncSession = Depends(get_session)
):
    # Get user and check if exists
    user = await auth_service.get_user_by_email(db, user_data.email)
    if not user:
        # Don't reveal if user exists or not
        await auth_service.simulate_auth_delay()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        remaining = int((user.locked_until - datetime.utcnow()).total_seconds() / 60)
        raise HTTPException(
            status_code=423,
            detail=f"Account locked. Try again in {remaining} minutes."
        )
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is disabled")
    
    # Verify password
    if not auth_service.verify_password(user_data.password, user.hashed_password):
        await auth_service.handle_failed_login(db, user)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check 2FA if enabled
    if user.is_2fa_enabled and user.totp_secret:
        if not user_data.totp_code:
            raise HTTPException(
                status_code=400,
                detail="2FA code required"
            )
        
        if not auth_service.verify_totp(user.totp_secret, user_data.totp_code):
            # Check backup codes
            if not await auth_service.verify_backup_code(db, user, user_data.totp_code):
                await auth_service.handle_failed_login(db, user)
                raise HTTPException(
                    status_code=401,
                    detail="Invalid 2FA code"
                )
    
    # Successful login - clear failed attempts
    await auth_service.handle_successful_login(db, user)
    
    # Generate tokens
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: AsyncSession = Depends(get_session)
):
    token = credentials.credentials
    payload = auth_service.verify_token(token, "refresh")
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    email = payload.get("sub")
    user = await auth_service.get_user_by_email(db, email)
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    # Generate new tokens
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)

@router.post("/setup-2fa", response_model=Setup2FA)
async def setup_2fa(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    if current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA is already enabled")
    
    setup_data = auth_service.setup_2fa(current_user.email)
    
    return Setup2FA(
        qr_code=setup_data["qr_code"],
        secret=setup_data["secret"],
        backup_codes=setup_data["backup_codes"]
    )

@router.post("/verify-2fa")
async def verify_and_enable_2fa(
    verify_data: Verify2FA,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    if current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA is already enabled")
    
    # This endpoint should be called with the secret from setup-2fa
    # In a real implementation, you'd store the temporary secret somewhere secure
    # For now, we'll require the secret to be passed again or stored in session
    
    # Since we can't store state between requests easily here,
    # we'll implement a simplified version where user needs to provide the secret
    # In production, you'd use Redis or database to store pending 2FA setups
    
    raise HTTPException(
        status_code=501, 
        detail="2FA verification requires session state management. Please implement Redis-based session storage."
    )

@router.post("/disable-2fa")
async def disable_2fa(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    if not current_user.is_2fa_enabled:
        raise HTTPException(status_code=400, detail="2FA is not enabled")
    
    await auth_service.disable_2fa(db, current_user)
    return {"message": "2FA disabled successfully"}

@router.post("/change-password")
async def change_password(
    password_data: PasswordReset,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    # Verify current password
    if not auth_service.verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Validate new password
    if len(password_data.new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="New password must be at least 8 characters long"
        )
    
    if password_data.old_password == password_data.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )
    
    # Update password
    await auth_service.change_password(db, current_user, password_data.new_password)
    
    return {"message": "Password changed successfully"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    # TODO: Invalidate tokens
    # In a real implementation, you'd invalidate the tokens
    # This requires a token blacklist in Redis or database
    return {"message": "Logged out successfully"}

# Admin endpoints
@router.get("/admin/users", response_model=list[UserResponse])
async def get_all_users(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    users = await auth_service.get_all_users(db)
    return [UserResponse.model_validate(user) for user in users]

@router.post("/admin/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    user = await auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="Cannot modify your own account")
    
    await auth_service.toggle_user_active(db, user)
    
    return {
        "message": f"User {'activated' if user.is_active else 'deactivated'} successfully"
    }

@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_session)
):
    user = await auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == admin_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    await auth_service.delete_user(db, user)
    
    return {"message": "User deleted successfully"}
