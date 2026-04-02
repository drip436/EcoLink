# 📁 **Estructura Final de EcoLink**

## 🎯 **PUNTO DE ENTRADA PRINCIPAL**

**Archivo:** `/home/adrian/Documentos/EcoLink/frontend/EcoLink/EcoLink.py`

Este archivo es el **núcleo del frontend**. Importa y organiza todos los componentes de la aplicación.

```python
"""
EcoLink Frontend Principal
Aplicación de Gestión Circular de Residuos
"""
from app.state import AppState
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.pages.profile import profile_page

app = rx.App()

@app.add_page
def login_route():
    return login_page()

@app.add_page
def register_route():
    return register_page()

@app.add_page
def dashboard_route():
    return dashboard_page()

@app.add_page
def profile_route():
    return profile_page()
```

---

## 📂 **Estructura Completa del Frontend**

```
/frontend/
│
├── 🎨 EcoLink/                          ⭐ CARPETA PRINCIPAL
│   ├── EcoLink.py                       ⭐ ARCHIVO PRINCIPAL (TODO EL FRONTEND)
│   └── __init__.py
│
├── 📊 app/
│   ├── __init__.py
│   │
│   ├── state.py                         # Estado global (AppState)
│   │   └── Contiene: Variables, métodos de autenticación, gamificación
│   │
│   ├── pages/                           # Todas las páginas de la app
│   │   ├── __init__.py
│   │   ├── login.py                     # Página de Login
│   │   ├── register.py                  # Página de Registro
│   │   ├── dashboard.py                 # Dashboard Principal
│   │   └── profile.py                   # Perfil de Usuario
│   │
│   └── components/                      # Componentes reutilizables
│       ├── __init__.py
│       └── navbar.py                    # Barra de navegación
│
├── 🔧 rxconfig.py                       # Configuración de Reflex
│   └── app_name="EcoLink"               # Apunta a EcoLink/EcoLink.py
│
└── 📦 requirements.txt                  # Dependencias
    ├── reflex>=0.4.0
    ├── httpx>=0.25.0
    ├── pydantic>=2.5.0
    └── requests>=2.31.0
```

---

## 🔄 **Flujo de Importación (Cómo todo se conecta)**

```
rxconfig.py (app_name="EcoLink")
    ↓
    Busca: EcoLink/EcoLink.py
    ↓
EcoLink/EcoLink.py (ARCHIVO PRINCIPAL)
    ├─→ from app.state import AppState
    ├─→ from app.pages.login import login_page
    ├─→ from app.pages.register import register_page
    ├─→ from app.pages.dashboard import dashboard_page
    ├─→ from app.pages.profile import profile_page
    └─→ from app.components.navbar import navbar
    ↓
app/state.py
    └─→ Define toda la lógica de estado (autenticación, datos, etc)
    ↓
app/pages/*.py
    └─→ Cada página importa desde app.state y app.components
    ↓
app/components/*.py
    └─→ Componentes reutilizables para todas las páginas
```

---

## 🎬 **Ciclo de Ejecución**

### 1️⃣ **Inicio de Reflex**
```bash
cd /home/adrian/Documentos/EcoLink/frontend
reflex run
```

### 2️⃣ **Reflex carga rxconfig.py**
```python
config = rx.Config(
    app_name="EcoLink",  # ← Busca esta carpeta
    ...
)
```

### 3️⃣ **Reflex busca EcoLink/EcoLink.py**
```
✅ Encontrado: frontend/EcoLink/EcoLink.py
✅ Importado: app.state, app.pages, app.components
✅ Compilado: React + Router + Frontend
```

### 4️⃣ **App se ejecuta en http://localhost:3000**
```
- Login page en /
- Register page en /register
- Dashboard en /dashboard
- Profile en /profile
```

---

## 📋 **Archivo EcoLink.py Completo**

```python
"""
EcoLink Frontend Principal
Aplicación de Gestión Circular de Residuos
Archivo principal que contiene toda la configuración del frontend
"""
import reflex as rx
import sys
import os

# Agregar ruta correcta para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================================
# IMPORTAR TODOS LOS COMPONENTES DEL FRONTEND
# ============================================================================

# Estado global (todas las variables y lógica)
from app.state import AppState

# Páginas (interfaces de usuario)
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.pages.profile import profile_page

# Componentes reutilizables
from app.components.navbar import navbar


# ============================================================================
# CREAR APLICACIÓN REFLEX
# ============================================================================

app = rx.App()


# ============================================================================
# DEFINIR RUTAS (PÁGINAS)
# ============================================================================

@app.add_page
def login_route() -> rx.Component:
    """
    Página de Login - Ruta principal (/)
    Muestra formulario de login
    """
    return login_page()


@app.add_page
def register_route() -> rx.Component:
    """
    Página de Registro (/register)
    Permite crear nueva cuenta
    """
    return register_page()


@app.add_page
def dashboard_route() -> rx.Component:
    """
    Dashboard Principal (/dashboard)
    Muestra estadísticas y opciones principales
    """
    return dashboard_page()


@app.add_page
def profile_route() -> rx.Component:
    """
    Perfil de Usuario (/profile)
    Información del usuario autenticado
    """
    return profile_page()


# ============================================================================
# INFORMACIÓN DE LA APLICACIÓN
# ============================================================================

"""
🌱 ECOLINK - Plataforma de Gestión Circular de Residuos

DESCRIPCIÓN:
Aplicación web que permite a los ciudadanos:
- Registrar reciclaje
- Ganar puntos y subir niveles
- Ver rutas de recolección
- Localizar puntos de acopio
- Participar en ranking de recicladores

CARACTERÍSTICAS:
✅ Autenticación de usuarios
✅ Dashboard de actividades
✅ Sistema de gamificación
✅ Visualización de rutas de recolección
✅ Mapa de puntos de acopio
✅ Historial de colecciones

USUARIOS DE PRUEBA:
- Admin: admin@ecolink.com / admin123
- Ciudadano: juan@example.com / citizen123
- Reciclador: recycler@ecolink.com / recycler123

ACCESO:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación: http://localhost:8000/docs

TECNOLOGÍAS:
- Frontend: Reflex (Python + React)
- Backend: FastAPI (Python)
- Base Datos: SQLite
- Autenticación: JWT + Argon2
"""
```

---

## 🚀 **Flujo de Usuario**

```
Usuario abre http://localhost:3000
    ↓
    ¿Tiene cuenta?
    ├─→ NO: Hace clic en "Registro"
    │       ↓
    │       Página register.py
    │       ↓
    │       Completa formulario
    │       ↓
    │       AppState.handle_register() POST /auth/register
    │       ↓
    │       Redirige a login
    │
    ├─→ SÍ: Está en página login.py
            ↓
            Ingresa email y contraseña
            ↓
            AppState.handle_login() POST /auth/login
            ↓
            ¿Login exitoso?
            ├─→ NO: Muestra error
            ├─→ SÍ: 
                    ↓
                    Guarda token JWT
                    ↓
                    Redirige a /dashboard
                    ↓
                    Muestra dashboard.py
                    ↓
                    Puede:
                    ├─ Ir a /profile
                    ├─ Ver navbar con opción Logout
                    └─ Interactuar con datos personales
```

---

## ✨ **Resumen Visual**

| Archivo | Propósito | Importancia |
|---------|-----------|-------------|
| `EcoLink.py` | Punto de entrada, define rutas | ⭐⭐⭐ CRÍTICO |
| `state.py` | Estado global y lógica | ⭐⭐⭐ CRÍTICO |
| `pages/login.py` | Interface de login | ⭐⭐⭐ Importante |
| `pages/register.py` | Interface de registro | ⭐⭐ Importante |
| `pages/dashboard.py` | Dashboard principal | ⭐⭐ Importante |
| `pages/profile.py` | Perfil de usuario | ⭐ Complementario |
| `components/navbar.py` | Barra de navegación | ⭐⭐ Importante |

---

## 🔧 **Cómo Editar el Frontend**

### Para agregar una nueva página:

1. **Crear archivo en `app/pages/new_page.py`**
```python
import reflex as rx
from app.state import AppState

def new_page() -> rx.Component:
    return rx.container(
        # Tu contenido aquí
    )
```

2. **Importar en `EcoLink.py`**
```python
from app.pages.new_page import new_page
```

3. **Agregar ruta en `EcoLink.py`**
```python
@app.add_page
def new_page_route() -> rx.Component:
    return new_page()
```

4. **Accede en `http://localhost:3000/new-page-route`**

---

## 📊 **Estructura de Datos (AppState)**

```python
AppState:
├── Autenticación
│   ├── token: str
│   ├── is_authenticated: bool
│   ├── current_user: User
│   ├── login_email: str
│   ├── login_password: str
│   └── auth_error: str
│
├── Gamificación
│   ├── gamification_stats: GamificationStats
│   └── leaderboard: List[dict]
│
├── Datos
│   ├── recycling_points: List[RecyclingPoint]
│   ├── active_routes: List[Route]
│   └── my_collections: List[Collection]
│
└── Estado UI
    ├── loading: bool
    ├── selected_point: RecyclingPoint
    └── waste_type_filter: str
```

---

## ✅ **Checklist de Verificación**

- ✅ `EcoLink.py` importa todas las páginas
- ✅ `state.py` define todo el estado global
- ✅ `pages/` contiene todas las interfaces
- ✅ `components/` tiene componentes reutilizables
- ✅ `rxconfig.py` apunta a `EcoLink`
- ✅ Todas las rutas están definidas en `EcoLink.py`
- ✅ Backend API disponible en puerto 8000
- ✅ Frontend disponible en puerto 3000

---

**¡El frontend está 100% centralizado en EcoLink.py! 🎉**
