# 🔧 Configuración de VS Code para EcoLink

##📝 ¿Qué se ha configurado?

Se ha creado una configuración completa de VS Code para que el proyecto EcoLink funcione correctamente:

### ✅ `settings.json`
- Apunta el intérprete de Python al `.venv` local
- Habilita Pylance para análisis de código
- Configura formateo automático con Black
- Excluye carpetas innecesarias del indexado

### ✅ `launch.json`
- **Backend FastAPI**: Ejecuta el servidor en puerto 8000
- **Frontend Reflex**: Ejecuta Reflex con hot reload

### ✅ `tasks.json`
Tareas disponibles (Ctrl+Shift+B):
- `Backend: Install Dependencies` - Instala requisitos del backend
- `Frontend: Install Dependencies` - Instala requisitos del frontend
- `Backend: Run FastAPI` - Ejecuta el servidor FastAPI
- `Frontend: Run Reflex` - Ejecuta la app Reflex
- `Database: Initialize` - Inicializa la base de datos
- `All: Install All Dependencies` - Instala todo de una vez

### ✅ `extensions.json`
Extensiones recomendadas para mejor desarrollo (VS Code las sugiere automáticamente)

---

## 🚀 Cómo usar

### Opción 1: Desde VS Code (Recomendado)
1. Abre VS Code
2. Presiona `Ctrl+Shift+B` para ver las tareas disponibles
3. Selecciona la tarea que quieras ejecutar

### Opción 2: Desde Terminal
```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar Backend (Terminal 1)
cd backend && python -m uvicorn app.main:app --reload

# Ejecutar Frontend (Terminal 2)
cd frontend && reflex run
```

### Opción 3: Usar Debug (F5)
1. Presiona `F5` en VS Code
2. Selecciona entre "Backend FastAPI" o "Frontend Reflex"
3. El código se ejecutará con breakpoints disponibles

---

## 🔍 Verificación

Para verificar que todo está correcto:

```bash
# Verificar que Python usa el entorno virtual
which python  # Debe mostrar .venv/bin/python

# Verificar que Reflex está instalado
python -c "import reflex; print('✅ Reflex OK')"

# Verificar que FastAPI está instalado
python -c "import fastapi; print('✅ FastAPI OK')"
```

---

## ⚙️ Solución de Problemas

### "Reflex no está instalado"
```bash
source .venv/bin/activate
pip install reflex --upgrade
```

### "No reconoce el intérprete de Python"
1. Presiona `Ctrl+Shift+P`
2. Escribe "Python: Select Interpreter"
3. Elige la opción que tenga `.venv` en la ruta

### "Los módulos no se encuentran"
```bash
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

---

## 📦 Estado de Instalación

✅ FastAPI instalado (0.135.3+)
✅ Reflex instalado (0.8.28+)
✅ SQLAlchemy instalado (2.0.48+)
✅ Pydantic instalado (2.12.5+)
✅ Todas las dependencias en `.venv`

