#!/bin/bash
# SCRIPT RÁPIDO PARA INICIAR ECOLINK CON POSTGRESQL
# Ejecutar este script desde la raíz del proyecto

echo "🚀 EcoLink - Setup Rápido"
echo "=========================="

# Verificar si PostgreSQL está corriendo
echo "📍 Verificando PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL no está instalado. Descargar desde: https://www.postgresql.org/download/windows/"
    exit 1
fi

# Crear directorio .venv si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv .venv
fi

# Activar venv
echo "✨ Activando entorno virtual..."
source .venv/Scripts/activate || .venv\\Scripts\\activate.bat

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Inicializar BD
echo "🗄️ Inicializando base de datos..."
cd backend
python init_db.py
cd ..

echo "✅ Setup completado!"
echo ""
echo "Próximos pasos:"
echo "1. Terminal 1 - Backend:"
echo "   source .venv/Scripts/activate"
echo "   cd backend"
echo "   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Terminal 2 - Frontend:"
echo "   source .venv/Scripts/activate"
echo "   cd frontend"
echo "   reflex run"
echo ""
echo "3. Frontend disponible en: http://localhost:3000"
echo "4. API disponible en: http://localhost:8000"
echo "5. Docs API en: http://localhost:8000/docs"
