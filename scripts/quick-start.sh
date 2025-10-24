#!/bin/bash

# Script de instalación rápida para Sistema de Noticias con IA
# FastAPI + React + Claude

echo "╔══════════════════════════════════════════╗"
echo "║   Sistema de Noticias con IA - Setup   ║"
echo "║   FastAPI + React + Claude              ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Verificar Python
echo "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python 3 no está instalado. Por favor instalar Python 3.8+"
    exit 1
fi

# Verificar Node.js
echo "Verificando Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js encontrado: $NODE_VERSION"
else
    print_error "Node.js no está instalado. Por favor instalar Node.js 18+"
    exit 1
fi

# Crear estructura del proyecto
echo ""
echo "═══════════════════════════════════════"
echo "Configurando Backend (FastAPI)..."
echo "═══════════════════════════════════════"

# Backend setup
cd backend || exit

# Crear entorno virtual
echo "Creando entorno virtual de Python..."
python3 -m venv venv
print_success "Entorno virtual creado"

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate
print_success "Entorno virtual activado"

# Instalar dependencias
echo "Instalando dependencias de Python..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Dependencias de Python instaladas"

# Crear .env si no existe
if [ ! -f .env ]; then
    echo "Creando archivo .env..."
    cp .env.example .env
    print_success "Archivo .env creado"
fi

cd ..

# Frontend setup
echo ""
echo "═══════════════════════════════════════"
echo "Configurando Frontend (React)..."
echo "═══════════════════════════════════════"

cd frontend || exit

# Instalar dependencias
echo "Instalando dependencias de Node.js..."
npm install > /dev/null 2>&1
print_success "Dependencias de Node.js instaladas"

cd ..

# Resumen de instalación
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║      ✅ Instalación Completada!          ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "Para ejecutar el proyecto:"
echo ""
echo "1️⃣  Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload"
echo ""
echo "2️⃣  Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3️⃣  Acceder a:"
echo "   Frontend: http://localhost:5173"
echo "   Backend: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
print_success "¡Listo para desarrollar! 🚀"