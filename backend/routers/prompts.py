
"""Router para Prompts - CRUD completo"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.orm_models import PromptMaestro as PromptMaestroORM, PromptItem
from models.schemas_fase6 import PromptMaestro, PromptMaestroCreate, PromptMaestroUpdate
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario
import re

router = APIRouter(prefix="/api/prompts", tags=["Prompts"])

@router.get("/activos", response_model=List[PromptMaestro])
async def listar_prompts_activos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return db.query(PromptMaestroORM).filter(PromptMaestroORM.activo == True).all()

@router.get("/", response_model=List[PromptMaestro])
async def listar_prompts(
    activo: Optional[bool] = None,
    # categoria eliminado
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = db.query(PromptMaestroORM)
    if activo is not None:
        query = query.filter(PromptMaestroORM.activo == activo)
    # Filtro por categoria eliminado
    return query.offset(skip).limit(limit).all()

@router.get("/{prompt_id}", response_model=PromptMaestro)
async def obtener_prompt(prompt_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    prompt = db.query(PromptMaestroORM).filter(PromptMaestroORM.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail=f"Prompt {prompt_id} no encontrado")
    return prompt

@router.post("/", response_model=PromptMaestro, status_code=201)
async def crear_prompt(prompt: PromptMaestroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    existing = db.query(PromptMaestroORM).filter(PromptMaestroORM.nombre == prompt.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Prompt '{prompt.nombre}' ya existe")
    items_data = prompt.items if hasattr(prompt, 'items') else []
    prompt_dict = prompt.model_dump(exclude={"items"})
    db_prompt = PromptMaestroORM(**prompt_dict)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    # Persistir items
    for idx, item in enumerate(items_data):
        db_item = PromptItem(
            prompt_id=db_prompt.id,
            nombre_archivo=item["nombre_archivo"],
            contenido=item.get("contenido", ""),
            orden=item.get("orden", idx+1)
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.put("/{prompt_id}", response_model=PromptMaestro)
async def actualizar_prompt(prompt_id: int, prompt_update: PromptMaestroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_prompt = db.query(PromptMaestroORM).filter(PromptMaestroORM.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(status_code=404, detail=f"Prompt {prompt_id} no encontrado")
    update_data = prompt_update.model_dump(exclude_unset=True, exclude={"items"})
    for field, value in update_data.items():
        setattr(db_prompt, field, value)
    # Actualizar items si vienen en el payload
    if hasattr(prompt_update, "items") and prompt_update.items is not None:
        print("[DEBUG] Items recibidos en PUT /api/prompts/{}:".format(prompt_id), prompt_update.items)
        # Eliminar items previos
        db.query(PromptItem).filter(PromptItem.prompt_id == prompt_id).delete()
        # Agregar nuevos items
        for idx, item in enumerate(prompt_update.items):
            db_item = PromptItem(
                prompt_id=prompt_id,
                nombre_archivo=item["nombre_archivo"],
                contenido=item.get("contenido", ""),
                orden=item.get("orden", idx+1)
            )
            db.add(db_item)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.delete("/{prompt_id}", status_code=204)
async def eliminar_prompt(prompt_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_prompt = db.query(PromptMaestroORM).filter(PromptMaestroORM.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(status_code=404, detail=f"Prompt {prompt_id} no encontrado")
    db.delete(db_prompt)
    db.commit()
    return None
