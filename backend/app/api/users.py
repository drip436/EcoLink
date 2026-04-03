"""
Endpoints de Usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.crud.user import get_user, get_users, update_user
from app.utils.security import decode_token

router = APIRouter(prefix="/users", tags=["users"])


def get_current_user(token: str, db: Session = Depends(get_db)):
    """Dependencia para obtener usuario actual del token"""
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = get_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/me", response_model=UserResponse)
def get_me(token: str, db: Session = Depends(get_db)):
    """Obtener perfil del usuario actual"""
    user = get_current_user(token, db)
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Obtener usuario por ID"""
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.model_validate(user)


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Listar todos los usuarios"""
    users = get_users(db, skip, limit)
    return [UserResponse.model_validate(u) for u in users]


@router.put("/me", response_model=UserResponse)
def update_me(token: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Actualizar perfil del usuario actual"""
    current_user = get_current_user(token, db)
    updated_user = update_user(db, current_user.id, user_update)  # type: ignore
    return UserResponse.model_validate(updated_user)
