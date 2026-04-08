"""
ecolink/ecolink.py
"""

import reflex as rx
from ecolink.components.ui import (
    C_GREEN_DARK, C_GREEN_MID, C_ACCENT, C_BG
)
from ecolink.pages.register import register_page  # noqa: F401
from ecolink.pages.login import login_page        # noqa: F401


@rx.page(route="/", title="EcoLink · Gestión Circular de Residuos")
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.icon("leaf", color="#4caf50", size=56),
                rx.text(
                    "Eco",
                    rx.text.span("Link", color=C_ACCENT),
                    font_size="3.8rem",
                    font_weight="900",
                    color="white",
                    font_family="Georgia, serif",
                    letter_spacing="-0.02em",
                ),
                align="center",
                gap="0.5rem",
                justify="center",
            ),
            rx.text(
                "Gestión Circular de Residuos",
                color="rgba(255,255,255,0.85)",
                font_size="1.2rem",
                font_weight="500",
                text_align="center",
            ),
            rx.text(
                "Proyecto Innovatec · Instituto tecnológico de Mérida",
                color="rgba(255,255,255,0.5)",
                font_size="0.85rem",
                text_align="center",
            ),
            rx.divider(border_color="rgba(255,255,255,0.18)", margin_y="1.4rem"),
            rx.flex(
                *[
                    rx.box(
                        rx.hstack(
                            rx.text(ic, font_size="1rem"),
                            rx.text(lb, font_size="0.8rem", font_weight="600", color="white"),
                            align="center", gap="0.35rem",
                        ),
                        background="rgba(255,255,255,0.1)",
                        border="1px solid rgba(255,255,255,0.22)",
                        border_radius="20px",
                        padding="0.35rem 0.8rem",
                    )
                    for ic, lb in [
                        ("🚛", "Rutas en tiempo real"),
                        ("📍", "Puntos de acopio"),
                        ("🏆", "Gamificación"),
                        ("🎁", "Recompensas"),
                        ("📊", "Ranking"),
                    ]
                ],
                wrap="wrap",
                justify="center",
                gap="0.55rem",
            ),
            rx.divider(border_color="rgba(255,255,255,0.18)", margin_y="1.4rem"),
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon("user-plus", size=17),
                        "Crear cuenta gratis",
                        size="4",
                        background="white",
                        color=C_GREEN_DARK,
                        font_weight="800",
                        cursor="pointer",
                        _hover={"background": "#f0faf0", "transform": "translateY(-2px)"},
                        transition="all 0.18s",
                    ),
                    href="/register",
                ),
                rx.link(
                    rx.button(
                        rx.icon("log-in", size=17),
                        "Iniciar sesión",
                        size="4",
                        variant="outline",
                        color="white",
                        border_color="rgba(255,255,255,0.55)",
                        cursor="pointer",
                        _hover={"background": "rgba(255,255,255,0.1)"},
                        transition="all 0.18s",
                    ),
                    href="/login",
                ),
                gap="1rem",
                justify="center",
                flex_wrap="wrap",
            ),
            align="center",
            gap="0.7rem",
            max_width="580px",
            padding="0 1.2rem",
            text_align="center",
        ),
        min_height="100vh",
        background=f"linear-gradient(160deg, {C_GREEN_DARK} 0%, {C_GREEN_MID} 55%, #1b5e20 100%)",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="green",
        radius="medium",
        scaling="100%",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    ],
    style={
        "font_family": "Inter, sans-serif",
        "background_color": C_BG,
    },
)