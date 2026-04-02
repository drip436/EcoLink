"""
Servicio de autenticación
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_user_by_email
from app.utils.security import verify_password, hash_password


def register_user(db: Session, user: UserCreate) -> User:
    """Registrar nuevo usuario"""
    # Verificar que no existe
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError(f"Email {user.email} already registered")
    
    # Crear usuario
    new_user = create_user(db, user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Autenticar usuario con email y contraseña"""
    user = get_user_by_email(db, email)
    
    if not user:
        raise ValueError("Invalid email or password")
    
    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")
    
    if not user.is_active:
        raise ValueError("User is not active")
    
    return user
