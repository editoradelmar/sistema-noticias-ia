@echo off
REM Script para configurar PostgreSQL en Windows
REM Ejecutar como Administrador

echo ========================================
echo   Setup PostgreSQL - Noticias IA
echo ========================================
echo.

REM Verificar si psql está disponible
where psql >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PostgreSQL no encontrado en PATH
    echo.
    echo Instala PostgreSQL desde: https://www.postgresql.org/download/windows/
    echo O agrega PostgreSQL al PATH: C:\Program Files\PostgreSQL\16\bin
    pause
    exit /b 1
)

echo [1/3] PostgreSQL encontrado
echo.

REM Solicitar password de postgres
set /p PGPASSWORD="Ingresa password de usuario postgres: "
echo.

REM Crear base de datos
echo [2/3] Creando base de datos noticias_ia...
psql -U postgres -c "CREATE DATABASE noticias_ia WITH ENCODING='UTF8';"
if %ERRORLEVEL% EQU 0 (
    echo [OK] Base de datos creada
) else (
    echo [INFO] Base de datos ya existe o error
)
echo.

REM Crear extensiones
echo [3/3] Configurando extensiones...
psql -U postgres -d noticias_ia -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
psql -U postgres -d noticias_ia -c "CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";"
echo.

echo ========================================
echo   SETUP COMPLETADO
echo ========================================
echo.
echo Proximos pasos:
echo   1. cd backend
echo   2. pip install -r requirements.txt
echo   3. alembic upgrade head
echo   4. python scripts/migrate_data.py
echo.
pause
