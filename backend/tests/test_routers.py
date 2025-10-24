"""
Tests para los Routers de Maestros (Fase 6)
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app


client = TestClient(app)


class TestLLMMaestroRouter:
    """Tests para el router de LLM Maestro"""
    
    def test_listar_llms_sin_auth(self):
        """Test: Listar LLMs sin autenticación debe fallar"""
        response = client.get("/api/llm-maestro/")
        assert response.status_code == 401
    
    @pytest.mark.skip("Requiere configurar auth mock")
    def test_listar_llms_con_auth(self):
        """Test: Listar LLMs con autenticación"""
        headers = {"Authorization": "Bearer test-token"}
        response = client.get("/api/llm-maestro/", headers=headers)
        assert response.status_code in [200, 401]  # Depende del token
    
    @pytest.mark.skip("Requiere configurar auth mock")
    def test_crear_llm_solo_admin(self):
        """Test: Solo admin puede crear LLMs"""
        data = {
            "nombre": "Test LLM",
            "proveedor": "Anthropic",
            "modelo_id": "claude-test",
            "api_key": "sk-test"
        }
        
        # Sin auth
        response = client.post("/api/llm-maestro/", json=data)
        assert response.status_code == 401
        
        # Con auth de editor (no admin)
        # Esto requeriría mock del sistema de auth


class TestPromptsRouter:
    """Tests para el router de Prompts"""
    
    def test_listar_prompts_sin_auth(self):
        """Test: Listar prompts sin autenticación"""
        response = client.get("/api/prompts/")
        assert response.status_code == 401
    
    def test_endpoint_activos_existe(self):
        """Test: Endpoint de prompts activos existe"""
        response = client.get("/api/prompts/activos")
        # Puede ser 401 (sin auth) o 200 (si endpoint público)
        assert response.status_code in [200, 401]


class TestEstilosRouter:
    """Tests para el router de Estilos"""
    
    def test_listar_estilos_sin_auth(self):
        """Test: Listar estilos sin autenticación"""
        response = client.get("/api/estilos/")
        assert response.status_code == 401


class TestSeccionesRouter:
    """Tests para el router de Secciones"""
    
    def test_listar_secciones_sin_auth(self):
        """Test: Listar secciones sin autenticación"""
        response = client.get("/api/secciones/")
        assert response.status_code == 401


class TestSalidasRouter:
    """Tests para el router de Salidas"""
    
    def test_listar_salidas_sin_auth(self):
        """Test: Listar salidas sin autenticación"""
        response = client.get("/api/salidas/")
        assert response.status_code == 401


class TestGeneracionRouter:
    """Tests para el router de Generación"""
    
    def test_generar_salidas_sin_auth(self):
        """Test: Generar salidas requiere autenticación"""
        data = {
            "noticia_id": 1,
            "salidas_ids": [1, 2],
            "llm_id": 1
        }
        response = client.post("/api/generar/salidas", json=data)
        assert response.status_code == 401
    
    def test_obtener_salidas_noticia_sin_auth(self):
        """Test: Obtener salidas requiere autenticación"""
        response = client.get("/api/generar/noticia/1/salidas")
        assert response.status_code == 401


class TestHealthCheck:
    """Tests para endpoints de health check"""
    
    def test_root_endpoint(self):
        """Test: Endpoint raíz funciona"""
        response = client.get("/")
        assert response.status_code == 200
        assert "mensaje" in response.json()
    
    def test_health_endpoint(self):
        """Test: Health check funciona"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
