from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool
    is_2fa_enabled: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

class Setup2FA(BaseModel):
    qr_code: str
    secret: str
    backup_codes: list[str]

class Verify2FA(BaseModel):
    totp_code: str

class PasswordReset(BaseModel):
    old_password: str
    new_password: str
