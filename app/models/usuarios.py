from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base

class UserRole(enum.Enum):
    admin = "admin"
    super_admin = "super_admin"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100))
    role = Column(SQLEnum(UserRole), default=UserRole.admin)
    activo = Column(Boolean, default=True, index=True)
    
    # 🆕 NUEVOS CAMPOS DE INFORMACIÓN PERSONAL
    telefono = Column(String(20), nullable=True)      # Teléfono opcional
    ciudad = Column(String(100), nullable=True)       # Ciudad opcional
    direccion = Column(String(500), nullable=True)    # Dirección opcional
    pais = Column(String(100), nullable=True)         # País opcional
    
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    ultimo_login = Column(DateTime(timezone=True), nullable=True)
    intentos_login = Column(Integer, default=0)
    bloqueado_hasta = Column(DateTime(timezone=True), nullable=True)