"""
Script para verificar usernames específicos
"""
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import orm_models

def check_usernames():
    """Verificar usernames específicos"""
    db: Session = SessionLocal()
    
    try:
        print("\n🔍 Verificando usernames específicos")
        print("=" * 50)
        
        # Obtener todos los usuarios con detalles completos
        usuarios = db.query(orm_models.Usuario).order_by(orm_models.Usuario.id).all()
        
        for usuario in usuarios:
            print(f"ID: {usuario.id}")
            print(f"  Email: {usuario.email}")
            print(f"  Username: '{usuario.username}'")
            print(f"  Nombre: {usuario.nombre_completo}")
            print(f"  Role: {usuario.role}")
            print()
        
        # Buscar específicamente el administrador
        admin = db.query(orm_models.Usuario).filter(orm_models.Usuario.role == 'admin').first()
        if admin:
            print(f"🔐 ADMINISTRADOR ENCONTRADO:")
            print(f"   ID: {admin.id}")
            print(f"   Username: '{admin.username}'")
            print(f"   Email: {admin.email}")
            print(f"   Nombre: {admin.nombre_completo}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_usernames()