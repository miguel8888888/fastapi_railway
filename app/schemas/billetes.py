from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EstadoBillete(str, Enum):
    EXCELENTE = "Excelente"
    BUENO = "Bueno" 
    REGULAR = "Regular"
    MALO = "Malo"

class CaracteristicaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    color: Optional[str] = Field(default="#007bff", pattern=r"^#[0-9A-Fa-f]{6}$")
    activo: bool = True

class CaracteristicaCreate(CaracteristicaBase):
    pass

class CaracteristicaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    activo: Optional[bool] = None

class Caracteristica(CaracteristicaBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class BilleteBase(BaseModel):
    pais: int
    denominacion: str = Field(..., min_length=1, max_length=100)
    precio: str = Field(..., min_length=1, max_length=50)
    
    # Campos de contenido
    banco_emisor: Optional[str] = Field(None, max_length=255)
    medidas: Optional[str] = Field(None, max_length=50)
    descripcion_anverso: Optional[str] = None
    descripcion_reverso: Optional[str] = None
    url_anverso: Optional[str] = None
    url_reverso: Optional[str] = None
    pick: Optional[str] = Field(None, max_length=50)
    estado: Optional[EstadoBillete] = EstadoBillete.BUENO
    vendido: bool = False
    destacado: bool = False

class BilleteCreate(BilleteBase):
    caracteristicas_ids: Optional[List[int]] = []

class BilleteUpdate(BaseModel):
    pais: Optional[int] = None
    denominacion: Optional[str] = Field(None, min_length=1, max_length=100)
    precio: Optional[str] = Field(None, min_length=1, max_length=50)
    banco_emisor: Optional[str] = Field(None, max_length=255)
    medidas: Optional[str] = Field(None, max_length=50)
    descripcion_anverso: Optional[str] = None
    descripcion_reverso: Optional[str] = None
    url_anverso: Optional[str] = None
    url_reverso: Optional[str] = None
    pick: Optional[str] = Field(None, max_length=50)
    estado: Optional[EstadoBillete] = None
    vendido: Optional[bool] = None
    destacado: Optional[bool] = None
    caracteristicas_ids: Optional[List[int]] = None

class BilletePais(BaseModel):
    id: int
    pais: str
    bandera: str

    class Config:
        from_attributes = True

class Billete(BilleteBase):
    id: int
    fecha_actualizacion: datetime
    caracteristicas: List[Caracteristica] = []
    pais_rel: Optional[BilletePais] = None
    
    class Config:
        from_attributes = True

# Schemas para consultas con filtros y paginación
class BilleteFilter(BaseModel):
    pais_id: Optional[int] = None
    denominacion: Optional[str] = None
    precio_min: Optional[float] = None
    precio_max: Optional[float] = None
    estado: Optional[EstadoBillete] = None
    vendido: Optional[bool] = None
    destacado: Optional[bool] = None
    pick: Optional[str] = None
    banco_emisor: Optional[str] = None
    caracteristica_id: Optional[int] = None
    search: Optional[str] = None  # Búsqueda general

class BilleteListResponse(BaseModel):
    billetes: List[Billete]
    total: int
    page: int
    per_page: int
    total_pages: int

class BilleteStatsResponse(BaseModel):
    total_billetes: int
    total_vendidos: int
    total_disponibles: int
    total_destacados: int
    valor_total_inventario: float
    valor_total_vendidos: float
    billetes_por_pais: List[dict]
    billetes_por_estado: List[dict]

class Billete(BilleteBase):
    id: int
    pais_rel: Optional[BilletePais] = None

    class Config:
        from_attributes  = True