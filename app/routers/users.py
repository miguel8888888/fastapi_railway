from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.auth import UserCreate, UserUpdate, UserResponse, UserResetPassword
from app.crud.auth import (
    create_user, get_users, get_user, update_user, 
    delete_user, reset_user_password, search_users
)
from app.utils.auth_dependencies import (
    require_admin, require_super_admin, get_current_active_user
)
from app.models.usuarios import Usuario
from uuid import UUID

router = APIRouter(
    prefix="/auth/users",
    tags=["Gestión de Usuarios"],
    dependencies=[Depends(require_admin)]
)

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Buscar por nombre, email, ciudad o país"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Listar usuarios con búsqueda opcional (solo admins)"""
    if search:
        users = search_users(db, query=search, skip=skip, limit=limit)
    else:
        users = get_users(db, skip=skip, limit=limit)
    return [UserResponse.from_orm(user) for user in users]

@router.post("/", response_model=UserResponse)
async def create_new_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_super_admin)  # Solo super_admin puede crear usuarios
):
    """Crear nuevo usuario (solo super_admin)"""
    user = create_user(db=db, user=user_data)
    return UserResponse.from_orm(user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Obtener usuario por ID"""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_id(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Actualizar usuario"""
    # Solo super_admin puede cambiar roles o crear super_admins
    if (user_data.role and 
        (current_user.role.value != "super_admin" and user_data.role.value == "super_admin")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los super administradores pueden asignar rol de super_admin"
        )
    
    user = update_user(db=db, user_id=user_id, user_update=user_data)
    return UserResponse.from_orm(user)

@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_super_admin)  # Solo super_admin puede eliminar
):
    """Eliminar usuario (solo super_admin)"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )
    
    delete_user(db=db, user_id=user_id)
    return {"message": "Usuario eliminado exitosamente"}

@router.post("/{user_id}/reset-password", response_model=UserResponse)
async def reset_user_password_by_admin(
    user_id: UUID,
    password_data: UserResetPassword,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """Resetear contraseña de usuario (admins)"""
    user = reset_user_password(db=db, user_id=user_id, password_data=password_data)
    return UserResponse.from_orm(user)