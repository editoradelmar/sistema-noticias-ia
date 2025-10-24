

"""Router para Estilos - CRUD completo"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.orm_models import EstiloMaestro as EstiloMaestroORM
from models.schemas_fase6 import EstiloMaestro, EstiloMaestroCreate, EstiloMaestroUpdate, TipoEstilo
from core.auth import get_current_user, get_current_admin
from models.schemas import Usuario

router = APIRouter(prefix="/api/estilos", tags=["Estilos"])

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
    db_estilo = EstiloMaestroORM(**estilo.model_dump())
    db.add(db_estilo)
    db.commit()
    db.refresh(db_estilo)
    return db_estilo

@router.put("/{estilo_id}", response_model=EstiloMaestro)
async def actualizar_estilo(estilo_id: int, estilo_update: EstiloMaestroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == estilo_id).first()
    if not db_estilo:
        raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado")
    update_data = estilo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_estilo, field, value)
    db.commit()
    db.refresh(db_estilo)
    return db_estilo

@router.delete("/{estilo_id}", status_code=204)
async def eliminar_estilo(estilo_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_admin)):
    db_estilo = db.query(EstiloMaestroORM).filter(EstiloMaestroORM.id == estilo_id).first()
    if not db_estilo:
        raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado")
    db.delete(db_estilo)
    db.commit()
    return None
