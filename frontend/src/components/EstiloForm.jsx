import React, { useEffect, useState } from 'react';
import { TIPOS_ESTILO, estiloService } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import { X, Save } from 'lucide-react';

export default function EstiloForm({ estilo = null, onSave, onCancel }) {
  const { isAdmin, canEdit } = useAuth();
  const [form, setForm] = useState({ nombre: '', descripcion: '', tipo_estilo: '', configuracion: { ejemplo: 'valor' }, activo: true, items: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (estilo) setForm({
      nombre: estilo.nombre || '',
      descripcion: estilo.descripcion || '',
      tipo_estilo: estilo.tipo_estilo || '',
      configuracion: estilo.configuracion || { ejemplo: 'valor' },
      activo: estilo.activo ?? true,
      items: Array.isArray(estilo.items) ? estilo.items.map((item, idx) => ({
        ...item,
        orden: item.orden ?? idx + 1
      })) : []
    });
    else setForm({ nombre: '', descripcion: '', tipo_estilo: '', configuracion: { ejemplo: 'valor' }, activo: true, items: [] });
  }, [estilo]);

  const submit = async () => {
    if (!canEdit() && !isAdmin()) { setError('No autorizado'); return; }
    setLoading(true); setError('');
    try {
      // Validar que configuracion sea objeto no vacío
      if (!form.configuracion || Object.keys(form.configuracion).length === 0) {
        setError('La configuración no puede estar vacía.');
        setLoading(false);
        return;
      }
      const payload = { ...form, items: form.items };
      if (estilo && estilo.id) await estiloService.update(estilo.id, payload);
      else await estiloService.create(payload);
      if (onSave) onSave(true);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Error');
    } finally { setLoading(false); }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/40" onClick={() => onCancel(false)} />
      <div className="relative w-full max-w-2xl bg-white dark:bg-slate-800 rounded-lg shadow-xl flex flex-col h-[90vh] border border-slate-200 dark:border-slate-700">
        {/* Header Fijo */}
        <div className="p-6 border-b border-slate-200 dark:border-slate-700">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100">{estilo ? 'Editar Estilo' : 'Nuevo Estilo'}</h3>
            <button onClick={() => onCancel(false)} className="p-2 rounded hover:bg-slate-100 dark:hover:bg-slate-900">
              <X className="w-5 h-5 text-slate-700 dark:text-slate-300" />
            </button>
          </div>
          {error && <div className="mt-4 text-sm text-red-600">{error}</div>}
        </div>

        {/* Contenido Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <div className="grid grid-cols-1 gap-4">
          <input value={form.nombre} onChange={(e) => setForm({...form, nombre: e.target.value})} placeholder="Nombre" className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900" />
          <select value={form.tipo_estilo} onChange={(e) => setForm({...form, tipo_estilo: e.target.value})} className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900">
            <option value="">-- Tipo de estilo --</option>
            {TIPOS_ESTILO.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
          </select>
          <textarea value={form.descripcion} onChange={(e) => setForm({...form, descripcion: e.target.value})} placeholder="Descripción" rows={2} className="w-full p-2 border-2 rounded-lg bg-white dark:bg-slate-900" />

          <div>
            <label className="block text-sm text-slate-700 dark:text-slate-300 mb-1">Configuración (JSON)</label>
            <textarea
              value={JSON.stringify(form.configuracion, null, 2)}
              onChange={e => {
                const val = e.target.value;
                if (!val.trim()) {
                  setError('La configuración no puede estar vacía.');
                  return;
                }
                try {
                  const parsed = JSON.parse(val);
                  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
                    setError('La configuración debe ser un objeto JSON.');
                  } else {
                    setForm(f => ({ ...f, configuracion: parsed }));
                    setError('');
                  }
                } catch {
                  setError('Configuración debe ser JSON válido.');
                }
              }}
              rows={2}
              className="w-full p-2 border-2 rounded-lg bg-white dark:bg-slate-900"
            />
          </div>

          {/* Gestión de items de estilo - diseño igual a PromptForm */}
          <div className="mb-4">
            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-1">ITEMS</label>
            <div className="bg-white dark:bg-slate-900 border border-green-400 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-slate-700 dark:text-slate-200">ITEMS</span>
                <label className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all flex items-center justify-center cursor-pointer" title="Agregar item">
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                  <input type="file" accept=".txt" multiple style={{ display: 'none' }} onChange={async e => {
                    const files = Array.from(e.target.files);
                    for (const file of files) {
                      try {
                        const text = await file.text();
                        console.log('Archivo leído:', {
                          nombre: file.name,
                          contenido: text.slice(0, 100) + '...' // Log solo los primeros 100 caracteres
                        });
                        
                        setForm(prev => {
                          const newItem = {
                            nombre_archivo: file.name,
                            contenido: text,
                            orden: (prev.items?.length || 0) + 1
                          };
                          console.log('Nuevo item a agregar:', newItem);
                          
                          const updatedItems = [...(prev.items || []), newItem];
                          console.log('Items actualizados:', updatedItems);
                          
                          return {
                            ...prev,
                            items: updatedItems
                          };
                        });
                      } catch (error) {
                        console.error('Error al procesar archivo:', file.name, error);
                        setError(`Error al procesar archivo ${file.name}: ${error.message}`);
                      }
                    }
                    e.target.value = '';
                  }} />
                </label>
              </div>
              <ul className="space-y-2">
                {form.items && form.items.length > 0 ? form.items.map((item, idx) => (
                  <li key={idx} className="flex items-center justify-between py-2 px-3 bg-slate-50 dark:bg-slate-800 rounded shadow-sm border border-slate-200 dark:border-slate-700">
                      <span className="font-mono text-sm text-slate-700 dark:text-slate-200">
                        {item.orden}: {item.nombre_archivo}
                      </span>
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
            <input id="activo_estilo" type="checkbox" checked={form.activo} onChange={(e) => setForm({...form, activo: e.target.checked})} />
            <label htmlFor="activo_estilo" className="text-sm text-slate-700 dark:text-slate-300">Activo</label>
          </div>
          </div>
        </div>

        {/* Botones Fijos Abajo */}
        <div className="p-6 border-t border-slate-200 dark:border-slate-700">
          <div className="flex justify-end gap-3">
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
