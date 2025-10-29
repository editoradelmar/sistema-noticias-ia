"""
Router para Métricas de Valor Periodístico
Endpoints para consultar métricas guardadas en BD
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db
from core.auth import get_current_user
from models.schemas import Usuario
from models.orm_models import MetricasValorPeriodistico
from models.schemas import MetricasValorResumen
from services.generador_ia import GeneradorIA

router = APIRouter(
    prefix="/api/metricas",
    tags=["Métricas"]
)

@router.get("/noticia/{noticia_id}", response_model=Optional[MetricasValorResumen])
async def obtener_metricas_noticia(
    noticia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene las métricas guardadas para una noticia específica
    
    **Usado para:**
    - Mostrar métricas al editar noticia existente
    - Solo admins pueden ver métricas
    
    **Retorna None si:**
    - No existen métricas para la noticia
    - Usuario no es admin
    """
    print(f"🔍 Obteniendo métricas para noticia {noticia_id}, usuario: {current_user.username}, role: {current_user.role}")
    
    # Solo admins pueden ver métricas
    if current_user.role != 'admin':
        print(f"❌ Usuario {current_user.username} no es admin, retornando None")
        return None
    
    # Buscar métricas más recientes para esta noticia
    metrica = db.query(MetricasValorPeriodistico).filter(
        MetricasValorPeriodistico.noticia_id == noticia_id
    ).order_by(MetricasValorPeriodistico.created_at.desc()).first()
    
    if not metrica:
        return None
    
    # Convertir a formato de resumen para el frontend
    generador = GeneradorIA(db)
    
    # Construir diccionario de métricas desde el registro de BD
    metricas_dict = {
        "tiempo_generacion_total": float(metrica.tiempo_generacion_total),
        "tiempo_estimado_manual": metrica.tiempo_estimado_manual,
        "ahorro_tiempo_minutos": metrica.ahorro_tiempo_minutos,
        "tokens_total": metrica.tokens_total,
        "costo_generacion": float(metrica.costo_generacion),
        "costo_estimado_manual": float(metrica.costo_estimado_manual),
        "ahorro_costo": float(metrica.ahorro_costo),
        "cantidad_salidas_generadas": metrica.cantidad_salidas_generadas,
        "cantidad_formatos_diferentes": metrica.cantidad_formatos_diferentes,
        "velocidad_palabras_por_segundo": float(metrica.velocidad_palabras_por_segundo),
        "modelo_usado": metrica.modelo_usado,
        "tipo_noticia": metrica.tipo_noticia,
        "complejidad_estimada": metrica.complejidad_estimada,
        "roi_porcentaje": float(metrica.roi_porcentaje),
        "porcentaje_contenido_aprovechable": float(metrica.porcentaje_contenido_aprovechable) if metrica.porcentaje_contenido_aprovechable else 0.9
    }
    
    # Usar el método existente para generar el resumen
    resumen = generador.obtener_resumen_metricas(metricas_dict)
    
    return resumen

@router.get("/estadisticas", response_model=dict)
async def obtener_estadisticas_generales(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene estadísticas generales de métricas
    Solo para administradores
    """
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden ver estadísticas"
        )
    
    # Estadísticas básicas
    from sqlalchemy import func
    
    stats = db.query(
        func.count(MetricasValorPeriodistico.id).label('total_metricas'),
        func.avg(MetricasValorPeriodistico.roi_porcentaje).label('roi_promedio'),
        func.sum(MetricasValorPeriodistico.ahorro_tiempo_minutos).label('tiempo_total_ahorrado'),
        func.sum(MetricasValorPeriodistico.ahorro_costo).label('costo_total_ahorrado'),
        func.sum(MetricasValorPeriodistico.tokens_total).label('tokens_totales_usados')
    ).first()
    
    return {
        "total_publicaciones_con_metricas": stats.total_metricas or 0,
        "roi_promedio": round(float(stats.roi_promedio or 0), 2),
        "tiempo_total_ahorrado_minutos": stats.tiempo_total_ahorrado or 0,
        "costo_total_ahorrado": round(float(stats.costo_total_ahorrado or 0), 2),
        "tokens_totales_procesados": stats.tokens_totales_usados or 0
    }