"""
Script para agregar múltiples usuarios al sistema de noticias
Permite crear periodistas, editores y otros autores para las noticias
"""
import sys
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import orm_models
from utils.security import get_password_hash

def add_default_users():
    """Agregar usuarios predeterminados del sistema"""
    db: Session = SessionLocal()
    
    # Lista de usuarios a crear
    users_to_create = [
        {
            'email': 'carlos.rodriguez@eldiario.com',
            'username': 'carlos.rodriguez',
            'password': 'periodista123',
            'nombre_completo': 'Carlos Rodríguez',
            'role': 'editor',
            'descripcion': 'Periodista de política y economía'
        },
        {
            'email': 'maria.garcia@eldiario.com',
            'username': 'maria.garcia',
            'password': 'periodista123',
            'nombre_completo': 'María García',
            'role': 'editor',
            'descripcion': 'Periodista de deportes y cultura'
        },
        {
            'email': 'luis.martinez@eldiario.com',
            'username': 'luis.martinez',
            'password': 'periodista123',
            'nombre_completo': 'Luis Martínez',
            'role': 'editor',
            'descripcion': 'Periodista de tecnología y ciencia'
        },
        {
            'email': 'ana.lopez@eldiario.com',
            'username': 'ana.lopez',
            'password': 'periodista123',
            'nombre_completo': 'Ana López',
            'role': 'editor',
            'descripcion': 'Periodista de salud y sociedad'
        },
        {
            'email': 'pedro.sanchez@eldiario.com',
            'username': 'pedro.sanchez',
            'password': 'periodista123',
            'nombre_completo': 'Pedro Sánchez',
            'role': 'editor',
            'descripcion': 'Periodista de entretenimiento y farándula'
        },
        {
            'email': 'laura.hernandez@eldiario.com',
            'username': 'laura.hernandez',
            'password': 'periodista123',
            'nombre_completo': 'Laura Hernández',
            'role': 'editor',
            'descripcion': 'Periodista de investigación'
        },
        {
            'email': 'jorge.ramirez@eldiario.com',
            'username': 'jorge.ramirez',
            'password': 'periodista123',
            'nombre_completo': 'Jorge Ramírez',
            'role': 'editor',
            'descripcion': 'Editor de sección regional'
        },
        {
            'email': 'sofia.torres@eldiario.com',
            'username': 'sofia.torres',
            'password': 'periodista123',
            'nombre_completo': 'Sofía Torres',
            'role': 'editor',
            'descripcion': 'Periodista de educación y juventud'
        }
    ]
    
    try:
        created_count = 0
        skipped_count = 0
        
        print("\n📰 Agregando usuarios periodistas al sistema")
        print("=" * 60)
        
        for user_data in users_to_create:
            # Verificar si ya existe
            existing = db.query(orm_models.Usuario).filter(
                (orm_models.Usuario.email == user_data['email']) |
                (orm_models.Usuario.username == user_data['username'])
            ).first()
            
            if existing:
                print(f"⚠️  Saltando {user_data['nombre_completo']} - ya existe")
                skipped_count += 1
                continue
            
            # Crear usuario
            new_user = orm_models.Usuario(
                email=user_data['email'],
                username=user_data['username'],
                hashed_password=get_password_hash(user_data['password']),
                nombre_completo=user_data['nombre_completo'],
                role=user_data['role'],
                is_active=True,
                is_superuser=False
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f"✅ Creado: {user_data['nombre_completo']} ({user_data['email']})")
            created_count += 1
        
        print(f"\n📊 Resumen:")
        print(f"   ✅ Usuarios creados: {created_count}")
        print(f"   ⚠️  Usuarios saltados: {skipped_count}")
        print(f"   📝 Total procesados: {len(users_to_create)}")
        
        if created_count > 0:
            print(f"\n💡 Contraseña para todos los nuevos usuarios: 'periodista123'")
            print(f"💡 Puedes cambiar las contraseñas usando update_passwords.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

def add_custom_user():
    """Agregar un usuario personalizado"""
    db: Session = SessionLocal()
    
    try:
        print("\n➕ Agregar Usuario Personalizado")
        print("=" * 40)
        
        email = input("Email: ").strip().lower()
        username = input("Username: ").strip().lower()
        password = input("Contraseña (mín 6 caracteres): ").strip()
        nombre_completo = input("Nombre completo: ").strip()
        
        print("\nRoles disponibles:")
        print("1. admin - Administrador del sistema")
        print("2. editor - Editor/Periodista")
        print("3. viewer - Solo lectura")
        
        role_choice = input("Selecciona rol (1-3): ").strip()
        role_map = {'1': 'admin', '2': 'editor', '3': 'viewer'}
        role = role_map.get(role_choice, 'viewer')
        
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
        
        if not nombre_completo:
            print("❌ Nombre completo es requerido")
            return
        
        # Verificar que no existan
        existing = db.query(orm_models.Usuario).filter(
            (orm_models.Usuario.email == email) |
            (orm_models.Usuario.username == username)
        ).first()
        
        if existing:
            print(f"❌ El email o username ya existe")
            return
        
        # Crear usuario
        new_user = orm_models.Usuario(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            nombre_completo=nombre_completo,
            role=role,
            is_active=True,
            is_superuser=(role == 'admin')
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"\n✅ Usuario creado exitosamente!")
        print(f"   ID: {new_user.id}")
        print(f"   Email: {new_user.email}")
        print(f"   Username: {new_user.username}")
        print(f"   Nombre: {new_user.nombre_completo}")
        print(f"   Role: {new_user.role}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

def list_users():
    """Listar todos los usuarios del sistema"""
    db: Session = SessionLocal()
    
    try:
        users = db.query(orm_models.Usuario).order_by(orm_models.Usuario.nombre_completo).all()
        
        print(f"\n👥 Usuarios en el sistema ({len(users)} total)")
        print("=" * 80)
        print(f"{'ID':<4} {'Nombre':<25} {'Email':<35} {'Role':<10} {'Activo'}")
        print("-" * 80)
        
        for user in users:
            active_status = "✅" if user.is_active else "❌"
            print(f"{user.id:<4} {user.nombre_completo:<25} {user.email:<35} {user.role:<10} {active_status}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()

def main():
    """Menú principal"""
    while True:
        print("\n📰 Gestión de Usuarios - Sistema de Noticias")
        print("=" * 50)
        print("1. Agregar usuarios periodistas predeterminados")
        print("2. Agregar usuario personalizado")
        print("3. Listar todos los usuarios")
        print("4. Salir")
        
        choice = input("\nSelecciona una opción (1-4): ").strip()
        
        if choice == '1':
            add_default_users()
        elif choice == '2':
            add_custom_user()
        elif choice == '3':
            list_users()
        elif choice == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()