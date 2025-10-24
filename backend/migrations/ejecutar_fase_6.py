#!/usr/bin/env python3
"""
Script para ejecutar la migración de Fase 6 - Sistema de Maestros
Ejecuta directamente en PostgreSQL sin necesidad de psql
"""
import sys
import os

# Agregar el directorio padre al path para importar config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import psycopg2
from config import settings

# SQL de migración Fase 6
MIGRATION_SQL = """
-- ============================================
-- FASE 6: SISTEMA DE MAESTROS Y MULTI-SALIDAS
-- ============================================

-- 1. MAESTRO LLM (Modelos de IA)
CREATE TABLE IF NOT EXISTS llm_maestro (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    proveedor VARCHAR(50) NOT NULL,
    modelo_id VARCHAR(100) NOT NULL,
    url_api VARCHAR(500) NOT NULL,
    api_key TEXT NOT NULL,
    version VARCHAR(50),
    configuracion JSONB DEFAULT '{}',
    headers_adicionales JSONB DEFAULT '{}',
    costo_entrada DECIMAL(10,6),
    costo_salida DECIMAL(10,6),
    limite_diario_tokens INTEGER,
    tokens_usados_hoy INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT true,
    fecha_expiracion_key DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. MAESTRO PROMPTS
CREATE TABLE IF NOT EXISTS prompt_maestro (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    categoria VARCHAR(50),
    contenido TEXT NOT NULL,
    variables JSONB DEFAULT '[]',
    ejemplos TEXT,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. MAESTRO ESTILOS
CREATE TABLE IF NOT EXISTS estilo_maestro (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    tipo_estilo VARCHAR(50),
    configuracion JSONB NOT NULL,
    ejemplos TEXT,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 4. SECCIONES (reemplazo de categorías)
CREATE TABLE IF NOT EXISTS seccion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    color VARCHAR(7) DEFAULT '#3B82F6',
    icono VARCHAR(50) DEFAULT 'newspaper',
    prompt_id INTEGER REFERENCES prompt_maestro(id) ON DELETE SET NULL,
    estilo_id INTEGER REFERENCES estilo_maestro(id) ON DELETE SET NULL,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 5. MAESTRO SALIDAS (Canales de publicación)
CREATE TABLE IF NOT EXISTS salida_maestro (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    tipo_salida VARCHAR(50) NOT NULL,
    configuracion JSONB DEFAULT '{}',
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 6. RELACIÓN NOTICIA-SALIDA (M2M con contenido generado)
CREATE TABLE IF NOT EXISTS noticia_salida (
    id SERIAL PRIMARY KEY,
    noticia_id INTEGER NOT NULL REFERENCES noticia(id) ON DELETE CASCADE,
    salida_id INTEGER NOT NULL REFERENCES salida_maestro(id) ON DELETE CASCADE,
    contenido_generado TEXT NOT NULL,
    llm_usado_id INTEGER REFERENCES llm_maestro(id) ON DELETE SET NULL,
    prompt_usado_id INTEGER REFERENCES prompt_maestro(id) ON DELETE SET NULL,
    estilo_usado_id INTEGER REFERENCES estilo_maestro(id) ON DELETE SET NULL,
    tokens_usados INTEGER,
    tiempo_generacion_ms INTEGER,
    generado_en TIMESTAMP DEFAULT NOW(),
    UNIQUE(noticia_id, salida_id)
);

-- ============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================

-- LLM Maestro
CREATE INDEX IF NOT EXISTS idx_llm_proveedor ON llm_maestro(proveedor);
CREATE INDEX IF NOT EXISTS idx_llm_activo ON llm_maestro(activo);

-- Prompt Maestro
CREATE INDEX IF NOT EXISTS idx_prompt_categoria ON prompt_maestro(categoria);
CREATE INDEX IF NOT EXISTS idx_prompt_activo ON prompt_maestro(activo);

-- Estilo Maestro
CREATE INDEX IF NOT EXISTS idx_estilo_tipo ON estilo_maestro(tipo_estilo);
CREATE INDEX IF NOT EXISTS idx_estilo_activo ON estilo_maestro(activo);

-- Sección
CREATE INDEX IF NOT EXISTS idx_seccion_activo ON seccion(activo);
CREATE INDEX IF NOT EXISTS idx_seccion_prompt ON seccion(prompt_id);
CREATE INDEX IF NOT EXISTS idx_seccion_estilo ON seccion(estilo_id);

-- Salida Maestro
CREATE INDEX IF NOT EXISTS idx_salida_tipo ON salida_maestro(tipo_salida);
CREATE INDEX IF NOT EXISTS idx_salida_activo ON salida_maestro(activo);

-- Noticia Salida
CREATE INDEX IF NOT EXISTS idx_noticia_salida_noticia ON noticia_salida(noticia_id);
CREATE INDEX IF NOT EXISTS idx_noticia_salida_salida ON noticia_salida(salida_id);

-- ============================================
-- DATOS DE EJEMPLO
-- ============================================

-- LLM Maestros
INSERT INTO llm_maestro (nombre, proveedor, modelo_id, url_api, api_key, version, activo) VALUES
('Claude Sonnet 4', 'Anthropic', 'claude-sonnet-4-20250514', 'https://api.anthropic.com/v1/messages', 'TEMP_KEY', '4.0', true),
('GPT-4 Turbo', 'OpenAI', 'gpt-4-turbo-preview', 'https://api.openai.com/v1/chat/completions', 'TEMP_KEY', '4.0', false),
('Gemini Pro', 'Google', 'gemini-pro', 'https://generativelanguage.googleapis.com/v1/models', 'TEMP_KEY', '1.0', false)
ON CONFLICT (nombre) DO NOTHING;

-- Prompts Maestros
INSERT INTO prompt_maestro (nombre, categoria, contenido, descripcion, activo) VALUES
('Noticia Estándar', 'noticia', 'Genera una noticia periodística profesional basada en el siguiente contenido: {contenido}. Mantén un tono objetivo y neutral.', 'Prompt básico para noticias generales', true),
('Reportaje Profundo', 'reportaje', 'Crea un reportaje detallado sobre: {tema}. Incluye contexto, análisis y múltiples perspectivas.', 'Para reportajes extensos', true),
('Nota Breve', 'breve', 'Resume en máximo 3 párrafos: {contenido}. Sé conciso y directo.', 'Para notas cortas', true)
ON CONFLICT (nombre) DO NOTHING;

-- Estilos Maestros
INSERT INTO estilo_maestro (nombre, tipo_estilo, configuracion, descripcion, activo) VALUES
('Formal Periodístico', 'tono', '{"tono": "formal", "persona": "tercera", "tiempo": "pasado"}', 'Estilo clásico de periódico', true),
('Casual Web', 'tono', '{"tono": "casual", "persona": "segunda", "longitud": "media"}', 'Para contenido web moderno', true),
('Redes Sociales', 'formato', '{"emojis": true, "hashtags": true, "longitud": "corta"}', 'Optimizado para redes', true)
ON CONFLICT (nombre) DO NOTHING;

-- Secciones (migrar categorías existentes)
INSERT INTO seccion (nombre, descripcion, color, icono, activo)
SELECT 
    DISTINCT categoria,
    'Sección de ' || categoria,
    '#3B82F6',
    'newspaper',
    true
FROM noticia
WHERE categoria IS NOT NULL
ON CONFLICT (nombre) DO NOTHING;

-- Agregar secciones comunes si no existen
INSERT INTO seccion (nombre, descripcion, color, icono, activo) VALUES
('Política', 'Noticias políticas y gubernamentales', '#EF4444', 'landmark', true),
('Economía', 'Finanzas y negocios', '#10B981', 'trending-up', true),
('Deportes', 'Noticias deportivas', '#F59E0B', 'trophy', true),
('Tecnología', 'Innovación y tecnología', '#3B82F6', 'cpu', true),
('Cultura', 'Arte, cine, música', '#8B5CF6', 'palette', true),
('Salud', 'Medicina y bienestar', '#06B6D4', 'heart-pulse', true)
ON CONFLICT (nombre) DO NOTHING;

-- Salidas Maestras
INSERT INTO salida_maestro (nombre, tipo_salida, descripcion, configuracion, activo) VALUES
('Impreso', 'print', 'Formato para periódico impreso', '{"max_caracteres": 2000, "columnas": 3}', true),
('Web', 'digital', 'Contenido para sitio web', '{"formato": "html", "seo": true}', true),
('Twitter/X', 'social', 'Publicación para Twitter/X', '{"max_caracteres": 280, "hashtags": 3}', true),
('Instagram', 'social', 'Post para Instagram', '{"max_caracteres": 2200, "emojis": true}', true),
('Facebook', 'social', 'Publicación para Facebook', '{"formato": "html", "enlaces": true}', true)
ON CONFLICT (nombre) DO NOTHING;

-- ============================================
-- MIGRACIÓN: Asociar noticias existentes con secciones
-- ============================================

-- Agregar columna temporal si no existe
ALTER TABLE noticia ADD COLUMN IF NOT EXISTS seccion_id INTEGER REFERENCES seccion(id) ON DELETE SET NULL;

-- Migrar categorías a secciones
UPDATE noticia n
SET seccion_id = s.id
FROM seccion s
WHERE n.categoria = s.nombre
AND n.seccion_id IS NULL;

-- ============================================
-- TRIGGERS PARA UPDATED_AT
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar triggers
DROP TRIGGER IF EXISTS update_llm_maestro_updated_at ON llm_maestro;
CREATE TRIGGER update_llm_maestro_updated_at BEFORE UPDATE ON llm_maestro FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_prompt_maestro_updated_at ON prompt_maestro;
CREATE TRIGGER update_prompt_maestro_updated_at BEFORE UPDATE ON prompt_maestro FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_estilo_maestro_updated_at ON estilo_maestro;
CREATE TRIGGER update_estilo_maestro_updated_at BEFORE UPDATE ON estilo_maestro FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_seccion_updated_at ON seccion;
CREATE TRIGGER update_seccion_updated_at BEFORE UPDATE ON seccion FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_salida_maestro_updated_at ON salida_maestro;
CREATE TRIGGER update_salida_maestro_updated_at BEFORE UPDATE ON salida_maestro FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- FIN DE MIGRACIÓN FASE 6
-- ============================================
"""

def ejecutar_migracion():
    """Ejecuta la migración SQL en PostgreSQL"""
    
    print("="*60)
    print("🚀 EJECUTANDO MIGRACIÓN FASE 6")
    print("="*60)
    print()
    
    # Extraer información de la URL de la BD
    db_url = settings.DATABASE_URL
    print(f"📊 Base de datos: {db_url}")
    print()
    
    try:
        # Conectar a PostgreSQL
        print("🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        print("✅ Conexión exitosa")
        print()
        
        # Ejecutar migración
        print("📝 Ejecutando SQL de migración...")
        cursor.execute(MIGRATION_SQL)
        print("✅ Migración ejecutada correctamente")
        print()
        
        # Verificar resultados
        print("="*60)
        print("🔍 VERIFICACIÓN DE RESULTADOS")
        print("="*60)
        print()
        
        tablas = [
            'llm_maestro',
            'prompt_maestro',
            'estilo_maestro',
            'seccion',
            'salida_maestro',
            'noticia_salida'
        ]
        
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"✅ {tabla:25} → {count:3} registros")
        
        print()
        print("="*60)
        print("🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print()
        print("📋 PRÓXIMOS PASOS:")
        print("   1. Verificar los datos con: SELECT * FROM llm_maestro;")
        print("   2. Continuar con Fase 6.2: Schemas Pydantic")
        print("   3. Continuar con Fase 6.3: Routers CRUD")
        print()
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print()
        print("="*60)
        print("❌ ERROR EN LA MIGRACIÓN")
        print("="*60)
        print()
        print(f"Error: {e}")
        print()
        print("💡 Posibles soluciones:")
        print("   1. Verifica que PostgreSQL esté corriendo")
        print("   2. Verifica las credenciales en backend/.env")
        print("   3. Verifica que la BD 'noticias_ia' exista")
        print()
        return False
    
    except Exception as e:
        print()
        print("="*60)
        print("❌ ERROR INESPERADO")
        print("="*60)
        print()
        print(f"Error: {e}")
        print()
        return False

if __name__ == "__main__":
    exito = ejecutar_migracion()
    sys.exit(0 if exito else 1)
