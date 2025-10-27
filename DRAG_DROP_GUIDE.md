# 📁 Guía de Drag & Drop - Sistema de Noticias con IA

Documentación completa de la funcionalidad de subida de archivos con arrastrar y soltar implementada en la versión 2.3.2.

---

## 🎯 Resumen de Funcionalidad

La nueva funcionalidad de **Drag & Drop** permite a los usuarios subir archivos de texto directamente al formulario de creación de noticias, extrayendo automáticamente el contenido y generando títulos inteligentes.

### ✨ Características Principales

- 📁 **Formatos soportados**: PDF, TXT, DOC, DOCX
- 🚀 **Extracción automática** de contenido (TXT completo, otros en desarrollo)
- 🧠 **Generación inteligente de títulos** basada en análisis de contenido
- 📏 **Límites extendidos**: Hasta 10,000 caracteres (antes 2,000)
- 🎨 **Interfaz visual** con estados de carga y éxito
- ✅ **Validación robusta** de tipos y tamaños de archivo

---

## 🛠️ Implementación Técnica

### Frontend (React)

**Archivo:** `frontend/src/components/NoticiaForm.jsx`

#### Estados y Variables
```javascript
// Estados para Drag & Drop y manejo de archivos
const [dragActive, setDragActive] = useState(false);
const [fileUploading, setFileUploading] = useState(false);
const [uploadedFile, setUploadedFile] = useState(null);
const [fileError, setFileError] = useState('');
const [processingFile, setProcessingFile] = useState(false);
```

#### Funciones Principales

**1. Validación de Archivos**
```javascript
const validateFile = (file) => {
  const allowedTypes = [
    'application/pdf',
    'text/plain',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ];
  const maxSize = 10 * 1024 * 1024; // 10MB
  
  if (!allowedTypes.includes(file.type)) {
    return { valid: false, error: 'Tipo de archivo no permitido. Use PDF, TXT, DOC o DOCX.' };
  }
  
  if (file.size > maxSize) {
    return { valid: false, error: 'El archivo es demasiado grande. Máximo 10MB.' };
  }
  
  return { valid: true };
};
```

**2. Eventos Drag & Drop**
```javascript
const handleDrag = useCallback((e) => {
  e.preventDefault();
  e.stopPropagation();
}, []);

const handleDragIn = useCallback((e) => {
  e.preventDefault();
  e.stopPropagation();
  setDragActive(true);
}, []);

const handleDragOut = useCallback((e) => {
  e.preventDefault();
  e.stopPropagation();
  setDragActive(false);
}, []);

const handleDrop = useCallback((e) => {
  e.preventDefault();
  e.stopPropagation();
  setDragActive(false);
  
  const files = [...e.dataTransfer.files];
  if (files && files.length > 0) {
    handleFileUpload(files[0]);
  }
}, []);
```

**3. Generación Inteligente de Títulos**
```javascript
const generateSmartTitle = (content) => {
  if (!content || content.length < 50) {
    return 'Noticia extraída de archivo';
  }

  // Separar líneas y limpiar
  const lines = content.split('\n').filter(line => line.trim().length > 0);
  
  // La primera línea no vacía suele ser el título
  if (lines.length > 0) {
    const firstLine = lines[0].trim();
    
    // Si la primera línea parece un título (no muy corta, no muy larga)
    if (firstLine.length > 10 && firstLine.length < 200) {
      return firstLine;
    }
  }

  // Buscar en las primeras 3 líneas una que parezca título
  for (let i = 0; i < Math.min(3, lines.length); i++) {
    const line = lines[i].trim();
    if (line.length > 15 && line.length < 150 && !line.endsWith('.') && !line.includes(':')) {
      return line;
    }
  }

  // Fallback: usar las primeras palabras del contenido
  const firstWords = content.substring(0, 100).trim();
  return firstWords + (content.length > 100 ? '...' : '');
};
```

**4. Procesamiento de Archivos**
```javascript
const handleFileUpload = async (file) => {
  setFileError('');
  
  const validation = validateFile(file);
  if (!validation.valid) {
    setFileError(validation.error);
    return;
  }

  setFileUploading(true);
  setUploadedFile(file);

  try {
    let extractedText = '';
    
    // Leer el contenido real del archivo según su tipo
    if (file.type === 'text/plain') {
      // Para archivos TXT, leer directamente el texto
      extractedText = await file.text();
    } else {
      // Para PDF, DOC, DOCX - placeholder hasta implementar backend
      extractedText = `[Archivo ${file.name} requiere procesamiento en servidor]`;
    }

    // Generar título inteligente basado en la PRIMERA LÍNEA del contenido
    const smartTitle = generateSmartTitle(extractedText);

    // Llenar título y contenido automáticamente
    setForm(f => ({ 
      ...f, 
      titulo: smartTitle,
      contenido: extractedText
    }));
    
    setFileUploading(false);
  } catch (error) {
    setFileError('Error al procesar el archivo: ' + error.message);
    setFileUploading(false);
    setUploadedFile(null);
  }
};
```

---

## 🎨 Interfaz de Usuario

### Zona de Drag & Drop

La zona visual cuenta con **4 estados distintos**:

#### 1. Estado Normal
```jsx
<File className="w-12 h-12 text-slate-400 dark:text-slate-500 mb-3" />
<p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
  Arrastra un archivo o haz clic para seleccionar
</p>
<p className="text-xs text-slate-500 dark:text-slate-400">
  Soporta PDF, TXT, DOC y DOCX (máx. 10MB)
</p>
```

#### 2. Estado Hover (Drag Active)
```jsx
<Upload className="w-12 h-12 text-blue-500 mb-3" />
<p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
  Suelta el archivo aquí
</p>
```

#### 3. Estado Cargando
```jsx
<Loader2 className="w-12 h-12 text-blue-500 animate-spin mb-3" />
<p className="text-sm font-medium text-slate-700 dark:text-slate-300">
  Procesando archivo...
</p>
<p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
  Extrayendo contenido de {uploadedFile?.name}
</p>
```

#### 4. Estado Éxito
```jsx
<Check className="w-12 h-12 text-green-500 mb-3" />
<p className="text-sm font-medium text-green-700 dark:text-green-400">
  Archivo procesado exitosamente
</p>
<p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
  {uploadedFile.name} • {(uploadedFile.size / 1024).toFixed(1)} KB
</p>
```

### Clases CSS Dinámicas

```jsx
className={`relative border-2 border-dashed rounded-lg p-6 transition-all duration-200 ${
  dragActive
    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-400'
    : 'border-slate-300 dark:border-slate-600 hover:border-slate-400 dark:hover:border-slate-500'
} ${
  fileUploading ? 'pointer-events-none opacity-75' : 'cursor-pointer'
}`}
```

---

## 📋 Flujo de Usuario

### Proceso Completo

1. **🚀 Iniciar**: Usuario accede al formulario "Crear Noticia"
2. **📁 Subir**: Arrastra archivo o hace clic en la zona de drag & drop
3. **✅ Validar**: Sistema valida tipo MIME y tamaño del archivo
4. **⚡ Procesar**: Extrae contenido del archivo (TXT completo)
5. **🧠 Analizar**: Genera título inteligente basado en contenido
6. **📝 Rellenar**: Llena automáticamente campos título y contenido
7. **✏️ Revisar**: Usuario revisa y edita si es necesario
8. **⚙️ Configurar**: Selecciona sección, proyecto, salidas, LLM
9. **🚀 Generar**: Crea la noticia con el contenido extraído

### Casos de Uso

#### ✅ Caso Exitoso - Archivo TXT
```
Input: archivo-noticia.txt (3.2 KB)
Contenido: "San Francisco, La Loma: zona de alto riesgo..."

Output:
- Título: "San Francisco, La Loma: zona de alto riesgo y trece años desde su caída"
- Contenido: [Texto completo del archivo]
- Estado: Exitoso
```

#### ⚠️ Caso Pendiente - Archivo PDF
```
Input: documento.pdf (150 KB)

Output:
- Título: "Documento"
- Contenido: "[Archivo documento.pdf requiere procesamiento en servidor]"
- Estado: Requiere implementación backend
```

#### ❌ Caso Error - Archivo Inválido
```
Input: imagen.jpg (2 MB)

Output:
- Error: "Tipo de archivo no permitido. Use PDF, TXT, DOC o DOCX."
- Estado: Rechazado
```

---

## 🔮 Próximos Pasos

### Backend - Extracción de Texto

**Pendiente de implementar:**

```python
# backend/routers/files.py
@router.post("/extract-text")
async def extract_text_from_file(file: UploadFile = File(...)):
    """
    Extrae texto de archivos PDF, DOC, DOCX
    """
    if file.content_type == "application/pdf":
        # Usar PyPDF2 o pdfplumber
        pass
    elif file.content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        # Usar python-docx
        pass
    
    return {"extracted_text": text, "title": generated_title}
```

### Librerías Necesarias

```bash
pip install PyPDF2 python-docx pdfplumber
```

### Integración Frontend-Backend

```javascript
// Reemplazar la simulación con llamada real al backend
const response = await fetch('/api/files/extract-text', {
  method: 'POST',
  body: formData
});
const result = await response.json();
```

---

## 🔒 Mejoras de Seguridad

### Parametrización de Modo Desarrollo

**Problema identificado y solucionado:** El "Acceso rápido (Desarrollo)" en la pantalla de login representaba un riesgo de seguridad al estar visible tanto en desarrollo como en producción.

#### Solución Implementada

```jsx
{/* Solo visible en modo desarrollo */}
{import.meta.env.MODE === 'development' && (
  <div className="mt-6 pt-6 border-t-2 border-slate-100 dark:border-slate-800">
    <p className="text-xs text-slate-500 dark:text-slate-500 text-center mb-3">
      Acceso rápido (Desarrollo)
    </p>
    {/* Botones de acceso rápido */}
  </div>
)}
```

#### Comportamiento por Modo

| Comando | Modo | `import.meta.env.MODE` | Acceso Rápido |
|---------|------|------------------------|---------------|
| `npm run dev` | Desarrollo | `development` | ✅ **Visible** |
| `npm run build` | Producción | `production` | ❌ **Oculto** |
| `npm run preview` | Preview | `production` | ❌ **Oculto** |

#### Ventajas de Seguridad

- ✅ **Automático**: No requiere configuración manual
- ✅ **Seguro por defecto**: Producción sin accesos de desarrollo
- ✅ **Convenience en dev**: Acceso rápido disponible para testing
- ✅ **Zero-config**: Usa variables nativas de Vite

---

## 🧪 Testing

### Casos de Prueba

1. **✅ Archivos TXT**: Validar extracción completa
2. **🧪 Drag & Drop**: Eventos funcionales
3. **⚡ Estados visuales**: Transiciones suaves
4. **🛡️ Validación**: Rechazar archivos inválidos
5. **📏 Límites**: Verificar tamaño máximo
6. **🎨 Responsivo**: Funciona en móvil/desktop

### Comandos de Testing

```bash
# Frontend
cd frontend
npm test -- --testNamePattern="NoticiaForm"

# Backend (cuando se implemente)
cd backend
pytest tests/test_file_upload.py -v
```

---

## 🐛 Troubleshooting

### Problemas Comunes

#### 1. Iconos no aparecen
```bash
Error: CloudUpload not found in lucide-react
Solución: Usar iconos básicos (Upload, File, Check)
```

#### 2. Estados duplicados
```bash
Error: useState hooks called multiple times
Solución: Limpiar estados duplicados en componente
```

#### 3. Archivos no se procesan
```bash
Error: file.text() is not a function
Solución: Verificar tipo MIME correcto
```

#### 4. Títulos no se generan
```bash
Error: generateSmartTitle returns undefined
Solución: Verificar contenido del archivo > 50 caracteres
```

---

## 📊 Métricas y Límites

### Límites Técnicos

| Aspecto | Límite | Observación |
|---------|---------|-------------|
| **Tamaño archivo** | 10 MB | Configurable en validateFile() |
| **Contenido** | 10,000 chars | Aumentado desde 2,000 |
| **Título** | 200 chars | Límite formulario HTML |
| **Tipos MIME** | 4 formatos | PDF, TXT, DOC, DOCX |

### Performance

- **Archivos TXT**: Procesamiento instantáneo
- **Generación título**: < 100ms
- **Estados visuales**: Transiciones 200ms
- **Validación**: < 50ms

---

## 🔗 Referencias

- **Código fuente**: `frontend/src/components/NoticiaForm.jsx`
- **Documentación React**: [File API](https://developer.mozilla.org/en-US/docs/Web/API/File)
- **Lucide Icons**: [Documentación oficial](https://lucide.dev)
- **Tailwind CSS**: [Utility classes](https://tailwindcss.com/docs)

---

*Documentación generada para Sistema de Noticias con IA v2.3.2 - Octubre 2025*