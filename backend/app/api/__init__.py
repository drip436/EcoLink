"""
Rutas API de EcoLink
"""
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.routes import router as routes_router
from app.api.recycling_points import router as recycling_points_router
from app.api.collections import router as collections_router
from app.api.gamification import router as gamification_router

__all__ = [
    "auth_router",
    "users_router",
    "routes_router",
    "recycling_points_router",
    "collections_router",
    "gamification_router",
]
