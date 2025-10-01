from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class TokenRecuperacion(Base):
    __tablename__ = "tokens_recuperacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    usado = Column(Boolean, default=False, index=True)
    fecha_expiracion = Column(DateTime(timezone=True), nullable=False, index=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    ip_solicitante = Column(INET)
    user_agent = Column(Text)

    usuario = relationship("Usuario", backref="tokens_recuperacion")

class Sesion(Base):
    __tablename__ = "sesiones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    token_jwt = Column(Text, nullable=False)
    ip_address = Column(INET)
    user_agent = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_expiracion = Column(DateTime(timezone=True), nullable=False, index=True)
    activa = Column(Boolean, default=True, index=True)

    usuario = relationship("Usuario", backref="sesiones")

class IntentoLogin(Base):
    __tablename__ = "intentos_login"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), index=True)
    ip_address = Column(INET, index=True)
    exitoso = Column(Boolean, default=False, index=True)
    fecha_intento = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_agent = Column(Text)
    mensaje = Column(String(255))