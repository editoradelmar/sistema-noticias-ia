-- Migración: Añadir tabla de métricas de valor periodístico
-- Fecha: 2025-10-28
-- Versión: 2.4.0

CREATE TABLE metricas_valor_periodistico (
    id SERIAL PRIMARY KEY,
    noticia_id INTEGER REFERENCES noticias(id),
    
    -- Métricas de Eficiencia Temporal
    tiempo_generacion_total DECIMAL(8,3), -- segundos totales
    tiempo_por_salida JSONB, -- {"web": 2.3, "twitter": 1.1, "instagram": 1.8}
    tiempo_estimado_manual INTEGER, -- minutos que tomaría manualmente
    ahorro_tiempo_minutos INTEGER, -- tiempo ahorrado vs proceso manual
    
    -- Métricas de Costo
    tokens_total INTEGER,
    costo_generacion DECIMAL(10,4), -- costo en USD
    costo_estimado_manual DECIMAL(10,2), -- costo de redactor manual
    ahorro_costo DECIMAL(10,2), -- diferencia de costo
    
    -- Métricas de Productividad
    cantidad_salidas_generadas INTEGER,
    cantidad_formatos_diferentes INTEGER, -- web, impreso, twitter, etc.
    velocidad_palabras_por_segundo DECIMAL(8,2),
    
    -- Métricas de Calidad
    adherencia_manual_estilo DECIMAL(3,2) DEFAULT 0.95, -- 0.0 a 1.0
    requiere_edicion_manual BOOLEAN DEFAULT FALSE,
    porcentaje_contenido_aprovechable DECIMAL(3,2) DEFAULT 0.90, -- cuánto se usa sin editar
    
    -- Contexto del Proceso
    modelo_usado VARCHAR(100),
    usuario_id INTEGER REFERENCES usuarios(id),
    tipo_noticia VARCHAR(50), -- breaking, feature, opinion, etc.
    complejidad_estimada VARCHAR(20) DEFAULT 'media', -- simple, media, compleja
    
    -- Resultados de Negocio (para análisis posterior)
    engagement_promedio DECIMAL(8,2) DEFAULT 0, -- views, likes, shares
    tiempo_en_tendencia INTEGER DEFAULT 0, -- minutos en trending
    roi_porcentaje DECIMAL(8,2), -- ROI calculado
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para optimizar consultas
CREATE INDEX idx_metricas_noticia_id ON metricas_valor_periodistico(noticia_id);
CREATE INDEX idx_metricas_usuario_id ON metricas_valor_periodistico(usuario_id);
CREATE INDEX idx_metricas_fecha ON metricas_valor_periodistico(created_at);
CREATE INDEX idx_metricas_modelo ON metricas_valor_periodistico(modelo_usado);

-- Comentarios para documentación
COMMENT ON TABLE metricas_valor_periodistico IS 'Métricas de valor y ROI de la IA en el proceso periodístico - Solo para administradores';
COMMENT ON COLUMN metricas_valor_periodistico.roi_porcentaje IS 'Porcentaje de ROI: (ahorro_tiempo_valor - costo_generacion) / costo_generacion * 100';
COMMENT ON COLUMN metricas_valor_periodistico.tiempo_por_salida IS 'JSON con tiempo de generación por tipo de salida';