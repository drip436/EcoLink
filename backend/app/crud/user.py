"""
CRUD operations para Usuario
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import hash_password


def create_user(db: Session, user: UserCreate) -> User:
    """Crear un nuevo usuario"""
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        phone=user.phone,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Crear registro de gamificación automáticamente
    from app.crud.gamification import get_or_create_user_gamification
    get_or_create_user_gamification(db, db_user.id)
    
    return db_user


def get_user(db: Session, user_id: int) -> User:
    """Obtener usuario por ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    """Obtener usuario por email"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Obtener lista de usuarios"""
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    """Actualizar usuario"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
