"""
Modelos Pydantic para validación de datos
Schemas para requests y responses
"""
from pydantic import BaseModel, Field, validator, field_serializer
from typing import Optional, List, Union
from datetime import datetime, date
from enum import Enum

# ==================== ENUMS ====================


class TipoAnalisisIA(str, Enum):
    """Tipos de análisis con IA"""
    RESUMEN = "resumen"
    SENTIMENT = "sentiment"
    KEYWORDS = "keywords"
    TRADUCCION = "traduccion"

# ==================== NOTICIAS ====================

class NoticiaBase(BaseModel):
    """Schema base para noticias"""
    titulo: str = Field(..., min_length=5, max_length=200)
    contenido: str = Field(..., min_length=20)
    seccion_id: Optional[int] = Field(None, description="ID de la sección a la que pertenece la noticia")
    proyecto_id: Optional[int] = None  # Asociar a proyecto
    llm_id: Optional[int] = None  # Modelo LLM asociado
    estado: Optional[str] = Field('activo', description="Estado de la noticia: activo, archivado, eliminado")

class NoticiaCreate(NoticiaBase):
    """Schema para crear noticias"""
    salidas_ids: Optional[list[int]] = []
    proyecto_id: Optional[int] = None
    llm_id: Optional[int] = None
    estado: Optional[str] = Field('activo', description="Estado de la noticia: activo, archivado, eliminado")

class NoticiaUpdate(BaseModel):
    """Schema para actualizar noticias (campos opcionales)"""
    titulo: Optional[str] = Field(None, min_length=5, max_length=200)
    contenido: Optional[str] = Field(None, min_length=20)
    seccion_id: Optional[int] = None
    salidas_ids: Optional[list[int]] = []
    proyecto_id: Optional[int] = None
    llm_id: Optional[int] = None
    estado: Optional[str] = Field(None, description="Estado de la noticia: activo, archivado, eliminado")

class Noticia(NoticiaBase):
    """Schema completo de noticia con metadata"""
    id: int
    fecha: Union[datetime, str]  # Acepta datetime del ORM o string
    resumen_ia: Optional[str] = None
    sentiment_score: Optional[float] = None
    keywords: Optional[List[str]] = None
    usuario_id: Optional[int] = None
    llm_id: Optional[int] = None
    estado: Optional[str] = Field('activo', description="Estado de la noticia: activo, archivado, eliminado")
    
    @field_serializer('fecha')
    def serialize_fecha(self, fecha: Union[datetime, str]) -> str:
        """Serializa el campo fecha a string ISO format"""
        if isinstance(fecha, datetime):
            return fecha.strftime('%Y-%m-%d %H:%M:%S')
        return fecha
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

# ==================== IA / CHAT ====================

class MensajeChat(BaseModel):
    """Mensaje individual en conversación"""
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1)

class ChatRequest(BaseModel):
    """Request para chat con IA"""
    mensaje: str = Field(..., min_length=1, max_length=4000)
    conversacion_id: Optional[str] = None
    contexto: Optional[str] = None
    llm_id: Optional[int] = None

class ChatResponse(BaseModel):
    """Response del chat con IA"""
    respuesta: dict  # Dict con 'contenido', 'tokens_usados', 'tiempo_ms'
    conversacion_id: str
    tokens_usados: Optional[int] = None

# ==================== ANÁLISIS IA ====================

class AnalisisIARequest(BaseModel):
    """Request para análisis con IA"""
    noticia_id: int
    tipo_analisis: TipoAnalisisIA = TipoAnalisisIA.RESUMEN
    idioma_destino: Optional[str] = Field(None, pattern="^(es|en|fr|de|it|pt)$")

class AnalisisIAResponse(BaseModel):
    """Response de análisis con IA"""
    noticia_id: int
    tipo_analisis: TipoAnalisisIA
    resultado: str
    metadata: Optional[dict] = None

class ResumenIAResponse(BaseModel):
    """Response específico para resumen con IA"""
    noticia_id: int
    resumen: str
    puntos_clave: List[str]
    longitud_original: int
    longitud_resumen: int

# ==================== RESPUESTAS GENERALES ====================

class ResponseModel(BaseModel):
    """Response genérico para operaciones"""
    success: bool
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    """Response para errores"""
    detail: str
    error_code: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

# ==================== ESTADÍSTICAS ====================

class EstadisticasResponse(BaseModel):
    """Estadísticas del sistema"""
    total_noticias: int
    noticias_por_seccion: dict
    noticias_con_ia: int
    ultimas_actualizaciones: List[str]

# ==================== USUARIOS Y AUTENTICACIÓN ====================

class RoleEnum(str, Enum):
    """Roles de usuario disponibles con jerarquía editorial"""
    ADMIN = "admin"              # Acceso total al sistema
    DIRECTOR = "director"        # Director de redacción (ve todo editorial)
    JEFE_SECCION = "jefe_seccion"  # Jefe de sección (ve su equipo)
    REDACTOR = "redactor"        # Redactor (ve solo sus noticias)
    VIEWER = "viewer"            # Solo lectura

class UsuarioBase(BaseModel):
    """Schema base para usuarios"""
    email: str = Field(..., min_length=3, max_length=255)
    username: str = Field(..., min_length=3, max_length=50)
    nombre_completo: Optional[str] = Field(None, max_length=200)
    
    @validator('email')
    def validate_email(cls, v):
        """Validar formato de email"""
        if '@' not in v:
            raise ValueError('Email debe contener @')
        return v.lower()
    
    @validator('username')
    def validate_username(cls, v):
        """Validar username sin espacios"""
        if ' ' in v:
            raise ValueError('Username no puede contener espacios')
        return v.lower()

class UsuarioCreate(UsuarioBase):
    """Schema para crear usuario (con contraseña)"""
    password: str = Field(..., min_length=6, max_length=100)
    role: RoleEnum = RoleEnum.VIEWER
    supervisor_id: Optional[int] = None
    secciones_asignadas: Optional[List[int]] = Field(default_factory=list)
    limite_tokens_diario: Optional[int] = Field(10000, ge=1000, le=100000)
    fecha_expiracion_acceso: Optional[str] = None  # YYYY-MM-DD format
    
    @validator('password')
    def validate_password(cls, v):
        """Validar contraseña fuerte"""
        if len(v) < 6:
            raise ValueError('Contraseña debe tener al menos 6 caracteres')
        return v

class UsuarioUpdate(BaseModel):
    """Schema para actualizar usuario (campos opcionales)"""
    email: Optional[str] = Field(None, min_length=3, max_length=255)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    nombre_completo: Optional[str] = Field(None, max_length=200)
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None
    supervisor_id: Optional[int] = None
    secciones_asignadas: Optional[List[int]] = None
    limite_tokens_diario: Optional[int] = Field(None, ge=1000, le=100000)
    fecha_expiracion_acceso: Optional[str] = None

class Usuario(UsuarioBase):
    """Schema completo de usuario (sin contraseña)"""
    id: int
    role: RoleEnum
    is_active: bool
    is_superuser: bool
    supervisor_id: Optional[int] = None
    secciones_asignadas: List[int] = Field(default_factory=list)
    limite_tokens_diario: int = 10000
    fecha_expiracion_acceso: Optional[Union[str, datetime, date]] = None
    created_at: Union[str, datetime]
    last_login: Optional[Union[str, datetime]] = None
    
    @field_serializer('fecha_expiracion_acceso', when_used='always')
    def serialize_fecha_expiracion(self, value):
        if value is None:
            return None
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)
    
    @field_serializer('created_at', when_used='always')
    def serialize_created_at(self, value):
        if value is None:
            return None
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)
    
    @field_serializer('last_login', when_used='always')
    def serialize_last_login(self, value):
        if value is None:
            return None
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)
    
    class Config:
        from_attributes = True

class UsuarioExtendido(Usuario):
    """Schema extendido con información de jerarquía y métricas"""
    supervisor_nombre: Optional[str] = None
    subordinados_count: int = 0
    noticias_count: int = 0
    secciones_nombres: List[str] = Field(default_factory=list)
    puede_supervisar: bool = False
    nivel_jerarquico: int = 5

class UsuarioInDB(Usuario):
    """Schema de usuario con contraseña hasheada (uso interno)"""
    hashed_password: str

# ==================== AUTENTICACIÓN ====================

class LoginRequest(BaseModel):
    """Request para login"""
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    """Response con token JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos
    user: Usuario

class TokenData(BaseModel):
    """Datos extraídos del token JWT"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None

# ==================== PROYECTOS ====================

class EstadoProyecto(str, Enum):
    """Estados posibles de un proyecto"""
    ACTIVO = "activo"
    ARCHIVADO = "archivado"
    ELIMINADO = "eliminado"

class ProyectoBase(BaseModel):
    """Schema base para proyectos"""
    nombre: str = Field(..., min_length=3, max_length=200)
    descripcion: Optional[str] = None
    estado: EstadoProyecto = EstadoProyecto.ACTIVO

class ProyectoCreate(ProyectoBase):
    """Schema para crear proyecto"""
    pass

class ProyectoUpdate(BaseModel):
    """Schema para actualizar proyecto (campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = None
    estado: Optional[EstadoProyecto] = None

class Proyecto(ProyectoBase):
    """Schema completo de proyecto"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProyectoConNoticias(Proyecto):
    """Schema de proyecto con sus noticias asociadas"""
    noticias: List[Noticia] = []
    total_noticias: int = 0

class ProyectoStats(BaseModel):
    """Estadísticas de un proyecto"""
    total_noticias: int
    noticias_por_seccion: dict
    ultima_actualizacion: Optional[datetime] = None


# ================================
# Schemas de Métricas de Valor Periodístico
# ================================

class MetricasValorPeriodisticoBase(BaseModel):
    """Base para métricas de valor periodístico"""
    noticia_id: int
    tiempo_generacion_total: float
    tiempo_por_salida: Optional[dict] = {}
    tiempo_estimado_manual: int
    ahorro_tiempo_minutos: int
    tokens_total: int
    costo_generacion: float
    costo_estimado_manual: float
    ahorro_costo: float
    cantidad_salidas_generadas: int
    cantidad_formatos_diferentes: int
    velocidad_palabras_por_segundo: float
    adherencia_manual_estilo: Optional[float] = 0.95
    requiere_edicion_manual: Optional[bool] = False
    porcentaje_contenido_aprovechable: Optional[float] = 0.90
    modelo_usado: str
    usuario_id: Optional[int] = None
    tipo_noticia: Optional[str] = 'feature'
    complejidad_estimada: Optional[str] = 'media'
    engagement_promedio: Optional[float] = 0
    tiempo_en_tendencia: Optional[int] = 0
    roi_porcentaje: float

class MetricasValorPeriodisticoCreate(MetricasValorPeriodisticoBase):
    """Crear nueva métrica de valor periodístico"""
    pass

class MetricasValorPeriodisticoResponse(MetricasValorPeriodisticoBase):
    """Respuesta completa de métrica de valor periodístico"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MetricasValorResumen(BaseModel):
    """Resumen de métricas para mostrar en frontend - Solo Admin"""
    ahorro_tiempo_minutos: int
    ahorro_costo: float = Field(description="Ahorro en dólares vs proceso manual")
    costo_generacion: float
    costo_estimado_manual: float
    cantidad_formatos: int
    roi_porcentaje: float
    velocidad_palabras_por_segundo: float
    eficiencia_temporal: float = Field(description="Porcentaje de eficiencia temporal")
    porcentaje_contenido_aprovechable: float = Field(default=0.90, description="Calidad del contenido IA")
    tokens_total: int = Field(description="Total de tokens utilizados")
    modelo_usado: str
    tiempo_total_segundos: float