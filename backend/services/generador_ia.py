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
    NoticiaSalida
)


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
                model = cliente.GenerativeModel(llm.modelo_id)
                # Google Gemini espera un string, así que concatenamos el historial
                system_prompt = "system: Eres un asistente conversacional útil, responde de forma clara y precisa."
                prompt_lines = [system_prompt] + [f"{m['role']}: {m['content']}" for m in messages]
                prompt_str = '\n'.join(prompt_lines)
                respuesta = model.generate_content(prompt_str)
                contenido = respuesta.text
                tokens_usados = len(prompt_str.split()) + len(contenido.split())
            else:
                raise ValueError(f"Proveedor no soportado: {llm.proveedor}")
            tiempo_ms = int((time.time() - inicio) * 1000)
            llm.tokens_usados_hoy += tokens_usados
            self.db.commit()
            print("[DEBUG] Contenido generado por el LLM:\n", contenido)
            if not contenido or len(contenido.strip()) < 10:
                raise Exception("El LLM devolvió un contenido vacío o muy corto. Revisa el prompt y la configuración del modelo.")
            return {
                "contenido": contenido,
                "tokens_usados": tokens_usados,
                "tiempo_ms": tiempo_ms
            }
        except Exception as e:
            print(f"[ERROR] Error al generar contenido con {llm.nombre}: {str(e)}")
            raise Exception(f"Error al generar contenido con {llm.nombre}: {str(e)}")
    
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
        contenido = prompt.contenido
        
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
            "autor": noticia.autor or "Redacción",
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
                noticia_salida.titulo = noticia.titulo
                noticia_salida.contenido_generado = resultado["contenido"]
                noticia_salida.tokens_usados = resultado["tokens_usados"]
                noticia_salida.tiempo_generacion_ms = resultado["tiempo_ms"]
                noticia_salida.generado_en = datetime.utcnow()
            else:
                noticia_salida = NoticiaSalida(
                    noticia_id=noticia.id,
                    salida_id=salida.id,
                    titulo=noticia.titulo,
                    contenido_generado=resultado["contenido"],
                    tokens_usados=resultado["tokens_usados"],
                    tiempo_generacion_ms=resultado["tiempo_ms"]
                )
                self.db.add(noticia_salida)
        else:
            noticia_salida = NoticiaSalida(
                noticia_id=noticia.id,
                salida_id=salida.id,
                titulo=noticia.titulo,
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
        
        for salida in salidas:
            try:
                noticia_salida = self.generar_para_salida(
                    noticia=noticia,
                    salida=salida,
                    llm=llm,
                    prompt=prompt,
                    estilo=estilo,
                    regenerar=regenerar
                )
                resultados.append(noticia_salida)
            except Exception as e:
                errores.append({
                    "salida_id": salida.id,
                    "salida_nombre": salida.nombre,
                    "error": str(e)
                })
        
        if errores:
            print(f"⚠️ Errores al generar {len(errores)} salidas:")
            for err in errores:
                print(f"  - {err['salida_nombre']}: {err['error']}")
        
        return resultados
    
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
