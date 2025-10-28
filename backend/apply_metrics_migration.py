#!/usr/bin/env python3
"""
Script para aplicar la migración de métricas de valor periodístico
"""
import sys
import os
sys.path.append('.')

from sqlalchemy import text
from core.database import engine

def apply_migration():
    try:
        # Leer el archivo SQL con codificación UTF-8
        sql_file = 'migrations/add_metricas_valor_periodistico.sql'
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir en statements individuales
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        with engine.connect() as conn:
            for statement in statements:
                if statement:
                    try:
                        print(f"Ejecutando: {statement[:50]}...")
                        conn.execute(text(statement))
                        conn.commit()
                        print("✅ Ejecutado correctamente")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        if "already exists" in str(e).lower():
                            print("⚠️ La tabla ya existe, continuando...")
                        else:
                            raise
        
        print("🎉 Migración completada exitosamente")
        
    except Exception as e:
        print(f"💥 Error aplicando migración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    apply_migration()