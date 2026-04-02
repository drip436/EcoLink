"""
Modelo de Ruta de Recolección
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import json
from app.database import Base


class RouteStatus(str, enum.Enum):
    """Estados de una ruta"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Route(Base):
    """Modelo de Ruta de Recolección de residuos"""
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    
    # Ubicación
    start_location = Column(String)  # JSON: {"lat": 0, "lng": 0}
    end_location = Column(String)    # JSON: {"lat": 0, "lng": 0}
    
    # Horario
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    
    # Estado
    status = Column(Enum(RouteStatus), default=RouteStatus.PENDING)
    
    # Información
    vehicle_type = Column(String, default="Camión")
    capacity_kg = Column(Integer, default=5000)
    current_weight_kg = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Route(id={self.id}, name={self.name}, status={self.status})>"
