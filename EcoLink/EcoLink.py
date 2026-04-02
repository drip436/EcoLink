"""
EcoLink Frontend Principal
Aplicación de Gestión Circular de Residuos
Archivo principal que contiene toda la configuración del frontend
"""
import reflex as rx
import sys
import os

# Agregar ruta del frontend para importaciones
frontend_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(frontend_path)
sys.path.insert(0, parent_path)

# Importar estado global
from frontend.app.state import AppState
from frontend.app.pages.login import login_page
from frontend.app.pages.register import register_page
from frontend.app.pages.dashboard import dashboard_page
from frontend.app.pages.profile import profile_page
from frontend.app.components.navbar import navbar


# ============================================================================
# CREAR APLICACIÓN REFLEX
# ============================================================================

app = rx.App()


# ============================================================================
# RUTAS PRINCIPALES
# ============================================================================

@app.add_page
def login_route() -> rx.Component:
    """Página de Login - Ruta principal (/)"""
    return login_page()


@app.add_page
def register_route() -> rx.Component:
    """Página de Registro (/register)"""
    return register_page()


@app.add_page
def dashboard_route() -> rx.Component:
    """Dashboard Principal (/dashboard)"""
    return dashboard_page()


@app.add_page
def profile_route() -> rx.Component:
    """Perfil de Usuario (/profile)"""
    return profile_page()


# ============================================================================
# INFORMACIÓN DE LA APLICACIÓN
# ============================================================================

"""
🌱 ECOLINK - Plataforma de Gestión Circular de Residuos

CARACTERÍSTICAS:
✅ Autenticación de usuarios
✅ Dashboard de actividades
✅ Sistema de gamificación
✅ Visualización de rutas de recolección
✅ Mapa de puntos de acopio
✅ Historial de colecciones

USUARIOS DE PRUEBA:
- Admin: admin@ecolink.com / admin123
- Ciudadano: juan@example.com / citizen123
- Reciclador: recycler@ecolink.com / recycler123

ACCESO:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación: http://localhost:8000/docs
"""
