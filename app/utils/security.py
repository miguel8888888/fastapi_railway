from passlib.context import CryptContext
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from typing import Optional
import secrets
import string
from fastapi import HTTPException, status

# Configuración de bcrypt con salt rounds >= 12
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt con salt rounds >= 12"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_reset_token() -> str:
    """Genera un token seguro para recuperación de contraseña"""
    # Token de 32 caracteres con letras y números
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def validate_password_strength(password: str) -> bool:
    """Valida que la contraseña cumpla con los requisitos mínimos"""
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres"
        )
    
    if not any(c.isupper() for c in password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos una mayúscula"
        )
    
    if not any(c.islower() for c in password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos una minúscula"
        )
    
    if not any(c.isdigit() for c in password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos un número"
        )
    
    return True

def is_token_expired(expiration_date: datetime) -> bool:
    """Verifica si un token ha expirado"""
    return datetime.utcnow() > expiration_date

def get_token_expiration_time(hours: int = 24) -> datetime:
    """Genera tiempo de expiración para tokens"""
    return datetime.utcnow() + timedelta(hours=hours)