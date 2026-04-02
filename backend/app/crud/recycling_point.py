"""
CRUD operations para Puntos de Acopio
"""
from sqlalchemy.orm import Session
from app.models.recycling_point import RecyclingPoint
from app.schemas.recycling_point import RecyclingPointCreate, RecyclingPointUpdate


def create_recycling_point(db: Session, point: RecyclingPointCreate) -> RecyclingPoint:
    """Crear un nuevo punto de acopio"""
    db_point = RecyclingPoint(
        name=point.name,
        description=point.description,
        latitude=point.latitude,
        longitude=point.longitude,
        address=point.address,
        accepts_cardboard=point.accepts_cardboard,
        accepts_plastic=point.accepts_plastic,
        accepts_glass=point.accepts_glass,
        accepts_metal=point.accepts_metal,
        accepts_organic=point.accepts_organic,
        accepts_batteries=point.accepts_batteries,
        accepts_oil=point.accepts_oil,
        accepts_electronics=point.accepts_electronics,
        opening_time=point.opening_time,
        closing_time=point.closing_time,
        contact_name=point.contact_name,
        contact_phone=point.contact_phone,
        contact_email=point.contact_email,
    )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


def get_recycling_point(db: Session, point_id: int) -> RecyclingPoint:
    """Obtener punto de acopio por ID"""
    return db.query(RecyclingPoint).filter(RecyclingPoint.id == point_id).first()


def get_recycling_points(
    db: Session, skip: int = 0, limit: int = 100, is_active: bool = True
) -> list[RecyclingPoint]:
    """Obtener lista de puntos de acopio"""
    query = db.query(RecyclingPoint)
    if is_active:
        query = query.filter(RecyclingPoint.is_active == True)
    return query.offset(skip).limit(limit).all()


def update_recycling_point(
    db: Session, point_id: int, point: RecyclingPointUpdate
) -> RecyclingPoint:
    """Actualizar punto de acopio"""
    db_point = get_recycling_point(db, point_id)
    if not db_point:
        return None
    
    update_data = point.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_point, field, value)
    
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point
