"""
Modelos ORM con SQLAlchemy
Define la estructura de las tablas en PostgreSQL
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Table, JSON, Boolean, DECIMAL, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from core.database import Base




class Proyecto(Base):
    """
    Modelo de Proyecto
    Agrupa noticias y documentos contextuales
    """
    __tablename__ = 'proyectos'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(50), default='activo')  # activo, archivado, eliminado
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    noticias = relationship('Noticia', back_populates='proyecto')
    documentos = relationship('DocumentoContexto', back_populates='proyecto', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}')>"


class Noticia(Base):
    """
    Modelo de Noticia
    Entidad principal del sistema
    """
    __tablename__ = 'noticias'
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False, index=True)
    contenido = Column(Text, nullable=False)
    seccion_id = Column(Integer, ForeignKey('seccion.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Campos IA
    resumen_ia = Column(Text, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    keywords = Column(JSON, nullable=True)  # Lista de strings
    
    # Metadata
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Estado de la noticia
    estado = Column(String(50), default='activo', index=True)  # activo, archivado, eliminado
    
    # Foreign Keys
    proyecto_id = Column(Integer, ForeignKey('proyectos.id', ondelete='SET NULL'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=False)  # Requerido para integridad
    llm_id = Column(Integer, ForeignKey('llm_maestro.id', ondelete='SET NULL'), nullable=True)

    # Relaciones
    proyecto = relationship('Proyecto', back_populates='noticias')
    usuario_creador = relationship('Usuario', back_populates='noticias', foreign_keys=[usuario_id])
    seccion = relationship('Seccion')
    llm = relationship('LLMMaestro')
    
    def __repr__(self):
        return f"<Noticia(id={self.id}, titulo='{self.titulo[:30]}...')>"
    
    @property
    def autor_nombre(self):
        """Obtener username del autor desde la relación usuario_creador"""
        if self.usuario_creador:
            return self.usuario_creador.username
        return 'Sin autor'
    
    @property 
    def autor_id(self):
        """Alias para usuario_id para compatibilidad"""
        return self.usuario_id
    
    def to_dict(self):
        """Convertir a diccionario usando usuario_id como fuente de verdad"""
        try:
            autor_nombre = self.autor_nombre  # Usa la propiedad que maneja la relación
        except:
            autor_nombre = 'Sin autor'  # Fallback
        
        return {
            'id': self.id,
            'titulo': self.titulo,
            'contenido': self.contenido,
            'seccion_id': self.seccion_id,
            'autor_nombre': autor_nombre,  # Solo nombre desde relación
            'resumen_ia': self.resumen_ia,
            'sentiment_score': self.sentiment_score,
            'keywords': self.keywords,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S') if self.fecha else None,
            'proyecto_id': self.proyecto_id,
            'usuario_id': self.usuario_id,  # Fuente de verdad para filtros
            'llm_id': self.llm_id,
            'estado': self.estado
        }


class DocumentoContexto(Base):
    """
    Documentos vinculados a proyectos
    Pueden ser .txt, .pdf, .docx, etc.
    """
    __tablename__ = 'documentos_contexto'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)  # txt, pdf, docx, imagen, video, audio, url
    ruta_archivo = Column(String(500), nullable=True)  # Path en filesystem
    url = Column(String(1000), nullable=True)  # Si es un link externo
    contenido_extraido = Column(Text, nullable=True)  # Texto extraído del archivo
    metadatos = Column(JSON, nullable=True)  # Info adicional (tamaño, duración, etc)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    proyecto_id = Column(Integer, ForeignKey('proyectos.id', ondelete='CASCADE'), nullable=False)
    
    # Relaciones
    proyecto = relationship('Proyecto', back_populates='documentos')
    
    def __repr__(self):
        return f"<DocumentoContexto(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}')>"


class Usuario(Base):
    """
    Modelo de Usuario
    Sistema de autenticación y autorización con jerarquía editorial
    """
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    nombre_completo = Column(String(200), nullable=True)
    
    # Roles y permisos
    role = Column(String(20), default='viewer', nullable=False)  # admin, director, jefe_seccion, redactor, viewer
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    puede_ver_metricas = Column(Boolean, default=False, nullable=False)  # Permiso para ver métricas
    puede_ver_metricas = Column(Boolean, default=False, nullable=False)  # Permiso individual para ver métricas
    
    # Jerarquía editorial
    supervisor_id = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True, index=True)
    secciones_asignadas = Column(JSON, default=[], nullable=False)  # Lista de IDs de secciones
    limite_tokens_diario = Column(Integer, default=10000, nullable=False)
    fecha_expiracion_acceso = Column(Date, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    noticias = relationship('Noticia', back_populates='usuario_creador', foreign_keys='Noticia.usuario_id')
    
    # Relaciones jerárquicas
    supervisor = relationship('Usuario', remote_side=[id], back_populates='subordinados')
    subordinados = relationship('Usuario', back_populates='supervisor')
    # Relaciones jerárquicas
    supervisor = relationship('Usuario', remote_side=[id], back_populates='subordinados')
    subordinados = relationship('Usuario', back_populates='supervisor')
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def puede_supervisar(self):
        """Determina si el usuario puede supervisar a otros"""
        return self.role in ['admin', 'director', 'jefe_seccion', 'editor']
    
    @property
    def nivel_jerarquico(self):
        """Nivel en la jerarquía editorial (1=admin, 2=director, 3=jefe/editor, 4=redactor, 5=viewer)"""
        nivel_map = {
            'admin': 1,
            'director': 2, 
            'jefe_seccion': 3,
            'editor': 3,
            'redactor': 4,
            'viewer': 5
        }
        return nivel_map.get(self.role, 5)
    
    def puede_acceder_usuario(self, target_user):
        """Determina si puede ver/editar información de otro usuario"""
        # Admin ve todo
        if self.role == 'admin':
            return True
        # Director ve todo editorial
        if self.role == 'director' and target_user.role != 'admin':
            return True
        # Jefe de sección ve su equipo
        if self.role == 'jefe_seccion':
            return target_user.supervisor_id == self.id or target_user.id == self.id
        # Redactor solo se ve a sí mismo
        return target_user.id == self.id
    
    def get_usuarios_accesibles(self, db_session):
        """Obtiene lista de usuarios que puede ver según jerarquía"""
        if self.role == 'admin':
            return db_session.query(Usuario).all()
        elif self.role == 'director':
            return db_session.query(Usuario).filter(Usuario.role != 'admin').all()
        elif self.role == 'jefe_seccion':
            return db_session.query(Usuario).filter(
                (Usuario.supervisor_id == self.id) | (Usuario.id == self.id)
            ).all()
        else:
            return [self]


class ConversacionIA(Base):
    """
    Historial de conversaciones con IA
    Para persistir chats entre sesiones
    """
    __tablename__ = 'conversaciones_ia'
    
    id = Column(Integer, primary_key=True, index=True)
    conversacion_id = Column(String(100), unique=True, index=True, nullable=False)
    mensajes = Column(JSON, nullable=False)  # Lista de {role, content}
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<ConversacionIA(id={self.id}, conversacion_id='{self.conversacion_id}')>"


# ============================================
# FASE 6: NUEVOS MODELOS - SISTEMA DE MAESTROS
# ============================================

class LLMMaestro(Base):
    """
    Maestro de Modelos LLM
    Configura diferentes proveedores de IA (Claude, GPT-4, Gemini)
    """
    __tablename__ = 'llm_maestro'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    proveedor = Column(String(50), nullable=False, index=True)  # Anthropic, OpenAI, Google
    modelo_id = Column(String(100), nullable=False)  # claude-sonnet-4-20250514
    url_api = Column(String(500), nullable=False)
    api_key = Column(Text, nullable=False)  # Encriptada
    version = Column(String(50), nullable=True)
    
    # Configuración adicional
    configuracion = Column(JSON, default={})  # Parámetros del modelo
    headers_adicionales = Column(JSON, default={})  # Headers HTTP custom
    
    # Costos y límites
    costo_entrada = Column(DECIMAL(10, 6), nullable=True)  # Costo por 1K tokens entrada
    costo_salida = Column(DECIMAL(10, 6), nullable=True)  # Costo por 1K tokens salida
    limite_diario_tokens = Column(Integer, nullable=True)
    tokens_usados_hoy = Column(Integer, default=0)
    
    # Estado
    activo = Column(Boolean, default=True, index=True)
    fecha_expiracion_key = Column(Date, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

    
    def __repr__(self):
        return f"<LLMMaestro(id={self.id}, nombre='{self.nombre}', proveedor='{self.proveedor}')>"


class PromptMaestro(Base):
    """
    Maestro de Prompts
    Plantillas de prompts reutilizables con variables
    """
    __tablename__ = 'prompt_maestro'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    # categoria eliminado
    # contenido eliminado: ahora los items contienen los archivos/fragmentos
    variables = Column(JSON, default=[])  # Lista de variables: ['contenido', 'tema']
    ejemplos = Column(Text, nullable=True)
    
    # Estado
    activo = Column(Boolean, default=True, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    secciones = relationship('Seccion', back_populates='prompt')
    items = relationship('PromptItem', back_populates='prompt', cascade='all, delete-orphan')

class PromptItem(Base):
    """
    Item asociado a un PromptMaestro (ej: archivo de sección)
    """
    __tablename__ = 'prompt_item'
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey('prompt_maestro.id', ondelete='CASCADE'), nullable=False, index=True)
    nombre_archivo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=True)  # Texto extenso del prompt
    orden = Column(Integer, nullable=False, default=1)
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Relaciones
    prompt = relationship('PromptMaestro', back_populates='items')
    
    def __repr__(self):
        return f"<PromptMaestro(id={self.id}, nombre='{self.nombre}')>"


class EstiloMaestro(Base):
    """
    Maestro de Estilos
    Define directivas de tono, formato y estructura
    """
    __tablename__ = 'estilo_maestro'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    tipo_estilo = Column(String(50), nullable=True, index=True)  # tono, formato, estructura
    configuracion = Column(JSON, nullable=False)  # {"tono": "formal", "persona": "tercera"}
    ejemplos = Column(Text, nullable=True)
    
    # Estado
    activo = Column(Boolean, default=True, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    secciones = relationship('Seccion', back_populates='estilo')
    items = relationship('EstiloItem', back_populates='estilo', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<EstiloMaestro(id={self.id}, nombre='{self.nombre}')>"


class EstiloItem(Base):
    """
    Item asociado a un EstiloMaestro
    Contiene fragmentos de configuración o reglas de estilo
    """
    __tablename__ = 'estilo_item'
    
    id = Column(Integer, primary_key=True, index=True)
    estilo_id = Column(Integer, ForeignKey('estilo_maestro.id', ondelete='CASCADE'), nullable=False, index=True)
    nombre_archivo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=True)
    orden = Column(Integer, nullable=False, default=1)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    estilo = relationship('EstiloMaestro', back_populates='items')
    
    def __repr__(self):
        return f"<EstiloItem(id={self.id}, nombre_archivo='{self.nombre_archivo}')>"


class Seccion(Base):
    """
    Secciones (reemplazo de categorías)
    Agrupa noticias con configuración de prompts y estilos
    """
    __tablename__ = 'seccion'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    color = Column(String(7), default='#3B82F6')  # HEX color
    icono = Column(String(50), default='newspaper')  # Lucide icon name
    
    # Relaciones con maestros
    prompt_id = Column(Integer, ForeignKey('prompt_maestro.id', ondelete='SET NULL'), nullable=True, index=True)
    estilo_id = Column(Integer, ForeignKey('estilo_maestro.id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Estado
    activo = Column(Boolean, default=True, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    prompt = relationship('PromptMaestro', back_populates='secciones')
    estilo = relationship('EstiloMaestro', back_populates='secciones')
    
    def __repr__(self):
        return f"<Seccion(id={self.id}, nombre='{self.nombre}')>"


class SalidaMaestro(Base):
    """
    Maestro de Salidas
    Define canales de publicación (impreso, web, redes sociales)
    """
    __tablename__ = 'salida_maestro'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    tipo_salida = Column(String(50), nullable=False, index=True)  # print, digital, social
    configuracion = Column(JSON, default={})  # {"max_caracteres": 280, "hashtags": 3}
    
    # Estado
    activo = Column(Boolean, default=True, index=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    noticias_salidas = relationship('NoticiaSalida', back_populates='salida')
    
    def __repr__(self):
        return f"<SalidaMaestro(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo_salida}')>"


class NoticiaSalida(Base):
    """
    Relación Many-to-Many entre Noticias y Salidas
    Almacena el contenido generado para cada salida
    """
    __tablename__ = 'noticia_salida'
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    noticia_id = Column(Integer, ForeignKey('noticias.id', ondelete='CASCADE'), nullable=False, index=True)
    salida_id = Column(Integer, ForeignKey('salida_maestro.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Título y contenido generado
    titulo = Column(String(200), nullable=False, default="")
    contenido_generado = Column(Text, nullable=False)
    
    # Metadatos de generación
    
    # Estadísticas
    tokens_usados = Column(Integer, nullable=True)
    tiempo_generacion_ms = Column(Integer, nullable=True)
    
    # Metadata
    generado_en = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    noticia = relationship('Noticia', backref='salidas')
    salida = relationship('SalidaMaestro', back_populates='noticias_salidas')
    
    def __repr__(self):
        return f"<NoticiaSalida(noticia_id={self.noticia_id}, salida_id={self.salida_id}, titulo='{self.titulo[:30]}...')>"


class MetricasValorPeriodistico(Base):
    """
    Métricas de valor y ROI de la IA en el proceso periodístico
    Solo accesible para administradores del sistema
    """
    __tablename__ = 'metricas_valor_periodistico'
    
    id = Column(Integer, primary_key=True, index=True)
    noticia_id = Column(Integer, ForeignKey('noticias.id', ondelete='CASCADE'), nullable=True, index=True)  # Ahora nullable
    # Eliminado: session_id, ya no se usa para métricas temporales
    
    # Métricas de Eficiencia Temporal
    tiempo_generacion_total = Column(Numeric(8, 3), nullable=False)  # segundos totales
    tiempo_por_salida = Column(JSON, default={})  # {"web": 2.3, "twitter": 1.1}
    tiempo_estimado_manual = Column(Integer, nullable=False)  # minutos manual
    ahorro_tiempo_minutos = Column(Integer, nullable=False)  # ahorro vs manual
    
    # Métricas de Costo
    tokens_total = Column(Integer, nullable=False)
    costo_generacion = Column(Numeric(10, 4), nullable=False)  # USD
    costo_estimado_manual = Column(Numeric(10, 2), nullable=False)  # USD manual
    ahorro_costo = Column(Numeric(10, 2), nullable=False)  # diferencia
    
    # Métricas de Productividad
    cantidad_salidas_generadas = Column(Integer, nullable=False)
    cantidad_formatos_diferentes = Column(Integer, nullable=False)
    velocidad_palabras_por_segundo = Column(Numeric(8, 2), nullable=False)
    
    # Métricas de Calidad
    adherencia_manual_estilo = Column(Numeric(3, 2), default=0.95)  # 0.0 a 1.0
    requiere_edicion_manual = Column(Boolean, default=False)
    porcentaje_contenido_aprovechable = Column(Numeric(3, 2), default=0.90)
    
    # Contexto del Proceso
    modelo_usado = Column(String(100), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True, index=True)
    tipo_noticia = Column(String(50), default='feature', index=True)
    complejidad_estimada = Column(String(20), default='media')
    
    # Resultados de Negocio
    engagement_promedio = Column(Numeric(8, 2), default=0)
    tiempo_en_tendencia = Column(Integer, default=0)
    roi_porcentaje = Column(Numeric(8, 2), nullable=False)  # ROI calculado
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relaciones
    noticia = relationship('Noticia', backref='metricas_valor')
    usuario = relationship('Usuario')
    
    def __repr__(self):
        return f"<MetricasValor(id={self.id}, noticia_id={self.noticia_id}, roi={self.roi_porcentaje}%)>"
