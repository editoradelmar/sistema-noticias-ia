"""
Script para verificar noticias del administrador
"""
from sqlalchemy.orm import Session, joinedload
from core.database import SessionLocal
from models import orm_models

def check_admin_news():
    """Verificar noticias del administrador"""
    db: Session = SessionLocal()
    
    try:
        print("\n📰 Verificando noticias del administrador")
        print("=" * 50)
        
        # Buscar noticias por campo autor = 'admin'
        noticias_autor = db.query(orm_models.Noticia).filter(
            orm_models.Noticia.autor == 'admin'
        ).order_by(orm_models.Noticia.fecha.desc()).limit(5).all()
        
        print(f"📊 Noticias con autor='admin': {len(noticias_autor)}")
        for noticia in noticias_autor:
            print(f"   ID: {noticia.id} - {noticia.titulo[:50]}...")
            print(f"   Autor campo: '{noticia.autor}' | Usuario ID: {noticia.usuario_id}")
        
        print()
        
        # Buscar noticias por usuario_id = 1 (administrador)
        noticias_usuario = db.query(orm_models.Noticia).options(
            joinedload(orm_models.Noticia.usuario_creador)
        ).filter(orm_models.Noticia.usuario_id == 1).order_by(orm_models.Noticia.fecha.desc()).limit(5).all()
        
        print(f"📊 Noticias con usuario_id=1: {len(noticias_usuario)}")
        for noticia in noticias_usuario:
            autor_username = noticia.usuario_creador.username if noticia.usuario_creador else 'Sin usuario'
            print(f"   ID: {noticia.id} - {noticia.titulo[:50]}...")
            print(f"   Autor campo: '{noticia.autor}' | Username: '{autor_username}' | Usuario ID: {noticia.usuario_id}")
        
        print()
        
        # Verificar método to_dict() 
        if noticias_usuario:
            noticia_test = noticias_usuario[0]
            print(f"🔍 Test to_dict() para noticia ID {noticia_test.id}:")
            dict_data = noticia_test.to_dict()
            print(f"   autor: '{dict_data.get('autor')}'")
            print(f"   autor_id: {dict_data.get('autor_id')}")
            print(f"   autor_nombre: '{dict_data.get('autor_nombre')}'")
            print(f"   usuario_id: {dict_data.get('usuario_id')}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_news()