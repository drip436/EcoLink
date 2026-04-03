"""
Endpoints de Gamificación
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.gamification import (
    UserGamificationResponse,
    UserRankingResponse,
)
from app.crud.gamification import get_or_create_user_gamification, get_user_ranking
from app.api.users import get_current_user
from app.services.gamification_service import get_user_leaderboard
from app.utils.security import decode_token

router = APIRouter(prefix="/gamification", tags=["gamification"])


@router.get("/my-stats", response_model=UserGamificationResponse)
def get_my_stats(
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """Obtener mis estadísticas de gamificación"""
    user = get_current_user(token, db)
    gamification = get_or_create_user_gamification(db, user.id)  # type: ignore
    return UserGamificationResponse.model_validate(gamification)


@router.get("/stats/{user_id}", response_model=UserGamificationResponse)
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """Obtener estadísticas de gamificación de un usuario"""
    gamification = get_or_create_user_gamification(db, user_id)
    return UserGamificationResponse.model_validate(gamification)


@router.get("/leaderboard", response_model=list[UserRankingResponse])
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Obtener leaderboard (top usuarios por puntos)"""
    ranking = get_user_leaderboard(db, limit)
    return ranking


@router.get("/leaderboard-month", response_model=list[UserRankingResponse])
def get_leaderboard_month(limit: int = 10, db: Session = Depends(get_db)):
    """Obtener leaderboard del mes"""
    # Esta es una versión simplificada. En producción,
    # se debería usar una query más sofisticada
    ranking = get_user_leaderboard(db, limit)
    return ranking


@router.get("/level/{user_id}")
def get_user_level(user_id: int, db: Session = Depends(get_db)):
    """Obtener nivel del usuario"""
    gamification = get_or_create_user_gamification(db, user_id)
    return {
        "user_id": user_id,
        "level": gamification.level,
        "experience": gamification.experience,
        "total_points": gamification.total_points,
    }
