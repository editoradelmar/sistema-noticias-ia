"""
Script para recrear todas las tablas de la base de datos
⚠️ SOLO PARA DESARROLLO - Borra todos los datos
"""
from core.database import engine, Base, drop_all_tables, init_db
from config import settings

if __name__ == "__main__":
    if not settings.DEBUG:
        print("❌ Este script solo puede ejecutarse en modo DEBUG")
        exit(1)
    
    print("⚠️  ADVERTENCIA: Esto eliminará TODOS los datos de la base de datos")
    respuesta = input("¿Estás seguro? (escribe 'SI' para confirmar): ")
    
    if respuesta != "SI":
        print("❌ Operación cancelada")
        exit(0)
    
    print("\n🗑️  Eliminando todas las tablas...")
    drop_all_tables()
    
    print("🔨 Creando tablas con nueva estructura...")
    init_db()
    
    print("✅ Base de datos recreada exitosamente!")
    print("\n📋 Ahora puedes:")
    print("   1. Reiniciar el servidor: uvicorn main:app --reload")
    print("   2. Crear datos de ejemplo: curl -X POST http://localhost:8000/api/noticias/seed")
