import React, { useEffect, useState } from 'react';

// Defaults centralizados por variable de entorno
const DEFAULT_LLM_PROVEEDOR = import.meta.env.VITE_DEFAULT_LLM_PROVEEDOR || 'Google';
const DEFAULT_LLM_MODELO_ID = import.meta.env.VITE_DEFAULT_LLM_MODELO_ID || '';
import { useAuth } from '../context/AuthContext';
import { llmService } from '../services/maestros';

export default function LLMSelector({ value, onChange, disabled = false }) {
  const { token } = useAuth();
  const [llms, setLlms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    llmService.getActivos().then(data => {
      let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
      setLlms(lista);
    }).finally(() => setLoading(false));
  }, [token]);

  // Determinar el valor por defecto si no se pasa value

  let defaultId = '';
  if (!value && llms.length > 0) {
    // Prioridad: modelo_id exacto, luego proveedor
    const byModelo = DEFAULT_LLM_MODELO_ID ? llms.find(l => String(l.modelo_id) === String(DEFAULT_LLM_MODELO_ID)) : null;
    const byProveedor = llms.find(l => String(l.proveedor) === String(DEFAULT_LLM_PROVEEDOR));
    defaultId = byModelo?.id ? String(byModelo.id) : (byProveedor?.id ? String(byProveedor.id) : String(llms[0].id));
  }

  return (
    <select
      value={value || defaultId || ''}
      onChange={e => onChange(e.target.value ? String(e.target.value) : '')}
      className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900"
      disabled={disabled || !token || loading}
    >
      <option value="">{loading ? 'Cargando modelos...' : 'Sin asignar'}</option>
      {llms.map(l => (
        <option key={l.id} value={String(l.id)}>{l.nombre}</option>
      ))}
    </select>
  );
}
