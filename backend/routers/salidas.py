"""Router para Salidas - CRUD completo"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.orm_models import SalidaMaestro as SalidaMaestroORM
from models.schemas_fase6 import SalidaMaestro, SalidaMaestroCreate, SalidaMaestroUpdate, TipoSalida
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario

router = APIRouter(prefix="/api/salidas", tags=["Salidas"])

@router.get("/", response_model=List[SalidaMaestro])
async def listar_salidas(
    activo: Optional[bool] = None,
    tipo_salida: Optional[TipoSalida] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    query = db.query(SalidaMaestroORM)
    if activo is not None:
        query = query.filter(SalidaMaestroORM.activo == activo)
    if tipo_salida:
        query = query.filter(SalidaMaestroORM.tipo_salida == tipo_salida.value)
    return query.offset(skip).limit(limit).all()

@router.get("/{salida_id}", response_model=SalidaMaestro)
async def obtener_salida(salida_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    salida = db.query(SalidaMaestroORM).filter(SalidaMaestroORM.id == salida_id).first()
    if not salida:
        raise HTTPException(status_code=404, detail=f"Salida {salida_id} no encontrada")
    return salida

@router.post("/", response_model=SalidaMaestro, status_code=201)
async def crear_salida(salida: SalidaMaestroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    existing = db.query(SalidaMaestroORM).filter(SalidaMaestroORM.nombre == salida.nombre).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Salida '{salida.nombre}' ya existe")
    db_salida = SalidaMaestroORM(**salida.model_dump())
    db.add(db_salida)
    db.commit()
    db.refresh(db_salida)
    return db_salida

@router.put("/{salida_id}", response_model=SalidaMaestro)
async def actualizar_salida(salida_id: int, salida_update: SalidaMaestroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_salida = db.query(SalidaMaestroORM).filter(SalidaMaestroORM.id == salida_id).first()
    if not db_salida:
        raise HTTPException(status_code=404, detail=f"Salida {salida_id} no encontrada")
    update_data = salida_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_salida, field, value)
    db.commit()
    db.refresh(db_salida)
    return db_salida

@router.delete("/{salida_id}", status_code=204)
async def eliminar_salida(salida_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_salida = db.query(SalidaMaestroORM).filter(SalidaMaestroORM.id == salida_id).first()
    if not db_salida:
        raise HTTPException(status_code=404, detail=f"Salida {salida_id} no encontrada")
    db.delete(db_salida)
    db.commit()
    return None
