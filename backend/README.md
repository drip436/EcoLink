# Backend - EcoLink API

API REST desarrollada con FastAPI para gestión de residuos reciclables.

## 📋 Estructura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Entrada principal
│   ├── config.py                  # Configuración
│   ├── database.py                # Conexión BD
│   ├── models/                    # Modelos ORM
│   │   ├── user.py
│   │   ├── route.py
│   │   ├── recycling_point.py
│   │   ├── collection.py
│   │   └── gamification.py
│   ├── schemas/                   # Validación Pydantic
│   │   ├── user.py
│   │   ├── route.py
│   │   ├── recycling_point.py
│   │   ├── collection.py
│   │   └── gamification.py
│   ├── crud/                      # Operaciones BD
│   │   ├── user.py
│   │   ├── route.py
│   │   ├── recycling_point.py
│   │   ├── collection.py
│   │   └── gamification.py
│   ├── api/                       # Endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── routes.py
│   │   ├── recycling_points.py
│   │   ├── collections.py
│   │   └── gamification.py
│   ├── services/                  # Lógica de negocio
│   │   ├── auth_service.py
│   │   └── gamification_service.py
│   └── utils/                     # Utilidades
│       └── security.py            # JWT, bcrypt
├── init_db.py                     # Inicializar BD
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear .env
cp .env.example .env

# Inicializar BD con datos demo
python init_db.py

# Ejecutar servidor
python -m uvicorn app.main:app --reload --port 8000
```

## 📡 Endpoints Principales

Ver [README.md principal](../README.md) para lista completa de endpoints.

## 🔑 Autenticación

Todos los endpoints protegidos requieren token JWT:

```bash
Authorization: Bearer {token}
```

## 🗄️ Modelos

### User
- Ciudadano, Administrador, Reciclador
- Autenticación con JWT
- Relación con colecciones y gamificación

### Route
- Ruta de recolección con ubicación GPS
- Estados: pending, in_progress, completed, cancelled
- Capacidad y peso actual

### RecyclingPoint
- Punto de acopio con ubicación
- Tipos de residuos que acepta
- Horario de funcionamiento
- Información de contacto

### Collection
- Residuo reportado por ciudadano
- Estados: pending, collected, cancelled
- Vinculación con usuario

### UserGamification
- Puntos, niveles, experiencia
- Estadísticas de reciclaje
- Ranking

## 📝 Ejemplos

### Registro
```python
POST /auth/register
{
  "email": "user@example.com",
  "full_name": "Juan Pérez",
  "password": "securepass123"
}
```

### Login
```python
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

### Crear Colección
```python
POST /collections/
Header: Authorization: Bearer {token}
{
  "waste_type": "plastic",
  "weight_kg": 5,
  "address": "Calle 50"
}
```

## 📚 Documentación Interactiva

Una vez ejecutando el servidor, acceder a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

Desarrollado para Innovatec 🌱
