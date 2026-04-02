"""
Schemas para Rutas de Recolección
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RouteCreate(BaseModel):
    """Schema para crear ruta"""
    name: str
    description: Optional[str] = None
    start_location: str  # JSON string
    end_location: str    # JSON string
    scheduled_start: datetime
    scheduled_end: datetime
    vehicle_type: str = "Camión"
    capacity_kg: int = 5000


class RouteUpdate(BaseModel):
    """Schema para actualizar ruta"""
    name: Optional[str] = None
    status: Optional[str] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    current_weight_kg: Optional[int] = None


class RouteResponse(BaseModel):
    """Schema de respuesta para ruta (simple)"""
    id: int
    name: str
    status: str
    scheduled_start: datetime
    scheduled_end: datetime
    current_weight_kg: int
    capacity_kg: int
    vehicle_type: str

    class Config:
        from_attributes = True


class RouteDetailResponse(BaseModel):
    """Schema de respuesta para ruta (detallado)"""
    id: int
    name: str
    description: Optional[str]
    start_location: str
    end_location: str
    status: str
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    current_weight_kg: int
    capacity_kg: int
    vehicle_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
