"""
Schemas para Colecciones/Recogidas de Residuos
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CollectionCreate(BaseModel):
    """Schema para crear una recogida/colección"""
    waste_type: str  # "cardboard", "plastic", "glass", etc.
    weight_kg: int = 1
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


class CollectionResponse(BaseModel):
    """Schema de respuesta para colección"""
    id: int
    user_id: int
    waste_type: str
    weight_kg: int
    status: str
    address: Optional[str]
    requested_at: datetime
    collected_at: Optional[datetime]

    class Config:
        from_attributes = True
