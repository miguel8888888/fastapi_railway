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
    # 🆕 NUEVOS CAMPOS OPCIONALES
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    pais: Optional[str] = None
    # 🖼️ CAMPOS PARA IMAGEN DE PERFIL
    profile_image: Optional[str] = None
    profile_image_path: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    role: Optional[UserRole] = None
    activo: Optional[bool] = None
    # 🆕 NUEVOS CAMPOS OPCIONALES PARA ACTUALIZACIÓN
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    pais: Optional[str] = None
    # 🖼️ CAMPOS PARA IMAGEN DE PERFIL
    profile_image: Optional[str] = None
    profile_image_path: Optional[str] = None

# 🆕 ESQUEMA PARA ACTUALIZAR PERFIL DE USUARIO (sin campos administrativos)
class UserProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    pais: Optional[str] = None
    # 🖼️ CAMPOS PARA IMAGEN DE PERFIL DE SUPABASE
    profile_image: Optional[str] = None
    profile_image_path: Optional[str] = None

class UserResponse(UserBase):
    id: UUID4
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    ultimo_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserResetPassword(BaseModel):
    new_password: str

# 🆕 ESQUEMA PARA CAMBIO DE CONTRASEÑA (usuario logueado)
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

# Token schemas
class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[UUID4] = None