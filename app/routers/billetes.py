from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.schemas.billetes import (
    Billete, BilleteCreate, BilleteUpdate, BilleteFilter, BilleteListResponse, BilleteStatsResponse,
    Caracteristica, CaracteristicaCreate, CaracteristicaUpdate, EstadoBillete,
    BilleteDestacadoToggle, BilleteVendidoToggle, BilleteToggleResponse
)
from app.crud.billetes import (
    create_billete, get_billetes, get_billete, update_billete, delete_billete,
    get_billetes_destacados, get_billetes_stats,
    create_caracteristica, get_caracteristicas, get_caracteristica, update_caracteristica, delete_caracteristica
)
from app.utils.auth_dependencies import get_current_user
from app.models.usuarios import Usuario
import math

router = APIRouter(
    prefix="/billetes",
    tags=["Billetes"]
)

# ==================== ENDPOINTS BILLETES ====================

@router.post("/", response_model=Billete)
def api_create_billete(
    billete: BilleteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear un nuevo billete (requiere autenticación)"""
    return create_billete(db, billete)

@router.get("/", response_model=BilleteListResponse)
def api_get_billetes(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Elementos por página"),
    pais_id: Optional[int] = Query(None, description="Filtrar por país"),
    denominacion: Optional[str] = Query(None, description="Filtrar por denominación"),
    precio_min: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    estado: Optional[EstadoBillete] = Query(None, description="Filtrar por estado"),
    vendido: Optional[bool] = Query(None, description="Filtrar por vendido"),
    destacado: Optional[bool] = Query(None, description="Filtrar por destacado"),
    pick: Optional[str] = Query(None, description="Filtrar por número Pick"),
    banco_emisor: Optional[str] = Query(None, description="Filtrar por banco emisor"),
    caracteristica_id: Optional[int] = Query(None, description="Filtrar por característica"),
    search: Optional[str] = Query(None, description="Búsqueda general"),
    db: Session = Depends(get_db)
):
    """Obtener billetes con filtros y paginación"""
    filters = BilleteFilter(
        pais_id=pais_id,
        denominacion=denominacion,
        precio_min=precio_min,
        precio_max=precio_max,
        estado=estado,
        vendido=vendido,
        destacado=destacado,
        pick=pick,
        banco_emisor=banco_emisor,
        caracteristica_id=caracteristica_id,
        search=search
    )
    
    skip = (page - 1) * per_page
    billetes, total = get_billetes(db, skip=skip, limit=per_page, filters=filters)
    
    total_pages = math.ceil(total / per_page)
    
    return BilleteListResponse(
        billetes=billetes,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/destacados", response_model=List[Billete])
def api_get_billetes_destacados(
    limit: int = Query(10, ge=1, le=50, description="Número de billetes destacados"),
    db: Session = Depends(get_db)
):
    """Obtener billetes destacados"""
    return get_billetes_destacados(db, limit)

@router.get("/estadisticas", response_model=BilleteStatsResponse)
def api_get_billetes_stats(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener estadísticas de billetes (requiere autenticación)"""
    return get_billetes_stats(db)

@router.get("/stats")
def api_get_billetes_stats_public(db: Session = Depends(get_db)):
    """Obtener estadísticas de billetes (público, para frontend)"""
    return get_billetes_stats(db)

@router.get("/{billete_id}", response_model=Billete)
def api_get_billete(billete_id: int, db: Session = Depends(get_db)):
    """Obtener un billete específico"""
    billete = get_billete(db, billete_id)
    if not billete:
        raise HTTPException(status_code=404, detail="Billete no encontrado")
    return billete

@router.put("/{billete_id}", response_model=Billete)
def api_update_billete(
    billete_id: int, 
    billete_data: BilleteUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar un billete (requiere autenticación)"""
    billete = update_billete(db, billete_id, billete_data)
    if not billete:
        raise HTTPException(status_code=404, detail="Billete no encontrado")
    return billete

@router.delete("/{billete_id}")
def api_delete_billete(
    billete_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar un billete (requiere autenticación)"""
    success = delete_billete(db, billete_id)
    if not success:
        raise HTTPException(status_code=404, detail="Billete no encontrado")
    return {"message": "Billete eliminado exitosamente"}

@router.patch("/{billete_id}/destacado", response_model=BilleteToggleResponse)
def api_toggle_billete_destacado(
    billete_id: int,
    toggle_data: BilleteDestacadoToggle,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Marcar/desmarcar billete como destacado (requiere autenticación)"""
    from app.crud.billetes import toggle_billete_destacado
    
    billete = toggle_billete_destacado(db, billete_id, toggle_data.destacado)
    if not billete:
        raise HTTPException(status_code=404, detail=f"Billete con ID {billete_id} no encontrado")
    
    mensaje = "Billete marcado como destacado" if toggle_data.destacado else "Billete desmarcado como destacado"
    
    return BilleteToggleResponse(
        id=billete.id,
        destacado=billete.destacado,
        mensaje=f"{mensaje} exitosamente",
        fecha_actualizacion=billete.fecha_actualizacion
    )

@router.patch("/{billete_id}/vendido", response_model=BilleteToggleResponse)
def api_toggle_billete_vendido(
    billete_id: int,
    toggle_data: BilleteVendidoToggle,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Marcar/desmarcar billete como vendido (requiere autenticación)"""
    from app.crud.billetes import toggle_billete_vendido
    
    billete = toggle_billete_vendido(db, billete_id, toggle_data.vendido)
    if not billete:
        raise HTTPException(status_code=404, detail=f"Billete con ID {billete_id} no encontrado")
    
    mensaje = "Billete marcado como vendido" if toggle_data.vendido else "Billete marcado como disponible"
    
    return BilleteToggleResponse(
        id=billete.id,
        vendido=billete.vendido,
        mensaje=f"{mensaje} exitosamente",
        fecha_actualizacion=billete.fecha_actualizacion
    )

# ==================== ENDPOINTS CARACTERÍSTICAS ====================

@router.post("/caracteristicas", response_model=Caracteristica)
def api_create_caracteristica(
    caracteristica: CaracteristicaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crear una nueva característica (requiere autenticación)"""
    return create_caracteristica(db, caracteristica)

@router.get("/caracteristicas", response_model=List[Caracteristica])
def api_get_caracteristicas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    activo: Optional[bool] = Query(None, description="Filtrar por características activas"),
    db: Session = Depends(get_db)
):
    """Obtener todas las características"""
    return get_caracteristicas(db, skip=skip, limit=limit, activo=activo)

@router.get("/caracteristicas/{caracteristica_id}", response_model=Caracteristica)
def api_get_caracteristica(caracteristica_id: int, db: Session = Depends(get_db)):
    """Obtener una característica específica"""
    caracteristica = get_caracteristica(db, caracteristica_id)
    if not caracteristica:
        raise HTTPException(status_code=404, detail="Característica no encontrada")
    return caracteristica

@router.put("/caracteristicas/{caracteristica_id}", response_model=Caracteristica)
def api_update_caracteristica(
    caracteristica_id: int,
    caracteristica_data: CaracteristicaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar una característica (requiere autenticación)"""
    caracteristica = update_caracteristica(db, caracteristica_id, caracteristica_data)
    if not caracteristica:
        raise HTTPException(status_code=404, detail="Característica no encontrada")
    return caracteristica

@router.delete("/caracteristicas/{caracteristica_id}")
def api_delete_caracteristica(
    caracteristica_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Eliminar una característica (requiere autenticación)"""
    success = delete_caracteristica(db, caracteristica_id)
    if not success:
        raise HTTPException(status_code=404, detail="Característica no encontrada")
    return {"message": "Característica eliminada exitosamente"}