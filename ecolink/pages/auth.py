"""
ecolink/pages/auth.py
Páginas de inicio de sesión y registro.
Toda la lógica vive en State (state.py) — aquí solo UI.
"""

import reflex as rx
from ecolink.state import State
from ecolink.components.ui import (
    logo, input_field,
    C_GREEN_DARK, C_GREEN_MID, C_ACCENT, C_BG, C_WHITE, C_MUTED,
)


def _auth_shell(title: str, subtitle: str, body: rx.Component, footer: rx.Component) -> rx.Component:
    """Layout base para las páginas de autenticación."""
    return rx.center(
        rx.box(
            # ── Cabecera verde ──────────────────────────────────────────
            rx.vstack(
                logo("2rem"),
                rx.text(
                    "Innovatec · Gestión Circular de Residuos",
                    color="rgba(255,255,255,0.7)",
                    font_size="0.78rem",
                    text_align="center",
                ),
                align="center",
                gap="0.3rem",
                padding="1.75rem 2rem 1.5rem",
                background=f"linear-gradient(135deg, {C_GREEN_DARK}, {C_GREEN_MID})",
                border_radius="18px 18px 0 0",
                width="100%",
            ),
            # ── Cuerpo del card ─────────────────────────────────────────
            rx.vstack(
                rx.text(title,    font_size="1.25rem", font_weight="800", color=C_GREEN_DARK),
                rx.text(subtitle, font_size="0.82rem", color=C_MUTED),
                rx.divider(margin_y="0.6rem"),
                body,
                rx.divider(margin_y="0.4rem"),
                footer,
                gap="0.45rem",
                padding="1.4rem 1.8rem 1.9rem",
                align_items="stretch",
            ),
            width=["95vw", "420px"],
            background=C_WHITE,
            border_radius="18px",
            box_shadow="0 24px 64px rgba(0,0,0,0.14)",
            overflow="hidden",
        ),
        min_height="100vh",
        background=f"linear-gradient(150deg, {C_BG} 0%, #c8e6c9 100%)",
    )


# ─── LOGIN ────────────────────────────────────────────────────────────────────

@rx.page(route="/login", title="EcoLink · Iniciar sesión")
def login_page() -> rx.Component:
    body = rx.vstack(
        # Error
        rx.cond(
            State.notification != "",
            rx.callout(
                State.notification,
                icon="triangle_alert",
                color_scheme="red",
                variant="soft",
                size="1",
            ),
            rx.box(),
        ),
        input_field("Correo electrónico", "tu@correo.com",
                    State.f_login_email, State.set_f_login_email, "email"),
        input_field("Contraseña", "••••••",
                    State.f_login_pass, State.set_f_login_pass, "password"),
        rx.button(
            rx.cond(State.is_loading, rx.spinner(size="2"), rx.icon("log-in", size=15)),
            rx.cond(State.is_loading, "Iniciando...", "Iniciar sesión"),
            on_click=State.login,
            width="100%",
            size="3",
            background=f"linear-gradient(135deg, {C_GREEN_MID}, {C_ACCENT})",
            color="white",
            font_weight="700",
            cursor="pointer",
            _hover={"opacity": "0.9"},
            disabled=State.is_loading,
            margin_top="0.3rem",
        ),
        gap="0.55rem",
        align_items="stretch",
        width="100%",
    )
    footer = rx.center(
        rx.text(
            "¿No tienes cuenta? ",
            rx.link("Regístrate aquí", href="/register", color=C_ACCENT, font_weight="700"),
            font_size="0.84rem",
            color=C_MUTED,
        )
    )
    return _auth_shell("Bienvenido de vuelta 👋", "Inicia sesión en tu cuenta EcoLink", body, footer)

# ─── REGISTRO ─────────────────────────────────────────────────────────────────

@rx.page(route="/register", title="EcoLink · Crear cuenta")
def register_page() -> rx.Component:
    body = rx.vstack(
        rx.cond(
            State.notification != "",
            rx.callout(
                State.notification,
                icon="triangle_alert",
                color_scheme="red",
                variant="soft",
                size="1",
            ),
            rx.box(),
        ),
        input_field("Nombre completo", "Tu nombre y apellido",
                    State.f_reg_name, State.set_f_reg_name),
        input_field("Correo electrónico", "tu@correo.com",
                    State.f_reg_email, State.set_f_reg_email, "email"),
        input_field("Contraseña", "Mínimo 6 caracteres",
                    State.f_reg_pass, State.set_f_reg_pass, "password"),
        rx.button(
            rx.cond(State.is_loading, rx.spinner(size="2"), rx.icon("user-plus", size=15)),
            rx.cond(State.is_loading, "Creando cuenta...", "Crear cuenta"),
            on_click=State.register,
            width="100%",
            size="3",
            background=f"linear-gradient(135deg, {C_GREEN_MID}, {C_ACCENT})",
            color="white",
            font_weight="700",
            cursor="pointer",
            _hover={"opacity": "0.9"},
            disabled=State.is_loading,
            margin_top="0.3rem",
        ),
        rx.text(
            "🌱 Empiezas con nivel Semilla. ¡Recicla para subir!",
            font_size="0.73rem",
            color=C_MUTED,
            text_align="center",
        ),
        gap="0.55rem",
        align_items="stretch",
        width="100%",
    )
    footer = rx.center(
        rx.text(
            "¿Ya tienes cuenta? ",
            rx.link("Inicia sesión", href="/login", color=C_ACCENT, font_weight="700"),
            font_size="0.84rem",
            color=C_MUTED,
        )
    )
    return _auth_shell("Únete a EcoLink 🌍", "Crea tu cuenta y empieza a reciclar", body, footer)
