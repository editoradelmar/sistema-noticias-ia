-- Migración para corregir la precisión del campo roi_porcentaje
-- El campo actual NUMERIC(8,2) solo permite hasta 999,999.99
-- Necesitamos NUMERIC(12,2) para permitir hasta 9,999,999,999.99

-- Aumentar la precisión del campo roi_porcentaje
ALTER TABLE metricas_valor_periodistico 
ALTER COLUMN roi_porcentaje TYPE NUMERIC(12,2);

-- Verificar el cambio
SELECT column_name, data_type, numeric_precision, numeric_scale
FROM information_schema.columns 
WHERE table_name = 'metricas_valor_periodistico' 
AND column_name = 'roi_porcentaje';