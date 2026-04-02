#!/bin/bash

# Script para instalar y ejecutar EcoLink completamente

echo "🚀 Instalando EcoLink..."

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Configurando Backend...${NC}"
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Inicializar BD
echo -e "${BLUE}🗄️  Inicializando Base de Datos...${NC}"
python init_db.py

echo -e "${GREEN}✅ Backend configurado!${NC}"
echo "Para ejecutar backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"

# Volver al directorio raíz
cd ..

echo ""
echo -e "${BLUE}📦 Configurando Frontend...${NC}"
cd frontend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

echo -e "${GREEN}✅ Frontend configurado!${NC}"
echo "Para ejecutar frontend: cd frontend && source venv/bin/activate && reflex run"

echo ""
echo -e "${GREEN}🎉 ¡Instalación completada!${NC}"
echo ""
echo "Para ejecutar la aplicación:"
echo "1. Terminal 1 - Backend:"
echo "   cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo ""
echo "2. Terminal 2 - Frontend:"
echo "   cd frontend && source venv/bin/activate && reflex run"
echo ""
echo "Aplicación disponible en: http://localhost:3000"
echo "API disponible en: http://localhost:8000/docs"
