from pydantic import BaseModel
from typing import Optional

class BilleteBase(BaseModel):
    anverso: str
    reverso: str
    pais: int
    denominacion: str
    precio: str

class BilleteCreate(BilleteBase):
    pass

class BilletePais(BaseModel):
    id: int
    pais: str
    bandera: str

    class Config:
        from_attributes  = True

class Billete(BilleteBase):
    id: int
    pais_rel: Optional[BilletePais] = None

    class Config:
        from_attributes  = True