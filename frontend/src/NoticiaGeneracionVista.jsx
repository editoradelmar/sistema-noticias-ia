

import React, { useState, useEffect } from "react";
import NoticiaForm from "./components/NoticiaForm";
import NoticiasGeneradasPanel from "./components/NoticiasGeneradasPanel";

import generacionService from "./services/generacion";
import { salidaService, llmService } from "./services/maestros";



import { api } from "./services/api";

function NoticiaGeneracionVista({ noticiaId: noticiaIdProp, onVolverLista }) {
  const [noticiasPorSalida, setNoticiasPorSalida] = useState({
    impreso: [],
    web: [],
    twitter: [],
    instagram: [],
    facebook: [],
  });
  const [noticiaId, setNoticiaId] = useState(noticiaIdProp || null);
  const [noticiaFormData, setNoticiaFormData] = useState(null);
  const [loadingSalidas, setLoadingSalidas] = useState(false);
  const [salidasMaestro, setSalidasMaestro] = useState([]);
  const [llms, setLlms] = useState([]);
  // El llmId real debe sincronizarse con el form y el selector
  const [llmId, setLlmId] = useState("");

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
        if (lista && lista.length > 0) setLlmId(lista[0].id);
      } catch {
        setLlms([]);
      }
    }
    fetchLlms();
  }, []);

  // Handler para cuando se genera una noticia y sus salidas (creación o edición)
  const handleGenerarNoticias = async (form, salidas_ids) => {
    // Sincroniza llmId con el form
    const llm_id_final = form.llm_id || llmId;
    if (noticiaId) {
      setNoticiaFormData({ ...form, salidas_ids, llm_id: llm_id_final });
    } else {
      setNoticiaId(null);
      setNoticiaFormData({ ...form, salidas_ids, llm_id: llm_id_final });
    }
    try {
      if (!llm_id_final) {
        alert("Debes seleccionar un modelo de IA (LLM)");
        return;
      }
      const agrupadas = {
        impreso: [],
        web: [],
        twitter: [],
        instagram: [],
        facebook: []
      };
      for (const salida of salidasMaestro) {
        let clave = salida.nombre.trim().toLowerCase();
        if (clave.includes("impreso")) clave = "impreso";
        else if (clave.includes("web")) clave = "web";
        else if (clave.includes("twitter")) clave = "twitter";
        else if (clave.includes("instagram")) clave = "instagram";
        else if (clave.includes("facebook")) clave = "facebook";
        if (salidas_ids.includes(salida.id) && agrupadas[clave]) {
          agrupadas[clave].push({
            id: Math.random().toString(36).substr(2, 9),
            titulo: form.titulo,
            contenido: form.contenido,
            salida_id: salida.id
          });
        }
      }
      setNoticiasPorSalida(agrupadas);
    } catch (err) {
      alert("Error generando salidas: " + err.message);
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
                {llms.map(llm => (
                  <option key={llm.id} value={llm.id}>{llm.nombre} ({llm.proveedor})</option>
                ))}
              </select>
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
          onPublicado={() => { if (onVolverLista) onVolverLista(); }}
        />
      </div>
    </div>
  );
}

export default NoticiaGeneracionVista;
