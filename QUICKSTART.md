# 🚀 GUÍA DE INICIO RÁPIDO - EcoLink

Sigue estos pasos para instalar y ejecutar **EcoLink** completamente.

---

## 📋 Requisitos Previos

- **Python 3.10 o superior**
- **pip** (gestor de paquetes - viene con Python)
- **Git** (opcional, para clonar)
- **Terminal/CMD** con acceso a comandos

Verifica que tengas Python instalado:
```bash
python --version
pip --version
```

---

## 🔧 Paso 1: Estructura Inicial

El proyecto ya tiene esta estructura:

```
EcoLink/
├── backend/          # API con FastAPI
├── frontend/         # UI con Reflex
├── docker-compose.yml
├── setup.sh
└── README.md
```

---

## 💻 Paso 2: Configurar Backend

### En una **NUEVA TERMINAL**, haz lo siguiente:

```bash
# Ir a carpeta del backend
cd EcoLink/backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias Python
pip install -r requirements.txt
```

✅ Si ves `(venv)` al inicio del prompt, está activado correctamente.

### Inicializar Base de Datos

```bash
# Crear archivo de configuración
cp .env.example .env

# Crear BD con datos de prueba
python init_db.py
```

Deberías ver:
```
✅ Base de datos inicializada exitosamente!

📝 Usuarios de prueba:
   Admin:    admin@ecolink.com / admin123
   Ciudadano 1: juan@example.com / citizen123
   Ciudadano 2: maria@example.com / citizen123
```

### Ejecutar FastAPI

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verás:
```
Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend ejecutándose en**: `http://localhost:8000`

**Prueba el API**:
- Ir a: http://localhost:8000/docs (Swagger UI)
- Ver documentación interactiva

---

## 🎨 Paso 3: Configurar Frontend

### En una **SEGUNDA TERMINAL (distinta a la del backend)**:

```bash
# Ir a carpeta del frontend
cd EcoLink/frontend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar aplicación Reflex

```bash
reflex run
```

Verás:
```
Reflex app running on http://127.0.0.1:3000
```

✅ **Frontend ejecutándose en**: `http://localhost:3000`

---

## 🌐 Paso 4: Acceder a la Aplicación

Abre tu navegador y ve a: **http://localhost:3000**

Deberías ver la página de **Login de EcoLink**.

### Pruebas de Login

Usa una de estas cuentas:

| Email | Contraseña | Rol |
|-------|-----------|-----|
| admin@ecolink.com | admin123 | Administrador |
| juan@example.com | citizen123 | Ciudadano |
| maria@example.com | citizen123 | Ciudadano |

**Haz clic en "Iniciar Sesión"** y accede al Dashboard.

---

## ✨ Prueba las Funcionalidades

### En el Dashboard (una vez logueado):

1. **Ver mis estadísticas**: Puntos, nivel, colecciones
2. **Crear colección**: Haz clic en botones de residuos (Plástico, Cartón, etc.)
3. **Ver leaderboard**: Top recicladores del sistema
4. **Ir a Perfil**: Botón en la navbar superior derecha

### En el Backend API (http://localhost:8000/docs):

Experimenta con los endpoints:
- `GET /recycling-points/` - Ver puntos de acopio
- `GET /routes/` - Ver rutas activas
- `GET /gamification/leaderboard` - Ver ranking

---

## 🆘 Solución de Problemas

### Error: "Port 8000 already in use"
```bash
# Cambiar puerto
python -m uvicorn app.main:app --reload --port 8001
```

### Error: "Port 3000 already in use"
Reflex usará automáticamente otro puerto.

### Error: "ModuleNotFoundError"
Asegúrate de:
1. Estar en el entorno virtual activado (`(venv)` visible)
2. Haber instalado dependencias: `pip install -r requirements.txt`

### Error: "Database locked" (SQLite)
```bash
# Eliminar base de datos anterior
rm backend/test.db
# Reiniciar
python init_db.py
```

### Backend corre pero frontend no conecta
Verifica que `API_URL` en `frontend/app/state.py` sea:
```python
API_URL = "http://localhost:8000"
```

---

## 📊 Estructura del Proyecto en Detalle

### Backend (`app/` en `backend/` directory)

```
models/       → Clases de BD (User, Route, Point, etc)
schemas/      → Validación de datos (Pydantic)
crud/         → Funciones para leer/escribir BD
api/          → Endpoints HTTP (GET, POST, etc)
services/     → Lógica de negocio
utils/        → Seguridad (JWT, bcrypt)
```

**Archivos clave**:
- `main.py` - Punto de entrada FastAPI
- `database.py` - Conexión a BD
- `config.py` - Configuración

### Frontend (`app/` en `frontend/` directory)

```
state.py      → Estado global (variables, funciones)
pages/        → Páginas (login, dashboard, etc)
components/   → Componentes reutilizables (navbar, cards)
```

**Archivos clave**:
- `__init__.py` - Punto de entrada, define rutas
- `state.py` - Conexión con API

---

## 🎯 Próximos Pasos (Extensiones Futuras)

Puedes agregar:

1. **Mapa interactivo** - Google Maps / Leaflet
2. **WebSockets** - Actualización en tiempo real de rutas
3. **Notificaciones** - Alertas cuando una ruta está cerca
4. **Base de datos PostgreSQL** - Para producción
5. **Autenticación con OAuth** - Google, GitHub login
6. **Modo oscuro** - Interfaz de noche
7. **Mobile app** - React Native / Flutter

---

## 📚 Recursos Útiles

- **FastAPI**: https://fastapi.tiangolo.com/
- **Reflex**: https://reflex.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/

---

## 🎓 Decisiones Técnicas Explicadas

### ¿Por qué FastAPI?
- Rápido (basado en Starlette)
- Documentación automática (Swagger, ReDoc)
- Validación integrada (Pydantic)
- Soporte para async/await
- Perfecto para APIs REST

### ¿Por qué Reflex?
- Todo en Python (sin JavaScript)
- Componentes reactivos (similar a React)
- Full-stack con un solo lenguaje
- Ideal para prototipos rápidos

### ¿Por qué SQLAlchemy?
- ORM flexible y poderoso
- Compatible con cualquier BD (SQLite, PostgreSQL, MySQL)
- Queries seguras contra SQL injection
- Relaciones entre modelos

### ¿Por qué JWT?
- Sin estado (stateless)
- Escalable
- Seguro (hay validación en servidor)
- Estándar de la industria

---

## 🔐 Notas de Seguridad

**Para desarrollo** (lo que estamos haciendo):
- OK usar contraseñas simples
- OK usar `SECRET_KEY` conocido
- OK CORS abierto

**Para producción**: 
- Cambiar `SECRET_KEY` en `.env`
- Usar HTTPS
- Base de datos PostgreSQL
- Validar CORS orígenes
- Variables de entorno secretas

---

## ✅ Checklist Final

- [ ] Backend ejecutándose en http://localhost:8000
- [ ] Frontend ejecutándose en http://localhost:3000
- [ ] Puedo loguearme con juan@example.com / citizen123
- [ ] Puedo ver dashboard con mis puntos
- [ ] Puedo crear colecciones (residuos)
- [ ] Puedo ver ranking de usuarios

---

## 🎉 ¡Felicidades!

Has instalado **EcoLink** correctamente. 

Ahora:
- **Explora el código**
- **Modifica los componentes**
- **Agrega nuevas características**
- **Aprende cómo funcionan FastAPI y Reflex**

---

## 📞 Soporte

Si tienes problemas:
1. Lee el README.md principal
2. Revisa los logs en terminal
3. Verifica puertos no estén ocupados
4. Asegúrate de usar Python 3.10+

---

**¡Disfruta construyendo EcoLink!** 🌱♻️

Hecho para Innovatec 2024
