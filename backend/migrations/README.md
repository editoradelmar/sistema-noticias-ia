# 🚀 Migración Fase 6 - Sistema de Maestros

## 📋 Descripción

Esta migración implementa el **Sistema de Maestros** para gestionar modelos LLM, prompts, estilos, secciones y salidas de contenido.

## 🎯 Lo que incluye

### Nuevas Tablas (6):
1. **llm_maestro** - Configuración de modelos de IA (Claude, GPT-4, Gemini)
2. **prompt_maestro** - Templates de prompts reutilizables
3. **estilo_maestro** - Estilos de generación de contenido
4. **seccion** - Reemplazo de categorías con configuración IA
5. **salida_maestro** - Canales de publicación (impreso, web, redes)
6. **noticia_salida** - Contenido generado por salida

### Datos de Ejemplo:
- ✅ 3 modelos LLM
- ✅ 3 prompts
- ✅ 3 estilos
- ✅ 6+ secciones
- ✅ 5 salidas

## 🚀 Cómo Ejecutar

### Opción 1: Script Automático (Recomendado)

#### En Windows:
```cmd
cd backend\migrations
ejecutar.bat
```

#### En Linux/Mac:
```bash
cd backend/migrations
chmod +x ejecutar.sh
./ejecutar.sh
```

### Opción 2: Python Directo
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# O en Windows: venv\Scripts\activate

python migrations/ejecutar_fase_6.py
```

### Opción 3: SQL Directo (psql)
```bash
psql -U openpg -d noticias_ia -f backend/migrations/fase_6_maestros.sql
```

### Opción 4: HeidiSQL (Windows)
1. Abrir HeidiSQL
2. Conectar a `noticias_ia`
3. Archivo → Cargar archivo SQL
4. Seleccionar `fase_6_maestros.sql`
5. Ejecutar ▶️

## ✅ Verificación

Después de ejecutar, verifica con:

```sql
-- Ver tablas creadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_name LIKE '%maestro%' OR table_name IN ('seccion', 'noticia_salida');

-- Ver datos insertados
SELECT 'llm_maestro' as tabla, COUNT(*) FROM llm_maestro
UNION ALL
SELECT 'prompt_maestro', COUNT(*) FROM prompt_maestro
UNION ALL
SELECT 'estilo_maestro', COUNT(*) FROM estilo_maestro
UNION ALL
SELECT 'seccion', COUNT(*) FROM seccion
UNION ALL
SELECT 'salida_maestro', COUNT(*) FROM salida_maestro;
```

Deberías ver:
- llm_maestro: 3 registros
- prompt_maestro: 3 registros
- estilo_maestro: 3 registros
- seccion: 6+ registros
- salida_maestro: 5 registros

## 🔧 Solución de Problemas

### Error: No se puede conectar a PostgreSQL
```bash
# Verificar que PostgreSQL esté corriendo
sudo service postgresql status  # Linux
# O verificar en Task Manager (Windows)

# Verificar credenciales en .env
cat backend/.env | grep DATABASE_URL
```

### Error: Módulo psycopg2 no encontrado
```bash
cd backend
source venv/bin/activate
pip install psycopg2-binary
```

### Error: Base de datos no existe
```bash
# Crear la base de datos
createdb -U openpg noticias_ia
```

## 📝 Próximos Pasos

Después de ejecutar esta migración:

1. ✅ **Actualizar API Keys reales** en `llm_maestro`
2. 📦 **Fase 6.2**: Crear Schemas Pydantic para validación
3. 🔌 **Fase 6.3**: Implementar Routers CRUD
4. 🎨 **Fase 6.4**: Crear componentes Frontend

## 📊 Estructura de Datos

### LLM Maestro
```sql
SELECT * FROM llm_maestro;
-- Gestiona: Claude, GPT-4, Gemini con sus API keys y configuraciones
```

### Prompt Maestro
```sql
SELECT * FROM prompt_maestro;
-- Contiene: Templates con variables dinámicas como {contenido}, {tema}
```

### Estilo Maestro
```sql
SELECT * FROM estilo_maestro;
-- Define: Tono, formato, longitud para cada tipo de contenido
```

### Secciones
```sql
SELECT * FROM seccion;
-- Reemplazo de: categorías con configuración de prompt y estilo
```

### Salida Maestro
```sql
SELECT * FROM salida_maestro;
-- Canales: Impreso, Web, Twitter, Instagram, Facebook
```

## ⚠️ Notas Importantes

1. **API Keys temporales**: Los modelos LLM se insertan con `TEMP_KEY_REEMPLAZAR`. Debes actualizar con tus API keys reales.

2. **Migración de categorías**: Las categorías existentes en `noticia` se migran automáticamente a la tabla `seccion`.

3. **Columna seccion_id**: Se agrega a la tabla `noticia` para relacionar con secciones.

4. **Triggers automáticos**: Se crean triggers para actualizar `updated_at` automáticamente.

## 🔒 Seguridad

- Las API keys se almacenan en la BD (considera encriptar en producción)
- Los tokens de acceso son temporales
- Validar permisos antes de exponer endpoints

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del script
2. Verifica la conexión a PostgreSQL
3. Confirma que el venv esté activado
4. Consulta el archivo `PROJECT_CONTEXT.md`

---

**Fecha de creación**: 2025-10-16  
**Versión**: Fase 6.1  
**Estado**: ✅ Listo para ejecutar
