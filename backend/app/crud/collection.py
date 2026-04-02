"""
CRUD operations para Colecciones
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.collection import Collection, CollectionStatus
from app.schemas.collection import CollectionCreate


def create_collection(db: Session, user_id: int, collection: CollectionCreate) -> Collection:
    """Crear una nueva colección/recogida"""
    db_collection = Collection(
        user_id=user_id,
        waste_type=collection.waste_type,
        weight_kg=collection.weight_kg,
        latitude=collection.latitude,
        longitude=collection.longitude,
        address=collection.address,
        description=collection.description,
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


def get_collections(
    db: Session, user_id: int = None, skip: int = 0, limit: int = 100
) -> list[Collection]:
    """Obtener colecciones"""
    query = db.query(Collection)
    if user_id:
        query = query.filter(Collection.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def update_collection_status(
    db: Session, collection_id: int, status: str
) -> Collection:
    """Actualizar estado de una colección"""
    db_collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not db_collection:
        return None
    
    db_collection.status = status
    if status == CollectionStatus.COLLECTED:
        db_collection.collected_at = datetime.utcnow()
    
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection
