"""
Servicio de Generación IA Multi-LLM
Gestiona la generación de contenido con diferentes proveedores (Claude, GPT, Gemini)
"""
from typing import Optional, Dict, Any, List
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


class GeneradorIA:
    """
    Clase principal para generar contenido con IA
    Soporta múltiples proveedores: Anthropic (Claude), OpenAI (GPT), Google (Gemini)
    """
    
    def __init__(self, db: Session):
        self.db = db
        self._clientes = {}  # Cache de clientes API
    
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
        # Obtener contenido de PromptItem (primer item activo)
        contenido = ""
        if prompt.items and len(prompt.items) > 0:
            contenido = prompt.items[0].contenido or ""
            print(f"[DEBUG] Contenido del prompt '{prompt.nombre}': {len(contenido)} caracteres")
        else:
            print(f"[DEBUG] No se encontraron items para el prompt '{prompt.nombre}'")
        
        # Si no hay contenido, usar prompt por defecto
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
        
        return prompt_final
    
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
        # Validar que el contenido generado tenga al menos 10 caracteres
        if not resultado["contenido"] or len(resultado["contenido"].strip()) < 10:
            resultado["contenido"] = "Contenido generado automáticamente (simulado) para esta salida."
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
        capturar_metricas: bool = False
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
            
        Returns:
            Dict con resultados temporales y métricas (si es admin)
        """
        resultados = []
        errores = []
        
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
                    tokens_totales += tokens_salida
                    contenido_total += f"{resultado_temporal.get('titulo', '')} {resultado_temporal.get('contenido', '')} "
                
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
                tipo_noticia = getattr(noticia_temporal, 'tipo', 'feature')
                complejidad = 'media'  # Se puede hacer más sofisticado
                
                metricas = self.calcular_metricas_valor(
                    tiempo_generacion_total=tiempo_total,
                    tokens_totales=max(tokens_totales, len(contenido_total.split()) * 1.3),  # Estimación si no hay tokens
                    cantidad_salidas=len(resultados),
                    modelo_usado=llm.modelo,
                    contenido_total=contenido_total,
                    tipo_noticia=tipo_noticia,
                    complejidad=complejidad
                )
                
                # Añadir resumen de métricas a la respuesta
                response["metricas_valor"] = self.obtener_resumen_metricas(metricas).dict()
                
                print(f"📈 Métricas calculadas - ROI: {metricas['roi_porcentaje']}%, Ahorro: {metricas['ahorro_tiempo_minutos']} min")
                
            except Exception as e:
                print(f"⚠️ Error calculando métricas: {e}")
                import traceback
                traceback.print_exc()
                # No fallar la respuesta por errores de métricas
        else:
            print(f"❌ No se calcularán métricas: capturar_metricas={capturar_metricas}, len(resultados)={len(resultados)}")
        
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
            "temporal": True  # Marca que es temporal
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
        
        # Cálculos base
        palabras_totales = len(contenido_total.split())
        velocidad_palabras_segundo = palabras_totales / max(tiempo_generacion_total, 0.1)
        
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
        
        # Estimación conservadora: 70% input, 30% output
        tokens_input = int(tokens_totales * 0.7)
        tokens_output = int(tokens_totales * 0.3)
        
        costo_generacion = (
            (tokens_input / 1000) * precio_modelo["input"] +
            (tokens_output / 1000) * precio_modelo["output"]
        )
        
        # Costo manual: $15/hora promedio periodista
        costo_manual = (tiempo_manual_total / 60) * 15.0
        ahorro_costo = max(0, costo_manual - costo_generacion)
        
        # Cálculo de ROI
        roi_porcentaje = ((ahorro_costo) / max(costo_generacion, 0.001)) * 100
        
        # Conteo de formatos diferentes
        formatos_diferentes = min(cantidad_salidas, 5)  # Max 5 formatos típicos
        
        return {
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
    
    def guardar_metricas_valor(
        self,
        metricas: Dict[str, Any],
        noticia_id: int,
        usuario_id: Optional[int] = None
    ) -> Optional[MetricasValorPeriodistico]:
        """
        Guarda métricas de valor en la base de datos
        Solo para uso por administradores
        """
        try:
            metrica_obj = MetricasValorPeriodistico(
                noticia_id=noticia_id,
                tiempo_generacion_total=metricas["tiempo_generacion_total"],
                tiempo_por_salida={},  # Se puede expandir en el futuro
                tiempo_estimado_manual=metricas["tiempo_estimado_manual"],
                ahorro_tiempo_minutos=metricas["ahorro_tiempo_minutos"],
                tokens_total=metricas["tokens_total"],
                costo_generacion=metricas["costo_generacion"],
                costo_estimado_manual=metricas["costo_estimado_manual"],
                ahorro_costo=metricas["ahorro_costo"],
                cantidad_salidas_generadas=metricas["cantidad_salidas_generadas"],
                cantidad_formatos_diferentes=metricas["cantidad_formatos_diferentes"],
                velocidad_palabras_por_segundo=metricas["velocidad_palabras_por_segundo"],
                modelo_usado=metricas["modelo_usado"],
                usuario_id=usuario_id,
                tipo_noticia=metricas["tipo_noticia"],
                complejidad_estimada=metricas["complejidad_estimada"],
                roi_porcentaje=metricas["roi_porcentaje"]
            )
            
            self.db.add(metrica_obj)
            self.db.commit()
            self.db.refresh(metrica_obj)
            
            return metrica_obj
            
        except Exception as e:
            print(f"❌ Error guardando métricas de valor: {e}")
            self.db.rollback()
            return None
    
    def obtener_resumen_metricas(self, metricas: Dict[str, Any]) -> MetricasValorResumen:
        """
        Convierte métricas completas a resumen para frontend
        Solo visible para administradores
        """
        return MetricasValorResumen(
            ahorro_tiempo_minutos=metricas["ahorro_tiempo_minutos"],
            costo_generacion=metricas["costo_generacion"],
            costo_estimado_manual=metricas["costo_estimado_manual"],
            cantidad_formatos=metricas["cantidad_salidas_generadas"],
            roi_porcentaje=metricas["roi_porcentaje"],
            velocidad_palabras_segundo=metricas["velocidad_palabras_por_segundo"],
            modelo_usado=metricas["modelo_usado"],
            tiempo_total_segundos=metricas["tiempo_generacion_total"]
        )
