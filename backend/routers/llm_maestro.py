"""
Router para LLM Maestro
CRUD completo para gestión de modelos LLM
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.orm_models import LLMMaestro as LLMMaestroORM
from models.schemas_fase6 import (
    LLMMaestro,
    LLMMaestroCreate,
    LLMMaestroUpdate,
    LLMMaestroConKey,
    ProveedorLLM
)
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario

router = APIRouter(
    prefix="/api/llm-maestro",
    tags=["LLM Maestro"]
)


# ==================== LISTAR ====================

@router.get("/", response_model=List[LLMMaestro])
async def listar_llms(
    activo: Optional[bool] = None,
    proveedor: Optional[ProveedorLLM] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar todos los modelos LLM
    - **activo**: Filtrar por estado (true/false)
    - **proveedor**: Filtrar por proveedor (Anthropic, OpenAI, etc.)
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a retornar
    """
    query = db.query(LLMMaestroORM)
    
    # Filtros
    if activo is not None:
        query = query.filter(LLMMaestroORM.activo == activo)
    
    if proveedor:
        query = query.filter(LLMMaestroORM.proveedor == proveedor.value)
    
    llms = query.offset(skip).limit(limit).all()
    
    # Ocultar API keys por seguridad (ya lo hace el schema)
    return llms


@router.get("/activos", response_model=List[LLMMaestro])
async def listar_llms_activos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar solo los modelos LLM activos
    """
    llms = db.query(LLMMaestroORM).filter(
        LLMMaestroORM.activo == True
    ).all()
    
    return llms


# ==================== OBTENER UNO ====================

@router.get("/{llm_id}", response_model=LLMMaestro)
async def obtener_llm(
    llm_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener un modelo LLM por ID (sin API key)
    """
    llm = db.query(LLMMaestroORM).filter(LLMMaestroORM.id == llm_id).first()
    
    if not llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM con ID {llm_id} no encontrado"
        )
    
    return llm


@router.get("/{llm_id}/with-key", response_model=LLMMaestroConKey)
async def obtener_llm_con_key(
    llm_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)  # Solo admin
):
    """
    Obtener un modelo LLM con API key visible
    ⚠️ Solo para administradores
    """
    llm = db.query(LLMMaestroORM).filter(LLMMaestroORM.id == llm_id).first()
    
    if not llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM con ID {llm_id} no encontrado"
        )
    
    return llm


# ==================== CREAR ====================

@router.post("/", response_model=LLMMaestro, status_code=status.HTTP_201_CREATED)
async def crear_llm(
    llm: LLMMaestroCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)  # Solo admin
):
    """
    Crear un nuevo modelo LLM
    ⚠️ Solo para administradores
    """
    # Verificar si ya existe un LLM con ese nombre
    existing = db.query(LLMMaestroORM).filter(
        LLMMaestroORM.nombre == llm.nombre
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un LLM con el nombre '{llm.nombre}'"
        )
    
    # Crear nuevo LLM sin items
    db_llm = LLMMaestroORM(**llm.model_dump(exclude={'items'}))
    db.add(db_llm)
    db.commit()
    db.refresh(db_llm)
    # Crear PromptItems asociados
    if hasattr(llm, 'items') and llm.items:
        from models.orm_models import PromptItem
        for idx, item in enumerate(llm.items):
            db_item = PromptItem(
                prompt_maestro_id=db_llm.id,
                nombre_archivo=item.nombre_archivo,
                contenido=item.contenido,
                orden=item.orden if item.orden is not None else idx+1
            )
            db.add(db_item)
        db.commit()
    db.refresh(db_llm)
    return db_llm


# ==================== ACTUALIZAR ====================

@router.put("/{llm_id}", response_model=LLMMaestro)
async def actualizar_llm(
    llm_id: int,
    llm_update: LLMMaestroUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)  # Solo admin
):
    """
    Actualizar un modelo LLM existente
    ⚠️ Solo para administradores
    """
    # Buscar el LLM
    db_llm = db.query(LLMMaestroORM).filter(LLMMaestroORM.id == llm_id).first()
    
    if not db_llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM con ID {llm_id} no encontrado"
        )
    
    # Verificar nombre único si se está cambiando
    if llm_update.nombre and llm_update.nombre != db_llm.nombre:
        existing = db.query(LLMMaestroORM).filter(
            LLMMaestroORM.nombre == llm_update.nombre,
            LLMMaestroORM.id != llm_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un LLM con el nombre '{llm_update.nombre}'"
            )
    
    # Actualizar campos del maestro
    update_data = llm_update.model_dump(exclude={'items'}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_llm, field, value)
    db.commit()
    # Actualizar PromptItems asociados
    if hasattr(llm_update, 'items') and llm_update.items is not None:
        from models.orm_models import PromptItem
        # Eliminar items actuales
        db.query(PromptItem).filter_by(prompt_maestro_id=llm_id).delete()
        db.commit()
        # Crear nuevos items
        for idx, item in enumerate(llm_update.items):
            db_item = PromptItem(
                prompt_maestro_id=llm_id,
                nombre_archivo=item.nombre_archivo,
                contenido=item.contenido,
                orden=item.orden if item.orden is not None else idx+1
            )
            db.add(db_item)
        db.commit()
    db.refresh(db_llm)
    return db_llm


# ==================== ELIMINAR ====================

@router.delete("/{llm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_llm(
    llm_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)  # Solo admin
):
    """
    Eliminar un modelo LLM
    ⚠️ Solo para administradores
    """
    db_llm = db.query(LLMMaestroORM).filter(LLMMaestroORM.id == llm_id).first()
    
    if not db_llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM con ID {llm_id} no encontrado"
        )
    
    db.delete(db_llm)
    db.commit()
    
    return None


# ==================== ACTIVAR/DESACTIVAR ====================

@router.patch("/{llm_id}/toggle-activo", response_model=LLMMaestro)
async def toggle_activo_llm(
    llm_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)  # Solo admin
):
    """
    Activar/Desactivar un modelo LLM
    ⚠️ Solo para administradores
    """
    db_llm = db.query(LLMMaestroORM).filter(LLMMaestroORM.id == llm_id).first()
    
    if not db_llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM con ID {llm_id} no encontrado"
        )
    
    db_llm.activo = not db_llm.activo
    db.commit()
    db.refresh(db_llm)
    
    return db_llm


# ==================== RESETEAR TOKENS DIARIOS ====================

@router.post("/{llm_id}/reset-tokens", response_model=LLMMaestro)
async def resetear_tokens_diarios(
    llm_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)  # Solo admin
):
    """
    Resetear el contador de tokens usados hoy
    ⚠️ Solo para administradores
    """
    db_llm = db.query(LLMMaestroORM).filter(LLMMaestroORM.id == llm_id).first()
    
    if not db_llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM con ID {llm_id} no encontrado"
        )
    
    db_llm.tokens_usados_hoy = 0
    db.commit()
    db.refresh(db_llm)
    
    return db_llm


# ==================== PRUEBA DE CONEXIÓN ====================

@router.post("/{llm_id}/test-connection")
async def probar_conexion_llm(
    llm_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)  # Solo admin
):
    """
    Probar la conexión con el modelo LLM
    ⚠️ Solo para administradores
    
    TODO: Implementar lógica de prueba real según proveedor
    """
    db_llm = db.query(LLMMaestroORM).filter(LLMMaestroORM.id == llm_id).first()
    
    if not db_llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM con ID {llm_id} no encontrado"
        )
    
    # TODO: Implementar prueba real según proveedor
    # Por ahora solo retorna success
    
    return {
        "success": True,
        "message": f"Conexión con {db_llm.nombre} simulada exitosamente",
        "proveedor": db_llm.proveedor,
        "modelo_id": db_llm.modelo_id,
        "nota": "Implementar prueba real en futuro"
    }
