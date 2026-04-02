"""
Endpoints de Rutas de Recolección
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.route import RouteCreate, RouteResponse, RouteUpdate, RouteDetailResponse
from app.crud.route import create_route, get_route, get_routes, update_route
from app.models.user import UserRole
from app.api.users import get_current_user
from app.utils.security import decode_token

router = APIRouter(prefix="/routes", tags=["routes"])


def check_admin(token: str, db: Session = Depends(get_db)):
    """Verificar que el usuario sea admin"""
    from app.crud.user import get_user
    payload = decode_token(token)
    user_id = int(payload.get("sub"))
    user = get_user(db, user_id)
    if not user or user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


@router.post("/", response_model=RouteDetailResponse)
def create_collection_route(
    route: RouteCreate,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """Crear nueva ruta de recolección (solo admin)"""
    check_admin(token, db)
    new_route = create_route(db, route)
    return RouteDetailResponse.model_validate(new_route)


@router.get("/{route_id}", response_model=RouteDetailResponse)
def get_collection_route(route_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de una ruta"""
    route = get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return RouteDetailResponse.model_validate(route)


@router.get("/", response_model=list[RouteResponse])
def list_routes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Listar rutas activas"""
    routes = get_routes(db, skip, limit)
    return [RouteResponse.model_validate(r) for r in routes]


@router.put("/{route_id}", response_model=RouteDetailResponse)
def update_collection_route(
    route_id: int,
    route_update: RouteUpdate,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """Actualizar ruta (solo admin)"""
    check_admin(token, db)
    route = get_route(db, route_id)
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    updated_route = update_route(db, route_id, route_update)
    return RouteDetailResponse.model_validate(updated_route)
