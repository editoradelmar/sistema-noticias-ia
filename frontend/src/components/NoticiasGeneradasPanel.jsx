import React, { useState } from "react";
import { FileText, Edit, Trash2, Send, Copy } from 'lucide-react';
import generacionService from '../services/generacion';
import Toast from './Toast';
import { api } from '../services/api';
import MetricasValor from './MetricasValor';

export default function NoticiasGeneradasPanel({ noticiasPorSalida, puedePublicar, onPublicado, noticiaFormData, llmId, loadingGeneracion, loadingPublicacion, metricas }) {
  // Variable de entorno para controlar el modo de funcionamiento
  const simplifiedMode = import.meta.env.VITE_SIMPLIFIED_PUBLICATION_MODE === 'true';

  const salidas = [
    { key: "impreso", label: "Impreso" },
    { key: "web", label: "Web" },
    { key: "twitter", label: "Twitter/X" },
    { key: "instagram", label: "Instagram" },
    { key: "facebook", label: "Facebook" },
  ];

  // Tabs para salidas seleccionadas
  const salidasConNoticias = salidas.filter(s => Array.isArray(noticiasPorSalida[s.key]) && noticiasPorSalida[s.key].length > 0);
  const [tab, setTab] = useState(() => salidasConNoticias.length > 0 ? salidasConNoticias[0].key : "");

  // Actualizar el tab si cambian las salidas generadas
  React.useEffect(() => {
    const nuevasSalidas = salidas.filter(s => Array.isArray(noticiasPorSalida[s.key]) && noticiasPorSalida[s.key].length > 0);
    if (nuevasSalidas.length > 0 && !nuevasSalidas.some(s => s.key === tab)) {
      setTab(nuevasSalidas[0].key);
    }
    if (nuevasSalidas.length === 0) {
      setTab("");
    }
  }, [noticiasPorSalida]);
  // Estado por id de salida, para cada canal
  const [contenidoPorSalida, setContenidoPorSalida] = useState({}); // { [id]: contenido }
  const [tituloPorSalida, setTituloPorSalida] = useState({}); // { [id]: titulo }
  // Eliminados estados de guardado manual

  // Actualizar contenido editable por salida
  const handleContenidoChange = (salidaKey, value) => {
    setContenidoPorSalida(prev => ({ ...prev, [salidaKey]: value }));
  };
  const handleTituloChange = (salidaKey, value) => {
    setTituloPorSalida(prev => ({ ...prev, [salidaKey]: value }));
  };

  // Guardar todas las salidas editadas antes de publicar
  const guardarTodasLasSalidas = async () => {
    // Recorrer TODAS las salidas individuales y guardar cada una
    const updates = [];
    Object.entries(noticiasPorSalida).forEach(([key, arr]) => {
      if (!Array.isArray(arr) || arr.length === 0) return;
      arr.forEach(noticiaSalida => {
        const id = noticiaSalida.id;
        const titulo = typeof tituloPorSalida[id] === 'string' ? tituloPorSalida[id] : noticiaSalida.titulo;
        const contenido = typeof contenidoPorSalida[id] === 'string' ? contenidoPorSalida[id] : noticiaSalida.contenido;
        if (titulo !== noticiaSalida.titulo || contenido !== noticiaSalida.contenido) {
          updates.push(generacionService.updateSalida(id, { titulo, contenido_generado: contenido }));
        }
      });
    });
    await Promise.all(updates);
  };

  // --- Botón de publicación y copiar ---
  const haySalidaConContenido = Object.values(noticiasPorSalida).some(arr =>
    Array.isArray(arr) && arr.some(noticiaSalida => {
      const titulo = typeof tituloPorSalida[noticiaSalida.id] === 'string' ? tituloPorSalida[noticiaSalida.id] : noticiaSalida.titulo;
      const contenido = typeof contenidoPorSalida[noticiaSalida.id] === 'string' ? contenidoPorSalida[noticiaSalida.id] : noticiaSalida.contenido;
      return !!(titulo && titulo.trim().length > 0 && contenido && contenido.trim().length > 0);
    })
  );

  const [copiado, setCopiado] = useState(false);
  const [toast, setToast] = useState({ show: false, message: "" });
  const [loadingPublicar, setLoadingPublicar] = useState(false);

  const handlePublicar = async () => {
    if (loadingPublicar) return; // Evitar doble clic

    // Mostrar métricas en consola justo antes de publicar
    if (typeof metricas === 'object' && metricas !== null && Object.keys(metricas).length > 0) {
      console.log('📊 Métricas a publicar:', metricas);
    } else {
      setToast({ show: true, message: 'Error: No hay métricas calculadas para publicar. No se enviará el registro.' });
      console.error('❌ Error: No hay métricas calculadas para publicar.');
      return;
    }

    // Validar y construir métricas completas para el payload
    const metricasCompletas = {
      tiempo_generacion_total: metricas?.tiempo_generacion_total ?? 0,
      ahorro_tiempo_minutos: metricas?.ahorro_tiempo_minutos ?? 0,
      ahorro_costo: metricas?.ahorro_costo ?? 0,
      costo_generacion: metricas?.costo_generacion ?? 0,
      costo_estimado_manual: metricas?.costo_estimado_manual ?? 0,
      cantidad_salidas_generadas: metricas?.cantidad_salidas_generadas ?? 0,
      cantidad_formatos_diferentes: metricas?.cantidad_formatos_diferentes ?? 0,
      velocidad_palabras_por_segundo: metricas?.velocidad_palabras_por_segundo ?? 0,
      modelo_usado: metricas?.modelo_usado ?? '',
      usuario_id: metricas?.usuario_id ?? null,
      tipo_noticia: metricas?.tipo_noticia ?? '',
      complejidad_estimada: metricas?.complejidad_estimada ?? '',
      roi_porcentaje: metricas?.roi_porcentaje ?? 0,
      tokens_total: metricas?.tokens_total ?? 0
    };

    setLoadingPublicar(true);
    try {
      // Determinar el llm_id a usar: preferir noticiaFormData.llm_id, si no, usar llmId prop
      let llm_id_final = noticiaFormData?.llm_id ? Number(noticiaFormData.llm_id) : (llmId ? Number(llmId) : null);
      if (!llm_id_final || isNaN(llm_id_final)) {
        setToast({ show: true, message: 'Debes seleccionar un modelo de IA (LLM) válido antes de publicar.' });
        throw new Error('Modelo de IA no válido');
      }
    // Validar que todos los títulos estén presentes para cada salida individual
    const salidasPublicadas = [];
    Object.entries(noticiasPorSalida).forEach(([key, arr]) => {
      if (!Array.isArray(arr) || arr.length === 0) return;
      arr.forEach(noticiaSalida => {
        const titulo = typeof tituloPorSalida[noticiaSalida.id] === 'string' ? tituloPorSalida[noticiaSalida.id] : noticiaSalida.titulo;
        const contenido = typeof contenidoPorSalida[noticiaSalida.id] === 'string' ? contenidoPorSalida[noticiaSalida.id] : noticiaSalida.contenido;
        salidasPublicadas.push({
          salida: key,
          titulo,
          contenido,
          salida_id: noticiaSalida.salida_id
        });
      });
    });
    const faltanTitulos = salidasPublicadas.some(s => !s.titulo || s.titulo.trim().length === 0);
    if (faltanTitulos) {
      setToast({ show: true, message: 'Debes ingresar un título para cada salida antes de publicar.' });
      setLoadingPublicar(false);
      setLoadingPublicar(false);
      return;
    }
    
    let noticiaId;
    // Si la noticia no existe, crearla primero
    if (!noticiaFormData?.id) {
      // Saneamiento de payload para evitar error 422
      const payload = {
        titulo: noticiaFormData.titulo,
        contenido: noticiaFormData.contenido,
        seccion_id: noticiaFormData.seccion_id ? Number(noticiaFormData.seccion_id) : undefined,
        proyecto_id: noticiaFormData.proyecto_id ? Number(noticiaFormData.proyecto_id) : undefined,
        salidas_ids: Array.isArray(noticiaFormData.salidas_ids)
          ? noticiaFormData.salidas_ids.map(Number).filter(n => !isNaN(n))
          : [],
        llm_id: llm_id_final,
        // CORRECCIÓN: incluir session_id en el payload desde noticiaFormData
        session_id: noticiaFormData.session_id || undefined
      };
      // Eliminar campos undefined
      Object.keys(payload).forEach(k => payload[k] === undefined && delete payload[k]);
      const noticia = await api.crearNoticia(payload);
      noticiaId = noticia.id;
      if (noticiaFormData.session_id) {
        console.log('🆔 Incluyendo session_id en publicación:', noticiaFormData.session_id);
      }
    } else {
      noticiaId = noticiaFormData.id;
    }
      // Crear las salidas en el backend
      // Solo enviar los campos esperados por el backend
      const payload = {
        noticia_id: noticiaId,
        salidas_ids: noticiaFormData.salidas_ids,
        llm_id: llm_id_final,
        salidas: salidasPublicadas.map(s => ({
          titulo: s.titulo,
          contenido_generado: s.contenido
        })),
        metricas_valor: metricasCompletas,
        session_id: noticiaFormData.session_id || undefined
      };
      // Eliminar cualquier campo undefined o null
      Object.keys(payload).forEach(k => (payload[k] === undefined) && delete payload[k]);
      // Imprimir en consola y mostrar en alerta el payload
      // eslint-disable-next-line no-console
      console.log('Payload enviado a /api/generar/salidas:', payload);
  // alert('Payload enviado a /api/generar/salidas:\n' + JSON.stringify(payload, null, 2)); // Comentado para evitar popup de debug
      const resp = await generacionService.generarSalidas(payload);
      // Actualizar los títulos/contenidos editados
      if (!resp || !Array.isArray(resp.salidas_generadas)) {
        setToast({ show: true, message: 'Error al publicar: No se generaron salidas en el backend.' });
        throw new Error('No se generaron salidas en el backend');
      }
      let erroresMapeo = [];
      await Promise.all(salidasPublicadas.map(async (s) => {
        // Buscar la salida real por salida_id
        const salidaReal = resp.salidas_generadas.find(sr => sr.salida_id === s.salida_id);
        if (!salidaReal) {
          erroresMapeo.push(s.salida_id);
          return;
        }
        if (s.titulo !== salidaReal.titulo || s.contenido !== salidaReal.contenido_generado) {
          await generacionService.updateSalida(salidaReal.id, {
            titulo: s.titulo,
            contenido_generado: s.contenido
          });
        }
      }));
      if (erroresMapeo.length > 0) {
        // Log detallado para depuración
        // eslint-disable-next-line no-console
        console.error('Error de mapeo de salidas:', {
          salidasPublicadas,
          salidasGeneradas: resp.salidas_generadas,
          erroresMapeo
        });
        setToast({ show: true, message: `Error al publicar: No se encontraron salidas generadas para salida_id(s): ${erroresMapeo.join(', ')}` });
        throw new Error(`No se encontraron salidas generadas para salida_id(s): ${erroresMapeo.join(', ')}`);
      }
      if (onPublicado) onPublicado();
      
      // En modo simplificado, copiar automáticamente al portapapeles
      if (simplifiedMode && tab && noticiasPorSalida[tab] && noticiasPorSalida[tab].length > 0) {
        const noticiaSalida = noticiasPorSalida[tab][0];
        const titulo = typeof tituloPorSalida[noticiaSalida.id] === 'string' ? tituloPorSalida[noticiaSalida.id] : noticiaSalida.titulo;
        const contenido = typeof contenidoPorSalida[noticiaSalida.id] === 'string' ? contenidoPorSalida[noticiaSalida.id] : noticiaSalida.contenido;
        if (titulo && titulo.trim().length > 0 && contenido && contenido.trim().length > 0) {
          const texto = `${titulo}\n\n${contenido}`;
          try {
            await navigator.clipboard.writeText(texto);
            setCopiado(true);
            setTimeout(() => setCopiado(false), 1800);
          } catch (clipboardError) {
            console.warn('No se pudo copiar al portapapeles:', clipboardError);
          }
        }
      }
    } catch (err) {
      console.error("Error al publicar:", err);
      setToast({ show: true, message: 'Error al publicar: ' + (err?.message || 'Error desconocido') });
    } finally {
      setLoadingPublicar(false);
    }
  };

  const handleCopiar = () => {
    if (!(noticiasPorSalida[tab] && noticiasPorSalida[tab].length > 0)) return;
    // Copia solo la primera salida activa (puedes ajustar para copiar todas si lo deseas)
    const noticiaSalida = noticiasPorSalida[tab][0];
    const titulo = typeof tituloPorSalida[noticiaSalida.id] === 'string' ? tituloPorSalida[noticiaSalida.id] : noticiaSalida.titulo;
    const contenido = typeof contenidoPorSalida[noticiaSalida.id] === 'string' ? contenidoPorSalida[noticiaSalida.id] : noticiaSalida.contenido;
    if (!titulo || titulo.trim().length === 0) {
  // alert('Debes ingresar un título para esta salida antes de copiar.'); // Comentado para evitar popup
      return;
    }
    const texto = `${titulo}\n\n${contenido}`;
    navigator.clipboard.writeText(texto).then(() => {
      setCopiado(true);
      setTimeout(() => setCopiado(false), 1800);
    });
  };

  // --- Render principal ---
  return (
  <div className="flex flex-col h-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl dark:shadow-glow-md overflow-hidden" style={{minHeight: '100%'}}>
      <Toast message={toast.message} show={toast.show} onClose={() => setToast({ show: false, message: '' })} />
      {/* Encabezado del panel derecho */}
      <div>
        <div className="bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-700 dark:to-cyan-700 p-6 flex items-center justify-between rounded-t-xl">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-white/20 dark:bg-black/20 rounded-lg backdrop-blur-sm">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Noticias Generadas</h2>
              <p className="text-blue-100 dark:text-cyan-100 text-sm">Visualiza y edita el contenido generado para cada salida seleccionada antes de publicar.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs de salidas generadas */}
      {salidasConNoticias.length > 0 && (
        <div className="flex gap-2 px-6 pt-4">
          {salidasConNoticias.map(salida => (
            <button
              key={salida.key}
              className={`px-4 py-2 rounded-lg font-bold text-sm transition-colors ${tab === salida.key ? 'bg-blue-600 text-white dark:bg-blue-500' : 'bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300'}`}
              onClick={() => setTab(salida.key)}
            >
              {salida.label}
            </button>
          ))}
        </div>
      )}

      {/* Panel de edición de noticias por salida */}
  <div className="flex-1 flex flex-col min-h-0">
        {tab && Array.isArray(noticiasPorSalida[tab]) && noticiasPorSalida[tab].length > 0 ? (
          <div className="flex flex-col gap-4 flex-1 min-h-0 px-6 pt-4 pb-2">
            <h3 className="text-lg font-bold text-blue-700 dark:text-blue-300 mb-2">
              {salidas.find(s => s.key === tab)?.label}
            </h3>
            {noticiasPorSalida[tab].map((noticiaSalida) => (
              <div key={noticiaSalida.id} className="flex flex-col flex-1 h-full">
                <div className="mb-4">
                  <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">Título de la noticia *</label>
                  <input
                    type="text"
                    className={`w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 transition-colors text-xl font-bold ${simplifiedMode ? 'cursor-not-allowed bg-slate-50 dark:bg-slate-800' : 'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'}`}
                    value={typeof tituloPorSalida[noticiaSalida.id] === 'string' ? tituloPorSalida[noticiaSalida.id] : noticiaSalida.titulo}
                    onChange={e => !simplifiedMode && handleTituloChange(noticiaSalida.id, e.target.value)}
                    placeholder="Título de la noticia"
                    maxLength={200}
                    readOnly={simplifiedMode}
                  />
                </div>
                <div className="flex flex-col flex-1">
                  <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">Contenido *</label>
                  <textarea
                    className={`w-full flex-1 px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 resize-none transition-colors ${simplifiedMode ? 'cursor-not-allowed bg-slate-50 dark:bg-slate-800' : 'focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'}`}
                    rows={12}
                    maxLength={2000}
                    value={typeof contenidoPorSalida[noticiaSalida.id] === 'string' ? contenidoPorSalida[noticiaSalida.id] : noticiaSalida.contenido}
                    onChange={e => !simplifiedMode && handleContenidoChange(noticiaSalida.id, e.target.value)}
                    placeholder="Aquí aparecerá el contenido generado para esta salida..."
                    readOnly={simplifiedMode}
                  />
                </div>
              </div>
            ))}
          </div>
        ) : tab ? (
          <div className="flex flex-col gap-4 mb-4 flex-1 min-h-0 px-6 pt-4 pb-2">
            <h3 className="text-lg font-bold text-blue-700 dark:text-blue-300 mb-2">
              {salidas.find(s => s.key === tab)?.label}
            </h3>
            <div className="text-slate-400 dark:text-slate-500 text-sm italic">Sin noticias generadas para esta salida.</div>
          </div>
        ) : null}
      </div>

      {/* Botón de publicación abajo del panel */}
      <div className="px-6 pb-6">
        <div className="flex gap-2 items-center mt-2 relative">
          <button
            className={`${simplifiedMode ? 'w-full' : 'flex-1'} py-3 font-bold rounded-lg flex items-center justify-center gap-2 text-lg transition-all shadow-md dark:shadow-glow-sm ${haySalidaConContenido ? 'bg-blue-600 dark:bg-blue-500 text-white hover:bg-blue-700 dark:hover:bg-blue-600' : 'bg-slate-300 dark:bg-slate-700 text-slate-400 cursor-not-allowed'}`}
            onClick={handlePublicar}
            style={{ marginTop: 'auto' }}
            disabled={!haySalidaConContenido}
          >
            <Send className="w-5 h-5" />
            {simplifiedMode ? 'Publicar y Copiar' : 'Publicar Noticias'}
          </button>
          {!simplifiedMode && (
            <button
              className={`p-3 rounded-lg transition-all shadow-md dark:shadow-glow-sm ${haySalidaConContenido ? 'bg-blue-600 dark:bg-blue-500 text-white hover:bg-blue-700 dark:hover:bg-blue-600' : 'bg-slate-300 dark:bg-slate-700 text-slate-400 cursor-not-allowed'}`}
              onClick={handleCopiar}
              disabled={!(noticiasPorSalida[tab] && noticiasPorSalida[tab][0])}
              title="Copiar al portapapeles"
            >
              <Copy className="w-5 h-5" />
            </button>
          )}
          {copiado && (
            <div className="absolute right-0 top-[-2.5rem] bg-blue-600 text-white text-xs px-3 py-1 rounded shadow-lg animate-fade-in-out z-20">
              ¡Copiado al portapapeles!
            </div>
          )}
        </div>
        
        {/* Métricas de Valor Periodístico - Solo para Admins */}
        <MetricasValor metricas={metricas} />
      </div>
    </div>
  );
}
