"""
Script para diagnosticar y corregir problemas de filtrado por autor
"""
from sqlalchemy.orm import Session, joinedload
from core.database import SessionLocal
from models import orm_models

def diagnose_autor_problems():
    """Diagnosticar problemas con el filtrado por autor"""
    db: Session = SessionLocal()
    
    try:
        print("\n🔍 DIAGNÓSTICO DEL PROBLEMA DE FILTRADO")
        print("=" * 60)
        
        # 1. Verificar usuarios
        print("\n1️⃣ USUARIOS EN EL SISTEMA:")
        usuarios = db.query(orm_models.Usuario).order_by(orm_models.Usuario.id).all()
        for user in usuarios:
            print(f"   ID {user.id}: username='{user.username}' | nombre='{user.nombre_completo}' | role='{user.role}'")
        
        # 2. Verificar noticias y sus relaciones
        print("\n2️⃣ NOTICIAS Y SUS AUTORES:")
        noticias = db.query(orm_models.Noticia).options(
            joinedload(orm_models.Noticia.usuario_creador)
        ).order_by(orm_models.Noticia.id.desc()).limit(10).all()
        
        for noticia in noticias:
            usuario_real = noticia.usuario_creador.username if noticia.usuario_creador else "NO ENCONTRADO"
            print(f"   Noticia ID {noticia.id}:")
            print(f"      campo autor: '{noticia.autor}'")
            print(f"      usuario_id: {noticia.usuario_id}")
            print(f"      usuario_real: '{usuario_real}'")
            print(f"      ✅ Coincide: {noticia.autor == usuario_real}")
            print()
        
        # 3. Verificar noticias del admin específicamente
        print("\n3️⃣ NOTICIAS DEL ADMIN (username='admin'):")
        admin = db.query(orm_models.Usuario).filter(orm_models.Usuario.username == 'admin').first()
        if admin:
            print(f"   Admin encontrado: ID {admin.id}, username='{admin.username}'")
            noticias_admin = db.query(orm_models.Noticia).filter(
                orm_models.Noticia.autor == 'admin'
            ).all()
            print(f"   Noticias con autor='admin': {len(noticias_admin)}")
            
            noticias_admin_id = db.query(orm_models.Noticia).filter(
                orm_models.Noticia.usuario_id == admin.id
            ).all()
            print(f"   Noticias con usuario_id={admin.id}: {len(noticias_admin_id)}")
            
            if len(noticias_admin) != len(noticias_admin_id):
                print("   ⚠️ INCONSISTENCIA DETECTADA!")
                
                # Mostrar noticias con autor='admin' pero usuario_id diferente
                problemas = db.query(orm_models.Noticia).filter(
                    orm_models.Noticia.autor == 'admin',
                    orm_models.Noticia.usuario_id != admin.id
                ).all()
                
                print(f"   📝 Noticias problemáticas ({len(problemas)}):")
                for noticia in problemas:
                    print(f"      ID {noticia.id}: autor='{noticia.autor}' pero usuario_id={noticia.usuario_id}")
        
        # 4. Revisar el filtro frontend
        print("\n4️⃣ SIMULACIÓN DEL FILTRO FRONTEND:")
        print("   Frontend filtra por: n.autor_id === parseInt(filtroUsuario)")
        print("   Donde autor_id es la propiedad que retorna usuario_id")
        
        test_user_id = 1  # ID del admin
        noticias_filtradas = db.query(orm_models.Noticia).filter(
            orm_models.Noticia.usuario_id == test_user_id
        ).all()
        print(f"   Filtro usuario_id={test_user_id}: {len(noticias_filtradas)} noticias")
        
        for noticia in noticias_filtradas[:3]:  # Mostrar solo las primeras 3
            print(f"      ID {noticia.id}: '{noticia.titulo[:40]}...'")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def fix_autor_inconsistencies():
    """Corregir inconsistencias entre autor y usuario_id"""
    db: Session = SessionLocal()
    
    try:
        print("\n🔧 CORRIGIENDO INCONSISTENCIAS")
        print("=" * 40)
        
        # Buscar noticias donde autor no coincide con usuario_id
        noticias = db.query(orm_models.Noticia).options(
            joinedload(orm_models.Noticia.usuario_creador)
        ).all()
        
        fixed_count = 0
        
        for noticia in noticias:
            if noticia.usuario_creador:
                username_real = noticia.usuario_creador.username
                
                # Si el campo autor no coincide con el username real
                if noticia.autor != username_real:
                    print(f"🔄 Noticia ID {noticia.id}:")
                    print(f"   autor: '{noticia.autor}' → '{username_real}'")
                    
                    noticia.autor = username_real
                    fixed_count += 1
            
            # También verificar el caso inverso: autor correcto pero usuario_id incorrecto
            elif noticia.autor:
                # Buscar usuario por username
                usuario = db.query(orm_models.Usuario).filter(
                    orm_models.Usuario.username == noticia.autor
                ).first()
                
                if usuario and noticia.usuario_id != usuario.id:
                    print(f"🔄 Noticia ID {noticia.id}:")
                    print(f"   usuario_id: {noticia.usuario_id} → {usuario.id}")
                    
                    noticia.usuario_id = usuario.id
                    fixed_count += 1
        
        if fixed_count > 0:
            db.commit()
            print(f"\n✅ Corregidas {fixed_count} inconsistencias")
        else:
            print("\n✅ No se encontraron inconsistencias")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def main():
    """Menú principal"""
    while True:
        print("\n🔍 Diagnóstico de Filtrado por Autor")
        print("=" * 40)
        print("1. Diagnosticar problemas")
        print("2. Corregir inconsistencias")
        print("3. Ambos (diagnóstico + corrección)")
        print("4. Salir")
        
        choice = input("\nSelecciona una opción (1-4): ").strip()
        
        if choice == '1':
            diagnose_autor_problems()
        elif choice == '2':
            fix_autor_inconsistencies()
        elif choice == '3':
            diagnose_autor_problems()
            fix_autor_inconsistencies()
            print("\n🔄 Ejecutando diagnóstico post-corrección...")
            diagnose_autor_problems()
        elif choice == '4':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()