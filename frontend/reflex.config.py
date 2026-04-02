"""
EcoLink Frontend - Configuración de Reflex
"""
import reflex as rx

config = rx.Config(
    app_name="ecolink",
    env=rx.Env.DEV,
)

# Configuración específica
web_config = {
    "theme": {
        "colors": {
            "primary": "#10b981",  # Verde eco
            "secondary": "#3b82f6",  # Azul
            "accent": "#f59e0b",  # Ámbar
            "error": "#ef4444",
            "success": "#22c55e",
            "warning": "#f97316",
        }
    },
    "fonts": ["Poppins"],
}

app = rx.App()
