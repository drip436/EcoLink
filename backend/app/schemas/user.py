"""
Schemas para Usuario
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema para crear usuario"""
    email: EmailStr
    full_name: str
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None


class UserLogin(BaseModel):
    """Schema para login de usuario"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None


class UserResponse(BaseModel):
    """Schema de respuesta para usuario"""
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    address: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema de respuesta con token JWT"""
    access_token: str
    token_type: str
    user: UserResponse
