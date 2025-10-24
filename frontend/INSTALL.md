# 📦 Instalación de Dependencias - Frontend

## 🚀 Instalación Básica

### 1. Verificar Node.js
```bash
node --version  # Debe ser v18+ o superior
npm --version   # Debe ser v9+ o superior
```

Si no tienes Node.js instalado, descárgalo de: https://nodejs.org/

### 2. Instalar dependencias
```bash
cd frontend
npm install
```

Esto instalará:
- ✅ React 18.2.0
- ✅ Vite 5.0.8 (Build tool)
- ✅ Tailwind CSS 3.4.0
- ✅ Lucide React 0.263.1 (Iconos)
- ✅ Y más...

---

## 🎯 Scripts Disponibles

### Desarrollo
```bash
npm run dev
```
Inicia servidor de desarrollo en http://localhost:5173

### Build de Producción
```bash
npm run build
```
Genera archivos optimizados en `/dist`

### Preview de Producción
```bash
npm run preview
```
Preview del build de producción

### Linting
```bash
npm run lint
```
Analiza el código con ESLint

### Formateo
```bash
npm run format
```
Formatea código con Prettier

### Tests
```bash
npm run test
```
Ejecuta tests con Vitest

---

## 📋 Dependencias Principales

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "lucide-react": "^0.263.1"
}
```

### React 18.2.0
Framework principal para construir la UI

### Lucide React
Librería de iconos moderna y ligera

---

## 🛠️ Dependencias de Desarrollo

```json
{
  "vite": "^5.0.8",
  "tailwindcss": "^3.4.0",
  "postcss": "^8.4.32",
  "autoprefixer": "^10.4.16",
  "eslint": "^8.55.0",
  "prettier": "^3.1.1"
}
```

### Vite
- Build tool ultra-rápido
- Hot Module Replacement (HMR)
- Optimización automática

### Tailwind CSS
- Framework CSS utility-first
- Modo oscuro incluido
- Totalmente personalizable

### ESLint + Prettier
- Análisis de código
- Formateo automático
- Mejores prácticas

---

## ⚙️ Configuración

### Vite Config (`vite.config.js`)
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

### Tailwind Config (`tailwind.config.js`)
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}"
  ],
  darkMode: 'class',
  theme: {
    extend: {}
  },
  plugins: []
}
```

---

## 🌐 Variables de Entorno

Crea un archivo `.env` en el directorio `frontend/`:

```bash
# API Backend
VITE_API_URL=http://localhost:8000

# Modo
VITE_MODE=development

# Nombre de la App
VITE_APP_NAME=Sistema de Noticias con IA
```

**Nota**: En Vite, todas las variables deben empezar con `VITE_`

---

## 📦 Estructura de Paquetes

```
node_modules/
├── react/              # Framework principal
├── react-dom/          # DOM renderer
├── vite/              # Build tool
├── tailwindcss/       # CSS framework
├── lucide-react/      # Iconos
├── @vitejs/           # Plugins de Vite
└── ...más paquetes
```

**Tamaño aproximado**: ~400 MB

---

## 🔄 Actualizar Dependencias

### Ver paquetes desactualizados
```bash
npm outdated
```

### Actualizar todos los paquetes
```bash
npm update
```

### Actualizar paquete específico
```bash
npm install react@latest
```

### Actualizar todo a última versión (cuidado)
```bash
npm install -g npm-check-updates
ncu -u
npm install
```

---

## 🐛 Solución de Problemas

### Error: "Cannot find module"
**Solución**: Reinstala node_modules
```bash
rm -rf node_modules package-lock.json
npm install
```

### Error: "Port 5173 already in use"
**Solución 1**: Cambia el puerto en `vite.config.js`
```javascript
server: {
  port: 3000
}
```

**Solución 2**: Mata el proceso en ese puerto
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5173 | xargs kill
```

### Error de CORS
**Solución**: Verifica el proxy en `vite.config.js` y que el backend esté corriendo

### Errores de caché
**Solución**: Limpia caché de Vite
```bash
npm run dev -- --force
```

---

## 🧹 Limpiar Proyecto

```bash
# Limpiar node_modules
rm -rf node_modules

# Limpiar caché
npm cache clean --force

# Limpiar dist
rm -rf dist

# Reinstalar todo
npm install
```

---

## 📊 Comandos Útiles

```bash
# Ver paquetes instalados
npm list --depth=0

# Ver tamaño de node_modules
du -sh node_modules  # Linux/Mac
dir node_modules     # Windows

# Auditar seguridad
npm audit

# Arreglar vulnerabilidades
npm audit fix

# Instalar paquete específico
npm install axios

# Desinstalar paquete
npm uninstall axios

# Ver info de paquete
npm info react
```

---

## 🚀 Build de Producción

### 1. Generar build
```bash
npm run build
```

Esto crea:
- `dist/` - Archivos optimizados
- HTML, CSS, JS minificados
- Assets optimizados

### 2. Preview local
```bash
npm run preview
```

### 3. Desplegar
Opciones:
- **Vercel**: `vercel --prod`
- **Netlify**: `netlify deploy --prod`
- **GitHub Pages**: `npm run build && gh-pages -d dist`

---

## 📚 Recursos

- [React Docs](https://react.dev/)
- [Vite Docs](https://vitejs.dev/)
- [Tailwind Docs](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)

---

## 🎨 Personalización

### Agregar nueva dependencia
```bash
npm install nombre-paquete
```

### Agregar dependencia de desarrollo
```bash
npm install -D nombre-paquete
```

### Ejemplos de paquetes útiles
```bash
# React Router (navegación)
npm install react-router-dom

# Axios (HTTP requests)
npm install axios

# React Query (data fetching)
npm install @tanstack/react-query

# Zustand (state management)
npm install zustand

# React Hook Form (formularios)
npm install react-hook-form

# Zod (validación)
npm install zod
```

---

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| **Dependencias principales** | 3 |
| **Dependencias dev** | 14 |
| **Tamaño node_modules** | ~400 MB |
| **Tiempo build** | ~5-10s |
| **Tamaño bundle** | ~200 KB (gzip) |

---

**Última actualización**: 2025-10-17  
**Versión del proyecto**: 2.3.0-alpha  
**Node.js recomendado**: v18+ o v20+
