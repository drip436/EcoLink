# rxconfig.py
# ─────────────────────────────────────────────────────────────────────────────
# Configuración principal de Reflex para EcoLink.
# El DB_URL apunta a Supabase (PostgreSQL).
# En Reflex "todo en uno", el backend (lógica, BD) y el frontend
# corren en el MISMO proceso: no hay servidor separado, y Reflex
# usa su propio WebSocket interno (no el puerto 8000 de FastAPI).
# ─────────────────────────────────────────────────────────────────────────────
import reflex as rx

# Conexión a Supabase — sustituye la contraseña si la cambias
SUPABASE_URL = (
    "postgresql://postgres:ecolinkinnovatec"
    "@db.djhiyafzjfwpaqccqdcy.supabase.co:5432/postgres"
)

config = rx.Config(
    app_name="ecolink",
    db_url=SUPABASE_URL,   # Reflex usa SQLModel; este URL alimenta el motor
    # Puerto del servidor Reflex (frontend + backend WebSocket)
    port=3000,
    # Para producción cambia a False
    # frontend_packages=[]  # agrega npm si necesitas librerías extra
)
