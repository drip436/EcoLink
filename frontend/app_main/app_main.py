"""
Aplicación Principal de Reflex - EcoLink
Define todas las rutas y la estructura de la app
"""
import reflex as rx
from app.state import AppState
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.pages.profile import profile_page


# Crear app
app = rx.App()

# Ruta principal - Alterna entre login y registro basado en state
@app.add_page
def index() -> rx.Component:
    return rx.cond(
        AppState.current_page == "register",
        register_page(),
        login_page(),
    )

# Ruta de registro (para acceso directo)
@app.add_page
def register_page_route() -> rx.Component:
    return register_page()

# Ruta de dashboard (solo usuarios autenticados)
@app.add_page
def dashboard_page_route() -> rx.Component:
    return rx.cond(
        AppState.is_authenticated,
        dashboard_page(),
        login_page(),
    )

# Ruta de perfil (solo usuarios autenticados)
@app.add_page
def profile_page_route() -> rx.Component:
    return rx.cond(
        AppState.is_authenticated,
        profile_page(),
        login_page(),
    )
