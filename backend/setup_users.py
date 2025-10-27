"""
Script para crear todos los usuarios del sistema de noticias de una vez
Incluye usuarios originales y nuevos periodistas/editores
"""
import sys
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models import orm_models
from utils.security import get_password_hash

def crear_todos_usuarios():
    """Crear todos los usuarios del sistema"""
    db: Session = SessionLocal()
    
    # Lista completa de usuarios
    todos_usuarios = [
        # Usuarios originales del sistema
        {
            'email': 'admin@sistema.com',
            'username': 'admin',
            'password': 'admin123456',
            'nombre_completo': 'Administrador del Sistema',
            'role': 'admin',
            'descripcion': 'Administrador principal del sistema'
        },
        {
            'email': 'editor@sistema.com',
            'username': 'editor',
            'password': 'editor123',
            'nombre_completo': 'Editor General',
            'role': 'editor',
            'descripcion': 'Editor general del sistema'
        },
        {
            'email': 'viewer@sistema.com',
            'username': 'viewer',
            'password': 'viewer123',
            'nombre_completo': 'Usuario Visualizador',
            'role': 'viewer',
            'descripcion': 'Usuario con permisos de solo lectura'
        },
        # Nuevos periodistas y editores
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
        
        print("\n📰 Creando todos los usuarios del sistema")
        print("=" * 70)
        
        for user_data in todos_usuarios:
            # Verificar si ya existe
            existing = db.query(orm_models.Usuario).filter(
                (orm_models.Usuario.email == user_data['email']) |
                (orm_models.Usuario.username == user_data['username'])
            ).first()
            
            if existing:
                print(f"⚠️  Saltando {user_data['nombre_completo']:<25} - ya existe")
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
                is_superuser=(user_data['role'] == 'admin')
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            role_icon = "👑" if user_data['role'] == 'admin' else "✏️" if user_data['role'] == 'editor' else "👁️"
            print(f"✅ {role_icon} {user_data['nombre_completo']:<25} ({user_data['email']})")
            created_count += 1
        
        print(f"\n📊 Resumen de creación:")
        print(f"   ✅ Usuarios creados: {created_count}")
        print(f"   ⚠️  Usuarios saltados: {skipped_count}")
        print(f"   📝 Total procesados: {len(todos_usuarios)}")
        
        if created_count > 0:
            print(f"\n🔑 Credenciales de acceso:")
            print("=" * 70)
            
            # Mostrar credenciales por categoría
            print("\n👑 ADMINISTRADORES:")
            for user in todos_usuarios:
                if user['role'] == 'admin':
                    print(f"   Email: {user['email']}")
                    print(f"   Password: {user['password']}")
                    print()
            
            print("✏️  EDITORES/PERIODISTAS:")
            for user in todos_usuarios:
                if user['role'] == 'editor':
                    print(f"   {user['nombre_completo']}: {user['email']} / {user['password']}")
            
            print("\n👁️  VISUALIZADORES:")
            for user in todos_usuarios:
                if user['role'] == 'viewer':
                    print(f"   Email: {user['email']}")
                    print(f"   Password: {user['password']}")
        
        print(f"\n💡 Puedes usar estos usuarios como autores de noticias")
        print(f"💡 Para cambiar contraseñas, usa: python update_passwords.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def verificar_usuarios():
    """Verificar qué usuarios ya existen"""
    db: Session = SessionLocal()
    
    try:
        users = db.query(orm_models.Usuario).order_by(orm_models.Usuario.role, orm_models.Usuario.nombre_completo).all()
        
        print(f"\n👥 Usuarios actuales en el sistema ({len(users)} total)")
        print("=" * 80)
        
        admin_count = editor_count = viewer_count = 0
        
        for user in users:
            role_icon = "👑" if user.role == 'admin' else "✏️" if user.role == 'editor' else "👁️"
            active_status = "✅" if user.is_active else "❌"
            
            print(f"{role_icon} {user.nombre_completo:<25} {user.email:<35} {active_status}")
            
            if user.role == 'admin':
                admin_count += 1
            elif user.role == 'editor':
                editor_count += 1
            elif user.role == 'viewer':
                viewer_count += 1
        
        print(f"\n📊 Resumen por roles:")
        print(f"   👑 Administradores: {admin_count}")
        print(f"   ✏️  Editores/Periodistas: {editor_count}")
        print(f"   👁️  Visualizadores: {viewer_count}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()

def main():
    """Función principal"""
    print("\n📰 Setup Completo de Usuarios - Sistema de Noticias")
    print("=" * 60)
    print("1. Verificar usuarios existentes")
    print("2. Crear todos los usuarios del sistema")
    print("3. Salir")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == '1':
        verificar_usuarios()
    elif choice == '2':
        print("\n⚠️  ¿Estás seguro de que quieres crear todos los usuarios?")
        print("   Esto creará 11 usuarios incluyendo administradores, editores y periodistas.")
        confirm = input("   Escribe 'SI' para confirmar: ").strip().upper()
        
        if confirm == 'SI':
            crear_todos_usuarios()
        else:
            print("❌ Operación cancelada")
    elif choice == '3':
        print("👋 ¡Hasta luego!")
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    main()