import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { estiloService } from '../services/maestros';

export default function EstiloSelector({ value, onChange, disabled = false }) {
  const { token } = useAuth();
  const [estilos, setEstilos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    estiloService.getActivos().then(data => {
      let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
      setEstilos(lista);
    }).finally(() => setLoading(false));
  }, [token]);

  return (
    <div>
      <label className="block mb-1 text-sm text-slate-700 dark:text-slate-300">Estilo Maestro</label>
      <select
        value={value || ''}
        onChange={e => onChange(e.target.value ? Number(e.target.value) : null)}
        className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900"
        disabled={disabled || !token || loading}
      >
        <option value="">{loading ? 'Cargando estilos...' : 'Sin asignar'}</option>
        {estilos.map(e => (
          <option key={e.id} value={e.id}>{e.nombre}</option>
        ))}
      </select>
    </div>
  );
}
