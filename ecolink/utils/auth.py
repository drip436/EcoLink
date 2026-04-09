"""
ecolink/utils/auth.py
═══════════════════════════════════════════════════════════════════════════════
Utilidades de autenticación:
  - Hash de contraseñas con bcrypt (via passlib)
  - Tokens de sesión simples firmados con HMAC-SHA256
    (En Reflex "todo en uno" no necesitamos JWT completo:
     el estado del servidor vive en memoria y la sesión
     se gestiona por WebSocket. El token solo se usa para
     persistir el usuario_id en rx.LocalStorage.)
═══════════════════════════════════════════════════════════════════════════════
"""

import hashlib
import hmac
import os
import secrets
from passlib.context import CryptContext

# ── Configuración de bcrypt ────────────────────────────────────────────────
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta para firmar tokens de sesión.
# En producción lee de variable de entorno.
SECRET_KEY = os.getenv("ECOLINK_SECRET", "ecolink-innovatec-secret-2025")


def hash_password(plain: str) -> str:
    """Devuelve el hash bcrypt de la contraseña."""
    return pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica contraseña contra su hash."""
    return pwd_ctx.verify(plain, hashed)


def make_session_token(user_id: int) -> str:
    """
    Genera un token de sesión: '{user_id}:{random}:{hmac}'.
    El frontend lo guarda en localStorage para sobrevivir recargas.
    """
    nonce = secrets.token_hex(16)
    payload = f"{user_id}:{nonce}"
    sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def verify_session_token(token: str) -> int | None:
    """
    Verifica el token y devuelve el user_id si es válido, o None.
    """
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        user_id_str, nonce, sig = parts
        payload = f"{user_id_str}:{nonce}"
        expected = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, sig):
            return None
        return int(user_id_str)
    except Exception:
        return None


def generate_claim_code() -> str:
    """Código único para un canje de recompensa."""
    return secrets.token_hex(4).upper()
