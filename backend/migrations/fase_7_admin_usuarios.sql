-- ========================================
-- FASE 7: ADMINISTRACIÓN DE USUARIOS
-- Migración para jerarquía editorial y control de acceso
-- ========================================

-- Extender tabla usuarios con campos de jerarquía
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS supervisor_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS secciones_asignadas JSONB DEFAULT '[]'::JSONB NOT NULL,
ADD COLUMN IF NOT EXISTS limite_tokens_diario INTEGER DEFAULT 10000 NOT NULL,
ADD COLUMN IF NOT EXISTS fecha_expiracion_acceso DATE;

-- Crear índices para performance
CREATE INDEX IF NOT EXISTS idx_usuarios_supervisor_id ON usuarios(supervisor_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_role ON usuarios(role);
CREATE INDEX IF NOT EXISTS idx_usuarios_active ON usuarios(is_active);

-- Migrar roles existentes a nueva estructura jerárquica
-- Convertir 'editor' a 'redactor' para mantener compatibilidad
UPDATE usuarios SET role = 'redactor' WHERE role = 'editor';

-- Actualizar constraint de roles para incluir nuevos roles jerárquicos
ALTER TABLE usuarios DROP CONSTRAINT IF EXISTS usuarios_role_check;
ALTER TABLE usuarios 
ADD CONSTRAINT usuarios_role_check 
CHECK (role IN ('admin', 'director', 'jefe_seccion', 'redactor', 'viewer'));

-- Crear tabla de auditoría para cambios en usuarios (para uso futuro)
CREATE TABLE IF NOT EXISTS auditoria_usuarios (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    accion VARCHAR(50) NOT NULL, -- 'create', 'update', 'delete', 'login'
    campo_modificado VARCHAR(100), -- nombre del campo que cambió
    valor_anterior TEXT,
    valor_nuevo TEXT,
    modificado_por INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_auditoria_usuarios_usuario_id ON auditoria_usuarios(usuario_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_usuarios_accion ON auditoria_usuarios(accion);
CREATE INDEX IF NOT EXISTS idx_auditoria_usuarios_created_at ON auditoria_usuarios(created_at);

-- Datos de ejemplo para testing (solo si no existen usuarios)
-- Actualizar usuario admin existente para incluir nuevos campos
UPDATE usuarios 
SET 
    role = 'admin',
    limite_tokens_diario = 50000,
    secciones_asignadas = '[]'::JSONB
WHERE role = 'admin' AND supervisor_id IS NULL;

-- Comentarios para documentación
COMMENT ON COLUMN usuarios.supervisor_id IS 'ID del supervisor directo en la jerarquía editorial';
COMMENT ON COLUMN usuarios.secciones_asignadas IS 'Array de IDs de secciones que puede gestionar el usuario';
COMMENT ON COLUMN usuarios.limite_tokens_diario IS 'Límite diario de tokens que puede usar con IA';
COMMENT ON COLUMN usuarios.fecha_expiracion_acceso IS 'Fecha de expiración del acceso del usuario';

COMMENT ON TABLE auditoria_usuarios IS 'Registro de auditoría para cambios en usuarios';

-- Verificar integridad
-- Nota: Esta query debe ejecutarse después de aplicar la migración para validar
-- SELECT 
--     u.id, u.username, u.role, s.username as supervisor_nombre,
--     CASE 
--         WHEN u.supervisor_id IS NOT NULL AND s.id IS NULL THEN 'ERROR: Supervisor no existe'
--         WHEN u.role = 'admin' AND u.supervisor_id IS NOT NULL THEN 'WARNING: Admin con supervisor'
--         ELSE 'OK'
--     END as validacion
-- FROM usuarios u
-- LEFT JOIN usuarios s ON u.supervisor_id = s.id;