"""
Router de Proyectos
Gestiona CRUD completo de proyectos con relaciones a noticias
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from core.database import get_db
from models import orm_models
from models.schemas import (
    Proyecto,
    ProyectoCreate,
    ProyectoUpdate,
    ProyectoConNoticias,
    ProyectoStats,
    EstadoProyecto
)
from routers.auth import get_current_active_user

router = APIRouter(prefix="/api/proyectos", tags=["proyectos"])


@router.post("/", response_model=Proyecto, status_code=status.HTTP_201_CREATED)
async def crear_proyecto(
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Crear un nuevo proyecto.
    Requiere autenticación.
    """
    # Verificar que el usuario tenga permisos (editor o admin)
    if current_user.role not in ['editor', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear proyectos"
        )
    
    # Crear proyecto
    db_proyecto = orm_models.Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        estado='activo',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto


@router.get("/", response_model=List[Proyecto])
async def listar_proyectos(
    estado: Optional[str] = 'activo',
    limite: int = 100,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Listar proyectos con filtros opcionales.
    
    Parámetros:
    - estado: 'activo', 'archivado', 'eliminado' (default: 'activo')
    - limite: número máximo de resultados (default: 100)
    """
    query = db.query(orm_models.Proyecto)
    
    # Filtrar por estado si se especifica
    if estado:
        query = query.filter(orm_models.Proyecto.estado == estado)
    
    # Ordenar por fecha de actualización descendente
    query = query.order_by(orm_models.Proyecto.updated_at.desc())
    
    # Limitar resultados
    proyectos = query.limit(limite).all()
    
    return proyectos


@router.get("/{proyecto_id}", response_model=ProyectoConNoticias)
async def obtener_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Obtener un proyecto específico con sus noticias relacionadas.
    """
    proyecto = db.query(orm_models.Proyecto).filter(
        orm_models.Proyecto.id == proyecto_id
    ).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    return proyecto


@router.put("/{proyecto_id}", response_model=Proyecto)
async def actualizar_proyecto(
    proyecto_id: int,
    proyecto_update: ProyectoUpdate,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Actualizar un proyecto existente.
    Requiere permisos de editor o admin.
    """
    # Verificar permisos
    if current_user.role not in ['editor', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar proyectos"
        )
    
    # Buscar proyecto
    db_proyecto = db.query(orm_models.Proyecto).filter(
        orm_models.Proyecto.id == proyecto_id
    ).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Actualizar campos
    update_data = proyecto_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_proyecto, key, value)
    
    db_proyecto.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto


@router.delete("/{proyecto_id}")
async def eliminar_proyecto(
    proyecto_id: int,
    permanente: bool = False,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Eliminar un proyecto.
    
    Parámetros:
    - permanente: si es True, elimina de la BD. Si es False, marca como eliminado (soft delete)
    
    Solo admins pueden hacer eliminación permanente.
    """
    # Buscar proyecto
    db_proyecto = db.query(orm_models.Proyecto).filter(
        orm_models.Proyecto.id == proyecto_id
    ).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    if permanente:
        # Eliminación permanente - solo admin
        if current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden eliminar proyectos permanentemente"
            )
        
        # Desvincular noticias asociadas (establecer proyecto_id a NULL)
        db.query(orm_models.Noticia).filter(
            orm_models.Noticia.proyecto_id == proyecto_id
        ).update({"proyecto_id": None})
        
        # Eliminar proyecto
        db.delete(db_proyecto)
        db.commit()
        
        return {"message": "Proyecto eliminado permanentemente"}
    else:
        # Soft delete - cambiar estado a eliminado
        if current_user.role not in ['editor', 'admin']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para eliminar proyectos"
            )
        
        db_proyecto.estado = 'eliminado'
        db_proyecto.updated_at = datetime.now()
        db.commit()
        
        return {"message": "Proyecto marcado como eliminado"}


@router.post("/{proyecto_id}/archivar")
async def archivar_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Archivar un proyecto (cambiar estado a 'archivado').
    Requiere permisos de editor o admin.
    """
    if current_user.role not in ['editor', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para archivar proyectos"
        )
    
    db_proyecto = db.query(orm_models.Proyecto).filter(
        orm_models.Proyecto.id == proyecto_id
    ).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    db_proyecto.estado = 'archivado'
    db_proyecto.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_proyecto)
    
    return {"message": "Proyecto archivado exitosamente", "proyecto": db_proyecto}


@router.post("/{proyecto_id}/restaurar")
async def restaurar_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Restaurar un proyecto archivado o eliminado (cambiar estado a 'activo').
    Requiere permisos de editor o admin.
    """
    if current_user.role not in ['editor', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para restaurar proyectos"
        )
    
    db_proyecto = db.query(orm_models.Proyecto).filter(
        orm_models.Proyecto.id == proyecto_id
    ).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    db_proyecto.estado = 'activo'
    db_proyecto.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_proyecto)
    
    return {"message": "Proyecto restaurado exitosamente", "proyecto": db_proyecto}


@router.get("/{proyecto_id}/stats", response_model=ProyectoStats)
async def obtener_estadisticas_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: orm_models.Usuario = Depends(get_current_active_user)
):
    """
    Obtener estadísticas de un proyecto específico.
    
    Retorna:
    - Total de noticias vinculadas
    - Distribución por categoría
    - Fecha de última actualización de noticia
    """
    proyecto = db.query(orm_models.Proyecto).filter(
        orm_models.Proyecto.id == proyecto_id
    ).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Contar noticias totales
    total_noticias = db.query(func.count(orm_models.Noticia.id)).filter(
        orm_models.Noticia.proyecto_id == proyecto_id
    ).scalar()
    
    # Distribución por sección (categoría)
    categorias = db.query(
        orm_models.Seccion.nombre,
        func.count(orm_models.Noticia.id).label('count')
    ).join(
        orm_models.Seccion, orm_models.Noticia.seccion_id == orm_models.Seccion.id
    ).filter(
        orm_models.Noticia.proyecto_id == proyecto_id
    ).group_by(
        orm_models.Seccion.nombre
    ).all()

    noticias_por_categoria = {cat: count for cat, count in categorias}
    
    # Última actualización de noticia
    ultima_noticia = db.query(orm_models.Noticia).filter(
        orm_models.Noticia.proyecto_id == proyecto_id
    ).order_by(
        orm_models.Noticia.created_at.desc()
    ).first()
    
    ultima_actualizacion = ultima_noticia.created_at if ultima_noticia else None
    
    return ProyectoStats(
        total_noticias=total_noticias or 0,
        noticias_por_seccion=noticias_por_categoria,
        ultima_actualizacion=ultima_actualizacion
    )
