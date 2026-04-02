"""
Schemas para Puntos de Acopio de Reciclaje
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RecyclingPointCreate(BaseModel):
    """Schema para crear punto de acopio"""
    name: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    address: str
    accepts_cardboard: bool = False
    accepts_plastic: bool = False
    accepts_glass: bool = False
    accepts_metal: bool = False
    accepts_organic: bool = False
    accepts_batteries: bool = False
    accepts_oil: bool = False
    accepts_electronics: bool = False
    opening_time: str = "08:00"
    closing_time: str = "18:00"
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class RecyclingPointUpdate(BaseModel):
    """Schema para actualizar punto de acopio"""
    name: Optional[str] = None
    description: Optional[str] = None
    current_capacity_percent: Optional[int] = None
    is_active: Optional[bool] = None


class RecyclingPointResponse(BaseModel):
    """Schema de respuesta para punto de acopio"""
    id: int
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
    address: str
    current_capacity_percent: int
    is_active: bool
    opening_time: str
    closing_time: str
    accepts_cardboard: bool
    accepts_plastic: bool
    accepts_glass: bool
    accepts_metal: bool
    accepts_organic: bool
    accepts_batteries: bool
    accepts_oil: bool
    accepts_electronics: bool
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @property
    def waste_types(self) -> List[str]:
        """Retorna lista de tipos de residuos"""
        types = []
        if self.accepts_cardboard:
            types.append("Cartón")
        if self.accepts_plastic:
            types.append("Plástico")
        if self.accepts_glass:
            types.append("Vidrio")
        if self.accepts_metal:
            types.append("Metal")
        if self.accepts_organic:
            types.append("Orgánico")
        if self.accepts_batteries:
            types.append("Pilas")
        if self.accepts_oil:
            types.append("Aceite")
        if self.accepts_electronics:
            types.append("Electrónica")
        return types
