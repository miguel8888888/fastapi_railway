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
            # Búsqueda general en múltiples campos incluyendo descripción general
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Billete.denominacion.ilike(search_term),
                    Billete.banco_emisor.ilike(search_term),
                    Billete.pick.ilike(search_term),
                    Billete.descripcion_anverso.ilike(search_term),
                    Billete.descripcion_reverso.ilike(search_term),
                    Billete.descripcion_general.ilike(search_term)
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
    """Obtener estadísticas completas de billetes según requerimientos del frontend"""
    total_billetes = db.query(Billete).count()
    total_vendidos = db.query(Billete).filter(Billete.vendido == True).count()
    total_disponibles = total_billetes - total_vendidos
    total_destacados = db.query(Billete).filter(Billete.destacado == True).count()
    
    # Calcular valores monetarios
    billetes_todos = db.query(Billete.precio).all()
    valor_total_inventario = 0.0
    for precio_tuple in billetes_todos:
        try:
            precio_str = precio_tuple[0]
            if precio_str:
                valor_total_inventario += float(precio_str)
        except (ValueError, TypeError):
            continue
    
    billetes_disponibles = db.query(Billete.precio).filter(Billete.vendido == False).all()
    valor_inventario_disponible = 0.0
    for precio_tuple in billetes_disponibles:
        try:
            precio_str = precio_tuple[0]
            if precio_str:
                valor_inventario_disponible += float(precio_str)
        except (ValueError, TypeError):
            continue
    
    # Estadísticas por país (formato requerido por frontend)
    paises_stats = db.query(
        Pais.pais.label('nombre_pais'),
        func.count(Billete.id).label('total'),
        func.sum(func.case((Billete.vendido == True, 1), else_=0)).label('vendidos'),
        func.sum(func.case((Billete.vendido == False, 1), else_=0)).label('disponibles')
    ).join(Billete, Pais.id == Billete.pais).group_by(Pais.pais, Pais.id).all()
    
    estadisticas_por_pais = {}
    for pais_stat in paises_stats:
        # Calcular valor total por país
        valor_pais = db.query(func.sum(
            func.cast(Billete.precio, func.Float)
        )).join(Pais).filter(Pais.pais == pais_stat.nombre_pais).scalar() or 0
        
        estadisticas_por_pais[pais_stat.nombre_pais] = {
            "total": int(pais_stat.total or 0),
            "vendidos": int(pais_stat.vendidos or 0),
            "disponibles": int(pais_stat.disponibles or 0),
            "valor_total": f"{valor_pais:.2f}"
        }
    
    # Estadísticas por estado
    estados_stats = db.query(
        func.coalesce(Billete.estado, 'Sin Estado').label('estado'),
        func.count(Billete.id).label('cantidad')
    ).group_by(Billete.estado).all()
    
    estadisticas_por_estado = {}
    for estado_stat in estados_stats:
        estadisticas_por_estado[estado_stat.estado] = int(estado_stat.cantidad)
    
    # Características más usadas (Top 10)
    caracteristicas_stats = db.query(
        Caracteristica.nombre.label('caracteristica'),
        Caracteristica.nombre.label('nombre'),
        Caracteristica.color.label('color'),
        func.count(billete_caracteristicas.c.billete_id).label('cantidad_billetes')
    ).join(
        billete_caracteristicas, Caracteristica.id == billete_caracteristicas.c.caracteristica_id
    ).group_by(
        Caracteristica.id, Caracteristica.nombre, Caracteristica.color
    ).order_by(
        func.count(billete_caracteristicas.c.billete_id).desc()
    ).limit(10).all()
    
    caracteristicas_mas_usadas = [
        {
            "caracteristica": stat.caracteristica,
            "nombre": stat.nombre,
            "color": stat.color,
            "cantidad_billetes": int(stat.cantidad_billetes)
        }
        for stat in caracteristicas_stats
    ]
    
    return {
        "total_billetes": total_billetes,
        "total_vendidos": total_vendidos,
        "total_disponibles": total_disponibles,
        "total_destacados": total_destacados,
        "valor_total_inventario": f"{valor_total_inventario:.2f}",
        "valor_inventario_disponible": f"{valor_inventario_disponible:.2f}",
        "estadisticas_por_pais": estadisticas_por_pais,
        "estadisticas_por_estado": estadisticas_por_estado,
        "caracteristicas_mas_usadas": caracteristicas_mas_usadas
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

# ==================== FUNCIONES TOGGLE BILLETES ====================

def toggle_billete_destacado(db: Session, billete_id: int, destacado: bool):
    """Cambiar estado destacado de un billete"""
    billete = db.query(Billete).filter(Billete.id == billete_id).first()
    if not billete:
        return None
    
    billete.destacado = destacado
    billete.fecha_actualizacion = func.now()
    
    db.commit()
    db.refresh(billete)
    return billete

def toggle_billete_vendido(db: Session, billete_id: int, vendido: bool):
    """Cambiar estado de venta de un billete"""
    billete = db.query(Billete).filter(Billete.id == billete_id).first()
    if not billete:
        return None
    
    billete.vendido = vendido
    billete.fecha_actualizacion = func.now()
    
    db.commit()
    db.refresh(billete)
    return billete