# 📝 Changelog - Sistema de Noticias con IA

Todos los cambios notables del proyecto se documentan en este archivo.

---

## [2.4.0] - 2025-10-27

### 🏗️ **BREAKING CHANGES - Arquitectura Optimizada**

#### Refactorización de Estructura de Datos
- **🔗 usuario_id como fuente única**: Eliminación del campo `autor` redundante
- **⚡ Performance mejorado**: Filtros basados en índices integer en lugar de strings
- **🔒 Integridad referencial**: Foreign keys garantizan consistencia de datos
- **📊 Modelo ORM simplificado**: Eliminación de redundancias y propiedades optimizadas

#### Mejoras de UX/UI
- **🔤 Ordenamiento alfabético**: Secciones ordenadas en todos los dropdowns
- **🧹 Código limpio**: Eliminación de archivos temporales y de diagnóstico
- **📱 Consistencia visual**: Mantenimiento de la experiencia de usuario

#### Cambios en API
- **Campo `autor` eliminado** de requests y responses
- **`autor_nombre` calculado** dinámicamente desde relación usuario
- **Respuestas optimizadas** con estructura de datos consistente
- **Filtros mejorados** usando usuario_id para mejor performance

#### Migración de Datos
- **Scripts de limpieza** ejecutados automáticamente
- **Integridad preservada** durante la transición
- **Backwards compatibility** en schemas donde sea necesario

### 🔧 **Technical Improvements**

#### Backend Optimizations
- Simplificación del modelo `Noticia` en `orm_models.py`
- Actualización de routers para usar solo `usuario_id`
- Optimización de `generador_ia.py` con relaciones mejoradas
- Eliminación de archivos de diagnóstico y migración temporales

#### Frontend Enhancements  
- Implementación de ordenamiento alfabético en `NoticiasList.jsx`
- Optimización de carga de secciones en `NoticiaForm.jsx`
- Mantenimiento de filtros existentes con mejor performance

#### Documentation Updates
- Actualización completa de `README.md` con arquitectura v2.4.0
- Modernización de `ARCHITECTURE.md` con nuevos diagramas
- Revisión de `API_REFERENCE.md` con ejemplos actualizados
- Expansión de `CHANGELOG.md` con detalles técnicos

---

## [2.3.2] - 2025-10-27

### 🚀 Added - Funcionalidad Drag & Drop

#### Subida de Archivos Inteligente
- **Drag & Drop**: Zona visual para arrastrar y soltar archivos
- **Formatos soportados**: PDF, TXT, DOC, DOCX (máximo 10MB)
- **Extracción automática**: Contenido real de archivos TXT
- **Validación robusta**: Tipos MIME y límites de tamaño
- **Estados visuales**: Loading, success, error con iconos animados

#### Generación Inteligente de Títulos
- **Análisis de contenido**: Extrae títulos de las primeras líneas del archivo
- **Palabras clave**: Identifica términos importantes y nombres propios
- **Múltiples estrategias**: Fallbacks inteligentes para garantizar títulos descriptivos
- **Límite inteligente**: Títulos optimizados entre 15-100 caracteres

#### Mejoras de UX
- **Orden reorganizado**: Drag & drop aparece antes que título/contenido
- **Llenado automático**: Título y contenido se populan simultáneamente
- **Límites extendidos**: Contenido hasta 10,000 caracteres (antes 2,000)
- **Contador visual**: Indicador de caracteres con colores de advertencia
- **Función limpiar**: Botón para resetear y subir otro archivo

#### Integración con IA
- **Títulos AI-generados**: Sistema mejorado para generar títulos únicos
- **Parsing estructurado**: Respuestas con formato "TÍTULO:" y "CONTENIDO:"
- **Modo simulado**: Procesamiento de archivos con backend placeholder
- **Compatibilidad**: Funciona con el sistema multi-LLM existente

### � Security - Mejoras de Seguridad

#### Parametrización de Modo Desarrollo
- **Acceso rápido**: Solo visible en modo desarrollo (`npm run dev`)
- **Producción segura**: Botones de login rápido ocultos en `npm run build`
- **Variable de entorno**: Usa `import.meta.env.MODE` para control automático
- **Sin configuración manual**: Cambio automático según comando de ejecución

### �🛠️ Fixed
- Iconos faltantes en lucide-react (CloudUpload, FilePlus, FileCheck)
- Estados duplicados en componente NoticiaForm
- Límites de contenido que causaban truncamiento
- Títulos genéricos reemplazados por títulos descriptivos
- **Riesgo de seguridad**: Acceso rápido ahora oculto en producción

### 📚 Updated
- **NoticiaForm.jsx**: Reestructurado con 70+ líneas de funcionalidad drag & drop
- **Login.jsx**: Parametrización de modo desarrollo con conditional rendering
- **README.md**: Versión actualizada a 2.3.2 con nuevas características
- **Documentación**: Nuevas funcionalidades y mejoras de seguridad documentadas

---

## [2.3.1] - 2025-10-25

### 🌐 Added - Acceso Externo y Fixes de Conectividad

#### Configuración ngrok
- **Acceso externo**: Configuración completa para testing remoto
- **Headers anti-advertencia**: `ngrok-skip-browser-warning: 'true'` implementado
- **CORS actualizado**: Soporte para dominios ngrok en config.py y .env
- **URLs demo**: Frontend y backend públicos configurados

#### Fixes de Conectividad
- **PostgreSQL**: Optimización de conexión localhost/127.0.0.1
- **Frontend API**: Interceptors mejorados con logs de debug
- **Autenticación**: Headers ngrok agregados al login
- **Error handling**: Mejor manejo de errores de conexión

#### Mejoras de Debugging
- **Logs detallados**: Implementados en componentes críticos
- **Troubleshooting**: Guía completa de resolución de problemas
- **Validación**: Sistema completamente validado y operativo

### 🛠️ Fixed
- Frontend no mostraba datos por interferencia de ngrok
- Advertencias de ngrok bloqueando solicitudes API
- Problemas de CORS con dominios externos
- Errores de codificación UTF-8 en PostgreSQL

### 📚 Updated
- **README.md**: URLs demo y estado actual del proyecto
- **QUICKSTART.md**: Sección ngrok y troubleshooting ampliado
- **Documentación**: Información del desarrollador actualizada

---

## [2.3.0-alpha] - 2025-10-17

### 🎉 Added - Fase 6 Completada

#### Sistema de Maestros
- **LLM Maestro**: Gestión de modelos IA (Claude, GPT, Gemini)
  - CRUD completo con 11 endpoints
  - Tracking de tokens diarios
  - Test de conexión
  - Sistema de activación/desactivación

- **Prompt Maestro**: Plantillas reutilizables
  - Soporte para variables dinámicas `{titulo}`, `{contenido}`, etc.
  - Validación de prompts
  - 8 endpoints REST

- **Estilo Maestro**: Directivas de formato
  - Configuración JSON flexible
  - Tipos: tono, formato, estructura, longitud
  - 7 endpoints REST

- **Secciones**: Organización de contenido
  - Reemplazo de categorías
  - Vinculación con prompts y estilos
  - Colores e iconos personalizables
  - 9 endpoints REST

- **Salida Maestro**: Canales de publicación
  - 5 tipos: print, digital, social, email, podcast
  - Configuración específica por canal
  - 8 endpoints REST

#### Generación Multi-LLM
- Servicio `GeneradorIA` con soporte para:
  - Anthropic Claude (Sonnet 4.5, Opus)
  - OpenAI GPT (GPT-4, GPT-3.5) - opcional
  - Google Gemini - opcional
- Procesamiento de prompts con variables
- Aplicación automática de estilos
- Instrucciones optimizadas por tipo de salida
- 5 endpoints de generación

#### Frontend
- 7 componentes nuevos para gestión de maestros
- Modal `GenerarSalidasModal` para generación interactiva
- Componente `SalidasNoticia` con tabs
- Integración completa con backend
- UI responsive con Tailwind CSS
- Soporte para modo oscuro

### 📊 Database
- 6 tablas nuevas (llm_maestro, prompt_maestro, estilo_maestro, seccion, salida_maestro, noticia_salida)
- 18 índices para optimización
- Datos de ejemplo insertados
- Migración de categorías → secciones

### 📚 Documentation
- README principal completo
- Guías de instalación (backend y frontend)
- Documentación de generación IA
- Guía de usuario completa
- Tests unitarios

### 🔧 Technical
- Configuración de axios en frontend
- Sistema de interceptores para auth
- Manejo de errores mejorado
- Logging de métricas (tokens, tiempo)

### 📦 Dependencies
- **Backend**: anthropic==0.69.0 (requerido)
- **Backend**: openai, google-generativeai (opcionales)
- **Frontend**: axios==1.6.0

---

## [2.2.1] - 2025-10-15

### Added
- Sistema de proyectos
- CRUD completo de proyectos
- Vinculación noticia-proyecto
- Estados: activo, archivado, completado
- Estadísticas por proyecto

---

## [2.2.0] - 2025-10-14

### Added
- Rediseño completo UI/UX
- Modo oscuro / claro
- Tema personalizable
- Mejora en componentes visuales

### Changed
- Migración a Tailwind CSS 3.4
- Iconos actualizados a Lucide React
- Paleta de colores mejorada

---

## [2.1.0] - 2025-10-10

### Added
- Sistema de autenticación JWT
- 3 roles: Admin, Editor, Viewer
- Registro de usuarios
- Login/Logout
- Protección de rutas
- Context API para auth

### Security
- Encriptación de contraseñas con bcrypt
- Tokens JWT con expiración
- Middleware de autenticación
- Validación de permisos por endpoint

---

## [2.0.0] - 2025-10-05

### Changed
- **Migración a PostgreSQL**
- SQLAlchemy 2.0 ORM
- Modelos relacionales
- Mejora en performance

### Removed
- Sistema de archivos JSON
- Base de datos SQLite

### Fixed
- Problemas de concurrencia
- Escalabilidad mejorada

---

## [1.0.0] - 2025-09-28

### Added
- MVP inicial del sistema
- CRUD de noticias básico
- Integración con Claude AI
- Generación de resúmenes
- Chat con IA
- Frontend con React
- Backend con FastAPI

### Features
- Crear, leer, actualizar, eliminar noticias
- Categorías: tecnología, desarrollo, IA, negocios, ciencia, general
- Búsqueda en tiempo real
- Filtrado por categoría
- Seed data para desarrollo

---

## Roadmap

### [2.4.0] - Próxima versión
- [ ] Dashboard con estadísticas
- [ ] Sistema de comentarios
- [ ] Notificaciones en tiempo real
- [ ] Análisis de costos por LLM
- [ ] Exportación de noticias
- [ ] Historial de chat

### [3.0.0] - Largo plazo
- [ ] Mobile App (React Native)
- [ ] Búsqueda avanzada (Elasticsearch)
- [ ] Internacionalización (i18n)
- [ ] Integración con CMS
- [ ] API pública
- [ ] Webhooks

---

## Tipos de Cambios

- **Added**: Nuevas funcionalidades
- **Changed**: Cambios en funcionalidades existentes
- **Deprecated**: Funcionalidades obsoletas
- **Removed**: Funcionalidades eliminadas
- **Fixed**: Correcciones de bugs
- **Security**: Mejoras de seguridad

---

**Formato basado en**: [Keep a Changelog](https://keepachangelog.com/)  
**Versionado**: [Semantic Versioning](https://semver.org/)
