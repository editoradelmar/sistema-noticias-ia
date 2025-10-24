# 🚀 Sistema de Noticias con IA v2.1.0

Sistema profesional de gestión de noticias con **autenticación JWT**, **PostgreSQL** e integración de inteligencia artificial usando **FastAPI + React + Claude**.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.118.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12.10-336791?style=flat&logo=postgresql)](https://postgresql.org)
[![Claude](https://img.shields.io/badge/Claude-Sonnet_4.5-7C3AED?style=flat)](https://anthropic.com)

---

## 📋 Características Principales

### 🔐 Autenticación y Seguridad
- ✅ **Autenticación JWT** con tokens seguros
- ✅ **Sistema de roles** (Admin, Editor, Viewer)
- ✅ **Control de permisos** granular por endpoint
- ✅ **Encriptación bcrypt** para contraseñas
- ✅ **Sesiones persistentes** con localStorage

### 📰 Gestión de Noticias
- ✅ **CRUD completo** con PostgreSQL
- ✅ **6 categorías** predefinidas
- ✅ **Búsqueda y filtrado** en tiempo real
- ✅ **Vinculación usuario-contenido**
- ✅ **Estadísticas** del sistema

### 🤖 Inteligencia Artificial
- ✅ **Integración con Claude Sonnet 4.5**
- ✅ **Resúmenes automáticos** de noticias
- ✅ **Chat conversacional** con contexto
- ✅ **Modo simulado** (fallback sin API)
- ✅ **Análisis de contenido**

### 🎨 Interfaz Moderna
- ✅ **React + Tailwind CSS**
- ✅ **Diseño responsive**
- ✅ **Componentes modulares**
- ✅ **Animaciones fluidas**
- ✅ **UX optimizada**

---

## 🛠️ Stack Tecnológico Completo

### Backend
```
Python 3.11+
├── FastAPI 0.118.0           # Framework web
├── Uvicorn 0.37.0            # Servidor ASGI
├── PostgreSQL 12.10          # Base de datos
├── SQLAlchemy 2.0.44         # ORM
├── Alembic 1.13.1            # Migraciones
├── Pydantic 2.11.9           # Validación
├── Anthropic 0.69.0          # SDK Claude
├── python-jose 3.3.0         # JWT
├── passlib 1.7.4             # Hash passwords
└── bcrypt 4.0.1              # Encriptación
```

### Frontend
```
Node.js 18+
├── React 18.2.0              # UI Library
├── Vite 5.0.8                # Build tool
├── Tailwind CSS 3.4.0        # Estilos
└── Lucide React 0.263.1      # Iconos
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

## 🚀 Instalación Rápida

### Prerrequisitos

```bash
✅ Python 3.11+
✅ Node.js 18+
✅ PostgreSQL 12+
✅ Git
```

### 1️⃣ Clonar Repositorio

```bash
git clone <repository-url>
cd sistema-noticias-ia
```

### 2️⃣ Configurar PostgreSQL

```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE noticias_ia;

-- Crear usuario
CREATE USER openpg WITH PASSWORD 'openpgpwd';

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE noticias_ia TO openpg;

-- Salir
\q
```

### 3️⃣ Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
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

1. Click en pestaña "✨ Crear"
2. Completa el formulario:
   - **Título**: Mínimo 5 caracteres
   - **Contenido**: Mínimo 20 caracteres
   - **Categoría**: Selecciona una
3. Click "Publicar Noticia"
4. ✅ Noticia creada y vinculada a tu usuario

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

## 🎯 Roadmap

### v2.2 (Próximamente)
- [ ] Refresh tokens para sesiones largas
- [ ] Cambiar contraseña
- [ ] Recuperar contraseña por email
- [ ] Perfil de usuario editable
- [ ] Avatar de usuario

### v2.3
- [ ] Dashboard con estadísticas
- [ ] Gráficos de actividad
- [ ] Notificaciones en tiempo real
- [ ] Sistema de comentarios
- [ ] Reacciones a noticias

### v3.0
- [ ] API pública con rate limiting
- [ ] Mobile app (React Native)
- [ ] Búsqueda full-text avanzada
- [ ] Traducción multi-idioma
- [ ] Exportar a PDF/Word

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m 'Add AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Abre un Pull Request

### Código de Conducta
- Sé respetuoso
- Código limpio y documentado
- Tests para nuevas features

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo [LICENSE](./LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework backend
- [React](https://react.dev/) - Librería frontend
- [Anthropic](https://anthropic.com/) - Claude AI
- [Tailwind CSS](https://tailwindcss.com/) - Estilos
- [PostgreSQL](https://postgresql.org/) - Base de datos

---

## 📞 Soporte

- 📧 Email: soporte@ejemplo.com
- 💬 Discord: [Servidor](https://discord.gg/ejemplo)
- 🐛 Issues: [GitHub Issues](https://github.com/usuario/proyecto/issues)
- 📚 Docs: [Documentación completa](https://docs.ejemplo.com)

---

## 📊 Estado del Proyecto

| Componente | Estado | Versión |
|------------|--------|---------|
| Backend API | ✅ Estable | 2.1.0 |
| Frontend | ✅ Estable | 2.1.0 |
| Autenticación | ✅ Completo | 2.1.0 |
| Base de Datos | ✅ PostgreSQL | 12.10 |
| IA Integration | ✅ Funcional | Claude 4.5 |
| Tests | 🟡 En progreso | 40% |
| Docs | ✅ Completa | 100% |

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**

**🚀 Desarrollado con ❤️ usando FastAPI, React, PostgreSQL y Claude IA**

---

**Última actualización:** 2025-10-14  
**Versión:** 2.1.0  
**Autor:** hromero
#   s i s t e m a - n o t i c i a s - i a  
 