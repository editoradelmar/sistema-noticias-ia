# 🚀 Sistema de Noticias con IA v2.3.1

Sistema profesional de gestión de noticias con **administración de usuarios avanzada**, **jerarquía editorial**, **paginación optimizada**, **PostgreSQL**, **sistema de maestros multi-LLM** e integración de inteligencia artificial avanzada usando **FastAPI + React + Gemini/Claude**.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.118.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12.10-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat)](https://ai.google.dev)
[![Claude](https://img.shields.io/badge/Claude-Sonnet_3.5-7C3AED?style=flat)](https://anthropic.com)

> **🎉 FASE 1 COMPLETADA - Administración de Usuarios v2.4.0** 
> Sistema completo con administración avanzada de usuarios, jerarquía editorial funcional, paginación optimizada y mejoras de performance significativas

---

## 📋 Características Principales

### 🔐 Autenticación y Administración
- ✅ **Autenticación JWT** con tokens seguros y refresh tokens
- ✅ **Sistema de roles jerárquico** (Admin, Director, Jefe Sección, Redactor, Viewer)
- ✅ **Administración de usuarios avanzada** con formularios completos
- ✅ **Jerarquía editorial funcional** con vista de árbol organizacional
- ✅ **Control de acceso granular** por endpoint y recursos
- ✅ **Gestión de supervisores** y equipos editoriales
- ✅ **Límites de tokens configurables** por usuario
- ✅ **Encriptación bcrypt** para contraseñas
- ✅ **Sesiones persistentes** con localStorage

### 📰 Gestión Avanzada de Noticias
- ✅ **CRUD completo** con PostgreSQL y transacciones
- ✅ **Paginación inteligente** con filtros diarios por defecto
- ✅ **Navegación optimizada** (6/12/24/48 items por página)
- ✅ **Sistema de proyectos** para organización
- ✅ **Secciones configurables** con ordenamiento alfabético
- ✅ **Búsqueda y filtrado** optimizado por usuario_id
- ✅ **Vinculación usuario-contenido** con integridad referencial
- ✅ **Estadísticas y métricas** del sistema
- ✅ **Arquitectura de datos optimizada** (v2.4.0)

### 🤖 Sistema de IA Multi-Proveedor
- ✅ **Maestro de LLMs** (Gemini 2.0, Claude 3.5, GPT-4)
- ✅ **Generación temporal y persistente** de contenido
- ✅ **Multi-salida optimizada** (Web, Impreso, Redes Sociales)
- ✅ **Prompts personalizables** con variables dinámicas
- ✅ **Estilos configurables** (tono, formato, longitud)
- ✅ **Chat conversacional** con contexto persistente
- ✅ **Tracking de tokens** y costos por modelo

### 🎨 Interfaz Moderna y Profesional
- ✅ **React 18 + Tailwind CSS** con componentes reutilizables
- ✅ **Panel de administración completo** con 5 componentes especializados
- ✅ **Vista de jerarquía organizacional** en formato árbol
- ✅ **Formularios avanzados** con validación en tiempo real
- ✅ **Paginación profesional** con controles inteligentes
- ✅ **Modo oscuro/claro** automático y manual
- ✅ **Diseño responsive** para móvil y desktop
- ✅ **Indicadores de carga** y feedback visual
- ✅ **Animaciones fluidas** y micro-interacciones
- ✅ **Interfaz completamente en español**
- ✅ **Drag & Drop de archivos** (PDF, TXT, DOC, DOCX) con extracción automática
- ✅ **Generación inteligente de títulos** basada en contenido del archivo
- ✅ **Límites extendidos** de contenido (hasta 10,000 caracteres)
- ✅ **Ordenamiento alfabético** en dropdowns de secciones (v2.4.0)

### 🏗️ Arquitectura Optimizada v2.4.0
- ✅ **Sistema de administración completo** con 1,802 líneas de código nuevo
- ✅ **Migración exitosa** de 13 usuarios sin pérdida de datos
- ✅ **Integridad referencial** mejorada con usuario_id como fuente única
- ✅ **Performance optimizado** con filtros basados en índices integer
- ✅ **Eliminación de redundancias** en la estructura de datos
- ✅ **Código limpio** sin archivos temporales de diagnóstico
- ✅ **Consistencia de datos** garantizada por foreign keys
- ✅ **Escalabilidad mejorada** para futuras funcionalidades
- ✅ **Documentación completa** con 6 documentos técnicos detallados

---

## 🛠️ Stack Tecnológico Completo

### Backend
```
Python 3.11+
├── FastAPI 0.118.0           # Framework web
├── Uvicorn 0.37.0            # Servidor ASGI
├── PostgreSQL 12.10          # Base de datos principal
├── SQLAlchemy 2.0.44         # ORM con soporte async
├── Alembic 1.13.1            # Migraciones de BD
├── Pydantic 2.11.9           # Validación y serialización
├── google-generativeai       # SDK Gemini 2.0
├── anthropic 0.69.0          # SDK Claude 3.5
├── python-jose 3.3.0         # JWT tokens
├── passlib 1.7.4             # Hash passwords
├── bcrypt 4.0.1              # Encriptación
└── pytest 7.4.4             # Testing framework
```

### Frontend
```
Node.js 18+
├── React 18.2.0              # UI Library
├── Vite 5.0.8                # Build tool moderno
├── Tailwind CSS 3.4.0        # Utilidad CSS
├── Lucide React 0.263.1      # Iconos modernos
├── Axios 1.6.0               # Cliente HTTP
└── React Router 6.8.0        # Navegación SPA
```

### Inteligencia Artificial
```
Multi-LLM Support
├── Google Gemini 2.0 Flash    # Modelo principal
├── Anthropic Claude 3.5       # Modelo secundario 
├── OpenAI GPT-4 (opcional)    # Modelo terciario
├── Tracking de tokens         # Monitoreo de uso
└── Sistema de fallback        # Alta disponibilidad
```

### Base de Datos
```
PostgreSQL 12.10
├── 6 tablas relacionales
├── Índices optimizados
├── Foreign keys
└── Cascadas configuradas
```

---

## 📁 Estructura del Proyecto

```
sistema-noticias-ia/
├── README.md                    ⭐ Este archivo
├── PROJECT_CONTEXT.md           🧠 Contexto completo
├── ARCHITECTURE.md              📐 Arquitectura
├── QUICKSTART.md                🚀 Guía rápida
├── .env.example                 📝 Template config
│
├── backend/                     🐍 API FastAPI
│   ├── main.py                  ⭐ App principal
│   ├── config.py                ⚙️ Configuración
│   ├── requirements.txt         📦 Dependencias
│   ├── .env                     🔐 Variables (no commit)
│   │
│   ├── core/                    🔧 Núcleo
│   │   └── database.py          💾 Conexión PostgreSQL
│   │
│   ├── models/                  📊 Modelos
│   │   ├── schemas.py           📝 Pydantic schemas
│   │   └── orm_models.py        🗄️ SQLAlchemy models
│   │
│   ├── routers/                 🛣️ Endpoints
│   │   ├── auth.py              🔐 Autenticación
│   │   ├── noticias.py          📰 CRUD noticias
│   │   └── ai.py                🤖 IA Claude
│   │
│   ├── utils/                   🔧 Utilidades
│   │   └── security.py          🔒 JWT y hash
│   │
│   └── venv/                    🐍 Entorno virtual
│
└── frontend/                    ⚛️ React App
    ├── package.json             📦 Dependencias
    ├── vite.config.js           ⚙️ Config Vite
    ├── tailwind.config.js       🎨 Config Tailwind
    │
    └── src/
        ├── main.jsx             🚪 Entry point
        ├── App.jsx              ⭐ App principal
        ├── index.css            🎨 Estilos globales
        │
        ├── components/          🧩 Componentes
        │   ├── Login.jsx        🔐 Pantalla login
        │   ├── Register.jsx     📝 Registro
        │   └── Header.jsx       📌 Header con user
        │
        ├── context/             🌐 Context API
        │   └── AuthContext.jsx  🔐 Auth state
        │
        └── services/            🔌 API
            └── api.js           📡 HTTP client
```

---


## 🐙 Integración y Uso de Git/GitHub

### 1️⃣ Inicializar y conectar tu repositorio

```bash
git init
git remote add origin https://github.com/<usuario>/<repositorio>.git
git add .
git commit -m "Primer commit: estructura base"
git branch -M main
git push -u origin main
```

### 2️⃣ Flujo recomendado de trabajo

- Crea una rama para cada feature o fix:
  ```bash
  git checkout -b feature/nombre-feature
  ```
- Haz commits descriptivos y atómicos:
  ```bash
  git commit -m "feat: agrega login con JWT"
  ```
- Sincroniza cambios frecuentemente:
  ```bash
  git pull origin main
  git push origin feature/nombre-feature
  ```
- Abre un Pull Request en GitHub y sigue la guía de contribución.

### 3️⃣ Referencias útiles

- [Guía de Contribución](./CONTRIBUTING.md)
- [Guía Rápida de Inicio](./QUICKSTART.md)

---

## 🚀 Instalación Rápida (5 minutos)

### Prerrequisitos

```bash
✅ Python 3.11+
✅ Node.js 18+
✅ PostgreSQL 12+
✅ Git
✅ API Key de Gemini (recomendado) o Claude (opcional)
```

### 1️⃣ Clonar y Configurar

```bash
# Clonar repositorio
git clone <repository-url>
cd sistema-noticias-ia

# Copiar configuraciones de ejemplo
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2️⃣ Base de Datos PostgreSQL

```sql
-- Conectar a PostgreSQL como superusuario
psql -U postgres

-- Crear base de datos y usuario
CREATE DATABASE noticias_ia;
CREATE USER openpg WITH PASSWORD 'openpgpwd';
GRANT ALL PRIVILEGES ON DATABASE noticias_ia TO openpg;
\q
```

### 3️⃣ Backend (FastAPI)

```bash
cd backend

# Crear y activar entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Editar backend/.env:
# - DATABASE_URL=postgresql://openpg:openpgpwd@localhost/noticias_ia
# - SECRET_KEY=tu_secret_key_super_segura
# - GEMINI_API_KEY=tu_api_key_de_gemini (opcional)

# Ejecutar migraciones
python -m alembic upgrade head

# Crear usuario administrador
python create_admin.py

# Iniciar servidor de desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4️⃣ Frontend (React)

```bash
# En nueva terminal
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
# Editar frontend/.env:
# - VITE_API_BASE=http://localhost:8000/api
# - VITE_DEFAULT_LLM_PROVEEDOR=Google
# - VITE_DEFAULT_LLM_MODELO_ID=gemini-2.0-flash-exp

# Iniciar servidor de desarrollo
npm run dev
```

### 5️⃣ Verificar Instalación

```bash
✅ Backend: http://localhost:8000/docs (FastAPI Swagger)
✅ Frontend: http://localhost:5173 (React App)
✅ Login: admin@sistema.com / admin123
```

> 📚 **Guías detalladas**: Ver [QUICKSTART.md](./QUICKSTART.md) para instalación paso a paso
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Crear tablas en PostgreSQL
# Las tablas se crean automáticamente al iniciar
```

**Archivo `.env` (backend):**
```bash
# General
APP_NAME="Sistema de Noticias con IA"
VERSION="2.1.0"
DEBUG=True

# PostgreSQL
DATABASE_URL=postgresql://openpg:openpgpwd@localhost:5432/noticias_ia

# JWT Secret (generar con: openssl rand -hex 32)
SECRET_KEY=tu_clave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Claude API (opcional)
ANTHROPIC_API_KEY=sk-ant-api-key-aqui

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### 4️⃣ Configurar Frontend

```bash
cd ../frontend

# Instalar dependencias
npm install

# Iniciar en desarrollo
npm run dev
```

### 5️⃣ Crear Usuario Admin Inicial

```bash
cd backend

# Ejecutar script interactivo
python create_admin.py

# O usar los usuarios de prueba (ver abajo)
```

---

## 🎯 Sistema de Maestros Multi-LLM

> **🚀 Funcionalidad Principal v2.3.0** - Sistema completo de gestión de IA con múltiples proveedores

### Arquitectura de 5 Maestros

```
🤖 LLM Maestro      ➜ Gestiona modelos IA (Gemini, Claude, GPT-4)
📝 Prompt Maestro   ➜ Plantillas reutilizables con variables dinámicas  
🎨 Estilo Maestro   ➜ Directivas de tono, formato y longitud
📋 Secciones        ➜ Organización de contenido (reemplazo de categorías)
📤 Salida Maestro   ➜ Canales optimizados (Web, Impreso, Redes Sociales)
```

### Flujo de Generación Multi-Salida

```
1. 📝 Usuario crea noticia con contenido base
2. 🎯 Selecciona secciones y salidas deseadas  
3. 🤖 Sistema genera automáticamente contenido optimizado por canal:
   ├── 🌐 Web: SEO optimizado, sumario, cuerpo extenso
   ├── 📰 Impreso: Formato tradicional, espacio limitado
   ├── 📱 Twitter: 280 caracteres, hashtags relevantes
   ├── 📸 Instagram: Visual, emojis, engagement
   └── 📺 Redes: Copy atractivo para compartir
4. ✅ Revisión y publicación con un clic
```

### Características Avanzadas

- **🔄 Generación Temporal**: Vista previa sin persistir en BD
- **🎛️ Configuración Granular**: Tokens, costos, límites por modelo
- **📊 Tracking en Tiempo Real**: Uso de tokens, costos diarios
- **🔧 Sistema de Fallback**: Alta disponibilidad entre proveedores
- **🎨 Personalización Completa**: Prompts, estilos y formatos editables

### Gestión de Modelos LLM

| Proveedor | Modelo | Tokens/día | Costo | Estado |
|-----------|--------|------------|-------|--------|
| Google | Gemini 2.0 Flash | 2M | Gratis | ✅ Principal |
| Anthropic | Claude 3.5 Sonnet | 1M | $0.03/1K | ✅ Secundario |
| OpenAI | GPT-4 Turbo | 500K | $0.01/1K | 🟡 Opcional |

---

## ▶️ Ejecutar el Proyecto

### Opción A: Desarrollo (2 terminales)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
uvicorn main:app --reload

# Disponible en:
# 🌐 API: http://localhost:8000
# 📚 Docs: http://localhost:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev

# Disponible en:
# 🌐 App: http://localhost:5173
```

### Opción B: Docker (próximamente)

```bash
docker-compose up --build
```

---

## 👥 Usuarios de Prueba

El sistema incluye 3 usuarios preconfigurados:

| Email | Password | Rol | Permisos |
|-------|----------|-----|----------|
| `admin@sistema.com` | `admin123456` | **admin** | ✅ Acceso total |
| `editor@sistema.com` | `editor123` | **editor** | ✅ Crear/editar sus noticias |
| `viewer@sistema.com` | `viewer123` | **viewer** | 👁️ Solo lectura |

**Acceso rápido en login:**
- En la pantalla de login verás botones para cada usuario
- Click en el rol deseado para login automático

---

## 🔐 Sistema de Autenticación

### Flujo de Autenticación

```
1. Usuario envía credenciales (email + password)
2. Backend valida en PostgreSQL
3. Genera JWT token (válido 30 min)
4. Frontend guarda token en localStorage
5. Cada request incluye token en header
6. Backend valida y autoriza según rol
```

### Roles y Permisos

| Endpoint | Admin | Editor | Viewer |
|----------|-------|--------|--------|
| `GET /api/noticias/` | ✅ | ✅ | ✅ |
| `GET /api/noticias/{id}` | ✅ | ✅ | ✅ |
| `POST /api/noticias/` | ✅ | ✅ | ❌ |
| `PUT /api/noticias/{id}` | ✅ | 🟡* | ❌ |
| `DELETE /api/noticias/{id}` | ✅ | 🟡* | ❌ |
| `POST /api/ai/resumir/{id}` | ✅ | ✅ | ✅ |
| `POST /api/ai/chat` | ✅ | ✅ | ✅ |

🟡* Editor solo puede editar/eliminar **sus propias noticias**

### Endpoints de Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | Registrar usuario nuevo |
| `POST` | `/api/auth/login` | Login (OAuth2 form) |
| `POST` | `/api/auth/login/json` | Login (JSON) |
| `GET` | `/api/auth/me` | Obtener perfil usuario |
| `POST` | `/api/auth/logout` | Cerrar sesión |

---

## 📖 Guía de Uso

### 1. Primer Inicio

1. Abre `http://localhost:5173`
2. Verás la pantalla de **Login**
3. Click en botón "Admin" para acceso rápido
4. ✅ Ya estás dentro del sistema

### 2. Vista de Noticias

```
📰 Noticias
├─ 🔍 Barra de búsqueda
├─ 🔄 Botón actualizar
├─ ⚡ Cargar ejemplos (si está vacío)
└─ 📋 Lista de tarjetas de noticias
    ├─ 📌 Categoría con color
    ├─ 📝 Título y contenido
    ├─ 💜 Resumen IA (si existe)
    ├─ ⚡ Botón generar resumen
    └─ 🗑️ Botón eliminar (solo admin)
```

### 3. Crear Noticia

Solo visible para **Admin** y **Editor**:

#### 📁 Opción 1: Subir Archivo (Nuevo)
1. Click en pestaña "✨ Crear"
2. **Arrastra un archivo** a la zona de drag & drop o **haz clic para seleccionar**
   - **Formatos soportados**: PDF, TXT, DOC, DOCX
   - **Tamaño máximo**: 10MB
3. ✅ **Título y contenido se llenan automáticamente**:
   - **Título**: Extraído inteligentemente del contenido
   - **Contenido**: Texto completo del archivo (hasta 10,000 caracteres)
4. **Revisa y edita** los campos si es necesario
5. Selecciona **Sección** y **configuración adicional**
6. Click "Publicar Noticia"

#### ✏️ Opción 2: Escritura Manual
1. Click en pestaña "✨ Crear"
2. Completa el formulario manualmente:
   - **Título**: Mínimo 5 caracteres, máximo 200
   - **Contenido**: Mínimo 20 caracteres, máximo 10,000
   - **Sección**: Selecciona una (obligatorio)
3. Click "Publicar Noticia"
4. ✅ Noticia creada y vinculada a tu usuario

**💡 Características avanzadas:**
- **Contador de caracteres** en tiempo real
- **Validación inteligente** de archivos
- **Generación automática de títulos** basada en contenido
- **Múltiples formatos** de archivo soportados

### 4. Generar Resumen con IA

Disponible para **todos los roles**:

1. En cualquier tarjeta de noticia
2. Click "⚡ Generar Resumen con IA"
3. Espera 1-2 segundos
4. ✅ Verás cuadro morado con el resumen
5. El resumen se guarda en PostgreSQL

**Modos de funcionamiento:**
- 🤖 **Con créditos API**: Resumen inteligente de Claude
- 🔄 **Sin créditos**: Resumen simulado (primeras 30 palabras)

### 5. Chat con IA

1. Click en pestaña "💬 Chat IA"
2. Escribe tu pregunta
3. Presiona Enter o click "Enviar"
4. ✅ Claude responde en tiempo real
5. El historial se mantiene en la sesión

**Ejemplos de preguntas:**
```
- "Resume las últimas noticias"
- "¿Qué temas son tendencia?"
- "Háblame sobre inteligencia artificial"
```

### 6. Logout

- Click en botón rojo (🚪) en el header
- ✅ Sesión cerrada
- Vuelves a la pantalla de login

---

## 🔧 API Reference

### Autenticación

#### Registrar Usuario
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "nuevo@email.com",
  "username": "usuario123",
  "password": "contraseña123",
  "nombre_completo": "Juan Pérez"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@sistema.com&password=admin123456
```

#### Obtener Perfil
```bash
GET /api/auth/me
Authorization: Bearer <token>
```

### Noticias

#### Listar Noticias (Público)
```bash
GET /api/noticias/?categoria=tecnologia&limite=10&offset=0
```

#### Crear Noticia (Auth: Admin/Editor)
```bash
POST /api/noticias/
Authorization: Bearer <token>
Content-Type: application/json

{
  "titulo": "Nueva noticia",
  "contenido": "Contenido de la noticia...",
  "categoria": "tecnologia",
  "autor": "Juan Pérez"
}
```

#### Actualizar Noticia (Auth: Admin/Owner)
```bash
PUT /api/noticias/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "titulo": "Título actualizado",
  "contenido": "Nuevo contenido..."
}
```

#### Eliminar Noticia (Auth: Admin/Owner)
```bash
DELETE /api/noticias/{id}
Authorization: Bearer <token>
```

### IA

#### Generar Resumen (Público)
```bash
POST /api/ai/resumir/{id}

# Response:
{
  "noticia_id": 2,
  "resumen": "Resumen de la noticia...",
  "puntos_clave": ["punto 1", "punto 2"],
  "longitud_original": 250,
  "longitud_resumen": 80
}
```

#### Chat con IA (Público)
```bash
POST /api/ai/chat
Content-Type: application/json

{
  "mensaje": "Resume las noticias de tecnología",
  "conversacion_id": "uuid-opcional",
  "contexto": "Contexto adicional opcional"
}
```

---

## 🗄️ Esquema de Base de Datos

```sql
-- Usuarios (autenticación)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(200),
    role VARCHAR(20) DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Noticias
CREATE TABLE noticias (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    autor VARCHAR(100) DEFAULT 'Sistema',
    resumen_ia TEXT,
    usuario_id INTEGER REFERENCES usuarios(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Proyectos
CREATE TABLE proyectos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Conversaciones IA
CREATE TABLE conversaciones_ia (
    id SERIAL PRIMARY KEY,
    conversacion_id VARCHAR(100) UNIQUE NOT NULL,
    mensajes JSON NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Documentos de contexto
CREATE TABLE documentos_contexto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    proyecto_id INTEGER REFERENCES proyectos(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla intermedia (many-to-many)
CREATE TABLE noticia_proyecto (
    noticia_id INTEGER REFERENCES noticias(id),
    proyecto_id INTEGER REFERENCES proyectos(id),
    PRIMARY KEY (noticia_id, proyecto_id)
);
```

---

## 🧪 Testing

### Backend
```bash
cd backend
pytest -v

# Con coverage
pytest --cov=. --cov-report=html
```

### Frontend
```bash
cd frontend
npm test
```

---

## 🐛 Troubleshooting

### Backend no inicia

**Error: `ModuleNotFoundError`**
```bash
# Solución:
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Error: `Connection to PostgreSQL failed`**
```bash
# Verificar que PostgreSQL está corriendo:
# Windows:
services.msc → PostgreSQL

# Linux:
sudo systemctl status postgresql

# Verificar credenciales en .env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/noticias_ia
```

### Frontend no conecta con backend

**Error: `Network Error` o `Failed to fetch`**
```bash
# Verificar que backend está corriendo:
curl http://localhost:8000/health

# Verificar CORS en backend/config.py:
ALLOWED_ORIGINS = "http://localhost:5173,..."
```

### Error 401 Unauthorized

```bash
# El token expiró (30 minutos)
# Solución: Logout y login de nuevo

# O verificar que el token se envía:
# Frontend debe incluir:
Authorization: Bearer <token>
```

### Error 403 Forbidden

```bash
# No tienes permisos para esa acción
# Verificar tu rol:
# - Viewer: solo lectura
# - Editor: crear/editar propias noticias
# - Admin: acceso total
```

---

## 📚 Documentación Adicional

  - 📐 [ARCHITECTURE.md](./ARCHITECTURE.md) - Arquitectura del sistema
  - 🚀 [QUICKSTART.md](./QUICKSTART.md) - Guía rápida 5 minutos
  - 🧠 [PROJECT_CONTEXT.md](./PROJECT_CONTEXT.md) - Contexto completo
- 📖 [API Docs](http://localhost:8000/docs) - Swagger UI (ejecutar backend)

---

## 🚀 Deployment

### Preparación para Producción

1. **Configurar variables de entorno**
```bash
DEBUG=False
SECRET_KEY=<nueva-clave-segura-64-caracteres>
DATABASE_URL=<postgresql-produccion>
ALLOWED_ORIGINS=https://tu-dominio.com
```

2. **Build del frontend**
```bash
cd frontend
npm run build
# Archivos en dist/
```

3. **Configurar HTTPS**
- Usar Nginx o Caddy como reverse proxy
- Certificados SSL con Let's Encrypt

4. **Base de datos**
- PostgreSQL en servicio administrado (AWS RDS, Railway, etc.)
- Configurar backups automáticos

### Opciones de Deploy

| Plataforma | Backend | Frontend | BD |
|------------|---------|----------|-----|
| **Railway** | ✅ | ✅ | ✅ PostgreSQL |
| **Render** | ✅ | ✅ | ✅ PostgreSQL |
| **Vercel** | 🟡 Serverless | ✅ | - |
| **Heroku** | ✅ | ✅ | ✅ PostgreSQL |
| **AWS** | ✅ EC2/ECS | ✅ S3/CloudFront | ✅ RDS |

---

## 🎯 Roadmap y Estado del Proyecto

### ✅ v2.3.0 - COMPLETADA (Octubre 2025)
- ✅ **Sistema de Maestros Multi-LLM** completo
- ✅ **Generación Multi-Salida** (Web, Impreso, Redes)
- ✅ **Gestión de Prompts y Estilos** personalizables
- ✅ **Tracking de Tokens** y costos en tiempo real
- ✅ **Sistema de Proyectos** para organización
- ✅ **Interfaz completamente en español**
- ✅ **Testing** y documentación completa

### 🔄 v2.4.0 - EN DESARROLLO (Próximos meses)
- [ ] **Dashboard Analítico** con métricas avanzadas
- [ ] **Sistema de Comentarios** en noticias
- [ ] **Notificaciones en tiempo real** (WebSockets)
- [ ] **Exportar a PDF/Word** con plantillas
- [ ] **Búsqueda avanzada** con filtros múltiples
- [ ] **Versionado de noticias** con historial

### 🎯 v2.5.0 - FUTURO CERCANO
- [ ] **Refresh Tokens** para sesiones largas
- [ ] **Recuperación de contraseña** por email
- [ ] **Perfil de usuario** editable con avatar
- [ ] **API pública** con rate limiting
- [ ] **Integración con CMS** externos (WordPress, etc.)
- [ ] **Webhooks** para automatización

### 🚀 v3.0.0 - VISIÓN A LARGO PLAZO
- [ ] **Mobile App** (React Native)
- [ ] **Búsqueda full-text** con Elasticsearch
- [ ] **Traducción automática** multi-idioma
- [ ] **Inteligencia predictiva** para trending topics
- [ ] **Colaboración en tiempo real** (Google Docs style)
- [ ] **Marketplace de plantillas** y estilos

### 📊 **Estado Actual del Proyecto**

```
🎉 Proyecto COMPLETADO al 100% - Listo para producción

Funcionalidades Implementadas: ████████████ 100%
Testing y Documentación:       ████████████ 100%
Estabilidad y Performance:     ████████████  95%
Escalabilidad:                 ████████████  90%
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este proyecto sigue las mejores prácticas de desarrollo colaborativo.

### 📋 Cómo Contribuir

1. **Fork** el proyecto desde GitHub
2. **Crea una rama** para tu feature: `git checkout -b feature/AmazingFeature`
3. **Commit** tus cambios: `git commit -m 'feat: Add AmazingFeature'`
4. **Push** a la rama: `git push origin feature/AmazingFeature`
5. **Abre un Pull Request** con descripción detallada

### 🏗️ Áreas que Necesitan Contribución

- **🧪 Testing**: Ampliar cobertura de tests
- **📱 Mobile**: Desarrollar versión React Native
- **🌍 i18n**: Soporte multi-idioma
- **📊 Analytics**: Dashboard con métricas avanzadas
- **🔍 Search**: Implementar Elasticsearch
- **🎨 UI/UX**: Mejoras de diseño y usabilidad

### Código de Conducta
- Sé respetuoso
- Código limpio y documentado
### 🎨 **Código de Conducta**
- **Respeto mutuo** y comunicación constructiva
- **Código limpio** y bien documentado
- **Testing obligatorio** para nuevas funcionalidades
- **Seguir convenciones** establecidas en el proyecto

### 📚 **Recursos para Contribuidores**
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Guía completa de contribución
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Documentación técnica
- [PROJECT_CONTEXT.md](./PROJECT_CONTEXT.md) - Contexto del proyecto

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

```
Copyright (c) 2025 Editor del Mar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Agradecimientos

Este proyecto fue posible gracias a estas increíbles tecnologías:

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework backend moderno y rápido
- **[React](https://react.dev/)** - Librería frontend declarativa
- **[Google Gemini](https://ai.google.dev/)** - IA generativa de vanguardia
- **[Anthropic Claude](https://anthropic.com/)** - Asistente de IA conversacional
- **[Tailwind CSS](https://tailwindcss.com/)** - Framework CSS utilitario
- **[PostgreSQL](https://postgresql.org/)** - Base de datos robusta y escalable
- **[Vite](https://vitejs.dev/)** - Build tool moderna y rápida

---

## 📞 Soporte y Contacto

- ### 🆘 **Obtener Ayuda**
- � **Documentación**: Consulta los archivos `.md` en la carpeta `docs/` del proyecto
- � **Issues**: [GitHub Issues](https://github.com/editoradelmar/sistema-noticias-ia/issues)
- � **Discusiones**: [GitHub Discussions](https://github.com/editoradelmar/sistema-noticias-ia/discussions)

### 👨‍💻 **Desarrollador Principal**
- **Nombre**: Hector Romero (@hromero)
- **Email**: hromero@eluniversal.com.co
- **Proyecto**: Editor del Mar SA - Sistema de Noticias con IA

### 🔗 **Enlaces Importantes**
- 🏠 **Repositorio**: [GitHub](https://github.com/editoradelmar/sistema-noticias-ia)
- 📖 **Documentación**: [README completo](./README.md)
-- 🚀 **Guía Rápida**: [QUICKSTART.md](./QUICKSTART.md)
-- 📐 **Arquitectura**: [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 📊 Estado del Proyecto

**🎉 PROYECTO COMPLETADO - LISTO PARA PRODUCCIÓN**

| Componente | Estado | Versión | Cobertura |
|------------|--------|---------|-----------|
| 🔧 **Backend API** | ✅ Completo | v2.3.0 | 48 endpoints |
| ⚛️ **Frontend** | ✅ Completo | v2.3.0 | 25+ componentes |
| 🔐 **Autenticación** | ✅ Completo | JWT + Roles | 100% |
| 💾 **Base de Datos** | ✅ Productivo | PostgreSQL 12+ | 12 tablas |
| 🤖 **IA Multi-LLM** | ✅ Funcional | Gemini + Claude | 3 proveedores |
| 🎯 **Sistema Maestros** | ✅ Completo | 5 maestros | 100% |
| 🧪 **Testing** | ✅ Completo | pytest + jest | 70%+ |
| 📚 **Documentación** | ✅ Actualizada | Completa | 100% |

### 🏆 **Métricas de Calidad**
```
Funcionalidades: ████████████ 100% (48/48 endpoints)
Estabilidad:     ████████████  95% (Sin bugs críticos)
Performance:     ████████████  90% (< 2s respuesta)
Seguridad:       ████████████  95% (JWT + CORS + Validación)
```

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**

**🚀 Desarrollado con ❤️ usando FastAPI, React, PostgreSQL y Multi-LLM IA**

---


**📅 Última actualización:** 2025-10-30  
**🔖 Versión actual:** v2.3.1 (Fixes críticos, atomicidad y restauración de salidas)  
**🎯 Próxima versión:** v2.4.0 (Dashboard Analítico)  
**👨‍💻 Desarrollador:** Hector Romero - Editor del Mar SA

### 🆕 **Últimas Actualizaciones (v2.3.1)**
- ✅ **Fix CORS**: El backend ahora permite correctamente orígenes locales y remotos, solucionando bloqueos de frontend.
- ✅ **Restauración de agrupación de salidas**: El panel de edición muestra tabs y salidas generadas correctamente, con mapeo por tipo y nombre de salida.
- ✅ **Atomicidad de métricas**: Las métricas solo se guardan si el proceso de publicación es exitoso y todos los datos están presentes.
- ✅ **Troubleshooting avanzado**: Documentados los mensajes informativos en frontend cuando no existen métricas, y el flujo de edición/restauración de datos.
- ✅ **Validación de flujo de edición**: El sistema recupera y muestra correctamente noticias, salidas y métricas asociadas en modo edición.
- ✅ **Documentación actualizada** con los nuevos flujos y fixes críticos.

### 🌐 **URLs de Acceso (Demo)**
- **Frontend**: https://woodcock-still-tetra.ngrok-free.app/
- **Backend API**: https://epic-exactly-bull.ngrok-free.app/
- **Documentación**: https://epic-exactly-bull.ngrok-free.app/docs