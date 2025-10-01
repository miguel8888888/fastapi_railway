from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    super_admin = "super_admin"

# Esquemas de autenticación
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# Esquemas de usuario
class UserBase(BaseModel):
    email: EmailStr
    nombre: str
    apellidos: Optional[str] = None
    role: UserRole = UserRole.admin
    activo: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    role: Optional[UserRole] = None
    activo: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID4
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    ultimo_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserResetPassword(BaseModel):
    new_password: str

# Token schemas
class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[UUID4] = None