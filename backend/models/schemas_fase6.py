"""
Schemas Pydantic para Fase 6 - Sistema de Maestros
Validación de datos para nuevas tablas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


# ==================== ENUMS ====================

class ProveedorLLM(str, Enum):
    """Proveedores de LLM disponibles"""
    ANTHROPIC = "Anthropic"
    OPENAI = "OpenAI"
    GOOGLE = "Google"
    COHERE = "Cohere"
    MISTRAL = "Mistral"


class TipoSalida(str, Enum):
    """Tipos de salida disponibles"""
    PRINT = "print"           # Impreso
    DIGITAL = "digital"       # Web/Digital
    SOCIAL = "social"         # Redes Sociales
    EMAIL = "email"           # Email/Newsletter
    PODCAST = "podcast"       # Audio/Podcast


class CategoriaPrompt(str, Enum):
    """Categorías de prompts"""
    NOTICIA = "noticia"
    REPORTAJE = "reportaje"
    BREVE = "breve"
    EDITORIAL = "editorial"
    ENTREVISTA = "entrevista"
    OPINION = "opinion"


class TipoEstilo(str, Enum):
    """Tipos de estilos"""
    TONO = "tono"
    FORMATO = "formato"
    ESTRUCTURA = "estructura"
    LONGITUD = "longitud"


# ==================== LLM MAESTRO ====================

class LLMMaestroBase(BaseModel):
    """Schema base para LLM Maestro"""
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del modelo LLM")
    proveedor: ProveedorLLM = Field(..., description="Proveedor del modelo")
    modelo_id: str = Field(..., min_length=3, max_length=100, description="ID del modelo (ej: claude-sonnet-4-20250514)")
    url_api: str = Field(..., min_length=10, max_length=500, description="URL del API")
    api_key: str = Field(..., min_length=10, description="API Key (se encriptará)")
    version: Optional[str] = Field(None, max_length=50, description="Versión del modelo")
    configuracion: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Parámetros adicionales")
    headers_adicionales: Optional[Dict[str, str]] = Field(default_factory=dict, description="Headers HTTP custom")
    costo_entrada: Optional[Decimal] = Field(None, ge=0, description="Costo por 1K tokens de entrada")
    costo_salida: Optional[Decimal] = Field(None, ge=0, description="Costo por 1K tokens de salida")
    limite_diario_tokens: Optional[int] = Field(None, ge=0, description="Límite diario de tokens")
    activo: bool = Field(default=True, description="¿Está activo el modelo?")
    fecha_expiracion_key: Optional[date] = Field(None, description="Fecha de expiración del API key")


class LLMMaestroCreate(LLMMaestroBase):
    """Schema para crear LLM Maestro"""
    pass


class LLMMaestroUpdate(BaseModel):
    """Schema para actualizar LLM Maestro (campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    proveedor: Optional[ProveedorLLM] = None
    modelo_id: Optional[str] = Field(None, min_length=3, max_length=100)
    url_api: Optional[str] = Field(None, min_length=10, max_length=500)
    api_key: Optional[str] = Field(None, min_length=10)
    version: Optional[str] = Field(None, max_length=50)
    configuracion: Optional[Dict[str, Any]] = None
    headers_adicionales: Optional[Dict[str, str]] = None
    costo_entrada: Optional[Decimal] = Field(None, ge=0)
    costo_salida: Optional[Decimal] = Field(None, ge=0)
    limite_diario_tokens: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None
    fecha_expiracion_key: Optional[date] = None


class LLMMaestro(LLMMaestroBase):
    """Schema completo de LLM Maestro (sin api_key por seguridad)"""
    id: int
    tokens_usados_hoy: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Excluir api_key de la respuesta por seguridad
    api_key: str = Field(default="***HIDDEN***", description="API Key oculta")
    
    class Config:
        from_attributes = True


class LLMMaestroConKey(LLMMaestro):
    """Schema con API Key visible (solo para admin)"""
    api_key: str  # Sobrescribe para mostrar el valor real
    
    class Config:
        from_attributes = True


# ==================== PROMPT MAESTRO ====================

class PromptMaestroBase(BaseModel):
    """Schema base para Prompt Maestro"""
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del prompt")
    descripcion: Optional[str] = Field(None, description="Descripción del prompt")
    # contenido eliminado: ahora los items contienen los archivos/fragmentos
    variables: Optional[List[str]] = Field(default_factory=list, description="Lista de variables usadas")
    ejemplos: Optional[str] = Field(None, description="Ejemplos de uso")
    activo: bool = Field(default=True, description="¿Está activo el prompt?")
    items: Optional[List['PromptItem']] = Field(default_factory=list, description="Lista de items asociados")


class PromptItem(BaseModel):
    id: Optional[int] = None
    nombre_archivo: str
    contenido: Optional[str] = None
    orden: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PromptMaestroCreate(PromptMaestroBase):
    """Schema para crear Prompt Maestro"""
    pass


class PromptMaestroUpdate(BaseModel):
    """Schema para actualizar Prompt Maestro (campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = None
    # contenido eliminado
    variables: Optional[List[str]] = None
    ejemplos: Optional[str] = None
    activo: Optional[bool] = None
    items: Optional[List[PromptItem]] = Field(default_factory=list, description="Lista de items asociados")


class PromptMaestro(PromptMaestroBase):
    """Schema completo de Prompt Maestro"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: Optional[List[PromptItem]] = Field(default_factory=list, description="Lista de items asociados")
    
    class Config:
        from_attributes = True


# ==================== ESTILO MAESTRO ====================

class EstiloItemBase(BaseModel):
    """Schema base para EstiloItem"""
    nombre_archivo: str = Field(..., description="Nombre del archivo")
    contenido: Optional[str] = Field(None, description="Contenido del archivo")
    orden: int = Field(default=1, description="Orden de procesamiento")

class EstiloItemCreate(EstiloItemBase):
    """Schema para crear EstiloItem"""
    estilo_id: int = Field(..., description="ID del estilo al que pertenece")

class EstiloItemUpdate(EstiloItemBase):
    """Schema para actualizar EstiloItem"""
    estilo_id: Optional[int] = None
    nombre_archivo: Optional[str] = None
    contenido: Optional[str] = None
    orden: Optional[int] = None

class EstiloItem(EstiloItemBase):
    """Schema para EstiloItem"""
    id: int
    estilo_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EstiloMaestroBase(BaseModel):
    """Schema base para Estilo Maestro"""
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del estilo")
    descripcion: Optional[str] = Field(None, description="Descripción del estilo")
    tipo_estilo: Optional[TipoEstilo] = Field(None, description="Tipo de estilo")
    configuracion: Dict[str, Any] = Field(..., description="Configuración del estilo (JSON)")
    ejemplos: Optional[str] = Field(None, description="Ejemplos del estilo")
    activo: bool = Field(default=True, description="¿Está activo el estilo?")
    items: Optional[List[EstiloItem]] = Field(default_factory=list, description="Lista de items asociados")
    
    @validator('configuracion')
    def validate_configuracion(cls, v):
        """Validar que configuración no esté vacía"""
        if not v:
            raise ValueError('La configuración no puede estar vacía')
        return v


class EstiloMaestroCreate(EstiloMaestroBase):
    """Schema para crear Estilo Maestro"""
    pass


class EstiloMaestroUpdate(BaseModel):
    """Schema para actualizar Estilo Maestro (campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100, description="Nombre del estilo")
    descripcion: Optional[str] = Field(None, description="Descripción del estilo")
    tipo_estilo: Optional[TipoEstilo] = Field(None, description="Tipo de estilo: tono, formato, estructura, longitud")
    configuracion: Optional[Dict[str, Any]] = Field(
        None,
        description="Configuración del estilo en formato JSON",
        example={"tono": "periodistico", "enfasis": "local"}
    )
    ejemplos: Optional[str] = Field(None, description="Ejemplos de uso del estilo")
    activo: Optional[bool] = Field(None, description="Estado del estilo")
    items: Optional[List[EstiloItemBase]] = Field(
        default_factory=list,
        description="Lista de items asociados",
        example=[{
            "nombre_archivo": "ejemplo.txt",
            "contenido": "Contenido del archivo",
            "orden": 1
        }]
    )


class EstiloMaestro(EstiloMaestroBase):
    """Schema completo de Estilo Maestro"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== SECCION ====================

class SeccionBase(BaseModel):
    """Schema base para Sección"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la sección")
    descripcion: Optional[str] = Field(None, description="Descripción de la sección")
    color: str = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$", description="Color HEX")
    icono: str = Field(default="newspaper", max_length=50, description="Nombre del icono Lucide")
    prompt_id: Optional[int] = Field(None, description="ID del prompt asociado")
    estilo_id: Optional[int] = Field(None, description="ID del estilo asociado")
    activo: bool = Field(default=True, description="¿Está activa la sección?")


class SeccionCreate(SeccionBase):
    """Schema para crear Sección"""
    pass


class SeccionUpdate(BaseModel):
    """Schema para actualizar Sección (campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icono: Optional[str] = Field(None, max_length=50)
    prompt_id: Optional[int] = None
    estilo_id: Optional[int] = None
    activo: Optional[bool] = None


class Seccion(SeccionBase):
    """Schema completo de Sección"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SeccionConRelaciones(Seccion):
    """Schema de Sección con relaciones cargadas"""
    prompt: Optional[PromptMaestro] = None
    estilo: Optional[EstiloMaestro] = None


# ==================== SALIDA MAESTRO ====================

class SalidaMaestroBase(BaseModel):
    """Schema base para Salida Maestro"""
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre de la salida")
    descripcion: Optional[str] = Field(None, description="Descripción de la salida")
    tipo_salida: TipoSalida = Field(..., description="Tipo de salida (print/digital/social)")
    configuracion: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Configuración específica")
    activo: bool = Field(default=True, description="¿Está activa la salida?")


class SalidaMaestroCreate(SalidaMaestroBase):
    """Schema para crear Salida Maestro"""
    pass


class SalidaMaestroUpdate(BaseModel):
    """Schema para actualizar Salida Maestro (campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    descripcion: Optional[str] = None
    tipo_salida: Optional[TipoSalida] = None
    configuracion: Optional[Dict[str, Any]] = None
    activo: Optional[bool] = None


class SalidaMaestro(SalidaMaestroBase):
    """Schema completo de Salida Maestro"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== NOTICIA SALIDA ====================

class NoticiaSalidaBase(BaseModel):
    """Schema base para Noticia-Salida"""
    noticia_id: int = Field(..., description="ID de la noticia")
    salida_id: int = Field(..., description="ID de la salida")
    titulo: str = Field(..., min_length=5, max_length=200, description="Título de la salida")
    contenido_generado: str = Field(..., min_length=10, description="Contenido generado para esta salida")
    tokens_usados: Optional[int] = Field(None, ge=0, description="Tokens consumidos")
    tiempo_generacion_ms: Optional[int] = Field(None, ge=0, description="Tiempo de generación en ms")


class NoticiaSalidaCreate(NoticiaSalidaBase):
    """Schema para crear Noticia-Salida"""
    pass


class NoticiaSalidaUpdate(BaseModel):
    """Schema para actualizar Noticia-Salida (campos opcionales)"""
    titulo: Optional[str] = Field(None, min_length=5, max_length=200)
    contenido_generado: Optional[str] = Field(None, min_length=10)
    tokens_usados: Optional[int] = Field(None, ge=0)
    tiempo_generacion_ms: Optional[int] = Field(None, ge=0)


class NoticiaSalida(NoticiaSalidaBase):
    """Schema completo de Noticia-Salida"""
    id: int
    generado_en: datetime
    nombre_salida: Optional[str] = None  # <-- Añadido para serializar el nombre
    class Config:
        from_attributes = True


class NoticiaSalidaConRelaciones(NoticiaSalida):
    """Schema de Noticia-Salida con relaciones cargadas"""
    salida: Optional[SalidaMaestro] = None


# ==================== GENERACIÓN IA ====================

class GenerarSalidasRequest(BaseModel):
    """Request para generar salidas de una noticia"""
    noticia_id: int = Field(..., description="ID de la noticia")
    salidas_ids: List[int] = Field(..., min_items=1, description="IDs de las salidas a generar")
    llm_id: int = Field(..., description="ID del LLM a usar")
        # prompt_id y estilo_id eliminados: ahora se heredan siempre de la sección
    regenerar: bool = Field(default=False, description="¿Regenerar si ya existe?")


class GenerarSalidasResponse(BaseModel):
    """Response de generación de salidas"""
    noticia_id: int
    salidas_generadas: List[NoticiaSalida]
    total_tokens: int
    tiempo_total_ms: int
    errores: List[str] = []


# ==================== ESTADÍSTICAS ====================

class EstadisticasLLM(BaseModel):
    """Estadísticas de uso de LLM"""
    llm_id: int
    nombre: str
    total_generaciones: int
    tokens_totales: int
    costo_estimado: Optional[Decimal] = None
    tiempo_promedio_ms: Optional[int] = None


class EstadisticasSalidas(BaseModel):
    """Estadísticas de salidas generadas"""
    salida_id: int
    nombre: str
    total_generadas: int
    noticias_unicas: int
    tokens_promedio: Optional[int] = None
