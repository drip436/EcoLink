"""
Aplicación Principal FastAPI - EcoLink
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import (
    auth_router,
    users_router,
    routes_router,
    recycling_points_router,
    collections_router,
    gamification_router,
)
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="EcoLink API",
    description="API para gestión circular de residuos",
    version="1.0.0",
)

# Configurar CORS para permitir solicitudes del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(routes_router)
app.include_router(recycling_points_router)
app.include_router(collections_router)
app.include_router(gamification_router)


@app.get("/")
def root():
    """
    Endpoint raíz de la API
    """
    return {
        "message": "Bienvenido a EcoLink API",
        "version": "1.0.0",
        "description": "Plataforma de gestión circular de residuos",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    """
    Health check del API
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
