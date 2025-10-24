"""
Router para manejo explícito de items de Prompt
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.orm_models import PromptItem, PromptMaestro
from models.schemas_fase6 import PromptItem as PromptItemSchema
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario

router = APIRouter(prefix="/api/prompt-items", tags=["PromptItems"])

@router.get("/by-prompt/{prompt_id}", response_model=List[PromptItemSchema])
def listar_items_por_prompt(prompt_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    items = db.query(PromptItem).filter(PromptItem.prompt_id == prompt_id).order_by(PromptItem.orden).all()
    return items

@router.get("/{item_id}", response_model=PromptItemSchema)
def obtener_item(item_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    item = db.query(PromptItem).filter(PromptItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    return item

@router.post("/", response_model=PromptItemSchema, status_code=201)
def crear_item(item: PromptItemSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("prompt_items")
    try:
        payload = item.model_dump(exclude_unset=True)
        logger.info(f"Payload recibido en crear_item: {payload}")
        # Validar que no haya campos extra
        allowed_fields = {'prompt_id', 'nombre_archivo', 'contenido', 'orden'}
        extra_fields = set(payload.keys()) - allowed_fields
        if extra_fields:
            logger.error(f"Campos extra no permitidos en payload: {extra_fields}")
            raise HTTPException(status_code=422, detail=f"Campos extra no permitidos: {', '.join(extra_fields)}")
        # Validar que prompt_id no sea None y que el Prompt exista
        if not payload.get('prompt_id'):
            logger.error("prompt_id es None o no proporcionado")
            raise HTTPException(status_code=422, detail="El campo prompt_id es obligatorio y no puede ser None")
        prompt_exists = db.query(PromptMaestro).filter(PromptMaestro.id == payload['prompt_id']).first()
        if not prompt_exists:
            logger.error(f"PromptMaestro con id={payload['prompt_id']} no existe")
            raise HTTPException(status_code=404, detail=f"PromptMaestro con id={payload['prompt_id']} no existe")
        db_item = PromptItem(**payload)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        logger.info(f"Item creado correctamente: id={db_item.id}")
        return db_item
    except Exception as e:
        logger.error(f"Error al crear PromptItem: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno al crear PromptItem: {str(e)}")

@router.put("/{item_id}", response_model=PromptItemSchema)
def actualizar_item(item_id: int, item_update: PromptItemSchema, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_item = db.query(PromptItem).filter(PromptItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=204)
def eliminar_item(item_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_item = db.query(PromptItem).filter(PromptItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    db.delete(db_item)
    db.commit()
    return None
