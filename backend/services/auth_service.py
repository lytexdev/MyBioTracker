from datetime import datetime, timedelta
from typing import Optional, List
import json
import secrets
import asyncio
from passlib.context import CryptContext
from jose import JWTError, jwt
import pyotp
import qrcode
from io import BytesIO
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.pwd_context = pwd_context
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create_user(self, db: AsyncSession, email: str, password: str, is_admin: bool = False) -> User:
        hashed_password = self.get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def authenticate_user(self, db: AsyncSession, email: str, password: str, totp_code: Optional[str] = None) -> Optional[User]:
        user = await self.get_user_by_email(db, email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        
        if user.is_2fa_enabled and user.totp_secret:
            if not totp_code or not self.verify_totp(user.totp_secret, totp_code):
                if not await self.verify_backup_code(db, user, totp_code):
                    return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        user.failed_login_attempts = 0
        user.locked_until = None
        await db.commit()
        
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str, token_type: str = "access"):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload
        except JWTError:
            return None
    
    def setup_2fa(self, user_email: str) -> dict:
        secret = pyotp.random_base32()
        
        # Generate QR code
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name="MyBioTracker"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Generate backup codes
        backup_codes = [secrets.token_hex(4).upper() for _ in range(10)]
        
        return {
            "secret": secret,
            "qr_code": f"data:image/png;base64,{qr_code_b64}",
            "backup_codes": backup_codes
        }
    
    def verify_totp(self, secret: str, token: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)
    
    async def verify_backup_code(self, db: AsyncSession, user: User, code: str) -> bool:
        if not user.backup_codes or not code:
            return False
        
        try:
            backup_codes = json.loads(user.backup_codes)
            if code.upper() in backup_codes:
                backup_codes.remove(code.upper())
                user.backup_codes = json.dumps(backup_codes)
                await db.commit()
                return True
        except json.JSONDecodeError:
            pass
        
        return False
    
    async def enable_2fa(self, db: AsyncSession, user: User, secret: str, backup_codes: list[str]):
        user.totp_secret = secret
        user.is_2fa_enabled = True
        user.backup_codes = json.dumps(backup_codes)
        await db.commit()
        await db.refresh(user)
    
    async def disable_2fa(self, db: AsyncSession, user: User):
        user.totp_secret = None
        user.is_2fa_enabled = False
        user.backup_codes = None
        await db.commit()
        await db.refresh(user)
    
    async def handle_failed_login(self, db: AsyncSession, user: User):
        user.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)
        
        await db.commit()
    
    async def handle_successful_login(self, db: AsyncSession, user: User):
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        await db.commit()
    
    async def simulate_auth_delay(self):
        # Simulate authentication delay to prevent timing attacks
        await asyncio.sleep(0.5)

# FastAPI Dependencies
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_session

security = HTTPBearer()
auth_service = AuthService()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session)
) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    
    # Verify token
    payload = auth_service.verify_token(token, "access")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user email from token (consistent with login endpoint)
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user by email (consistent with how token was created)
    user = await auth_service.get_user_by_email(db, user_email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
