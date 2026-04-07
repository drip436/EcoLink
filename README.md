# 🌿 EcoLink — Gestión Circular de Residuos
**Proyecto Innovatec · Universidad · Mérida, Yucatán**

---

## ⚠️ Por qué desapareció el error WebSocket

El error anterior:
```
Cannot connect to server: websocket error
Check if server is reachable at ws://localhost:8000/_event
```
ocurría porque había **dos servidores separados** (FastAPI en :8000 + Reflex en :3000).
Reflex necesita conectarse a su **propio** backend via WebSocket, no a FastAPI.

**En esta versión**: todo vive en un solo proceso Reflex.
- No hay `uvicorn main:app` separado.
- La base de datos se accede con `rx.session()` dentro de los EventHandlers.
- Reflex gestiona su WebSocket internamente.

---

## 📁 Estructura del proyecto

```
ecolink_v2/
├── rxconfig.py                  ← Config Reflex + URL Supabase
├── requirements.txt
├── create_admin.py              ← Script setup inicial (ejecutar 1 vez)
└── ecolink/
    ├── ecolink.py               ← App Reflex + landing page /
    ├── state.py                 ← Estado global + toda la lógica de BD
    ├── models/
    │   └── db.py               ← Modelos SQLModel (User, routes, points…)
    ├── utils/
    │   └── auth.py             ← Hash bcrypt + tokens de sesión
    ├── components/
    │   └── ui.py               ← Navbar, cards, badges, notificaciones
    └── pages/
        ├── auth.py             ← /login y /register
        ├── dashboard.py        ← /dashboard (ciudadano)
        └── admin.py            ← /admin (administrador)
```

---

## 🚀 Instrucciones de ejecución

### Requisitos
- Python 3.11+
- Node.js 18+ (Reflex lo necesita para compilar el frontend)

### Paso 1 — Instalar dependencias

```bash
cd ecolink_v2
pip install -r requirements.txt
```

### Paso 2 — Crear tablas y usuario admin en Supabase

```bash
python create_admin.py
```

Esto:
1. Crea todas las tablas en tu BD de Supabase
2. Crea el usuario `admin@ecolink.mx` con contraseña `admin123`
3. Inserta datos de demo (rutas, puntos, recompensas)

### Paso 3 — Ejecutar la aplicación

```bash
reflex run
```

La primera vez tarda ~2 minutos mientras descarga Node.js y los paquetes npm.

**URLs:**
| URL | Descripción |
|---|---|
| http://localhost:3000 | Landing page |
| http://localhost:3000/register | Crear cuenta |
| http://localhost:3000/login | Iniciar sesión |
| http://localhost:3000/dashboard | Panel ciudadano |
| http://localhost:3000/admin | Panel administrador |

---

## 👤 Credenciales de prueba

| Rol | Email | Contraseña |
|---|---|---|
| Administrador | admin@ecolink.mx | admin123 |
| Ciudadano | (crear en /register) | (la que elijas) |

---

## 🗄️ Base de datos (Supabase)

Tablas creadas automáticamente:
- `users` — Usuarios con gamificación integrada
- `collection_routes` — Rutas de recolección
- `pickup_requests` — Solicitudes de recogida por ciudadanos
- `collection_points` — Puntos de acopio en el mapa
- `recycling_history` — Log de acciones de reciclaje
- `rewards` — Recompensas canjeables
- `reward_claims` — Historial de canjes

---

## 🎮 Gamificación

| Acción | Puntos |
|---|---|
| Solicitar recogida pendiente | +30 |
| Visitar punto de acopio | +40 a +70 (según el punto) |
| Canjear recompensa | −N puntos |

| Nivel | Mínimo |
|---|---|
| 🌱 Semilla | 0 pts |
| 🌿 Brote | 100 pts |
| 🍃 Hoja | 300 pts |
| 🌳 Árbol | 700 pts |
| 🌲 Bosque | 1500 pts |

---

## 🔧 Cambiar la base de datos

En `rxconfig.py` cambia `SUPABASE_URL`:
```python
# Para SQLite local (sin configuración):
SUPABASE_URL = "sqlite:///ecolink.db"

# Para otro PostgreSQL:
SUPABASE_URL = "postgresql://user:pass@host:5432/db"
```

---

## 📐 Cómo funciona Reflex "todo en uno"

```
Browser (React compilado por Reflex)
    ↕  WebSocket (ws://localhost:3000/_event)
Reflex Server
    ├── EventHandlers (Python puro en state.py)
    │     └── rx.session() → SQLModel → Supabase
    └── Estado → serializado → enviado al browser
```

No hay REST API, no hay FastAPI, no hay fetch().
Cada acción del usuario dispara un EventHandler Python en el servidor,
que actualiza el estado y Reflex refresca la UI automáticamente.
