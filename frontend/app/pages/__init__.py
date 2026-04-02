"""
Paginas de la aplicación
"""
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.pages.profile import profile_page

__all__ = [
    "login_page",
    "register_page",
    "dashboard_page",
    "profile_page",
]
