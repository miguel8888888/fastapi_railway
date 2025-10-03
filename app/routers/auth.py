from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.auth import (
    LoginRequest, LoginResponse, ForgotPasswordRequest, 
    ResetPasswordRequest, UserResponse, UserProfileUpdate
)
from app.crud.auth import (
    authenticate_user, create_reset_token, verify_reset_token, 
    use_reset_token, get_user_by_email, clean_expired_tokens,
    update_user_profile
)
from app.utils.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.auth_dependencies import get_current_active_user, get_client_info, rate_limit_check
from app.utils.email_service import send_reset_email
from app.models.usuarios import Usuario

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post("/login/", response_model=LoginResponse)
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limit_check)
):
    """Endpoint de login de usuario"""
    ip_address, user_agent = get_client_info(request)
    
    user = authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo. Contacta al administrador.",
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@router.post("/logout/")
async def logout(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Endpoint de logout (invalidar token del lado del cliente)"""
    # En una implementación más robusta, podrías invalidar el token en una blacklist
    return {"message": "Logout exitoso"}

@router.post("/forgot-password/")
async def forgot_password(
    request: Request,
    forgot_data: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: bool = Depends(rate_limit_check)
):
    """Solicitar recuperación de contraseña"""
    ip_address, user_agent = get_client_info(request)
    
    user = get_user_by_email(db, forgot_data.email)
    if not user:
        # Por seguridad, no revelamos si el email existe o no
        return {"message": "Si el email existe, recibirás un enlace de recuperación"}
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo. Contacta al administrador."
        )
    
    # Crear token de recuperación
    reset_token = create_reset_token(
        db=db,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    # Enviar email con el token de recuperación
    background_tasks.add_task(
        send_reset_email, 
        user.email, 
        reset_token, 
        f"{user.nombre} {user.apellidos or ''}".strip() or "Usuario"
    )
    
    # Limpiar tokens expirados en background
    background_tasks.add_task(clean_expired_tokens, db)
    
    return {"message": "Si el email existe, recibirás un enlace de recuperación"}

@router.get("/verify-token/{token}")
async def verify_token_endpoint(
    token: str,
    db: Session = Depends(get_db)
):
    """Verificar token de recuperación"""
    db_token = verify_reset_token(db, token)
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    return {"message": "Token válido", "valid": True}

@router.post("/reset-password/")
async def reset_password(
    reset_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Resetear contraseña con token"""
    success = use_reset_token(
        db=db,
        token=reset_data.token,
        new_password=reset_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo resetear la contraseña"
        )
    
    return {"message": "Contraseña actualizada exitosamente"}

@router.get("/me/", response_model=UserResponse)
async def get_current_user_info(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener información del usuario actual"""
    return UserResponse.from_orm(current_user)

@router.post("/test-email/")
async def test_email_config(
    background_tasks: BackgroundTasks,
    current_user: Usuario = Depends(get_current_active_user)
):
    """Endpoint para probar configuración de email (solo para administradores)"""
    
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden probar la configuración de email"
        )
    
    from app.utils.email_service import test_email_configuration
    
    # Probar configuración en background
    background_tasks.add_task(test_email_configuration)
    
    return {
        "message": "Prueba de email iniciada. Revisa tu bandeja de entrada.",
        "email": current_user.email
    }

@router.post("/test-emailjs/")
async def test_emailjs_config(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Endpoint para probar configuración de EmailJS"""
    
    if current_user.role.value not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden probar EmailJS"
        )
    
    from app.utils.email_emailjs import test_emailjs_config
    
    # Probar EmailJS
    success = test_emailjs_config()
    
    if success:
        return {
            "message": "Email de prueba EmailJS enviado exitosamente",
            "email": current_user.email,
            "service": "EmailJS"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error enviando email de prueba con EmailJS"
        )

# 🆕 NUEVOS ENDPOINTS PARA GESTIÓN DE PERFIL

@router.get("/perfil/", response_model=UserResponse)
async def obtener_perfil(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Obtener perfil completo del usuario actual"""
    return current_user

@router.put("/perfil/", response_model=UserResponse)
async def actualizar_perfil(
    perfil_data: UserProfileUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar perfil del usuario actual (incluyendo nuevos campos)
    """
    # Convertir a dict excluyendo valores no establecidos
    update_data = perfil_data.model_dump(exclude_unset=True)
    
    usuario_actualizado = update_user_profile(db, current_user.id, update_data)
    return usuario_actualizado