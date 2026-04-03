# 🗄️ Configuración de PostgreSQL para EcoLink

## Opción 1: Instalar PostgreSQL en Windows (Recomendado)

### Paso 1: Descargar PostgreSQL
1. Ir a https://www.postgresql.org/download/windows/
2. Descargar PostgreSQL 15 o 16 (recomendado)
3. Ejecutar el instalador (.exe)

### Paso 2: Instalación
- Elegir la ruta de instalación (ej: C:\Program Files\PostgreSQL)
- Crear contraseña para usuario `postgres` (ej: `postgres`)
- Puerto por defecto: `5432`
- Locale: Spanish o English (tu preferencia)
- **Importante**: Marcar "Stack Builder" al final para instalar herramientas adicionales (opcional pero útil)

### Paso 3: Verificar instalación
```bash
# Abrir Command Prompt como Administrador
psql --version
# Debería mostrar: psql (PostgreSQL) XX.X

# Conectarse a PostgreSQL
psql -U postgres
# Pedir la contraseña que creaste
```

### Paso 4: Crear base de datos para EcoLink
```sql
-- En la consola psql:
CREATE DATABASE ecolink;
CREATE USER ecolink WITH PASSWORD 'ecolink_password';
ALTER ROLE ecolink SET client_encoding TO 'utf8';
ALTER ROLE ecolink SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecolink SET default_transaction_deferrable TO on;
ALTER ROLE ecolink SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE ecolink TO ecolink;
\c ecolink
GRANT ALL PRIVILEGES ON SCHEMA public TO ecolink;
\quit

# Verificar conexión:
psql -U ecolink -d ecolink -W
# Pedir contraseña: ecolink_password
```

---

## Opción 2: Usar PostgreSQL con Docker (Alternativa)

```bash
# Instalar Docker desde https://www.docker.com/products/docker-desktop

# Crear contenedor PostgreSQL
docker run --name ecolink-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=ecolink \
  -p 5432:5432 \
  -d postgres:15

# Verificar que está corriendo
docker ps | grep ecolink-postgres

# Para detener:
docker stop ecolink-postgres

# Para reiniciar:
docker start ecolink-postgres
```

---

## Paso 5: Configurar EcoLink para PostgreSQL

### Actualizar archivo `.env`
```env
# Base de datos PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecolink

# Resto de configuración...
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Inicializar la base de datos
```bash
# En la raíz del proyecto
source .venv/Scripts/activate  # Windows CMD
cd backend
python init_db.py
```

Debería ver:
```
🗄️ Inicializando base de datos PostgreSQL...
📍 Base de datos: postgresql://postgres:postgres@localhost:5432/ecolink
✅ Tablas creadas exitosamente
📝 Creando usuarios de demostración...
✨ Base de datos inicializada exitosamente!
```

---

## Paso 6: Iniciar el Backend

```bash
# Desde la raíz del proyecto
source .venv/Scripts/activate  # Windows CMD
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Herramientas útiles para administrar PostgreSQL

### pgAdmin (GUI Web)
La mayoría de instalaciones de PostgreSQL incluyen pgAdmin. Acceder a:
- URL: `http://localhost:5050`
- Email: `postgres@example.com` (o lo que configuraste)
- Password: que configuraste durante la instalación

### DBeaver (IDE SQL Gratuito)
Descargar desde: https://dbeaver.io/download/
- Mejor para queries complejas y análisis de datos
- Interfaz más intuitiva que pgAdmin

### Comandos útiles en psql
```sql
-- Listar todos los usuarios
\du

-- Listar todas las bases de datos
\l

-- Conectarse a una BD
\c ecolink

-- Listar tablas
\dt

-- Ver estructura de una tabla
\d users

-- Salir
\quit
```

---

## Troubleshooting

### Error: "FATAL: Ident authentication failed"
```bash
# En PostgreSQL, cambiar a autenticación por contraseña
# Editar: C:\Program Files\PostgreSQL\XX\data\pg_hba.conf
# Cambiar "ident" por "md5" o "password" para conexiones locales

# Luego reiniciar el servicio PostgreSQL
```

### Error: "SSL error: certificate verify failed"
```env
# Agregar a .env:
DATABASE_URL=postgresql://user:password@localhost:5432/ecolink?sslmode=disable
```

### Base de datos no se inicia
```bash
# Reiniciar el servicio PostgreSQL (Windows)
# Panel de Control > Servicios > PostgreSQL

# O desde Command Prompt como Admin:
net stop postgresql-x64-15
net start postgresql-x64-15
```

---

## Migración desde SQLite a PostgreSQL

Si ya tenías SQLite, no hay problema:
1. El nuevo `init_db.py` detectará si la BD ya tiene datos
2. Las migraciones de SQLAlchemy se manejan automáticamente
3. Todos los modelos son compatibles con ambas bases de datos

---

¡Listo! Ahora puedes usar EcoLink con PostgreSQL. 🚀
