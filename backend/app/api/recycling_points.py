"""
Endpoints de Puntos de Acopio
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.recycling_point import (
    RecyclingPointCreate,
    RecyclingPointResponse,
    RecyclingPointUpdate,
)
from app.crud.recycling_point import (
    create_recycling_point,
    get_recycling_point,
    get_recycling_points,
    update_recycling_point,
)
from app.api.routes import check_admin
from app.utils.security import decode_token

router = APIRouter(prefix="/recycling-points", tags=["recycling_points"])


@router.post("/", response_model=RecyclingPointResponse)
def create_point(
    point: RecyclingPointCreate,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """Crear nuevo punto de acopio (solo admin)"""
    check_admin(token, db)
    new_point = create_recycling_point(db, point)
    return RecyclingPointResponse.model_validate(new_point)


@router.get("/{point_id}", response_model=RecyclingPointResponse)
def get_point(point_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de punto de acopio"""
    point = get_recycling_point(db, point_id)
    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Point not found")
    return RecyclingPointResponse.model_validate(point)


@router.get("/", response_model=list[RecyclingPointResponse])
def list_points(
    skip: int = 0,
    limit: int = 50,
    waste_type: str = None,
    db: Session = Depends(get_db)
):
    """Listar puntos de acopio activos"""
    points = get_recycling_points(db, skip, limit)
    
    # Filtrar por tipo de residuo si se especifica
    if waste_type:
        waste_type = waste_type.lower()
        points = [
            p for p in points
            if (
                (waste_type == "cardboard" and p.accepts_cardboard) or
                (waste_type == "plastic" and p.accepts_plastic) or
                (waste_type == "glass" and p.accepts_glass) or
                (waste_type == "metal" and p.accepts_metal) or
                (waste_type == "organic" and p.accepts_organic) or
                (waste_type == "batteries" and p.accepts_batteries) or
                (waste_type == "oil" and p.accepts_oil) or
                (waste_type == "electronics" and p.accepts_electronics)
            )
        ]
    
    return [RecyclingPointResponse.model_validate(p) for p in points]


@router.put("/{point_id}", response_model=RecyclingPointResponse)
def update_point(
    point_id: int,
    point_update: RecyclingPointUpdate,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """Actualizar punto de acopio (solo admin)"""
    check_admin(token, db)
    point = get_recycling_point(db, point_id)
    if not point:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Point not found")
    updated_point = update_recycling_point(db, point_id, point_update)
    return RecyclingPointResponse.model_validate(updated_point)
