"""
Configuración de Reflex para EcoLink Frontend
"""
import reflex as rx
from reflex.plugins.sitemap import SitemapPlugin


config = rx.Config(
    app_name="EcoLink",
    api_url="http://localhost:8000",
    baseurl="http://localhost:3000",
    env=rx.Env.DEV,
    disable_plugins=[SitemapPlugin],
)
