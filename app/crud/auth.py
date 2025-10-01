from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status
from app.models.usuarios import Usuario
from app.models.auth import TokenRecuperacion, Sesion, IntentoLogin
from app.schemas.auth import UserCreate, UserUpdate, UserResetPassword
from app.utils.security import hash_password, verify_password, generate_reset_token, get_token_expiration_time, validate_password_strength

# CRUD para usuarios
def create_user(db: Session, user: UserCreate) -> Usuario:
    """Crea un nuevo usuario"""
    # Validar fortaleza de contraseña
    validate_password_strength(user.password)
    
    # Verificar si el email ya existe
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_password = hash_password(user.password)
    db_user = Usuario(
        email=user.email,
        password_hash=hashed_password,
        nombre=user.nombre,
        apellidos=user.apellidos,
        role=user.role,
        activo=user.activo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: UUID) -> Optional[Usuario]:
    """Obtiene un usuario por ID"""
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
    """Obtiene un usuario por email"""
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    """Obtiene lista de usuarios"""
    return db.query(Usuario).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Usuario:
    """Actualiza un usuario"""
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID):
    """Elimina un usuario"""
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    db.delete(db_user)
    db.commit()
    return True

def reset_user_password(db: Session, user_id: UUID, password_data: UserResetPassword) -> Usuario:
    """Resetea la contraseña de un usuario (admin)"""
    validate_password_strength(password_data.new_password)
    
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    db_user.password_hash = hash_password(password_data.new_password)
    db_user.intentos_login = 0
    db_user.bloqueado_hasta = None
    db.commit()
    db.refresh(db_user)
    return db_user

# CRUD para autenticación
def authenticate_user(db: Session, email: str, password: str, ip_address: str, user_agent: str) -> Optional[Usuario]:
    """Autentica un usuario"""
    user = get_user_by_email(db, email)
    
    # Registrar intento de login
    log_login_attempt(db, email, ip_address, user_agent, False, "Credenciales inválidas")
    
    if not user:
        return None
    
    # Verificar si está bloqueado
    if user.bloqueado_hasta and user.bloqueado_hasta > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Usuario bloqueado hasta {user.bloqueado_hasta}"
        )
    
    # Verificar contraseña
    if not verify_password(password, user.password_hash):
        # Incrementar intentos fallidos
        user.intentos_login += 1
        if user.intentos_login >= 5:
            user.bloqueado_hasta = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        return None
    
    # Login exitoso
    user.intentos_login = 0
    user.bloqueado_hasta = None
    user.ultimo_login = datetime.utcnow()
    db.commit()
    
    # Registrar login exitoso
    log_login_attempt(db, email, ip_address, user_agent, True, "Login exitoso")
    
    return user

def log_login_attempt(db: Session, email: str, ip_address: str, user_agent: str, exitoso: bool, mensaje: str):
    """Registra un intento de login"""
    intento = IntentoLogin(
        email=email,
        ip_address=ip_address,
        user_agent=user_agent,
        exitoso=exitoso,
        mensaje=mensaje
    )
    db.add(intento)
    db.commit()

# CRUD para tokens de recuperación
def create_reset_token(db: Session, user_id: UUID, ip_address: str, user_agent: str) -> str:
    """Crea un token de recuperación de contraseña"""
    # Invalidar tokens anteriores
    db.query(TokenRecuperacion).filter(
        and_(
            TokenRecuperacion.usuario_id == user_id,
            TokenRecuperacion.usado == False
        )
    ).update({"usado": True})
    
    token = generate_reset_token()
    expiration = get_token_expiration_time(24)  # 24 horas
    
    db_token = TokenRecuperacion(
        usuario_id=user_id,
        token=token,
        fecha_expiracion=expiration,
        ip_solicitante=ip_address,
        user_agent=user_agent
    )
    db.add(db_token)
    db.commit()
    return token

def verify_reset_token(db: Session, token: str) -> Optional[TokenRecuperacion]:
    """Verifica un token de recuperación"""
    db_token = db.query(TokenRecuperacion).filter(
        and_(
            TokenRecuperacion.token == token,
            TokenRecuperacion.usado == False,
            TokenRecuperacion.fecha_expiracion > datetime.utcnow()
        )
    ).first()
    
    return db_token

def use_reset_token(db: Session, token: str, new_password: str) -> bool:
    """Usa un token para resetear contraseña"""
    validate_password_strength(new_password)
    
    db_token = verify_reset_token(db, token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    # Actualizar contraseña del usuario
    user = get_user(db, db_token.usuario_id)
    user.password_hash = hash_password(new_password)
    user.intentos_login = 0
    user.bloqueado_hasta = None
    
    # Marcar token como usado
    db_token.usado = True
    
    db.commit()
    return True

def clean_expired_tokens(db: Session):
    """Limpia tokens expirados y usados"""
    db.query(TokenRecuperacion).filter(
        or_(
            TokenRecuperacion.fecha_expiracion < datetime.utcnow(),
            TokenRecuperacion.usado == True
        )
    ).delete()
    db.commit()

# Rate limiting
def check_rate_limit(db: Session, ip_address: str, max_attempts: int = 5, window_hours: int = 1) -> bool:
    """Verifica límite de intentos por IP"""
    since = datetime.utcnow() - timedelta(hours=window_hours)
    
    attempts = db.query(func.count(IntentoLogin.id)).filter(
        and_(
            IntentoLogin.ip_address == ip_address,
            IntentoLogin.fecha_intento >= since,
            IntentoLogin.exitoso == False
        )
    ).scalar()
    
    if attempts >= max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos fallidos. Intenta de nuevo en {window_hours} hora(s)"
        )
    
    return True