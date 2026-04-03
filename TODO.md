# ✅ CHECKLIST: Qué tienes que hacer ahora

## 🎯 PASO 1: Instalar PostgreSQL (5 minutos)

- [ ] Opción A: Descargar Windows installer
  - Link: https://www.postgresql.org/download/windows/
  - O Opción B: Usar Docker (si lo tienes instalado)
  
**Prueba que funciona:**
```bash
psql --version
# Debería mostrar la versión de PostgreSQL
```

---

## 🎯 PASO 2: Crear base de datos EcoLink (2 minutos)

```bash
# Conectarse como admin (te pedirá contraseña)
psql -U postgres

# Copiar y pegar esto en la consola psql:
CREATE DATABASE ecolink;
\quit
```

---

## 🎯 PASO 3: Inicializar EcoLink en PostgreSQL (1 minuto)

```bash
# Desde la raíz de la carpeta del proyecto
.venv\Scripts\activate.bat
cd backend
python init_db.py
```

**Resultado esperado:**
```
✅ Tablas creadas exitosamente
✨ Base de datos inicializada exitosamente!

📝 Usuarios de prueba:
   Admin:    admin@ecolink.com / admin123
   Ciudadano 1: juan@example.com / citizen123
   Ciudadano 2: maria@example.com / citizen123
   Reciclador: recycler@ecolink.com / recycler123
```

---

## 🎯 PASO 4: Iniciar Backend (Terminal 1)

```bash
.venv\Scripts\activate.bat
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Resultado esperado:**
```
Uvicorn running on http://0.0.0.0:8000
```

---

## 🎯 PASO 5: Iniciar Frontend (Terminal 2)

```bash
.venv\Scripts\activate.bat
cd frontend
reflex run
```

**Resultado esperado:**
```
App running at: http://localhost:3000
```

---

## 🎯 PASO 6: Probar la aplicación

1. **Abrir navegador**: http://localhost:3000
2. **Click en "Regístrate aquí"** → Ir a página de registro
3. **Llenar formulario:**
   - Nombre: Tu nombre
   - Email: tunombre@example.com
   - Contraseña: 123456
   - Confirmar: 123456
4. **Click "Registrarse"**
   - ✅ Debe aparecer: "¡Registro exitoso! Bienvenido [Tu nombre]"
   - Espera 1.5 segundos
   - Auto-redirige a Login
5. **Login con credenciales:**
   - Email: tunombre@example.com
   - Contraseña: 123456
   - **Éxito si**: accedes al dashboard
6. **Verificar en base de datos:**
   ```bash
   psql -U postgres -d ecolink
   SELECT email, full_name FROM users;
   # Deberías ver tu usuario nuevo
   ```

---

## 🐛 Si hay error en PASO 3 (init_db.py):

**Error: "could not connect to server"**
- PostgreSQL no está corriendo
- Solución: Instalar PostgreSQL e iniciarlo

**Error: "database does not exist"**
- No creaste la BD en PASO 2
- Solución: Ejecutar `CREATE DATABASE ecolink;` en psql

**Error: "psycopg2 not found"**
- Falta driver PostgreSQL
- Solución: `pip install psycopg2-binary`

---

## 🐛 Si hay error en PASO 4 (Backend):

**Error: "Address already in use"**
- Otro proceso usa puerto 8000
- Solución: `lsof -i :8000` y matar el proceso, o cambiar puerto

**Error: "ModuleNotFoundError"**
- Faltan dependencias
- Solución: `pip install -r backend/requirements.txt`

---

## 🐛 Si hay error en PASO 5 (Frontend):

**Error: "Cannot connect to server"**
- Backend no está corriendo en PASO 4
- Solución: Verificar que PASO 4 esté completado

**Error: "reflex command not found"**
- Reflex no está instalado
- Solución: `pip install -r frontend/requirements.txt`

---

## 🎉 ¡Listo!

Cuando todo funcione:
- ✅ Frontend: http://localhost:3000
- ✅ Backend API: http://localhost:8000
- ✅ API Docs: http://localhost:8000/docs (prueba los endpoints)
- ✅ PostgreSQL: Datos persistosos en la BD

---

## 📚 Documentación completa

Si necesitas entender más:
- [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md) - Guía de instalación
- [CAMBIOS_REALIZADOS.md](./CAMBIOS_REALIZADOS.md) - Detalle técnico de todos los cambios
- [MIGRACION_POSTGRESQL.md](./MIGRACION_POSTGRESQL.md) - Proceso de migración completo

---

## 🆘 ¿Problema?

Revisa:
1. ¿PostgreSQL está corriendo? → `pg_isready`
2. ¿.env tiene DATABASE_URL? → `cat .env | grep DATABASE`
3. ¿Tablas existen? → `psql -U postgres -d ecolink -c "\dt"`
4. ¿Backend inició? → http://localhost:8000/docs
5. ¿Frontend inició? → http://localhost:3000

**Si nada de esto soluciona, verifica los logs en las terminales del backend/frontend.**

---

¡Adelante! 🚀 Cuando termines, confirma que todo funciona y podemos continuar con más features.
