# 🛠️ Propuesta: Vistas de Mantenimiento v2.4.0

## 📊 **Resumen Ejecutivo**

El sistema necesita vistas de mantenimiento dedicadas para:
1. **Gestión de Usuarios y Jerarquías**: Roles, supervisores, secciones asignadas
2. **Configuración de Métricas**: Seguimiento del valor periodístico de la IA
3. **Administración del Sistema**: Configuración global y auditoría

## 🎯 **Justificación**

### **Problemas Actuales:**
- ❌ No hay interfaz para gestionar usuarios más allá del registro básico
- ❌ No se pueden asignar jerarquías editoriales (supervisor_id, secciones)
- ❌ Las métricas de valor periodístico están documentadas pero no implementadas
- ❌ No hay visibilidad de la configuración del sistema para administradores
- ❌ No hay auditoría de cambios críticos

### **Beneficios Esperados:**
- ✅ Control granular de acceso basado en jerarquía editorial real
- ✅ Métricas de ROI para justificar inversión en IA
- ✅ Reducción de tiempo en configuración manual
- ✅ Visibilidad completa del estado del sistema
- ✅ Auditoría para cumplimiento y seguridad

---

## 🧑‍💼 **Vista 1: Administración de Usuarios**

### **Funcionalidades Principales:**

#### **Lista de Usuarios Avanzada**
```typescript
interface UsuarioExtendido {
  id: number;
  username: string;
  email: string;
  nombre_completo: string;
  role: 'admin' | 'director' | 'jefe_seccion' | 'redactor' | 'viewer';
  supervisor_id?: number;
  secciones_asignadas: number[];
  is_active: boolean;
  last_login?: Date;
  noticias_count: number;
  metricas_productividad: {
    noticias_mes: number;
    tiempo_promedio: number;
    calidad_promedio: number;
  };
}
```

#### **Formulario de Edición**
- **Información Básica**: Email, username, nombre completo
- **Roles y Permisos**: 
  - Sistema Admin (acceso total)
  - Director de Redacción (ve todo editorial)
  - Jefe de Sección (ve su equipo)
  - Redactor (ve solo sus noticias)
  - Viewer (solo lectura)
- **Jerarquía Editorial**:
  - Selector de supervisor (solo para jefes de sección y redactores)
  - Multi-selector de secciones asignadas
  - Vista de equipo (subordinados directos)
- **Estado y Configuración**:
  - Activo/Inactivo
  - Fecha de expiración de acceso
  - Límites de uso de IA (tokens/día)

#### **Vista de Jerarquía**
```
📊 Director de Redacción (María González)
├── 📰 Jefe Sección Política (Juan Pérez)
│   ├── ✍️ Redactor Ana López
│   └── ✍️ Redactor Carlos Ruiz
├── 🎭 Jefe Sección Cultura (Sofia Martín)
│   └── ✍️ Redactor Laura Torres
└── ⚽ Jefe Sección Deportes (Miguel Ángel)
    ├── ✍️ Redactor Pedro Santos
    └── ✍️ Redactor Elena Vargas
```

#### **Acciones Masivas**
- Activar/Desactivar múltiples usuarios
- Cambiar supervisor en lote
- Exportar lista con métricas
- Enviar notificaciones

---

## 📈 **Vista 2: Configuración de Métricas**

### **Panel de Control de Métricas**

#### **Configuración de Indicadores**
```typescript
interface MetricaConfig {
  id: string;
  nombre: string;
  descripcion: string;
  activa: boolean;
  peso: number; // 1-10 para ponderación
  thresholds: {
    excelente: number;
    bueno: number;
    regular: number;
  };
  frecuencia_calculo: 'tiempo_real' | 'diario' | 'semanal';
}
```

**Métricas Disponibles:**
1. **Eficiencia Operativa**
   - Tiempo promedio de generación
   - Reducción vs. redacción manual
   - Tokens utilizados por noticia
   
2. **Calidad del Contenido**
   - Score de legibilidad
   - Coherencia temática
   - Originalidad (anti-plagio)
   
3. **Impacto Editorial**
   - Tasa de publicación (IA vs manual)
   - Engagement estimado
   - Satisfacción del editor

#### **Dashboard de Valor Periodístico**
- **KPIs Principales**: Cards con valores actuales vs objetivos
- **Gráficos de Tendencia**: Evolución temporal de métricas clave
- **Comparativas**: IA vs manual, por sección, por redactor
- **Alertas**: Métricas fuera de rangos esperados

#### **Configuración de Reportes**
- **Frecuencia**: Diaria, semanal, mensual
- **Destinatarios**: Lista de emails para envío automático
- **Formato**: PDF, Excel, dashboard web
- **Contenido**: Selección de métricas a incluir

---

## ⚙️ **Vista 3: Administración del Sistema**

### **Configuración Global**

#### **Parámetros del Sistema**
- **Modo de Publicación**: Simplificado vs. Completo
- **Límites Globales**: Tokens/día, usuarios concurrentes
- **Configuración de IA**: Timeouts, reintentos, fallbacks
- **Seguridad**: Políticas de contraseñas, expiración de sesiones

#### **Monitor de Estado**
- **Salud del Sistema**: APIs, base de datos, servicios IA
- **Uso de Recursos**: CPU, memoria, almacenamiento
- **Estadísticas de Uso**: Usuarios activos, noticias generadas/día
- **Logs de Sistema**: Errores, warnings, eventos importantes

#### **Auditoría y Seguridad**
- **Log de Acciones**: Quién hizo qué y cuándo
- **Cambios Críticos**: Modificaciones a usuarios admin, configuración
- **Intentos de Acceso**: Logins fallidos, accesos no autorizados
- **Backup Status**: Estado de respaldos automáticos

---

## 🏗️ **Arquitectura Técnica**

### **Backend - Nuevos Endpoints**

```python
# routers/admin_usuarios.py
@router.get("/admin/usuarios", dependencies=[Depends(require_admin)])
async def get_usuarios_admin() -> List[UsuarioExtendido]:
    """Lista completa con métricas y jerarquía"""

@router.put("/admin/usuarios/{user_id}", dependencies=[Depends(require_admin)])
async def update_usuario_admin(user_id: int, data: UsuarioUpdate):
    """Actualización completa incluyendo rol y jerarquía"""

@router.post("/admin/usuarios/{user_id}/assign-supervisor")
async def assign_supervisor(user_id: int, supervisor_id: int):
    """Asignar supervisor en jerarquía editorial"""

# routers/admin_metricas.py
@router.get("/admin/metricas/config", dependencies=[Depends(require_admin)])
async def get_metricas_config() -> List[MetricaConfig]:
    """Configuración de métricas"""

@router.get("/admin/metricas/dashboard", dependencies=[Depends(require_admin)])
async def get_dashboard_data() -> DashboardData:
    """Datos para dashboard de métricas"""

@router.post("/admin/metricas/calculate", dependencies=[Depends(require_admin)])
async def trigger_metrics_calculation():
    """Recalcular métricas manualmente"""
```

### **Frontend - Nuevos Componentes**

```typescript
// components/admin/
- UsuariosAdminList.jsx      // Lista con filtros y búsqueda
- UsuarioAdminForm.jsx       // Formulario completo de edición
- JerarquiaViewer.jsx        // Vista de árbol organizacional
- MetricasConfig.jsx         // Configuración de métricas
- MetricasDashboard.jsx      // Dashboard con gráficos
- SistemaMonitor.jsx         // Estado del sistema
- AuditoriaLog.jsx           // Registro de auditoría
```

### **Base de Datos - Nuevas Tablas**

```sql
-- Extensión de usuarios para jerarquía
ALTER TABLE usuarios ADD COLUMN supervisor_id INTEGER REFERENCES usuarios(id);
ALTER TABLE usuarios ADD COLUMN secciones_asignadas INTEGER[];
ALTER TABLE usuarios ADD COLUMN limite_tokens_diario INTEGER DEFAULT 10000;

-- Tabla de métricas
CREATE TABLE metricas_valor (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha DATE NOT NULL,
    tiempo_generacion_promedio DECIMAL(10,2),
    calidad_promedio DECIMAL(3,2),
    eficiencia_score DECIMAL(3,2),
    noticias_generadas INTEGER,
    tokens_utilizados INTEGER,
    valor_estimado_usd DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Configuración de métricas
CREATE TABLE metricas_config (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    activa BOOLEAN DEFAULT true,
    peso INTEGER DEFAULT 5,
    configuracion JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Auditoría
CREATE TABLE auditoria_log (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(50) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INTEGER,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🎨 **Diseño UX/UI**

### **Navegación**
```
Sistema de Noticias IA
├── 📰 Noticias (existente)
├── 👥 Proyectos (existente)
├── 🎯 Maestros (existente)
└── ⚙️ Administración (NUEVO - solo admins)
    ├── 👥 Gestión de Usuarios
    ├── 📊 Métricas y Valor
    └── 🔧 Configuración del Sistema
```

### **Permisos de Acceso**
- **Sistema Admin**: Ve todas las vistas de administración
- **Director de Redacción**: Ve gestión de usuarios (sin métricas técnicas)
- **Jefe de Sección**: Ve solo su equipo en usuarios
- **Redactor/Viewer**: No ve vistas de administración

### **Responsive Design**
- **Desktop**: Vistas completas con tablas y gráficos
- **Tablet**: Layout adaptado, funcionalidad reducida
- **Mobile**: Solo vistas críticas (estado del sistema, usuarios básico)

---

## 📅 **Plan de Implementación**

### **Fase 1: Gestión de Usuarios (2-3 días)**
1. Crear backend APIs para administración de usuarios
2. Implementar componentes frontend básicos
3. Agregar campos de jerarquía a la base de datos
4. Testing y validación

### **Fase 2: Configuración de Métricas (3-4 días)**
1. Crear tablas de métricas y configuración
2. Implementar cálculo básico de métricas
3. Crear dashboard frontend
4. Configuración de reportes automáticos

### **Fase 3: Administración del Sistema (2-3 días)**
1. Monitor de estado y salud del sistema
2. Sistema de auditoría
3. Configuración global
4. Testing integral

### **Fase 4: Pulimiento y Documentación (1-2 días)**
1. Refinamiento de UX
2. Optimización de performance
3. Documentación de usuario
4. Testing de regresión

**Tiempo Total Estimado: 8-12 días**

---

## 🚀 **Próximos Pasos**

1. **Validación de Propuesta**: Revisar y ajustar según feedback
2. **Priorización**: Decidir qué vista implementar primero
3. **Diseño Detallado**: Wireframes y especificaciones técnicas
4. **Setup de Desarrollo**: Crear ramas y estructura de archivos
5. **Implementación Iterativa**: Desarrollo por fases con testing continuo

---

## 💡 **Consideraciones Importantes**

### **Seguridad**
- Todas las vistas de administración requieren autenticación admin
- Auditoría completa de acciones sensibles
- Validación estricta de permisos en backend

### **Performance**
- Caching para métricas calculadas
- Paginación en listas grandes de usuarios
- Lazy loading para gráficos complejos

### **Usabilidad**
- Interfaces intuitivas siguiendo patrones existentes
- Confirmación para acciones destructivas
- Feedback claro de estado de operaciones

### **Escalabilidad**
- Diseño preparado para crecimiento de usuarios
- Métricas optimizadas para grandes volúmenes
- APIs diseñadas para futuras integraciones

---

*Documento generado para Sistema de Noticias con IA v2.4.0*  
*Fecha: Octubre 2025*