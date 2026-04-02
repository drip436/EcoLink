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

# Ruta de login (default)
@app.add_page
def index() -> rx.Component:
    return login_page()

# Ruta de registro
@app.add_page
def register_page_route() -> rx.Component:
    return register_page()

# Ruta de dashboard (solo usuarios autenticados)
@app.add_page
def dashboard_page_route() -> rx.Component:
    return dashboard_page()

# Ruta de perfil (solo usuarios autenticados)
@app.add_page
def profile_page_route() -> rx.Component:
    return profile_page()
