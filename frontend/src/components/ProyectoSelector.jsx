import React, { useState, useEffect } from 'react';
import { Folder, ChevronDown, X } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';

export default function ProyectoSelector({ 
  proyectoId, 
  onChange, 
  disabled = false 
}) {
  const { isDark } = useTheme();
  const { token } = useAuth();
  const [proyectos, setProyectos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      cargarProyectos();
    }
  }, [token]);

  const cargarProyectos = async () => {
    setLoading(true);
    try {
  const data = await api.getProyectos('activo', token);
  let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
  setProyectos(lista);
    } catch (error) {
      console.error('Error al cargar proyectos:', error);
    } finally {
      setLoading(false);
    }
  };

  const proyectoSeleccionado = proyectos.find(p => p.id === proyectoId);

  return (
    <div>
      <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
        Proyecto (Opcional)
      </label>
      
      <div className="relative">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <Folder className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5" />
            <select
              value={proyectoId || ''}
              onChange={(e) => onChange(e.target.value ? parseInt(e.target.value) : null)}
              disabled={disabled || loading}
              className="w-full pl-11 pr-10 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed appearance-none transition-colors"
            >
              <option value="">
                {loading ? 'Cargando proyectos...' : 'Sin proyecto (noticia independiente)'}
              </option>
              {proyectos.map((proyecto) => (
                <option key={proyecto.id} value={proyecto.id}>
                  {proyecto.nombre}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5 pointer-events-none" />
          </div>

          {proyectoId && (
            <button
              type="button"
              onClick={() => onChange(null)}
              disabled={disabled}
              className="px-3 py-3 bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              title="Quitar proyecto"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Proyecto seleccionado info */}
      {proyectoSeleccionado && (
        <div className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
          <div className="flex items-start gap-2">
            <Folder className="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-blue-900 dark:text-blue-100 truncate">
                {proyectoSeleccionado.nombre}
              </p>
              {proyectoSeleccionado.descripcion && (
                <p className="text-xs text-blue-700 dark:text-blue-300 mt-1 line-clamp-2">
                  {proyectoSeleccionado.descripcion}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Ayuda */}
      {!proyectoId && proyectos.length > 0 && (
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
          Vincula esta noticia a un proyecto para organizarla mejor
        </p>
      )}

      {proyectos.length === 0 && !loading && (
        <p className="text-xs text-amber-600 dark:text-amber-400 mt-2 flex items-center gap-1">
          <span>⚠️</span>
          No hay proyectos activos. Crea uno desde la sección de Proyectos.
        </p>
      )}
    </div>
  );
}
