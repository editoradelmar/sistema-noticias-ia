import React, { useState, useEffect } from 'react';
import { Layers, ChevronDown } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { seccionService } from '../services/maestros';

export default function SeccionSelector({ seccionId, onChange, disabled = false }) {
  const { isDark } = useTheme();
  const [secciones, setSecciones] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarSecciones();
  }, []);

  const cargarSecciones = async () => {
    setLoading(true);
    try {
      const data = await seccionService.getActivas();
      setSecciones(data);
    } catch (error) {
      console.error('Error al cargar secciones:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
        Sección
      </label>
      <div className="relative">
        <Layers className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5" />
        <select
          value={seccionId || ''}
          onChange={e => onChange(e.target.value ? parseInt(e.target.value) : null)}
          disabled={disabled || loading}
          className="w-full pl-11 pr-10 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed appearance-none transition-colors"
        >
          <option value="">
            {loading ? 'Cargando secciones...' : 'Seleccione una sección'}
          </option>
          {secciones.map(seccion => (
            <option key={seccion.id} value={seccion.id}>
              {seccion.nombre}
            </option>
          ))}
        </select>
        <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5 pointer-events-none" />
      </div>
    </div>
  );
}
