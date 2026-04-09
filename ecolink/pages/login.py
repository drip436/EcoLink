"""
ecolink/pages/login.py
Página de inicio de sesión.
"""

import reflex as rx
from ecolink.state import State
from ecolink.components.ui import (
    C_GREEN_DARK, C_GREEN_MID, C_ACCENT,
    C_WHITE, C_MUTED, input_field, notification_bar,
)


@rx.page(route="/login", title="EcoLink · Iniciar sesión")
def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Logo
            rx.hstack(
                rx.icon("leaf", color="#4caf50", size=32),
                rx.text(
                    "Eco",
                    rx.text.span("Link", color=C_ACCENT),
                    font_size="2rem",
                    font_weight="900",
                    color="white",
                    font_family="Georgia, serif",
                ),
                align="center",
                gap="0.4rem",
                justify="center",
            ),
            rx.text(
                "Bienvenido de nuevo",
                color="rgba(255,255,255,0.8)",
                font_size="0.95rem",
                text_align="center",
            ),

            # Card del formulario
            rx.box(
                rx.vstack(
                    notification_bar(),
                    input_field(
                        "Correo electrónico",
                        "tucorreo@ejemplo.com",
                        State.f_login_email,
                        State.set_f_login_email,
                        type_="email",
                    ),
                    input_field(
                        "Contraseña",
                        "Tu contraseña",
                        State.f_login_pass,
                        State.set_f_login_pass,
                        type_="password",
                    ),
                    rx.button(
                        rx.cond(
                            State.is_loading,
                            rx.hstack(
                                rx.spinner(size="2"),
                                rx.text("Ingresando..."),
                                align="center", gap="0.5rem",
                            ),
                            rx.hstack(
                                rx.icon("log-in", size=16),
                                rx.text("Iniciar sesión"),
                                align="center", gap="0.5rem",
                            ),
                        ),
                        on_click=State.login,
                        width="100%",
                        size="3",
                        background=f"linear-gradient(135deg, {C_GREEN_MID}, {C_ACCENT})",
                        color="white",
                        font_weight="700",
                        cursor="pointer",
                        _hover={"opacity": "0.9", "transform": "translateY(-1px)"},
                        transition="all 0.18s",
                        disabled=State.is_loading,
                    ),
                    rx.center(
                        rx.hstack(
                            rx.text("¿No tienes cuenta?", color=C_MUTED, font_size="0.85rem"),
                            rx.link(
                                "Regístrate gratis",
                                href="/register",
                                color=C_GREEN_MID,
                                font_weight="700",
                                font_size="0.85rem",
                                _hover={"color": C_ACCENT},
                            ),
                            gap="0.35rem",
                            align="center",
                        ),
                    ),
                    gap="1rem",
                    width="100%",
                ),
                background=C_WHITE,
                border_radius="18px",
                padding="2rem 1.8rem",
                box_shadow="0 8px 32px rgba(0,0,0,0.18)",
                width="100%",
                max_width="420px",
            ),
            align="center",
            gap="1.2rem",
            width="100%",
            max_width="420px",
            padding="0 1rem",
        ),
        min_height="100vh",
        background=f"linear-gradient(160deg, {C_GREEN_DARK} 0%, {C_GREEN_MID} 55%, #1b5e20 100%)",
        padding="2rem 1rem",
    )