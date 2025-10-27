"""
Script para probar la nueva arquitectura sin campo 'autor'
Verifica que usuario_id funcione como fuente de verdad
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import SessionLocal
from models import orm_models
import json

def test_model_properties():
    """Probar las propiedades del modelo actualizado"""
    db = SessionLocal()
    try:
        print("\n🧪 PRUEBA 1: Propiedades del modelo")
        print("=" * 40)
        
        # Obtener una noticia con usuario
        noticia = db.query(orm_models.Noticia).join(orm_models.Usuario).first()
        
        if not noticia:
            print("❌ No hay noticias con usuarios para probar")
            return False
        
        print(f"📰 Noticia ID {noticia.id}: '{noticia.titulo[:50]}...'")
        print(f"   👤 Usuario ID: {noticia.usuario_id}")
        print(f"   👤 autor_nombre: {noticia.autor_nombre}")
        print(f"   👤 autor_id (alias): {noticia.autor_id}")
        
        # Verificar que autor_nombre viene del usuario relacionado
        if noticia.usuario_creador:
            expected_autor = noticia.usuario_creador.username
            actual_autor = noticia.autor_nombre
            
            if expected_autor == actual_autor:
                print(f"   ✅ autor_nombre correcto: '{actual_autor}'")
            else:
                print(f"   ❌ autor_nombre incorrecto: esperado '{expected_autor}', got '{actual_autor}'")
                return False
        
        print("✅ Propiedades del modelo funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error probando modelo: {e}")
        return False
    finally:
        db.close()

def test_to_dict_method():
    """Probar el método to_dict actualizado"""
    db = SessionLocal()
    try:
        print("\n🧪 PRUEBA 2: Método to_dict()")
        print("=" * 40)
        
        noticia = db.query(orm_models.Noticia).join(orm_models.Usuario).first()
        
        if not noticia:
            print("❌ No hay noticias para probar")
            return False
        
        noticia_dict = noticia.to_dict()
        
        # Verificar campos esperados
        expected_fields = ['id', 'titulo', 'contenido', 'seccion_id', 'autor_nombre', 
                          'usuario_id', 'fecha', 'proyecto_id', 'llm_id', 'estado']
        
        missing_fields = [f for f in expected_fields if f not in noticia_dict]
        unexpected_fields = [f for f in noticia_dict.keys() if f not in expected_fields + ['resumen_ia', 'sentiment_score', 'keywords']]
        
        if missing_fields:
            print(f"❌ Campos faltantes en to_dict: {missing_fields}")
            return False
        
        # Verificar que NO tiene campo 'autor'
        if 'autor' in noticia_dict:
            print("❌ ERROR: to_dict() todavía incluye campo 'autor'")
            return False
        
        print("✅ Campos presentes:", list(noticia_dict.keys()))
        print(f"✅ autor_nombre: '{noticia_dict['autor_nombre']}'")
        print(f"✅ usuario_id: {noticia_dict['usuario_id']}")
        print("✅ Campo 'autor' eliminado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando to_dict: {e}")
        return False
    finally:
        db.close()

def test_api_response_structure():
    """Simular la estructura de respuesta de la API"""
    db = SessionLocal()
    try:
        print("\n🧪 PRUEBA 3: Estructura de respuesta API")
        print("=" * 40)
        
        # Obtener noticias como lo haría la API
        noticias = db.query(orm_models.Noticia).join(orm_models.Usuario).limit(3).all()
        
        if not noticias:
            print("❌ No hay noticias para probar")
            return False
        
        # Simular respuesta de la API
        api_response = []
        for noticia in noticias:
            noticia_data = noticia.to_dict()
            api_response.append(noticia_data)
        
        print(f"✅ {len(api_response)} noticias en respuesta simulada")
        
        # Verificar estructura de la primera noticia
        first_noticia = api_response[0]
        print("\n📊 Estructura de noticia:")
        for key, value in first_noticia.items():
            if isinstance(value, str) and len(value) > 50:
                value = value[:50] + "..."
            print(f"   {key}: {value}")
        
        # Verificar que funciona el filtrado por usuario_id
        usuario_test = noticias[0].usuario_id
        noticias_filtered = [n for n in api_response if n['usuario_id'] == usuario_test]
        
        print(f"\n🔍 Filtrado por usuario_id={usuario_test}:")
        print(f"   Noticias encontradas: {len(noticias_filtered)}")
        
        if noticias_filtered:
            print(f"   ✅ Filtro funciona: {noticias_filtered[0]['autor_nombre']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando API response: {e}")
        return False
    finally:
        db.close()

def test_database_constraints():
    """Probar las restricciones de base de datos"""
    db = SessionLocal()
    try:
        print("\n🧪 PRUEBA 4: Restricciones de base de datos")
        print("=" * 40)
        
        # Verificar que todas las noticias tienen usuario_id
        noticias_sin_usuario = db.query(orm_models.Noticia).filter(
            orm_models.Noticia.usuario_id.is_(None)
        ).count()
        
        print(f"Noticias sin usuario_id: {noticias_sin_usuario}")
        
        if noticias_sin_usuario > 0:
            print(f"❌ {noticias_sin_usuario} noticias sin usuario_id válido")
            return False
        
        # Verificar integridad referencial
        total_noticias = db.query(orm_models.Noticia).count()
        noticias_con_usuario_valido = db.query(orm_models.Noticia).join(orm_models.Usuario).count()
        
        print(f"Total de noticias: {total_noticias}")
        print(f"Noticias con usuario válido: {noticias_con_usuario_valido}")
        
        if total_noticias != noticias_con_usuario_valido:
            print(f"❌ {total_noticias - noticias_con_usuario_valido} noticias con usuario_id inválido")
            return False
        
        print("✅ Todas las noticias tienen usuario_id válido")
        print("✅ Integridad referencial correcta")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando restricciones: {e}")
        return False
    finally:
        db.close()

def test_user_statistics():
    """Mostrar estadísticas por usuario"""
    db = SessionLocal()
    try:
        print("\n📊 ESTADÍSTICAS POR USUARIO")
        print("=" * 40)
        
        # Estadísticas por usuario
        from sqlalchemy import func
        
        stats = db.query(
            orm_models.Usuario.username,
            func.count(orm_models.Noticia.id).label('total_noticias')
        ).join(
            orm_models.Noticia, orm_models.Usuario.id == orm_models.Noticia.usuario_id
        ).group_by(
            orm_models.Usuario.username
        ).order_by(
            func.count(orm_models.Noticia.id).desc()
        ).all()
        
        for username, count in stats:
            print(f"   👤 {username}: {count} noticias")
        
        return True
        
    except Exception as e:
        print(f"❌ Error calculando estadísticas: {e}")
        return False
    finally:
        db.close()

def main():
    print("🚀 PRUEBAS DE ARQUITECTURA SIN CAMPO 'AUTOR'")
    print("=" * 50)
    
    tests = [
        test_model_properties,
        test_to_dict_method,
        test_api_response_structure,
        test_database_constraints,
        test_user_statistics
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Línea en blanco entre pruebas
        except Exception as e:
            print(f"❌ Error en prueba {test.__name__}: {e}")
    
    print("=" * 50)
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ La arquitectura usuario_id está funcionando correctamente")
        print("✅ Lista para eliminar la columna 'autor' de la base de datos")
    else:
        print("❌ Algunas pruebas fallaron")
        print("🔧 Revisa los errores antes de proceder con la migración")
    
    return passed == total

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")