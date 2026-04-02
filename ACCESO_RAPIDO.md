# 🚀 **GUÍA DE ACCESO RÁPIDO - ECOLINK**

## 📍 **ACCESOS PRINCIPALES**

### 🌐 **Frontend (Interfaz Usuario)**
**URL:** http://localhost:3000

```
Pantalla de Login
  ├─ Email: juan@example.com
  ├─ Password: citizen123
  └─ [Iniciar Sesión]
```

### 🔌 **Backend API (FastAPI)**
**URL:** http://localhost:8000

```
{"message":"Bienvenido a EcoLink API","version":"1.0.0","docs":"/docs"}
```

### 📚 **Documentación API (Swagger UI)**
**URL:** http://localhost:8000/docs

```
Aquí puedes probar todos los endpoints:
- POST /auth/login
- GET /users/me
- GET /recycling-points
- POST /collections
- Y mucho más...
```

### 🔄 **Documentación Alternativa (ReDoc)**
**URL:** http://localhost:8000/redoc

---

## 🎯 **RUTAS DEL FRONTEND**

| Ruta | Página | Acceso |
|------|--------|--------|
| `/` | Login | Público |
| `/register` | Registro | Público |
| `/dashboard` | Dashboard | Autenticado |
| `/profile` | Perfil | Autenticado |

---

## 👤 **USUARIOS DE PRUEBA**

### Admin (Municipio)
```
Email:    admin@ecolink.com
Password: admin123
Rol:      Admin
```

### Ciudadano 1
```
Email:    juan@example.com
Password: citizen123
Rol:      Citizen
```

### Ciudadano 2
```
Email:    maria@example.com
Password: citizen123
Rol:      Citizen
```

### Reciclador
```
Email:    recycler@ecolink.com
Password: recycler123
Rol:      Recycler
```

---

## 🔧 **INICIADOR RÁPIDO (Copy & Paste)**

### Terminal 1 - Backend
```bash
cd /home/adrian/Documentos/EcoLink/backend && source ../.venv/bin/activate && python -m uvicorn app.main:app --reload
```

### Terminal 2 - Frontend
```bash
cd /home/adrian/Documentos/EcoLink/frontend && source ../.venv/bin/activate && reflex run
```

---

## 🎨 **ESTRUCTURA DE ARCHIVOS CLAVE**

```
🌱 ECOLINK (Raíz)
│
├── 🔙 BACKEND
│   └── /backend/
│       ├── app/main.py              ← Servidor FastAPI
│       ├── app/models/              ← BD Models
│       ├── app/api/                 ← Endpoints
│       └── init_db.py               ← BD Init
│
├── 🎨 FRONTEND
│   └── /frontend/
│       ├── EcoLink/EcoLink.py       ⭐ PUNTO DE ENTRADA
│       ├── app/state.py             ← Estado Global
│       ├── app/pages/               ← Páginas
│       ├── app/components/          ← Componentes
│       └── rxconfig.py              ← Config Reflex
│
├── 🔧 CONFIGURACIÓN VS CODE
│   └── /.vscode/
│       ├── settings.json
│       ├── launch.json
│       └── tasks.json
│
└── 📚 DOCUMENTACIÓN
    ├── README.md
    ├── QUICKSTART.md
    ├── PROJECT_SUMMARY.md
    ├── ECOLINK_FINAL_REPORT.md
    ├── ECOLINK_FRONTEND_STRUCTURE.md
    └── ECOLINK_CONFIRMACION_FINAL.md
```

---

## 🧪 **PRUEBAS RÁPIDAS**

### Test 1: Verificar Backend
```bash
curl http://localhost:8000/
```
**Respuesta esperada:**
```json
{
  "message": "Bienvenido a EcoLink API",
  "version": "1.0.0"
}
```

### Test 2: Ver documentación
```bash
Abre en navegador: http://localhost:8000/docs
```

### Test 3: Probar login en API
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"juan@example.com","password":"citizen123"}'
```

### Test 4: Acceder Frontend
```bash
Abre en navegador: http://localhost:3000
```

---

## ⚙️ **TROUBLESHOOTING RÁPIDO**

### "Puerto 8000 en uso"
```bash
lsof -i :8000
kill -9 <PID>
```

### "Reflex no inicia"
```bash
rm -rf frontend/.web
rm -rf frontend/.states
reflex run
```

### "No importa módulos"
```bash
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

---

## 📋 **CHECKLIST DE ARRANQUE**

- [ ] Terminal 1: Backend iniciado (puerto 8000)
- [ ] Terminal 2: Frontend iniciado (puerto 3000)
- [ ] Browser: http://localhost:3000 abierto
- [ ] Login: jwt@example.com / citizen123
- [ ] Dashboard: Cargó correctamente
- [ ] API Docs: http://localhost:8000/docs accesible

---

## 🎬 **VÍDEO MENTAL - FLUJO COMPLETO**

```
1. Usuario abre http://localhost:3000
                ↓
2. Ve página de LOGIN
                ↓
3. Ingresa: juan@example.com / citizen123
                ↓
4. Hace POST a http://localhost:8000/auth/login
                ↓
5. Backend retorna JWT token
                ↓
6. Frontend guarda token y redirige a /dashboard
                ↓
7. Usuario ve su Dashboard con:
   - Puntos: 0
   - Nivel: 1
   - Colecciones: 0
                ↓
8. Frontend puede hacer nuevas requests con JWT:
   - GET /users/me
   - GET /routes
   - POST /collections
   - GET /gamification/stats
```

---

## 🛠️ **COMANDOS ÚTILES**

### Limpiar BD
```bash
rm backend/ecolink.db
```

### Reinicializar BD
```bash
cd backend && python init_db.py
```

### Ver logs en tiempo real
```bash
tail -f reflex.log
```

### Ver procesos de Python
```bash
ps aux | grep -E "reflex|uvicorn|python" | grep -v grep
```

### Matar todos los procesos
```bash
pkill -9 -f reflex
pkill -9 -f uvicorn
```

---

## 📱 **PUNTOS DE ACCESO FINALES**

### Para Desarrollo
| Aspecto | URL | Puerto |
|--------|-----|--------|
| Frontend | http://localhost:3000 | 3000 |
| Backend | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |
| Hot Reload | ✅ Habilitado | - |

### Base de Datos
| Tipo | Ubicación |
|------|-----------|
| sqlite | `/backend/ecolink.db` |

### Entorno Virtual
| Path |
|------|
| `/home/adrian/Documentos/EcoLink/.venv/` |

---

## 🎓 **CÓMO FUNCIONA INTERNAMENTE**

### 1. Reflex detecta app_name
```python
# rxconfig.py
app_name="EcoLink"  # Busca EcoLink/EcoLink.py
```

### 2. Carga EcoLink.py
```python
# frontend/EcoLink/EcoLink.py
from app.state import AppState
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.pages.profile import profile_page

app = rx.App()

@app.add_page
def login_route():
    return login_page()
```

### 3. Compila con React
```
EcoLink.py → React Components → HTML/CSS/JS
```

### 4. Ejecuta en puerto 3000
```
http://localhost:3000/ → Login Page
```

---

## ✅ **ESTADO FINAL**

```
🌱 ECOLINK v1.0.0

✅ Backend: FastAPI en puerto 8000
✅ Frontend: Reflex en puerto 3000
✅ Database: SQLite inicializada
✅ Auth: JWT + Argon2 implementado
✅ API: 30+ endpoints documentados
✅ Componentes: 4 páginas principales
✅ Estado: AppState global funcionando
✅ Documentación: Completa

STATUS: 🚀 LISTO PARA USAR
```

---

## 🎉 **¡LISTO PARA COMENZAR!**

**Próximo paso:**
1. Abre dos terminales
2. Ejecuta backend y frontend
3. Abre http://localhost:3000
4. ¡Disfruta EcoLink! 🌱

---

*Última actualización: 01/04/2026*  
*Todas las funciones testeadas y operacionales.*
