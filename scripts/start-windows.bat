@echo off
REM Script de inicio para Windows
REM Sistema de Noticias con IA

color 0A
echo ========================================
echo   Sistema de Noticias con IA
echo   FastAPI + React + Claude
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado
    echo Por favor instalar Python 3.8+
    pause
    exit /b 1
)

REM Verificar Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no esta instalado
    echo Por favor instalar Node.js 18+
    pause
    exit /b 1
)

echo [OK] Python y Node.js detectados
echo.

REM Iniciar Backend
echo ========================================
echo Iniciando Backend (FastAPI)...
echo ========================================
cd backend
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

start cmd /k "title Backend - FastAPI && venv\Scripts\activate.bat && uvicorn main:app --reload"

cd ..
timeout /t 3 /nobreak >nul

REM Iniciar Frontend
echo ========================================
echo Iniciando Frontend (React)...
echo ========================================
cd frontend

if not exist node_modules (
    echo Instalando dependencias...
    call npm install
)

start cmd /k "title Frontend - React && npm run dev"

cd ..

echo.
echo ========================================
echo   Servidores iniciados!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Presiona cualquier tecla para salir...
pause >nul