"""
Script para eliminar la columna 'autor' de la tabla noticias
después de migrar a usar usuario_id como fuente de verdad

ADVERTENCIA: Este script elimina la columna 'autor' PERMANENTEMENTE.
Asegúrate de haber respaldado la base de datos antes de ejecutar.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import engine, SessionLocal
from models import orm_models

def verificar_usuario_id_consistency():
    """Verificar que todas las noticias tengan usuario_id válido"""
    db = SessionLocal()
    try:
        print("\n🔍 Verificando consistencia de usuario_id...")
        
        # Contar noticias sin usuario_id
        noticias_sin_usuario = db.query(orm_models.Noticia).filter(
            orm_models.Noticia.usuario_id.is_(None)
        ).count()
        
        if noticias_sin_usuario > 0:
            print(f"❌ ERROR: {noticias_sin_usuario} noticias sin usuario_id válido")
            print("Debes corregir estas noticias antes de eliminar la columna autor")
            return False
        
        # Verificar que todos los usuario_id existen
        noticias_usuario_invalido = db.query(orm_models.Noticia).filter(
            ~orm_models.Noticia.usuario_id.in_(
                db.query(orm_models.Usuario.id)
            )
        ).count()
        
        if noticias_usuario_invalido > 0:
            print(f"❌ ERROR: {noticias_usuario_invalido} noticias con usuario_id inválido")
            print("Debes corregir estas referencias antes de proceder")
            return False
        
        print("✅ Todas las noticias tienen usuario_id válido")
        return True
        
    except Exception as e:
        print(f"Error verificando consistencia: {e}")
        return False
    finally:
        db.close()

def backup_autor_data():
    """Crear un respaldo de los datos de la columna autor"""
    db = SessionLocal()
    try:
        print("\n💾 Creando respaldo de datos de la columna autor...")
        
        # Crear tabla temporal para respaldo
        backup_query = """
        CREATE TABLE IF NOT EXISTS autor_backup AS 
        SELECT id, autor, usuario_id, titulo, 
               created_at, updated_at
        FROM noticias 
        WHERE autor IS NOT NULL;
        """
        
        db.execute(text(backup_query))
        db.commit()
        
        # Verificar respaldo
        backup_count = db.execute(text("SELECT COUNT(*) FROM autor_backup")).scalar()
        print(f"✅ Respaldo creado: {backup_count} registros guardados en tabla 'autor_backup'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return False
    finally:
        db.close()

def drop_autor_column():
    """Eliminar la columna autor de la tabla noticias"""
    
    try:
        print("\n🗑️ Eliminando columna 'autor' de la tabla noticias...")
        
        with engine.connect() as connection:
            # Ejecutar DROP COLUMN
            connection.execute(text("ALTER TABLE noticias DROP COLUMN IF EXISTS autor"))
            connection.commit()
        
        print("✅ Columna 'autor' eliminada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error eliminando columna: {e}")
        return False

def verify_migration():
    """Verificar que la migración fue exitosa"""
    
    try:
        print("\n🔍 Verificando migración...")
        
        with engine.connect() as connection:
            # Verificar que la columna autor ya no existe
            columns_query = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'noticias' 
            AND column_name = 'autor'
            """
            
            result = connection.execute(text(columns_query)).fetchone()
            
            if result:
                print("❌ ERROR: La columna 'autor' todavía existe")
                return False
            else:
                print("✅ Columna 'autor' eliminada correctamente")
            
            # Verificar que las noticias siguen funcionando
            noticias_count = connection.execute(text("SELECT COUNT(*) FROM noticias")).scalar()
            print(f"✅ {noticias_count} noticias mantenidas en la tabla")
            
            return True
            
    except Exception as e:
        print(f"❌ Error verificando migración: {e}")
        return False

def main():
    print("🚀 MIGRACIÓN: Eliminación de columna 'autor'")
    print("=" * 50)
    
    # Paso 1: Verificar consistencia
    if not verificar_usuario_id_consistency():
        print("\n❌ Migración cancelada: Inconsistencias en usuario_id")
        return False
    
    # Paso 2: Crear respaldo
    if not backup_autor_data():
        print("\n❌ Migración cancelada: Error en respaldo")
        return False
    
    # Confirmación del usuario
    print("\n⚠️ ADVERTENCIA: Se eliminará la columna 'autor' PERMANENTEMENTE")
    print("Los datos están respaldados en la tabla 'autor_backup'")
    confirm = input("¿Continuar con la migración? (escribir 'SI' para confirmar): ")
    
    if confirm != 'SI':
        print("❌ Migración cancelada por el usuario")
        return False
    
    # Paso 3: Eliminar columna
    if not drop_autor_column():
        print("\n❌ Migración fallida")
        return False
    
    # Paso 4: Verificar migración
    if not verify_migration():
        print("\n❌ Verificación fallida")
        return False
    
    print("\n🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 50)
    print("✅ Columna 'autor' eliminada")
    print("✅ Datos respaldados en 'autor_backup'")
    print("✅ Sistema usando usuario_id como fuente de verdad")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Migración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")