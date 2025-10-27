
"""
Router para Generación de Contenido IA
Endpoints para generar contenido optimizado por salidas
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from core.database import get_db
from core.auth import get_current_user, get_current_editor
from models.schemas import Usuario
from models.orm_models import (
    Noticia as NoticiaORM,
    SalidaMaestro as SalidaMaestroORM,
    LLMMaestro as LLMMaestroORM,
    PromptMaestro as PromptMaestroORM,
    EstiloMaestro as EstiloMaestroORM
)
from models.schemas_fase6 import (
    NoticiaSalida,
    NoticiaSalidaConRelaciones,
    NoticiaSalidaTemporal,
    GenerarSalidasRequest,
    GenerarSalidasResponse,
    GenerarSalidasTemporalRequest,
    GenerarSalidasTemporalResponse
)
from services.generador_ia import GeneradorIA

router = APIRouter(
    prefix="/api/generar",
    tags=["Generación IA"]
)
# Endpoint GET: obtener todas las salidas generadas de una noticia
@router.get("/noticia/{noticia_id}/salidas", response_model=List[NoticiaSalida])
async def obtener_salidas_de_noticia(
    noticia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Devuelve todas las salidas generadas (noticia_salida) para una noticia dada.
    """
    from models.orm_models import NoticiaSalida, SalidaMaestro
    salidas = db.query(NoticiaSalida).filter(NoticiaSalida.noticia_id == noticia_id).all()
    if not salidas:
        raise HTTPException(status_code=404, detail="No se encontraron salidas para esta noticia")
    # Enriquecer con nombre_salida si es posible
    salida_ids = [s.salida_id for s in salidas]
    salidas_maestro = db.query(SalidaMaestro).filter(SalidaMaestro.id.in_(salida_ids)).all()
    id2nombre = {s.id: s.nombre for s in salidas_maestro}
    for s in salidas:
        s.nombre_salida = id2nombre.get(s.salida_id, "")
    return salidas


@router.post("/salidas", response_model=GenerarSalidasResponse)
async def generar_salidas(
    request: GenerarSalidasRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Genera contenido optimizado para múltiples salidas
    
    **Flujo:**
    1. Toma una noticia (existente o temporal)
    2. Selecciona salidas (web, print, social, etc.)
    3. Usa un LLM (Claude, GPT, etc.)
    4. Genera contenido optimizado para cada salida
    
    **Requiere permisos de Editor o Admin**
    """
    noticia = None
    
    # Modo temporal o normal
    if request.temporal and request.datosNoticia:
        print("🔄 Modo temporal detectado - creando objeto temporal")
        # Crear objeto temporal
        from types import SimpleNamespace
        from models.orm_models import Seccion
        
        seccion_real = db.query(Seccion).filter(Seccion.id == request.datosNoticia.seccion_id).first()
        if not seccion_real:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sección {request.datosNoticia.seccion_id} no encontrada"
            )
        
        # Pre-cargar relaciones de prompt y estilo
        if seccion_real.prompt and seccion_real.prompt.items:
            _ = seccion_real.prompt.items
        if seccion_real.estilo and seccion_real.estilo.items:
            _ = seccion_real.estilo.items
        
        # Crear objeto temporal
        noticia = SimpleNamespace()
        noticia.id = request.datosNoticia.id
        noticia.titulo = request.datosNoticia.titulo
        noticia.contenido = request.datosNoticia.contenido
        noticia.seccion_id = request.datosNoticia.seccion_id
        noticia.proyecto_id = request.datosNoticia.proyecto_id
        noticia.usuario_id = current_user.id  # Usar usuario_id en lugar de autor
        noticia.fecha = datetime.now()
        noticia.seccion = seccion_real
        
    else:
        # Modo normal - validar noticia existente
        if not request.noticia_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se requiere noticia_id para modo normal o temporal=True con datosNoticia"
            )
            
        noticia = db.query(NoticiaORM).filter(NoticiaORM.id == request.noticia_id).first()
        if not noticia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Noticia {request.noticia_id} no encontrada"
            )
        
        # Asegurar que las relaciones estén cargadas
        if noticia.seccion:
            if noticia.seccion.prompt:
                _ = noticia.seccion.prompt.items
            if noticia.seccion.estilo:
                _ = noticia.seccion.estilo.items
    
    # Validar salidas
    salidas = db.query(SalidaMaestroORM).filter(
        SalidaMaestroORM.id.in_(request.salidas_ids),
        SalidaMaestroORM.activo == True
    ).all()
    
    if len(salidas) != len(request.salidas_ids):
        salidas_encontradas = [s.id for s in salidas]
        salidas_faltantes = set(request.salidas_ids) - set(salidas_encontradas)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salidas no encontradas o inactivas: {salidas_faltantes}"
        )
    
    # Validar LLM
    llm = db.query(LLMMaestroORM).filter(
        LLMMaestroORM.id == request.llm_id,
        LLMMaestroORM.activo == True
    ).first()
    
    if not llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM {request.llm_id} no encontrado o inactivo"
        )
    
        # prompt y estilo ahora siempre se heredan de la sección; validación eliminada
    
    # Generar contenido
    generador = GeneradorIA(db)
    
    if request.temporal:
        print("🎯 Generación temporal - usando método temporal")
        resultados = generador.generar_multiples_salidas_temporal(
            noticia_temporal=noticia,
            salidas=salidas,
            llm=llm,
            regenerar=request.regenerar
        )
    else:
        print("🎯 Generación normal - usando método normal")
        resultados = generador.generar_multiples_salidas(
            noticia=noticia,
            salidas=salidas,
            llm=llm,
            regenerar=request.regenerar
        )
    
    # Calcular totales (diferentes para temporal vs normal)
    if request.temporal:
        # Los resultados temporales son diccionarios
        total_tokens = sum(r.get("tokens_usados", 0) for r in resultados if r.get("tokens_usados"))
        tiempo_total_ms = sum(r.get("tiempo_generacion_ms", 0) for r in resultados if r.get("tiempo_generacion_ms"))
    else:
        # Los resultados normales son objetos
        total_tokens = sum(r.tokens_usados for r in resultados if r.tokens_usados)
        tiempo_total_ms = sum(r.tiempo_generacion_ms for r in resultados if r.tiempo_generacion_ms)
    return GenerarSalidasResponse(
        noticia_id=getattr(noticia, 'id', 0),  # 0 para temporal
        salidas_generadas=resultados,
        total_tokens=total_tokens,
        tiempo_total_ms=tiempo_total_ms,
        errores=[]
    )


@router.post("/salidas-temporal", response_model=GenerarSalidasTemporalResponse)
async def generar_salidas_temporal(
    request: GenerarSalidasTemporalRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Genera contenido para múltiples salidas SIN crear la noticia en BD
    
    **Flujo temporal:**
    1. Toma datos de noticia (no guardada)
    2. Selecciona salidas (web, print, social, etc.)
    3. Usa un LLM para generar contenido
    4. Devuelve resultados SIN guardar en BD
    
    **Usado por "Generar Noticias" antes de "Publicar"**
    """
    # Validar salidas
    salidas = db.query(SalidaMaestroORM).filter(
        SalidaMaestroORM.id.in_(request.salidas_ids),
        SalidaMaestroORM.activo == True
    ).all()
    
    if len(salidas) != len(request.salidas_ids):
        salidas_encontradas = [s.id for s in salidas]
        salidas_faltantes = set(request.salidas_ids) - set(salidas_encontradas)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Salidas no encontradas o inactivas: {salidas_faltantes}"
        )
    
    # Validar LLM
    llm = db.query(LLMMaestroORM).filter(
        LLMMaestroORM.id == request.llm_id,
        LLMMaestroORM.activo == True
    ).first()
    
    if not llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM {request.llm_id} no encontrado o inactivo"
        )
    
    # Obtener sección para prompts y estilos
    from models.orm_models import Seccion
    seccion_real = db.query(Seccion).filter(Seccion.id == request.datosNoticia.seccion_id).first()
    if not seccion_real:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sección {request.datosNoticia.seccion_id} no encontrada"
        )
    
    # Pre-cargar relaciones de prompt y estilo
    if seccion_real.prompt and seccion_real.prompt.items:
        _ = seccion_real.prompt.items
    if seccion_real.estilo and seccion_real.estilo.items:
        _ = seccion_real.estilo.items
    
    # Crear objeto temporal con los datos
    from types import SimpleNamespace
    noticia_temporal = SimpleNamespace()
    noticia_temporal.id = request.datosNoticia.id
    noticia_temporal.titulo = request.datosNoticia.titulo
    noticia_temporal.contenido = request.datosNoticia.contenido
    noticia_temporal.seccion_id = request.datosNoticia.seccion_id
    noticia_temporal.proyecto_id = request.datosNoticia.proyecto_id
    noticia_temporal.usuario_id = current_user.id  # Usar usuario_id en lugar de autor
    noticia_temporal.fecha = datetime.now()
    noticia_temporal.seccion = seccion_real
    
    # Generar contenido temporal
    generador = GeneradorIA(db)
    print(f"🔄 Iniciando generación temporal para {len(salidas)} salidas")
    resultados = generador.generar_multiples_salidas_temporal(
        noticia_temporal=noticia_temporal,
        salidas=salidas,
        llm=llm,
        regenerar=True  # Siempre regenerar para temporal
    )
    
    print(f"📊 Resultados obtenidos: {len(resultados)} items")
    if resultados:
        print(f"🔍 Primer resultado: {type(resultados[0])} - Keys: {list(resultados[0].keys()) if isinstance(resultados[0], dict) else 'No es dict'}")
    
    # Calcular totales - los resultados temporales son diccionarios
    total_tokens = sum(r.get("tokens_usados", 0) for r in resultados if r.get("tokens_usados"))
    tiempo_total_ms = sum(r.get("tiempo_generacion_ms", 0) for r in resultados if r.get("tiempo_generacion_ms"))
    
    return GenerarSalidasTemporalResponse(
        noticia_id=request.datosNoticia.id,  # Puede ser None para temporal
        salidas_generadas=resultados,
        total_tokens=total_tokens,
        tiempo_total_ms=tiempo_total_ms,
        errores=[]
    )


@router.post("/salida-individual", response_model=NoticiaSalida)
async def generar_salida_individual(
    noticia_id: int,
    salida_id: int,
    llm_id: int,
    # prompt_id y estilo_id eliminados del endpoint individual (ajustar frontend si es necesario)
    regenerar: bool = False,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Genera contenido para una sola salida
    
    **Más simple que generar múltiples salidas**
    """
    # Validaciones
    noticia = db.query(NoticiaORM).filter(NoticiaORM.id == noticia_id).first()
    if not noticia:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    
    # Asegurar que las relaciones estén cargadas
    if noticia.seccion:
        if noticia.seccion.prompt:
            _ = noticia.seccion.prompt.items
        if noticia.seccion.estilo:
            _ = noticia.seccion.estilo.items
    
    salida = db.query(SalidaMaestroORM).filter(
        SalidaMaestroORM.id == salida_id,
        SalidaMaestroORM.activo == True
    ).first()
    if not salida:
        raise HTTPException(status_code=404, detail="Salida no encontrada o inactiva")
    
    llm = db.query(LLMMaestroORM).filter(
        LLMMaestroORM.id == llm_id,
        LLMMaestroORM.activo == True
    ).first()
    if not llm:
        raise HTTPException(status_code=404, detail="LLM no encontrado o inactivo")
    
    # prompt y estilo ahora siempre se heredan de la sección
    
    # Generar
    generador = GeneradorIA(db)
    resultado = generador.generar_para_salida(
        noticia=noticia,
        salida=salida
    )
    return resultado


@router.delete("/salida/{noticia_salida_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_salida_generada(
    noticia_salida_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Elimina una salida generada
    
    **Útil para limpiar versiones antiguas**
    """
    from models.orm_models import NoticiaSalida
    
    salida = db.query(NoticiaSalida).filter(NoticiaSalida.id == noticia_salida_id).first()
    if not salida:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    
    db.delete(salida)
    db.commit()
    
    return None


# --- NUEVO ENDPOINT: Actualizar NoticiaSalida (PUT) ---
from models.schemas_fase6 import NoticiaSalidaUpdate, NoticiaSalida as NoticiaSalidaSchema
from models.orm_models import NoticiaSalida as NoticiaSalidaORM

@router.put("/salida/{noticia_salida_id}", response_model=NoticiaSalidaSchema)
async def actualizar_salida_generada(
    noticia_salida_id: int,
    datos: NoticiaSalidaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Actualiza los campos editables de una salida generada (título, contenido_generado, etc)
    """
    salida = db.query(NoticiaSalidaORM).filter(NoticiaSalidaORM.id == noticia_salida_id).first()
    if not salida:
        raise HTTPException(status_code=404, detail="Salida no encontrada")
    if datos.titulo is not None:
        salida.titulo = datos.titulo
    if datos.contenido_generado is not None:
        salida.contenido_generado = datos.contenido_generado
    if datos.tokens_usados is not None:
        salida.tokens_usados = datos.tokens_usados
    if datos.tiempo_generacion_ms is not None:
        salida.tiempo_generacion_ms = datos.tiempo_generacion_ms
    db.commit()
    db.refresh(salida)
    return salida


@router.post("/regenerar-todo/{noticia_id}")
async def regenerar_todas_salidas(
    noticia_id: int,
    llm_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Regenera TODAS las salidas existentes de una noticia
    
    **Útil cuando se actualiza el contenido de la noticia**
    """
    from models.orm_models import NoticiaSalida
    
    # Validar noticia
    noticia = db.query(NoticiaORM).filter(NoticiaORM.id == noticia_id).first()
    if not noticia:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    
    # Obtener salidas ya generadas
    salidas_existentes = db.query(NoticiaSalida).filter(
        NoticiaSalida.noticia_id == noticia_id
    ).all()
    
    if not salidas_existentes:
        raise HTTPException(
            status_code=404,
            detail="Esta noticia no tiene salidas generadas aún"
        )
    
    # Validar LLM
    llm = db.query(LLMMaestroORM).filter(
        LLMMaestroORM.id == llm_id,
        LLMMaestroORM.activo == True
    ).first()
    if not llm:
        raise HTTPException(status_code=404, detail="LLM no encontrado")
    
    # Obtener las salidas maestro
    salidas_ids = [s.salida_id for s in salidas_existentes]
    salidas = db.query(SalidaMaestroORM).filter(
        SalidaMaestroORM.id.in_(salidas_ids)
    ).all()
    
    # Regenerar todas
    try:
        generador = GeneradorIA(db)
        resultados = generador.generar_multiples_salidas(
            noticia=noticia,
            salidas=salidas,
            llm=llm,
            regenerar=True
        )
        
        return {
            "message": f"Regeneradas {len(resultados)} salidas",
            "salidas": resultados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
