"""
Modelos de base de datos de EcoLink
"""
from app.models.user import User
from app.models.route import Route
from app.models.recycling_point import RecyclingPoint
from app.models.collection import Collection
from app.models.gamification import UserGamification, Achievement

__all__ = [
    "User",
    "Route",
    "RecyclingPoint",
    "Collection",
    "UserGamification",
    "Achievement",
]
