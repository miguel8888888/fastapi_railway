from sqlalchemy.orm import Session
from app.models.pais import Pais
from app.schemas.pais import PaisCreate

# Crear un nuevo país
def create_pais(db: Session, pais: PaisCreate):
    db_pais = Pais(pais=pais.pais, bandera=pais.bandera)
    db.add(db_pais)
    db.commit()
    db.refresh(db_pais)
    return db_pais

# Obtener todos los países
def get_paises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pais).offset(skip).limit(limit).all()

# Obtener un país por id
def get_pais(db: Session, pais_id: int):
    return db.query(Pais).filter(Pais.id == pais_id).first()

# Actualizar un país
def update_pais(db: Session, pais_id: int, pais_data: PaisCreate):
    pais = db.query(Pais).filter(Pais.id == pais_id).first()
    if pais:
        pais.pais = pais_data.pais
        pais.bandera = pais_data.bandera
        db.commit()
        db.refresh(pais)
    return pais

# Eliminar un país
def delete_pais(db: Session, pais_id: int):
    pais = db.query(Pais).filter(Pais.id == pais_id).first()
    if pais:
        db.delete(pais)
        db.commit()
    return pais
