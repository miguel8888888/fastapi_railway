from pydantic import BaseModel
from typing import Optional

class BilleteBase(BaseModel):
    anverso: str
    reverso: str
    pais: int

class BilleteCreate(BilleteBase):
    pass

class BilletePais(BaseModel):
    id: int
    pais: str
    bandera: str

    class Config:
        orm_mode = True

class Billete(BilleteBase):
    id: int
    pais_rel: Optional[BilletePais] = None

    class Config:
        orm_mode = True