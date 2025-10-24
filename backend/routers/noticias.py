"""
Router de Noticias - Endpoints CRUD con PostgreSQL y Autenticación
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core.database import get_db
from models import orm_models
from models.schemas import (
    Noticia, 
    NoticiaCreate, 
    NoticiaUpdate, 
    ResponseModel,
    EstadisticasResponse
)
from routers.auth import get_current_user, get_current_active_user

router = APIRouter()


def verificar_permiso_noticia(
    noticia: orm_models.Noticia,
    usuario: orm_models.Usuario
) -> bool:
    """
    Verificar si el usuario tiene permiso para modificar la noticia
    - Admin: puede todo
    - Editor: solo sus propias noticias
    - Viewer: nada
    """
    if usuario.role == 'admin':
        return True
    
    if usuario.role == 'editor' and noticia.usuario_id == usuario.id:
        return True
    
    return False


# ==================== ENDPOINTS PÚBLICOS (SIN AUTH) ====================


@router.get("/", response_model=List[Noticia])
async def listar_noticias(
    seccion_id: Optional[int] = None,
    proyecto_id: Optional[int] = None,
    estado: Optional[str] = None,  # Nuevo filtro
    limite: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Listar todas las noticias con filtros opcionales
    
    📖 Endpoint PÚBLICO - No requiere autenticación
    
    **Filtros disponibles:**
    - seccion_id: Filtrar por sección de noticia
    - proyecto_id: Filtrar noticias de un proyecto específico
    - estado: Filtrar por estado ('activo', 'archivado', etc)
    """
    query = db.query(orm_models.Noticia)
    if seccion_id:
        query = query.filter(orm_models.Noticia.seccion_id == seccion_id)
    if proyecto_id:
        query = query.filter(orm_models.Noticia.proyecto_id == proyecto_id)
    if estado:
        query = query.filter(orm_models.Noticia.estado == estado)
    # Ordenar por fecha más reciente
    query = query.order_by(orm_models.Noticia.created_at.desc())
    noticias = query.offset(offset).limit(limite).all()
    return [n.to_dict() for n in noticias]


@router.get("/{noticia_id}")
async def obtener_noticia(noticia_id: int, db: Session = Depends(get_db)):
    """
    Obtener una noticia específica por ID
    
    📖 Endpoint PÚBLICO - No requiere autenticación
    """
    noticia = db.query(orm_models.Noticia).filter(
        orm_models.Noticia.id == noticia_id
    ).first()
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noticia con ID {noticia_id} no encontrada"
        )
    # Buscar todas las salidas asociadas
    salidas_ids = [rel.salida_id for rel in db.query(orm_models.NoticiaSalida).filter_by(noticia_id=noticia_id)]
    data = noticia.to_dict()
    data['salidas_ids'] = salidas_ids
    return data



@router.get("/stats/resumen", response_model=EstadisticasResponse)
async def obtener_estadisticas(db: Session = Depends(get_db)):
    """
    Obtener estadísticas generales del sistema
    
    📖 Endpoint PÚBLICO - No requiere autenticación
    """
    noticias = db.query(orm_models.Noticia).all()
    # Contar noticias por sección
    secciones_count = {}
    for noticia in noticias:
        sec = noticia.seccion_id
        secciones_count[sec] = secciones_count.get(sec, 0) + 1
    # Contar noticias con análisis IA
    noticias_ia = sum(1 for n in noticias if n.resumen_ia)
    # Últimas 5 noticias
    ultimas = db.query(orm_models.Noticia).order_by(
        orm_models.Noticia.created_at.desc()
    ).limit(5).all()
    ultimas_titulos = [n.titulo for n in ultimas]
    return EstadisticasResponse(
        total_noticias=len(noticias),
        noticias_por_seccion=secciones_count,
        noticias_con_ia=noticias_ia,
        ultimas_actualizaciones=ultimas_titulos
    )


# ==================== ENDPOINTS PROTEGIDOS (CON AUTH) ====================

@router.post("/", response_model=Noticia, status_code=status.HTTP_201_CREATED)
async def crear_noticia(
    noticia: NoticiaCreate,
    current_user: orm_models.Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear una nueva noticia
    
    🔒 Requiere autenticación
    👤 Roles permitidos: admin, editor
    """
    # Verificar permisos
    if current_user.role not in ['admin', 'editor']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo admin y editor pueden crear noticias"
        )
    
    # Validar que el proyecto exista si se proporciona proyecto_id
    if noticia.proyecto_id:
        proyecto = db.query(orm_models.Proyecto).filter(
            orm_models.Proyecto.id == noticia.proyecto_id
        ).first()
        
        if not proyecto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proyecto con ID {noticia.proyecto_id} no encontrado"
            )
    
    # Crear noticia vinculada al usuario y opcionalmente al proyecto
    nueva_noticia = orm_models.Noticia(
        titulo=noticia.titulo,
        contenido=noticia.contenido,
        seccion_id=noticia.seccion_id,
        autor=noticia.autor,
        usuario_id=current_user.id,  # Vincular con el usuario
        proyecto_id=noticia.proyecto_id,  # Vincular con proyecto (opcional)
        llm_id=noticia.llm_id,
        estado=noticia.estado if hasattr(noticia, 'estado') and noticia.estado else 'activo'
    )
    db.add(nueva_noticia)
    db.commit()
    db.refresh(nueva_noticia)
    # Asociar salidas si se envían
    if getattr(noticia, 'salidas_ids', None):
        for salida_id in noticia.salidas_ids:
            rel = orm_models.NoticiaSalida(
                noticia_id=nueva_noticia.id,
                salida_id=salida_id,
                titulo=nueva_noticia.titulo,
                contenido_generado=""
            )
            db.add(rel)
        db.commit()
    # Devolver noticia con salidas asociadas
    salidas_ids = [rel.salida_id for rel in db.query(orm_models.NoticiaSalida).filter_by(noticia_id=nueva_noticia.id)]
    data = nueva_noticia.to_dict()
    data['salidas_ids'] = salidas_ids
    return data


@router.put("/{noticia_id}", response_model=Noticia)
async def actualizar_noticia(
    noticia_id: int, 
    noticia_update: NoticiaUpdate,
    current_user: orm_models.Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar una noticia existente
    
    🔒 Requiere autenticación
    👤 Permisos:
       - admin: puede editar cualquier noticia
       - editor: solo puede editar sus propias noticias
       - viewer: sin permisos
    """
    noticia = db.query(orm_models.Noticia).filter(
        orm_models.Noticia.id == noticia_id
    ).first()
    
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noticia con ID {noticia_id} no encontrada"
        )
    
    # Verificar permisos
    if not verificar_permiso_noticia(noticia, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta noticia"
        )
    
    # Actualizar solo campos no None
    update_data = noticia_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "proyecto_id":
            noticia.proyecto_id = value
        elif field == "estado":
            noticia.estado = value if value else noticia.estado
        else:
            setattr(noticia, field, value)
    # Actualizar salidas asociadas si se envía salidas_ids
    salidas_ids = update_data.get("salidas_ids")
    if salidas_ids is not None:
        # Eliminar relaciones actuales
        db.query(orm_models.NoticiaSalida).filter_by(noticia_id=noticia_id).delete()
        # Crear nuevas relaciones
        for salida_id in salidas_ids:
            rel = orm_models.NoticiaSalida(
                noticia_id=noticia_id,
                salida_id=salida_id,
                titulo=noticia.titulo,
                contenido_generado=""
            )
            db.add(rel)
        db.commit()
    db.commit()  # <--- Asegura que los cambios de estado y otros campos se guarden
    db.refresh(noticia)
    # Devolver noticia con salidas asociadas
    salidas_ids_resp = [rel.salida_id for rel in db.query(orm_models.NoticiaSalida).filter_by(noticia_id=noticia_id)]
    data = noticia.to_dict()
    data['salidas_ids'] = salidas_ids_resp
    return data


@router.delete("/{noticia_id}", response_model=ResponseModel)
async def eliminar_noticia(
    noticia_id: int,
    current_user: orm_models.Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una noticia por ID
    
    🔒 Requiere autenticación
    👤 Permisos:
       - admin: puede eliminar cualquier noticia
       - editor: solo puede eliminar sus propias noticias
       - viewer: sin permisos
    """
    noticia = db.query(orm_models.Noticia).filter(
        orm_models.Noticia.id == noticia_id
    ).first()
    
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noticia con ID {noticia_id} no encontrada"
        )
    
    # Verificar permisos
    if not verificar_permiso_noticia(noticia, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta noticia"
        )
    
    # Eliminar relaciones de salidas asociadas
    db.query(orm_models.NoticiaSalida).filter_by(noticia_id=noticia_id).delete()
    db.delete(noticia)
    db.commit()
    
    return ResponseModel(
        success=True,
        message=f"Noticia {noticia_id} eliminada correctamente"
    )


# ==================== ENDPOINTS DE DESARROLLO ====================

@router.post("/seed", response_model=ResponseModel)
async def crear_datos_ejemplo(db: Session = Depends(get_db)):
    """
    Crear datos de ejemplo para testing
    
    📖 Endpoint PÚBLICO (solo desarrollo)
    """
    # NOTA: Debes ajustar los IDs de sección según existan en tu base de datos
    datos_ejemplo = [
        {
            "titulo": "FastAPI supera a Flask en popularidad",
            "contenido": "Según las últimas estadísticas, FastAPI ha superado a Flask como el framework web más utilizado en Python para nuevos proyectos en 2025.",
            "seccion_id": 1,
            "autor": "Sistema"
        },
        {
            "titulo": "Claude 4 establece nuevo récord en benchmarks",
            "contenido": "El modelo Claude Sonnet 4.5 ha demostrado capacidades superiores en razonamiento y generación de código, superando modelos anteriores.",
            "seccion_id": 2,
            "autor": "Sistema"
        },
        {
            "titulo": "PostgreSQL 16 trae mejoras significativas",
            "contenido": "La nueva versión de PostgreSQL incluye mejoras en rendimiento, replicación lógica y nuevas funcionalidades para JSON.",
            "seccion_id": 3,
            "autor": "Sistema"
        }
    ]
    for dato in datos_ejemplo:
        noticia = orm_models.Noticia(**dato)
        db.add(noticia)
    db.commit()
    return ResponseModel(
        success=True,
        message=f"Se crearon {len(datos_ejemplo)} noticias de ejemplo",
        data={"total_noticias": db.query(orm_models.Noticia).count()}
    )
