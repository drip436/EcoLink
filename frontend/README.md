# Frontend - EcoLink

Interfaz de usuario desarrollada con Reflex (Python + React) para EcoLink.

## 📋 Estructura

```
frontend/
├── app/
│   ├── __init__.py                # App principal
│   ├── state.py                   # Estado global (Reflex State)
│   ├── pages/                     # Páginas
│   │   ├── login.py
│   │   ├── register.py
│   │   ├── dashboard.py
│   │   └── profile.py
│   └── components/                # Componentes reutilizables
│       └── navbar.py
├── __init__.py                    # Entrada principal
├── reflex.config.py               # Configuración
├── requirements.txt
└── README.md
```

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dev server
reflex run
```

Acceder a `http://localhost:3000`

## 🏗️ Componentes Principales

### State Management (`app/state.py`)

Gestiona todo el estado de la aplicación:
- Autenticación (token, usuario)
- Datos (puntos, rutas, colecciones)
- Interacciones (loading, errores)

```python
class AppState(rx.State):
    token: Optional[str]
    is_authenticated: bool
    current_user: Optional[User]
    gamification_stats: Optional[GamificationStats]
    # ... etc
```

### Páginas

1. **Login** (`pages/login.py`)
   - Formulario de autenticación
   - Manejo de errores

2. **Registro** (`pages/register.py`)
   - Crear nueva cuenta
   - Validaciones

3. **Dashboard** (`pages/dashboard.py`)
   - Vista principal del ciudadano
   - Estadísticas personales
   - Opciones para reportar residuos
   - Leaderboard

4. **Perfil** (`pages/profile.py`)
   - Información del usuario
   - Logros desbloqueados

### Componentes (`components/navbar.py`)

Componentes reutilizables:
- `navbar()` - Navegación principal
- `stats_card()` - Tarjeta de estadísticas
- `point_card()` - Tarjeta de punto de acopio
- `route_card()` - Tarjeta de ruta
- `achievement_badge()` - Badge de logro

## 🎨 Estilo y Tema

Utiliza tema personalizado:
- **Color primario**: Verde (#10b981) - Eco
- **Color secundario**: Azul (#3b82f6)
- **Color acentó**: Ámbar (#f59e0b)
- **Fuente**: Poppins

## 📡 Integración con Backend

La aplicación se conecta a `http://localhost:8000` (API):

```python
API_URL = "http://localhost:8000"
```

Ejemplos de llamadas en `state.py`:
- `handle_login()` - POST /auth/login
- `handle_register()` - POST /auth/register
- `load_recycling_points()` - GET /recycling-points/
- `load_gamification_stats()` - GET /gamification/my-stats

## 🔄 Flujo de Autenticación

1. Usuario ingresa email/contraseña en `/login`
2. `handle_login()` hace POST a `/auth/login`
3. Backend retorna token JWT
4. Token se almacena en `AppState.token`
5. Redireccionar a `/dashboard`
6. Cargar datos del usuario

## 🎮 Sistema de Gamificación en Frontend

- Mostrar puntos actuales, nivel y ranking
- Botones para reportar residuos
- Ganar puntos automáticamente
- Visualizar progress hacia siguiente nivel

## 🚀 Mejoras Futuras

- [ ] Mapa interactivo (Google Maps / Leaflet)
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)
- [ ] Progressive Web App (PWA)
- [ ] Filtros avanzados de puntos

---

Desarrollado para Innovatec 🌱
