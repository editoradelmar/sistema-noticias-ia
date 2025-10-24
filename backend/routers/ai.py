
"""
Router de IA - Solo acceso a modelos vía llm_maestro. No se permite fallback ni texto suelto fuera de funciones.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Dict, List
import httpx
import uuid
from services.generador_ia import GeneradorIA
from core.database import get_db
from models import orm_models
from models.schemas import (
    ChatRequest,
    ChatResponse,
    AnalisisIARequest,
    AnalisisIAResponse,
    ResumenIAResponse,
    TipoAnalisisIA
)

router = APIRouter()

# Almacenamiento de conversaciones en memoria
conversaciones: Dict[str, List[dict]] = {}

# ==================== ENDPOINTS ====================

# Chat conversacional con IA usando modelo seleccionado
@router.post("/chat", response_model=ChatResponse)
async def chat_con_ia(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat conversacional con IA (modelo configurable)
    - mensaje: Mensaje del usuario
    - conversacion_id: ID de conversación (opcional)
    - contexto: Contexto adicional (opcional)
    - llm_id: ID del modelo LLM a usar
    """
    if not request.llm_id:
        raise HTTPException(status_code=400, detail="Debe especificar un llm_id válido")
    llm = db.query(orm_models.LLMMaestro).filter(orm_models.LLMMaestro.id == request.llm_id, orm_models.LLMMaestro.activo == True).first()
    if not llm:
        raise HTTPException(status_code=404, detail=f"Modelo LLM con id {request.llm_id} no encontrado o inactivo")

    conv_id = request.conversacion_id or str(uuid.uuid4())
    if conv_id not in conversaciones:
        conversaciones[conv_id] = []


    # Preparar historial de mensajes
    historial = conversaciones[conv_id].copy()
    mensaje_usuario = request.mensaje
    if request.contexto:
        mensaje_usuario = f"Contexto: {request.contexto}\n\nPregunta: {request.mensaje}"
    historial.append({"role": "user", "content": mensaje_usuario})

    # Generar respuesta usando el modelo seleccionado, enviando el historial completo
    generador = GeneradorIA(db)
    try:
        respuesta_llm = generador.generar_contenido(
            llm=llm,
            prompt_contenido=historial,  # Enviar historial acumulado
            max_tokens=2000
        )
        respuesta_texto = respuesta_llm.get("contenido", "")
        tokens_usados = respuesta_llm.get("tokens_usados", 0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar respuesta con el modelo: {str(e)}")

    # Guardar en historial
    historial.append({"role": "assistant", "content": respuesta_texto})
    conversaciones[conv_id] = historial

    return ChatResponse(
        respuesta=respuesta_llm,  # dict completo
        conversacion_id=conv_id,
        tokens_usados=tokens_usados
    )

# ==================== HELPERS ====================

def obtener_noticia_por_id(noticia_id: int, db: Session) -> orm_models.Noticia:
    """Obtener noticia de PostgreSQL"""

    noticia = db.query(orm_models.Noticia).filter(orm_models.Noticia.id == noticia_id).first()
    if not noticia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Noticia con ID {noticia_id} no encontrada"
        )
    return noticia

    # Guardar respuesta en historial
    conversaciones[conv_id].append({
        "role": "assistant",
        "content": respuesta_texto
    })

    return ChatResponse(
        respuesta=respuesta_texto,
        conversacion_id=conv_id,
        tokens_usados=tokens_usados
    )
    # Generar un resumen detallado de una noticia (solo modo simulado o vía llm_maestro)
    # Obtener noticia de PostgreSQL
    noticia = obtener_noticia_por_id(noticia_id, db)
    noticia_dict = noticia.to_dict()
    
    # Solo modo simulado permitido aquí
    print("ℹ️ Generando resumen simulado (solo permitido vía llm_maestro)")
    contenido = noticia.contenido
    palabras = contenido.split()
    resumen = ' '.join(palabras[:30]) + "..."
    puntos_clave = [
        f"📌 Sección: {noticia.seccion.nombre if noticia.seccion else 'Sin sección'}",
        f"📅 Publicado el {noticia.fecha}",
        "ℹ️ Para resúmenes más inteligentes, use un modelo LLM válido"
    ]
    
    # Actualizar noticia con el resumen en PostgreSQL
    noticia.resumen_ia = resumen
    db.commit()
    db.refresh(noticia)
    
    return ResumenIAResponse(
        noticia_id=noticia_id,
        resumen=resumen,
        puntos_clave=puntos_clave,
        longitud_original=len(noticia.contenido),
        longitud_resumen=len(resumen)
    )


@router.post("/analizar", response_model=AnalisisIAResponse)
async def analizar_noticia(
    request: AnalisisIARequest,
    db: Session = Depends(get_db)
):
    # Analizar una noticia con IA (solo modo simulado o vía llm_maestro)
    noticia = obtener_noticia_por_id(request.noticia_id, db)
    
    # Preparar prompts
    prompts = {
        TipoAnalisisIA.RESUMEN: f"Resume en 3-4 oraciones:\n\nTítulo: {noticia.titulo}\nContenido: {noticia.contenido}",
        TipoAnalisisIA.SENTIMENT: f"Analiza el sentimiento (positivo/neutral/negativo):\n\n{noticia.contenido}",
        TipoAnalisisIA.KEYWORDS: f"Extrae las 5 palabras clave:\n\n{noticia.contenido}",
        TipoAnalisisIA.TRADUCCION: f"Traduce al {request.idioma_destino or 'inglés'}:\n\n{noticia.titulo}\n{noticia.contenido}"
    }
    
    prompt = prompts.get(request.tipo_analisis)
    
    # Solo modo simulado permitido aquí
    resultado = f"[Modo Simulado] Análisis de '{noticia.titulo}': {noticia.seccion.nombre if noticia.seccion else 'Sin sección'}, {noticia.fecha}"
    
    return AnalisisIAResponse(
        noticia_id=request.noticia_id,
        tipo_analisis=request.tipo_analisis,
        resultado=resultado,
        metadata={
            "titulo_noticia": noticia.titulo,
            "timestamp": str(noticia.fecha)
        }
    )


@router.get("/conversaciones/{conversacion_id}")
async def obtener_conversacion(conversacion_id: str):
    # Obtener historial de conversación
    if conversacion_id not in conversaciones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversación {conversacion_id} no encontrada"
        )
    
    return {
        "conversacion_id": conversacion_id,
        "mensajes": conversaciones[conversacion_id],
        "total_mensajes": len(conversaciones[conversacion_id])
    }


@router.delete("/conversaciones/{conversacion_id}")
async def eliminar_conversacion(conversacion_id: str):
    # Eliminar conversación
    if conversacion_id in conversaciones:
        del conversaciones[conversacion_id]
        return {"success": True, "message": "Conversación eliminada"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Conversación {conversacion_id} no encontrada"
    )
