"""
Servicio de Generación IA Multi-LLM
Gestiona la generación de contenido con diferentes proveedores (Claude, GPT, Gemini)
"""
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from anthropic import Anthropic
import time
import re
from datetime import datetime

# Importaciones opcionales de otros proveedores
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

from models.orm_models import (
    LLMMaestro,
    PromptMaestro,
    EstiloMaestro,
    Seccion,
    SalidaMaestro,
    Noticia,
    NoticiaSalida,
    MetricasValorPeriodistico
)
from models.schemas import MetricasValorResumen
from config import settings
from services import runtime_settings


class GeneradorIA:
    """
    Clase principal para generar contenido con IA
    Soporta múltiples proveedores: Anthropic (Claude), OpenAI (GPT), Google (Gemini)
    """
    
    def __init__(self, db: Session):
        self.db = db
        self._clientes = {}  # Cache de clientes API
        # Máximo de caracteres permitidos en el prompt final (protección contra prompts excesivamente largos)
        # Tomado desde la configuración central si está disponible
        try:
            self.max_prompt_chars = int(getattr(settings, 'MAX_PROMPT_CHARS', 50000))
        except Exception:
            self.max_prompt_chars = 50000
    
    # ==================== CLIENTE LLM ====================
    
    def _get_cliente_llm(self, llm: LLMMaestro) -> Any:
        """
        Obtiene o crea un cliente para el proveedor LLM
        
        Args:
            llm: Instancia de LLMMaestro
            
        Returns:
            Cliente API configurado
        """
        # Usar cache si ya existe
        if llm.id in self._clientes:
            return self._clientes[llm.id]
        
        # Crear cliente según proveedor
        if llm.proveedor == "Anthropic":
            if not llm.api_key or llm.api_key == "":
                print(f"⚠️  API Key no configurada para {llm.nombre}. Usando modo simulado.")
                return None  # Modo simulado
            cliente = Anthropic(api_key=llm.api_key)
            
        elif llm.proveedor == "OpenAI":
            if not OPENAI_AVAILABLE:
                raise ImportError(
                    "OpenAI no está instalado. Instala con: pip install openai --break-system-packages"
                )
            openai.api_key = llm.api_key
            cliente = openai
            
        elif llm.proveedor == "Google":
            if not GOOGLE_AVAILABLE:
                raise ImportError(
                    "Google Generative AI no está instalado. Instala con: pip install google-generativeai --break-system-packages"
                )
            genai.configure(api_key=llm.api_key)
            cliente = genai
            
        else:
            raise ValueError(f"Proveedor no soportado: {llm.proveedor}")
        
        # Guardar en cache
        self._clientes[llm.id] = cliente
        return cliente
    
    # ==================== GENERACIÓN DE CONTENIDO ====================
    
    def generar_contenido(
        self,
        llm: LLMMaestro,
        prompt_contenido,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Genera contenido usando el LLM especificado
        
        Args:
            llm: Modelo LLM a usar
            prompt_contenido: Contenido del prompt
            max_tokens: Máximo de tokens a generar
            temperature: Temperatura para la generación (0.0-1.0)
            
        Returns:
            Dict con 'contenido', 'tokens_usados', 'tiempo_ms'
        """
        inicio = time.time()
        cliente = self._get_cliente_llm(llm)
        
        try:
            print("[DEBUG] Prompt enviado al LLM:\n", prompt_contenido)
            
            # Modo simulado si no hay cliente API
            if cliente is None:
                print(f"🤖 Modo simulado activado para {llm.nombre}")
                tiempo_ms = int((time.time() - inicio) * 1000)
                
                # Extraer información del prompt para simular mejor
                titulo_original = "Título de la noticia"
                contenido_original = "Contenido original de la noticia"
                
                # Intentar extraer datos reales del prompt si es posible
                if isinstance(prompt_contenido, str):
                    # Buscar patrones en el prompt
                    titulo_match = re.search(r'TÍTULO:\s*(.+)', prompt_contenido)
                    if titulo_match:
                        titulo_original = titulo_match.group(1).strip()
                    
                    contenido_match = re.search(r'CONTENIDO ORIGINAL:\s*(.+?)(?:\nSECCIÓN:|$)', prompt_contenido, re.DOTALL)
                    if contenido_match:
                        contenido_original = contenido_match.group(1).strip()
                
                # Si no pudo extraer del prompt, usar contenido genérico pero útil
                if contenido_original == "Contenido original de la noticia":
                    contenido_original = "Este es el contenido procesado por IA en modo simulado. El contenido original ha sido optimizado según el prompt y estilo configurados para esta salida."
                
                # Generar título simulado DIFERENTE al original
                prefijos_simulados = [
                    "IA optimiza:", "Nuevo enfoque:", "Transformado:", "Actualización:", 
                    "Versión IA:", "Mejorado:", "Adaptado:", "Rediseñado:"
                ]
                import random
                titulo_simulado = f"{random.choice(prefijos_simulados)} {titulo_original[:150]}"
                
                # Generar respuesta simulada con formato estructurado
                respuesta_simulada = f"""TÍTULO: {titulo_simulado}

CONTENIDO:
{contenido_original}

---
*✨ Contenido optimizado con IA ({llm.nombre}) - MODO SIMULADO*
*🔧 Configura API key para usar IA real*
*📅 Procesado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
                
                # Parsear la respuesta simulada para extraer título y contenido
                resultado_parseado = self._parsear_respuesta_estructurada(respuesta_simulada)
                
                return {
                    "contenido": resultado_parseado["contenido"],
                    "titulo": resultado_parseado["titulo"],
                    "tokens_usados": 150,  # Simulado
                    "tiempo_ms": tiempo_ms
                }
            
            # prompt_contenido puede ser un string (caso legacy) o una lista de mensajes (nuevo)
            messages = prompt_contenido if isinstance(prompt_contenido, list) else [{"role": "user", "content": prompt_contenido}]
            if llm.proveedor == "Anthropic":
                respuesta = cliente.messages.create(
                    model=llm.modelo_id,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages
                )
                contenido = respuesta.content[0].text
                tokens_usados = respuesta.usage.input_tokens + respuesta.usage.output_tokens
            elif llm.proveedor == "OpenAI":
                if not OPENAI_AVAILABLE:
                    raise ImportError("OpenAI no está disponible")
                respuesta = cliente.ChatCompletion.create(
                    model=llm.modelo_id,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                contenido = respuesta.choices[0].message.content
                tokens_usados = respuesta.usage.total_tokens
            elif llm.proveedor == "Google":
                if not GOOGLE_AVAILABLE:
                    raise ImportError("Google Gemini no está disponible")
                
                # Usar exactamente el modelo configurado en BD
                print(f"[DEBUG] Usando modelo Gemini configurado: {llm.modelo_id}")
                
                model = cliente.GenerativeModel(llm.modelo_id)
                
                # Simplificar prompt para Gemini (aprendido del código de referencia)
                if isinstance(prompt_contenido, list):
                    # Convertir mensajes a string simple para Gemini
                    prompt_str = ""
                    for msg in prompt_contenido:
                        if msg.get('role') == 'system':
                            prompt_str += f"Instrucciones del sistema: {msg['content']}\n\n"
                        elif msg.get('role') == 'user':
                            prompt_str += f"Usuario: {msg['content']}\n"
                        elif msg.get('role') == 'assistant':
                            prompt_str += f"Asistente: {msg['content']}\n"
                        else:
                            prompt_str += f"{msg['content']}\n"
                else:
                    prompt_str = str(prompt_contenido)
                
                print(f"[DEBUG] Prompt para Gemini (primeros 300 chars):\n{prompt_str[:300]}...")
                print(f"[DEBUG] API Key válida: {bool(llm.api_key and len(llm.api_key) > 10)}")
                
                try:
                    print(f"[DEBUG] Iniciando llamada a Gemini...")
                    respuesta = model.generate_content(prompt_str)
                    print(f"[DEBUG] Respuesta de Gemini recibida")
                    contenido = respuesta.text
                    tokens_usados = len(prompt_str.split()) + len(contenido.split())
                    print(f"[DEBUG] Gemini respuesta exitosa. Tokens estimados: {tokens_usados}")
                    print(f"[DEBUG] Contenido generado (primeros 200 chars): {contenido[:200]}...")
                except Exception as e:
                    print(f"[ERROR] Error en Gemini API: {str(e)}")
                    print(f"[DEBUG] Modelo usado: {llm.modelo_id}")
                    print(f"[DEBUG] API Key (últimos 8 chars): ...{llm.api_key[-8:] if llm.api_key else 'None'}")
                    print(f"[DEBUG] Tipo de error: {type(e).__name__}")
                    
                    # Activar modo simulación para debug
                    print(f"[DEBUG] Activando modo simulación debido a error de Gemini")
                    contenido = f"[SIMULADO - Error Gemini] Contenido generado optimizado para salida. Error: {str(e)[:100]}"
                    tokens_usados = 50
            else:
                raise ValueError(f"Proveedor no soportado: {llm.proveedor}")
            tiempo_ms = int((time.time() - inicio) * 1000)
            llm.tokens_usados_hoy += tokens_usados
            self.db.commit()
            print("[DEBUG] Contenido generado por el LLM:\n", contenido)
            if not contenido or len(contenido.strip()) < 10:
                raise Exception("El LLM devolvió un contenido vacío o muy corto. Revisa el prompt y la configuración del modelo.")
            
            # Parsear la respuesta estructurada para extraer título y contenido
            resultado_parseado = self._parsear_respuesta_estructurada(contenido)
            
            return {
                "contenido": resultado_parseado["contenido"],
                "titulo": resultado_parseado["titulo"],
                "tokens_usados": tokens_usados,
                "tiempo_ms": tiempo_ms
            }
        except Exception as e:
            error_str = str(e)
            print(f"[ERROR] Error al generar contenido con {llm.nombre}: {error_str}")
            
            # Si es error de autenticación o API key, caer a modo simulado
            if any(keyword in error_str.lower() for keyword in ['authentication', 'api_key', 'invalid', '401', 'unauthorized']):
                print(f"🔄 Error de autenticación detectado. Activando modo simulado para {llm.nombre}")
                tiempo_ms = int((time.time() - inicio) * 1000)
                
                # Intentar extraer datos del prompt para simular mejor
                titulo_extraido = "Título de la noticia"
                contenido_original = "Contenido original de la noticia"
                
                if isinstance(prompt_contenido, str):
                    titulo_match = re.search(r'TÍTULO:\s*(.+)', prompt_contenido)
                    if titulo_match:
                        titulo_extraido = titulo_match.group(1).strip()
                    
                    contenido_match = re.search(r'CONTENIDO ORIGINAL:\s*(.+?)(?:\nSECCIÓN:|$)', prompt_contenido, re.DOTALL)
                    if contenido_match:
                        contenido_original = contenido_match.group(1).strip()
                
                if contenido_original == "Contenido original de la noticia":
                    contenido_original = "Este es el contenido procesado por IA en modo simulado. El contenido original ha sido optimizado según el prompt y estilo configurados para esta salida."
                
                # Generar título simulado DIFERENTE al original para modo error
                titulo_error = f"Error API - {titulo_extraido[:150]}"
                
                # Generar respuesta simulada con formato estructurado para error
                respuesta_error = f"""TÍTULO: {titulo_error}

CONTENIDO:
{contenido_original}

---
*✨ Contenido optimizado con IA ({llm.nombre}) - MODO SIMULADO*
*🔧 Error de API detectado - Configura API key válida para usar IA real*
*📅 Procesado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
                
                # Parsear la respuesta de error
                resultado_error = self._parsear_respuesta_estructurada(respuesta_error)
                
                return {
                    "contenido": resultado_error["contenido"],
                    "titulo": resultado_error["titulo"],
                    "tokens_usados": 150,  # Simulado
                    "tiempo_ms": tiempo_ms
                }
            else:
                # Para otros errores, fallar completamente
                raise Exception(f"Error al generar contenido con {llm.nombre}: {error_str}")
    
    # ==================== PROCESAMIENTO DE PROMPTS ====================
    
    def procesar_prompt(
        self,
        prompt: PromptMaestro,
        variables: Dict[str, str]
    ) -> str:
        """
        Procesa un prompt reemplazando las variables
        
        Args:
            prompt: PromptMaestro con el template
            variables: Dict con valores para reemplazar {variable}
            
        Returns:
            Prompt procesado con variables reemplazadas
        """
        # Concatenar el contenido de TODOS los PromptItem ordenados por 'orden'
        contenido = ""
        if getattr(prompt, 'items', None) and len(prompt.items) > 0:
            # Ordenar por 'orden' si existe, si no por id
            try:
                items_ordenados = sorted(prompt.items, key=lambda it: getattr(it, 'orden', 0) or 0)
            except Exception:
                items_ordenados = list(prompt.items)

            partes = []
            for it in items_ordenados:
                if it and getattr(it, 'contenido', None):
                    partes.append(it.contenido.strip())

            contenido = "\n\n---\n\n".join(partes).strip()
            print(f"[DEBUG] Contenido del prompt '{prompt.nombre}': concatenados {len(partes)} items -> {len(contenido)} caracteres")
        else:
            print(f"[DEBUG] No se encontraron items para el prompt '{prompt.nombre}'")
        
        # Si no hay contenido suficiente, usar prompt por defecto
        if not contenido or len(contenido.strip()) < 10:
            print(f"[WARNING] Prompt '{prompt.nombre}' vacío o muy corto. Usando prompt por defecto.")
            contenido = f"""Eres un redactor profesional de noticias. 

Tu tarea es reescribir la siguiente noticia optimizándola para {prompt.nombre}.

TÍTULO: {{titulo}}
CONTENIDO ORIGINAL: {{contenido}}
SECCIÓN: {{seccion}}
TIPO DE SALIDA: {{tipo_salida}}

Instrucciones:
- Mantén la información factual
- Adapta el tono y formato para {{nombre_salida}}
- Asegúrate de que sea claro y atractivo
- Respeta la longitud apropiada para {{tipo_salida}}

Genera el contenido optimizado:"""
        
        # Reemplazar cada variable
        for nombre_var, valor in variables.items():
            placeholder = f"{{{nombre_var}}}"
            contenido = contenido.replace(placeholder, str(valor))
        
        # Verificar que no queden variables sin reemplazar
        variables_faltantes = re.findall(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}', contenido)
        if variables_faltantes:
            raise ValueError(
                f"Variables faltantes en el prompt: {', '.join(variables_faltantes)}"
            )
        
        # Validación final: asegurar que el prompt tenga contenido mínimo
        if not contenido or len(contenido.strip()) < 20:
            raise ValueError(f"El prompt procesado es demasiado corto o está vacío. Verifica la configuración del prompt '{prompt.nombre}'")

        # Protección: truncar prompt si excede el tamaño máximo permitido
        current_limit = runtime_settings.get_max_prompt_chars() or getattr(self, 'max_prompt_chars', 50000)
        if len(contenido) > current_limit:
            print(f"[WARNING] Prompt procesado demasiado largo ({len(contenido)} chars). Truncando a {current_limit} chars.")
            contenido = contenido[:current_limit]
        
        return contenido
    
    # ==================== APLICACIÓN DE ESTILOS ====================
    
    def aplicar_estilo(
        self,
        prompt_base: str,
        estilo: EstiloMaestro
    ) -> str:
        """
        Aplica directivas de estilo al prompt
        
        Args:
            prompt_base: Prompt base
            estilo: EstiloMaestro con configuración de estilo
            
        Returns:
            Prompt con directivas de estilo añadidas
        """
        directivas_estilo = []
        
        # Extraer configuración del estilo
        config = estilo.configuracion or {}
        
        # Tono
        if "tono" in config:
            directivas_estilo.append(f"Tono: {config['tono']}")
        
        # Longitud
        if "longitud" in config:
            directivas_estilo.append(f"Longitud aproximada: {config['longitud']} palabras")
        
        # Formato
        if "formato" in config:
            directivas_estilo.append(f"Formato: {config['formato']}")
        
        # Estructura
        if "estructura" in config:
            directivas_estilo.append(f"Estructura: {config['estructura']}")
        
        # Otras directivas
        for key, value in config.items():
            if key not in ["tono", "longitud", "formato", "estructura"]:
                directivas_estilo.append(f"{key.title()}: {value}")
        
        # Construir prompt final
        if directivas_estilo:
            estilo_texto = "\n".join([f"- {d}" for d in directivas_estilo])
            prompt_final = f"{prompt_base}\n\n**ESTILO Y DIRECTIVAS:**\n{estilo_texto}"
        else:
            prompt_final = prompt_base

        # Concatenar todos los EstiloItem si existen (ejemplos, reglas, fragmentos)
        estilo_items_text = ""
        if getattr(estilo, 'items', None) and len(estilo.items) > 0:
            try:
                estilo_items_ordenados = sorted(estilo.items, key=lambda it: getattr(it, 'orden', 0) or 0)
            except Exception:
                estilo_items_ordenados = list(estilo.items)

            partes_items = [it.contenido.strip() for it in estilo_items_ordenados if it and getattr(it, 'contenido', None)]
            if partes_items:
                estilo_items_text = "\n\n".join(partes_items)
                # Anexar los ejemplos/reglas al prompt final
                prompt_final = f"{prompt_final}\n\n**EJEMPLOS Y REGLAS DE ESTILO:**\n{estilo_items_text}"
                print(f"[DEBUG] Se anexaron {len(partes_items)} estilo.items al prompt (chars añadidos: {len(estilo_items_text)})")

        # Protección: truncar prompt si excede el tamaño máximo permitido
        current_limit = runtime_settings.get_max_prompt_chars() or getattr(self, 'max_prompt_chars', 50000)
        if len(prompt_final) > current_limit:
            print(f"[WARNING] Prompt con estilo demasiado largo ({len(prompt_final)} chars). Truncando a {current_limit} chars.")
            prompt_final = prompt_final[:current_limit]
        
        return prompt_final

    # ==================== CONFIGURACIONES Y MERGE ====================

    def merge_configs(self, estilo_config: Optional[Dict[str, Any]], salida_config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge runtime entre configuraciones de Estilo y Salida.

        Reglas soportadas (modo en salida_config['modo_fusion']):
        - 'replace': usar solo salida_config (sin 'modo_fusion').
        - 'merge'  : shallow merge por defecto (salida sobreescribe estilo).
        - 'combine': deep-merge inteligente que preserva/combina estructuras y
          devuelve metadata con resolución de conflictos.

        Nota: La clave 'max_caracteres' es exclusivamente de Salida: si no está en
        salida_config, no se hereda desde estilo.
        """
        estilo_config = estilo_config or {}
        salida_config = salida_config or {}

        modo = salida_config.get('modo_fusion', 'merge')

        # Helper: deep merge for 'combine'
        def _deep_merge(a: Any, b: Any, path: str = '') -> Tuple[Any, Dict[str, Any]]:
            """Merge recursively dicts/lists. b overrides a for scalars. Returns (merged, metadata)"""
            metadata = {"overrides": {}, "source_map": {}}
            if isinstance(a, dict) and isinstance(b, dict):
                result = dict(a)
                for key in b:
                    new_path = f"{path}.{key}" if path else key
                    if key in a:
                        merged_val, meta = _deep_merge(a[key], b[key], new_path)
                        result[key] = merged_val
                        # merge metadata
                        if meta.get('overrides'):
                            metadata['overrides'].update(meta['overrides'])
                        if meta.get('source_map'):
                            metadata['source_map'].update(meta['source_map'])
                    else:
                        result[key] = b[key]
                        metadata['source_map'][new_path] = 'salida'
                return result, metadata
            # Lists: concatenate and deduplicate simple values
            if isinstance(a, list) and isinstance(b, list):
                try:
                    merged_list = a + [item for item in b if item not in a]
                except Exception:
                    merged_list = a + b
                # mark list source as combined
                metadata['source_map'][path or '/'] = 'combined_list'
                return merged_list, metadata
            # Scalars or differing types: prefer salida (b) but record override
            if a is not None and b is not None and a != b:
                metadata['overrides'][path or '/'] = {'estilo': a, 'salida': b}
                metadata['source_map'][path or '/'] = 'salida'
                return b, metadata
            # Fallback: prefer b if set, otherwise a
            chosen = b if b is not None else a
            metadata['source_map'][path or '/'] = 'salida' if b is not None else 'estilo'
            return chosen, metadata

        if modo == 'replace':
            # usar solo la configuración de salida (sin modo_fusion)
            return {k: v for k, v in salida_config.items() if k != 'modo_fusion'}

        if modo == 'merge':
            merged = dict(estilo_config)
            for k, v in salida_config.items():
                if k == 'modo_fusion':
                    continue
                merged[k] = v
            # Asegurar que max_caracteres sólo venga de la Salida
            if 'max_caracteres' not in salida_config and 'max_caracteres' in merged:
                merged.pop('max_caracteres', None)
            return merged

        if modo == 'combine':
            # Deep merge con metadata
            merged, metadata = _deep_merge(estilo_config, salida_config)
            # Asegurar que max_caracteres sólo venga de la Salida
            if 'max_caracteres' not in salida_config and 'max_caracteres' in merged:
                merged.pop('max_caracteres', None)
                # si fue removida, limpiar metadata correspondiente
                metadata['source_map'].pop('max_caracteres', None)
                metadata['overrides'].pop('max_caracteres', None)
            # Devolver una estructura especial para quien pida metadata
            return {'_merged': merged, '_metadata': metadata}

        # Si modo desconocido, fallback a merge
        merged = dict(estilo_config)
        for k, v in salida_config.items():
            if k == 'modo_fusion':
                continue
            merged[k] = v
        if 'max_caracteres' not in salida_config and 'max_caracteres' in merged:
            merged.pop('max_caracteres', None)
        return merged

    def _remove_emojis(self, text: str) -> str:
        """Eliminar emojis básicos del texto usando regex simple."""
        try:
            # Rango unicode básico para emojis
            emoji_pattern = re.compile(
                "[\U0001F600-\U0001F64F"  # emoticons
                "\U0001F300-\U0001F5FF"  # symbols & pictographs
                "\U0001F680-\U0001F6FF"  # transport & map symbols
                "\U0001F1E0-\U0001F1FF]", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)
        except Exception:
            # Fallback: eliminar caracteres no ASCII extendidos
            return re.sub(r'[\u2600-\u27bf]|[\U00010000-\U0010ffff]', '', text)

    def _apply_max_caracteres(self, text: str, max_caracteres: int, estrategia: str = 'smart') -> str:
        """Aplica truncado según max_caracteres y estrategia ('smart' intenta cortar en punto)."""
        if not max_caracteres or max_caracteres <= 0:
            return text
        if len(text) <= max_caracteres:
            return text
        if estrategia == 'hard':
            return text[:max_caracteres]
        # Estrategia smart: intentar cortar en el último punto antes del límite
        corte = text.rfind('.', 0, max_caracteres)
        if corte != -1 and corte > int(max_caracteres * 0.5):
            return text[:corte+1]
        # Si no hay punto adecuado, truncar al último espacio
        corte_ws = text.rfind(' ', 0, max_caracteres)
        if corte_ws != -1 and corte_ws > int(max_caracteres * 0.3):
            return text[:corte_ws]
        # Fallback duro
        return text[:max_caracteres]
    
    # ==================== GENERACIÓN PARA SALIDA ====================
    
    def generar_para_salida(
        self,
        noticia: Noticia,
        salida: SalidaMaestro,
        llm: LLMMaestro,
        prompt: Optional[PromptMaestro] = None,
        estilo: Optional[EstiloMaestro] = None,
        regenerar: bool = False
    ) -> NoticiaSalida:
        """
        Genera contenido optimizado para una salida específica
        
        Args:
            noticia: Noticia fuente
            salida: Canal de salida (web, print, social, etc.)
            llm: Modelo LLM a usar
            prompt: Prompt a usar (usa el de la sección si no se especifica)
            estilo: Estilo a usar (usa el de la sección si no se especifica)
            regenerar: Si True, regenera incluso si ya existe
            
        Returns:
            NoticiaSalida con el contenido generado
        """
        # Verificar si ya existe y no queremos regenerar
        if not regenerar:
            existente = self.db.query(NoticiaSalida).filter(
                NoticiaSalida.noticia_id == noticia.id,
                NoticiaSalida.salida_id == salida.id
            ).first()
            if existente:
                # Validar que el contenido existente tenga al menos 10 caracteres
                if not existente.contenido_generado or len(existente.contenido_generado.strip()) < 10:
                    existente.contenido_generado = "Contenido generado automáticamente (simulado) para esta salida."
                    self.db.commit()
                return existente
        
        # Obtener prompt y estilo de la sección si no se especificaron
        if not prompt and noticia.seccion and noticia.seccion.prompt:
            prompt = noticia.seccion.prompt
        
        if not estilo and noticia.seccion and noticia.seccion.estilo:
            estilo = noticia.seccion.estilo
        
        # Validar que tengamos un prompt
        if not prompt:
            raise ValueError("Se requiere un prompt para generar contenido")
        
        # Preparar variables para el prompt
        variables = {
            "titulo": noticia.titulo,
            "contenido": noticia.contenido,
            "autor": noticia.autor_nombre,  # Usar la propiedad que obtiene el username
            "seccion": noticia.seccion.nombre if noticia.seccion else "General",
            "tipo_salida": salida.tipo_salida,
            "nombre_salida": salida.nombre,
            "fecha": noticia.fecha.strftime("%d/%m/%Y") if noticia.fecha else "",
            # Añadido para prompts que requieren {tema}
            "tema": noticia.titulo
        }
        
        # Añadir configuración específica de la salida
        if salida.configuracion:
            for key, value in salida.configuracion.items():
                variables[f"salida_{key}"] = str(value)
        
        # Procesar prompt con variables
        prompt_procesado = self.procesar_prompt(prompt, variables)
        
        # Aplicar estilo si existe
        if estilo:
            prompt_final = self.aplicar_estilo(prompt_procesado, estilo)
        else:
            prompt_final = prompt_procesado
        # Añadir instrucciones específicas del tipo de salida
        instrucciones_salida = self._get_instrucciones_salida(salida)
        if instrucciones_salida:
            prompt_final = f"{prompt_final}\n\n{instrucciones_salida}"
        # Generar contenido
        resultado = self.generar_contenido(
            llm=llm,
            prompt_contenido=prompt_final,
            max_tokens=self._get_max_tokens_salida(salida),
            temperature=0.7
        )
        # Aplicar configuración merged (Estilo + Salida) en post-procesamiento
        merged_raw = self.merge_configs(getattr(estilo, 'configuracion', {}) if estilo else {}, getattr(salida, 'configuracion', {}) or {})
        # merge_configs puede devolver {'_merged':..., '_metadata':...} cuando modo='combine'
        if isinstance(merged_raw, dict) and '_merged' in merged_raw:
            merged_config = merged_raw.get('_merged', {})
            merge_metadata = merged_raw.get('_metadata', {})
        else:
            merged_config = merged_raw or {}
            merge_metadata = {}
        try:
            contenido_proc = resultado.get('contenido', '')
            # Eliminar emojis si la salida no los permite
            if merged_config.get('permite_emojis') is False:
                contenido_proc = self._remove_emojis(contenido_proc)
            # Aplicar truncado por max_caracteres (solo si está definido en la Salida)
            if 'max_caracteres' in merged_config and merged_config.get('max_caracteres'):
                try:
                    mc = int(merged_config.get('max_caracteres'))
                    estrategia = merged_config.get('truncar_estrategia', 'smart')
                    contenido_proc = self._apply_max_caracteres(contenido_proc, mc, estrategia)
                except Exception:
                    pass
            resultado['contenido'] = contenido_proc
        except Exception as e:
            print(f"[WARNING] Error post-procesando contenido según configuración de salida: {e}")
        # Validar que el contenido generado tenga al menos 10 caracteres
        if not resultado["contenido"] or len(resultado["contenido"].strip()) < 10:
            resultado["contenido"] = "Contenido generado automáticamente (simulado) para esta salida."

        # Aplicar configuración merged (Estilo + Salida) en post-procesamiento (temporal)
        merged_raw = self.merge_configs(getattr(estilo, 'configuracion', {}) if estilo else {}, getattr(salida, 'configuracion', {}) or {})
        if isinstance(merged_raw, dict) and '_merged' in merged_raw:
            merged_config = merged_raw.get('_merged', {})
            merge_metadata = merged_raw.get('_metadata', {})
        else:
            merged_config = merged_raw or {}
            merge_metadata = {}
        try:
            contenido_proc = resultado.get('contenido', '')
            if merged_config.get('permite_emojis') is False:
                contenido_proc = self._remove_emojis(contenido_proc)
            if 'max_caracteres' in merged_config and merged_config.get('max_caracteres'):
                try:
                    mc = int(merged_config.get('max_caracteres'))
                    estrategia = merged_config.get('truncar_estrategia', 'smart')
                    contenido_proc = self._apply_max_caracteres(contenido_proc, mc, estrategia)
                except Exception:
                    pass
            resultado['contenido'] = contenido_proc
        except Exception as e:
            print(f"[WARNING] Error post-procesando contenido temporal según configuración de salida: {e}")
        # Crear o actualizar NoticiaSalida
        if regenerar:
            noticia_salida = self.db.query(NoticiaSalida).filter(
                NoticiaSalida.noticia_id == noticia.id,
                NoticiaSalida.salida_id == salida.id
            ).first()
            if noticia_salida:
                noticia_salida.titulo = resultado["titulo"]  # ← CAMBIO: usar título generado por IA
                noticia_salida.contenido_generado = resultado["contenido"]
                noticia_salida.tokens_usados = resultado["tokens_usados"]
                noticia_salida.tiempo_generacion_ms = resultado["tiempo_ms"]
                noticia_salida.generado_en = datetime.utcnow()
            else:
                noticia_salida = NoticiaSalida(
                    noticia_id=noticia.id,
                    salida_id=salida.id,
                    titulo=resultado["titulo"],  # ← CAMBIO: usar título generado por IA
                    contenido_generado=resultado["contenido"],
                    tokens_usados=resultado["tokens_usados"],
                    tiempo_generacion_ms=resultado["tiempo_ms"]
                )
                self.db.add(noticia_salida)
        else:
            noticia_salida = NoticiaSalida(
                noticia_id=noticia.id,
                salida_id=salida.id,
                titulo=resultado["titulo"],  # ← CAMBIO: usar título generado por IA
                contenido_generado=resultado["contenido"],
                tokens_usados=resultado["tokens_usados"],
                tiempo_generacion_ms=resultado["tiempo_ms"]
            )
            self.db.add(noticia_salida)
        self.db.commit()
        self.db.refresh(noticia_salida)
        return noticia_salida
    
    # ==================== GENERACIÓN MÚLTIPLE ====================
    
    def generar_multiples_salidas(
        self,
        noticia: Noticia,
        salidas: List[SalidaMaestro],
        llm: LLMMaestro,
        prompt: Optional[PromptMaestro] = None,
        estilo: Optional[EstiloMaestro] = None,
        regenerar: bool = False
    ) -> List[NoticiaSalida]:
        """
        Genera contenido para múltiples salidas
        
        Args:
            noticia: Noticia fuente
            salidas: Lista de salidas a generar
            llm: Modelo LLM a usar
            prompt: Prompt opcional
            estilo: Estilo opcional
            regenerar: Si True, regenera incluso si ya existen
            
        Returns:
            Lista de NoticiaSalida generadas
        """
        resultados = []
        errores = []
        
        print(f"🔄 Iniciando generación para {len(salidas)} salidas:")
        for i, salida in enumerate(salidas):
            print(f"  {i+1}. {salida.nombre} (ID: {salida.id})")
        
        for salida in salidas:
            try:
                print(f"🎯 Generando para salida: {salida.nombre}")
                noticia_salida = self.generar_para_salida(
                    noticia=noticia,
                    salida=salida,
                    llm=llm,
                    prompt=prompt,
                    estilo=estilo,
                    regenerar=regenerar
                )
                print(f"✅ Salida generada exitosamente: {salida.nombre}")
                resultados.append(noticia_salida)
            except Exception as e:
                print(f"❌ Error generando salida {salida.nombre}: {str(e)}")
                errores.append({
                    "salida_id": salida.id,
                    "salida_nombre": salida.nombre,
                    "error": str(e)
                })
        
        if errores:
            print(f"⚠️ Errores al generar {len(errores)} salidas:")
            for err in errores:
                print(f"  - {err['salida_nombre']}: {err['error']}")
        
        print(f"📊 Resumen: {len(resultados)} salidas generadas exitosamente, {len(errores)} errores")
        return resultados
    
    def generar_multiples_salidas_temporal(
        self,
        noticia_temporal: Any,  # SimpleNamespace con datos de noticia
        salidas: List[SalidaMaestro],
        llm: LLMMaestro,
        regenerar: bool = True,
        usuario_id: Optional[int] = None,
        capturar_metricas: bool = False,
        session_id: Optional[str] = None  # Para métricas temporales
    ) -> Dict[str, Any]:
        """
        Genera contenido para múltiples salidas usando datos temporales
        NO guarda en BD, solo devuelve resultados
        
        Args:
            noticia_temporal: Objeto con datos de noticia (no guardada en BD)
            salidas: Lista de salidas a generar
            llm: Modelo LLM a usar
            regenerar: Siempre True para temporal
            usuario_id: ID del usuario (para métricas admin)
            capturar_metricas: Si capturar métricas de valor periodístico
            session_id: ID de sesión para métricas temporales
            
        Returns:
            Dict con resultados temporales y métricas (si es admin)
        """
        resultados = []
        errores = []
        
        # Identificador único para detectar llamadas duplicadas
        import uuid
        llamada_id = str(uuid.uuid4())[:8]
        print(f"🚀 INICIO generar_multiples_salidas_temporal - Llamada ID: {llamada_id}")
        print(f"🔍 Params: noticia_id={getattr(noticia_temporal, 'id', None)}, salidas={len(salidas)}, capturar_metricas={capturar_metricas}")
        
        # Captura de tiempo inicio para métricas
        inicio_total = time.time()
        tokens_totales = 0
        contenido_total = ""
        
        print(f"🔄 Iniciando generación TEMPORAL para {len(salidas)} salidas:")
        for i, salida in enumerate(salidas):
            print(f"  {i+1}. {salida.nombre} (ID: {salida.id}) - MODO TEMPORAL")
        
        for salida in salidas:
            try:
                print(f"🎯 Generando temporalmente para salida: {salida.nombre}")
                
                # Capturar tiempo por salida individual
                inicio_salida = time.time()
                
                resultado_temporal = self.generar_para_salida_temporal(
                    noticia_temporal=noticia_temporal,
                    salida=salida,
                    llm=llm
                )
                
                fin_salida = time.time()
                tiempo_salida = fin_salida - inicio_salida
                
                # Añadir tiempo de esta salida al resultado
                resultado_temporal["tiempo_generacion"] = tiempo_salida
                
                # Acumular para métricas
                if capturar_metricas:
                    tokens_salida = resultado_temporal.get("tokens_usados", 0)
                    print(f"🔍 Debug tokens - Salida {salida.nombre}: tokens_salida={tokens_salida}")
                    tokens_totales += tokens_salida
                    contenido_total += f"{resultado_temporal.get('titulo', '')} {resultado_temporal.get('contenido', '')} "
                    print(f"🔍 Debug tokens - Total acumulado: {tokens_totales}")
                
                print(f"✅ Salida temporal generada: {salida.nombre} ({tiempo_salida:.2f}s)")
                resultados.append(resultado_temporal)
                
            except Exception as e:
                print(f"❌ Error generando salida temporal {salida.nombre}: {str(e)}")
                errores.append({
                    "salida_id": salida.id,
                    "salida_nombre": salida.nombre,
                    "error": str(e)
                })
        
        # Tiempo total transcurrido
        fin_total = time.time()
        tiempo_total = fin_total - inicio_total
        
        if errores:
            print(f"⚠️ Errores al generar {len(errores)} salidas temporales:")
            for err in errores:
                print(f"  - {err['salida_nombre']}: {err['error']}")
        
        print(f"📊 Resumen temporal: {len(resultados)} salidas generadas, {len(errores)} errores en {tiempo_total:.2f}s")
        
        # Preparar respuesta
        response = {
            "salidas_generadas": resultados,
            "errores": errores,
            "tiempo_total": tiempo_total,
            "cantidad_salidas": len(resultados)
        }
        
        # Calcular y añadir métricas si es solicitado (solo admin)
        print(f"🔍 Debug métricas: capturar_metricas={capturar_metricas}, len(resultados)={len(resultados)}")
        if capturar_metricas and len(resultados) > 0:
            try:
                print("📈 Iniciando cálculo de métricas...")
                print(f"🔍 Debug métricas - tokens_totales={tokens_totales}, contenido_total_len={len(contenido_total)}")
                tipo_noticia = getattr(noticia_temporal, 'tipo', 'feature')
                complejidad = 'media'  # Se puede hacer más sofisticado
                
                tokens_estimados = len(contenido_total.split()) * 1.3
                tokens_finales = max(tokens_totales, tokens_estimados)
                print(f"🔍 Debug métricas DETALLADO:")
                print(f"  - tokens_totales (acumulado): {tokens_totales}")
                print(f"  - contenido_total_len: {len(contenido_total)} chars")
                print(f"  - contenido_total palabras: {len(contenido_total.split())} palabras")
                print(f"  - tokens_estimados: {tokens_estimados}")
                print(f"  - tokens_finales (max): {tokens_finales}")
                print(f"  - tiempo_total: {tiempo_total} segundos")
                print(f"  - cantidad_salidas: {len(resultados)}")
                print(f"  - modelo_usado: {llm.modelo_id}")
                
                metricas = self.calcular_metricas_valor(
                    tiempo_generacion_total=tiempo_total,
                    tokens_totales=tokens_finales,
                    cantidad_salidas=len(resultados),
                    modelo_usado=llm.modelo_id,  # Corregido: modelo_id en lugar de modelo
                    contenido_total=contenido_total,
                    tipo_noticia=tipo_noticia,
                    complejidad=complejidad
                )
                
                print(f"🔍 Debug métricas CALCULADAS:")
                print(f"  - tokens_total: {metricas.get('tokens_total', 'NO EXISTE')}")
                print(f"  - costo_generacion: {metricas.get('costo_generacion', 'NO EXISTE')}")
                print(f"  - costo_estimado_manual: {metricas.get('costo_estimado_manual', 'NO EXISTE')}")
                print(f"  - roi_porcentaje: {metricas.get('roi_porcentaje', 'NO EXISTE')}")
                
                # Añadir resumen de métricas a la respuesta
                response["metricas_valor"] = self.obtener_resumen_metricas(metricas).dict()
                
                print(f"📈 Métricas calculadas - ROI: {metricas['roi_porcentaje']}%, Ahorro: {metricas['ahorro_tiempo_minutos']} min")
                print(f"🔍 Debug métricas finales - tokens_total: {metricas['tokens_total']}, costo_generacion: {metricas['costo_generacion']}")
                
                # Determinar si se debe guardar en BD
                es_noticia_existente = hasattr(noticia_temporal, 'id') and noticia_temporal.id
                tiene_usuario_id = usuario_id is not None
                
                print(f"🔍 Evaluación guardado BD:")
                print(f"  - es_noticia_existente: {es_noticia_existente}")
                print(f"  - tiene_usuario_id: {tiene_usuario_id}")
                print(f"  - noticia_temporal.id: {getattr(noticia_temporal, 'id', 'NO EXISTE')}")
                
                # Guardar métricas si: es noticia existente O si tenemos usuario_id (admin generando temporal)
                if es_noticia_existente or tiene_usuario_id:
                    try:
                        # Determinar el noticia_id para guardar
                        if es_noticia_existente:
                            noticia_id_para_guardar = noticia_temporal.id
                            print(f"💾 Guardando métricas para noticia existente ID: {noticia_id_para_guardar}")
                        else:
                            # Es generación temporal pero queremos guardar métricas (admin)
                            # Necesitamos crear una entrada temporal o usar un ID especial
                            print(f"💾 Generación temporal con métricas para usuario {usuario_id}")
                            print(f"⚠️ SKIP: No se puede guardar métricas sin noticia_id válido")
                            noticia_id_para_guardar = None
                        
                        if noticia_id_para_guardar:
                            print(f"🔍 Valores consolidados a guardar: tokens={metricas['tokens_total']}, costo={metricas['costo_generacion']}")
                            
                            # Primero limpiar duplicados existentes
                            self.limpiar_metricas_duplicadas(noticia_id_para_guardar)
                            
                            # Verificar si ya existe una métrica para esta noticia en esta sesión
                            metrica_existente = self.db.query(MetricasValorPeriodistico).filter(
                                MetricasValorPeriodistico.noticia_id == noticia_id_para_guardar
                            ).order_by(MetricasValorPeriodistico.created_at.desc()).first()
                            
                            # Si existe una métrica reciente (menos de 5 minutos), actualizarla en lugar de crear nueva
                            from datetime import datetime, timedelta
                            now = datetime.now()
                            
                            if (metrica_existente and 
                                metrica_existente.created_at and 
                                (now - metrica_existente.created_at) < timedelta(minutes=5)):
                                
                                print(f"🔄 Actualizando métrica existente ID: {metrica_existente.id} (creada hace {(now - metrica_existente.created_at).total_seconds():.0f}s)")
                                
                                # Actualizar con nuevos valores consolidados
                                metrica_existente.tiempo_generacion_total = metricas["tiempo_generacion_total"]
                                metrica_existente.tokens_total = metricas["tokens_total"]
                                metrica_existente.costo_generacion = metricas["costo_generacion"]
                                metrica_existente.costo_estimado_manual = metricas["costo_estimado_manual"]
                                metrica_existente.ahorro_costo = metricas["ahorro_costo"]
                                metrica_existente.cantidad_salidas_generadas = metricas["cantidad_salidas_generadas"]
                                metrica_existente.cantidad_formatos_diferentes = metricas["cantidad_formatos_diferentes"]
                                metrica_existente.velocidad_palabras_por_segundo = metricas["velocidad_palabras_por_segundo"]
                                metrica_existente.roi_porcentaje = metricas["roi_porcentaje"]
                                metrica_existente.updated_at = now
                                
                                self.db.commit()
                                self.db.refresh(metrica_existente)
                                metrica_guardada = metrica_existente
                                print(f"✅ Métrica actualizada en BD con ID: {metrica_guardada.id}")
                            else:
                                # Crear nueva métrica
                                print(f"📝 Creando nueva métrica para noticia {noticia_id_para_guardar} o session {session_id}")
                                metrica_guardada = self.guardar_metricas_valor(
                                    noticia_id=noticia_id_para_guardar,
                                    usuario_id=usuario_id,
                                    metricas=metricas,
                                    session_id=session_id  # Pasar session_id para métricas temporales
                                )
                                print(f"✅ Nueva métrica creada en BD con ID: {metrica_guardada.id}")
                            
                            # Verificar que se guardó correctamente
                            if metrica_guardada:
                                print(f"🔍 Verificación final: BD tokens={metrica_guardada.tokens_total}, BD costo={metrica_guardada.costo_generacion}")
                    except Exception as save_error:
                        print(f"⚠️ Error guardando métricas en BD: {save_error}")
                        import traceback
                        traceback.print_exc()
                        # No fallar la respuesta por errores de guardado
                
            except Exception as e:
                print(f"⚠️ Error calculando métricas: {e}")
                import traceback
                traceback.print_exc()
                # No fallar la respuesta por errores de métricas
        else:
            print(f"❌ No se calcularán métricas: capturar_metricas={capturar_metricas}, len(resultados)={len(resultados)}")
        
        print(f"🏁 FIN generar_multiples_salidas_temporal - Llamada ID: {llamada_id}")
        return response
    
    def generar_para_salida_temporal(
        self,
        noticia_temporal: Any,
        salida: SalidaMaestro,
        llm: LLMMaestro,
        prompt: Optional[PromptMaestro] = None,
        estilo: Optional[EstiloMaestro] = None
    ) -> Dict[str, Any]:
        """
        Genera contenido para una salida específica usando datos temporales
        NO guarda en BD, solo procesa y devuelve resultado
        
        Returns:
            Dict con resultado temporal (similar a NoticiaSalida pero sin BD)
        """
        # Obtener prompt y estilo de la sección si no se especificaron
        if not prompt and hasattr(noticia_temporal, 'seccion') and noticia_temporal.seccion.prompt:
            prompt = noticia_temporal.seccion.prompt
        
        if not estilo and hasattr(noticia_temporal, 'seccion') and noticia_temporal.seccion.estilo:
            estilo = noticia_temporal.seccion.estilo
        
        # Validar que tengamos un prompt
        if not prompt:
            raise ValueError("Se requiere un prompt para generar contenido")
        
        # Preparar variables para el prompt
        variables = {
            "titulo": noticia_temporal.titulo,
            "contenido": noticia_temporal.contenido,
            "autor": getattr(noticia_temporal, 'autor_nombre', 'Redacción'),  # Usar autor_nombre
            "seccion": noticia_temporal.seccion.nombre if hasattr(noticia_temporal, 'seccion') else "General",
            "tipo_salida": salida.tipo_salida,
            "nombre_salida": salida.nombre,
            "fecha": noticia_temporal.fecha.strftime("%d/%m/%Y") if hasattr(noticia_temporal, 'fecha') else "",
            "tema": noticia_temporal.titulo
        }
        
        # Añadir configuración específica de la salida
        if salida.configuracion:
            for key, value in salida.configuracion.items():
                variables[f"salida_{key}"] = str(value)
        
        # Procesar prompt con variables
        prompt_procesado = self.procesar_prompt(prompt, variables)
        
        # Aplicar estilo si existe
        if estilo:
            prompt_final = self.aplicar_estilo(prompt_procesado, estilo)
        else:
            prompt_final = prompt_procesado
            
        # Añadir instrucciones específicas del tipo de salida
        instrucciones_salida = self._get_instrucciones_salida(salida)
        if instrucciones_salida:
            prompt_final = f"{prompt_final}\n\n{instrucciones_salida}"
        
        # 🔧 SOLUCIÓN: Asegurar que el contenido de la noticia esté incluido
        # Si el prompt no incluye las variables de noticia, agregarlas automáticamente
        if "{{titulo}}" not in prompt_final and "{{contenido}}" not in prompt_final:
            prompt_final = f"""{prompt_final}

---
**NOTICIA A PROCESAR:**

TÍTULO: {noticia_temporal.titulo}

CONTENIDO ORIGINAL:
{noticia_temporal.contenido}

---

Con base en la noticia anterior, genera el contenido optimizado para {salida.nombre} ({salida.tipo_salida}) siguiendo todas las directrices mencionadas."""
            print(f"[DEBUG] ✅ Contenido de noticia agregado automáticamente al prompt")
        else:
            print(f"[DEBUG] ❌ Prompt ya contiene variables de noticia")
        
        print(f"[DEBUG] Prompt COMPLETO enviado al LLM ({len(prompt_final)} chars):")
        print(f"[DEBUG] Primeros 500 chars: {prompt_final[:500]}...")
        print(f"[DEBUG] Últimos 300 chars: ...{prompt_final[-300:]}")
        print(f"[DEBUG] ¿Contiene título de noticia '{noticia_temporal.titulo[:30]}'? {noticia_temporal.titulo[:30] in prompt_final}")
            
        # Generar contenido
        resultado = self.generar_contenido(
            llm=llm,
            prompt_contenido=prompt_final,
            max_tokens=self._get_max_tokens_salida(salida),
            temperature=0.7
        )
        
        # Validar que el contenido generado tenga al menos 10 caracteres
        if not resultado["contenido"] or len(resultado["contenido"].strip()) < 10:
            resultado["contenido"] = "Contenido generado automáticamente (simulado) para esta salida."
        # Aplicar post-procesamiento según configuración (Estilo + Salida)
        merged_raw = self.merge_configs(getattr(estilo, 'configuracion', {}) if estilo else {}, getattr(salida, 'configuracion', {}) or {})
        if isinstance(merged_raw, dict) and '_merged' in merged_raw:
            merged_config = merged_raw.get('_merged', {})
            merge_metadata = merged_raw.get('_metadata', {})
        else:
            merged_config = merged_raw or {}
            merge_metadata = {}

        try:
            contenido_proc = resultado.get('contenido', '')
            if merged_config.get('permite_emojis') is False:
                contenido_proc = self._remove_emojis(contenido_proc)
            if 'max_caracteres' in merged_config and merged_config.get('max_caracteres'):
                try:
                    mc = int(merged_config.get('max_caracteres'))
                    estrategia = merged_config.get('truncar_estrategia', 'smart')
                    contenido_proc = self._apply_max_caracteres(contenido_proc, mc, estrategia)
                except Exception:
                    pass
            resultado['contenido'] = contenido_proc
        except Exception as e:
            print(f"[WARNING] Error post-procesando contenido temporal según configuración de salida: {e}")

        # Devolver resultado temporal (formato similar a NoticiaSalida)
        return {
            "id": None,  # Temporal - no tiene ID de BD
            "noticia_id": getattr(noticia_temporal, 'id', None),
            "salida_id": salida.id,
            "titulo": resultado["titulo"],  # ← CAMBIO: usar título generado por IA
            "contenido_generado": resultado["contenido"],
            "tokens_usados": resultado["tokens_usados"],
            "tiempo_generacion_ms": resultado["tiempo_ms"],
            "generado_en": datetime.now().isoformat(),
            "nombre_salida": salida.nombre,
            "temporal": True,  # Marca que es temporal
            "merge_metadata": merge_metadata
        }
    
    # ==================== UTILIDADES ====================
    
    def _get_instrucciones_salida(self, salida: SalidaMaestro) -> str:
        """
        Obtiene instrucciones específicas según el tipo de salida
        """
        instrucciones = {
            "print": "Optimiza para formato impreso: claridad, estructura formal, uso eficiente del espacio.",
            "digital": "Optimiza para web: usa subtítulos, listas, párrafos cortos, SEO-friendly.",
            "social": "Optimiza para redes sociales: conciso, llamativo, incluye hashtags relevantes, tono casual.",
            "email": "Optimiza para newsletter: asunto atractivo, introducción enganchadora, call-to-action claro.",
            "podcast": "Optimiza para audio: lenguaje conversacional, transiciones claras, ritmo narrativo."
        }
        
        return instrucciones.get(salida.tipo_salida, "")
    
    def _get_max_tokens_salida(self, salida: SalidaMaestro) -> int:
        """
        Determina el máximo de tokens según el tipo de salida
        """
        max_tokens = {
            "print": 2000,
            "digital": 1500,
            "social": 500,
            "email": 1000,
            "podcast": 2500
        }
        
        return max_tokens.get(salida.tipo_salida, 1500)
    
    def _parsear_respuesta_estructurada(self, contenido_respuesta: str) -> Dict[str, str]:
        """
        Parsea la respuesta del LLM para extraer título y contenido por separado
        
        Args:
            contenido_respuesta: Respuesta completa del LLM con formato "TÍTULO: ... CONTENIDO: ..."
            
        Returns:
            Dict con 'titulo' y 'contenido' extraídos
        """
        import re
        
        # Patrón para capturar TÍTULO: y CONTENIDO:
        patron_titulo = r'TÍTULO:\s*(.+?)(?=\n\s*CONTENIDO:|$)'
        patron_contenido = r'CONTENIDO:\s*(.+)'
        
        # Extraer título
        match_titulo = re.search(patron_titulo, contenido_respuesta, re.DOTALL | re.IGNORECASE)
        titulo_extraido = match_titulo.group(1).strip() if match_titulo else ""
        
        # Extraer contenido
        match_contenido = re.search(patron_contenido, contenido_respuesta, re.DOTALL | re.IGNORECASE)
        contenido_extraido = match_contenido.group(1).strip() if match_contenido else ""
        
        # Si no se pudo parsear el formato, usar fallbacks
        if not titulo_extraido or not contenido_extraido:
            print(f"[WARNING] No se pudo parsear respuesta estructurada. Usando fallbacks.")
            
            # Fallback: usar las primeras líneas como título si no hay estructura
            lineas = contenido_respuesta.strip().split('\n')
            if not titulo_extraido and len(lineas) > 0:
                # Buscar una línea que parezca título (corta, sin punto final)
                for linea in lineas[:3]:
                    linea_limpia = linea.strip()
                    if 10 <= len(linea_limpia) <= 200 and not linea_limpia.endswith('.'):
                        titulo_extraido = linea_limpia
                        break
                
                # Si no encontró un título apropiado, usar la primera línea
                if not titulo_extraido:
                    titulo_extraido = lineas[0].strip()[:200]
            
            # Fallback: usar todo el contenido si no se encontró separación
            if not contenido_extraido:
                contenido_extraido = contenido_respuesta.strip()
        
        # Limpiar y validar
        titulo_extraido = titulo_extraido.replace('TÍTULO:', '').strip()
        contenido_extraido = contenido_extraido.replace('CONTENIDO:', '').strip()
        
        # Validaciones básicas
        if len(titulo_extraido) > 200:
            titulo_extraido = titulo_extraido[:200].strip()
        
        if len(titulo_extraido) < 10:
            titulo_extraido = "Título generado por IA"
        
        if len(contenido_extraido) < 50:
            contenido_extraido = f"{titulo_extraido}\n\n{contenido_extraido}" if contenido_extraido else f"Contenido generado automáticamente para {titulo_extraido}"
        
        print(f"[DEBUG] Parsing completado:")
        print(f"[DEBUG] - Título extraído: '{titulo_extraido[:50]}...'")
        print(f"[DEBUG] - Contenido extraído: {len(contenido_extraido)} caracteres")
        
        return {
            "titulo": titulo_extraido,
            "contenido": contenido_extraido
        }

    # ==================== MÉTRICAS DE VALOR PERIODÍSTICO ====================
    
    def calcular_metricas_valor(
        self,
        tiempo_generacion_total: float,
        tokens_totales: int,
        cantidad_salidas: int,
        modelo_usado: str,
        contenido_total: str,
        tipo_noticia: str = "feature",
        complejidad: str = "media"
    ) -> Dict[str, Any]:
        """
        Calcula métricas de valor periodístico para administradores
        
        Args:
            tiempo_generacion_total: Tiempo total en segundos
            tokens_totales: Tokens consumidos en total
            cantidad_salidas: Número de salidas generadas
            modelo_usado: Nombre del modelo usado
            contenido_total: Todo el contenido generado
            tipo_noticia: Tipo de noticia (breaking, feature, opinion)
            complejidad: Complejidad estimada (simple, media, compleja)
            
        Returns:
            Dict con métricas calculadas
        """
        
        print(f"📊 INICIO calcular_metricas_valor:")
        print(f"  - tiempo_generacion_total: {tiempo_generacion_total}")
        print(f"  - tokens_totales: {tokens_totales}")
        print(f"  - cantidad_salidas: {cantidad_salidas}")
        print(f"  - modelo_usado: {modelo_usado}")
        print(f"  - contenido_total_len: {len(contenido_total)}")
        
        # Cálculos base
        palabras_totales = len(contenido_total.split())
        velocidad_palabras_segundo = palabras_totales / max(tiempo_generacion_total, 0.1)
        
        print(f"  - palabras_totales: {palabras_totales}")
        print(f"  - velocidad_palabras_segundo: {velocidad_palabras_segundo}")
        
        # Estimaciones de tiempo manual basadas en tipo y complejidad
        tiempos_base_manual = {
            "breaking": {"simple": 10, "media": 15, "compleja": 25},
            "feature": {"simple": 20, "media": 30, "compleja": 45},
            "opinion": {"simple": 25, "media": 40, "compleja": 60}
        }
        
        tiempo_base_manual = tiempos_base_manual.get(tipo_noticia, tiempos_base_manual["feature"])
        tiempo_manual_minutos = tiempo_base_manual.get(complejidad, 30)
        
        # Multiplicar por cantidad de salidas (cada salida requiere adaptación manual)
        tiempo_manual_total = tiempo_manual_minutos * cantidad_salidas
        ahorro_tiempo_minutos = max(0, tiempo_manual_total - (tiempo_generacion_total / 60))
        
        # Cálculos de costo
        precios_modelo = {
            "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},  # por 1K tokens
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gemini-pro": {"input": 0.001, "output": 0.002}
        }
        
        precio_modelo = precios_modelo.get(modelo_usado, precios_modelo["claude-3-5-sonnet-20241022"])
        
        print(f"  - modelo_usado buscado: '{modelo_usado}'")
        print(f"  - precio_modelo encontrado: {precio_modelo}")
        
        # Estimación conservadora: 70% input, 30% output
        tokens_input = int(tokens_totales * 0.7)
        tokens_output = int(tokens_totales * 0.3)
        
        print(f"  - tokens_input (70%): {tokens_input}")
        print(f"  - tokens_output (30%): {tokens_output}")
        
        costo_generacion = (
            (tokens_input / 1000) * precio_modelo["input"] +
            (tokens_output / 1000) * precio_modelo["output"]
        )
        
        print(f"  - costo_input: {(tokens_input / 1000) * precio_modelo['input']}")
        print(f"  - costo_output: {(tokens_output / 1000) * precio_modelo['output']}")
        print(f"  - costo_generacion TOTAL: {costo_generacion}")
        
        # Costo manual: $15/hora promedio periodista
        costo_manual = (tiempo_manual_total / 60) * 15.0
        ahorro_costo = max(0, costo_manual - costo_generacion)
        
        # Cálculo de ROI con protección contra valores extremos
        if costo_generacion > 0.001:  # Solo calcular ROI si hay costo real
            roi_porcentaje = ((ahorro_costo) / costo_generacion) * 100
            # Limitar ROI a un máximo razonable para evitar desbordamiento de BD
            roi_porcentaje = min(roi_porcentaje, 999999.99)
        else:
            # Si el costo es casi cero, usar un ROI fijo muy alto pero controlado
            roi_porcentaje = 999999.99
        
        # Proteger velocidad también
        velocidad_palabras_segundo = min(velocidad_palabras_segundo, 999999.99)
        
        # Conteo de formatos diferentes
        formatos_diferentes = min(cantidad_salidas, 5)  # Max 5 formatos típicos
        
        resultado = {
            "tiempo_generacion_total": tiempo_generacion_total,
            "tiempo_estimado_manual": tiempo_manual_total,
            "ahorro_tiempo_minutos": int(ahorro_tiempo_minutos),
            "tokens_total": tokens_totales,
            "costo_generacion": round(costo_generacion, 4),
            "costo_estimado_manual": round(costo_manual, 2),
            "ahorro_costo": round(ahorro_costo, 2),
            "cantidad_salidas_generadas": cantidad_salidas,
            "cantidad_formatos_diferentes": formatos_diferentes,
            "velocidad_palabras_por_segundo": round(velocidad_palabras_segundo, 2),
            "roi_porcentaje": round(roi_porcentaje, 2),
            "modelo_usado": modelo_usado,
            "tipo_noticia": tipo_noticia,
            "complejidad_estimada": complejidad
        }
        
        print(f"📊 FIN calcular_metricas_valor - RESULTADO:")
        print(f"  - tokens_total: {resultado['tokens_total']}")
        print(f"  - costo_generacion: {resultado['costo_generacion']}")
        print(f"  - costo_estimado_manual: {resultado['costo_estimado_manual']}")
        print(f"  - roi_porcentaje: {resultado['roi_porcentaje']}")
        
        return resultado
    
    def limpiar_metricas_duplicadas(self, noticia_id: int) -> None:
        """
        Limpia métricas duplicadas para una noticia, manteniendo solo la más reciente
        """
        try:
            # Buscar todas las métricas para esta noticia
            metricas = self.db.query(MetricasValorPeriodistico).filter(
                MetricasValorPeriodistico.noticia_id == noticia_id
            ).order_by(MetricasValorPeriodistico.created_at.desc()).all()
            
            if len(metricas) > 1:
                print(f"🧹 Limpiando {len(metricas)-1} métricas duplicadas para noticia {noticia_id}")
                
                # Mantener solo la más reciente, eliminar el resto
                metricas_a_eliminar = metricas[1:]  # Todas excepto la primera (más reciente)
                
                for metrica in metricas_a_eliminar:
                    print(f"🗑️ Eliminando métrica duplicada ID: {metrica.id}")
                    self.db.delete(metrica)
                
                self.db.commit()
                print(f"✅ Métricas duplicadas eliminadas. Quedó solo ID: {metricas[0].id}")
                
        except Exception as e:
            print(f"⚠️ Error limpiando métricas duplicadas: {e}")
            self.db.rollback()

    def guardar_metricas_valor(
        self,
        metricas: Dict[str, Any],
        noticia_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
    # Eliminado: session_id, ya no se usa para métricas temporales
    ) -> Optional[MetricasValorPeriodistico]:
        """
        Guarda métricas de valor en la base de datos
        Solo para uso por administradores
    Solo soporta noticia_id (persistente)
        """
        import uuid
        save_id = str(uuid.uuid4())[:8]
        print(f"💾 INICIO guardar_metricas_valor - Save ID: {save_id}")
        print(f"💾 Input metricas dict keys: {list(metricas.keys())}")
        print(f"💾 Guardando para noticia_id={noticia_id}")
        
        # Validar que tenga noticia_id
        if not noticia_id:
            print(f"⚠️ ERROR: Necesita noticia_id para guardar métricas")
            return None
        print(f"💾 tokens_total: {metricas.get('tokens_total', 'MISSING')}")
        print(f"💾 costo_generacion: {metricas.get('costo_generacion', 'MISSING')}")
        
        try:
            print(f"🔎 Dump metricas dict antes de asignar:")
            for k, v in metricas.items():
                print(f"    {k}: {v} (type={type(v)})")

                metrica_obj = MetricasValorPeriodistico(
                    noticia_id=noticia_id,
                    tiempo_generacion_total=metricas.get("tiempo_generacion_total", 0),
                    tiempo_por_salida={},  # Se puede expandir en el futuro
                    tiempo_estimado_manual=metricas.get("tiempo_estimado_manual", 30),
                    ahorro_tiempo_minutos=metricas.get("ahorro_tiempo_minutos", 0),
                    tokens_total=metricas.get("tokens_total", 0),
                    costo_generacion=metricas.get("costo_generacion", 0.0),
                    costo_estimado_manual=metricas.get("costo_estimado_manual", 0),
                    ahorro_costo=metricas.get("ahorro_costo", 0.0),
                    cantidad_salidas_generadas=metricas.get("cantidad_salidas_generadas", 0),
                    cantidad_formatos_diferentes=metricas.get("cantidad_formatos_diferentes", 0),
                    velocidad_palabras_por_segundo=metricas.get("velocidad_palabras_por_segundo", 0.0),
                    modelo_usado=metricas.get("modelo_usado", ""),
                    usuario_id=usuario_id,
                    tipo_noticia=metricas.get("tipo_noticia", ""),
                    complejidad_estimada=metricas.get("complejidad_estimada", ""),
                    roi_porcentaje=metricas.get("roi_porcentaje", 0.0)
                )

            print(f"🔎 Dump metrica_obj antes de commit:")
            print(f"    tokens_total: {metrica_obj.tokens_total} (type={type(metrica_obj.tokens_total)})")
            print(f"    costo_generacion: {metrica_obj.costo_generacion} (type={type(metrica_obj.costo_generacion)})")

            self.db.add(metrica_obj)
            self.db.commit()
            self.db.refresh(metrica_obj)

            print(f"💾 FIN guardar_metricas_valor - Save ID: {save_id} - BD ID: {metrica_obj.id}")
            print(f"💾 Verificación post-commit: tokens={metrica_obj.tokens_total}, costo={metrica_obj.costo_generacion}")
            return metrica_obj

        except Exception as e:
            print(f"❌ Error guardando métricas de valor (Save ID: {save_id}): {e}")
            self.db.rollback()
            return None
    
    def obtener_resumen_metricas(self, metricas: Dict[str, Any]) -> MetricasValorResumen:
        """
        Convierte métricas completas a resumen para frontend
        Solo visible para administradores
        """
        # Calcular eficiencia temporal
        tiempo_manual = metricas.get("tiempo_estimado_manual", 30)
        tiempo_ia = metricas.get("tiempo_generacion_total", 1) / 60  # convertir a minutos
        eficiencia_temporal = max(0, (tiempo_manual - tiempo_ia) / tiempo_manual * 100)
        
        return MetricasValorResumen(
            ahorro_tiempo_minutos=metricas["ahorro_tiempo_minutos"],
            ahorro_costo=metricas.get("ahorro_costo", 0.0),
            costo_generacion=metricas["costo_generacion"],
            costo_estimado_manual=metricas["costo_estimado_manual"],
            cantidad_formatos=metricas["cantidad_salidas_generadas"],
            roi_porcentaje=metricas["roi_porcentaje"],
            velocidad_palabras_por_segundo=metricas["velocidad_palabras_por_segundo"],
            eficiencia_temporal=round(eficiencia_temporal, 1),
            porcentaje_contenido_aprovechable=0.90,  # Valor por defecto optimista
            tokens_total=metricas.get("tokens_total", 0),
            modelo_usado=metricas["modelo_usado"],
            tiempo_total_segundos=metricas["tiempo_generacion_total"]
        )
