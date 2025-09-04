from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.pais import Pais, PaisCreate
from app.crud.pais import create_pais, get_paises, get_pais, update_pais, delete_pais

router = APIRouter(
    prefix="/paises",
    tags=["Paises"]
)

@router.post("/", response_model=Pais)
def api_create_pais(pais: PaisCreate, db: Session = Depends(get_db)):
    return create_pais(db, pais)

@router.get("/", response_model=list[Pais])
def api_get_paises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_paises(db, skip, limit)

@router.get("/{pais_id}", response_model=Pais)
def api_get_pais(pais_id: int, db: Session = Depends(get_db)):
    pais = get_pais(db, pais_id)
    if not pais:
        raise HTTPException(status_code=404, detail="Pais no encontrado")
    return pais

@router.put("/{pais_id}", response_model=Pais)
def api_update_pais(pais_id: int, pais_data: PaisCreate, db: Session = Depends(get_db)):
    pais = update_pais(db, pais_id, pais_data)
    if not pais:
        raise HTTPException(status_code=404, detail="Pais no encontrado")
    return pais

@router.delete("/{pais_id}", response_model=Pais)
def api_delete_pais(pais_id: int, db: Session = Depends(get_db)):
    pais = delete_pais(db, pais_id)
    if not pais:
        raise HTTPException(status_code=404, detail="Pais no encontrado")
    return pais
