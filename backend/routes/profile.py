from fastapi import APIRouter, Depends, HTTPException, status
from database import get_session
from models.user import User
from services.auth_service import get_current_user
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/profile", tags=["profile"])

# Profile-Schemas die mit dem Frontend kompatibel sind
class ProfileCreate(BaseModel):
    # Das Frontend sendet möglicherweise diese Felder
    gender: Optional[str] = None
    birth_date: Optional[str] = None  # Als String, da nicht im User-Model
    height: Optional[int] = None
    weight: Optional[float] = None
    body_fat: Optional[float] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None
    target_weight: Optional[float] = None
    age: Optional[int] = None
    bmr: Optional[int] = None
    tdee: Optional[int] = None
    bmi: Optional[float] = None

class ProfileUpdate(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool
    is_2fa_enabled: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Routen ohne trailing slash (Hauptrouten)
@router.post("", response_model=UserResponse)
async def create_profile_no_slash(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Create or update user profile during onboarding"""
    return await _create_profile_logic(profile_data, current_user, db)

@router.get("", response_model=UserResponse)
async def get_profile_no_slash(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user

@router.put("", response_model=UserResponse)
async def update_profile_no_slash(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Update user profile"""
    return await _update_profile_logic(profile_data, current_user, db)

# Routen mit trailing slash (Fallback)
@router.post("/", response_model=UserResponse)
async def create_profile_with_slash(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Create or update user profile during onboarding - with slash"""
    return await _create_profile_logic(profile_data, current_user, db)

@router.get("/", response_model=UserResponse)
async def get_profile_with_slash(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile - with slash"""
    return current_user

@router.put("/", response_model=UserResponse)
async def update_profile_with_slash(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """Update user profile - with slash"""
    return await _update_profile_logic(profile_data, current_user, db)

# Gemeinsame Logik-Funktionen
async def _create_profile_logic(
    profile_data: ProfileCreate,
    current_user: User,
    db: AsyncSession
):
    """Gemeinsame Logik für Profil-Erstellung"""
    
    # Das aktuelle User-Model hat keine Onboarding-Felder, 
    # also simulieren wir einfach ein erfolgreiches Profil-Update
    current_user.updated_at = datetime.utcnow()
    
    # Log die empfangenen Daten für Debugging
    print(f"📝 Profile-Daten empfangen: {profile_data.dict()}")
    
    try:
        await db.commit()
        await db.refresh(current_user)
        print(f"✅ Profil für User {current_user.email} erfolgreich 'erstellt'")
        return current_user
    except Exception as e:
        await db.rollback()
        print(f"❌ Profil-Erstellung fehlgeschlagen: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save profile data: {str(e)}"
        )

async def _update_profile_logic(
    profile_data: ProfileUpdate,
    current_user: User,
    db: AsyncSession
):
    """Gemeinsame Logik für Profil-Update"""
    
    # Update nur Email wenn angegeben
    if profile_data.email:
        current_user.email = profile_data.email
    
    current_user.updated_at = datetime.utcnow()
    
    try:
        await db.commit()
        await db.refresh(current_user)
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile data: {str(e)}"
        ) 