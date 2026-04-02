"""
CRUD operations para Rutas
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.route import Route
from app.schemas.route import RouteCreate, RouteUpdate


def create_route(db: Session, route: RouteCreate) -> Route:
    """Crear una nueva ruta"""
    db_route = Route(
        name=route.name,
        description=route.description,
        start_location=route.start_location,
        end_location=route.end_location,
        scheduled_start=route.scheduled_start,
        scheduled_end=route.scheduled_end,
        vehicle_type=route.vehicle_type,
        capacity_kg=route.capacity_kg,
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


def get_route(db: Session, route_id: int) -> Route:
    """Obtener ruta por ID"""
    return db.query(Route).filter(Route.id == route_id).first()


def get_routes(db: Session, skip: int = 0, limit: int = 100) -> list[Route]:
    """Obtener rutas activas"""
    return db.query(Route).filter(Route.is_active == True).offset(skip).limit(limit).all()


def update_route(db: Session, route_id: int, route: RouteUpdate) -> Route:
    """Actualizar ruta"""
    db_route = get_route(db, route_id)
    if not db_route:
        return None
    
    update_data = route.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_route, field, value)
    
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route
