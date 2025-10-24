"""
Tests para endpoints de noticias
Ejecutar con: pytest tests/test_noticias.py -v
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ==================== FIXTURES ====================

@pytest.fixture
def noticia_ejemplo():
    """Fixture que retorna datos de noticia de ejemplo"""
    return {
        "titulo": "Noticia de prueba",
        "contenido": "Este es el contenido de una noticia de prueba para el testing",
        "seccion_id": 1,
        "autor": "Test User"
    }

@pytest.fixture
def crear_noticia_test(noticia_ejemplo):
    """Fixture que crea una noticia y retorna su ID"""
    response = client.post("/api/noticias/", json=noticia_ejemplo)
    assert response.status_code == 201
    return response.json()["id"]

# ==================== TESTS DE LECTURA ====================

def test_health_check():
    """Verificar que el servidor esté funcionando"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "noticias_en_cache" in data

def test_listar_noticias():
    """Verificar listado de noticias"""
    response = client.get("/api/noticias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ==================== TESTS DE CREACIÓN ====================

def test_crear_noticia_valida(noticia_ejemplo):
    """Crear noticia con datos válidos"""
    response = client.post("/api/noticias/", json=noticia_ejemplo)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == noticia_ejemplo["titulo"]
    assert data["seccion_id"] == noticia_ejemplo["seccion_id"]
    assert "id" in data
    assert "fecha" in data

def test_crear_noticia_titulo_corto():
    """Verificar validación de título muy corto"""
    noticia_invalida = {
        "titulo": "Test",  # Menos de 5 caracteres
        "contenido": "Contenido de prueba con más de 20 caracteres",
        "seccion_id": 1
    }
    response = client.post("/api/noticias/", json=noticia_invalida)
    assert response.status_code == 422  # Unprocessable Entity

def test_crear_noticia_contenido_corto():
    """Verificar validación de contenido muy corto"""
    noticia_invalida = {
        "titulo": "Título válido de prueba",
        "contenido": "Corto",  # Menos de 20 caracteres
        "seccion_id": 1
    }
    response = client.post("/api/noticias/", json=noticia_invalida)
    assert response.status_code == 422



# ==================== TESTS DE ACTUALIZACIÓN ====================

def test_actualizar_noticia(crear_noticia_test):
    """Actualizar noticia existente"""
    noticia_id = crear_noticia_test
    datos_actualizacion = {
        "titulo": "Título actualizado"
    }
    response = client.put(f"/api/noticias/{noticia_id}", json=datos_actualizacion)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Título actualizado"
def test_actualizar_noticia_no_existe():
    """Verificar error al actualizar noticia inexistente"""


# ==================== TESTS DE ELIMINACIÓN ====================

def test_eliminar_noticia(crear_noticia_test):
    """Eliminar noticia existente"""
    noticia_id = crear_noticia_test
    
    response = client.delete(f"/api/noticias/{noticia_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    
    # Verificar que la noticia ya no existe
    response_get = client.get(f"/api/noticias/{noticia_id}")
    assert response_get.status_code == 404

def test_eliminar_noticia_no_existe():
    """Verificar error al eliminar noticia inexistente"""
    response = client.delete("/api/noticias/99999")
    assert response.status_code == 404

# ==================== TESTS DE ESTADÍSTICAS ====================

def test_obtener_estadisticas():
    """Verificar endpoint de estadísticas"""
    response = client.get("/api/noticias/stats/resumen")
    assert response.status_code == 200
    data = response.json()
    assert "total_noticias" in data
    assert "noticias_por_seccion" in data
    assert "noticias_con_ia" in data
    assert isinstance(data["total_noticias"], int)

# ==================== TESTS DE PAGINACIÓN ====================

def test_paginacion_noticias():
    """Verificar paginación de noticias"""
    # Crear datos de prueba
    client.post("/api/noticias/seed")
    
    # Test con límite
    response = client.get("/api/noticias/?limite=2")
    assert response.status_code == 200
    assert len(response.json()) <= 2
    
    # Test con offset
    response = client.get("/api/noticias/?limite=2&offset=1")
    assert response.status_code == 200


def test_filtro_por_seccion():
    """Verificar filtrado por sección"""
    # Crear datos de prueba
    client.post("/api/noticias/seed")
    response = client.get("/api/noticias/?seccion_id=1")
    assert response.status_code == 200
    noticias = response.json()
    for noticia in noticias:
        assert noticia["seccion_id"] == 1

# ==================== TESTS DE DATOS DE EJEMPLO ====================

def test_seed_data():
    """Verificar creación de datos de ejemplo"""
    response = client.post("/api/noticias/seed")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "total_noticias" in data["data"]