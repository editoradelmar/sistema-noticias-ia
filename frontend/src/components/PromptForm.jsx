import React, { useState, useEffect } from 'react';
import { promptService } from '../services/maestros';
import { promptItemService } from '../services/promptItemService';
import { useAuth } from '../context/AuthContext';
import { X, Save } from 'lucide-react';

export default function PromptForm({ prompt = null, onSave, onCancel }) {
  const { isAdmin, canEdit } = useAuth();
  const [form, setForm] = useState({ nombre: '', descripcion: '', contenido: '', variables: [], activo: true, items: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchItems() {
      if (prompt && prompt.id) {
        const items = await promptItemService.getByPrompt(prompt.id);
        setForm({
          nombre: prompt.nombre || '',
          descripcion: prompt.descripcion || '',
          contenido: prompt.contenido || '',
          variables: (prompt.variables && Array.isArray(prompt.variables)) ? prompt.variables : [],
          activo: prompt.activo ?? true,
          items: Array.isArray(items) ? items.map((item, idx) => ({
            ...item,
            orden: item.orden ?? idx + 1
          })) : []
        });
      } else {
        setForm({ nombre: '', descripcion: '', contenido: '', variables: [], activo: true, items: [] });
      }
    }
    fetchItems();
  }, [prompt]);

  const handleChange = (key) => (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setForm((s) => ({ ...s, [key]: value }));
  };

  const handleVariablesChange = (e) => {
    const raw = e.target.value;
    const arr = raw.split(',').map(s => s.trim()).filter(Boolean);
    setForm((s) => ({ ...s, variables: arr }));
  };

  const submit = async () => {
    if (!canEdit() && !isAdmin()) {
      setError('No tienes permisos para realizar esta acción.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      // Limpiar items: solo enviar los campos relevantes
      const cleanItems = (form.items || []).map(item => ({
        nombre_archivo: item.nombre_archivo,
        contenido: item.contenido,
        orden: item.orden
      }));
      const payload = { ...form, items: cleanItems };
      console.log('Payload enviado:', payload);
      let result;
      if (prompt && prompt.id) {
        result = await promptService.update(prompt.id, payload);
      } else {
        result = await promptService.create(payload);
      }
      if (result) {
        if (onSave) {
          // Llamar a onSave con el resultado y cerrar el formulario
          onSave(result);
          onCancel(false); // Esto cerrará el formulario
        }
      }
    } catch (err) {
      const message = err.response?.data?.detail || err.message || 'Error desconocido';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/40" onClick={() => onCancel(false)} />
      <div className="relative w-full max-w-2xl bg-white dark:bg-slate-800 rounded-lg shadow-xl flex flex-col h-[90vh] border border-slate-200 dark:border-slate-700">
        {/* Header Fijo */}
        <div className="p-6 border-b border-slate-200 dark:border-slate-700">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100">{prompt ? 'Editar Prompt' : 'Nuevo Prompt'}</h3>
            <button onClick={() => onCancel(false)} className="p-2 rounded hover:bg-slate-100 dark:hover:bg-slate-900">
              <X className="w-5 h-5 text-slate-700 dark:text-slate-300" />
            </button>
          </div>
          {error && <div className="mt-4 text-sm text-red-600">{error}</div>}
        </div>

        {/* Contenido Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <div className="grid grid-cols-1 gap-4">
          <input type="text" placeholder="Nombre" value={form.nombre} onChange={(e) => setForm({...form, nombre: e.target.value})} className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100" />

          {/* Campo de categoría eliminado */}

          <textarea placeholder="Descripción" value={form.descripcion} onChange={(e) => setForm({...form, descripcion: e.target.value})} className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100" rows={4} />

          {/* Gestión de items tipo texto para prompts */}
          <div className="mb-8">
            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">ITEMS</label>
            <div className="bg-white dark:bg-slate-900 border border-green-400 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-slate-700 dark:text-slate-200">ITEMS</span>
                <label
                  className="p-2 bg-blue-600 text-white rounded-lg flex items-center justify-center transition-all hover:bg-blue-700 cursor-pointer"
                  title="Agregar item"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                  <input
                    type="file"
                    accept=".txt"
                    multiple
                    style={{ display: 'none' }}
                    onChange={async e => {
                      const files = Array.from(e.target.files);
                      for (const file of files) {
                        const text = await file.text();
                        const newItem = {
                          nombre_archivo: file.name,
                          contenido: text,
                          orden: (form.items?.length || 0) + 1
                        };
                        setForm(prev => ({
                          ...prev,
                          items: [...(prev.items || []), newItem]
                        }));
                      }
                      e.target.value = '';
                    }}
                  />
                </label>
              </div>
              <ul className="space-y-2">
                {form.items && form.items.length > 0 ? form.items.map((item, idx) => (
                  <li key={idx} className="flex items-center justify-between py-2 px-3 bg-slate-50 dark:bg-slate-800 rounded shadow-sm border border-slate-200 dark:border-slate-700">
                    <span className="font-mono text-sm text-slate-700 dark:text-slate-200">{item.orden}: {item.nombre_archivo}</span>
                    <button type="button" onClick={() => {
                      setForm(prev => ({
                        ...prev,
                        items: prev.items.filter((_, i) => i !== idx)
                      }));
                    }} className="p-2 text-blue-600 hover:text-white bg-blue-100 dark:bg-blue-900/20 rounded-lg hover:bg-blue-600 transition-all" title="Eliminar item">
                      <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3" /></svg>
                    </button>
                  </li>
                )) : (
                  <li className="text-slate-400 italic">No hay items aún.</li>
                )}
              </ul>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <input id="activo" type="checkbox" checked={form.activo} onChange={(e) => setForm({...form, activo: e.target.checked})} />
            <label htmlFor="activo" className="text-sm text-slate-700 dark:text-slate-300">Activo</label>
          </div>

          </div>
        </div>

        {/* Botones Fijos Abajo */}
        <div className="p-6 border-t border-slate-200 dark:border-slate-700">
          <div className="flex justify-end gap-3">
            <button onClick={() => onCancel(false)} className="px-4 py-2 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg">Cancelar</button>
            <button onClick={submit} disabled={loading} className="flex items-center gap-2 px-4 py-2 bg-emerald-600 dark:bg-emerald-500 text-white rounded-lg">
              <Save className="w-4 h-4" />
              {loading ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
