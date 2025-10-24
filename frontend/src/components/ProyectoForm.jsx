import React, { useState, useEffect } from 'react';
import { X, Save, Folder, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { api } from '../services/api';

export default function ProyectoForm({ proyecto, onClose }) {
  const { token } = useAuth();
  const { isDark } = useTheme();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    nombre: '',
    descripcion: '',
    estado: 'activo'
  });

  useEffect(() => {
    if (proyecto) {
      setForm({
        nombre: proyecto.nombre || '',
        descripcion: proyecto.descripcion || '',
        estado: proyecto.estado || 'activo'
      });
    }
  }, [proyecto]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validaciones
    if (form.nombre.trim().length < 3) {
      setError('El nombre debe tener al menos 3 caracteres');
      return;
    }

    setLoading(true);
    setError('');

    try {
      if (proyecto) {
        // Actualizar proyecto existente
        await api.actualizarProyecto(proyecto.id, form, token);
      } else {
        // Crear nuevo proyecto
        await api.crearProyecto(form, token);
      }
      onClose(true); // true indica que hubo cambios
    } catch (err) {
      setError(err.message || 'Error al guardar el proyecto');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (form.nombre || form.descripcion) {
      if (confirm('¿Descartar los cambios?')) {
        onClose(false);
      }
    } else {
      onClose(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md overflow-hidden border border-slate-200 dark:border-slate-700">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-700 dark:to-cyan-700 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 dark:bg-black/20 rounded-lg backdrop-blur-sm">
                <Folder className="w-8 h-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">
                  {proyecto ? 'Editar Proyecto' : 'Nuevo Proyecto'}
                </h2>
                <p className="text-blue-100 dark:text-cyan-100 text-sm">
                  {proyecto ? 'Actualiza la información del proyecto' : 'Crea un nuevo proyecto para organizar tus noticias'}
                </p>
              </div>
            </div>
            <button
              onClick={handleCancel}
              className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-all"
            >
              <X className="w-6 h-6 text-white" />
            </button>
          </div>
        </div>

        {/* Formulario */}
        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          {/* Error */}
          {error && (
            <div className="flex items-start gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
            </div>
          )}

          {/* Nombre */}
          <div>
            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
              Nombre del Proyecto *
            </label>
            <input
              type="text"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              placeholder="Ej: Campaña Marketing 2025"
              required
              maxLength={200}
              className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-colors"
            />
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Mínimo 3 caracteres, máximo 200
            </p>
          </div>

          {/* Descripción */}
          <div>
            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
              Descripción
            </label>
            <textarea
              value={form.descripcion}
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
              placeholder="Describe el objetivo y alcance del proyecto..."
              rows={4}
              className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 resize-none transition-colors"
            />
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Opcional - Ayuda a tu equipo a entender el contexto del proyecto
            </p>
          </div>

          {/* Estado (solo en edición) */}
          {proyecto && (
            <div>
              <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
                Estado
              </label>
              <select
                value={form.estado}
                onChange={(e) => setForm({ ...form, estado: e.target.value })}
                className="w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-colors"
              >
                <option value="activo">Activo</option>
                <option value="archivado">Archivado</option>
              </select>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                Los proyectos archivados no se muestran en la vista principal
              </p>
            </div>
          )}

          {/* Botones */}
          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={handleCancel}
              className="flex-1 px-6 py-3 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 font-semibold rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all border border-slate-300 dark:border-slate-700"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed shadow-md dark:shadow-glow-sm transition-all"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Guardando...
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  {proyecto ? 'Actualizar' : 'Crear Proyecto'}
                </>
              )}
            </button>
          </div>
        </form>

        {/* Info adicional */}
        <div className="bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-700 p-6">
          <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">
            💡 Consejos:
          </h3>
          <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
            <li className="flex items-start gap-2">
              <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
              <span>Usa nombres descriptivos que identifiquen claramente el proyecto</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
              <span>La descripción ayuda a mantener el contexto a largo plazo</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
              <span>Archiva proyectos completados para mantener tu workspace limpio</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
