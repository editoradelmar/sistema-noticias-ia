"""
Script para crear noticias de ejemplo con diferentes autores
Esto ayudará a probar el sistema de filtrado por autor
"""
import sys
from sqlalchemy.orm import Session, joinedload
from core.database import SessionLocal
from models import orm_models
from datetime import datetime, timedelta
import random

def create_sample_news():
    """Crear noticias de ejemplo con diferentes autores"""
    db: Session = SessionLocal()
    
    try:
        # Obtener usuarios para asignar como autores
        usuarios = db.query(orm_models.Usuario).filter(orm_models.Usuario.is_active == True).all()
        
        if len(usuarios) < 5:
            print("❌ Se necesitan al menos 5 usuarios activos. Ejecuta add_users.py primero.")
            return
        
        # Obtener secciones
        secciones = db.query(orm_models.Seccion).filter(orm_models.Seccion.activo == True).all()
        
        if len(secciones) == 0:
            print("❌ No hay secciones activas en el sistema.")
            return
        
        # Noticias de ejemplo
        noticias_ejemplo = [
            {
                'titulo': 'Nuevo desarrollo urbano en el centro de la ciudad',
                'contenido': 'Las autoridades municipales anunciaron un ambicioso proyecto de renovación urbana que transformará el centro histórico de la ciudad. El proyecto incluye la construcción de nuevas áreas verdes, mejoramiento del transporte público y modernización de la infraestructura.',
                'dias_atras': 1
            },
            {
                'titulo': 'Festival de música local atrae miles de visitantes',
                'contenido': 'El festival anual de música local concluyó con gran éxito, atrayendo a más de 10,000 visitantes durante el fin de semana. Los organizadores destacaron la participación de 25 bandas locales y el impacto económico positivo para la región.',
                'dias_atras': 2
            },
            {
                'titulo': 'Nueva tecnología mejora servicios de salud pública',
                'contenido': 'El hospital regional implementó un sistema de telemedicina que permitirá atender a pacientes en zonas rurales remotas. Esta iniciativa busca reducir las brechas de acceso a servicios médicos especializados.',
                'dias_atras': 3
            },
            {
                'titulo': 'Programa educativo beneficia a estudiantes de escasos recursos',
                'contenido': 'Un nuevo programa de becas estudiantiles beneficiará a 200 jóvenes de familias de bajos ingresos. La iniciativa incluye apoyo económico, material educativo y tutorías especializadas.',
                'dias_atras': 4
            },
            {
                'titulo': 'Inversión extranjera impulsa sector manufacturero',
                'contenido': 'Una empresa multinacional anunció la apertura de una nueva planta manufacturera que generará 500 empleos directos. La inversión de $50 millones fortalecerá la economía local y promoverá la transferencia de tecnología.',
                'dias_atras': 5
            },
            {
                'titulo': 'Campaña ambiental promueve el reciclaje urbano',
                'contenido': 'La municipalidad lanzó una campaña de concienciación ambiental que ha logrado incrementar el reciclaje doméstico en un 40%. La iniciativa incluye talleres comunitarios y la instalación de nuevos puntos de recolección.',
                'dias_atras': 6
            },
            {
                'titulo': 'Competencia deportiva regional reúne a jóvenes atletas',
                'contenido': 'Más de 300 jóvenes atletas participaron en los juegos deportivos regionales celebrados el fin de semana. La competencia incluyó 15 disciplinas deportivas y promovió valores de compañerismo y fair play.',
                'dias_atras': 7
            },
            {
                'titulo': 'Innovación tecnológica en agricultura local',
                'contenido': 'Agricultores locales adoptan nuevas técnicas de cultivo asistidas por drones y sensores IoT. Estas tecnologías prometen incrementar la productividad y reducir el impacto ambiental.',
                'dias_atras': 8
            }
        ]
        
        print(f"\n📰 Creando {len(noticias_ejemplo)} noticias de ejemplo")
        print("=" * 60)
        
        created_count = 0
        
        for i, noticia_data in enumerate(noticias_ejemplo):
            # Asignar autor aleatorio
            autor = random.choice(usuarios)
            
            # Asignar sección aleatoria
            seccion = random.choice(secciones)
            
            # Calcular fecha
            fecha_noticia = datetime.now() - timedelta(days=noticia_data['dias_atras'])
            
            # Crear noticia
            nueva_noticia = orm_models.Noticia(
                titulo=noticia_data['titulo'],
                contenido=noticia_data['contenido'],
                fecha=fecha_noticia,
                estado='publicado',
                usuario_id=autor.id,  # Usar usuario_id en lugar de autor_id
                autor=autor.username,  # Usar username en lugar de nombre_completo
                seccion_id=seccion.id,
                proyecto_id=None  # Sin proyecto asignado por ahora
            )
            
            db.add(nueva_noticia)
            db.commit()
            db.refresh(nueva_noticia)
            
            print(f"✅ Noticia #{nueva_noticia.id}: {noticia_data['titulo'][:50]}...")
            print(f"   👤 Autor: {autor.username} ({autor.nombre_completo})")
            print(f"   📂 Sección: {seccion.nombre}")
            print(f"   📅 Fecha: {fecha_noticia.strftime('%Y-%m-%d')}")
            print()
            
            created_count += 1
        
        print(f"📊 Resumen:")
        print(f"   ✅ Noticias creadas: {created_count}")
        print(f"   👥 Autores disponibles: {len(usuarios)}")
        print(f"   📂 Secciones disponibles: {len(secciones)}")
        print(f"\n💡 Ahora puedes probar los filtros por autor en el frontend!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

def list_news():
    """Listar noticias existentes"""
    db: Session = SessionLocal()
    
    try:
        # Usar joinedload para cargar las relaciones
        noticias = db.query(orm_models.Noticia).options(
            joinedload(orm_models.Noticia.usuario_creador),
            joinedload(orm_models.Noticia.seccion)
        ).order_by(orm_models.Noticia.fecha.desc()).limit(10).all()
        
        print(f"\n📰 Últimas {len(noticias)} noticias en el sistema")
        print("=" * 80)
        
        for noticia in noticias:
            # Usar la propiedad autor_nombre que definimos en el modelo
            autor_nombre = noticia.autor_nombre
            seccion_nombre = noticia.seccion.nombre if noticia.seccion else "Sin sección"
            
            print(f"ID: {noticia.id} | {noticia.titulo[:50]}...")
            print(f"   👤 {autor_nombre} | 📂 {seccion_nombre} | 📅 {noticia.fecha.strftime('%Y-%m-%d')}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def main():
    """Menú principal"""
    while True:
        print("\n📰 Crear Noticias de Ejemplo")
        print("=" * 40)
        print("1. Crear noticias de ejemplo")
        print("2. Listar noticias existentes")
        print("3. Salir")
        
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == '1':
            create_sample_news()
        elif choice == '2':
            list_news()
        elif choice == '3':
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()