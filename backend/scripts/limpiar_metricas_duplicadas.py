#!/usr/bin/env python3
"""
Script para limpiar métricas duplicadas en la base de datos
Mantiene solo la métrica más reciente por noticia
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.database import get_db
from models.orm_models import MetricasValorPeriodistico
import os
from dotenv import load_dotenv

def limpiar_metricas_duplicadas():
    """
    Limpia métricas duplicadas manteniendo solo la más reciente por noticia
    """
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🔍 Buscando métricas duplicadas...")
        
        # Buscar noticias con múltiples métricas
        duplicadas = db.execute(text("""
            SELECT noticia_id, COUNT(*) as cantidad
            FROM metricas_valor_periodistico 
            GROUP BY noticia_id 
            HAVING COUNT(*) > 1
            ORDER BY noticia_id
        """)).fetchall()
        
        if not duplicadas:
            print("✅ No se encontraron métricas duplicadas")
            return
            
        print(f"📊 Encontradas {len(duplicadas)} noticias con métricas duplicadas:")
        for noticia_id, cantidad in duplicadas:
            print(f"  - Noticia {noticia_id}: {cantidad} métricas")
        
        # Limpiar cada noticia
        total_eliminadas = 0
        for noticia_id, cantidad in duplicadas:
            print(f"\n🧹 Limpiando noticia {noticia_id}...")
            
            # Obtener todas las métricas de esta noticia ordenadas por fecha (más reciente primero)
            metricas = db.query(MetricasValorPeriodistico).filter(
                MetricasValorPeriodistico.noticia_id == noticia_id
            ).order_by(MetricasValorPeriodistico.created_at.desc()).all()
            
            if len(metricas) > 1:
                # Mantener solo la primera (más reciente)
                metrica_conservada = metricas[0]
                metricas_a_eliminar = metricas[1:]
                
                print(f"  ✅ Conservando métrica ID {metrica_conservada.id} (más reciente)")
                print(f"     tokens={metrica_conservada.tokens_total}, costo={metrica_conservada.costo_generacion}")
                
                for metrica in metricas_a_eliminar:
                    print(f"  🗑️ Eliminando métrica ID {metrica.id}")
                    print(f"     tokens={metrica.tokens_total}, costo={metrica.costo_generacion}")
                    db.delete(metrica)
                    total_eliminadas += 1
        
        # Confirmar cambios
        print(f"\n💾 Confirmando eliminación de {total_eliminadas} métricas duplicadas...")
        db.commit()
        
        # Verificar resultado
        print("\n🔍 Verificando resultado final...")
        resultado = db.execute(text("""
            SELECT noticia_id, COUNT(*) as cantidad
            FROM metricas_valor_periodistico 
            GROUP BY noticia_id 
            HAVING COUNT(*) > 1
        """)).fetchall()
        
        if not resultado:
            print("✅ ¡Limpieza completada exitosamente! No quedan métricas duplicadas.")
        else:
            print(f"⚠️ Aún quedan {len(resultado)} noticias con duplicados")
            
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🧹 Iniciando limpieza de métricas duplicadas...")
    limpiar_metricas_duplicadas()
    print("🏁 Proceso completado.")