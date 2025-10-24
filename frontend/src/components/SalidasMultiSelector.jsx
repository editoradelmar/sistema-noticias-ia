import React, { useEffect, useState } from 'react';
import { salidaService } from '../services/maestros';

export default function SalidasMultiSelector({ salidasIds = [], onChange, disabled = false }) {
  const [salidas, setSalidas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSalidas() {
      setLoading(true);
      try {
        const data = await salidaService.getAll({ activo: true });
        setSalidas(data || []);
      } catch (err) {
        setSalidas([]);
      } finally {
        setLoading(false);
      }
    }
    fetchSalidas();
  }, []);

  const handleChange = e => {
    const selected = Array.from(e.target.selectedOptions, opt => Number(opt.value));
    onChange(selected);
  };

  return (
    <div>
      <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
        Salidas asociadas (puedes elegir varias)
      </label>
      <select
        multiple
        value={salidasIds}
        onChange={handleChange}
        disabled={disabled || loading}
        className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-colors h-40"
      >
        {salidas.map(salida => (
          <option key={salida.id} value={salida.id}>
            {salida.nombre} ({salida.tipo_salida})
          </option>
        ))}
      </select>
      <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
        Mantén presionada Ctrl (Windows) o Cmd (Mac) para seleccionar varias opciones.
      </p>
    </div>
  );
}
