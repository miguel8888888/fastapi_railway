from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Tabla de asociación para la relación many-to-many entre billetes y características
billete_caracteristicas = Table(
    'billete_caracteristicas', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('billete_id', Integer, ForeignKey('billetes.id'), nullable=False),
    Column('caracteristica_id', Integer, ForeignKey('caracteristicas.id'), nullable=False),
    Column('fecha_creacion', DateTime(timezone=True), server_default=func.now())
)

class Billete(Base):
    __tablename__ = "billetes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Campos principales
    pais = Column(Integer, ForeignKey("paises.id"), nullable=False)
    denominacion = Column(String, nullable=False)
    precio = Column(String, nullable=False)
    
    # Nuevos campos agregados en la migración
    banco_emisor = Column(String(255), nullable=True)
    medidas = Column(String(50), nullable=True)
    descripcion_anverso = Column(Text, nullable=True)
    descripcion_reverso = Column(Text, nullable=True)
    url_anverso = Column(Text, nullable=True)
    url_reverso = Column(Text, nullable=True)
    pick = Column(String(50), nullable=True, index=True)
    estado = Column(String(20), nullable=True, default="Bueno")
    vendido = Column(Boolean, default=False, index=True)
    destacado = Column(Boolean, default=False, index=True)
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relaciones
    pais_rel = relationship("Pais", backref="billetes")
    caracteristicas = relationship("Caracteristica", secondary=billete_caracteristicas, back_populates="billetes")

class Caracteristica(Base):
    __tablename__ = "caracteristicas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    color = Column(String(7), nullable=True, default="#007bff")  # Color hexadecimal
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación inversa
    billetes = relationship("Billete", secondary=billete_caracteristicas, back_populates="caracteristicas")