-- Migración: Añadir session_id a métricas para generación temporal
-- Fecha: 2025-10-28
-- Descripción: Permite guardar métricas temporalmente antes de publicar noticia

-- 1. Añadir columna session_id
ALTER TABLE metricas_valor_periodistico 
ADD COLUMN session_id VARCHAR(100);

-- 2. Crear índice para session_id
CREATE INDEX idx_metricas_session_id ON metricas_valor_periodistico(session_id);

-- 3. Hacer noticia_id nullable (permitir nulos temporalmente)
ALTER TABLE metricas_valor_periodistico 
ALTER COLUMN noticia_id DROP NOT NULL;

-- 4. Añadir constraint para asegurar que tenga noticia_id O session_id
ALTER TABLE metricas_valor_periodistico 
ADD CONSTRAINT chk_noticia_or_session 
CHECK (
    (noticia_id IS NOT NULL AND session_id IS NULL) OR 
    (noticia_id IS NULL AND session_id IS NOT NULL)
);

-- Comentarios para documentar cambios
COMMENT ON COLUMN metricas_valor_periodistico.session_id IS 'ID de sesión temporal para métricas antes de publicar noticia';
COMMENT ON CONSTRAINT chk_noticia_or_session ON metricas_valor_periodistico IS 'Asegura que tenga noticia_id (persistente) O session_id (temporal)';