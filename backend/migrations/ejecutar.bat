@echo off
REM ============================================
REM Script para ejecutar migración Fase 6
REM ============================================

echo.
echo ============================================
echo   MIGRACION FASE 6 - Sistema de Maestros
echo ============================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0.."

echo [1/3] Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo [2/3] Verificando conexion a PostgreSQL...
python -c "import psycopg2; from config import settings; conn = psycopg2.connect(settings.DATABASE_URL); print('✅ Conexion exitosa'); conn.close()" 2>nul
if errorlevel 1 (
    echo ❌ Error: No se pudo conectar a PostgreSQL
    echo.
    echo Verificar:
    echo   - PostgreSQL esta corriendo
    echo   - Credenciales en .env son correctas
    echo   - Base de datos 'noticias_ia' existe
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Ejecutando migracion SQL...
python migrations\ejecutar_fase_6.py

if errorlevel 1 (
    echo.
    echo ❌ Error en la migracion
    pause
    exit /b 1
)

echo.
echo ============================================
echo   MIGRACION COMPLETADA
echo ============================================
echo.
pause
