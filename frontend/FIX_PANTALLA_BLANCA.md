# 🔧 SOLUCIÓN - Pantalla en Blanco en Frontend

## 🚨 Problema Identificado

El frontend muestra pantalla en blanco porque:
1. **Falta axios** - El código de `maestros.js` usa axios pero no está instalado
2. **Incompatibilidad** - El archivo `api.js` anterior usaba fetch, no axios

## ✅ SOLUCIÓN RÁPIDA

### Paso 1: Instalar axios
```bash
cd frontend
npm install axios
```

### Paso 2: Reiniciar el servidor de desarrollo
```bash
# Ctrl+C para detener
npm run dev
```

### Paso 3: Abrir navegador
```
http://localhost:5173
```

### Paso 4: Revisar consola del navegador
- Presiona F12
- Ve a la pestaña "Console"
- Busca errores en rojo

---

## 🔍 VERIFICAR QUE FUNCIONA

### Test Mínimo
Si quieres probar con un componente mínimo primero:

1. **Edita `frontend/index.html`** temporalmente:
```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Test</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main-test.jsx"></script>
  </body>
</html>
```

2. **Recarga el navegador**
   - Si ves "🟢 Frontend funcionando" → React está OK
   - El problema es en App.jsx o los contextos

3. **Restaura `index.html`** a:
```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sistema de Noticias con IA</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

## 🐛 DEBUGGING

### Ver errores en consola del navegador
```javascript
// F12 → Console
// Busca errores como:
// - "Cannot find module"
// - "Unexpected token"
// - "import/export"
```

### Ver errores en terminal de Vite
```bash
# En la terminal donde corre npm run dev
# Busca:
# - [vite] error
# - Failed to resolve
# - Cannot find module
```

---

## 📋 CHECKLIST

- [ ] Axios instalado: `npm list axios`
- [ ] Backend corriendo: http://localhost:8000/docs
- [ ] Frontend sin errores en terminal
- [ ] No hay errores en consola del navegador (F12)
- [ ] `node_modules` existe en frontend
- [ ] Archivo `api.js` actualizado con axios

---

## 🔄 SI SIGUE SIN FUNCIONAR

### Opción 1: Reinstalar dependencias
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Opción 2: Limpiar caché de Vite
```bash
cd frontend
rm -rf node_modules/.vite
npm run dev
```

### Opción 3: Verificar archivos críticos

**Verifica que existan:**
```
frontend/
├── src/
│   ├── main.jsx          ✅ Debe existir
│   ├── App.jsx           ✅ Debe existir
│   ├── index.css         ✅ Debe existir
│   ├── services/
│   │   └── api.js        ✅ Debe tener axios
│   └── context/
│       ├── AuthContext.jsx  ✅
│       └── ThemeContext.jsx ✅
├── index.html            ✅
├── package.json          ✅
└── vite.config.js        ✅
```

---

## 💡 ERRORES COMUNES Y SOLUCIONES

### Error: "Cannot find module 'axios'"
**Solución:**
```bash
npm install axios
```

### Error: "Failed to resolve import"
**Solución:**
```bash
# Verifica que el archivo exista
# Verifica que la ruta sea correcta (case-sensitive)
```

### Error: "Unexpected token"
**Solución:**
```bash
# Revisa sintaxis JSX
# Asegúrate que los archivos terminen en .jsx
```

### Pantalla blanca + No hay errores
**Posibles causas:**
1. CSS no cargando → Revisa `index.css`
2. Tailwind no compilando → Revisa `tailwind.config.js`
3. Componente renderiza null → Revisa `App.jsx`

---

## 🎯 SIGUIENTE PASO

Una vez que axios esté instalado y el servidor reiniciado:

1. **Abre http://localhost:5173**
2. **Deberías ver la pantalla de login**
3. **Si ves errores**, cópialos y los revisamos

---

## 📞 REPORTAR PROBLEMA

Si después de instalar axios sigue sin funcionar, reporta:

1. **Errores en terminal de Vite**
2. **Errores en consola del navegador (F12)**
3. **Resultado de:**
   ```bash
   npm list axios
   npm list react
   node --version
   npm --version
   ```

---

**Actualizado**: 2025-10-17
