"""
CRUD operations
"""
from app.crud.user import create_user, get_user, get_user_by_email, update_user, get_users
from app.crud.route import create_route, get_route, get_routes, update_route
from app.crud.recycling_point import (
    create_recycling_point,
    get_recycling_point,
    get_recycling_points,
    update_recycling_point,
)
from app.crud.collection import create_collection, get_collections, update_collection_status
from app.crud.gamification import (
    get_or_create_user_gamification,
    update_user_points,
    get_user_ranking,
)

__all__ = [
    "create_user",
    "get_user",
    "get_user_by_email",
    "update_user",
    "get_users",
    "create_route",
    "get_route",
    "get_routes",
    "update_route",
    "create_recycling_point",
    "get_recycling_point",
    "get_recycling_points",
    "update_recycling_point",
    "create_collection",
    "get_collections",
    "update_collection_status",
    "get_or_create_user_gamification",
    "update_user_points",
    "get_user_ranking",
]
