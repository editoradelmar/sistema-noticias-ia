"""Router para Secciones - CRUD completo"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from core.database import get_db
from models.orm_models import Seccion as SeccionORM
from models.schemas_fase6 import Seccion, SeccionCreate, SeccionUpdate, SeccionConRelaciones
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario

router = APIRouter(prefix="/api/secciones", tags=["Secciones"])

@router.get("/", response_model=List[SeccionConRelaciones])
async def listar_secciones(
    activo: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = db.query(SeccionORM).options(joinedload(SeccionORM.prompt), joinedload(SeccionORM.estilo))
    if activo is not None:
        query = query.filter(SeccionORM.activo == activo)
    return query.offset(skip).limit(limit).all()

@router.get("/{seccion_id}", response_model=SeccionConRelaciones)
async def obtener_seccion(
    seccion_id: int,
    con_relaciones: bool = True,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = db.query(SeccionORM)
    if con_relaciones:
        query = query.options(joinedload(SeccionORM.prompt), joinedload(SeccionORM.estilo))
    seccion = query.filter(SeccionORM.id == seccion_id).first()
    if not seccion:
        raise HTTPException(status_code=404, detail=f"Sección {seccion_id} no encontrada")
    return seccion

@router.post("/", response_model=Seccion, status_code=201)
async def crear_seccion(seccion: SeccionCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    existing = db.query(SeccionORM).filter(SeccionORM.nombre == seccion.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Sección '{seccion.nombre}' ya existe")
    db_seccion = SeccionORM(**seccion.model_dump())
    db.add(db_seccion)
    db.commit()
    db.refresh(db_seccion)
    return db_seccion

@router.put("/{seccion_id}", response_model=Seccion)
async def actualizar_seccion(seccion_id: int, seccion_update: SeccionUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_seccion = db.query(SeccionORM).filter(SeccionORM.id == seccion_id).first()
    if not db_seccion:
        raise HTTPException(status_code=404, detail=f"Sección {seccion_id} no encontrada")
    update_data = seccion_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_seccion, field, value)
    db.commit()
    db.refresh(db_seccion)
    return db_seccion

@router.delete("/{seccion_id}", status_code=204)
async def eliminar_seccion(seccion_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_seccion = db.query(SeccionORM).filter(SeccionORM.id == seccion_id).first()
    if not db_seccion:
        raise HTTPException(status_code=404, detail=f"Sección {seccion_id} no encontrada")
    db.delete(db_seccion)
    db.commit()
    return None
