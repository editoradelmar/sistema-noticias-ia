-- Migración: agregar campo puede_ver_metricas a usuarios
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS puede_ver_metricas BOOLEAN DEFAULT FALSE NOT NULL;
-- Opcional: dar permiso a los admins actuales
UPDATE usuarios SET puede_ver_metricas = TRUE WHERE role = 'admin';
