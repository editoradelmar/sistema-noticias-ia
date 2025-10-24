
import React, { useEffect, useState } from 'react';
import { seccionService } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import { X, Save } from 'lucide-react';
import PromptSelector from './PromptSelector';
import EstiloSelector from './EstiloSelector';

export default function SeccionForm({ seccion = null, onSave, onCancel, isOpen = true }) {
  const { token, isAdmin, canEdit } = useAuth();
  const [form, setForm] = useState({ nombre: '', descripcion: '', color: '#2563eb', icono: '', prompt_id: null, estilo_id: null, activo: true });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  // Ya no se usan prompts/estilos locales, se delega a los componentes selector

  useEffect(() => {
    if (seccion) setForm({
      nombre: seccion.nombre || '',
      descripcion: seccion.descripcion || '',
      color: seccion.color || '#2563eb',
      icono: seccion.icono || '',
      prompt_id: seccion.prompt_id || null,
      estilo_id: seccion.estilo_id || null,
      activo: seccion.activo ?? true
    });
    else setForm({ nombre: '', descripcion: '', color: '#2563eb', icono: '', prompt_id: null, estilo_id: null, activo: true });
  }, [seccion]);

  // Eliminado: la carga de prompts/estilos ahora es responsabilidad de los componentes selector

  const submit = async () => {
    if (!canEdit() && !isAdmin()) { setError('No autorizado'); return; }
    setLoading(true); setError('');
    try {
      if (seccion && seccion.id) await seccionService.update(seccion.id, form);
      else await seccionService.create(form);
      if (onSave) onSave(true);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Error');
    } finally { setLoading(false); }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/40" onClick={() => onCancel(false)} />
      <div className="relative w-full max-w-2xl bg-white dark:bg-slate-800 rounded-lg shadow-xl p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100">{seccion ? 'Editar Sección' : 'Nueva Sección'}</h3>
          <button onClick={() => onCancel(false)} className="p-2 rounded hover:bg-slate-100 dark:hover:bg-slate-900"><X className="w-5 h-5 text-slate-700 dark:text-slate-300" /></button>
        </div>

        {!token && (
          <div className="mb-4 text-sm text-red-600">Debe iniciar sesión para visualizar y asociar Prompts y Estilos.</div>
        )}

  {error && <div className="mb-4 text-sm text-red-600">{error}</div>}

        <div className="grid grid-cols-1 gap-4">
          <input value={form.nombre} onChange={(e) => setForm({...form, nombre: e.target.value})} placeholder="Nombre de la sección" className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900" />
          <input value={form.icono} onChange={(e) => setForm({...form, icono: e.target.value})} placeholder="Icono (emoji o texto)" className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900" />
          <input type="color" value={form.color} onChange={(e) => setForm({...form, color: e.target.value})} className="w-24 h-10 p-1 border-2 rounded-lg" />
          <textarea value={form.descripcion} onChange={(e) => setForm({...form, descripcion: e.target.value})} placeholder="Descripción de la sección" rows={3} className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900" />

          {/* Selector de Prompt */}
          <PromptSelector
            value={form.prompt_id}
            onChange={id => setForm({ ...form, prompt_id: id })}
            disabled={!token}
          />

          {/* Selector de Estilo */}
          <EstiloSelector
            value={form.estilo_id}
            onChange={id => setForm({ ...form, estilo_id: id })}
            disabled={!token}
          />

          <div className="flex items-center gap-3">
            <input id="activo_seccion" type="checkbox" checked={form.activo} onChange={(e) => setForm({...form, activo: e.target.checked})} />
            <label htmlFor="activo_seccion" className="text-sm text-slate-700 dark:text-slate-300">Sección activa</label>
          </div>

          <div className="flex justify-end gap-3 mt-2">
            <button onClick={() => onCancel(false)} className="px-4 py-2 bg-slate-100 dark:bg-slate-900 rounded-lg">Cancelar</button>
            <button onClick={submit} disabled={loading} className="flex items-center gap-2 px-4 py-2 bg-emerald-600 dark:bg-emerald-500 text-white rounded-lg">
              <Save className="w-4 h-4" /> {loading ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
