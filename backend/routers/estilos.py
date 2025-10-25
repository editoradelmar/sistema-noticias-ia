

"""Router para Estilos - CRUD completo"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional
from core.database import get_db
from models.orm_models import EstiloMaestro as EstiloMaestroORM, EstiloItem as EstiloItemORM
from models.schemas_fase6 import (
    EstiloMaestro, EstiloMaestroCreate, EstiloMaestroUpdate, TipoEstilo,
    EstiloItem, EstiloItemCreate, EstiloItemUpdate, EstiloItemBase
)
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario

router = APIRouter(prefix="/api/estilos", tags=["Estilos"])

# Endpoints para items individuales
@router.get("/{estilo_id}/items/", response_model=List[EstiloItem])
async def listar_items_estilo(
    estilo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar todos los items de un estilo"""
    # Verificar que existe el estilo
    estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == estilo_id).first()
    if not estilo:
        raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado")
    
    items = db.query(EstiloItemORM).filter(EstiloItemORM.estilo_id == estilo_id).order_by(EstiloItemORM.orden).all()
    return items

@router.get("/{estilo_id}/items/{item_id}", response_model=EstiloItem)
async def obtener_item_estilo(
    estilo_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener un item específico de un estilo"""
    item = db.query(EstiloItemORM).filter(
        EstiloItemORM.estilo_id == estilo_id,
        EstiloItemORM.id == item_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado en estilo {estilo_id}")
    return item

@router.post("/{estilo_id}/items/", response_model=EstiloItem, status_code=201)
async def crear_item_estilo(
    estilo_id: int,
    item: EstiloItemBase,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Crear un nuevo item para un estilo"""
    # Verificar que existe el estilo
    estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == estilo_id).first()
    if not estilo:
        raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado")
    
    # Obtener el último orden + 1 si no se especifica
    if not item.orden:
        ultimo_orden = db.query(func.max(EstiloItemORM.orden)).filter(
            EstiloItemORM.estilo_id == estilo_id
        ).scalar() or 0
        item.orden = ultimo_orden + 1
    
    # Crear el item
    db_item = EstiloItemORM(
        estilo_id=estilo_id,
        nombre_archivo=item.nombre_archivo,
        contenido=item.contenido if item.contenido else "",
        orden=item.orden
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{estilo_id}/items/{item_id}", response_model=EstiloItem)
async def actualizar_item_estilo(
    estilo_id: int,
    item_id: int,
    item_update: EstiloItemUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Actualizar un item específico de un estilo"""
    # Verificar que existe el item
    db_item = db.query(EstiloItemORM).filter(
        EstiloItemORM.estilo_id == estilo_id,
        EstiloItemORM.id == item_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado en estilo {estilo_id}")
    
    # Actualizar campos si están presentes
    if item_update.nombre_archivo is not None:
        db_item.nombre_archivo = item_update.nombre_archivo
    if item_update.contenido is not None:
        db_item.contenido = item_update.contenido
    if item_update.orden is not None:
        db_item.orden = item_update.orden
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{estilo_id}/items/{item_id}", status_code=204)
async def eliminar_item_estilo(
    estilo_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """Eliminar un item específico de un estilo"""
    # Verificar que existe el item
    db_item = db.query(EstiloItemORM).filter(
        EstiloItemORM.estilo_id == estilo_id,
        EstiloItemORM.id == item_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado en estilo {estilo_id}")
    
    db.delete(db_item)
    db.commit()
    return None

# Antiguo endpoint de items (mantenido por compatibilidad)
@router.post("/items/", response_model=EstiloItem, status_code=201)
async def crear_estilo_item(
    item: EstiloItemCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin)
):
    """[DEPRECATED] Usar POST /{estilo_id}/items/ en su lugar"""
    # Verificar que existe el estilo
    estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == item.estilo_id).first()
    if not estilo:
        raise HTTPException(status_code=404, detail=f"Estilo {item.estilo_id} no encontrado")
    
    # Crear el item
    db_item = EstiloItem(
        estilo_id=item.estilo_id,
        nombre_archivo=item.nombre_archivo,
        contenido=item.contenido if item.contenido else "",
        orden=item.orden if item.orden else 1
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/activos", response_model=List[EstiloMaestro])
async def listar_estilos_activos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(EstiloMaestroORM).filter(EstiloMaestroORM.activo == True).all()

@router.get("/", response_model=List[EstiloMaestro])
async def listar_estilos(
    activo: Optional[bool] = None,
    tipo_estilo: Optional[TipoEstilo] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = db.query(EstiloMaestroORM)
    if activo is not None:
        query = query.filter(EstiloMaestroORM.activo == activo)
    if tipo_estilo:
        query = query.filter(EstiloMaestroORM.tipo_estilo == tipo_estilo.value)
    return query.offset(skip).limit(limit).all()

@router.get("/{estilo_id}", response_model=EstiloMaestro)
async def obtener_estilo(estilo_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == estilo_id).first()
    if not estilo:
        raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado")
    return estilo

@router.post("/", response_model=EstiloMaestro, status_code=201)
async def crear_estilo(estilo: EstiloMaestroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    existing = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.nombre == estilo.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Estilo '{estilo.nombre}' ya existe")
    
    # Separar items del resto de los datos
    items_data = estilo.items if hasattr(estilo, 'items') else []
    estilo_dict = estilo.model_dump(exclude={"items"})
    
    # Crear el estilo
    db_estilo = EstiloMaestroORM(**estilo_dict)
    db.add(db_estilo)
    db.commit()
    db.refresh(db_estilo)
    
    # Crear los items asociados
    for idx, item_data in enumerate(items_data):
        if isinstance(item_data, dict):
            db_item = EstiloItem(
                estilo_id=db_estilo.id,
                nombre_archivo=item_data.get("nombre_archivo"),
                contenido=item_data.get("contenido", ""),
                orden=item_data.get("orden", idx+1)
            )
        else:
            db_item = EstiloItem(
                estilo_id=db_estilo.id,
                nombre_archivo=item_data.nombre_archivo,
                contenido=item_data.contenido if hasattr(item_data, 'contenido') else "",
                orden=item_data.orden if hasattr(item_data, 'orden') else idx+1
            )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_estilo)
    return db_estilo

@router.put("/{estilo_id}", response_model=EstiloMaestro)
async def actualizar_estilo(estilo_id: int, estilo_update: EstiloMaestroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("estilos")
    
    logger.info(f"[DEBUG] Actualizando estilo: {estilo_id}")
    logger.info(f"[DEBUG] Datos de actualización: {estilo_update.model_dump(exclude={'items'})}")
    if hasattr(estilo_update, 'items'):
        logger.info(f"[DEBUG] Items recibidos: {estilo_update.items}")
    
    try:
        db_estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == estilo_id).first()
        if not db_estilo:
            raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado")

        # Actualizar campos básicos del estilo
        update_data = estilo_update.model_dump(exclude={"items"})
        for field, value in update_data.items():
            if value is not None:  # Solo actualizar si el valor no es None
                setattr(db_estilo, field, value)
        
        # Manejar items - siempre procesamos items ya que el schema los incluye
        logger.info(f"[DEBUG] Procesando items desde actualización")
        
        # Eliminar items existentes
        items_deleted = db.query(EstiloItemORM).filter(EstiloItemORM.estilo_id == estilo_id).delete()
        logger.info(f"[DEBUG] Items eliminados: {items_deleted}")
        
        # Agregar nuevos items si hay
        if estilo_update.items:
            logger.info(f"[DEBUG] Procesando {len(estilo_update.items)} items nuevos")
            for idx, item_data in enumerate(estilo_update.items):
                try:
                    # Convertir el item_data a diccionario y agregar estilo_id
                    item_dict = {
                        "estilo_id": estilo_id,
                        "nombre_archivo": item_data.nombre_archivo,
                        "contenido": item_data.contenido if item_data.contenido is not None else "",
                        "orden": item_data.orden if item_data.orden is not None else idx+1
                    }
                    # Crear nuevo item usando el modelo ORM
                    db_item = EstiloItemORM(**item_dict)
                    db.add(db_item)
                    logger.info(f"[DEBUG] Item {idx + 1} agregado correctamente: {item_data.nombre_archivo}")
                except Exception as item_error:
                    logger.error(f"[ERROR] Error al procesar item {idx + 1}: {str(item_error)}")
                    raise
        
        # Commit y refresh
        db.commit()
        db.refresh(db_estilo)
        logger.info("[DEBUG] Estilo actualizado exitosamente")
        
        # Verificar items guardados
        items_count = db.query(EstiloItemORM).filter(EstiloItemORM.estilo_id == estilo_id).count()
        logger.info(f"[DEBUG] Items guardados en la base de datos: {items_count}")
        
        return db_estilo
        
    except Exception as e:
        db.rollback()
        logger.error(f"[ERROR] Error al actualizar estilo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar estilo: {str(e)}")

@router.delete("/{estilo_id}", status_code=204)
async def eliminar_estilo(estilo_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == estilo_id).first()
    if not db_estilo:
        raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado")
    db.delete(db_estilo)
    db.commit()
    return None
