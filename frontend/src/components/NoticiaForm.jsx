
import React, { useState, useEffect, useCallback } from 'react';
import { Save, FileText, AlertCircle, X, Upload, File, Check } from 'lucide-react';
import { api } from '../services/api';
import { seccionService } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import ProyectoSelector from './ProyectoSelector';
import SalidasCheckboxGroup from './SalidasCheckboxGroup';
import LLMSelector from './LLMSelector';


export default function NoticiaForm({ noticia, loading, onClose, onGenerarNoticias, extraFields }) {
  // Maneja el cambio del selector de LLM
  const handleLLMChange = llmId => {
    setForm(f => ({ ...f, llm_id: llmId }));
  };
  const { token } = useAuth();
  const [form, setForm] = useState({
    titulo: '',
    contenido: '',
    seccion_id: '',
    proyecto_id: null,
    salidas_ids: [],
    llm_id: ''
  });

  // Hook de secciones: SIEMPRE debe estar al inicio del componente
  const [secciones, setSecciones] = useState([]);
  useEffect(() => {
    async function fetchSecciones() {
      const data = await seccionService.getAll({ activo: true });
      let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
      setSecciones(lista);
    }
    fetchSecciones();
  }, []);

  useEffect(() => {
    if (noticia) {
      setForm({
        titulo: noticia.titulo || '',
        contenido: noticia.contenido || '',
        seccion_id: noticia.seccion_id || '',
        proyecto_id: noticia.proyecto_id || null,
        salidas_ids: noticia.salidas_ids || [],
        llm_id: noticia.llm_id || ''
      });
    }
  }, [noticia]);
  const [error, setError] = useState('');

  // Estados para drag & drop y upload de archivos
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  const handleCancel = () => {
    if (form.titulo || form.contenido) {
      if (window.confirm('¿Descartar los cambios?')) {
        onClose(false);
      }
    } else {
      onClose(false);
    }
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    if (!form.titulo || form.titulo.trim().length < 5) {
      setError('El título debe tener al menos 5 caracteres');
      return;
    }
    if (!form.contenido || form.contenido.trim().length < 20) {
      setError('El contenido debe tener al menos 20 caracteres');
      return;
    }
    if (form.contenido.trim().length > 10000) {
      setError('El contenido no puede exceder 10,000 caracteres');
      return;
    }
    if (!form.seccion_id) {
      setError('La sección es obligatoria');
      return;
    }
    try {
      // Si es edición, sí persiste
      if (noticia && noticia.id) {
  const { titulo, contenido, seccion_id, proyecto_id, salidas_ids } = form;
  const payload = { titulo, contenido, seccion_id, proyecto_id, salidas_ids };
  await api.actualizarNoticia(noticia.id, payload, token);
        if (onClose) onClose(true);
      } else {
        // Solo genera las salidas, no persiste la noticia
        if (onGenerarNoticias) {
          onGenerarNoticias(form, form.salidas_ids);
        }
      }
    } catch (err) {
      setError(noticia ? 'Error al actualizar noticia' : 'Error al crear noticia');
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md overflow-hidden border border-slate-200 dark:border-slate-700">
        {/* Header estilo proyectos */}
        <div className="bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-700 dark:to-cyan-700 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 dark:bg-black/20 rounded-lg backdrop-blur-sm">
                <FileText className="w-8 h-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">
                  {noticia && noticia.id ? 'Editar Noticia' : 'Crear Noticia'}
                </h2>
                <p className="text-blue-100 dark:text-cyan-100 text-sm">
                  {noticia && noticia.id
                    ? 'Edita los datos de la noticia y su canal de salida.'
                    : 'Publica una noticia para el sistema, vinculada a un proyecto y salida si lo deseas'}
                </p>
              </div>
            </div>
            <button
              onClick={handleCancel}
              className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-all"
            >
              <X className="w-6 h-6 text-white" />
            </button>
          </div>
        </div>

        {/* Formulario */}
  <form onSubmit={handleSubmit} className="p-8 space-y-6">
          {/*
          Bloque de error visual completamente comentado por solicitud:
          {error && (
            <div className="flex items-start gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}
          */}

          {/* Título */}
          <div>
            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
              Título de la noticia *
            </label>
            <input
              name="titulo"
              value={form.titulo}
              onChange={handleChange}
              required
              maxLength={200}
              placeholder="Ej: PostgreSQL 16 trae mejoras significativas"
              className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-colors"
            />
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Mínimo 3 caracteres, máximo 200
            </p>
          </div>

          {/* Contenido */}
          <div>
            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
              Contenido *
            </label>
            <textarea
              name="contenido"
              value={form.contenido}
              onChange={handleChange}
              required
              rows={8}
              maxLength={10000}
              placeholder="Escriba el cuerpo de la noticia..."
              className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 resize-none transition-colors"
            />
            <div className="flex justify-between items-center mt-1">
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Mínimo 20 caracteres, máximo 10,000
              </p>
              <p className={`text-xs font-mono ${
                form.contenido.length > 10000 
                  ? 'text-red-500 dark:text-red-400' 
                  : form.contenido.length > 8500 
                    ? 'text-orange-500 dark:text-orange-400'
                    : 'text-slate-500 dark:text-slate-400'
              }`}>
                {form.contenido.length.toLocaleString()}/10,000
              </p>
            </div>
          </div>

          {/* Sección */}
          <div>
            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
              Sección *
            </label>
            <select
              name="seccion_id"
              value={form.seccion_id}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-colors"
            >
              <option value="">Selecciona una sección</option>
              {secciones.map(sec => (
                <option key={sec.id} value={sec.id}>{sec.nombre}</option>
              ))}
            </select>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Selecciona la sección a la que pertenece la noticia
            </p>
          </div>

          {/* Proyecto (opcional) */}
          <div>
            <ProyectoSelector proyectoId={form.proyecto_id} onChange={id => setForm(f => ({ ...f, proyecto_id: id }))} />
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Puedes asociar la noticia a un proyecto existente
            </p>
          </div>

          {/* Salidas (opcional, múltiple) */}
          <div>
            <SalidasCheckboxGroup
              salidasIds={form.salidas_ids}
              onChange={ids => setForm(f => ({ ...f, salidas_ids: ids }))}
            />
          </div>

          {/* Selector de LLM ÚNICO */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
              Modelo de IA (LLM) *
            </label>
            <LLMSelector
              value={form.llm_id}
              onChange={handleLLMChange}
              disabled={loading}
            />
          </div>

          {/* Autor eliminado, el backend lo toma del usuario autenticado */}

          {/* Botones */}
          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={handleCancel}
              className="flex-1 px-6 py-3 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 font-semibold rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all border border-slate-300 dark:border-slate-700"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed shadow-md dark:shadow-glow-sm transition-all"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Generando...
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  Generar Noticias
                </>
              )}
            </button>
          </div>
        </form>

        {/* Info adicional */}
        <div className="bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-700 p-6">
          <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">
            💡 Consejos:
          </h3>
          <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <li className="flex items-start gap-2">
              <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
              <span>Usa títulos descriptivos y claros</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
              <span>El contenido debe ser relevante y bien redactado</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
              <span>Asocia la noticia a un proyecto para mejor organización</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
