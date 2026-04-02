# 🌱 EcoLink - Plataforma de Gestión Circular de Residuos

**EcoLink** es una plataforma web integral para gestionar la recolección circular de residuos en ciudades. Permite a ciudadanos, administradores y recicladores colaborar en tiempo real para reducir residuos y promover la sostenibilidad.

---

## 🎯 Características Principales

### 👤 Para Ciudadanos
- ✅ Registro e inicio de sesión seguro
- ✅ Ver rutas de recolección en tiempo real
- ✅ Localizar puntos de acopio de reciclaje (mapa interactivo)
- ✅ Reportar residuos para recolección
- ✅ Historial personal de reciclaje
- ✅ **Sistema de Gamificación**:
  - Ganar puntos por cada colección
  - Subir de nivel
  - Ver ranking global de recicladores
  - Desbloquear logros

### 🏢 Para Administradores
- ✅ Panel de administración
- ✅ Crear y gestionar rutas de recolección
- ✅ Actualizar estado de rutas en tiempo real
- ✅ Agregar/editar puntos de acopio
- ✅ Ver estadísticas de reciclaje

### ♻️ Sistema de Gamificación
- **Puntos**: 10 puntos base por colección + bonificación por peso
- **Niveles**: Avanza de nivel cada 100 puntos de experiencia
- **Ranking**: Competición semanal y mensual entre usuarios
- **Logros**: Desbloquea badges por hitos alcanzados

---

## 🏗️ Arquitectura Técnica

```
EcoLink/
├── backend/                 # FastAPI REST API
│   ├── app/
│   │   ├── models/         # SQLAlchemy ORM
│   │   ├── schemas/        # Pydantic validación
│   │   ├── crud/           # Operaciones BD
│   │   ├── api/            # Endpoints FastAPI
│   │   ├── services/       # Lógica de negocio
│   │   └── utils/          # JWT, seguridad
│   ├── init_db.py          # Script inicialización
│   └── requirements.txt
│
├── frontend/               # Reflex (Python React-like)
│   ├── app/
│   │   ├── state.py        # Estado global
│   │   ├── pages/          # Páginas de la app
│   │   └── components/     # Componentes reutilizables
│   ├── __init__.py         # Entrada principal Reflex
│   └── requirements.txt
│
├── docker-compose.yml      # BD PostgreSQL
└── README.md
```

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.10+
- pip (gestor de paquetes)
- Git

### Paso 1: Clonar el repositorio

```bash
cd EcoLink
```

### Paso 2: Configurar Backend

```bash
# Entrar en directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (copiar de .env.example y ajustar)
cp .env.example .env

# Inicializar bases de datos con datos de demostración
python init_db.py

# Ejecutar servidor FastAPI
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en `http://localhost:8000`
- **Documentación interactiva**: http://localhost:8000/docs (Swagger UI)
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Paso 3: Configurar Frontend

En otra terminal:

```bash
# Entrar en directorio frontend
cd frontend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\\Scripts\\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar Reflex dev server
reflex run
```

El frontend estará disponible en `http://localhost:3000`

---

## 📝 Credenciales de Prueba

Después de ejecutar `python init_db.py`, puedes usar:

| Rol | Email | Password |
|-----|-------|----------|
| **Admin** | admin@ecolink.com | admin123 |
| **Ciudadano 1** | juan@example.com | citizen123 |
| **Ciudadano 2** | maria@example.com | citizen123 |
| **Reciclador** | recycler@ecolink.com | recycler123 |

---

## 📡 API REST Endpoints

### Autenticación
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión
- `POST /auth/verify` - Verificar token

### Usuarios
- `GET /users/me` - Obtener perfil actual
- `GET /users/{user_id}` - Obtener usuario por ID
- `GET /users/` - Listar usuarios

### Rutas de Recolección
- `POST /routes/` - Crear ruta (admin)
- `GET /routes/` - Listar rutas activas
- `GET /routes/{route_id}` - Obtener detalles de ruta
- `PUT /routes/{route_id}` - Actualizar ruta (admin)

### Puntos de Acopio
- `POST /recycling-points/` - Crear punto (admin)
- `GET /recycling-points/` - Listar puntos
- `GET /recycling-points/{point_id}` - Obtener punto
- `PUT /recycling-points/{point_id}` - Actualizar punto (admin)

### Colecciones
- `POST /collections/` - Crear colección
- `GET /collections/my-collections` - Mis colecciones
- `GET /collections/` - Todas las colecciones
- `PUT /collections/{collection_id}/status/{status}` - Actualizar estado

### Gamificación
- `GET /gamification/my-stats` - Mis estadísticas
- `GET /gamification/stats/{user_id}` - Stats de usuario
- `GET /gamification/leaderboard` - Top 10 usuarios
- `GET /gamification/level/{user_id}` - Nivel del usuario

---

## 🗄️ Base de Datos

### Modelos Principales

**User**
- ID, email, contraseña hasheada, rol, datos personales

**Route**
- ID, nombre, ubicación, horario, estado, capacidad

**RecyclingPoint**
- ID, ubicación (lat/lng), tipos de residuos, capacidad

**Collection**
- ID, usuario, tipo residuo, peso, estado, timestamp

**UserGamification**
- ID usuario, puntos, nivel, estadísticas

**Achievement**
- ID, nombre, descripción, criterios, puntos recompensa

### Base de datos por defecto
- **SQLite** (desarrollo) - archivo `test.db`
- **PostgreSQL** (producción recomendada)

Para cambiar aPostgreSQL, editar `DATABASE_URL` en `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/ecolink
```

---

## 🔐 Seguridad

- **Contraseñas**: Hashadas con bcrypt
- **Autenticación**: JWT (JSON Web Tokens)
- **CORS**: Configurado para desarrollo (ajustar en producción)
- **Validación**: Pydantic schemas en todos los endpoints

---

## 🎮 Sistema de Gamificación - Detalles

### Cálculo de Puntos
```python
puntos = 10 * (peso_kg // 5 + 1)
# Ejemplo: 5kg = 20 puntos, 10kg = 30 puntos
```

### Niveles
```python
nivel = (experiencia // 100) + 1
# Nivel 1: 0-99 exp
# Nivel 2: 100-199 exp
# Nivel 3: 200-299 exp
```

### Logros Predefinidos
- 🌱 **Primer Reciclaje**: Realiza tu primera colección (50pts)
- 💪 **Eco Warrior**: 10 colecciones (500pts)
- ♻️ **Sustentable**: 100kg reciclados (1000pts)

---

## 📊 Ejemplos de Uso

### Registrarse y Loguear
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "full_name": "Juan Pérez",
    "password": "securepass123"
  }'
```

### Reportar Residuo para Recolección
```bash
curl -X POST http://localhost:8000/collections/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "waste_type": "plastic",
    "weight_kg": 5,
    "address": "Calle 50 #100"
  }'
```

### Ver Ranking
```bash
curl http://localhost:8000/gamification/leaderboard
```

---

## 🛠️ Desarrollo y Extensiones

### Agregar nuevo endpoint
1. Crear modelo en `models/`
2. Crear schema en `schemas/`
3. Crear CRUD en `crud/`
4. Crear rotas en `api/`
5. Incluir router en `main.py`

### Agregar página en frontend
1. Crear página en `app/pages/`
2. Registrar ruta en `app/__init__.py`
3. Agregar navegación si es necesario

---

## 📚 Dependencias Principales

### Backend
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **Pydantic** - Validación
- **python-jose** - JWT
- **passlib** - Hashing de contraseñas
- **Uvicorn** - Servidor ASGI

### Frontend
- **Reflex** - Framework Python para UI reactivo
- **httpx** - Cliente HTTP

---

## 🤝 Contribuir

Para reportar bugs o sugerir mejoras, crear un issue en el repositorio.

---

## 📄 Licencia

EcoLink © 2024 - Proyecto Innovatec

---

## 👨‍💼 Autor

Desarrollado por: **[Tu Nombre]**
Para: Proyecto Innovatec - Gestión Circular de Residuos

---

## 🎓 Recursos Educativos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Reflex Docs](https://reflex.dev/)
- [JWT en Python](https://python-jose.readthedocs.io/)

---

**¡Únete a EcoLink y ayuda a construir un futuro sostenible!** 🌍♻️
