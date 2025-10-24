"""
Script para crear el primer usuario administrador
"""
import sys
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import orm_models
from utils.security import get_password_hash

def create_first_admin():
    """Crear el primer usuario administrador"""
    db: Session = SessionLocal()
    
    try:
        # Verificar si ya existe un admin
        admin_exists = db.query(orm_models.Usuario).filter(
            orm_models.Usuario.role == 'admin'
        ).first()
        
        if admin_exists:
            print("❌ Ya existe un usuario administrador:")
            print(f"   Email: {admin_exists.email}")
            print(f"   Username: {admin_exists.username}")
            return
        
        print("\n🔐 Crear Usuario Administrador")
        print("=" * 50)
        
        email = input("Email: ").strip().lower()
        username = input("Username: ").strip().lower()
        password = input("Contraseña (mín 6 caracteres): ").strip()
        nombre_completo = input("Nombre completo (opcional): ").strip()
        
        # Validaciones básicas
        if not email or '@' not in email:
            print("❌ Email inválido")
            return
        
        if not username or len(username) < 3:
            print("❌ Username debe tener al menos 3 caracteres")
            return
        
        if not password or len(password) < 6:
            print("❌ Contraseña debe tener al menos 6 caracteres")
            return
        
        # Verificar que no existan
        existing = db.query(orm_models.Usuario).filter(
            (orm_models.Usuario.email == email) |
            (orm_models.Usuario.username == username)
        ).first()
        
        if existing:
            print(f"❌ El email o username ya existe")
            return
        
        # Crear admin
        admin = orm_models.Usuario(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            nombre_completo=nombre_completo if nombre_completo else None,
            role='admin',
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("\n✅ Usuario administrador creado exitosamente!")
        print(f"   ID: {admin.id}")
        print(f"   Email: {admin.email}")
        print(f"   Username: {admin.username}")
        print(f"   Role: {admin.role}")
        print("\n💡 Ahora puedes hacer login en: POST /api/auth/login")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_first_admin()
