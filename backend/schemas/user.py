from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    newsletter: Optional[bool] = False

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_2fa_enabled: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProfileCreate(BaseModel):
    pass

class ProfileUpdate(BaseModel):
    email: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class TOTPSetupResponse(BaseModel):
    secret: str
    qr_code: str
    backup_codes: list[str]

class TOTPVerifyRequest(BaseModel):
    token: str

class BackupCodeVerifyRequest(BaseModel):
    code: str 