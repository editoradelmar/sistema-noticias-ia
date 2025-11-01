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
    Noticia,  # Para crear nuevas noticias
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

@router.post("/salidas", response_model=GenerarSalidasResponse)
async def publicar_salidas(
    request: GenerarSalidasRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_editor)
):
    """
    Publica las salidas generadas de una noticia y guarda métricas de valor.
    """
    # Validar noticia existente
    noticia = db.query(NoticiaORM).filter(NoticiaORM.id == request.noticia_id).first()
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noticia {request.noticia_id} no encontrada"
        )
    # Verificar que exista un Estilo efectivo (heredado de la sección o presente en la sección)
    if not getattr(noticia, 'seccion', None) or not getattr(noticia.seccion, 'estilo', None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La noticia no tiene un Estilo asociado. Asocie un Estilo a la Sección antes de generar."
        )
    # Validar salidas
    salidas = db.query(SalidaMaestroORM).filter(
        SalidaMaestroORM.id.in_(request.salidas_ids),
        SalidaMaestroORM.activo == True
    ).all()
    if len(salidas) != len(request.salidas_ids):
        salidas_encontradas = [s.id for s in salidas]
        salidas_faltantes = set(request.salidas_ids) - set(salidas_encontradas)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Salidas no encontradas o inactivas: {salidas_faltantes}"
        )
    # Log detallado del contenido recibido en metricas_valor
    import logging
    logging.warning(f"[LOG CRÍTICO] metricas_valor recibido en request: {request.metricas_valor}")
    print(f"[LOG CRÍTICO] metricas_valor recibido en request: {request.metricas_valor}")

    # Generar y guardar métricas de valor
    generador = GeneradorIA(db)
    metricas_valor = request.metricas_valor if hasattr(request, 'metricas_valor') else {}
    metrica_guardada = generador.guardar_metricas_valor(
        metricas=metricas_valor,
        noticia_id=noticia.id,
        usuario_id=current_user.id
    )
    # Responder con las salidas generadas y métricas
    from models.orm_models import NoticiaSalida as NoticiaSalidaORM
    salidas_generadas = db.query(NoticiaSalidaORM).filter(NoticiaSalidaORM.noticia_id == noticia.id).all()
    total_tokens = sum(s.tokens_usados or 0 for s in salidas_generadas)
    # Asegura que cada salida tenga contenido válido
    salidas_generadas_validas = []
    for s in salidas_generadas:
        if not getattr(s, 'contenido_generado', None) or len(s.contenido_generado) < 10:
            s.contenido_generado = 'Contenido generado automáticamente.'
        salidas_generadas_validas.append(s)

    # Calcula tiempo_total_ms (dummy, puedes ajustar según lógica real)
    tiempo_total_ms = 0.0
    return GenerarSalidasResponse(
        noticia_id=noticia.id,
        salidas_generadas=salidas_generadas_validas,
        total_tokens=total_tokens,
        tiempo_total_ms=tiempo_total_ms
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
    # Asignar nombre_salida a cada objeto para serialización correcta
    for salida in salidas:
        salida.nombre_salida = salida.salida.nombre if salida.salida else None
    return salidas
    generador = GeneradorIA(db)
    
    if request.temporal:
        print("🎯 Generación temporal - usando método temporal")
        # Capturar métricas para todos los usuarios cuando es noticia existente (tiene ID)
        capturar_metricas = hasattr(noticia, 'id') and noticia.id is not None
        print(f"📊 Métricas temporales: capturar={capturar_metricas}, noticia_id={getattr(noticia, 'id', None)}")
        
        resultados = generador.generar_multiples_salidas_temporal(
            noticia_temporal=noticia,
            salidas=salidas,
            llm=llm,
            regenerar=request.regenerar,
            capturar_metricas=capturar_metricas,
            usuario_id=current_user.id
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
        
        # Para modo normal (publicación): guardar métricas para TODOS los usuarios
        if len(resultados) > 0:
            try:
                print("💾 Usuario publicando - guardando métricas en BD...")
                # Calcular métricas de valor
                contenido_total = f"{noticia.titulo} {noticia.contenido} "
                for r in resultados:
                    contenido_total += f"{r.titulo} {r.contenido_generado} "
                tipo_noticia = getattr(noticia, 'tipo', 'feature')
                complejidad = 'media'
                metricas = generador.calcular_metricas_valor(
                    tiempo_generacion_total=tiempo_total_ms / 1000.0,  # Convertir a segundos
                    tokens_totales=total_tokens,
                    cantidad_salidas=len(resultados),
                    modelo_usado=llm.modelo_id,
                    contenido_total=contenido_total,
                    tipo_noticia=tipo_noticia,
                    complejidad=complejidad
                )
                # Si el request incluye session_id, asociar métricas temporales
                session_id = getattr(request, 'session_id', None)
                if session_id:
                    print(f"🔄 Intentando asociar métricas temporales con session_id: {session_id}")
                    metrica_guardada = generador.guardar_metricas_valor(
                        metricas=metricas,
                        noticia_id=noticia.id,
                        usuario_id=current_user.id,
                        session_id=session_id
                    )
                else:
                    metrica_guardada = generador.guardar_metricas_valor(
                        metricas=metricas,
                        noticia_id=noticia.id,
                        usuario_id=current_user.id,
                        session_id=request.session_id if hasattr(request, 'session_id') else None
                    )
                if metrica_guardada:
                    print(f"✅ Métricas guardadas en BD - ID: {metrica_guardada.id}, Usuario: {current_user.username}")
                else:
                    print("⚠️ Error guardando métricas en BD")
            except Exception as e:
                print(f"❌ Error procesando métricas al publicar: {e}")
                import traceback
                traceback.print_exc()
                # No fallar la publicación por errores de métricas
    
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
    5. **Métricas**: Se calculan y muestran solo para admins (para análisis)
    
    **Nota**: Al publicar posteriormente, las métricas se guardan para TODOS los usuarios
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
    # Requerir que la sección tenga un Estilo asociado (regla: Estilo y Salida son obligatorios para generación)
    if not getattr(seccion_real, 'estilo', None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sección {seccion_real.id} no tiene Estilo asociado. Asocie un Estilo para poder generar salidas temporales."
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
    
    # Determinar si capturar métricas
    # - Siempre para noticia existente (modo edición) 
    # - SIEMPRE para creación nueva (todos los usuarios pueden publicar noticias)
    es_noticia_existente = noticia_temporal.id is not None
    capturar_metricas = True  # SIEMPRE capturar métricas para noticias
    
    # Eliminado: generación y uso de session_id para métricas temporales
    
    # Generar contenido temporal
    generador = GeneradorIA(db)
    print(f"🔄 Iniciando generación temporal para {len(salidas)} salidas (métricas: {capturar_metricas})")
    
    resultado_completo = generador.generar_multiples_salidas_temporal(
        noticia_temporal=noticia_temporal,
        salidas=salidas,
        llm=llm,
        regenerar=True,  # Siempre regenerar para temporal
        usuario_id=current_user.id,
        capturar_metricas=capturar_metricas
    )
    
    # Extraer datos del resultado completo
    resultados = resultado_completo.get("salidas_generadas", [])
    errores = resultado_completo.get("errores", [])
    tiempo_total = resultado_completo.get("tiempo_total", 0)
    metricas_valor = resultado_completo.get("metricas_valor", None)
    
    print(f"✅ Resultados obtenidos: {len(resultados)} items, {len(errores)} errores")
    if metricas_valor:
        if es_noticia_existente:
            print(f"📈 Métricas incluidas para noticia existente: ROI {metricas_valor.get('roi_porcentaje', 0)}%")
        else:
            print(f"📈 Métricas incluidas para admin: ROI {metricas_valor.get('roi_porcentaje', 0)}%")
    
    # Calcular totales - los resultados temporales son diccionarios
    total_tokens = sum(r.get("tokens_usados", 0) for r in resultados if r.get("tokens_usados"))
    tiempo_total_ms = tiempo_total * 1000  # Convertir a ms para compatibilidad
    
    # Preparar respuesta
    response_data = {
        "noticia_id": request.datosNoticia.id,  # Puede ser None para temporal
        "salidas_generadas": resultados,
        "total_tokens": total_tokens,
        "tiempo_total_ms": tiempo_total_ms,
        "errores": errores
    }
    # Eliminado: session_id en la respuesta, ya no se usa
    
    # Añadir métricas si están disponibles (para noticia existente o admin)
    if metricas_valor:
        response_data["metricas_valor"] = metricas_valor
    
    return GenerarSalidasTemporalResponse(**response_data)


@router.post("/salida-individual", response_model=NoticiaSalida)
async def generar_salida_individual(
    noticia_id: int,
    salida_id: int,
    llm_id: int,
    estilo_id: Optional[int] = None,
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
    # Resolver estilo: preferir estilo de la sección, si no existe usar estilo_id proporcionado
    estilo_obj = None
    if noticia.seccion and getattr(noticia.seccion, 'estilo', None):
        estilo_obj = noticia.seccion.estilo
    elif estilo_id is not None:
        estilo_obj = db.query(EstiloMaestroORM).filter(
            EstiloMaestroORM.id == estilo_id,
            EstiloMaestroORM.activo == True
        ).first()
        if not estilo_obj:
            raise HTTPException(status_code=404, detail=f"Estilo {estilo_id} no encontrado o inactivo")
    else:
        raise HTTPException(status_code=400, detail="No hay Estilo efectivo: asocie un Estilo a la Sección o pase estilo_id")

    # Generar
    generador = GeneradorIA(db)
    resultado = generador.generar_para_salida(
        noticia=noticia,
        salida=salida,
        estilo=estilo_obj,
        regenerar=regenerar
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
