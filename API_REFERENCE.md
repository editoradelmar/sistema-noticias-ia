# 📖 API Reference - Sistema de Noticias con IA v2.4.0

## 📋 Índice

- [Información General](#información-general)
- [Cambios v2.4.0](#cambios-v240)
- [Autenticación](#autenticación)
- [Endpoints de Autenticación](#endpoints-de-autenticación)
- [Endpoints de Noticias](#endpoints-de-noticias)
- [Endpoints de IA](#endpoints-de-ia)
- [Endpoints de Sistema](#endpoints-de-sistema)
- [Códigos de Estado](#códigos-de-estado)
- [Errores Comunes](#errores-comunes)

---

## 🌐 Información General

### Base URL
```
Desarrollo: http://localhost:8000
Producción: https://api.tu-dominio.com
```

### Formato de Respuestas
Todas las respuestas son en formato **JSON**.

### Autenticación
La mayoría de endpoints requieren autenticación JWT mediante header:
```
Authorization: Bearer <token>
```

### Documentación Interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🚀 Cambios v2.4.0

### 🔗 **Estructura de Datos Optimizada**
- **Campo `autor` eliminado** de requests y responses
- **`usuario_id` como fuente única** para relaciones
- **`autor_nombre` calculado** dinámicamente desde relación usuario
- **Secciones ordenadas alfabéticamente** en frontend

### ⚡ **Performance Mejorado**
- **Filtros optimizados** usando IDs integer en lugar de strings
- **Consultas más eficientes** con índices mejorados
- **Integridad referencial** garantizada por foreign keys

---

## 🔐 Autenticación

### Headers Requeridos

#### Autenticación OAuth2 (Login)
```http
Content-Type: application/x-www-form-urlencoded
```

#### Requests Autenticados
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
```

### Obtener Token

1. Login en `/api/auth/login`
2. Recibir `access_token` en response
3. Incluir en header `Authorization: Bearer <token>`
4. Token válido por 30 minutos

---

## 🔑 Endpoints de Autenticación

### 1. Registrar Usuario

Crea una nueva cuenta de usuario.

```http
POST /api/auth/register
```

**Body (JSON):**
```json
{
  "email": "usuario@ejemplo.com",
  "username": "usuario123",
  "password": "contraseña123",
  "nombre_completo": "Juan Pérez"
}
```

**Response 201 Created:**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "username": "usuario123",
  "nombre_completo": "Juan Pérez",
  "role": "viewer",
  "is_active": true,
  "created_at": "2025-10-14T10:00:00Z"
}
```

**Errores:**
- `400` - Email o username ya existen
- `422` - Validación fallida

---

### 2. Login (OAuth2)

Autentica usuario y devuelve token JWT.

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded
```

**Body (Form Data):**
```
username=usuario@ejemplo.com&password=contraseña123
```

**Response 200 OK:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "username": "usuario123",
    "nombre_completo": "Juan Pérez",
    "role": "viewer",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2025-10-14T10:00:00Z",
    "last_login": "2025-10-14T15:30:00Z"
  }
}
```

**Errores:**
- `401` - Credenciales incorrectas
- `400` - Usuario inactivo

---

### 3. Login (JSON Alternative)

Alternativa de login con JSON.

```http
POST /api/auth/login/json
Content-Type: application/json
```

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

**Response:** Igual que `/login`

---

### 4. Obtener Perfil

Obtiene información del usuario autenticado.

```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response 200 OK:**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "username": "usuario123",
  "nombre_completo": "Juan Pérez",
  "role": "viewer",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-14T10:00:00Z",
  "last_login": "2025-10-14T15:30:00Z"
}
```

**Errores:**
- `401` - Token inválido o expirado

---

### 5. Logout

Cierra sesión (simbólico, tokens JWT son stateless).

```http
POST /api/auth/logout
Authorization: Bearer <token>
```

**Response 200 OK:**
```json
{
  "success": true,
  "message": "Sesión cerrada correctamente"
}
```

---

### 6. Crear Admin (Development)

Crea un usuario administrador. Solo para desarrollo.

```http
POST /api/auth/create-admin
Content-Type: application/json
```

**Body:**
```json
{
  "email": "admin@sistema.com",
  "username": "admin",
  "password": "admin123456",
  "nombre_completo": "Administrador"
}
```

**Response 201 Created:**
```json
{
  "id": 1,
  "email": "admin@sistema.com",
  "username": "admin",
  "role": "admin",
  "is_superuser": true
}
```

---

## 📰 Endpoints de Noticias

### 1. Listar Noticias (Público)

Obtiene lista de noticias con filtros opcionales.

```http
GET /api/noticias/?categoria={categoria}&limite={limite}&offset={offset}
```

**Query Parameters:**
- `categoria` (opcional): tecnologia, desarrollo, ia, negocios, ciencia, general
- `limite` (opcional, default=100): Número máximo de resultados (1-100)
- `offset` (opcional, default=0): Offset para paginación

**Ejemplo:**
```http
GET /api/noticias/?categoria=tecnologia&limite=10&offset=0
```

**Response 200 OK:**
```json
[
  {
    "id": 1,
    "titulo": "FastAPI supera a Flask",
    "contenido": "Según estadísticas...",
    "seccion_id": 1,
    "autor_nombre": "admin",
    "fecha": "2025-10-14T10:00:00Z",
    "resumen_ia": "FastAPI es ahora el framework...",
    "sentiment_score": null,
    "keywords": null,
    "usuario_id": 1,
    "proyecto_id": null,
    "estado": "activo"
  }
]
```

---

### 2. Obtener Noticia (Público)

Obtiene una noticia específica por ID.

```http
GET /api/noticias/{id}
```

**Ejemplo:**
```http
GET /api/noticias/1
```

**Response 200 OK:**
```json
{
  "id": 1,
  "titulo": "FastAPI supera a Flask",
  "contenido": "Según estadísticas recientes...",
  "seccion_id": 1,
  "autor_nombre": "admin",
  "fecha": "2025-10-14T10:00:00Z",
  "resumen_ia": "FastAPI es ahora...",
  "sentiment_score": null,
  "keywords": null,
  "usuario_id": 1,
  "proyecto_id": null,
  "estado": "activo"
}
```

**Errores:**
- `404` - Noticia no encontrada

---

### 3. Crear Noticia (Auth: Admin/Editor)

Crea una nueva noticia.

```http
POST /api/noticias/
Authorization: Bearer <token>
Content-Type: application/json
```

**Body:**
```json
{
  "titulo": "Mi primera noticia",
  "contenido": "Este es el contenido de la noticia con mínimo 20 caracteres.",
  "seccion_id": 1,
  "proyecto_id": null,
  "llm_id": null,
  "estado": "activo"
}
```

**Validaciones:**
- `titulo`: 5-200 caracteres
- `contenido`: mínimo 20 caracteres
- `seccion_id`: ID de sección válida
- `usuario_id`: se toma automáticamente del usuario autenticado

**Response 201 Created:**
```json
{
  "id": 5,
  "titulo": "Mi primera noticia",
  "contenido": "Este es el contenido...",
  "seccion_id": 1,
  "autor_nombre": "juan_editor",
  "fecha": "2025-10-14T16:23:34Z",
  "resumen_ia": null,
  "usuario_id": 1,
  "estado": "activo"
}
```

**Errores:**
- `401` - No autenticado
- `403` - Rol insuficiente (solo admin/editor)
- `422` - Validación fallida

---

### 4. Actualizar Noticia (Auth: Admin/Owner)

Actualiza una noticia existente.

```http
PUT /api/noticias/{id}
Authorization: Bearer <token>
Content-Type: application/json
```

**Permisos:**
- Admin: puede editar cualquier noticia
- Editor: solo sus propias noticias

**Body:**
```json
{
  "titulo": "Título actualizado",
  "contenido": "Contenido actualizado..."
}
```

**Response 200 OK:**
```json
{
  "id": 5,
  "titulo": "Título actualizado",
  "contenido": "Contenido actualizado...",
  "categoria": "tecnologia",
  "fecha": "2025-10-14T16:30:00Z"
}
```

**Errores:**
- `401` - No autenticado
- `403` - Sin permisos para editar
- `404` - Noticia no encontrada

---

### 5. Eliminar Noticia (Auth: Admin/Owner)

Elimina una noticia.

```http
DELETE /api/noticias/{id}
Authorization: Bearer <token>
```

**Permisos:**
- Admin: puede eliminar cualquier noticia
- Editor: solo sus propias noticias

**Response 200 OK:**
```json
{
  "success": true,
  "message": "Noticia 5 eliminada correctamente"
}
```

**Errores:**
- `401` - No autenticado
- `403` - Sin permisos para eliminar
- `404` - Noticia no encontrada

---

### 6. Estadísticas (Público)

Obtiene estadísticas generales del sistema.

```http
GET /api/noticias/stats/resumen
```

**Response 200 OK:**
```json
{
  "total_noticias": 50,
  "noticias_por_categoria": {
    "tecnologia": 20,
    "desarrollo": 15,
    "ia": 10,
    "negocios": 3,
    "ciencia": 2
  },
  "noticias_con_ia": 30,
  "ultimas_actualizaciones": [
    "Mi primera noticia",
    "FastAPI supera a Flask",
    "Claude 4 establece récord"
  ]
}
```

---

### 7. Cargar Datos de Ejemplo (Público)

Crea noticias de ejemplo para testing.

```http
POST /api/noticias/seed
```

**Response 200 OK:**
```json
{
  "success": true,
  "message": "Se crearon 3 noticias de ejemplo",
  "data": {
    "total_noticias": 3
  }
}
```

---

## 🤖 Endpoints de IA

### 1. Chat con IA (Público)

Chat conversacional con Claude.

```http
POST /api/ai/chat
Content-Type: application/json
```

**Body:**
```json
{
  "mensaje": "Resume las noticias de tecnología",
  "conversacion_id": "uuid-opcional",
  "contexto": "Contexto adicional opcional"
}
```

**Response 200 OK:**
```json
{
  "respuesta": "Las noticias de tecnología más relevantes son...",
  "conversacion_id": "550e8400-e29b-41d4-a716-446655440000",
  "tokens_usados": 150
}
```

**Modo de Funcionamiento:**
- Con créditos API: Respuesta de Claude real
- Sin créditos: Respuesta simulada basada en keywords

---

### 2. Generar Resumen (Público)

Genera resumen detallado de una noticia.

```http
POST /api/ai/resumir/{noticia_id}
```

**Ejemplo:**
```http
POST /api/ai/resumir/2
```

**Response 200 OK:**
```json
{
  "noticia_id": 2,
  "resumen": "El modelo Claude Sonnet 4.5 ha demostrado capacidades superiores...",
  "puntos_clave": [
    "Claude 4.5 supera benchmarks anteriores",
    "Mejoras en razonamiento lógico",
    "Optimización de generación de código"
  ],
  "longitud_original": 250,
  "longitud_resumen": 80
}
```

**Efecto Secundario:**
- El resumen se guarda en `noticias.resumen_ia`

**Errores:**
- `404` - Noticia no encontrada

---

### 3. Analizar Noticia (Público)

Realiza análisis específico de una noticia.

```http
POST /api/ai/analizar
Content-Type: application/json
```

**Body:**
```json
{
  "noticia_id": 2,
  "tipo_analisis": "resumen",
  "idioma_destino": "ingles"
}
```

**Tipos de Análisis:**
- `resumen` - Resumen conciso
- `sentiment` - Análisis de sentimiento
- `keywords` - Extracción de palabras clave
- `traduccion` - Traducción a otro idioma

**Response 200 OK:**
```json
{
  "noticia_id": 2,
  "tipo_analisis": "resumen",
  "resultado": "Análisis detallado...",
  "metadata": {
    "titulo_noticia": "Claude 4...",
    "timestamp": "2025-10-14T10:00:00Z"
  }
}
```

---

### 4. Obtener Conversación (Público)

Recupera historial de una conversación.

```http
GET /api/ai/conversaciones/{conversacion_id}
```

**Response 200 OK:**
```json
{
  "conversacion_id": "550e8400-e29b-41d4-a716-446655440000",
  "mensajes": [
    {
      "role": "user",
      "content": "Hola"
    },
    {
      "role": "assistant",
      "content": "¡Hola! ¿En qué puedo ayudarte?"
    }
  ],
  "total_mensajes": 2
}
```

**Errores:**
- `404` - Conversación no encontrada

---

### 5. Eliminar Conversación (Público)

Elimina historial de conversación.

```http
DELETE /api/ai/conversaciones/{conversacion_id}
```

**Response 200 OK:**
```json
{
  "success": true,
  "message": "Conversación eliminada"
}
```

---

## ⚙️ Endpoints de Sistema

### 1. Health Check

Verifica estado del servidor y base de datos.

```http
GET /health
```

**Response 200 OK:**
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "database": "connected",
  "timestamp": "2025-10-14T16:30:00Z"
}
```

---

### 2. Info de la API

Información general de la API.

```http
GET /
```

**Response 200 OK:**
```json
{
  "app_name": "Sistema de Noticias con IA",
  "version": "2.1.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## 📊 Códigos de Estado

### Exitosos (2xx)

| Código | Significado | Uso |
|--------|-------------|-----|
| `200` | OK | Request exitoso |
| `201` | Created | Recurso creado |

### Errores del Cliente (4xx)

| Código | Significado | Cuándo Ocurre |
|--------|-------------|---------------|
| `400` | Bad Request | Datos inválidos |
| `401` | Unauthorized | Sin autenticación o token inválido |
| `403` | Forbidden | Sin permisos |
| `404` | Not Found | Recurso no existe |
| `422` | Unprocessable Entity | Validación Pydantic fallida |

### Errores del Servidor (5xx)

| Código | Significado | Cuándo Ocurre |
|--------|-------------|---------------|
| `500` | Internal Server Error | Error inesperado |

---

## 🐛 Errores Comunes

### Error 401: Token Inválido

**Causa:** Token expirado o mal formado

**Response:**
```json
{
  "detail": "Token inválido"
}
```

**Solución:**
1. Verificar que el token existe
2. Verificar formato: `Bearer <token>`
3. Si expiró (30 min), hacer login nuevamente

---

### Error 403: Sin Permisos

**Causa:** Usuario no tiene el rol necesario

**Response:**
```json
{
  "detail": "Solo admin y editor pueden crear noticias"
}
```

**Solución:**
- Verificar rol del usuario actual
- Contactar admin para cambio de rol

---

### Error 422: Validación Fallida

**Causa:** Datos no cumplen validación Pydantic

**Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "titulo"],
      "msg": "ensure this value has at least 5 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

**Solución:**
- Revisar campo indicado en `loc`
- Ajustar dato según `msg`

---

## 📝 Ejemplos de Uso

### Ejemplo Completo: Flujo de Usuario

```bash
# 1. Registrar usuario
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@test.com",
    "username": "nuevo123",
    "password": "password123"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=nuevo@test.com&password=password123"

# Response:
# {
#   "access_token": "eyJhbGci...",
#   "token_type": "bearer",
#   "user": {...}
# }

# 3. Guardar token
TOKEN="eyJhbGci..."

# 4. Obtener perfil
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# 5. Ver noticias (público)
curl -X GET http://localhost:8000/api/noticias/

# 6. Crear noticia (requiere admin/editor)
curl -X POST http://localhost:8000/api/noticias/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Mi noticia",
    "contenido": "Contenido con más de 20 caracteres...",
    "categoria": "tecnologia"
  }'

# 7. Generar resumen
curl -X POST http://localhost:8000/api/ai/resumir/1

# 8. Chat con IA
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "Resume las noticias de hoy"
  }'
```

---

## 📚 Referencias

- [Swagger UI](http://localhost:8000/docs) - Documentación interactiva
- [ReDoc](http://localhost:8000/redoc) - Documentación alternativa
- [AUTH_GUIDE.md](./AUTH_GUIDE.md) - Guía de autenticación
- [README.md](./README.md) - Documentación general

---

**📖 Documento actualizado:** 2025-10-14  
**🔖 Versión API:** 2.1.0  
**📧 Soporte:** soporte@ejemplo.com
