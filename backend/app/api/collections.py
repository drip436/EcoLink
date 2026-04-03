"""
Endpoints de Colecciones/Recogidas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.collection import CollectionCreate, CollectionResponse
from app.crud.collection import create_collection, get_collections, update_collection_status
from app.api.users import get_current_user
from app.utils.security import decode_token

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("/", response_model=CollectionResponse)
def create_new_collection(
    token: str = Query(...),
    collection: Optional[CollectionCreate] = None,
    db: Session = Depends(get_db)
):
    """Crear una nueva colección/recogida"""
    user = get_current_user(token, db)
    new_collection = create_collection(db, user.id, collection)  # type: ignore
    return CollectionResponse.model_validate(new_collection)


@router.get("/my-collections", response_model=list[CollectionResponse])
def get_my_collections(
    token: str = Query(...),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Obtener mis colecciones"""
    user = get_current_user(token, db)
    collections = get_collections(db, user.id, skip, limit)  # type: ignore
    return [CollectionResponse.model_validate(c) for c in collections]


@router.get("/", response_model=list[CollectionResponse])
def list_all_collections(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Listar todas las colecciones (público)"""
    collections = get_collections(db, skip=skip, limit=limit)
    return [CollectionResponse.model_validate(c) for c in collections]


@router.put("/{collection_id}/status/{status}")
def update_status(
    collection_id: int,
    status: str,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Actualizar estado de colección
    Estados: pending, collected, cancelled
    """
    user = get_current_user(token, db)
    collection = update_collection_status(db, collection_id, status)
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Si se marca como collected, agregar puntos al usuario
    if status == "collected":
        from app.services.gamification_service import add_collection_points
        add_collection_points(db, user.id, collection.weight_kg)  # type: ignore
    
    return CollectionResponse.model_validate(collection)
