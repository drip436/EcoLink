"""
Modelo de Usuario
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    """Roles de usuario"""
    CITIZEN = "citizen"
    ADMIN = "admin"
    RECYCLER = "recycler"


class User(Base):
    """Modelo de Usuario de EcoLink"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(String, nullable=True)  # Para mapas
    longitude = Column(String, nullable=True)
    
    # Rol del usuario
    role = Column(Enum(UserRole), default=UserRole.CITIZEN)
    
    # Estado
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    collections = relationship("Collection", back_populates="user")
    gamification = relationship("UserGamification", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
