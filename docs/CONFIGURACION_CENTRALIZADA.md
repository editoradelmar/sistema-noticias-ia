# 🔧 Variables de Configuración Centralizadas

## 📋 **Resumen**

Se ha implementado un sistema centralizado de variables de configuración para mantener consistencia en el nombre del proyecto, versión y configuraciones a través de todo el sistema.

---

## 🏗️ **Estructura de Configuración**

### **Backend** (`backend/config.py`)
```python
class Settings(BaseSettings):
    APP_NAME: str = "Sistema de Noticias con IA"
    APP_VERSION: str = "2.4.0"
    APP_DESCRIPTION: str = "Sistema profesional de gestión de noticias con IA"
    COMPANY: str = "Editor del Mar SA"
    AUTHOR: str = "Hector Romero"
    EMAIL: str = "hromero@eluniversal.com.co"
```

### **Frontend** (`frontend/src/config/appConfig.js`)
```javascript
export const appConfig = {
  APP_NAME: getEnvVar('VITE_APP_NAME', 'Sistema de Noticias con IA'),
  VERSION: getEnvVar('VITE_APP_VERSION', '2.4.0'),
  COMPANY: getEnvVar('VITE_COMPANY', 'Editor del Mar SA'),
  // ... más configuraciones
};
```

---

## 🎯 **Variables Disponibles**

### **Información de la Aplicación**
| Variable | Backend | Frontend | Descripción |
|----------|---------|----------|-------------|
| `APP_NAME` | ✅ | `VITE_APP_NAME` | Nombre del proyecto |
| `APP_VERSION` | ✅ | `VITE_APP_VERSION` | Versión actual |
| `APP_DESCRIPTION` | ✅ | `VITE_APP_DESCRIPTION` | Descripción del sistema |
| `COMPANY` | ✅ | `VITE_COMPANY` | Empresa desarrolladora |
| `AUTHOR` | ✅ | `VITE_AUTHOR` | Autor principal |
| `EMAIL` | ✅ | `VITE_EMAIL` | Email de contacto |

### **Feature Flags Frontend**
| Variable | Default | Descripción |
|----------|---------|-------------|
| `VITE_FEATURE_ADMIN_PANEL` | `true` | Mostrar panel de administración |
| `VITE_FEATURE_METRICS` | `false` | Habilitar métricas de valor |
| `VITE_FEATURE_DRAG_DROP` | `true` | Subida de archivos drag & drop |
| `VITE_FEATURE_QUICK_LOGIN` | `true` | Botones de login rápido (dev) |

### **Configuración UI**
| Variable | Default | Descripción |
|----------|---------|-------------|
| `VITE_DEFAULT_THEME` | `light` | Tema por defecto |
| `VITE_PAGINATION_DEFAULT` | `12` | Items por página por defecto |
| `VITE_MAX_FILE_SIZE` | `10485760` | Tamaño máximo de archivo (10MB) |

---

## 🚀 **Uso en Componentes**

### **Frontend - Funciones Helper**
```javascript
import { getAppTitle, getCopyright, isFeatureEnabled } from '../config/appConfig';

// Título completo de la app
const title = getAppTitle(); // "Sistema de Noticias con IA v2.4.0"

// Copyright dinámico
const copyright = getCopyright(); // "© 2025 Editor del Mar SA. Todos los derechos reservados."

// Verificar features
if (isFeatureEnabled('ADMIN_PANEL')) {
  // Mostrar panel de admin
}
```

### **Backend - Configuración Settings**
```python
from config import settings

print(f"Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
print(f"Empresa: {settings.COMPANY}")
```

---

## 📁 **Archivos de Variables de Entorno**

### **Frontend** (`.env.example`)
```bash
# Información de la aplicación
VITE_APP_NAME=Sistema de Noticias con IA
VITE_APP_VERSION=2.4.0
VITE_COMPANY=Editor del Mar SA

# Feature flags
VITE_FEATURE_ADMIN_PANEL=true
VITE_FEATURE_METRICS=false

# URLs
VITE_API_BASE_URL=http://localhost:8000
```

### **Backend** (`.env.example`)
```bash
# Configuración general
APP_NAME="Sistema de Noticias con IA"
APP_VERSION="2.4.0"
COMPANY="Editor del Mar SA"

# Base de datos
DATABASE_URL=postgresql://openpg:openpgpwd@localhost:5432/noticias_ia

# APIs
ANTHROPIC_API_KEY=
```

---

## 🔄 **Migración de Componentes**

### **Componentes Actualizados:**
1. ✅ **Login.jsx** - Usa `getAppTitle()`
2. ✅ **Header.jsx** - Usa `appConfig.APP_NAME` y `appConfig.VERSION`
3. ✅ **Footer.jsx** - Usa `getCopyright()`
4. ✅ **package.json** - Versión actualizada a 2.4.0

### **Beneficios de la Migración:**
- 🎯 **Consistencia**: Un solo lugar para cambiar versión
- 🔧 **Mantenibilidad**: Fácil actualización de información
- 🚀 **Flexibilidad**: Variables de entorno por ambiente
- 📊 **Feature Flags**: Control granular de funcionalidades

---

## ⚙️ **Configuración de Desarrollo**

### **1. Frontend - Crear `.env.local`**
```bash
# Copiar desde .env.example
cp .env.example .env.local

# Editar con configuraciones locales
VITE_APP_NAME=Sistema de Noticias con IA [DEV]
VITE_API_BASE_URL=http://localhost:8000
VITE_FEATURE_QUICK_LOGIN=true
```

### **2. Backend - Usar `.env`**
```bash
# El archivo .env ya existe con configuraciones de desarrollo
# Editar según necesidades locales
APP_NAME="Sistema de Noticias con IA [LOCAL]"
DEBUG=True
ANTHROPIC_API_KEY=tu_api_key_aqui
```

### **3. Producción - Variables Seguras**
```bash
# En producción, usar variables de entorno del servidor
export APP_NAME="Sistema de Noticias con IA"
export APP_VERSION="2.4.0"
export SECRET_KEY="clave_secreta_real"
export DATABASE_URL="postgresql://user:pass@prod-db:5432/prod_db"
```

---

## 📝 **Próximos Pasos**

### **Opcional - Componentes Pendientes:**
- [ ] **Register.jsx** - Usar configuración centralizada
- [ ] **About/Help modals** - Información de la empresa
- [ ] **Admin panel headers** - Título consistente
- [ ] **Email templates** - Información de contacto

### **Mejoras Futuras:**
- [ ] **Build-time injection** - Variables en tiempo de compilación
- [ ] **Runtime config** - Configuración dinámica desde API
- [ ] **Multi-tenancy** - Configuración por tenant
- [ ] **Theme variables** - Colores y estilos centralizados

---

## 🎯 **Resultado Final**

### **✅ Logrado:**
- **Configuración centralizada** en backend y frontend
- **Variables de entorno** organizadas y documentadas
- **Funciones helper** para uso consistente
- **Feature flags** para control de funcionalidades
- **Componentes migrados** usando configuración

### **📊 Impacto:**
- **Mantenimiento simplificado** - Un solo lugar para cambios
- **Consistencia garantizada** - Mismo nombre en toda la app
- **Flexibilidad** - Configuración por ambiente
- **Escalabilidad** - Fácil agregar nuevas variables

---

*Documentación generada para Sistema de Noticias con IA v2.4.0*  
*Fecha: 28 de octubre, 2025*