import { useState } from 'react';
import { salidaService } from '../services/maestros';
import { TIPOS_SALIDA } from '../services/tipos_salida';

const SalidaForm = ({ salida, onSave, onCancel }) => {
  const [form, setForm] = useState(salida || { nombre: '', descripcion: '', tipo_salida: '', activo: true });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(f => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-8 w-full max-w-md border border-slate-200 dark:border-slate-700">
        <h2 className="text-2xl font-bold mb-4 text-slate-900 dark:text-slate-100">{salida ? 'Editar Salida' : 'Nueva Salida'}</h2>
        {error && <div className="mb-3 text-red-600">{error}</div>}
        <div className="mb-4">
          <label className="block mb-1 font-medium">Nombre</label>
          <input name="nombre" value={form.nombre} onChange={handleChange} required className="w-full px-4 py-2 rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900" />
        </div>
        <div className="mb-4">
          <label className="block mb-1 font-medium">Descripción</label>
          <textarea name="descripcion" value={form.descripcion} onChange={handleChange} rows={2} className="w-full px-4 py-2 rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900" />
        </div>
        <div className="mb-4">
          <label className="block mb-1 font-medium">Tipo de salida</label>
          <select name="tipo_salida" value={form.tipo_salida} onChange={handleChange} required className="w-full px-4 py-2 rounded border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900">
            <option value="">Selecciona un tipo...</option>
            {TIPOS_SALIDA.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
          </select>
        </div>
        <div className="flex items-center mb-6">
          <input type="checkbox" name="activo" checked={form.activo} onChange={handleChange} id="activo" className="mr-2" />
          <label htmlFor="activo" className="text-sm">Activo</label>
        </div>
        <div className="flex justify-end gap-3">
          <button type="button" onClick={() => onCancel(false)} className="px-4 py-2 rounded bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-300 dark:hover:bg-slate-600">Cancelar</button>
          <button type="submit" disabled={loading} className="px-4 py-2 rounded bg-emerald-600 dark:bg-emerald-500 text-white font-semibold hover:bg-emerald-700 dark:hover:bg-emerald-600 disabled:opacity-60">
            {loading ? 'Guardando...' : 'Guardar'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SalidaForm;
