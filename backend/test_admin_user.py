#!/usr/bin/env python3
"""
Script para probar la conexión y verificar el usuario admin
"""
import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from core.database import engine
from models.orm_models import Usuario

def test_usuario_admin():
    with Session(engine) as db:
        # Buscar usuarios admin
        admins = db.query(Usuario).filter(Usuario.role == 'admin').all()
        
        print("👤 Usuarios con rol 'admin':")
        for admin in admins:
            print(f"  - ID: {admin.id}, Username: {admin.username}, Email: {admin.email}")
            print(f"    Role: {admin.role}, Active: {admin.is_active}")
        
        if not admins:
            print("⚠️ No se encontraron usuarios admin")
            
            # Mostrar todos los usuarios
            users = db.query(Usuario).all()
            print(f"\n📋 Todos los usuarios ({len(users)}):")
            for user in users:
                print(f"  - {user.username} ({user.role}) - {user.email}")
        
        return len(admins) > 0

if __name__ == "__main__":
    try:
        print("🔍 Verificando usuarios admin en la base de datos...")
        has_admin = test_usuario_admin()
        if has_admin:
            print("✅ Configuración de admin correcta")
        else:
            print("❌ No hay usuarios admin disponibles")
    except Exception as e:
        print(f"💥 Error: {e}")