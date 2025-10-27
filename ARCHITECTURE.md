
# 🏗️ Arquitectura del Sistema de Noticias con IA v2.4.0

Documentación técnica de la arquitectura optimizada del proyecto.

---

## 🚀 Mejoras de Arquitectura v2.4.0

### 🔗 **Integridad Referencial Optimizada**
- **usuario_id como fuente única de verdad** para relaciones usuario-noticia
- **Eliminación del campo autor redundante** en favor de relaciones FK
- **Índices optimizados** para consultas más eficientes
- **Cascadas y restricciones** automatizadas por base de datos

### ⚡ **Performance Mejorado**
- **Filtros basados en integers** (usuario_id) en lugar de strings
- **Ordenamiento alfabético** implementado en frontend para secciones
- **Consultas SQL optimizadas** con joins eficientes
- **Reducción de duplicación** de datos en base de datos

### 🧹 **Código Limpio**
- **Eliminación de archivos temporales** de diagnóstico y migración
- **Consistencia en naming** y estructura de datos
- **Simplificación de modelos ORM** sin redundancias

---

## 📐 Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Noticias   │  │    Chat IA   │  │  Formularios │          │
│  │  Component   │  │   Component  │  │   Component  │          │
│  │ (Ord. Alfab.)│  │              │  │ (Ord. Alfab.)│          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│         └──────────────────┴──────────────────┘                  │
│                            │                                      │
│                 ┌──────────▼──────────┐                          │
│                 │   API Service       │                          │
│                 │   (fetch calls)     │                          │
│                 └──────────┬──────────┘                          │
└────────────────────────────┼──────────────────────────────────────┘
                             │ HTTP/JSON
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    MAIN APP (main.py)                   │    │
│  │  - CORS Middleware                                      │    │
│  │  - Lifespan Management                                  │    │
│  │  - Error Handling                                       │    │
│  └───────────┬────────────────────────────────────────────┘    │
│              │                                                   │
│  ┌───────────▼────────────┐  ┌──────────────────────────┐     │
│  │  ROUTERS               │  │   CONFIG & SCHEMAS       │     │
│  │                        │  │                          │     │
│  │  ┌──────────────────┐ │  │  ┌────────────────────┐ │     │
│  │  │ noticias.py      │ │  │  │  config.py         │ │     │
│  │  │ - CRUD           │ │  │  │  - Settings        │ │     │
│  │  │ - Paginación     │ │  │  │  - API Keys        │ │     │
│  │  │ - Filtros        │ │  │  └────────────────────┘ │     │
│  │  └──────────────────┘ │  │                          │     │
│  │                        │  │  ┌────────────────────┐ │     │
│  │  ┌──────────────────┐ │  │  │  schemas.py        │ │     │
│  │  │ ai.py            │ │  │  │  - Pydantic Models │ │     │
│  │  │ - Chat           │ │  │  │  - Validation      │ │     │
│  │  │ - Resúmenes      │ │  │  └────────────────────┘ │     │
│  │  │ - Análisis       │ │  │                          │     │
│  │  └──────────────────┘ │  └──────────────────────────┘     │
│  └────────────────────────┘                                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │            ALMACENAMIENTO (En Memoria)                │     │
│  │  - noticias_db: List[dict]                            │     │
│  │  - conversaciones: Dict[str, List[dict]]              │     │
│  └──────────────────────────────────────────────────────┘     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE API (Anthropic)                        │
│                                                                  │
│  - Claude Sonnet 4.5                                            │
│  - Resúmenes de noticias                                        │
│  - Chat conversacional                                          │
│  - Análisis de contenido                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos

### 1. Crear Noticia
```
Usuario → Frontend Form → POST /api/noticias/
                           ↓
                    Validación (Pydantic)
                           ↓
                    Guardar en memoria
                           ↓
                    Response 201 Created
                           ↓
                    Frontend actualiza UI
```

### 2. Generar Resumen con IA
```
Usuario → Click "Generar Resumen"
           ↓
    POST /api/ai/resumir/{id}
           ↓
    Backend obtiene noticia
           ↓
    Construye prompt para Claude
           ↓
    POST https://api.anthropic.com/v1/messages
           ↓
    Claude procesa y responde
           ↓
    Backend guarda resumen en noticia
           ↓
    Response con resumen
           ↓
    Frontend muestra resumen
```

### 3. Chat con IA
```
Usuario → Escribe mensaje
           ↓
    POST /api/ai/chat
           ↓
    Backend recupera historial
           ↓
    Agrega mensaje al historial
           ↓
    Envía todo el historial a Claude
           ↓
    Claude genera respuesta
           ↓
    Backend actualiza historial
           ↓
    Response con respuesta
           ↓
    Frontend muestra mensaje
```

---

## 🗂️ Estructura de Datos Optimizada (v2.4.0)

### Noticia (Schema) - Arquitectura Optimizada
```python
{
    "id": int,
    "titulo": str,              # 5-200 caracteres
    "contenido": str,           # mínimo 20 caracteres
    "seccion_id": int,          # FK a secciones
    "usuario_id": int,          # FK a usuarios (fuente de verdad)
    "autor_nombre": str,        # Calculado desde relación usuario
    "fecha": str,               # ISO format
    "resumen_ia": str | None,
    "sentiment_score": float | None,
    "keywords": List[str] | None,
    "proyecto_id": int | None,  # FK opcional
    "llm_id": int | None,       # FK opcional
    "estado": str               # "activo", "archivado", "eliminado"
}
```

### Usuario (Relaciones Optimizadas)
```python
{
    "id": int,                  # PK - Fuente de verdad
    "username": str,            # Único, usado para autor_nombre
    "email": str,               # Único
    "nombre_completo": str,
    "rol": str,                 # "admin", "editor", "viewer"
    "activo": bool,
    "noticias": List[Noticia]   # Relación 1:N optimizada
}
```

### Sección (Con Ordenamiento)
```python
{
    "id": int,
    "nombre": str,              # Ordenado alfabéticamente en frontend
    "descripcion": str,
    "color": str,
    "icono": str,
    "activo": bool,
    "noticias": List[Noticia]   # Relación 1:N
}
```

### Mensaje Chat (Schema)
```python
{
    "role": "user" | "assistant",
    "content": str
}
```

### Conversación
```python
{
    "conversacion_id": str (UUID),
    "mensajes": List[Mensaje],
    "timestamp": str
}
```

---

## 🔌 API Endpoints

### Noticias

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/api/noticias/` | GET | Listar noticias con filtros | No |
| `/api/noticias/{id}` | GET | Obtener noticia específica | No |
| `/api/noticias/` | POST | Crear noticia | No |
| `/api/noticias/{id}` | PUT | Actualizar noticia | No |
| `/api/noticias/{id}` | DELETE | Eliminar noticia | No |
| `/api/noticias/stats/resumen` | GET | Estadísticas | No |
| `/api/noticias/seed` | POST | Crear datos ejemplo | No |

### IA

| Endpoint | Método | Descripción | Auth |
|----------|--------|-------------|------|
| `/api/ai/chat` | POST | Chat conversacional | No |
| `/api/ai/analizar` | POST | Analizar noticia | No |
| `/api/ai/resumir/{id}` | POST | Generar resumen | No |
| `/api/ai/conversaciones/{id}` | GET | Ver conversación | No |
| `/api/ai/conversaciones/{id}` | DELETE | Eliminar conversación | No |

---

## 🛠️ Stack Tecnológico Detallado

### Backend
```
Python 3.11
├── FastAPI 0.109.0         # Framework web
├── Uvicorn 0.27.0          # ASGI server
├── Pydantic 2.5.3          # Validación de datos
├── Anthropic 0.18.1        # SDK de Claude
├── HTTPX 0.26.0            # Cliente HTTP async
└── Python-dotenv 1.0.0     # Variables de entorno
```

### Frontend
```
Node.js 18+
├── React 18.2.0            # UI library
├── Vite 5.0.8              # Build tool
├── Tailwind CSS 3.4.0      # CSS framework
└── Lucide React 0.263.1    # Iconos
```

### Infraestructura
```
Docker & Docker Compose      # Containerización
Nginx                         # Reverse proxy
PostgreSQL (opcional)         # Base de datos
```

---

## 🔒 Seguridad

### Implementado
- ✅ Validación de entrada con Pydantic
- ✅ CORS configurado
- ✅ Sanitización de datos
- ✅ Type hints en todo el código

### Para Producción
- [ ] Autenticación JWT
- [ ] Rate limiting
- [ ] API keys para endpoints sensibles
- [ ] HTTPS obligatorio
- [ ] Logging de accesos
- [ ] Backup automático

---

## 📊 Performance

### Optimizaciones Actuales
- Almacenamiento en memoria (muy rápido)
- Validación en schema (early return)
- Async/await en todas las operaciones I/O
- Paginación en listados

### Métricas Esperadas (desarrollo)
- Response time: < 100ms (sin IA)
- Response time: 2-5s (con IA)
- Throughput: 100+ req/s
- Memory usage: ~50MB base

---

## 🔄 Estados de la Aplicación

### Frontend
```javascript
{
  noticias: Array<Noticia>,
  vista: 'noticias' | 'crear' | 'chat',
  filtro: string,
  loading: boolean,
  error: string | null
}
```

### Backend
```python
{
  noticias_db: List[dict],      # Almacén de noticias
  conversaciones: Dict[str, List], # Historial de chats
  contador_id: int              # ID incremental
}
```

---

## 🌐 Deployment Strategies

### Desarrollo
```
Local Machine
├── Backend: http://localhost:8000
└── Frontend: http://localhost:5173
```

### Staging
```
Docker Compose
├── Backend Container
├── Frontend Container
└── Nginx Container
```

### Producción
```
Cloud Platform (Railway/Render/AWS)
├── Backend: API en servidor dedicado
├── Frontend: CDN para assets estáticos
├── Database: PostgreSQL managed
└── Cache: Redis para sesiones
```

---

## 📈 Escalabilidad

### Horizontal
- Múltiples instancias de FastAPI detrás de load balancer
- Redis para cache compartido
- PostgreSQL con read replicas

### Vertical
- Aumentar recursos de containers
- Optimizar queries
- Implementar índices en DB

---

## 🧪 Testing Strategy

```
tests/
├── unit/
│   ├── test_models.py       # Test schemas
│   ├── test_routers.py      # Test endpoints
│   └── test_services.py     # Test lógica
├── integration/
│   ├── test_api_flow.py     # Test flujos completos
│   └── test_ai_integration.py
└── e2e/
    └── test_user_flows.py   # Test end-to-end
```

---

## 🔄 CI/CD Pipeline

```
GitHub Push
    ↓
GitHub Actions
    ↓
┌─── Tests ───┐
│             │
│  ├─ Lint   │
│  ├─ Unit   │
│  └─ E2E    │
└─────┬──────┘
      ↓
   Build Docker
      ↓
   Push to Registry
      ↓
   Deploy to Server
      ↓
   Health Check
      ↓
   🎉 Done
```

---

## 📚 Referencias

- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **Claude API**: https://docs.anthropic.com
- **Tailwind CSS**: https://tailwindcss.com
- **Pydantic**: https://docs.pydantic.dev

---

**Última actualización:** 2025-10-01