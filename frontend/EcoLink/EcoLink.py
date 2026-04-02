"""
EcoLink Frontend - Aplicación Completa
Todo el código frontend con todos los estilos en un único archivo
"""
import reflex as rx
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.state import AppState


# ============================================================================
# COMPONENTE: NAVBAR
# ============================================================================

def navbar() -> rx.Component:
    """Barra de navegación estilizada"""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.text("🌱", font_size="2rem"),
                rx.text("EcoLink", font_size="1.5rem", font_weight="bold", color="#065f46"),
                spacing="2",
            ),
            rx.spacer(),
            rx.cond(
                AppState.is_authenticated,
                rx.hstack(
                    rx.box(
                        rx.hstack(
                            rx.text("👤", font_size="1.25rem"),
                            rx.vstack(
                                rx.text("Usuario", font_size="0.875rem", color="#6b7280"),
                                rx.text("admin@ecolink.com", font_size="0.75rem", color="#9ca3af"),
                                spacing="1",
                            ),
                            spacing="3",
                        ),
                        padding="8px 16px",
                        background="#f3f4f6",
                        border_radius="8px",
                    ),
                    rx.button("🚪 Cerrar", on_click=AppState.handle_logout, padding="8px 16px", background="#ef4444", color="white", border="none", border_radius="8px"),
                    spacing="4",
                ),
                rx.hstack(
                    rx.link("🔐 Iniciar", href="/", color="#10b981", font_weight="600"),
                    rx.link("✍️ Registrar", href="/register", color="white", background="#10b981", padding="8px 16px", border_radius="8px"),
                    spacing="4",
                ),
            ),
            width="100%",
            spacing="8",
        ),
        width="100%",
        padding="16px 32px",
        background="white",
        border_bottom="2px solid #f0fdf4",
    )


# ============================================================================
# PÁGINA: LOGIN
# ============================================================================

def login_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading("¡Bienvenido a EcoLink!", size="9", text_align="center", color="#065f46", font_weight="bold"),
                rx.text("Gestión circular de residuos", text_align="center", color="#4b5563", size="4"),
                rx.box(
                    rx.form(
                        rx.vstack(
                            rx.input(
                                placeholder="📧 Email",
                                value=AppState.login_email,
                                on_change=AppState.set_login_email,
                                type="email",
                                width="100%",
                                padding="20px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                color="#000000",
                                font_size="20px",
                                height="56px",
                                _focus={"border_color": "#10b981"},
                                _placeholder={"color": "#9ca3af"},
                            ),
                            rx.input(
                                placeholder="🔒 Contraseña",
                                value=AppState.login_password,
                                on_change=AppState.set_login_password,
                                type="password",
                                width="100%",
                                padding="20px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                color="#000000",
                                font_size="20px",
                                height="56px",
                                _focus={"border_color": "#10b981"},
                                _placeholder={"color": "#9ca3af"},
                            ),
                            rx.cond(
                                AppState.auth_error != "",
                                rx.box(
                                    rx.text(AppState.auth_error, color="#dc2626", font_weight="600"),
                                    padding="12px 16px",
                                    background="#fee2e2",
                                    border_radius="8px",
                                    width="100%",
                                ),
                            ),
                            rx.button(
                                "Iniciar Sesión",
                                on_click=AppState.handle_login,
                                width="100%",
                                padding="12px 24px",
                                background="#10b981",
                                color="white",
                                border_radius="8px",
                                font_weight="600",
                                border="none",
                                _hover={"background": "#059669"},
                            ),
                            rx.hstack(
                                rx.text("¿Sin cuenta?", color="#4b5563"),
                                rx.link("Regístrate", href="/register", color="#10b981", font_weight="600"),
                                spacing="2",
                                justify_content="center",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    padding="32px",
                    background="white",
                    border_radius="16px",
                    box_shadow="0 4px 20px rgba(0,0,0,0.08)",
                    width="100%",
                    max_width="450px",
                ),
                spacing="6",
                width="100%",
                max_width="450px",
                margin="auto",
            ),
            width="100%",
            padding="32px 16px",
            background="linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%)",
            min_height="100vh",
        ),
        width="100%",
        spacing="0",
        margin="0",
        padding="0",
    )


# ============================================================================
# PÁGINA: REGISTER
# ============================================================================

def register_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading("Crear Cuenta", size="9", text_align="center", color="#065f46", font_weight="bold"),
                rx.text("Únete a EcoLink", text_align="center", color="#4b5563", size="4"),
                rx.box(
                    rx.form(
                        rx.vstack(
                            rx.input(
                                placeholder="👤 Nombre",
                                value=AppState.register_full_name,
                                on_change=AppState.set_register_full_name,
                                width="100%",
                                padding="20px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                color="#000000",
                                font_size="20px",
                                height="56px",
                                _focus={"border_color": "#10b981"},
                                _placeholder={"color": "#9ca3af"},
                            ),
                            rx.input(
                                placeholder="📧 Email",
                                value=AppState.register_email,
                                on_change=AppState.set_register_email,
                                type="email",
                                width="100%",
                                padding="20px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                color="#000000",
                                font_size="20px",
                                height="56px",
                                _focus={"border_color": "#10b981"},
                                _placeholder={"color": "#9ca3af"},
                            ),
                            rx.input(
                                placeholder="🔒 Contraseña",
                                value=AppState.register_password,
                                on_change=AppState.set_register_password,
                                type="password",
                                width="100%",
                                padding="20px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                color="#000000",
                                font_size="20px",
                                height="56px",
                                _focus={"border_color": "#10b981"},
                                _placeholder={"color": "#9ca3af"},
                            ),
                            rx.input(
                                placeholder="🔒 Confirmar",
                                value=AppState.register_confirm_password,
                                on_change=AppState.set_register_confirm_password,
                                type="password",
                                width="100%",
                                padding="20px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                color="#000000",
                                font_size="20px",
                                height="56px",
                                _focus={"border_color": "#10b981"},
                                _placeholder={"color": "#9ca3af"},
                            ),
                            rx.cond(
                                AppState.auth_error != "",
                                rx.box(
                                    rx.text(AppState.auth_error, color="#dc2626", font_weight="600"),
                                    padding="12px 16px",
                                    background="#fee2e2",
                                    border_radius="8px",
                                    width="100%",
                                ),
                            ),
                            rx.button(
                                "Registrarse",
                                on_click=AppState.handle_register,
                                width="100%",
                                padding="12px 24px",
                                background="#10b981",
                                color="white",
                                border_radius="8px",
                                font_weight="600",
                                border="none",
                                _hover={"background": "#059669"},
                            ),
                            rx.hstack(
                                rx.text("¿Tienes cuenta?", color="#4b5563"),
                                rx.link("Inicia", href="/", color="#10b981", font_weight="600"),
                                spacing="2",
                                justify_content="center",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    padding="32px",
                    background="white",
                    border_radius="16px",
                    box_shadow="0 4px 20px rgba(0,0,0,0.08)",
                    width="100%",
                    max_width="450px",
                ),
                spacing="6",
                width="100%",
                max_width="450px",
                margin="auto",
            ),
            width="100%",
            padding="32px 16px",
            background="linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%)",
            min_height="100vh",
        ),
        width="100%",
        spacing="0",
        margin="0",
        padding="0",
    )


# ============================================================================
# PÁGINA: DASHBOARD
# ============================================================================

def dashboard_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading("Dashboard", size="9", color="#065f46", font_weight="bold"),
                rx.text("Tu actividad de reciclaje", color="#4b5563", size="4"),
                rx.grid(
                    rx.box(
                        rx.vstack(
                            rx.text("⭐ Puntos", color="#6b7280", font_weight="500"),
                            rx.text("0", font_size="2rem", font_weight="bold", color="#10b981"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #10b981",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("🏆 Nivel", color="#6b7280", font_weight="500"),
                            rx.text("1", font_size="2rem", font_weight="bold", color="#f59e0b"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #f59e0b",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("♻️ Colecciones", color="#6b7280", font_weight="500"),
                            rx.text("0", font_size="2rem", font_weight="bold", color="#3b82f6"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #3b82f6",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("🎖️ Logros", color="#6b7280", font_weight="500"),
                            rx.text("0", font_size="2rem", font_weight="bold", color="#8b5cf6"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #8b5cf6",
                    ),
                    columns="2",
                    spacing="6",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("🎯 Objetivos", size="6", color="#1f2937"),
                        rx.box(
                            rx.vstack(
                                rx.text("Primera Colección", font_weight="600", color="#1f2937"),
                                rx.text("Gana 50 puntos", color="#6b7280", font_size="0.9rem"),
                            ),
                            padding="16px",
                            background="#f0fdf4",
                            border_radius="8px",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    padding="24px",
                    background="white",
                    border_radius="12px",
                    width="100%",
                ),
                spacing="6",
                width="100%",
                max_width="1000px",
                margin="auto",
            ),
            width="100%",
            padding="32px 16px",
            background="#f9fafb",
            min_height="100vh",
        ),
        width="100%",
        spacing="0",
        margin="0",
        padding="0",
    )


# ============================================================================
# PÁGINA: PROFILE
# ============================================================================

def profile_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.box(rx.text("👤", font_size="3rem"), width="80px", height="80px", padding="8px", background="#f0fdf4", border_radius="12px", display="flex", align_items="center", justify_content="center"),
                        rx.vstack(
                            rx.text("Usuario EcoLink", font_size="1.5rem", font_weight="bold", color="#065f46"),
                            rx.text("usuario@example.com", color="#6b7280"),
                            spacing="2",
                        ),
                        spacing="6",
                        padding="24px",
                        width="100%",
                    ),
                    background="white",
                    border_radius="12px",
                    width="100%",
                ),
                rx.grid(
                    rx.box(
                        rx.vstack(
                            rx.text("🏆 Nivel", color="#6b7280", font_weight="500"),
                            rx.text("5", font_size="2rem", font_weight="bold", color="#10b981"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #10b981",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("⭐ Puntos", color="#6b7280", font_weight="500"),
                            rx.text("1,250", font_size="2rem", font_weight="bold", color="#f59e0b"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #f59e0b",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("♻️ Colecciones", color="#6b7280", font_weight="500"),
                            rx.text("23", font_size="2rem", font_weight="bold", color="#3b82f6"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #3b82f6",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("🎖️ Logros", color="#6b7280", font_weight="500"),
                            rx.text("8", font_size="2rem", font_weight="bold", color="#8b5cf6"),
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border_left="4px solid #8b5cf6",
                    ),
                    columns="2",
                    spacing="6",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("🎖️ Logros", size="6", color="#1f2937"),
                    rx.grid(
                        rx.box(rx.vstack(rx.text("♻️", font_size="2rem", text_align="center"), rx.text("Novato", font_weight="600", font_size="0.9rem"), spacing="2"), padding="16px", background="white", border="2px solid #10b981", border_radius="8px", text_align="center"),
                        rx.box(rx.vstack(rx.text("🌱", font_size="2rem", text_align="center"), rx.text("Verde", font_weight="600", font_size="0.9rem"), spacing="2"), padding="16px", background="white", border="2px solid #10b981", border_radius="8px", text_align="center"),
                        rx.box(rx.vstack(rx.text("⭐", font_size="2rem", text_align="center"), rx.text("Campeón", font_weight="600", font_size="0.9rem"), spacing="2"), padding="16px", background="white", border="2px solid #10b981", border_radius="8px", text_align="center"),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    spacing="4",
                ),
                spacing="6",
                width="100%",
                max_width="1000px",
                margin="auto",
            ),
            width="100%",
            padding="32px 16px",
            background="#f9fafb",
            min_height="100vh",
        ),
        width="100%",
        spacing="0",
        margin="0",
        padding="0",
    )


# ============================================================================
# APLICACIÓN
# ============================================================================

app = rx.App()


@app.add_page
def index() -> rx.Component:
    return login_page()


@app.add_page
def register() -> rx.Component:
    return register_page()


@app.add_page
def dashboard() -> rx.Component:
    return dashboard_page()


@app.add_page
def profile() -> rx.Component:
    return profile_page()
