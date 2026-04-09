"""
ecolink/components/ui.py
═══════════════════════════════════════════════════════════════════════════════
Componentes visuales reutilizables de EcoLink.
Paleta de colores y sistema de diseño coherente.
═══════════════════════════════════════════════════════════════════════════════
"""

import reflex as rx
from ecolink.state import State

# ── Paleta ────────────────────────────────────────────────────────────────────
C_GREEN_DARK  = "#1a4731"
C_GREEN_MID   = "#2d7a4f"
C_GREEN_LIGHT = "#4caf50"
C_GREEN_PALE  = "#e8f5e9"
C_ACCENT      = "#00bfa5"
C_GOLD        = "#f59e0b"
C_BG          = "#f0f7f0"
C_WHITE       = "#ffffff"
C_TEXT        = "#1b2d1f"
C_MUTED       = "#6b8c71"
C_ERROR       = "#dc2626"
C_SUCCESS_BG  = "#d1fae5"
C_ERROR_BG    = "#fee2e2"


def logo(size: str = "1.5rem") -> rx.Component:
    return rx.hstack(
        rx.icon("leaf", color=C_GREEN_LIGHT, size=24),
        rx.text(
            "Eco",
            rx.text.span("Link", color=C_ACCENT),
            font_size=size,
            font_weight="800",
            color="white",
            font_family="Georgia, serif",
        ),
        align="center",
        gap="0.35rem",
    )


def navbar() -> rx.Component:
    """Barra de navegación superior — sticky."""
    return rx.box(
        rx.hstack(
            logo("1.55rem"),
            rx.spacer(),
            # Puntos y nivel
            rx.hstack(
                rx.badge(
                    "⭐ " + State.user_points.to_string() + " pts",
                    color_scheme="yellow",
                    variant="solid",
                    font_weight="700",
                    font_size="0.82rem",
                ),
                rx.badge(
                    State.user_level,
                    color_scheme="green",
                    variant="soft",
                    font_size="0.8rem",
                ),
                rx.text(
                    State.user_name,
                    color="white",
                    font_size="0.88rem",
                    font_weight="600",
                    display=["none", "none", "block"],
                ),
                # Botón admin
                rx.cond(
                    State.user_role == "admin",
                    rx.link(
                        rx.button(
                            rx.icon("settings", size=14),
                            "Admin",
                            variant="ghost",
                            color="white",
                            size="2",
                            cursor="pointer",
                            _hover={"background": "rgba(255,255,255,0.15)"},
                        ),
                        href="/admin",
                    ),
                    rx.box(),
                ),
                rx.button(
                    rx.icon("log-out", size=15),
                    on_click=State.logout,
                    variant="ghost",
                    color="white",
                    size="2",
                    cursor="pointer",
                    _hover={"background": "rgba(255,255,255,0.15)"},
                ),
                align="center",
                gap="0.6rem",
            ),
            align="center",
            width="100%",
        ),
        background=f"linear-gradient(135deg, {C_GREEN_DARK} 0%, {C_GREEN_MID} 100%)",
        padding="0.85rem 1.4rem",
        position="sticky",
        top="0",
        z_index="100",
        box_shadow="0 2px 16px rgba(0,0,0,0.2)",
        width="100%",
    )


def notification_bar() -> rx.Component:
    """Barra de notificación temporal en la parte superior del contenido."""
    
    return rx.cond(
        State.notification != "",
        rx.box(
            rx.hstack(
                rx.text(State.notification, font_weight="600", font_size="0.9rem"),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x", size=13),
                    on_click=State.clear_notification,
                    variant="ghost",
                    size="1",
                    cursor="pointer",
                ),
                align="center",
                width="100%",
            ),
            background=rx.cond(
                State.notif_type == "success", C_SUCCESS_BG,
                rx.cond(State.notif_type == "error", C_ERROR_BG, "#dbeafe"),
            ),
            color=rx.cond(
                State.notif_type == "success", "#065f46",
                rx.cond(State.notif_type == "error", "#7f1d1d", "#1e3a5f"),
            ),
            border_radius="10px",
            padding="0.7rem 1.1rem",
            margin="0.75rem 0 0",
            border=rx.cond(
                State.notif_type == "success", "1px solid #6ee7b7",
                rx.cond(State.notif_type == "error", "1px solid #fca5a5", "1px solid #93c5fd"),
            ),
        ),
        rx.box(),
    )


def stat_card(icon_name: str, label: str, value: rx.Component, color: str = C_GREEN_MID) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(icon_name, size=22, color="white"),
                background=color,
                padding="0.6rem",
                border_radius="10px",
            ),
            rx.text(value, font_size="1.75rem", font_weight="800", color=C_TEXT),
            rx.text(label, font_size="0.75rem", color=C_MUTED, text_align="center"),
            align="center",
            gap="0.35rem",
        ),
        background=C_WHITE,
        border_radius="14px",
        padding="1.1rem 0.9rem",
        box_shadow="0 2px 10px rgba(0,0,0,0.07)",
        flex="1",
        min_width="120px",
        border=f"1px solid {C_GREEN_PALE}",
        _hover={"transform": "translateY(-2px)", "box_shadow": "0 6px 18px rgba(0,0,0,0.1)"},
        transition="all 0.18s ease",
    )


def section_title(icon_name: str, title: str, subtitle: str = "") -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.icon(icon_name, size=18, color="white"),
            background=f"linear-gradient(135deg, {C_GREEN_MID}, {C_ACCENT})",
            padding="0.45rem",
            border_radius="9px",
        ),
        rx.vstack(
            rx.text(title, font_size="1.1rem", font_weight="800", color=C_TEXT),
            rx.text(subtitle, font_size="0.75rem", color=C_MUTED) if subtitle else rx.box(),
            gap="0",
            align_items="flex-start",
        ),
        align="center",
        gap="0.55rem",
        margin_bottom="0.9rem",
    )


def card(children: rx.Component, **kwargs) -> rx.Component:
    """Contenedor tipo card con sombra suave."""
    return rx.box(
        children,
        background=C_WHITE,
        border_radius="14px",
        padding="1.2rem 1.4rem",
        box_shadow="0 2px 12px rgba(0,0,0,0.07)",
        border=f"1px solid {C_GREEN_PALE}",
        width="100%",
        **kwargs,
    )


def route_status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        ("scheduled",   rx.badge("🕐 Programada", color_scheme="blue",   variant="soft")),
        ("in_progress", rx.badge("🚛 En curso",    color_scheme="orange", variant="solid")),
        ("completed",   rx.badge("✅ Completada",  color_scheme="green",  variant="soft")),
        ("cancelled",   rx.badge("❌ Cancelada",   color_scheme="red",    variant="soft")),
        rx.badge(status, color_scheme="gray", variant="soft"),
    )


def level_icon(level: str) -> rx.Component:
    return rx.match(
        level,
        ("Semilla", rx.text("🌱")),
        ("Brote",   rx.text("🌿")),
        ("Hoja",    rx.text("🍃")),
        ("Árbol",   rx.text("🌳")),
        ("Bosque",  rx.text("🌲")),
        rx.text("🌱"),
    )


def waste_chip(wtype: str) -> rx.Component:
    scheme_map = {
        "plástico": "blue", "orgánico": "green", "vidrio": "cyan",
        "papel": "yellow", "electronico": "purple", "pilas": "orange",
        "aceite": "brown", "ropa": "pink", "general": "gray",
    }
    return rx.badge(
        wtype,
        color_scheme=scheme_map.get(wtype.lower(), "gray"),
        variant="soft",
        font_size="0.72rem",
    )


def empty_state(msg: str, icon_name: str = "inbox") -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon(icon_name, size=38, color=C_MUTED, opacity="0.45"),
            rx.text(msg, color=C_MUTED, font_size="0.88rem", text_align="center"),
            align="center",
            gap="0.4rem",
        ),
        padding="2rem",
    )


def green_button(label: str, on_click=None, icon_name: str = "", size: str = "2", **kw) -> rx.Component:
    return rx.button(
        rx.icon(icon_name, size=15) if icon_name else rx.box(),
        label,
        on_click=on_click,
        background=f"linear-gradient(135deg, {C_GREEN_MID}, {C_ACCENT})",
        color="white",
        font_weight="700",
        size=size,
        cursor="pointer",
        _hover={"opacity": "0.88", "transform": "translateY(-1px)"},
        transition="all 0.18s",
        **kw,
    )


def input_field(label: str, placeholder: str, value: rx.Var, on_change, type_: str = "text") -> rx.Component:
    return rx.vstack(
        rx.text(label, font_size="0.82rem", font_weight="600", color=C_GREEN_DARK),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            type=type_,
            width="100%",
            size="3",
            border_color=C_GREEN_PALE,
            _focus={"border_color": C_GREEN_MID, "box_shadow": f"0 0 0 2px {C_GREEN_PALE}"},
        ),
        align_items="flex-start",
        gap="0.25rem",
        width="100%",
    )
