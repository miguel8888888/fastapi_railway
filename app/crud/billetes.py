from sqlalchemy.orm import Session, joinedload
from app.models.billetes import Billete
from app.schemas.billetes import BilleteCreate

def create_billete(db: Session, billete: BilleteCreate):
    db_billete = Billete(**billete.model_dump())  # Cambia dict() por model_dump()
    db.add(db_billete)
    db.commit()
    db.refresh(db_billete)
    return db_billete

def get_billetes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Billete).options(joinedload(Billete.pais_rel)).offset(skip).limit(limit).all()

def get_billete(db: Session, billete_id: int):
    return db.query(Billete).options(joinedload(Billete.pais_rel)).filter(Billete.id == billete_id).first()

def update_billete(db: Session, billete_id: int, billete_data: BilleteCreate):
    billete = db.query(Billete).filter(Billete.id == billete_id).first()
    if billete:
        billete.anverso = billete_data.anverso
        billete.reverso = billete_data.reverso
        billete.pais = billete_data.pais
        billete.denominacion = billete_data.denominacion  # Faltaba esta línea
        billete.precio = billete_data.precio  # Faltaba esta línea
        db.commit()
        db.refresh(billete)
    return billete

def delete_billete(db: Session, billete_id: int):
    billete = db.query(Billete).filter(Billete.id == billete_id).first()
    if billete:
        db.delete(billete)
        db.commit()
    return billete