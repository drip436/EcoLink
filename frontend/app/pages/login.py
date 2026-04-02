"""
Página de Login - Fully Styled
"""
import reflex as rx
from app.state import AppState
from app.components.navbar import navbar


def login_page() -> rx.Component:
    """Página de login con estilos modernos"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                # Header section
                rx.vstack(
                    rx.heading(
                        "¡Bienvenido a EcoLink!",
                        size="9",
                        text_align="center",
                        color="#065f46",
                        font_weight="bold",
                    ),
                    rx.text(
                        "Plataforma de gestión circular de residuos",
                        text_align="center",
                        color="#4b5563",
                        size="4",
                    ),
                    width="100%",
                    spacing="2",
                ),
                # Form section
                rx.box(
                    rx.form(
                        rx.vstack(
                            # Email Input
                            rx.input(
                                placeholder="📧 Email",
                                value=AppState.login_email,
                                on_change=AppState.set_login_email,
                                type="email",
                                width="100%",
                                padding="12px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                font_size="1rem",
                                _focus={
                                    "border_color": "#10b981",
                                    "box_shadow": "0 0 0 3px rgba(16, 185, 129, 0.1)",
                                },
                            ),
                            # Password Input
                            rx.input(
                                placeholder="🔒 Contraseña",
                                value=AppState.login_password,
                                on_change=AppState.set_login_password,
                                type="password",
                                width="100%",
                                padding="12px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                font_size="1rem",
                                _focus={
                                    "border_color": "#10b981",
                                    "box_shadow": "0 0 0 3px rgba(16, 185, 129, 0.1)",
                                },
                            ),
                            # Error message
                            rx.cond(
                                AppState.auth_error != "",
                                rx.box(
                                    rx.hstack(
                                        rx.text("⚠️", font_size="1.25rem"),
                                        rx.text(
                                            AppState.auth_error,
                                            color="#7f1d1d",
                                            font_weight="500",
                                        ),
                                        spacing="2",
                                        width="100%",
                                    ),
                                    padding="16px",
                                    background="#fee2e2",
                                    border_left="4px solid #dc2626",
                                    border_radius="8px",
                                    width="100%",
                                ),
                            ),
                            # Login Button
                            rx.button(
                                rx.cond(
                                    AppState.loading,
                                    rx.hstack(
                                        rx.spinner(size="3"),
                                        rx.text("Iniciando..."),
                                        spacing="2",
                                    ),
                                    rx.text("Iniciar Sesión"),
                                ),
                                on_click=AppState.handle_login,
                                width="100%",
                                padding="12px 24px",
                                background="#10b981",
                                color="white",
                                border_radius="8px",
                                font_size="1rem",
                                font_weight="600",
                                border="none",
                                cursor="pointer",
                                _hover={
                                    "background": "#059669",
                                    "box_shadow": "0 4px 12px rgba(16, 185, 129, 0.4)",
                                },
                                _active={
                                    "background": "#047857",
                                },
                                is_disabled=AppState.loading,
                            ),
                            # Register link
                            rx.hstack(
                                rx.text(
                                    "¿No tienes cuenta?",
                                    color="#4b5563",
                                    font_size="0.95rem",
                                ),
                                rx.link(
                                    "Regístrate aquí",
                                    href="/register",
                                    color="#10b981",
                                    font_weight="600",
                                    text_decoration="none",
                                    _hover={
                                        "text_decoration": "underline",
                                        "color": "#059669",
                                    },
                                ),
                                spacing="1",
                                justify_content="center",
                                width="100%",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    width="100%",
                    padding="32px",
                    background="white",
                    border_radius="16px",
                    box_shadow="0 4px 20px rgba(0, 0, 0, 0.08)",
                ),
                spacing="8",
                width="100%",
                max_width="450px",
                margin="0 auto",
            ),
            width="100%",
            min_height="100vh",
            padding="32px 16px",
            background="linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%)",
        ),
        width="100%",
        min_height="100vh",
        margin="0",
        padding="0",
        spacing="0",
    )
