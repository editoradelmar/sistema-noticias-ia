# Guía de Troubleshooting CORS - Sistema de Noticias IA v2.4.0

## 🚨 Estado Actual del Problema

**Error**: `No 'Access-Control-Allow-Origin' header is present on the requested resource`

**Causa**: El backend aún no se ha reiniciado con la nueva configuración CORS que permite `credentials=True` con orígenes específicos.

## 🔧 Pasos para Resolver

### 1. Reiniciar Backend (CRÍTICO)
```bash
# Navegar al directorio backend
cd d:\hromero\Desktop\projects\sistema-noticias-ia\backend

# Activar entorno virtual si es necesario
venv\Scripts\activate

# Iniciar con configuración CORS actualizada
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Verificar Logs de Inicio
Cuando el backend inicie, deberías ver:
```
🌐 Modo ngrok detectado: True, DEBUG: True
CORS origins configurados: ['http://localhost:5173', 'http://localhost:3000', ..., 'https://woodcock-still-tetra.ngrok-free.app']
🔧 CORS credentials habilitadas: True
🔧 Verificar que el frontend esté en: ['https://woodcock-still-tetra.ngrok-free.app']
```

### 3. Probar Conectividad
```bash
# Ejecutar script de verificación
python test_cors.py
```

## 📋 Configuración Aplicada (Lista de Verificación)

### ✅ Backend (main.py)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ✅ Orígenes específicos
    allow_credentials=True,         # ✅ Credentials habilitadas
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)
```

### ✅ Frontend (AuthContext.jsx)
```javascript
// ✅ Usando axiosInstance en lugar de fetch directo
const response = await axiosInstance.post('/auth/login', formData, {
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
});
```

### ✅ API Configuration (api.js)
```javascript
// ✅ Usando configuración centralizada
import { appConfig } from '../config/appConfig.js';
const API_BASE = `${appConfig.API_BASE_URL}/api`;
```

## 🔍 Diagnóstico Rápido

### Verificar Puerto 8000
```bash
netstat -ano | findstr :8000
```

### Verificar Procesos Python
```bash
tasklist | findstr python
```

### Headers Esperados en Response
- `Access-Control-Allow-Origin: https://woodcock-still-tetra.ngrok-free.app`
- `Access-Control-Allow-Credentials: true`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: *`

## 🐛 Posibles Problemas

### 1. Backend No Reiniciado
**Síntoma**: Mismo error CORS  
**Solución**: Detener proceso (taskkill) y reiniciar uvicorn

### 2. Cache del Browser
**Síntoma**: Headers viejos  
**Solución**: Hard refresh (Ctrl+Shift+R) o DevTools > Network > Disable cache

### 3. Ngrok Headers
**Síntoma**: Pantalla de advertencia ngrok  
**Solución**: Headers `ngrok-skip-browser-warning: true` (ya aplicado)

### 4. Variables de Entorno
**Síntoma**: URLs incorrectas  
**Solución**: Verificar appConfig.js y config.py tienen URLs correctas

## 🎯 Prueba Final

Una vez reiniciado el backend, el login debería:

1. **Hacer preflight OPTIONS** a `/api/auth/login`
2. **Recibir headers CORS** correctos
3. **Hacer POST real** a `/api/auth/login`
4. **Completar autenticación** o mostrar error específico (no CORS)

## 📞 Si Persiste el Problema

1. Verificar logs del backend durante startup
2. Ejecutar `python test_cors.py` 
3. Verificar DevTools > Network > Headers en el browser
4. Confirmar que allowed_origins incluye el dominio frontend exacto

---

**Next Step**: 🚀 **Reiniciar backend y probar login**