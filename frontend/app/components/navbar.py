"""
Componente de Navegación - Fully Styled
"""
import reflex as rx
from app.state import AppState


def navbar() -> rx.Component:
    """Navbar de la aplicación con estilos modernos"""
    return rx.vstack(
        rx.box(
            rx.hstack(
                # Logo
                rx.hstack(
                    rx.text(
                        "🌱",
                        font_size="2rem",
                    ),
                    rx.text(
                        "EcoLink",
                        font_size="1.5rem",
                        font_weight="bold",
                        color="#065f46",
                    ),
                    spacing="2",
                    align_items="center",
                ),
                rx.spacer(),
                # Auth section
                rx.cond(
                    AppState.is_authenticated,
                    rx.hstack(
                        # User menu
                        rx.box(
                            rx.hstack(
                                rx.text(
                                    "👤",
                                    font_size="1.25rem",
                                ),
                                rx.vstack(
                                    rx.text(
                                        "Usuario",
                                        font_size="0.875rem",
                                        color="#6b7280",
                                    ),
                                    rx.text(
                                        "admin@ecolink.com",
                                        font_size="0.75rem",
                                        color="#9ca3af",
                                        font_weight="500",
                                    ),
                                    spacing="1",
                                ),
                                spacing="3",
                            ),
                            padding="8px 16px",
                            background="#f3f4f6",
                            border_radius="8px",
                        ),
                        # Logout button
                        rx.button(
                            "🚪 Cerrar Sesión",
                            on_click=AppState.handle_logout,
                            padding="8px 16px",
                            background="#ef4444",
                            color="white",
                            border="none",
                            border_radius="8px",
                            cursor="pointer",
                            _hover={
                                "background": "#dc2626",
                                "box_shadow": "0 4px 12px rgba(239, 68, 68, 0.4)",
                            },
                        ),
                        spacing="4",
                        align_items="center",
                    ),
                    # Unauthenticated menu
                    rx.hstack(
                        rx.link(
                            rx.text(
                                "🔐 Iniciar Sesión",
                                font_weight="600",
                                color="#10b981",
                            ),
                            href="/login",
                            text_decoration="none",
                            _hover={
                                "color": "#059669",
                                "text_decoration": "underline",
                            },
                        ),
                        rx.link(
                            rx.box(
                                rx.text(
                                    "✍️ Registrarse",
                                    color="white",
                                    font_weight="600",
                                ),
                                padding="8px 16px",
                                background="#10b981",
                                border_radius="8px",
                                text_decoration="none",
                                _hover={
                                    "background": "#059669",
                                    "box_shadow": "0 4px 12px rgba(16, 185, 129, 0.4)",
                                },
                            ),
                            href="/register",
                            text_decoration="none",
                        ),
                        spacing="6",
                        align_items="center",
                    ),
                ),
                spacing="8",
                width="100%",
                align_items="center",
            ),
            width="100%",
            padding="16px 32px",
            background="white",
            border_bottom="2px solid #f0fdf4",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.05)",
        ),
        width="100%",
        margin="0",
        padding="0",
        spacing="0",
    )


def stats_card(title: str, value: rx.Var | str, icon: str = "📊") -> rx.Component:
    """Tarjeta de estadísticas con estilos mejorados"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(icon, font_size="2rem"),
                rx.vstack(
                    rx.text(
                        title,
                        font_size="0.875rem",
                        color="#6b7280",
                        font_weight="500",
                    ),
                    rx.text(
                        value,
                        font_size="1.5rem",
                        font_weight="bold",
                        color="#10b981",
                    ),
                    spacing="1",
                ),
                spacing="4",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),
        border="1px solid #e5e7eb",
        border_radius="12px",
        padding="24px",
        background="white",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
        _hover={
            "box_shadow": "0 4px 16px rgba(0, 0, 0, 0.12)",
            "border_color": "#10b981",
        },
    )


def point_card(point) -> rx.Component:
    """Tarjeta de punto de acopio con estilos mejorados"""
    capacity_color = rx.cond(
        point.current_capacity_percent > 80,
        "#ef4444",
        rx.cond(
            point.current_capacity_percent > 50,
            "#f59e0b",
            "#10b981"
        ),
    )
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text(
                    "📍",
                    font_size="1.5rem",
                ),
                rx.vstack(
                    rx.heading(
                        point.name,
                        size="sm",
                        color="#1f2937",
                    ),
                    rx.text(
                        point.address,
                        font_size="0.875rem",
                        color="#6b7280",
                    ),
                    spacing="1",
                ),
                spacing="4",
                width="100%",
            ),
            # Capacity indicator
            rx.vstack(
                rx.hstack(
                    rx.text(
                        f"Capacidad: {point.current_capacity_percent}%",
                        font_size="0.875rem",
                        font_weight="500",
                        color="#1f2937",
                    ),
                    rx.spacer(),
                    rx.box(
                        rx.text(
                            f"{point.current_capacity_percent}%",
                            font_size="0.75rem",
                            font_weight="bold",
                            color=capacity_color,
                        ),
                    ),
                ),
                rx.progress(
                    value=point.current_capacity_percent / 100,
                    width="100%",
                    color_scheme=rx.cond(point.current_capacity_percent > 80, "red", rx.cond(point.current_capacity_percent > 50, "orange", "green")),
                ),
                spacing="2",
                width="100%",
            ),
            # Waste types
            rx.hstack(
                *[rx.badge(waste_type, color_scheme="green", padding="4px 12px") for waste_type in point.waste_types[:3]],
                spacing="2",
                width="100%",
            ),
            # Coordinates
            rx.text(
                f"🧭 {point.latitude:.4f}, {point.longitude:.4f}",
                font_size="0.75rem",
                color="#9ca3af",
            ),
            spacing="4",
            width="100%",
        ),
        border="1px solid #e5e7eb",
        border_radius="12px",
        padding="24px",
        background="white",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
        cursor="pointer",
        _hover={
            "box_shadow": "0 4px 16px rgba(0, 0, 0, 0.12)",
            "border_color": "#10b981",
        },
    )


def route_card(route) -> rx.Component:
    """Tarjeta de ruta de recolección con estilos mejorados"""
    status_color = "#10b981" if route.status == "in_progress" else "#3b82f6"
    status_label = "En Progreso" if route.status == "in_progress" else "Completada"
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(route.name, size="sm", color="#1f2937"),
                rx.spacer(),
                rx.badge(
                    status_label,
                    color_scheme="green" if route.status == "in_progress" else "blue",
                    padding="4px 12px",
                ),
            ),
            # Weight indicator
            rx.vstack(
                rx.hstack(
                    rx.text(
                        f"Peso: {route.current_weight_kg}/{route.capacity_kg} kg",
                        font_size="0.875rem",
                        font_weight="500",
                        color="#1f2937",
                    ),
                    rx.spacer(),
                    rx.text(
                        f"{(route.current_weight_kg / route.capacity_kg * 100):.0f}%",
                        font_size="0.75rem",
                        font_weight="bold",
                        color="gray",
                    ),
                ),
                rx.progress(
                    value=route.current_weight_kg / route.capacity_kg,
                    width="100%",
                    color_scheme="green",
                ),
                spacing="2",
                width="100%",
            ),
            # Vehicle type
            rx.hstack(
                rx.text("🚗", font_size="1rem"),
                rx.text(
                    route.vehicle_type,
                    font_size="0.875rem",
                    color="#6b7280",
                ),
                spacing="2",
            ),
            spacing="4",
            width="100%",
        ),
        border="1px solid #e5e7eb",
        border_radius="12px",
        padding="24px",
        background="white",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.08)",
        _hover={
            "box_shadow": "0 4px 16px rgba(0, 0, 0, 0.12)",
            "border_color": status_color,
        },
    )


def achievement_badge(name: str, icon: str = "⭐") -> rx.Component:
    """Badge de logro con estilos mejorados"""
    return rx.box(
        rx.vstack(
            rx.text(icon, font_size="2rem"),
            rx.text(
                name,
                font_size="0.75rem",
                text_align="center",
                color="#1f2937",
                font_weight="600",
            ),
            spacing="2",
            align_items="center",
        ),
        border="2px solid #10b981",
        border_radius="12px",
        padding="16px",
        text_align="center",
        background="white",
        box_shadow="0 2px 8px rgba(16, 185, 129, 0.1)",
        cursor="pointer",
        _hover={
            "box_shadow": "0 4px 16px rgba(16, 185, 129, 0.2)",
            "background": "#f0fdf4",
        },
    )
