"""
ecolink/pages/admin.py  — VERSIÓN CON SIMULACIÓN DE RUTAS
Panel de administración con controles de simulación en tiempo real.
"""

import reflex as rx
from ecolink.state import State, WASTE_TYPES
from ecolink.components.ui import (
    navbar, notification_bar, section_title, card, green_button,
    route_status_badge, waste_chip, empty_state,
    C_GREEN_DARK, C_GREEN_MID, C_GREEN_PALE, C_ACCENT,
    C_BG, C_WHITE, C_TEXT, C_MUTED,
)

# Zonas reales de Mérida con waypoints definidos
ROUTE_ZONES = [
    "Centro Norte", "Col. Sur", "Zona Industrial",
    "Frac. Bello", "Altabrisa", "García Ginerés", "Itzimná",
]


def simulation_controls(r) -> rx.Component:
    """Botones de control de simulación según estado de la ruta."""
    return rx.hstack(
        # Iniciar
        rx.cond(
            r.status == "scheduled",
            rx.button(
                rx.icon("play", size=13), "▶ Iniciar",
                on_click=State.start_route_simulation(r.id),
                size="1", color_scheme="orange", variant="solid",
                cursor="pointer", font_weight="700",
                _hover={"opacity": "0.85"},
            ),
            rx.box(),
        ),
        # Avanzar manualmente
        rx.cond(
            r.status == "in_progress",
            rx.button(
                rx.icon("skip-forward", size=13), "⏩ Avanzar",
                on_click=State.advance_truck(r.id),
                size="1", color_scheme="blue", variant="soft",
                cursor="pointer",
            ),
            rx.box(),
        ),
        # Completar
        rx.cond(
            r.status == "in_progress",
            rx.button(
                rx.icon("check", size=13), "✅ Completar",
                on_click=State.update_route_status(r.id, "completed"),
                size="1", color_scheme="green", variant="soft",
                cursor="pointer",
            ),
            rx.box(),
        ),
        # Detener
        rx.cond(
            r.status == "in_progress",
            rx.button(
                rx.icon("square", size=13), "⛔ Detener",
                on_click=State.stop_route(r.id),
                size="1", color_scheme="red", variant="soft",
                cursor="pointer",
            ),
            rx.box(),
        ),
        # Reiniciar
        rx.cond(
            (r.status == "completed") | (r.status == "cancelled"),
            rx.button(
                rx.icon("refresh-cw", size=13), "🔄 Reiniciar",
                on_click=State.reset_route(r.id),
                size="1", color_scheme="gray", variant="soft",
                cursor="pointer",
            ),
            rx.box(),
        ),
        gap="0.35rem", flex_wrap="wrap", align="center",
    )


def route_admin_card(r) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text(r.name, font_weight="700", color=C_TEXT, font_size="0.92rem"),
                        route_status_badge(r.status),
                        flex_wrap="wrap", gap="0.4rem", align="center",
                    ),
                    rx.hstack(
                        waste_chip(r.waste_type),
                        rx.text("📍 " + r.zone, font_size="0.75rem", color=C_MUTED),
                        gap="0.4rem", align="center",
                    ),
                    # Posición actual del camión
                    rx.cond(
                        r.status == "in_progress",
                        rx.hstack(
                            rx.spinner(size="1", color="#ff6d00"),
                            rx.text(
                                "🚛 Camión en movimiento · avanza cada 5s",
                                font_size="0.73rem", color="#e65100", font_weight="600",
                            ),
                            align="center", gap="0.3rem",
                        ),
                        rx.box(),
                    ),
                    gap="0.3rem", align_items="flex-start", flex="1",
                ),
                rx.icon("chevron-right", color=C_MUTED, size=17),
                align="center", width="100%",
            ),
            # Controles de simulación
            simulation_controls(r),
            gap="0.5rem", width="100%",
        ),
        background=rx.cond(r.status == "in_progress", "#fff8f0", C_WHITE),
        border_radius="12px",
        padding="0.9rem 1.1rem",
        border=rx.cond(
            r.status == "in_progress",
            "1px solid #ffcc80",
            f"1px solid {C_GREEN_PALE}",
        ),
        box_shadow="0 1px 6px rgba(0,0,0,0.05)",
        width="100%",
        transition="all 0.15s",
    )


def admin_routes() -> rx.Component:
    return card(rx.vstack(
        section_title("truck", "Simulación de Rutas",
                      "Crea rutas y simula el movimiento del camión en tiempo real"),

        # Info de zonas disponibles
        rx.box(
            rx.hstack(
                rx.icon("info", size=14, color=C_GREEN_MID),
                rx.text(
                    "Al iniciar ▶ una ruta, el camión seguirá waypoints reales de esa zona en Mérida.",
                    font_size="0.78rem", color=C_MUTED,
                ),
                align="center", gap="0.4rem",
            ),
            background=C_GREEN_PALE,
            border_radius="8px",
            padding="0.5rem 0.8rem",
            margin_bottom="0.6rem",
        ),

        # Formulario nueva ruta
        rx.box(
            rx.text("➕ Nueva ruta de recolección",
                    font_weight="700", color=C_GREEN_DARK,
                    font_size="0.88rem", margin_bottom="0.6rem"),
            rx.vstack(
                rx.flex(
                    rx.input(
                        placeholder="Nombre de la ruta",
                        value=State.f_route_name,
                        on_change=State.set_f_route_name,
                        size="2", flex="3", min_width="180px",
                    ),
                    rx.select(
                        WASTE_TYPES,
                        value=State.f_route_waste,
                        on_change=State.set_f_route_waste,
                        size="2", flex="1", min_width="130px",
                    ),
                    rx.select(
                        ROUTE_ZONES,
                        value=State.f_route_zone,
                        on_change=State.set_f_route_zone,
                        placeholder="Zona de Mérida",
                        size="2", flex="2", min_width="160px",
                    ),
                    gap="0.55rem", wrap="wrap", align="center", width="100%",
                ),
                green_button(
                    "Crear ruta",
                    on_click=State.create_route,
                    icon_name="plus", size="2",
                ),
                gap="0.5rem", align_items="flex-start", width="100%",
            ),
            background="#f6fbf6",
            border="1px dashed #a5d6a7",
            border_radius="10px",
            padding="1rem",
            margin_bottom="0.85rem",
        ),

        # Lista de rutas
        rx.cond(
            State.routes.length() == 0,
            empty_state("No hay rutas. Crea la primera.", "truck"),
            rx.vstack(
                rx.foreach(State.routes, route_admin_card),
                gap="0.55rem", width="100%",
            ),
        ),

        # Botón ir al mapa
        rx.link(
            rx.button(
                rx.icon("map", size=15), "Ver mapa en tiempo real",
                variant="outline", size="2", cursor="pointer",
                color=C_GREEN_MID, border_color=C_GREEN_MID,
                width="100%",
            ),
            href="/map",
        ),

        gap="0.4rem", width="100%",
    ))


def admin_points() -> rx.Component:
    def point_row(p) -> rx.Component:
        return rx.box(
            rx.hstack(
                rx.icon("map-pin", color="#4caf50", size=15),
                rx.vstack(
                    rx.text(p.name, font_weight="600", color=C_TEXT, font_size="0.88rem"),
                    rx.text(p.address, font_size="0.75rem", color=C_MUTED),
                    rx.text("Tipos: " + p.types, font_size="0.7rem", color=C_MUTED),
                    gap="0.08rem", align_items="flex-start", flex="1",
                ),
                rx.badge(
                    "+" + p.pts.to_string() + " pts",
                    color_scheme="green", variant="soft",
                ),
                align="center", gap="0.65rem", width="100%",
            ),
            background=C_WHITE, border_radius="9px",
            padding="0.7rem 0.9rem",
            border=f"1px solid {C_GREEN_PALE}",
        )

    return card(rx.vstack(
        section_title("map", "Puntos de acopio",
                      "Agrega ubicaciones de reciclaje al mapa"),
        rx.box(
            rx.text("➕ Nuevo punto", font_weight="700", color=C_GREEN_DARK,
                    font_size="0.88rem", margin_bottom="0.6rem"),
            rx.vstack(
                rx.flex(
                    rx.input(placeholder="Nombre del punto",
                             value=State.f_point_name,
                             on_change=State.set_f_point_name,
                             size="2", flex="2", min_width="180px"),
                    rx.input(placeholder="Dirección completa",
                             value=State.f_point_address,
                             on_change=State.set_f_point_address,
                             size="2", flex="3", min_width="200px"),
                    gap="0.5rem", wrap="wrap", width="100%",
                ),
                rx.flex(
                    rx.input(placeholder="Latitud (20.9674)",
                             value=State.f_point_lat,
                             on_change=State.set_f_point_lat,
                             size="2", flex="1", min_width="120px"),
                    rx.input(placeholder="Longitud (-89.5926)",
                             value=State.f_point_lng,
                             on_change=State.set_f_point_lng,
                             size="2", flex="1", min_width="120px"),
                    rx.input(placeholder="Tipos CSV (pilas,aceite)",
                             value=State.f_point_types,
                             on_change=State.set_f_point_types,
                             size="2", flex="2", min_width="160px"),
                    rx.input(placeholder="Horario",
                             value=State.f_point_schedule,
                             on_change=State.set_f_point_schedule,
                             size="2", flex="2", min_width="140px"),
                    rx.input(placeholder="Puntos (50)",
                             value=State.f_point_pts,
                             on_change=State.set_f_point_pts,
                             size="2", flex="1", min_width="90px"),
                    gap="0.5rem", wrap="wrap", width="100%",
                ),
                green_button(
                    "Agregar punto de acopio",
                    on_click=State.create_point,
                    icon_name="plus", size="2",
                ),
                gap="0.5rem", align_items="flex-start", width="100%",
            ),
            background="#f6fbf6",
            border="1px dashed #a5d6a7",
            border_radius="10px",
            padding="1rem",
            margin_bottom="0.85rem",
        ),
        rx.cond(
            State.points.length() == 0,
            empty_state("No hay puntos de acopio. Agrega el primero.", "map-pin"),
            rx.vstack(
                rx.foreach(State.points, point_row),
                gap="0.4rem", width="100%",
            ),
        ),
        gap="0.4rem", width="100%",
    ))


@rx.page(
    route="/admin",
    title="EcoLink · Administración",
    on_load=[State.on_load, State.load_dashboard_data],
)
def admin_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            notification_bar(),
            # Header
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text("⚙️ Panel de Administración",
                                font_size="1.35rem", font_weight="800", color="white"),
                        rx.text(
                            "Municipio · Gestores de reciclaje · EcoLink Innovatec",
                            font_size="0.82rem", color="rgba(255,255,255,0.7)",
                        ),
                        align_items="flex-start", gap="0.2rem",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                rx.icon("map", size=14), "Ver mapa",
                                variant="outline", color="white",
                                border_color="rgba(255,255,255,0.55)",
                                cursor="pointer", size="2",
                                _hover={"background": "rgba(255,255,255,0.12)"},
                            ),
                            href="/map",
                        ),
                        rx.link(
                            rx.button(
                                rx.icon("layout-dashboard", size=14), "Dashboard",
                                variant="outline", color="white",
                                border_color="rgba(255,255,255,0.55)",
                                cursor="pointer", size="2",
                                _hover={"background": "rgba(255,255,255,0.12)"},
                            ),
                            href="/dashboard",
                        ),
                        gap="0.5rem",
                    ),
                    align="center", width="100%",
                ),
                background=f"linear-gradient(135deg, {C_GREEN_DARK}, #1b5e20)",
                border_radius="14px",
                padding="1.3rem 1.5rem",
                margin_bottom="1.1rem",
            ),
            # Contenido
            rx.cond(
                State.user_role != "admin",
                rx.callout(
                    "🚫 Esta sección es solo para administradores.",
                    icon="shield", color_scheme="red", variant="outline", size="2",
                ),
                rx.vstack(
                    admin_routes(),
                    admin_points(),
                    gap="1.1rem", width="100%",
                ),
            ),
            max_width="1080px",
            margin="0 auto",
            padding="0.75rem 1.1rem 2.5rem",
            width="100%",
        ),
        background=C_BG,
        min_height="100vh",
    )