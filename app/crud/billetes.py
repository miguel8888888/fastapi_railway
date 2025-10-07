from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, text
from typing import Optional, List
from app.models.billetes import Billete, Caracteristica, billete_caracteristicas
from app.models.pais import Pais
from app.schemas.billetes import BilleteCreate, BilleteUpdate, BilleteFilter, CaracteristicaCreate, CaracteristicaUpdate

# ==================== FUNCIONES CRUD BILLETES ====================

def create_billete(db: Session, billete: BilleteCreate):
    """Crear un nuevo billete con características"""
    billete_data = billete.model_dump(exclude={'caracteristicas_ids'})
    db_billete = Billete(**billete_data)
    
    db.add(db_billete)
    db.commit()
    db.refresh(db_billete)
    
    # Asociar características si se proporcionaron
    if billete.caracteristicas_ids:
        caracteristicas = db.query(Caracteristica).filter(
            Caracteristica.id.in_(billete.caracteristicas_ids)
        ).all()
        db_billete.caracteristicas = caracteristicas
        db.commit()
        db.refresh(db_billete)
    
    return db_billete

def get_billetes(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    filters: Optional[BilleteFilter] = None
):
    """Obtener billetes con filtros y paginación"""
    query = db.query(Billete).options(
        joinedload(Billete.pais_rel),
        joinedload(Billete.caracteristicas)
    )
    
    # Aplicar filtros
    if filters:
        if filters.pais_id:
            query = query.filter(Billete.pais == filters.pais_id)
        
        if filters.denominacion:
            query = query.filter(Billete.denominacion.ilike(f"%{filters.denominacion}%"))
        
        if filters.precio_min is not None:
            # Convertir precio a float para comparación
            query = query.filter(func.cast(Billete.precio, "REAL") >= filters.precio_min)
        
        if filters.precio_max is not None:
            query = query.filter(func.cast(Billete.precio, "REAL") <= filters.precio_max)
        
        if filters.estado:
            query = query.filter(Billete.estado == filters.estado)
        
        if filters.vendido is not None:
            query = query.filter(Billete.vendido == filters.vendido)
        
        if filters.destacado is not None:
            query = query.filter(Billete.destacado == filters.destacado)
        
        if filters.pick:
            query = query.filter(Billete.pick.ilike(f"%{filters.pick}%"))
        
        if filters.banco_emisor:
            query = query.filter(Billete.banco_emisor.ilike(f"%{filters.banco_emisor}%"))
        
        if filters.caracteristica_id:
            query = query.join(billete_caracteristicas).filter(
                billete_caracteristicas.c.caracteristica_id == filters.caracteristica_id
            )
        
        if filters.search:
            # Búsqueda general en múltiples campos
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Billete.denominacion.ilike(search_term),
                    Billete.banco_emisor.ilike(search_term),
                    Billete.pick.ilike(search_term),
                    Billete.descripcion_anverso.ilike(search_term),
                    Billete.descripcion_reverso.ilike(search_term)
                )
            )
    
    # Ordenar por destacados primero, luego por fecha de actualización
    query = query.order_by(Billete.destacado.desc(), Billete.fecha_actualizacion.desc())
    
    total = query.count()
    billetes = query.offset(skip).limit(limit).all()
    
    return billetes, total

def get_billete(db: Session, billete_id: int):
    """Obtener un billete por ID con todas sus relaciones"""
    return db.query(Billete).filter(Billete.id == billete_id).options(
        joinedload(Billete.pais_rel),
        joinedload(Billete.caracteristicas)
    ).first()

def update_billete(db: Session, billete_id: int, billete_data: BilleteUpdate):
    """Actualizar un billete existente"""
    billete = db.query(Billete).filter(Billete.id == billete_id).first()
    if not billete:
        return None
    
    # Actualizar campos básicos
    update_data = billete_data.model_dump(exclude_unset=True, exclude={'caracteristicas_ids'})
    for field, value in update_data.items():
        setattr(billete, field, value)
    
    # Actualizar características si se proporcionaron
    if billete_data.caracteristicas_ids is not None:
        caracteristicas = db.query(Caracteristica).filter(
            Caracteristica.id.in_(billete_data.caracteristicas_ids)
        ).all()
        billete.caracteristicas = caracteristicas
    
    db.commit()
    db.refresh(billete)
    return billete

def delete_billete(db: Session, billete_id: int):
    """Eliminar un billete"""
    billete = db.query(Billete).filter(Billete.id == billete_id).first()
    if billete:
        db.delete(billete)
        db.commit()
        return True
    return False

def get_billetes_destacados(db: Session, limit: int = 10):
    """Obtener billetes destacados"""
    return db.query(Billete).filter(Billete.destacado == True).options(
        joinedload(Billete.pais_rel),
        joinedload(Billete.caracteristicas)
    ).limit(limit).all()

def get_billetes_stats(db: Session):
    """Obtener estadísticas de billetes"""
    total_billetes = db.query(Billete).count()
    total_vendidos = db.query(Billete).filter(Billete.vendido == True).count()
    total_disponibles = total_billetes - total_vendidos
    total_destacados = db.query(Billete).filter(Billete.destacado == True).count()
    
    # Calcular valores totales manualmente (SQLite tiene problemas con CAST)
    billetes_precios = db.query(Billete.precio).all()
    valor_total = 0.0
    for precio_tuple in billetes_precios:
        try:
            precio_str = precio_tuple[0]
            if precio_str:
                valor_total += float(precio_str)
        except (ValueError, TypeError):
            continue  # Ignorar precios que no se pueden convertir
    
    billetes_vendidos_precios = db.query(Billete.precio).filter(Billete.vendido == True).all()
    valor_vendidos = 0.0
    for precio_tuple in billetes_vendidos_precios:
        try:
            precio_str = precio_tuple[0]
            if precio_str:
                valor_vendidos += float(precio_str)
        except (ValueError, TypeError):
            continue
    
    # Billetes por país
    billetes_por_pais = db.query(
        Pais.pais.label('pais'),
        func.count(Billete.id).label('cantidad')
    ).join(Billete, Pais.id == Billete.pais).group_by(Pais.pais).all()
    
    # Billetes por estado (usando SQL directo para evitar problemas con NULL)
    billetes_por_estado = db.query(
        func.coalesce(Billete.estado, 'Sin Estado').label('estado'),
        func.count(Billete.id).label('cantidad')
    ).group_by(Billete.estado).all()
    
    return {
        "total_billetes": total_billetes,
        "total_vendidos": total_vendidos,
        "total_disponibles": total_disponibles,
        "total_destacados": total_destacados,
        "valor_total_inventario": valor_total,
        "valor_total_vendidos": valor_vendidos,
        "billetes_por_pais": [{"pais": item.pais, "cantidad": item.cantidad} for item in billetes_por_pais],
        "billetes_por_estado": [{"estado": item.estado, "cantidad": item.cantidad} for item in billetes_por_estado]
    }

# ==================== FUNCIONES CRUD CARACTERÍSTICAS ====================

def create_caracteristica(db: Session, caracteristica: CaracteristicaCreate):
    """Crear una nueva característica"""
    db_caracteristica = Caracteristica(**caracteristica.model_dump())
    db.add(db_caracteristica)
    db.commit()
    db.refresh(db_caracteristica)
    return db_caracteristica

def get_caracteristicas(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None):
    """Obtener todas las características"""
    query = db.query(Caracteristica)
    
    if activo is not None:
        query = query.filter(Caracteristica.activo == activo)
    
    return query.offset(skip).limit(limit).all()

def get_caracteristica(db: Session, caracteristica_id: int):
    """Obtener una característica por ID"""
    return db.query(Caracteristica).filter(Caracteristica.id == caracteristica_id).first()

def update_caracteristica(db: Session, caracteristica_id: int, caracteristica_data: CaracteristicaUpdate):
    """Actualizar una característica"""
    caracteristica = db.query(Caracteristica).filter(Caracteristica.id == caracteristica_id).first()
    if not caracteristica:
        return None
    
    update_data = caracteristica_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(caracteristica, field, value)
    
    db.commit()
    db.refresh(caracteristica)
    return caracteristica

def delete_caracteristica(db: Session, caracteristica_id: int):
    """Eliminar una característica"""
    caracteristica = db.query(Caracteristica).filter(Caracteristica.id == caracteristica_id).first()
    if caracteristica:
        db.delete(caracteristica)
        db.commit()
        return True
    return False
    billete = db.query(Billete).filter(Billete.id == billete_id).first()
    if billete:
        db.delete(billete)
        db.commit()
    return billete