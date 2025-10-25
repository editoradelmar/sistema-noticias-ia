import React, { useState } from 'react';
import { salidaService, TIPOS_SALIDA } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import { X, Save } from 'lucide-react';

const SalidaForm = ({ salida, onSave, onCancel }) => {
  const [form, setForm] = useState(salida || { nombre: '', descripcion: '', tipo_salida: '', activo: true });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(f => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async e => {
    if (e) e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const payload = { ...form, configuracion: form.configuracion || {} };
      if (salida && salida.id) {
        await salidaService.update(salida.id, payload);
      } else {
        await salidaService.create(payload);
      }
      onSave(true);
    } catch (err) {
      setError(err?.message || 'Error al guardar');
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
            <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100">
              {salida ? 'Editar Salida' : 'Nueva Salida'}
            </h3>
            <button 
              type="button" 
              onClick={() => onCancel(false)} 
              className="p-2 rounded hover:bg-slate-100 dark:hover:bg-slate-900"
            >
              <X className="w-5 h-5 text-slate-700 dark:text-slate-300" />
            </button>
          </div>
          {error && <div className="mt-4 text-sm text-red-600">{error}</div>}
        </div>

        {/* Contenido Scrollable */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label htmlFor="nombre" className="block mb-1 font-medium text-slate-700 dark:text-slate-300">
                Nombre
              </label>
              <input
                id="nombre"
                name="nombre"
                value={form.nombre}
                onChange={handleChange}
                required
                className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
              />
            </div>

            <div>
              <label htmlFor="descripcion" className="block mb-1 font-medium text-slate-700 dark:text-slate-300">
                Descripción
              </label>
              <textarea
                id="descripcion"
                name="descripcion"
                value={form.descripcion}
                onChange={handleChange}
                rows={3}
                className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
              />
            </div>

            <div>
              <label htmlFor="tipo_salida" className="block mb-1 font-medium text-slate-700 dark:text-slate-300">
                Tipo de salida
              </label>
              <select
                id="tipo_salida"
                name="tipo_salida"
                value={form.tipo_salida}
                onChange={handleChange}
                required
                className="w-full p-3 border-2 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100"
              >
                <option value="">Selecciona un tipo...</option>
                {TIPOS_SALIDA.map(t => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="activo"
                name="activo"
                checked={form.activo}
                onChange={handleChange}
                className="rounded border-slate-300 dark:border-slate-600"
              />
              <label htmlFor="activo" className="text-sm text-slate-700 dark:text-slate-300">
                Activo
              </label>
            </div>
          </div>
        </div>

        {/* Botones Fijos Abajo */}
        <div className="p-6 border-t border-slate-200 dark:border-slate-700">
          <div className="flex justify-end gap-3">
            <button
              type="button"
              onClick={() => onCancel(false)}
              className="px-4 py-2 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800"
            >
              Cancelar
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-emerald-600 dark:bg-emerald-500 text-white rounded-lg hover:bg-emerald-700 dark:hover:bg-emerald-600 disabled:opacity-60"
            >
              <Save className="w-4 h-4" />
              {loading ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SalidaForm;