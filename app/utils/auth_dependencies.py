from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.jwt_handler import verify_token
from app.crud.auth import get_user_by_email, check_rate_limit
from app.models.usuarios import Usuario, UserRole
from typing import Optional
from uuid import UUID

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtiene el usuario actual desde el token JWT"""
    token = credentials.credentials
    token_data = verify_token(token)
    
    user = get_user_by_email(db, token_data["email"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Obtiene el usuario actual y verifica que esté activo"""
    return current_user

async def require_admin(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Requiere que el usuario sea admin o super_admin"""
    if current_user.role not in [UserRole.admin, UserRole.super_admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes"
        )
    return current_user

async def require_super_admin(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Requiere que el usuario sea super_admin"""
    if current_user.role != UserRole.super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los super administradores pueden realizar esta acción"
        )
    return current_user

async def rate_limit_check(request: Request, db: Session = Depends(get_db)):
    """Middleware para verificar rate limiting"""
    client_ip = request.client.host
    check_rate_limit(db, client_ip)
    return True

def get_client_info(request: Request) -> tuple[str, str]:
    """Obtiene información del cliente (IP y User-Agent)"""
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    return ip_address, user_agent