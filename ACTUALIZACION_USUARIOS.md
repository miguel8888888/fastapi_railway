# Actualización de Tabla Usuarios - Nuevos Campos

## 📋 Campos a Agregar

- **Teléfono**: Campo de texto opcional
- **Ciudad**: Campo de texto opcional  
- **Dirección**: Campo de texto opcional
- **País**: Campo de texto opcional

## 🔧 Pasos para Implementar

### 1. Actualizar el Modelo de Base de Datos

**Archivo**: `app/models/usuarios.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    es_admin = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    
    # 🆕 NUEVOS CAMPOS
    telefono = Column(String(20), nullable=True)  # Teléfono opcional
    ciudad = Column(String(100), nullable=True)   # Ciudad opcional
    direccion = Column(Text, nullable=True)       # Dirección opcional (puede ser larga)
    pais = Column(String(100), nullable=True)     # País opcional
    
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
```

### 2. Actualizar los Esquemas Pydantic

**Archivo**: `app/schemas/auth.py`

```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    # 🆕 NUEVOS CAMPOS OPCIONALES
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    pais: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    # 🆕 NUEVOS CAMPOS OPCIONALES PARA ACTUALIZACIÓN
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    pais: Optional[str] = None
    es_admin: Optional[bool] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    es_admin: bool
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# 🆕 ESQUEMA PARA ACTUALIZAR PERFIL (sin campos administrativos)
class UsuarioPerfilUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    pais: Optional[str] = None

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordConfirm(BaseModel):
    token: str
    new_password: str
```

### 3. Actualizar las Funciones CRUD

**Archivo**: `app/crud/auth.py`

```python
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.usuarios import Usuario
from app.schemas.auth import UsuarioCreate, UsuarioUpdate, UsuarioPerfilUpdate
from app.utils.security import get_password_hash, verify_password
from typing import Optional, List

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = get_password_hash(usuario.password)
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash=hashed_password,
        # 🆕 NUEVOS CAMPOS
        telefono=usuario.telefono,
        ciudad=usuario.ciudad,
        direccion=usuario.direccion,
        pais=usuario.pais
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario_update: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        update_data = usuario_update.model_dump(exclude_unset=True)
        
        # Si se está actualizando la contraseña, hashearla
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        # Actualizar todos los campos
        for field, value in update_data.items():
            setattr(db_usuario, field, value)
        
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

# 🆕 FUNCIÓN PARA ACTUALIZAR PERFIL DE USUARIO (sin permisos admin)
def update_usuario_perfil(db: Session, usuario_id: int, perfil_update: UsuarioPerfilUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        update_data = perfil_update.model_dump(exclude_unset=True)
        
        # Actualizar solo campos del perfil
        for field, value in update_data.items():
            if hasattr(db_usuario, field):
                setattr(db_usuario, field, value)
        
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def authenticate_user(db: Session, email: str, password: str):
    usuario = get_usuario_by_email(db, email)
    if not usuario:
        return False
    if not verify_password(password, usuario.password_hash):
        return False
    return usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario

# 🆕 BÚSQUEDA MEJORADA DE USUARIOS
def search_usuarios(db: Session, query: str, skip: int = 0, limit: int = 100):
    """Buscar usuarios por nombre, email, ciudad o país"""
    return db.query(Usuario).filter(
        or_(
            Usuario.nombre.contains(query),
            Usuario.email.contains(query),
            Usuario.ciudad.contains(query),
            Usuario.pais.contains(query)
        )
    ).offset(skip).limit(limit).all()
```

### 4. Actualizar las Rutas de API

**Archivo**: `app/routers/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import (
    UsuarioCreate, UsuarioResponse, UsuarioLogin, Token, 
    UsuarioUpdate, UsuarioPerfilUpdate, ResetPasswordRequest, ResetPasswordConfirm
)
from app.crud.auth import (
    create_usuario, authenticate_user, get_usuario_by_email, 
    get_usuarios, get_usuario, update_usuario, update_usuario_perfil,
    delete_usuario, search_usuarios
)
from app.utils.jwt_handler import create_access_token, verify_token
from app.utils.auth_dependencies import get_current_user, get_current_admin_user
from app.utils.email_service import send_reset_email
from app.models.usuarios import Usuario
from typing import List
import secrets

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# ... [endpoints existentes] ...

# 🆕 ENDPOINT PARA ACTUALIZAR PERFIL DE USUARIO
@router.put("/perfil", response_model=UsuarioResponse)
async def actualizar_perfil(
    perfil_data: UsuarioPerfilUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar perfil del usuario actual (incluyendo nuevos campos)
    """
    usuario_actualizado = update_usuario_perfil(db, current_user.id, perfil_data)
    if not usuario_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario_actualizado

# 🆕 ENDPOINT PARA OBTENER PERFIL COMPLETO
@router.get("/perfil", response_model=UsuarioResponse)
async def obtener_perfil(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener perfil completo del usuario actual
    """
    return current_user

# 🆕 ENDPOINT PARA BÚSQUEDA DE USUARIOS (Solo admins)
@router.get("/usuarios/search", response_model=List[UsuarioResponse])
async def buscar_usuarios(
    q: str,
    skip: int = 0,
    limit: int = 100,
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Buscar usuarios por nombre, email, ciudad o país (Solo admins)
    """
    usuarios = search_usuarios(db, query=q, skip=skip, limit=limit)
    return usuarios

# ENDPOINT ACTUALIZADO PARA CREAR USUARIO
@router.post("/register", response_model=UsuarioResponse)
async def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registrar nuevo usuario (con campos adicionales)
    """
    # Verificar si el usuario ya existe
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear usuario
    return create_usuario(db=db, usuario=usuario)

# ... [resto de endpoints existentes] ...
```

### 5. Actualizar Rutas de Usuarios (Admin)

**Archivo**: `app/routers/users.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UsuarioResponse, UsuarioUpdate, UsuarioCreate
from app.crud.auth import (
    get_usuarios, get_usuario, update_usuario, 
    delete_usuario, create_usuario, search_usuarios
)
from app.utils.auth_dependencies import get_current_admin_user
from app.models.usuarios import Usuario
from typing import List, Optional

router = APIRouter(prefix="/usuarios", tags=["Gestión de Usuarios"])

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Buscar por nombre, email, ciudad o país"),
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Listar todos los usuarios con búsqueda opcional (Solo admins)
    """
    if search:
        usuarios = search_usuarios(db, query=search, skip=skip, limit=limit)
    else:
        usuarios = get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: int,
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Obtener usuario por ID (Solo admins)
    """
    usuario = get_usuario(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar usuario (Solo admins)
    """
    usuario = update_usuario(db, usuario_id=usuario_id, usuario_update=usuario_update)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.post("/", response_model=UsuarioResponse)
async def crear_usuario_admin(
    usuario: UsuarioCreate,
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo usuario (Solo admins)
    """
    from app.crud.auth import get_usuario_by_email
    
    # Verificar si el usuario ya existe
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    return create_usuario(db=db, usuario=usuario)

@router.delete("/{usuario_id}")
async def eliminar_usuario(
    usuario_id: int,
    current_admin: Usuario = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar usuario (Solo admins)
    """
    usuario = delete_usuario(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return {"message": "Usuario eliminado correctamente"}
```

### 6. Script de Migración de Base de Datos

**Archivo**: `app/scripts/migrate_usuarios.py`

```python
"""
Script para migrar la base de datos y agregar los nuevos campos a la tabla usuarios
"""

from sqlalchemy import text
from app.database import engine, SessionLocal

def migrate_usuarios_table():
    """
    Agregar nuevos campos a la tabla usuarios existente
    """
    
    # Comandos SQL para agregar las nuevas columnas
    migrations = [
        "ALTER TABLE usuarios ADD COLUMN telefono VARCHAR(20)",
        "ALTER TABLE usuarios ADD COLUMN ciudad VARCHAR(100)",
        "ALTER TABLE usuarios ADD COLUMN direccion TEXT",
        "ALTER TABLE usuarios ADD COLUMN pais VARCHAR(100)"
    ]
    
    db = SessionLocal()
    
    try:
        for migration in migrations:
            try:
                db.execute(text(migration))
                print(f"✅ Ejecutado: {migration}")
            except Exception as e:
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    print(f"⚠️  Columna ya existe: {migration}")
                else:
                    print(f"❌ Error en: {migration}")
                    print(f"   Error: {e}")
        
        db.commit()
        print("\n✅ Migración completada exitosamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error en la migración: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔄 Iniciando migración de tabla usuarios...")
    migrate_usuarios_table()
```

### 7. Actualizar el Main de la Aplicación

**Archivo**: `app/main.py` (agregar al final)

```python
# ... [código existente] ...

# 🆕 ENDPOINT PARA MIGRAR LA BASE DE DATOS (Solo en desarrollo)
@app.post("/admin/migrate-usuarios")
async def migrate_usuarios_table(
    current_admin: Usuario = Depends(get_current_admin_user)
):
    """
    Migrar tabla usuarios para agregar nuevos campos (Solo admins)
    """
    try:
        from app.scripts.migrate_usuarios import migrate_usuarios_table
        migrate_usuarios_table()
        return {"message": "Migración de usuarios completada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la migración: {str(e)}"
        )
```

## 🚀 Pasos para Ejecutar la Actualización

### 1. **Ejecutar la migración de base de datos**
```bash
# Opción 1: Ejecutar script directamente
python app/scripts/migrate_usuarios.py

# Opción 2: Usar el endpoint (necesita estar autenticado como admin)
POST /admin/migrate-usuarios
```

### 2. **Reiniciar la aplicación**
```bash
# Detener la aplicación
Ctrl+C

# Reiniciar
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. **Probar los nuevos endpoints**

#### Actualizar perfil de usuario:
```http
PUT /auth/perfil
Content-Type: application/json
Authorization: Bearer {tu_token}

{
  "nombre": "Miguel García",
  "telefono": "+34 123 456 789",
  "ciudad": "Madrid",
  "direccion": "Calle Ejemplo 123, Piso 2A",
  "pais": "España"
}
```

#### Buscar usuarios (admin):
```http
GET /usuarios/?search=Madrid
Authorization: Bearer {admin_token}
```

## ✅ Ventajas de esta Implementación

1. **✅ Compatibilidad**: Los campos son opcionales, no rompe usuarios existentes
2. **✅ Seguridad**: Separación entre actualización de perfil y administración
3. **✅ Búsqueda**: Permite buscar usuarios por los nuevos campos
4. **✅ Flexibilidad**: Los campos son opcionales y pueden actualizarse independientemente
5. **✅ API RESTful**: Endpoints bien estructurados y documentados

## 📝 Notas Importantes

- Los nuevos campos son **opcionales** (nullable=True)
- La migración es **segura** para datos existentes
- Se mantiene la **compatibilidad** con el código actual
- Los usuarios existentes seguirán funcionando sin problemas
- Solo los **administradores** pueden gestionar todos los usuarios
- Los **usuarios normales** solo pueden actualizar su propio perfil