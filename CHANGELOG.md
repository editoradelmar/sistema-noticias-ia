# 📝 Changelog - Sistema de Noticias con IA

Todos los cambios notables del proyecto se documentan en este archivo.

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
