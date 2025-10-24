"""
Script para migrar datos desde almacenamiento en memoria a PostgreSQL
Ejecutar: python scripts/migrate_data.py
"""
import sys
import os

# Agregar directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from core.database import SessionLocal, init_db
from models import orm_models


def migrar_noticias_ejemplo():
    """Migrar noticias de ejemplo a PostgreSQL"""
    
    # Mapeo de nombre de sección a ID (ajustar según los IDs reales en la tabla seccion)
    seccion_map = {
        "tecnologia": 1,
        "ia": 2,
        "desarrollo": 3,
        "negocios": 4,
        "ciencia": 5,
        "general": 6
    }
    datos_ejemplo = [
        {
            "titulo": "FastAPI supera a Flask en popularidad",
            "contenido": "Según las últimas estadísticas, FastAPI ha superado a Flask como el framework web más utilizado en Python para nuevos proyectos en 2025.",
            "seccion_id": seccion_map["tecnologia"],
            "autor": "Sistema"
        },
        {
            "titulo": "Apple presenta el iPhone 16 con chip M4",
            "contenido": "La nueva generación del iPhone incorpora el revolucionario chip M4, ofreciendo un 40% más de rendimiento que su predecesor.",
            "seccion_id": seccion_map["tecnologia"],
            "autor": "Sistema"
        },
        {
            "titulo": "Claude 4 establece nuevo récord en benchmarks",
            "contenido": "El modelo Claude Sonnet 4.5 ha demostrado capacidades superiores en razonamiento y generación de código.",
            "seccion_id": seccion_map["ia"],
            "autor": "Sistema"
        },
        {
            "titulo": "GPT-5 supera pruebas de razonamiento humano",
            "contenido": "OpenAI ha revelado que GPT-5 puede resolver problemas de física avanzada y matemáticas a nivel de doctorado.",
            "seccion_id": seccion_map["ia"],
            "autor": "Sistema"
        },
        {
            "titulo": "Python 3.13 trae mejoras de rendimiento del 60%",
            "contenido": "La nueva versión de Python incluye el JIT compiler experimental y optimizaciones significativas.",
            "seccion_id": seccion_map["desarrollo"],
            "autor": "Sistema"
        },
        {
            "titulo": "Startups de IA reciben $100B en inversión",
            "contenido": "Las empresas de inteligencia artificial han recibido inversiones récord en el primer trimestre de 2025.",
            "seccion_id": seccion_map["negocios"],
            "autor": "Sistema"
        },
        {
            "titulo": "Científicos logran fusión nuclear sostenible",
            "contenido": "El reactor de fusión ITER ha logrado mantener una reacción sostenida durante 100 segundos.",
            "seccion_id": seccion_map["ciencia"],
            "autor": "Sistema"
        },
        {
            "titulo": "Juegos Olímpicos de París 2024 baten récords",
            "contenido": "Los Juegos Olímpicos fueron los más vistos de la historia con 5 mil millones de espectadores.",
            "seccion_id": seccion_map["general"],
            "autor": "Sistema"
        }
    ]
    
    db = SessionLocal()
    
    try:
        print("🔄 Iniciando migración de datos...")
        
        count = db.query(orm_models.Noticia).count()
        if count > 0:
            respuesta = input(f"⚠️  Ya hay {count} noticias. ¿Continuar? (s/n): ")
            if respuesta.lower() != 's':
                print("❌ Migración cancelada")
                return
        
        for dato in datos_ejemplo:
            noticia = orm_models.Noticia(**dato)
            db.add(noticia)
        
        db.commit()
        
        total = db.query(orm_models.Noticia).count()
        print(f"✅ Migración completada: {total} noticias en la base de datos")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        
    finally:
        db.close()


def crear_proyecto_default():
    """Crear proyecto por defecto"""
    db = SessionLocal()
    
    try:
        proyecto = db.query(orm_models.Proyecto).filter(
            orm_models.Proyecto.nombre == "Proyecto Default"
        ).first()
        
        if proyecto:
            print("ℹ️  Proyecto default ya existe")
            return
        
        proyecto = orm_models.Proyecto(
            nombre="Proyecto Default",
            descripcion="Proyecto por defecto para noticias sin asignar",
            estado="activo"
        )
        
        db.add(proyecto)
        db.commit()
        
        print(f"✅ Proyecto default creado (ID: {proyecto.id})")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        
    finally:
        db.close()


def main():
    """Función principal"""
    print("""
    ╔════════════════════════════════════════════╗
    ║  Migración a PostgreSQL                    ║
    ║  Sistema de Noticias con IA                ║
    ╚════════════════════════════════════════════╝
    """)
    
    print("1. Inicializando base de datos...")
    init_db()
    
    print("\n2. Creando proyecto default...")
    crear_proyecto_default()
    
    print("\n3. Migrando noticias de ejemplo...")
    migrar_noticias_ejemplo()
    
    print("\n✅ Proceso completado exitosamente")
    print("\nPróximos pasos:")
    print("  - Ejecutar backend: uvicorn main:app --reload")
    print("  - Verificar en: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
