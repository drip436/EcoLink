"""
Modelo de Recogida/Colección de Residuos
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class CollectionStatus(str, enum.Enum):
    """Estados de una recogida"""
    PENDING = "pending"
    COLLECTED = "collected"
    CANCELLED = "cancelled"


class Collection(Base):
    """Modelo de una colección/recogida de residuos por un ciudadano"""
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Tipo de residuo
    waste_type = Column(String)  # "cardboard", "plastic", "glass", etc.
    
    # Cantidad (kg aproximados)
    weight_kg = Column(Integer, default=1)
    
    # Ubicación (del ciudadano)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    # Estado
    status = Column(Enum(CollectionStatus), default=CollectionStatus.PENDING)
    description = Column(String, nullable=True)
    
    # Timestamps
    requested_at = Column(DateTime, default=datetime.utcnow)
    collected_at = Column(DateTime, nullable=True)
    
    # Relación
    user = relationship("User", back_populates="collections")

    def __repr__(self):
        return f"<Collection(id={self.id}, user_id={self.user_id}, waste_type={self.waste_type}, status={self.status})>"
