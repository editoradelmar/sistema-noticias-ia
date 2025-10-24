-- MIGRACIÓN MANUAL: Agregar columna 'titulo' a noticia_salida
ALTER TABLE noticia_salida ADD COLUMN titulo VARCHAR(200) NOT NULL DEFAULT '';
