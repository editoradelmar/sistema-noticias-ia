"""
Router para manejo explícito de items de Estilo
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.orm_models import EstiloItem, EstiloMaestro
from models.schemas_fase6 import EstiloItem as EstiloItemSchema
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario

router = APIRouter(prefix="/api/estilo-items", tags=["EstiloItems"])

@router.get("/by-estilo/{estilo_id}", response_model=List[EstiloItemSchema])
def listar_items_por_estilo(estilo_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    items = db.query(EstiloItem).filter(EstiloItem.estilo_id == estilo_id).order_by(EstiloItem.orden).all()
    return items

@router.get("/{item_id}", response_model=EstiloItemSchema)
def obtener_item(item_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    item = db.query(EstiloItem).filter(EstiloItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    return item

@router.post("/", response_model=EstiloItemSchema, status_code=201)
def crear_item(item: EstiloItemSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("estilo_items")
    try:
        # Validar que no haya campos extra y que el estilo exista
        if not item.estilo_id:
            logger.error("estilo_id es None o no proporcionado")
            raise HTTPException(status_code=422, detail="El campo estilo_id es obligatorio")
        
        estilo_exists = db.query(EstiloMaestro).filter(EstiloMaestro.id == item.estilo_id).first()
        if not estilo_exists:
            logger.error(f"EstiloMaestro con id={item.estilo_id} no existe")
            raise HTTPException(status_code=404, detail=f"EstiloMaestro con id={item.estilo_id} no existe")
        
        db_item = EstiloItem(
            estilo_id=item.estilo_id,
            nombre_archivo=item.nombre_archivo,
            contenido=item.contenido if item.contenido is not None else "",
            orden=item.orden
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        logger.info(f"Item creado correctamente: id={db_item.id}")
        return db_item
    except Exception as e:
        logger.error(f"Error al crear EstiloItem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno al crear EstiloItem: {str(e)}")

@router.put("/{item_id}", response_model=EstiloItemSchema)
def actualizar_item(item_id: int, item_update: EstiloItemSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_item = db.query(EstiloItem).filter(EstiloItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    
    db_item.nombre_archivo = item_update.nombre_archivo
    db_item.contenido = item_update.contenido if item_update.contenido is not None else ""
    db_item.orden = item_update.orden
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=204)
def eliminar_item(item_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_item = db.query(EstiloItem).filter(EstiloItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    db.delete(db_item)
    db.commit()
    return None