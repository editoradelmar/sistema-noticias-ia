-- Migración: Crear tabla prompt_item para asociar items a PromptMaestro
-- Fecha: 2025-10-24

CREATE TABLE IF NOT EXISTS prompt_item (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER NOT NULL REFERENCES prompt_maestro(id) ON DELETE CASCADE,
    nombre_archivo VARCHAR(200) NOT NULL,
    orden INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_prompt_item_prompt_id ON prompt_item(prompt_id);
CREATE INDEX IF NOT EXISTS idx_prompt_item_orden ON prompt_item(orden);
