

import React, { useState, useEffect } from "react";
import NoticiaForm from "./components/NoticiaForm";
import NoticiasGeneradasPanel from "./components/NoticiasGeneradasPanel";
import { useAuth } from "./context/AuthContext";

import generacionService from "./services/generacion";
import { salidaService, llmService } from "./services/maestros";

import { api } from "./services/api";

function NoticiaGeneracionVista({ noticiaId: noticiaIdProp, onVolverLista }) {
  const { token } = useAuth();
  
  // Detectar si estamos en modo edición desde URL
  const urlParams = new URLSearchParams(window.location.search);
  const editId = urlParams.get('edit');
  const isEditMode = editId && !isNaN(parseInt(editId));
  
  // Estado para controlar si el modo edición es válido
  const [editModeValid, setEditModeValid] = useState(!isEditMode); // Si no es modo edición, es válido por defecto
  
  const [noticiasPorSalida, setNoticiasPorSalida] = useState({
    impreso: [],
    web: [],
    twitter: [],
    instagram: [],
    facebook: [],
  });
  const [noticiaId, setNoticiaId] = useState(noticiaIdProp || (isEditMode ? parseInt(editId) : null));
  const [noticiaFormData, setNoticiaFormData] = useState(null);
  const [loadingSalidas, setLoadingSalidas] = useState(false);
  const [loadingPublicar, setLoadingPublicar] = useState(false);
  const [salidasMaestro, setSalidasMaestro] = useState([]);
  const [llms, setLlms] = useState([]);
  // El llmId real debe sincronizarse con el form y el selector
  const [llmId, setLlmId] = useState("");
  
  // Estado para salidas temporales (antes de publicar)
  const [salidasTemporales, setSalidasTemporales] = useState([]);
  
  // Estado para métricas de valor periodístico (solo para admins)
  const [metricas, setMetricas] = useState(null);

  // Obtener salidas reales desde el backend
  useEffect(() => {
    async function fetchSalidas() {
      try {
        const data = await salidaService.getAll({ activo: true });
        setSalidasMaestro(data || []);
      } catch {
        setSalidasMaestro([]);
      }
    }
    fetchSalidas();
  }, []);

  // Obtener LLMs activos desde el backend
  useEffect(() => {
    async function fetchLlms() {
      try {
        const data = await llmService.getActivos();
        let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
        setLlms(lista);
        
        // Autoseleccionar el primer LLM que esté configurado (con API key)
        if (lista && lista.length > 0) {
          const llmConfigurado = lista.find(llm => llm.api_key && llm.api_key.length > 10);
          if (llmConfigurado) {
            console.log(`🎯 LLM autoseleccionado: ${llmConfigurado.nombre} (${llmConfigurado.proveedor})`);
            setLlmId(llmConfigurado.id);
          } else {
            console.log("⚠️ No hay LLMs configurados. Usando el primero disponible.");
            setLlmId(lista[0].id);
          }
        }
      } catch {
        setLlms([]);
      }
    }
    fetchLlms();
  }, []);

  // Cargar datos de la noticia si estamos en modo edición
  useEffect(() => {
    if (isEditMode && noticiaId) {
      async function cargarNoticiaParaEdicion() {
        try {
          console.log(`📝 Cargando noticia ${noticiaId} para edición...`);
          const noticia = await api.getNoticia(noticiaId);
          
          // Establecer los datos del formulario con la noticia existente
          setNoticiaFormData({
            id: noticia.id, // ✅ Incluir el ID para que NoticiaForm detecte modo edición
            titulo: noticia.titulo,
            contenido: noticia.contenido,
            seccion_id: noticia.seccion_id,
            proyecto_id: noticia.proyecto_id || null
          });
          
          console.log("✅ Noticia cargada para edición:", noticia.titulo);
          setEditModeValid(true); // ✅ Modo edición válido
        } catch (error) {
          console.error("❌ Error cargando noticia para edición:", error);
          
          // Si la noticia no existe, limpiar la URL y cambiar a modo creación
          if (error?.response?.status === 404 || error?.message?.includes('404')) {
            console.log("🔄 Noticia no encontrada, cambiando a modo creación...");
            // Limpiar parámetros de URL
            window.history.pushState({}, '', '/crear');
            // Salir del modo edición
            setNoticiaId(null);
            setEditModeValid(false); // ❌ Modo edición inválido
            alert("La noticia que intentas editar ya no existe. Se ha cambiado a modo creación.");
          } else {
            setEditModeValid(false); // ❌ Modo edición inválido por error
            alert("Error al cargar la noticia para edición: " + (error?.response?.data?.detail || error.message));
          }
        }
      }
      
      cargarNoticiaParaEdicion();
    }
  }, [isEditMode, noticiaId]);

  // Handler para cuando se genera una noticia y sus salidas (creación o edición)
  const handleGenerarNoticias = async (form, salidas_ids) => {
    // Validaciones básicas
    if (!form.titulo || !form.contenido || !form.seccion_id) {
      alert("Por favor completa título, contenido y sección antes de generar");
      return;
    }

    // Sincroniza llmId con el form
    const llm_id_final = form.llm_id || llmId;
    if (!llm_id_final) {
      alert("Debes seleccionar un modelo de IA (LLM)");
      return;
    }

    if (!salidas_ids || salidas_ids.length === 0) {
      alert("Debes seleccionar al menos una salida para generar");
      return;
    }

    console.log("🔍 Debug - Datos para generación:", {
      llm_id_final,
      salidas_ids,
      form
    });

    setLoadingSalidas(true);
    setMetricas(null); // Limpiar métricas previas
    try {
      // 1. Para CUALQUIER caso: NO crear en BD, solo generar con IA usando datos temporales
      const datosParaIA = {
        id: noticiaId || null, // null para creación, ID para edición
        titulo: form.titulo,
        contenido: form.contenido,
        seccion_id: form.seccion_id,
        proyecto_id: form.proyecto_id
      };

      // 2. Generar salidas usando IA con datos temporales (NO guardar en BD)
      console.log("🎯 Generando salidas con IA (modo temporal):", datosParaIA);
      
      // Usar el endpoint temporal específico
      const resultadoGeneracion = await generacionService.generarSalidasTemporal({
        datosNoticia: datosParaIA,  // Datos temporales para enviar al backend
        salidas_ids: salidas_ids,
        llm_id: llm_id_final,
        regenerar: true
      });

      console.log("✅ Salidas generadas (temporal):", resultadoGeneracion);

      // Extraer métricas si están disponibles (solo para admins)
      if (resultadoGeneracion.metricas_valor) {
        console.log("📈 Métricas de valor recibidas:", resultadoGeneracion.metricas_valor);
        setMetricas(resultadoGeneracion.metricas_valor);
      } else {
        setMetricas(null);
      }

      // 3. Procesar salidas temporales (no están en BD)
      if (resultadoGeneracion.salidas_generadas && resultadoGeneracion.salidas_generadas.length > 0) {
        console.log("📋 Procesando salidas temporales:", resultadoGeneracion.salidas_generadas);
        
        // Agrupar salidas temporales por tipo para el panel derecho
        const agrupadas = { impreso: [], web: [], twitter: [], instagram: [], facebook: [] };
        
        for (const salida of resultadoGeneracion.salidas_generadas) {
          let clave = (salida.nombre_salida || '').normalize('NFD').replace(/\p{Diacritic}/gu, '').replace(/\s+/g, '').toLowerCase();
          
          if (clave.includes('impreso') || clave.includes('print')) clave = 'impreso';
          else if (clave.includes('web') || clave.includes('digital')) clave = 'web';
          else if (clave.includes('twitter')) clave = 'twitter';
          else if (clave.includes('instagram')) clave = 'instagram';
          else if (clave.includes('facebook')) clave = 'facebook';
          else clave = null;
          
          if (clave && agrupadas[clave]) {
            agrupadas[clave].push({
              ...salida,
              contenido: salida.contenido_generado, // Para temporal
              temporal: true // Marca que es temporal
            });
          }
        }

        console.log("📊 Salidas agrupadas (temporal):", agrupadas);
        setNoticiasPorSalida(agrupadas);
        
        // Guardar salidas temporales para uso posterior en "Publicar"
        setSalidasTemporales(resultadoGeneracion.salidas_generadas);
        
      } else {
        console.log("⚠️ No se generaron salidas. Creando mensaje informativo...");
        setNoticiasPorSalida({
          "info": [{
            id: 1,
            titulo: "⚠️ No se generaron salidas",
            contenido: `No se pudieron generar salidas con IA. Posibles causas:

📋 **Verificar configuración:**
• ¿Está seleccionado un modelo con "✅ Listo"?
• ¿La sección tiene prompts y estilos configurados?
• ¿Hay problemas de conectividad con la API del LLM?

🔧 **Soluciones:**
• Cambiar a un modelo que muestre "✅ Listo"
• Verificar que la sección tenga prompt y estilo
• En caso de error de API, el sistema usará modo simulado

💡 **Recomendación:** Usar Gemini si está disponible y configurado.`,
            nombre_salida: "Información"
          }]
        });
      }

      // 4. Actualizar form data (modo temporal)
      setNoticiaFormData({ 
        ...form, 
        salidas_ids, 
        llm_id: llm_id_final,
        temporal: !noticiaId // Marcar como temporal si es creación
      });

    } catch (err) {
      console.error("❌ Error generando noticias:", err);
      alert("Error generando salidas: " + (err?.response?.data?.detail || err.message));
    } finally {
      setLoadingSalidas(false);
    }
  };

  // Cargar noticia y salidas si noticiaIdProp está presente (modo edición)
  useEffect(() => {
    if (!noticiaIdProp) return;
    async function fetchNoticiaYSalidas() {
      setLoadingSalidas(true);
      try {
        const noticia = await api.getNoticia(noticiaIdProp);
        // Debug: mostrar datos de la noticia en consola
        console.log('Datos de la noticia desde la base de datos:', noticia);
        let salidas = [];
        try {
          salidas = await generacionService.obtenerSalidasNoticia(noticiaIdProp);
          // Debug: mostrar datos de las salidas generadas en consola
          console.log('Datos de las salidas generadas desde la base de datos:', salidas);
          // Log detallado de nombre_salida
          salidas.forEach((s, i) => {
            console.log(`Salida[${i}]: id=${s.id}, salida_id=${s.salida_id}, nombre_salida='${s.nombre_salida}'`);
          });
        } catch (errSalidas) {
          // Si es 404, simplemente no hay salidas generadas aún
          if (!(errSalidas?.response && errSalidas.response.status === 404)) {
            alert("Error cargando salidas: " + (errSalidas?.message || ''));
          }
          salidas = [];
        }
        // Agrupar salidas por tipo y mapear contenido_generado -> contenido
        const agrupadas = { impreso: [], web: [], twitter: [], instagram: [], facebook: [] };
        for (const salida of salidas) {
          let clave = (salida.nombre_salida || '').normalize('NFD').replace(/\p{Diacritic}/gu, '').replace(/\s+/g, '').toLowerCase();
          if (clave.includes('impreso') || clave.includes('print')) clave = 'impreso';
          else if (clave.includes('web') || clave.includes('digital')) clave = 'web';
          else if (clave.includes('twitter')) clave = 'twitter';
          else if (clave.includes('instagram')) clave = 'instagram';
          else if (clave.includes('facebook')) clave = 'facebook';
          else clave = null;
          if (clave && agrupadas[clave]) {
            agrupadas[clave].push({
              ...salida,
              contenido: salida.contenido_generado // mapea para el panel
            });
          }
        }
        // Log para depuración de agrupamiento de salidas
        console.log('Agrupadas para panel derecho:', agrupadas);
        setNoticiasPorSalida(agrupadas);
        setNoticiaFormData({
          titulo: noticia.titulo,
          contenido: noticia.contenido,
          seccion_id: noticia.seccion_id,
          proyecto_id: noticia.proyecto_id,
          salidas_ids: noticia.salidas_ids || [],
          llm_id: noticia.llm_id ? String(noticia.llm_id) : ""
        });
        // Sincroniza el selector de LLM con el valor de la noticia (siempre string)
        setLlmId(noticia.llm_id ? String(noticia.llm_id) : "");
        setNoticiaId(noticiaIdProp);
      } finally {
        setLoadingSalidas(false);
      }
    }
    fetchNoticiaYSalidas();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [noticiaIdProp]);

  return (
    <div className="flex flex-col md:flex-row gap-8 w-full">
      <div className="flex-1">
        <NoticiaForm
          noticia={noticiaFormData}
          loading={loadingSalidas}
          onClose={() => { if (onVolverLista) onVolverLista(); }}
          onGenerarNoticias={handleGenerarNoticias}
          extraFields={
            <div className="mt-4">
              <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">Modelo de IA (LLM) *</label>
              <select
                value={llmId}
                onChange={e => {
                  setLlmId(e.target.value);
                  // Si hay datos cargados, sincroniza el form también
                  setNoticiaFormData(prev => prev ? { ...prev, llm_id: e.target.value } : prev);
                }}
                className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-colors"
              >
                <option value="">-- Selecciona un modelo de IA --</option>
                {llms.map(llm => {
                  // Determinar si está configurado basado en si tiene API key
                  const configurado = llm.api_key && llm.api_key.length > 10;
                  const estado = configurado ? "✅" : "⚠️";
                  const descripcion = configurado ? "Listo" : "No configurado";
                  
                  return (
                    <option 
                      key={llm.id} 
                      value={llm.id}
                      disabled={!configurado}
                    >
                      {estado} {llm.nombre} ({llm.proveedor}) - {descripcion}
                    </option>
                  );
                })}
              </select>
              {llmId && (
                <p className="text-sm text-slate-600 dark:text-slate-400 mt-2">
                  💡 <strong>Recomendación:</strong> Si tienes problemas, prueba con un modelo que muestre "✅ Listo"
                </p>
              )}
            </div>
          }
        />
      </div>
      <div className="flex-1 min-w-[350px]">
        <NoticiasGeneradasPanel
          noticiasPorSalida={noticiasPorSalida}
          loading={loadingSalidas}
          noticiaFormData={noticiaFormData}
          llmId={llmId}
          salidasTemporales={salidasTemporales}
          metricas={metricas}
          onPublicado={() => { if (onVolverLista) onVolverLista(true); }}
        />
      </div>
    </div>
  );
}

export default NoticiaGeneracionVista;
