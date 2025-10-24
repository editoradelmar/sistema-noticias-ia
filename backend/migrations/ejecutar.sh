#!/bin/bash
# ============================================
# Script para ejecutar migración Fase 6
# ============================================

echo ""
echo "============================================"
echo "  MIGRACIÓN FASE 6 - Sistema de Maestros"
echo "============================================"
echo ""

# Obtener directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

echo "[1/3] Activando entorno virtual..."
source venv/bin/activate

echo ""
echo "[2/3] Verificando conexión a PostgreSQL..."
python3 -c "import psycopg2; from config import settings; conn = psycopg2.connect(settings.DATABASE_URL); print('✅ Conexión exitosa'); conn.close()" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: No se pudo conectar a PostgreSQL"
    echo ""
    echo "Verificar:"
    echo "  - PostgreSQL está corriendo"
    echo "  - Credenciales en .env son correctas"
    echo "  - Base de datos 'noticias_ia' existe"
    echo ""
    exit 1
fi

echo ""
echo "[3/3] Ejecutando migración SQL..."
python3 migrations/ejecutar_fase_6.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error en la migración"
    exit 1
fi

echo ""
echo "============================================"
echo "  MIGRACIÓN COMPLETADA"
echo "============================================"
echo ""
