"""
Script para actualizar contraseñas de usuarios
Regenera los hashes con la versión correcta de bcrypt
"""
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import orm_models
from utils.security import get_password_hash

def actualizar_contraseñas():
    """Actualizar contraseñas de los usuarios existentes"""
    db: Session = SessionLocal()
    
    try:
        # Definir usuarios y sus contraseñas
        usuarios_passwords = [
            {
                "email": "admin@sistema.com",
                "password": "admin123456"
            },
            {
                "email": "editor@sistema.com",
                "password": "editor123"
            },
            {
                "email": "viewer@sistema.com",
                "password": "viewer123"
            }
        ]
        
        print("\n🔐 Actualizando contraseñas de usuarios...")
        print("=" * 60)
        
        for user_data in usuarios_passwords:
            # Buscar usuario
            user = db.query(orm_models.Usuario).filter(
                orm_models.Usuario.email == user_data["email"]
            ).first()
            
            if user:
                # Generar nuevo hash
                new_hash = get_password_hash(user_data["password"])
                user.hashed_password = new_hash
                
                print(f"✅ {user.email:<30} → Contraseña actualizada")
            else:
                print(f"❌ {user_data['email']:<30} → Usuario no encontrado")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("✅ Contraseñas actualizadas correctamente!")
        print("\n📋 Credenciales:")
        print("-" * 60)
        for user_data in usuarios_passwords:
            user = db.query(orm_models.Usuario).filter(
                orm_models.Usuario.email == user_data["email"]
            ).first()
            if user:
                print(f"  Email: {user.email}")
                print(f"  Password: {user_data['password']}")
                print(f"  Role: {user.role}")
                print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    actualizar_contraseñas()
