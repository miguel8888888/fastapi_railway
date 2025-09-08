from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.billetes import Billete, BilleteCreate
from app.crud.billetes import create_billete, get_billetes, get_billete, update_billete, delete_billete

router = APIRouter(
    prefix="/billetes",
    tags=["Billetes"]
)

@router.post("/", response_model=Billete)
def api_create_billete(billete: BilleteCreate, db: Session = Depends(get_db)):
    return create_billete(db, billete)

@router.get("/", response_model=list[Billete])
def api_get_billetes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_billetes(db, skip, limit)

@router.get("/{billete_id}", response_model=Billete)
def api_get_billete(billete_id: int, db: Session = Depends(get_db)):
    billete = get_billete(db, billete_id)
    if not billete:
        raise HTTPException(status_code=404, detail="Billete no encontrado")
    return billete

@router.put("/{billete_id}", response_model=Billete)
def api_update_billete(billete_id: int, billete_data: BilleteCreate, db: Session = Depends(get_db)):
    billete = update_billete(db, billete_id, billete_data)
    if not billete:
        raise HTTPException(status_code=404, detail="Billete no encontrado")
    return billete

@router.delete("/{billete_id}", response_model=Billete)
def api_delete_billete(billete_id: int, db: Session = Depends(get_db)):
    billete = delete_billete(db, billete_id)
    if not billete:
        raise HTTPException(status_code=404, detail="Billete no encontrado")
    return billete