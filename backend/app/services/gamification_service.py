"""
Servicio de gamificación
"""
from sqlalchemy.orm import Session
from app.crud.gamification import increment_collection_count, get_user_ranking


def add_collection_points(db: Session, user_id: int, weight_kg: int) -> dict:
    """
    Agregar puntos al usuario por una colección
    """
    gamification = increment_collection_count(db, user_id, weight_kg)
    
    return {
        "user_id": user_id,
        "total_points": gamification.total_points,
        "level": gamification.level,
        "total_collections": gamification.total_collections,
        "message": f"¡Excelente! Ganaste puntos por reciclar {weight_kg}kg"
    }


def get_user_leaderboard(db: Session, limit: int = 10) -> list[dict]:
    """
    Obtener leaderboard (ranking) de usuarios
    """
    return get_user_ranking(db, limit)
