"""
CRUD operations para Gamificación
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.gamification import UserGamification
from app.models.user import User
from app.config import BASE_POINTS_PER_COLLECTION, POINTS_PER_LEVEL


def get_or_create_user_gamification(db: Session, user_id: int) -> UserGamification:
    """Obtener o crear registro de gamificación del usuario"""
    gamification = db.query(UserGamification).filter(
        UserGamification.user_id == user_id
    ).first()
    
    if not gamification:
        gamification = UserGamification(user_id=user_id)
        db.add(gamification)
        db.commit()
        db.refresh(gamification)
    
    return gamification


def update_user_points(db: Session, user_id: int, points: int) -> UserGamification:
    """Actualizar puntos del usuario y calcular nivel"""
    gamification = get_or_create_user_gamification(db, user_id)
    
    # Actualizar valores de forma segura con SQLAlchemy
    new_total_points = (gamification.total_points or 0) + points
    new_points_month = (gamification.points_this_month or 0) + points
    new_points_week = (gamification.points_this_week or 0) + points
    new_experience = (gamification.experience or 0) + points
    new_level = (new_experience // POINTS_PER_LEVEL) + 1
    
    gamification.total_points = new_total_points  # type: ignore
    gamification.points_this_month = new_points_month  # type: ignore
    gamification.points_this_week = new_points_week  # type: ignore
    gamification.experience = new_experience  # type: ignore
    gamification.level = new_level  # type: ignore
    
    db.add(gamification)
    db.commit()
    db.refresh(gamification)
    
    return gamification


def increment_collection_count(db: Session, user_id: int, weight_kg: int) -> UserGamification:
    """Incrementar contador de colecciones del usuario"""
    gamification = get_or_create_user_gamification(db, user_id)
    
    gamification.total_collections = (gamification.total_collections or 0) + 1  # type: ignore
    gamification.total_weight_kg = (gamification.total_weight_kg or 0) + weight_kg  # type: ignore
    
    # Le damos puntos por la colección
    points = BASE_POINTS_PER_COLLECTION * (weight_kg // 5 + 1)  # Más peso = más puntos
    update_user_points(db, user_id, points)
    
    db.add(gamification)
    db.commit()
    db.refresh(gamification)
    
    return gamification


def get_user_ranking(db: Session, limit: int = 10) -> list[dict]:
    """Obtener ranking de usuarios por puntos"""
    results = (
        db.query(
            UserGamification.user_id,
            User.full_name,
            UserGamification.total_points,
            UserGamification.level,
            UserGamification.total_collections,
        )
        .join(User, UserGamification.user_id == User.id)
        .order_by(desc(UserGamification.total_points))
        .limit(limit)
        .all()
    )
    
    ranking = []
    for rank, result in enumerate(results, 1):
        ranking.append({
            "rank": rank,
            "user_id": result[0],
            "full_name": result[1],
            "total_points": result[2],
            "level": result[3],
            "total_collections": result[4],
        })
    
    return ranking
