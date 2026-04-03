"""
Página de Registro - Fully Styled
"""
import reflex as rx
from app.state import AppState
from app.components.navbar import navbar


def register_page() -> rx.Component:
    """Página de registro con estilos modernos"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                # Header section
                rx.vstack(
                    rx.heading(
                        "Crear Cuenta en EcoLink",
                        size="9",
                        text_align="center",
                        color="#065f46",
                        font_weight="bold",
                    ),
                    rx.text(
                        "Únete a nuestra comunidad de recicladores",
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
                            # Full Name Input
                            rx.input(
                                placeholder="👤 Nombre Completo",
                                value=AppState.register_full_name,
                                on_change=AppState.set_register_full_name,
                                width="100%",
                                padding="20px 16px",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                font_size="1rem",
                                _focus={
                                    "border_color": "#10b981",
                                    "box_shadow": "0 0 0 3px rgba(16, 185, 129, 0.1)",
                                },
                            ),
                            # Email Input
                            rx.input(
                                placeholder="📧 Email",
                                value=AppState.register_email,
                                on_change=AppState.set_register_email,
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
                                value=AppState.register_password,
                                on_change=AppState.set_register_password,
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
                            # Confirm Password Input
                            rx.input(
                                placeholder="🔒 Confirmar Contraseña",
                                value=AppState.register_confirm_password,
                                on_change=AppState.set_register_confirm_password,
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
                            # Register Button
                            rx.button(
                                rx.cond(
                                    AppState.loading,
                                    rx.hstack(
                                        rx.spinner(size="3"),
                                        rx.text("Registrando..."),
                                        spacing="2",
                                    ),
                                    rx.text("Registrarse"),
                                ),
                                on_click=AppState.handle_register,
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
                            # Login link
                            rx.hstack(
                                rx.text(
                                    "¿Ya tienes cuenta?",
                                    color="#4b5563",
                                    font_size="0.95rem",
                                ),
                                rx.button(
                                    "Inicia sesión",
                                    on_click=AppState.go_to_login,
                                    background="transparent",
                                    color="#10b981",
                                    font_weight="600",
                                    border="none",
                                    padding="0",
                                    cursor="pointer",
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
