
# ⚡ Guía de Inicio Rápido - Sistema de Noticias con IA v2.3.0

> **🎯 Objetivo:** Tener el sistema completo funcionando en **menos de 10 minutos**

Guía ultra-optimizada para poner el proyecto en marcha rápidamente con todas las funcionalidades de la **Fase 6 completada**.

---

## 🎯 Lo que vas a construir

Sistema completo de noticias con tecnología de vanguardia:
- ✅ **CRUD avanzado** de noticias con proyectos y secciones
- 🤖 **IA Multi-Proveedor** (Gemini 2.0, Claude 3.5, GPT-4)
- 📤 **Generación Multi-Salida** (Web, Impreso, Redes Sociales)
- 💬 **Chat inteligente** con contexto persistente
- 🎨 **Interfaz moderna** responsive con modo oscuro
- 🔐 **Autenticación JWT** con sistema de roles
- 📊 **Sistema de Maestros** para configuración IA

**Stack:** FastAPI + React + PostgreSQL + Multi-LLM + Tailwind CSS

---

## 🚀 Instalación Ultra-Rápida (5 minutos)

### Prerrequisitos
```bash
✅ Python 3.11+
✅ Node.js 18+ 
✅ PostgreSQL 12+
✅ Git
```

### 🐧 Linux/Mac - Instalación Completa

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd sistema-noticias-ia

# 2. Configurar PostgreSQL
sudo -u postgres createdb noticias_ia
sudo -u postgres psql -c "CREATE USER openpg WITH PASSWORD 'openpgpwd';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE noticias_ia TO openpg;"

# 3. Backend (Terminal 1)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Configurar .env (ver sección siguiente)
python -m alembic upgrade head
python create_admin.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Frontend (Terminal 2)
cd frontend
npm install
cp .env.example .env
# Configurar .env (ver sección siguiente)
npm run dev
```

### 🪟 Windows PowerShell - Instalación Completa

```powershell
# 1. Clonar repositorio
git clone <repository-url>
cd sistema-noticias-ia

# 2. Configurar PostgreSQL
psql -U postgres -c "CREATE DATABASE noticias_ia;"
psql -U postgres -c "CREATE USER openpg WITH PASSWORD 'openpgpwd';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE noticias_ia TO openpg;"

# 3. Backend (Terminal 1)
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Configurar .env (ver sección siguiente)
python -m alembic upgrade head
python create_admin.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Frontend (Terminal 2)
cd frontend
npm install
copy .env.example .env
# Configurar .env (ver sección siguiente)
npm run dev
```

### ✅ Verificación Exitosa

```bash
✅ Backend: http://localhost:8000/docs (Swagger UI)
✅ Frontend: http://localhost:5173 (React App)
✅ Login: admin@sistema.com / admin123
✅ Health: http://localhost:8000/api/health
```

---

## 📁 Archivos Esenciales

### Backend (copiar en orden)

1. `backend/main.py` - ⭐ Aplicación principal
2. `backend/config.py` - Configuración
3. `backend/requirements.txt` - Dependencias
4. `backend/models/schemas.py` - Modelos de datos
5. `backend/routers/__init__.py` - Init routers
6. `backend/routers/noticias.py` - Endpoints CRUD
7. `backend/routers/ai.py` - Endpoints IA

### Frontend (reemplazar)

1. `frontend/src/App.jsx` - ⭐ Componente principal
2. `frontend/vite.config.js` - Config de Vite
3. `frontend/package.json` - Actualizar dependencias

---

## ▶️ Ejecutar (Método 1 - Manual)

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
uvicorn main:app --reload
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

**Abrir:** http://localhost:5173

---

## ▶️ Ejecutar (Método 2 - Con Makefile)

```bash
# Instalar todo
make install

# Ejecutar backend
make dev-backend

# Ejecutar frontend (en otra terminal)
make dev-frontend

# Ver todos los comandos
make help
```

---

## ▶️ Ejecutar (Método 3 - Docker)

```bash
# Build y run
docker-compose up --build

# En background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🎮 Primeros Pasos en la App

1. **Abrir** http://localhost:5173
2. **Cargar datos:** Click en "Cargar Ejemplos"
3. **Crear noticia:** Click en "Crear" → llenar formulario
4. **Generar resumen:** Click en "Generar resumen con IA"
5. **Chat:** Click en "Chat IA" → hacer preguntas

---

## 📊 Estructura del Proyecto

```
sistema-noticias-ia/
├── backend/              ← API FastAPI
│   ├── main.py          ← ⭐ IMPORTANTE
│   ├── config.py
│   ├── models/
│   │   └── schemas.py   ← ⭐ IMPORTANTE
│   └── routers/
│       ├── noticias.py  ← ⭐ IMPORTANTE
│       └── ai.py        ← ⭐ IMPORTANTE
│
└── frontend/            ← UI React
    ├── src/
    │   └── App.jsx      ← ⭐ IMPORTANTE
    └── vite.config.js
```

---

## 🔧 Comandos Útiles

### Backend
```bash
# Docs interactivas
http://localhost:8000/docs

# Health check
curl http://localhost:8000/health

# Ver todas las noticias
curl http://localhost:8000/api/noticias/

# Crear datos de ejemplo
curl -X POST http://localhost:8000/api/noticias/seed
```

### Tests
```bash
# Backend
cd backend && pytest -v

# Ver coverage
pytest --cov=. --cov-report=html
```

---

## 🐛 Solución de Problemas Comunes

### ❌ "Connection refused" en frontend

**Problema:** Frontend no puede conectar con backend

**Solución:**
```bash
# Verificar que backend esté corriendo
curl http://localhost:8000/health

# Verificar CORS en backend/config.py
ALLOWED_ORIGINS = ["http://localhost:5173"]
```

### ❌ "Module not found" en backend

**Solución:**
```bash
# Activar venv
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### ❌ Error de importación en routers

**Solución:**
```bash
# Verificar que existe __init__.py
touch routers/__init__.py
touch models/__init__.py
```

### ❌ Frontend muestra página en blanco

**Solución:**
```bash
# Limpiar cache y reinstalar
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📖 Endpoints Principales

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/noticias/` | Lista todas las noticias |
| POST | `/api/noticias/` | Crea noticia |
| DELETE | `/api/noticias/{id}` | Elimina noticia |
| POST | `/api/ai/resumir/{id}` | Genera resumen |
| POST | `/api/ai/chat` | Chat con IA |
| GET | `/health` | Estado del servidor |
| GET | `/docs` | Documentación Swagger |

---

## 🎨 Personalización Rápida

### Cambiar colores (Frontend)

Editar `App.jsx`:
```javascript
// Buscar y reemplazar
bg-purple-600  →  bg-blue-600
bg-purple-50   →  bg-blue-50
```

### Agregar nueva categoría (Backend)

En `models/schemas.py`:
```python
class CategoriaNoticia(str, Enum):
    TECNOLOGIA = "tecnologia"
    # ... existentes
    TU_NUEVA = "tu_nueva"  # ← Agregar aquí
```

### Cambiar puerto del backend

```bash
uvicorn main:app --reload --port 9000
```

### Cambiar puerto del frontend

En `vite.config.js`:
```javascript
server: {
  port: 3000  // Cambiar de 5173 a 3000
}
```

---

## 📚 Recursos Adicionales

- **README.md** - Documentación completa
- **DEPLOYMENT.md** - Guía de producción
- **Makefile** - Comandos automatizados
- **Backend Docs** - http://localhost:8000/docs

---

## 🔥 Comandos de Un Solo Línea

```bash
# Instalación completa
git clone repo && cd repo && make install

# Iniciar todo
make dev

---

## 🔑 Configuración de Variables de Entorno

### Backend (.env)
```bash
# Base de datos
DATABASE_URL=postgresql://openpg:openpgpwd@localhost/noticias_ia

# Seguridad JWT
SECRET_KEY=tu_secret_key_super_segura_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30

# IA APIs (Configurar al menos una)
GEMINI_API_KEY=tu_gemini_api_key_aqui          # GRATIS - Recomendado
ANTHROPIC_API_KEY=sk-ant-api-key-aqui          # PAGO - Opcional

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)
```bash
# Backend URL
VITE_API_BASE=http://localhost:8000/api

# IA por defecto
VITE_DEFAULT_LLM_PROVEEDOR=Google
VITE_DEFAULT_LLM_MODELO_ID=gemini-2.0-flash-exp
VITE_DEFAULT_LLM_URL_API=https://generativelanguage.googleapis.com/v1beta/models
```

---

## 🤖 Configuración de APIs de IA

### 1. Google Gemini (GRATIS - Recomendado)
```bash
# 1. Ir a: https://ai.google.dev/
# 2. Crear cuenta y obtener API Key
# 3. Agregar a backend/.env:
GEMINI_API_KEY=tu_api_key_aqui

# 4. Configurar en el sistema:
#    - Ir a "Maestros" → "LLM Maestro" 
#    - Crear nuevo modelo con los datos del README
```

### 2. Anthropic Claude (PAGO - Opcional)
```bash
# 1. Ir a: https://console.anthropic.com/
# 2. Crear cuenta y obtener API Key  
# 3. Agregar a backend/.env:
ANTHROPIC_API_KEY=sk-ant-api-key-aqui
```

---

## � Primeros Pasos Después de la Instalación

### 1. **Configurar Modelos LLM** (Obligatorio)
```bash
# Acceder al sistema con admin@sistema.com / admin123
# Ir a "Maestros" → "LLM Maestro" → "Crear Nuevo"
# Usar los datos JSON del README principal
```

### 2. **Crear Contenido de Prueba**
```bash
# 1. Crear un proyecto: "Mi Primer Proyecto"
# 2. Crear secciones: "Tecnología", "Deportes", etc.
# 3. Configurar prompts y estilos personalizados
# 4. Crear tu primera noticia con IA
```

### 3. **Probar Funcionalidades**
```bash
✅ Crear noticias manualmente
✅ Generar contenido con IA 
✅ Probar generación multi-salida
✅ Usar el chat inteligente
✅ Cambiar entre modo claro/oscuro
```

---

## ⚡ Comandos Útiles de Desarrollo

```bash
# Backend - Desarrollo
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend - Desarrollo  
cd frontend
npm run dev

# Tests Backend
cd backend
pytest -v

# Tests Frontend
cd frontend
npm test

# Backup de base de datos
pg_dump noticias_ia > backup.sql

# Restaurar base de datos
psql noticias_ia < backup.sql
```

---

## 🚀 Next Steps - Personalización

### 1. **Configuración Avanzada**
- [ ] Configurar múltiples modelos LLM
- [ ] Personalizar prompts por sección
- [ ] Configurar estilos de escritura
- [ ] Ajustar límites de tokens

### 2. **Desarrollo**
- [ ] Revisar código fuente marcado con ⭐
- [ ] Personalizar componentes UI
- [ ] Agregar nuevos endpoints
- [ ] Implementar funcionalidades específicas

### 3. **Producción**
- [ ] Configurar HTTPS
- [ ] Usar base de datos en la nube
- [ ] Configurar CI/CD
- [ ] Monitoreo y logs

---

## 🆘 Resolución de Problemas

### Problemas Comunes

**❌ Error de conexión a PostgreSQL**
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql   # Linux
brew services list                  # Mac
```

**❌ Error "No module named 'something'"**
```bash
# Verificar entorno virtual activado
which python  # Debe apuntar a venv
pip install -r requirements.txt
```

**❌ Frontend no se conecta al backend**
```bash
# Verificar CORS en backend/.env
ALLOWED_ORIGINS=http://localhost:5173

# Verificar URL en frontend/.env
VITE_API_BASE=http://localhost:8000/api
```

**❌ APIs de IA no funcionan**
```bash
# Verificar API keys en backend/.env
# Probar con: http://localhost:8000/docs → Endpoints /api/ai/
```

### 🔍 **Recursos de Ayuda**
- 📚 [README Completo](./README.md) - Documentación detallada
- 📐 [ARCHITECTURE.md](./ARCHITECTURE.md) - Arquitectura técnica
- 🐛 [GitHub Issues](https://github.com/editoradelmar/sistema-noticias-ia/issues)
- 💬 [Discussions](https://github.com/editoradelmar/sistema-noticias-ia/discussions)

---

**🎉 ¡Listo! Tu sistema de noticias con IA está funcionando**

**📅 Última actualización:** 2025-10-25  
**🔖 Versión:** v2.3.0 (Fase 6 Completada)  
**⚡ Tiempo estimado:** 5-10 minutos
- [ ] CI/CD con GitHub Actions
- [ ] Modo oscuro

---

**¡Listo! Ahora tienes un sistema completo de noticias con IA funcionando. 🎉**

Para más detalles, consulta **README.md** y **DEPLOYMENT.md**.