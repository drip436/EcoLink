"""
ecolink/pages/admin.py
Panel de administración — accede a atributos de rx.Base (r.name, no r["name"])
"""

import reflex as rx
from ecolink.state import State, WASTE_TYPES
from ecolink.components.ui import (
    navbar, notification_bar, section_title, card, green_button,
    route_status_badge, waste_chip, empty_state,
    C_GREEN_DARK, C_GREEN_PALE,
    C_BG, C_WHITE, C_TEXT, C_MUTED,
)


def admin_routes() -> rx.Component:
    def route_row(r) -> rx.Component:
        return rx.box(
            rx.flex(
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
                    gap="0.3rem", align_items="flex-start", flex="1",
                ),
                rx.hstack(
                    rx.button(
                        "▶ Iniciar",
                        on_click=State.update_route_status(r.id, "in_progress"),
                        size="1", color_scheme="orange", variant="soft", cursor="pointer",
                        disabled=(r.status != "scheduled"),
                    ),
                    rx.button(
                        "✅ Completar",
                        on_click=State.update_route_status(r.id, "completed"),
                        size="1", color_scheme="green", variant="soft", cursor="pointer",
                        disabled=(r.status != "in_progress"),
                    ),
                    gap="0.4rem", flex_wrap="wrap", align="center",
                ),
                gap="0.75rem", wrap="wrap", align="center", width="100%",
            ),
            background=C_WHITE, border_radius="10px", padding="0.85rem 1.1rem",
            border=f"1px solid {C_GREEN_PALE}",
            box_shadow="0 1px 5px rgba(0,0,0,0.05)", width="100%",
        )

    return card(rx.vstack(
        section_title("truck", "Gestión de rutas", "Crea y controla las rutas de recolección"),
        # Formulario nueva ruta
        rx.box(
            rx.text("➕ Nueva ruta", font_weight="700", color=C_GREEN_DARK,
                    font_size="0.88rem", margin_bottom="0.6rem"),
            rx.flex(
                rx.input(placeholder="Nombre de la ruta",
                         value=State.f_route_name, on_change=State.set_f_route_name,
                         size="2", flex="3", min_width="180px"),
                rx.select(WASTE_TYPES, value=State.f_route_waste,
                          on_change=State.set_f_route_waste,
                          size="2", flex="1", min_width="130px"),
                rx.input(placeholder="Zona / Colonia",
                         value=State.f_route_zone, on_change=State.set_f_route_zone,
                         size="2", flex="2", min_width="140px"),
                green_button("Crear", on_click=State.create_route, icon_name="plus", size="2"),
                gap="0.55rem", wrap="wrap", align="center", width="100%",
            ),
            background="#f6fbf6", border="1px dashed #a5d6a7",
            border_radius="10px", padding="1rem", margin_bottom="0.85rem",
        ),
        rx.cond(
            State.routes.length() == 0,
            empty_state("No hay rutas. Crea la primera.", "truck"),
            rx.vstack(rx.foreach(State.routes, route_row), gap="0.5rem", width="100%"),
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
                rx.badge("+" + p.pts.to_string() + " pts",
                         color_scheme="green", variant="soft"),
                align="center", gap="0.65rem", width="100%",
            ),
            background=C_WHITE, border_radius="9px",
            padding="0.7rem 0.9rem", border=f"1px solid {C_GREEN_PALE}",
        )

    return card(rx.vstack(
        section_title("map", "Puntos de acopio", "Agrega ubicaciones de reciclaje al mapa"),
        # Formulario nuevo punto
        rx.box(
            rx.text("➕ Nuevo punto", font_weight="700", color=C_GREEN_DARK,
                    font_size="0.88rem", margin_bottom="0.6rem"),
            rx.vstack(
                rx.flex(
                    rx.input(placeholder="Nombre del punto",
                             value=State.f_point_name, on_change=State.set_f_point_name,
                             size="2", flex="2", min_width="180px"),
                    rx.input(placeholder="Dirección completa",
                             value=State.f_point_address, on_change=State.set_f_point_address,
                             size="2", flex="3", min_width="200px"),
                    gap="0.5rem", wrap="wrap", width="100%",
                ),
                rx.flex(
                    rx.input(placeholder="Latitud (20.9674)",
                             value=State.f_point_lat, on_change=State.set_f_point_lat,
                             size="2", flex="1", min_width="120px"),
                    rx.input(placeholder="Longitud (-89.5926)",
                             value=State.f_point_lng, on_change=State.set_f_point_lng,
                             size="2", flex="1", min_width="120px"),
                    rx.input(placeholder="Tipos CSV (pilas,aceite)",
                             value=State.f_point_types, on_change=State.set_f_point_types,
                             size="2", flex="2", min_width="160px"),
                    rx.input(placeholder="Horario",
                             value=State.f_point_schedule, on_change=State.set_f_point_schedule,
                             size="2", flex="2", min_width="140px"),
                    rx.input(placeholder="Puntos (50)",
                             value=State.f_point_pts, on_change=State.set_f_point_pts,
                             size="2", flex="1", min_width="90px"),
                    gap="0.5rem", wrap="wrap", width="100%",
                ),
                green_button("Agregar punto de acopio", on_click=State.create_point,
                             icon_name="plus", size="2"),
                gap="0.5rem", align_items="flex-start", width="100%",
            ),
            background="#f6fbf6", border="1px dashed #a5d6a7",
            border_radius="10px", padding="1rem", margin_bottom="0.85rem",
        ),
        rx.cond(
            State.points.length() == 0,
            empty_state("No hay puntos de acopio. Agrega el primero.", "map-pin"),
            rx.vstack(rx.foreach(State.points, point_row), gap="0.4rem", width="100%"),
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
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text("⚙️ Panel de Administración",
                                font_size="1.35rem", font_weight="800", color="white"),
                        rx.text("Municipio / Gestores de reciclaje · EcoLink Innovatec",
                                font_size="0.82rem", color="rgba(255,255,255,0.7)"),
                        align_items="flex-start", gap="0.2rem",
                    ),
                    rx.spacer(),
                    rx.link(
                        rx.button(
                            rx.icon("layout-dashboard", size=14), "Ver dashboard",
                            variant="outline", color="white",
                            border_color="rgba(255,255,255,0.55)", cursor="pointer", size="2",
                            _hover={"background": "rgba(255,255,255,0.12)"},
                        ),
                        href="/dashboard",
                    ),
                    align="center", width="100%",
                ),
                background=f"linear-gradient(135deg, {C_GREEN_DARK}, #1b5e20)",
                border_radius="14px", padding="1.3rem 1.5rem", margin_bottom="1.1rem",
            ),
            rx.cond(
                State.user_role != "admin",
                rx.callout(
                    "🚫 Esta sección es solo para administradores.",
                    icon="shield", color_scheme="red", variant="outline", size="2",  # ✅ CAMBIADO: "outline"
                ),
                rx.vstack(
                    admin_routes(),
                    admin_points(),
                    gap="1.1rem", width="100%",
                ),
            ),
            max_width="1080px", margin="0 auto",
            padding="0.75rem 1.1rem 2.5rem", width="100%",
        ),
        background=C_BG, min_height="100vh",
    )