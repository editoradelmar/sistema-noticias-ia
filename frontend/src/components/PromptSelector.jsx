import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { promptService } from '../services/maestros';

export default function PromptSelector({ value, onChange, disabled = false }) {
  const { token } = useAuth();
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    promptService.getActivos().then(data => {
      let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
      setPrompts(lista);
    }).finally(() => setLoading(false));
  }, [token]);

  return (
    <div>
      <label className="block mb-1 text-sm text-slate-700 dark:text-slate-300">Prompt Maestro</label>
      <select
        value={value || ''}
        onChange={e => onChange(e.target.value ? Number(e.target.value) : null)}
        className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900"
        disabled={disabled || !token || loading}
      >
        <option value="">{loading ? 'Cargando prompts...' : 'Sin asignar'}</option>
        {prompts.map(p => (
          <option key={p.id} value={p.id}>{p.nombre}</option>
        ))}
      </select>
    </div>
  );
}
