"""
ecolink/pages/dashboard.py
Panel principal del ciudadano — accede a atributos de rx.Base (r.name, no r["name"])
"""

import reflex as rx
from ecolink.state import State, WASTE_TYPES
from ecolink.components.ui import (
    navbar, notification_bar, stat_card, section_title, card,
    route_status_badge, waste_chip, level_icon, empty_state, green_button,
    C_GREEN_DARK, C_GREEN_MID, C_GREEN_LIGHT, C_ACCENT, C_GOLD,
    C_BG, C_WHITE, C_TEXT, C_MUTED, C_GREEN_PALE,
)


# ═══ TAB INICIO ══════════════════════════════════════════════════════════════

def tab_home() -> rx.Component:
    return rx.vstack(
        # Stats
        rx.flex(
            stat_card("star",    "Puntos totales",   State.user_points.to_string(),  C_GREEN_MID),
            stat_card("recycle", "Acciones",          State.user_actions.to_string(), C_ACCENT),
            stat_card("truck",   "Rutas activas",     State.routes.length().to_string(), "#e67e22"),
            stat_card("map-pin", "Puntos de acopio",  State.points.length().to_string(), "#8e44ad"),
            gap="0.85rem",
            wrap="wrap",
            width="100%",
        ),

        # Nivel del usuario
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text("🏆 Nivel actual:", font_weight="600", color=C_GREEN_DARK),
                        rx.badge(
                            level_icon(State.user_level), " ", State.user_level,
                            color_scheme="green", variant="solid", font_size="0.9rem",
                        ),
                        align="center", gap="0.5rem",
                    ),
                    rx.text(State.user_points.to_string() + " puntos acumulados",
                            font_size="0.83rem", color=C_MUTED),
                    rx.text("🌱 Semilla→100  🌿 Brote→300  🍃 Hoja→700  🌳 Árbol→1500  🌲 Bosque",
                            font_size="0.7rem", color=C_MUTED),
                    align_items="flex-start", gap="0.25rem", flex="1",
                ),
                rx.text("♻️", font_size="2.8rem"),
                align="center", width="100%", gap="1rem",
            ),
            background=f"linear-gradient(135deg, {C_GREEN_PALE}, #c8e6c9)",
            border_radius="14px", padding="1.1rem 1.4rem",
            border="1px solid #a5d6a7", width="100%",
        ),

        # Formulario recogida pendiente
        card(rx.vstack(
            section_title("package", "Solicitar recogida", "Gana 30 puntos por cada solicitud"),
            rx.flex(
                rx.vstack(
                    rx.text("Dirección", font_size="0.82rem", font_weight="600", color=C_GREEN_DARK),
                    rx.input(
                        placeholder="Calle, número, colonia...",
                        value=State.f_pickup_address,
                        on_change=State.set_f_pickup_address,
                        width="100%", size="2",
                    ),
                    align_items="flex-start", gap="0.2rem", flex="2", min_width="200px",
                ),
                rx.vstack(
                    rx.text("Tipo de residuo", font_size="0.82rem", font_weight="600", color=C_GREEN_DARK),
                    rx.select(
                        WASTE_TYPES,
                        value=State.f_pickup_waste_type,
                        on_change=State.set_f_pickup_waste_type,
                        width="100%", size="2",
                    ),
                    align_items="flex-start", gap="0.2rem", flex="1", min_width="150px",
                ),
                gap="0.7rem", wrap="wrap", width="100%", align="end",
            ),
            rx.input(
                placeholder="Notas adicionales (opcional)",
                value=State.f_pickup_notes,
                on_change=State.set_f_pickup_notes,
                width="100%", size="2",
            ),
            green_button("Solicitar recogida (+30 pts)", on_click=State.request_pickup,
                         icon_name="package-plus", size="3", width="100%"),
            gap="0.6rem", align_items="stretch", width="100%",
        )),

        # Mis últimas solicitudes
        rx.cond(
            State.my_pickups.length() > 0,
            card(rx.vstack(
                section_title("list", "Mis solicitudes recientes", ""),
                rx.vstack(
                    rx.foreach(
                        State.my_pickups,
                        lambda p: rx.box(
                            rx.hstack(
                                rx.icon("package", size=15, color=C_ACCENT),
                                rx.text(p.address, font_size="0.83rem", flex="1", color=C_TEXT),
                                waste_chip(p.waste),
                                rx.match(
                                    p.status,
                                    ("pending",   rx.badge("⏳ Pendiente", color_scheme="yellow", variant="soft", font_size="0.7rem")),
                                    ("collected", rx.badge("✅ Recogido",  color_scheme="green",  variant="soft", font_size="0.7rem")),
                                    rx.badge(p.status, color_scheme="gray", variant="soft", font_size="0.7rem"),
                                ),
                                rx.text(p.date, font_size="0.7rem", color=C_MUTED),
                                align="center", gap="0.5rem", flex_wrap="wrap", width="100%",
                            ),
                            padding="0.6rem 0.8rem", border_radius="8px",
                            border=f"1px solid {C_GREEN_PALE}",
                        )
                    ),
                    gap="0.4rem", width="100%",
                ),
                gap="0.5rem", width="100%",
            )),
            rx.box(),
        ),
        gap="1rem", width="100%",
    )


# ═══ TAB RUTAS ═══════════════════════════════════════════════════════════════

def tab_routes() -> rx.Component:
    def route_card(r) -> rx.Component:
        return rx.box(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text(r.name, font_weight="700", color=C_TEXT),
                        route_status_badge(r.status),
                        flex_wrap="wrap", gap="0.4rem", align="center",
                    ),
                    rx.hstack(
                        waste_chip(r.waste_type),
                        rx.text("📍 " + r.zone, font_size="0.76rem", color=C_MUTED),
                        gap="0.4rem", align="center",
                    ),
                    rx.cond(
                        r.status == "in_progress",
                        rx.hstack(
                            rx.spinner(size="1", color=C_GREEN_LIGHT),
                            rx.text("🚛 Camión en movimiento",
                                    font_size="0.75rem", color=C_GREEN_MID, font_weight="600"),
                            align="center", gap="0.35rem",
                        ),
                        rx.box(),
                    ),
                    align_items="flex-start", gap="0.3rem", flex="1",
                ),
                rx.icon("chevron-right", color=C_MUTED, size=17),
                align="center", width="100%",
            ),
            background=C_WHITE, border_radius="12px", padding="0.9rem 1.1rem",
            border=f"1px solid {C_GREEN_PALE}",
            box_shadow="0 1px 6px rgba(0,0,0,0.05)",
            _hover={"border_color": C_GREEN_LIGHT, "transform": "translateX(3px)"},
            transition="all 0.15s", width="100%",
        )

    return rx.vstack(
        section_title("truck", "Rutas de recolección", "Consulta las rutas programadas"),
        rx.callout("💡 Las rutas 'En curso' actualizan su posición cada 10 s (simulado).",
                   color_scheme="blue", variant="soft", size="1"),
        rx.cond(
            State.routes.length() == 0,
            empty_state("No hay rutas disponibles aún", "truck"),
            rx.vstack(rx.foreach(State.routes, route_card), gap="0.55rem", width="100%"),
        ),
        gap="0.65rem", width="100%",
    )


# ═══ TAB PUNTOS DE ACOPIO ════════════════════════════════════════════════════

def tab_points() -> rx.Component:
    def point_card(p) -> rx.Component:
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("map-pin", color=C_GREEN_LIGHT, size=17),
                    rx.text(p.name, font_weight="700", color=C_TEXT),
                    rx.spacer(),
                    rx.badge("+" + p.pts.to_string() + " pts",
                             color_scheme="blue", variant="soft", font_weight="700"),
                    align="center", width="100%",
                ),
                rx.text(p.address, font_size="0.8rem", color=C_MUTED),
                rx.hstack(
                    rx.foreach(p.types.split(","), lambda t: waste_chip(t)),
                    flex_wrap="wrap", gap="0.3rem",
                ),
                rx.text("🕐 " + p.schedule, font_size="0.75rem", color=C_MUTED),
                rx.button(
                    rx.icon("check-circle", size=13),
                    "Registrar visita y ganar puntos",
                    on_click=State.register_dropoff(p.id),
                    size="1", variant="soft", color_scheme="cyan",
                    cursor="pointer", width="100%",
                    _hover={"background": C_GREEN_PALE},
                ),
                align_items="flex-start", gap="0.4rem", width="100%",
            ),
            background=C_WHITE, border_radius="13px", padding="1rem 1.2rem",
            box_shadow="0 2px 8px rgba(0,0,0,0.07)",
            border=f"1px solid {C_GREEN_PALE}",
            _hover={"border_color": C_GREEN_LIGHT},
            transition="all 0.15s",
        )

    return rx.vstack(
        section_title("map", "Puntos de acopio", "Lleva residuos y gana puntos"),
        rx.callout("Registra tu visita al llegar para sumar puntos automáticamente.",
                   color_scheme="green", variant="soft", size="1"),
        rx.cond(
            State.points.length() == 0,
            empty_state("No hay puntos de acopio registrados", "map-pin"),
            rx.grid(
                rx.foreach(State.points, point_card),
                columns=rx.breakpoints({"0px": "1", "768px": "2"}),
                gap="0.7rem", width="100%",
            ),
        ),
        gap="0.65rem", width="100%",
    )


# ═══ TAB HISTORIAL ═══════════════════════════════════════════════════════════

def tab_history() -> rx.Component:
    def hist_row(h) -> rx.Component:
        return rx.box(
            rx.hstack(
                rx.box(
                    rx.cond(
                        h.action_type == "pickup",
                        rx.icon("package", size=16, color=C_ACCENT),
                        rx.icon("map-pin", size=16, color=C_GREEN_LIGHT),
                    ),
                    background=rx.cond(h.action_type == "pickup", "#e0f7fa", C_GREEN_PALE),
                    padding="0.45rem", border_radius="7px",
                ),
                rx.vstack(
                    rx.text(h.desc, font_size="0.83rem", color=C_TEXT, font_weight="500"),
                    rx.hstack(
                        waste_chip(h.waste),
                        rx.text(h.date, font_size="0.7rem", color=C_MUTED),
                        gap="0.35rem", align="center",
                    ),
                    gap="0.12rem", align_items="flex-start", flex="1",
                ),
                rx.badge("+" + h.pts.to_string() + " pts",
                         color_scheme="green", variant="solid", font_weight="700"),
                align="center", gap="0.65rem", width="100%",
            ),
            background=C_WHITE, border_radius="9px", padding="0.65rem 0.9rem",
            border=f"1px solid {C_GREEN_PALE}",
        )

    return rx.vstack(
        section_title("clock", "Historial de reciclaje", "Todas tus acciones eco-responsables"),
        rx.cond(
            State.history.length() == 0,
            empty_state("Aún no tienes acciones. ¡Empieza a reciclar!", "clock"),
            rx.vstack(rx.foreach(State.history, hist_row), gap="0.4rem", width="100%"),
        ),
        gap="0.65rem", width="100%",
    )


# ═══ TAB RECOMPENSAS ═════════════════════════════════════════════════════════

def tab_rewards() -> rx.Component:
    def reward_card(r) -> rx.Component:
        can_claim = State.user_points >= r.pts
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("🎁", font_size="1.4rem"),
                    rx.vstack(
                        rx.text(r.title, font_weight="700", color=C_TEXT, font_size="0.95rem"),
                        rx.text(r.partner, font_size="0.74rem", color=C_MUTED),
                        gap="0.1rem", align_items="flex-start",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.badge(r.pts.to_string() + " pts",
                                 color_scheme="yellow", variant="solid", font_weight="700"),
                        rx.text("requeridos", font_size="0.66rem", color=C_MUTED, text_align="right"),
                        align="end", gap="0.1rem",
                    ),
                    align="center", width="100%",
                ),
                rx.text(r.desc, font_size="0.8rem", color=C_MUTED),
                rx.button(
                    rx.icon("gift", size=13), "Canjear",
                    on_click=State.claim_reward(r.id),
                    width="100%", size="2",
                    background=rx.cond(
                        can_claim,
                        f"linear-gradient(135deg, {C_GREEN_MID}, {C_ACCENT})",
                        "#e5e7eb",
                    ),
                    color=rx.cond(can_claim, "white", "#9ca3af"),
                    font_weight="700",
                    cursor=rx.cond(can_claim, "pointer", "not-allowed"),
                    disabled=~can_claim,
                ),
                gap="0.45rem", align_items="stretch",
            ),
            background=C_WHITE, border_radius="13px", padding="1.1rem",
            border=rx.cond(can_claim, f"1px solid {C_GREEN_LIGHT}", f"1px solid {C_GREEN_PALE}"),
            box_shadow="0 2px 8px rgba(0,0,0,0.06)",
            opacity=rx.cond(can_claim, "1", "0.72"),
            transition="all 0.15s",
        )

    return rx.vstack(
        section_title("gift", "Recompensas", "Canjea tus puntos por beneficios reales"),
        rx.callout(
            "Tus puntos: " + State.user_points.to_string() +
            " · El botón se activa cuando tienes suficientes.",
            color_scheme="yellow", variant="soft", size="1",
        ),
        rx.cond(
            State.rewards.length() == 0,
            empty_state("No hay recompensas disponibles", "gift"),
            rx.grid(
                rx.foreach(State.rewards, reward_card),
                columns=rx.breakpoints({"0px": "1", "640px": "2", "1024px": "3"}),
                gap="0.7rem", width="100%",
            ),
        ),
        gap="0.65rem", width="100%",
    )


# ═══ TAB RANKING ═════════════════════════════════════════════════════════════

def tab_ranking() -> rx.Component:
    def rank_row(u) -> rx.Component:
        is_me = u.id == State.user_id
        return rx.box(
            rx.hstack(
                rx.text(
                    rx.cond(u.rank == 1, "🥇",
                    rx.cond(u.rank == 2, "🥈",
                    rx.cond(u.rank == 3, "🥉",
                    "#" + u.rank.to_string()))),
                    font_size=rx.cond(u.rank <= 3, "1.3rem", "0.95rem"),
                    font_weight="800",
                    color=rx.cond(u.rank <= 3, C_GOLD, C_MUTED),
                    min_width="2.3rem", text_align="center",
                ),
                rx.vstack(
                    rx.text(u.name, font_weight="600", color=C_TEXT, font_size="0.9rem"),
                    rx.badge(
                        level_icon(u.level), " ", u.level,
                        color_scheme="green", variant="soft", font_size="0.72rem",
                    ),
                    gap="0.15rem", align_items="flex-start", flex="1",
                ),
                rx.vstack(
                    rx.text(u.points.to_string() + " pts",
                            font_weight="800", color=C_GREEN_MID, font_size="0.9rem"),
                    rx.text(u.actions.to_string() + " acciones",
                            font_size="0.7rem", color=C_MUTED),
                    align="end", gap="0.1rem",
                ),
                align="center", gap="0.7rem", width="100%",
            ),
            background=rx.cond(
                is_me,
                f"linear-gradient(135deg, {C_GREEN_PALE}, #c8e6c9)",
                C_WHITE,
            ),
            border=rx.cond(is_me, f"2px solid {C_GREEN_LIGHT}", f"1px solid {C_GREEN_PALE}"),
            border_radius="11px", padding="0.8rem 1.1rem",
            box_shadow=rx.cond(is_me, "0 4px 14px rgba(76,175,80,0.18)", "0 1px 5px rgba(0,0,0,0.04)"),
        )

    return rx.vstack(
        section_title("trophy", "Ranking de recicladores", "Top 10 de tu comunidad"),
        rx.callout("Tu posición aparece resaltada en verde. ¡Sigue reciclando para subir!",
                   color_scheme="green", variant="soft", size="1"),
        rx.cond(
            State.ranking.length() == 0,
            empty_state("Aún no hay suficientes usuarios para el ranking", "trophy"),
            rx.vstack(rx.foreach(State.ranking, rank_row), gap="0.45rem", width="100%"),
        ),
        gap="0.65rem", width="100%",
    )


# ═══ PÁGINA DASHBOARD ════════════════════════════════════════════════════════

@rx.page(
    route="/dashboard",
    title="EcoLink · Dashboard",
    on_load=[State.on_load, State.load_dashboard_data, State.seed_if_empty],
)
def dashboard_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            notification_bar(),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(rx.hstack(rx.icon("home",    size=14), rx.text("Inicio", color="black"),      gap="0.3rem", align="center"), value="home"),
                    rx.tabs.trigger(rx.hstack(rx.icon("truck",   size=14), rx.text("Rutas", color="black"),       gap="0.3rem", align="center"), value="routes"),
                    rx.tabs.trigger(rx.hstack(rx.icon("map-pin", size=14), rx.text("Acopio", color="black"),      gap="0.3rem", align="center"), value="points"),
                    rx.tabs.trigger(rx.hstack(rx.icon("clock",   size=14), rx.text("Historial", color="black"),   gap="0.3rem", align="center"), value="history"),
                    rx.tabs.trigger(rx.hstack(rx.icon("gift",    size=14), rx.text("Recompensas", color="black"), gap="0.3rem", align="center"), value="rewards"),
                    rx.tabs.trigger(rx.hstack(rx.icon("trophy",  size=14), rx.text("Ranking", color="black"),     gap="0.3rem", align="center"), value="ranking"),
                    overflow_x="auto", width="100%",
                ),
                rx.tabs.content(tab_home(),    value="home",    padding_top="1.1rem"),
                rx.tabs.content(tab_routes(),  value="routes",  padding_top="1.1rem"),
                rx.tabs.content(tab_points(),  value="points",  padding_top="1.1rem"),
                rx.tabs.content(tab_history(), value="history", padding_top="1.1rem"),
                rx.tabs.content(tab_rewards(), value="rewards", padding_top="1.1rem"),
                rx.tabs.content(tab_ranking(), value="ranking", padding_top="1.1rem"),
                default_value="home", width="100%",
            ),
            max_width="1080px", margin="0 auto",
            padding="0.75rem 1.1rem 2.5rem", width="100%",
        ),
        background=C_BG, min_height="100vh",
    )
