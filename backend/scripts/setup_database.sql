-- Script SQL para crear base de datos PostgreSQL
-- Ejecutar como superusuario: psql -U postgres -f setup_database.sql

-- Crear base de datos
CREATE DATABASE noticias_ia
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_CO.UTF-8'
    LC_CTYPE = 'es_CO.UTF-8'
    TEMPLATE = template0;

-- Comentario
COMMENT ON DATABASE noticias_ia IS 'Base de datos del Sistema de Noticias con IA';

-- Conectar a la base de datos
\c noticias_ia;

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Para búsquedas de texto

-- Mensaje de confirmación
\echo '✅ Base de datos noticias_ia creada exitosamente'
\echo 'Siguiente paso: alembic upgrade head'
