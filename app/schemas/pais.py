from pydantic import BaseModel

class PaisBase(BaseModel):
    pais: str
    bandera: str | None = None

class PaisCreate(PaisBase):
    pass

class Pais(PaisBase):
    id: int

    class Config:
        orm_mode = True
