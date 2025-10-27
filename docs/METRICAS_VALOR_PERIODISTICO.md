# 📊 Métricas de Valor Periodístico - Análisis e Implementación

## 🎯 Objetivo Principal

Desarrollar un sistema de métricas para **evaluar el beneficio de la IA en el proceso periodístico**, permitiendo demostrar el ROI y valor agregado de la implementación de inteligencia artificial en la redacción y publicación de noticias.

### 🔐 Acceso Restringido
**Estas métricas son exclusivas para administradores del sistema**, proporcionando información estratégica y de gestión que no debe ser visible para usuarios editores o colaboradores regulares.

---

## 📈 Enfoque: Métricas de Negocio Periodístico

### **⏱️ Eficiencia Temporal**
- **Tiempo de redacción manual vs IA**: Comparativa antes/después
- **Tiempo de adaptación multi-formato**: Una noticia → múltiples salidas en minutos  
- **Velocidad de publicación**: Desde evento hasta publicación
- **Breaking news**: Velocidad de respuesta en tiempo real

### **💰 Costo-Beneficio**
- **Costo por noticia generada**: Tokens × precio del modelo
- **Comparativa costo redactor vs IA**: $/hora vs $/tokens
- **ROI por noticia**: Engagement/views vs costo de generación
- **Ahorro operativo**: Reducción de costos vs proceso manual

### **📈 Calidad y Productividad**
- **Noticias publicadas por día**: Antes vs después de IA
- **Formatos generados simultáneamente**: Web, impreso, redes sociales
- **Consistencia editorial**: Adherencia al manual de estilo
- **Aprovechamiento de contenido**: % de contenido usado sin edición

### **📱 Alcance Multi-Canal**
- **Adaptación automática**: Misma noticia para diferentes plataformas
- **Optimización por canal**: Twitter (280 chars), Instagram (visual), Web (completo)
- **Cobertura simultánea**: Múltiples formatos en paralelo

---

## 🗄️ Estructura de Base de Datos Propuesta

```sql
CREATE TABLE metricas_valor_periodistico (
    id SERIAL PRIMARY KEY,
    noticia_id INTEGER REFERENCES noticias(id),
    
    -- Métricas de Eficiencia Temporal
    tiempo_generacion_total DECIMAL(8,3), -- segundos totales
    tiempo_por_salida JSONB, -- {"web": 2.3, "twitter": 1.1, "instagram": 1.8}
    tiempo_estimado_manual INTEGER, -- minutos que tomaría manualmente
    ahorro_tiempo_minutos INTEGER, -- tiempo ahorrado vs proceso manual
    
    -- Métricas de Costo
    tokens_total INTEGER,
    costo_generacion DECIMAL(10,4), -- costo en USD
    costo_estimado_manual DECIMAL(10,2), -- costo de redactor manual
    ahorro_costo DECIMAL(10,2), -- diferencia de costo
    
    -- Métricas de Productividad
    cantidad_salidas_generadas INTEGER,
    cantidad_formatos_diferentes INTEGER, -- web, impreso, twitter, etc.
    velocidad_palabras_por_segundo DECIMAL(8,2),
    
    -- Métricas de Calidad
    adherencia_manual_estilo DECIMAL(3,2), -- 0.0 a 1.0 (futuro: análisis automático)
    requiere_edicion_manual BOOLEAN DEFAULT FALSE,
    porcentaje_contenido_aprovechable DECIMAL(3,2), -- cuánto se usa sin editar
    
    -- Contexto del Proceso
    modelo_usado VARCHAR(100),
    usuario_id INTEGER REFERENCES usuarios(id),
    tipo_noticia VARCHAR(50), -- breaking, feature, opinion, etc.
    complejidad_estimada VARCHAR(20), -- simple, media, compleja
    
    -- Resultados de Negocio (para análisis posterior)
    engagement_promedio DECIMAL(8,2), -- views, likes, shares
    tiempo_en_tendencia INTEGER, -- minutos en trending
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🎨 Implementación en Frontend

### **� Control de Acceso**
- **Solo visible para administradores**: `isAdmin()` debe retornar `true`
- **Ocultado para usuarios regulares**: Editores y colaboradores no verán estas métricas
- **Variable de entorno**: `VITE_SHOW_ADMIN_METRICS=true` (solo en builds administrativos)

### **�📍 Ubicación**: Panel Derecho - Debajo de Botones

```jsx
{/* Pie de métricas con enfoque periodístico - SOLO ADMIN */}
{isAdmin() && (
  <div className="bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-700 p-6">
    <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">
      📊 Impacto de la IA en el Proceso: <span className="text-xs text-red-600">(Solo Admin)</span>
    </h3>
  
  <div className="grid grid-cols-2 gap-4 text-sm text-slate-600 dark:text-slate-400">
    {/* Ahorro de Tiempo */}
    <div className="flex items-center gap-2">
      <span className="text-green-600 dark:text-green-400 font-bold">⚡</span>
      <span>Ahorro: <strong className="text-green-600">-{metricas.ahorro_tiempo_minutos} min</strong></span>
    </div>
    
    {/* Costo vs Manual */}
    <div className="flex items-center gap-2">
      <span className="text-blue-600 dark:text-blue-400 font-bold">💰</span>
      <span>Costo: <strong>${metricas.costo_generacion}</strong> vs ${metricas.costo_manual}</span>
    </div>
    
    {/* Productividad */}
    <div className="flex items-center gap-2">
      <span className="text-purple-600 dark:text-purple-400 font-bold">📈</span>
      <span>Formatos: <strong>{metricas.cantidad_formatos}</strong> simultáneos</span>
    </div>
    
    {/* Velocidad */}
    <div className="flex items-center gap-2">
      <span className="text-orange-600 dark:text-orange-400 font-bold">🚀</span>
      <span>Velocidad: <strong>{metricas.palabras_por_segundo} pal/s</strong></span>
    </div>
  </div>
  
  {/* Indicador de ROI */}
  <div className="mt-3 p-2 bg-green-50 dark:bg-green-900/20 rounded-lg">
    <div className="flex items-center gap-2">
      <TrendingUp className="w-4 h-4 text-green-600" />
      <span className="text-sm font-semibold text-green-700 dark:text-green-400">
        ROI: {metricas.roi_porcentaje}% más eficiente que proceso manual
      </span>
    </div>
  </div>
)}
```

---

## 🔧 Implementación en Backend

### **📍 Captura en `services/generador_ia.py`**

```python
class GeneradorIA:
    async def generar_contenido_salida(self, noticia, salida, prompt, estilo):
        # Capturar tiempo inicio
        inicio = datetime.now()
        
        try:
            # ... lógica de generación existente ...
            respuesta = await cliente_llm.generar(...)
            
            # Capturar métricas
            fin = datetime.now()
            tiempo_generacion = (fin - inicio).total_seconds()
            tokens_usados = respuesta.usage.total_tokens if hasattr(respuesta, 'usage') else 0
            
            # Calcular métricas de valor periodístico
            await self._guardar_metricas_valor(
                noticia_id=noticia.id,
                tiempo_generacion=tiempo_generacion,
                tokens=tokens_usados,
                modelo=self.llm_config.modelo,
                salidas_generadas=len(salidas_solicitadas)
            )
            
        except Exception as e:
            # También capturar métricas de errores
            await self._guardar_metricas_error(...)
```

### **📍 Endpoint en `routers/generacion.py`**

```python
@router.post("/generar-temporal")
async def generar_temporal(request: GeneracionRequest, current_user: Usuario = Depends(get_current_user)):
    metricas_sesion = []
    
    for salida in salidas_seleccionadas:
        # ... generación ...
        
        # Obtener métricas de valor periodístico (solo para admin)
        metricas = None
        if current_user.rol == "admin":
            metricas = await obtener_metricas_valor_recientes(noticia_temporal.id)
            metricas_sesion.append(metricas)
    
    response_data = {
        "salidas_generadas": salidas
    }
    
    # Solo incluir métricas si el usuario es administrador
    if current_user.rol == "admin" and metricas_sesion:
        # Calcular métricas agregadas
        total_tiempo = sum(m.tiempo_generacion for m in metricas_sesion)
        ahorro_estimado = calcular_ahorro_vs_manual(len(salidas_seleccionadas), complejidad)
        costo_total = sum(m.costo_generacion for m in metricas_sesion)
        
        response_data["metricas_valor"] = {
            "ahorro_tiempo_minutos": ahorro_estimado,
            "costo_generacion": costo_total,
            "cantidad_formatos": len(salidas_seleccionadas),
            "roi_porcentaje": calcular_roi(ahorro_estimado, costo_total),
            "velocidad_palabras_segundo": calcular_velocidad(total_palabras, total_tiempo)
        }
    
    return response_data
```

---

## 📊 Dashboard Futuro: "Valor de la IA Periodística"

### **� Acceso Exclusivo Administrativo**
El dashboard de métricas será una sección completa del panel administrativo, accesible únicamente para usuarios con rol `admin`.

### **�📈 KPIs Principales:**
1. **Ahorro temporal total** (horas/semana)
2. **Reducción de costos** (% vs proceso manual)  
3. **Aumento de productividad** (noticias/día/redactor)
4. **Velocidad de respuesta** (breaking news)
5. **Multi-formato efficiency** (salidas simultáneas)

### **📈 Reportes de Impacto:**
- "La IA nos ahorra 15 horas/semana en redacción"
- "Reducción de 40% en costo por noticia publicada"
- "300% más formatos generados con el mismo equipo"  
- "Breaking news 5x más rápidas de publicar"

### **📊 Métricas para Directivos:**
- **ROI mensual**: Ahorro vs inversión en IA
- **Productividad del equipo**: Antes vs después
- **Calidad mantenida**: Engagement sin pérdida de audiencia
- **Velocidad competitiva**: Time-to-market vs competencia

---

## 🎯 Objetivos de Medición

### **📈 Justificar Inversión:**
- Demostrar ROI positivo de implementación IA
- Cuantificar beneficios vs costos operativos
- Mostrar mejoras en eficiencia del equipo periodístico

### **📊 Optimizar Procesos:**
- Identificar qué tipos de noticias se benefician más de IA
- Encontrar el balance óptimo IA/edición manual
- Mejorar tiempo de respuesta en breaking news

### **🎯 Toma de Decisiones:**
- Expandir uso de IA a más secciones
- Invertir en modelos más avanzados
- Contratar menos redactores o redirigir talento

---

## 📝 Próximos Pasos para Implementación

1. **✅ Crear tabla `metricas_valor_periodistico`**
2. **✅ Modificar `GeneradorIA`** para capturar métricas
3. **✅ Actualizar endpoints** para devolver métricas solo a admins
4. **✅ Implementar pie visual** en panel derecho con control `isAdmin()`
5. **✅ Agregar configuración** con variable de entorno `VITE_SHOW_ADMIN_METRICS`
6. **🔄 Fase 2**: Dashboard de métricas agregadas (sección admin)
7. **🔄 Fase 3**: Reportes ejecutivos automatizados

### **🔐 Consideraciones de Seguridad**
- **Backend**: Validar rol de administrador en todos los endpoints de métricas
- **Frontend**: Ocultar componente completo si no es admin
- **Variables de entorno**: Separar builds para diferentes niveles de acceso
- **Logging**: Registrar accesos a métricas para auditoría

---

## 📅 Estado del Documento

- **Creado**: 27/10/2025
- **Estado**: Análisis completo - Listo para implementación
- **Próximo paso**: Implementar según acuerdo con stakeholders
- **Archivo**: `docs/METRICAS_VALOR_PERIODISTICO.md`

---

*Documento generado para Sistema de Noticias con IA v2.4.0*