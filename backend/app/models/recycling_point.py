"""
Modelo de Punto de Acopio de Reciclaje
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from datetime import datetime
from app.database import Base


class RecyclingPoint(Base):
    """Modelo de Punto de Acopio de Reciclaje"""
    __tablename__ = "recycling_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    
    # Ubicación
    latitude = Column(Float)
    longitude = Column(Float)
    address = Column(String)
    
    # Tipos de residuos que acepta
    accepts_cardboard = Column(Boolean, default=False)
    accepts_plastic = Column(Boolean, default=False)
    accepts_glass = Column(Boolean, default=False)
    accepts_metal = Column(Boolean, default=False)
    accepts_organic = Column(Boolean, default=False)
    accepts_batteries = Column(Boolean, default=False)
    accepts_oil = Column(Boolean, default=False)
    accepts_electronics = Column(Boolean, default=False)
    
    # Capacidad y estado
    current_capacity_percent = Column(Integer, default=0)  # 0-100
    is_active = Column(Boolean, default=True)
    
    # Horarios
    opening_time = Column(String, default="08:00")  # HH:MM
    closing_time = Column(String, default="18:00")  # HH:MM
    
    # Información del responsable
    contact_name = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<RecyclingPoint(id={self.id}, name={self.name})>"

    def get_waste_types(self):
        """Retorna lista de tipos de residuos que acepta"""
        waste_types = []
        if self.accepts_cardboard is True:
            waste_types.append("Cartón")
        if self.accepts_plastic is True:
            waste_types.append("Plástico")
        if self.accepts_glass is True:
            waste_types.append("Vidrio")
        if self.accepts_metal is True:
            waste_types.append("Metal")
        if self.accepts_organic is True:
            waste_types.append("Orgánico")
        if self.accepts_batteries is True:
            waste_types.append("Pilas")
        if self.accepts_oil is True:
            waste_types.append("Aceite")
        if self.accepts_electronics is True:
            waste_types.append("Electrónica")
        return waste_types
