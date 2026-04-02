"""
Dashboard Principal - Fully Styled
"""
import reflex as rx
from app.state import AppState
from app.components.navbar import navbar


def stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    """Componente reutilizable para tarjetas de estadísticas"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    icon,
                    font_size="2rem",
                ),
                rx.vstack(
                    rx.text(
                        title,
                        color="#6b7280",
                        font_size="0.9rem",
                        font_weight="500",
                    ),
                    rx.text(
                        value,
                        font_size="1.875rem",
                        font_weight="bold",
                        color=color,
                    ),
                    spacing="1",
                ),
                spacing="4",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),
        padding="24px",
        background="white",
        border_radius="12px",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
        border_left=f"4px solid {color}",
        width="100%",
        _hover={
            "box_shadow": "0 4px 16px rgba(0, 0, 0, 0.12)",
        },
    )


def dashboard_page() -> rx.Component:
    """Dashboard principal con estilos modernos"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                # Header section
                rx.vstack(
                    rx.heading(
                        "¡Bienvenido al Dashboard!",
                        size="9",
                        color="#065f46",
                        font_weight="bold",
                    ),
                    rx.text(
                        "Monitorea tu actividad en reciclaje y controla tus estadísticas",
                        color="#4b5563",
                        size="4",
                    ),
                    width="100%",
                    spacing="2",
                ),
                # Stats grid
                rx.vstack(
                    rx.heading(
                        "📊 Mis Estadísticas",
                        size="6",
                        color="#1f2937",
                    ),
                    rx.grid(
                        stat_card(
                            "Puntos Totales",
                            "0",
                            "⭐",
                            "#10b981"
                        ),
                        stat_card(
                            "Nivel Actual",
                            "1",
                            "🏆",
                            "#f59e0b"
                        ),
                        stat_card(
                            "Colecciones",
                            "0",
                            "♻️",
                            "#3b82f6"
                        ),
                        stat_card(
                            "Logros Desbloqueados",
                            "0",
                            "🎖️",
                            "#8b5cf6"
                        ),
                        columns="2",
                        spacing="6",
                        width="100%",
                    ),
                    width="100%",
                    spacing="4",
                ),
                # Activity section
                rx.vstack(
                    rx.heading(
                        "🎯 Próximos Objetivos",
                        size="6",
                        color="#1f2937",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.text("1️⃣", font_size="1.5rem"),
                                width="48px",
                                padding="8px",
                                background="#f0fdf4",
                                border_radius="8px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Realiza tu primera colección",
                                    font_weight="600",
                                    color="#1f2937",
                                ),
                                rx.text(
                                    "Gana 50 puntos al completar tu primer reciclaje",
                                    color="#6b7280",
                                    font_size="0.9rem",
                                ),
                                spacing="1",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border="1px solid #e5e7eb",
                    ),
                    rx.hstack(
                        rx.box(
                            rx.text("2️⃣", font_size="1.5rem"),
                            width="48px",
                            padding="8px",
                            background="#fef3c7",
                            border_radius="8px",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        rx.vstack(
                            rx.text(
                                "Alcanza nivel 2",
                                font_weight="600",
                                color="#1f2937",
                            ),
                            rx.text(
                                "Necesitas 200 puntos más para avanzar",
                                color="#6b7280",
                                font_size="0.9rem",
                            ),
                            spacing="1",
                        ),
                        spacing="4",
                        width="100%",
                        padding="24px",
                        background="white",
                        border_radius="12px",
                        border="1px solid #e5e7eb",
                    ),
                    width="100%",
                    spacing="4",
                ),
            ),
            width="100%",
            min_height="100vh",
            padding="32px 16px",
            background="#f9fafb",
            spacing="8",
        ),
        width="100%",
        min_height="100vh",
        margin="0",
        padding="0",
        spacing="0",
    )
