"""
EcoLink Frontend - Configuración de Reflex
"""
import reflex as rx

# Configuración de Reflex sin websockets
config = rx.Config(
    app_name="ecolink",
    # No usar websockets - usar solo HTTP
)

app = rx.App()
