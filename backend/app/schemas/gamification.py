"""
Schemas para Gamificación
"""
from pydantic import BaseModel
from datetime import datetime


class UserGamificationResponse(BaseModel):
    """Schema de respuesta para stats de gamificación del usuario"""
    id: int
    user_id: int
    total_points: int
    points_this_month: int
    points_this_week: int
    level: int
    experience: int
    total_collections: int
    total_weight_kg: int
    total_recycling_points_visited: int
    current_rank: int

    class Config:
        from_attributes = True


class AchievementResponse(BaseModel):
    """Schema de respuesta para Achievement"""
    id: int
    name: str
    description: str
    icon: str
    criteria: str
    points_reward: int

    class Config:
        from_attributes = True


class UserRankingResponse(BaseModel):
    """Schema de respuesta para ranking de usuarios"""
    rank: int
    user_id: int
    full_name: str
    total_points: int
    level: int
    total_collections: int
