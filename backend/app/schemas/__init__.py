"""
Schemas Pydantic para validación
"""
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.schemas.route import RouteCreate, RouteResponse, RouteUpdate, RouteDetailResponse
from app.schemas.recycling_point import (
    RecyclingPointCreate, 
    RecyclingPointResponse, 
    RecyclingPointUpdate
)
from app.schemas.collection import CollectionCreate, CollectionResponse
from app.schemas.gamification import (
    UserGamificationResponse,
    AchievementResponse,
    UserRankingResponse
)

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "RouteCreate",
    "RouteResponse",
    "RouteUpdate",
    "RouteDetailResponse",
    "RecyclingPointCreate",
    "RecyclingPointResponse",
    "RecyclingPointUpdate",
    "CollectionCreate",
    "CollectionResponse",
    "UserGamificationResponse",
    "AchievementResponse",
    "UserRankingResponse",
]
