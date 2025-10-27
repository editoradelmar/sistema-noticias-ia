"""
Script para migrar el campo autor de nombre_completo a username
Actualiza todas las noticias existentes para usar username en lugar de nombre_completo
"""
from sqlalchemy.orm import Session, joinedload
from core.database import SessionLocal
from models import orm_models

def migrate_autor_to_username():
    """Migrar el campo autor para usar username en lugar de nombre_completo"""
    db: Session = SessionLocal()
    
    try:
        print("\n🔄 Migrando campo autor de nombre_completo a username")
        print("=" * 60)
        
        # Obtener todas las noticias que tienen usuario_id
        noticias = db.query(orm_models.Noticia).options(
            joinedload(orm_models.Noticia.usuario_creador)
        ).filter(orm_models.Noticia.usuario_id.isnot(None)).all()
        
        updated_count = 0
        
        for noticia in noticias:
            if noticia.usuario_creador:
                old_autor = noticia.autor
                new_autor = noticia.usuario_creador.username
                
                # Solo actualizar si es diferente
                if old_autor != new_autor:
                    noticia.autor = new_autor
                    updated_count += 1
                    
                    print(f"📝 Noticia ID {noticia.id}: '{old_autor}' → '{new_autor}'")
        
        if updated_count > 0:
            db.commit()
            print(f"\n✅ Migración completada:")
            print(f"   📊 Noticias actualizadas: {updated_count}")
            print(f"   📊 Total de noticias con usuario: {len(noticias)}")
        else:
            print("\n✅ No hay noticias que requieran actualización")
            
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def verify_migration():
    """Verificar que la migración se haya realizado correctamente"""
    db: Session = SessionLocal()
    
    try:
        print(f"\n🔍 Verificando migración...")
        print("=" * 40)
        
        # Obtener algunas noticias para verificar
        noticias = db.query(orm_models.Noticia).options(
            joinedload(orm_models.Noticia.usuario_creador)
        ).filter(orm_models.Noticia.usuario_id.isnot(None)).limit(5).all()
        
        for noticia in noticias:
            if noticia.usuario_creador:
                autor_campo = noticia.autor
                username_real = noticia.usuario_creador.username
                nombre_completo = noticia.usuario_creador.nombre_completo
                
                status = "✅" if autor_campo == username_real else "❌"
                
                print(f"{status} Noticia ID {noticia.id}:")
                print(f"   Campo autor: '{autor_campo}'")
                print(f"   Username real: '{username_real}'")
                print(f"   Nombre completo: '{nombre_completo}'")
                print()
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
    finally:
        db.close()

def main():
    """Menú principal"""
    while True:
        print("\n🔄 Migración de Campo Autor")
        print("=" * 35)
        print("1. Ejecutar migración (nombre_completo → username)")
        print("2. Verificar estado actual")
        print("3. Salir")
        
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == '1':
            migrate_autor_to_username()
        elif choice == '2':
            verify_migration()
        elif choice == '3':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()