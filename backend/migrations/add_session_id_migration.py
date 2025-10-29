#!/usr/bin/env python3
"""
Script para añadir columna session_id a métricas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import SessionLocal

def add_session_id_column():
    """Añade columna session_id a la tabla metricas_valor_periodistico"""
    db = SessionLocal()
    try:
        print("🔧 Añadiendo columna session_id...")
        
        # 1. Añadir columna session_id
        db.execute(text("ALTER TABLE metricas_valor_periodistico ADD COLUMN session_id VARCHAR(100);"))
        print("✅ Columna session_id añadida")
        
        # 2. Crear índice
        db.execute(text("CREATE INDEX idx_metricas_session_id ON metricas_valor_periodistico(session_id);"))
        print("✅ Índice creado")
        
        # 3. Hacer noticia_id nullable
        db.execute(text("ALTER TABLE metricas_valor_periodistico ALTER COLUMN noticia_id DROP NOT NULL;"))
        print("✅ noticia_id ahora es nullable")
        
        # 4. Añadir constraint
        db.execute(text("""
            ALTER TABLE metricas_valor_periodistico 
            ADD CONSTRAINT chk_noticia_or_session 
            CHECK (
                (noticia_id IS NOT NULL AND session_id IS NULL) OR 
                (noticia_id IS NULL AND session_id IS NOT NULL)
            );
        """))
        print("✅ Constraint añadido")
        
        db.commit()
        print("🎉 Migración completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante migración: {e}")
        db.rollback()
        
        # Verificar si ya existe la columna
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'metricas_valor_periodistico' 
            AND column_name = 'session_id';
        """))
        
        if result.fetchone():
            print("✅ La columna session_id ya existe")
        else:
            raise e
    finally:
        db.close()

if __name__ == "__main__":
    add_session_id_column()