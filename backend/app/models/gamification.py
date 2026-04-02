"""
Modelo de Gamificación
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class UserGamification(Base):
    """Modelo de estadísticas de gamificación de usuario"""
    __tablename__ = "user_gamification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Puntos
    total_points = Column(Integer, default=0)
    points_this_month = Column(Integer, default=0)
    points_this_week = Column(Integer, default=0)
    
    # Nivel y progreso
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    
    # Estadísticas
    total_collections = Column(Integer, default=0)
    total_weight_kg = Column(Integer, default=0)
    total_recycling_points_visited = Column(Integer, default=0)
    
    # Rankings
    current_rank = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación
    user = relationship("User", back_populates="gamification")

    def __repr__(self):
        return f"<UserGamification(user_id={self.user_id}, level={self.level}, points={self.total_points})>"


class Achievement(Base):
    """Modelo de logros/Achievement del usuario"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    icon = Column(String)  # URL o nombre de icono
    criteria = Column(String)  # Descripción de cómo desbloquearlo
    points_reward = Column(Integer, default=50)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Achievement(id={self.id}, name={self.name})>"
