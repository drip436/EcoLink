"""
Configuración de la aplicación EcoLink
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Aplicación
DEBUG = os.getenv("DEBUG", "True") == "True"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Gamificación
BASE_POINTS_PER_COLLECTION = 10
BASE_POINTS_PER_RECYCLING_POINT = 5
POINTS_PER_LEVEL = 100
