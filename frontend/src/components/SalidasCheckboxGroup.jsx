import React, { useEffect, useState } from 'react';
import { salidaService } from '../services/maestros';

export default function SalidasCheckboxGroup({ salidasIds = [], onChange, disabled = false }) {
  const [salidas, setSalidas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSalidas() {
      setLoading(true);
      try {
        const data = await salidaService.getAll({ activo: true });
  let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
  setSalidas(lista);
      } catch (err) {
        setSalidas([]);
      } finally {
        setLoading(false);
      }
    }
    fetchSalidas();
  }, []);

  const handleCheck = (id) => {
    if (salidasIds.includes(id)) {
      onChange(salidasIds.filter(sid => sid !== id));
    } else {
      onChange([...salidasIds, id]);
    }
  };

  return (
    <div>
      <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
        Salidas asociadas (puedes elegir varias)
      </label>
      <div className="flex flex-col gap-2">
        {salidas.map(salida => (
          <label key={salida.id} className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={salidasIds.includes(salida.id)}
              onChange={() => handleCheck(salida.id)}
              disabled={disabled || loading}
              className="accent-blue-600 w-4 h-4"
            />
            <span className="text-slate-800 dark:text-slate-100">
              {salida.nombre} <span className="text-xs text-slate-500">({salida.tipo_salida})</span>
            </span>
          </label>
        ))}
      </div>
      <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
        Marca los canales donde se publicará/generará la noticia.
      </p>
    </div>
  );
}
