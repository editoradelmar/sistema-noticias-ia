"""
Tests para el Servicio de Generación IA
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.orm import Session

from services.generador_ia import GeneradorIA
from models.orm_models import (
    LLMMaestro,
    PromptMaestro,
    EstiloMaestro,
    Seccion,
    SalidaMaestro,
    Noticia,
    NoticiaSalida
)


class TestGeneradorIA:
    """Tests para la clase GeneradorIA"""
    
    @pytest.fixture
    def mock_db(self):
        """Mock de la sesión de base de datos"""
        return Mock(spec=Session)
    
    @pytest.fixture
    def generador(self, mock_db):
        """Instancia del generador con DB mock"""
        return GeneradorIA(mock_db)
    
    @pytest.fixture
    def mock_llm_anthropic(self):
        """Mock de LLM Anthropic"""
        llm = Mock(spec=LLMMaestro)
        llm.id = 1
        llm.nombre = "Claude Sonnet 4.5"
        llm.proveedor = "Anthropic"
        llm.modelo_id = "claude-sonnet-4-20250514"
        llm.api_key = "sk-ant-test-key"
        llm.tokens_usados_hoy = 0
        return llm
    
    @pytest.fixture
    def mock_prompt(self):
        """Mock de Prompt"""
        prompt = Mock(spec=PromptMaestro)
        prompt.id = 1
        prompt.nombre = "Noticia Estándar"
        prompt.contenido = "Reescribe: {titulo}\n\n{contenido}"
        prompt.variables = ["titulo", "contenido"]
        return prompt
    
    @pytest.fixture
    def mock_estilo(self):
        """Mock de Estilo"""
        estilo = Mock(spec=EstiloMaestro)
        estilo.id = 1
        estilo.nombre = "Profesional"
        estilo.configuracion = {
            "tono": "profesional",
            "longitud": "500 palabras"
        }
        return estilo
    
    @pytest.fixture
    def mock_salida(self):
        """Mock de Salida"""
        salida = Mock(spec=SalidaMaestro)
        salida.id = 1
        salida.nombre = "Web Principal"
        salida.tipo_salida = "digital"
        salida.configuracion = {}
        return salida
    
    @pytest.fixture
    def mock_noticia(self):
        """Mock de Noticia"""
        noticia = Mock(spec=Noticia)
        noticia.id = 1
        noticia.titulo = "Noticia de Prueba"
        noticia.contenido = "Contenido de prueba para testing."
        noticia.autor = "Test Author"
        noticia.fecha = Mock()
        noticia.fecha.strftime = Mock(return_value="17/10/2025")
        
        # Mock de sección
        seccion = Mock(spec=Seccion)
        seccion.nombre = "Tecnología"
        noticia.seccion = seccion
        
        return noticia
    
    # ==================== TESTS ====================
    
    def test_procesar_prompt_con_variables(self, generador, mock_prompt):
        """Test: Procesar prompt reemplazando variables"""
        variables = {
            "titulo": "Título de prueba",
            "contenido": "Contenido de prueba"
        }
        
        resultado = generador.procesar_prompt(mock_prompt, variables)
        
        assert "Título de prueba" in resultado
        assert "Contenido de prueba" in resultado
        assert "{titulo}" not in resultado
        assert "{contenido}" not in resultado
    
    def test_procesar_prompt_variables_faltantes(self, generador, mock_prompt):
        """Test: Error cuando faltan variables"""
        variables = {
            "titulo": "Solo título"
            # Falta 'contenido'
        }
        
        with pytest.raises(ValueError, match="Variables faltantes"):
            generador.procesar_prompt(mock_prompt, variables)
    
    def test_aplicar_estilo(self, generador, mock_estilo):
        """Test: Aplicar estilo a un prompt"""
        prompt_base = "Escribe una noticia sobre tecnología."
        
        resultado = generador.aplicar_estilo(prompt_base, mock_estilo)
        
        assert "profesional" in resultado.lower()
        assert "500 palabras" in resultado.lower()
        assert prompt_base in resultado
    
    def test_get_instrucciones_salida_digital(self, generador, mock_salida):
        """Test: Obtener instrucciones para salida digital"""
        mock_salida.tipo_salida = "digital"
        
        instrucciones = generador._get_instrucciones_salida(mock_salida)
        
        assert "web" in instrucciones.lower()
        assert "seo" in instrucciones.lower()
    
    def test_get_instrucciones_salida_print(self, generador, mock_salida):
        """Test: Obtener instrucciones para salida impresa"""
        mock_salida.tipo_salida = "print"
        
        instrucciones = generador._get_instrucciones_salida(mock_salida)
        
        assert "impreso" in instrucciones.lower() or "print" in instrucciones.lower()
    
    def test_get_max_tokens_por_tipo_salida(self, generador, mock_salida):
        """Test: Obtener max tokens según tipo de salida"""
        # Digital
        mock_salida.tipo_salida = "digital"
        assert generador._get_max_tokens_salida(mock_salida) == 1500
        
        # Print
        mock_salida.tipo_salida = "print"
        assert generador._get_max_tokens_salida(mock_salida) == 2000
        
        # Social
        mock_salida.tipo_salida = "social"
        assert generador._get_max_tokens_salida(mock_salida) == 500
    
    @patch('services.generador_ia.Anthropic')
    def test_generar_contenido_anthropic(
        self, 
        mock_anthropic_class,
        generador, 
        mock_llm_anthropic,
        mock_db
    ):
        """Test: Generar contenido con Anthropic"""
        # Configurar mock de respuesta
        mock_response = Mock()
        mock_response.content = [Mock(text="Contenido generado por IA")]
        mock_response.usage = Mock(
            input_tokens=100,
            output_tokens=200
        )
        
        mock_client = Mock()
        mock_client.messages.create = Mock(return_value=mock_response)
        mock_anthropic_class.return_value = mock_client
        
        # Ejecutar
        resultado = generador.generar_contenido(
            llm=mock_llm_anthropic,
            prompt_contenido="Test prompt",
            max_tokens=1000
        )
        
        # Verificar
        assert resultado["contenido"] == "Contenido generado por IA"
        assert resultado["tokens_usados"] == 300
        assert resultado["tiempo_ms"] > 0
    
    def test_cache_cliente_llm(self, generador, mock_llm_anthropic):
        """Test: Cliente LLM se cachea correctamente"""
        with patch('services.generador_ia.Anthropic') as mock_anthropic:
            # Primera llamada
            cliente1 = generador._get_cliente_llm(mock_llm_anthropic)
            
            # Segunda llamada (debe usar cache)
            cliente2 = generador._get_cliente_llm(mock_llm_anthropic)
            
            # Verificar que solo se creó una instancia
            assert mock_anthropic.call_count == 1
            assert cliente1 is cliente2
    
    def test_proveedor_no_soportado(self, generador, mock_llm_anthropic):
        """Test: Error con proveedor no soportado"""
        mock_llm_anthropic.proveedor = "ProveedorInexistente"
        
        with pytest.raises(ValueError, match="Proveedor no soportado"):
            generador._get_cliente_llm(mock_llm_anthropic)


class TestIntegracionGeneradorIA:
    """Tests de integración para GeneradorIA"""
    
    @pytest.fixture
    def generador_integracion(self, mock_db):
        """Generador para tests de integración"""
        return GeneradorIA(mock_db)
    
    def test_flujo_completo_generacion(
        self,
        generador_integracion,
        mock_noticia,
        mock_salida,
        mock_llm_anthropic,
        mock_prompt,
        mock_estilo
    ):
        """Test: Flujo completo de generación de salida"""
        # Este test requeriría una configuración más compleja
        # Por ahora verificamos que los métodos existen
        assert hasattr(generador_integracion, 'generar_para_salida')
        assert hasattr(generador_integracion, 'generar_multiples_salidas')
        assert hasattr(generador_integracion, 'procesar_prompt')
        assert hasattr(generador_integracion, 'aplicar_estilo')


# ==================== FIXTURES GLOBALES ====================

@pytest.fixture(scope="session")
def test_config():
    """Configuración para tests"""
    return {
        "test_api_key": "sk-test-key-for-testing",
        "test_model": "claude-sonnet-4-test"
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
