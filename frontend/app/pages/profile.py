"""
Página de Perfil - Fully Styled
"""
import reflex as rx
from app.state import AppState
from app.components.navbar import navbar


def profile_page() -> rx.Component:
    """Página de perfil del usuario con estilos modernos"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.vstack(
                # Header section with profile card
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.text(
                                "👤",
                                font_size="4rem",
                            ),
                            width="80px",
                            height="80px",
                            padding="8px",
                            background="#f0fdf4",
                            border_radius="16px",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        rx.vstack(
                            rx.text(
                                "Usuario EcoLink",
                                font_size="1.875rem",
                                font_weight="bold",
                                color="#065f46",
                            ),
                            rx.text(
                                "usuario@example.com",
                                color="#6b7280",
                                font_size="1rem",
                            ),
                            rx.badge(
                                rx.text("🌟 Miembro Activo"),
                                color_scheme="green",
                                padding="8px 16px",
                            ),
                            spacing="2",
                        ),
                        spacing="8",
                        width="100%",
                        padding="32px",
                        align_items="center",
                    ),
                    padding="0",
                    background="white",
                    border_radius="16px",
                    box_shadow="0 4px 20px rgba(0, 0, 0, 0.08)",
                    width="100%",
                ),
                # Stats grid
                rx.vstack(
                    rx.heading(
                        "📈 Estadísticas",
                        size="6",
                        color="#1f2937",
                    ),
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("🏆", font_size="1.5rem"),
                                    rx.text(
                                        "Nivel",
                                        color="#6b7280",
                                        font_weight="500",
                                    ),
                                    spacing="2",
                                ),
                                rx.text(
                                    "5",
                                    font_size="2rem",
                                    font_weight="bold",
                                    color="#10b981",
                                ),
                                spacing="2",
                            ),
                            padding="24px",
                            background="white",
                            border_radius="12px",
                            box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
                            border_left="4px solid #10b981",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("⭐", font_size="1.5rem"),
                                    rx.text(
                                        "Puntos",
                                        color="#6b7280",
                                        font_weight="500",
                                    ),
                                    spacing="2",
                                ),
                                rx.text(
                                    "1,250",
                                    font_size="2rem",
                                    font_weight="bold",
                                    color="#f59e0b",
                                ),
                                spacing="2",
                            ),
                            padding="24px",
                            background="white",
                            border_radius="12px",
                            box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
                            border_left="4px solid #f59e0b",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("♻️", font_size="1.5rem"),
                                    rx.text(
                                        "Colecciones",
                                        color="#6b7280",
                                        font_weight="500",
                                    ),
                                    spacing="2",
                                ),
                                rx.text(
                                    "23",
                                    font_size="2rem",
                                    font_weight="bold",
                                    color="#3b82f6",
                                ),
                                spacing="2",
                            ),
                            padding="24px",
                            background="white",
                            border_radius="12px",
                            box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
                            border_left="4px solid #3b82f6",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("🎖️", font_size="1.5rem"),
                                    rx.text(
                                        "Logros",
                                        color="#6b7280",
                                        font_weight="500",
                                    ),
                                    spacing="2",
                                ),
                                rx.text(
                                    "8",
                                    font_size="2rem",
                                    font_weight="bold",
                                    color="#8b5cf6",
                                ),
                                spacing="2",
                            ),
                            padding="24px",
                            background="white",
                            border_radius="12px",
                            box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
                            border_left="4px solid #8b5cf6",
                        ),
                        columns="2",
                        spacing="6",
                        width="100%",
                    ),
                    width="100%",
                    spacing="4",
                ),
                # Achievements section
                rx.vstack(
                    rx.heading(
                        "🎖️ Logros Desbloqueados",
                        size="6",
                        color="#1f2937",
                    ),
                    rx.grid(
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "♻️",
                                    font_size="2rem",
                                    text_align="center",
                                ),
                                rx.text(
                                    "Reciclador Novato",
                                    font_weight="600",
                                    text_align="center",
                                    color="#1f2937",
                                    font_size="0.9rem",
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            padding="24px",
                            background="white",
                            border_radius="12px",
                            border="2px solid #10b981",
                            text_align="center",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "🌱",
                                    font_size="2rem",
                                    text_align="center",
                                ),
                                rx.text(
                                    "Guerrero Verde",
                                    font_weight="600",
                                    text_align="center",
                                    color="#1f2937",
                                    font_size="0.9rem",
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            padding="24px",
                            background="white",
                            border_radius="12px",
                            border="2px solid #10b981",
                            text_align="center",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "⭐",
                                    font_size="2rem",
                                    text_align="center",
                                ),
                                rx.text(
                                    "Campeón",
                                    font_weight="600",
                                    text_align="center",
                                    color="#1f2937",
                                    font_size="0.9rem",
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            padding="24px",
                            background="white",
                            border_radius="12px",
                            border="2px solid #10b981",
                            text_align="center",
                        ),
                        columns="3",
                        spacing="4",
                        width="100%",
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
