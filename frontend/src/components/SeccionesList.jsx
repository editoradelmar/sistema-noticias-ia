import { useState, useEffect } from 'react';
import { seccionService } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import SeccionForm from './SeccionForm';
import { Search, Plus, RefreshCw, Edit, Trash2, Power, PowerOff } from 'lucide-react';

const SeccionesList = () => {
  const [secciones, setSecciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filtro, setFiltro] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const { isAdmin, canEdit } = useAuth();

  useEffect(() => { loadSecciones(); }, []);

  const loadSecciones = async () => {
    setLoading(true);
    try {
  const data = await seccionService.getAll();
  let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
  setSecciones(lista);
    } catch (err) {
      setError(err?.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (s = null) => { setEditing(s); setIsModalOpen(true); };
  const handleClose = (reload = false) => { setIsModalOpen(false); setEditing(null); if (reload) loadSecciones(); };

  const handleToggle = async (id, activoActual) => {
    try {
      await seccionService.toggleActivo(id, activoActual);
      loadSecciones();
    } catch (err) {
      alert('Error al cambiar estado: ' + (err?.response?.data?.detail || err.message));
    }
  };
  const handleDelete = async (id) => { if (!isAdmin()) { alert('No autorizado'); return; } if (!confirm('Eliminar sección?')) return; try { await seccionService.delete(id); loadSecciones(); } catch (err) { alert('Error al eliminar: ' + (err?.message || err)); } };

  const filtered = secciones.filter(s => (s?.nombre || '').toLowerCase().includes(filtro.toLowerCase()) || (s?.descripcion || '').toLowerCase().includes(filtro.toLowerCase()));

  if (loading) return (
    <div className="p-8 text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando secciones...</p>
    </div>
  );

  if (error) return (
    <div className="p-8 text-center">
      <p className="text-red-600">Error: {error}</p>
      <button onClick={loadSecciones} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Reintentar</button>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Secciones</h2>
            <p className="text-slate-600 dark:text-slate-400">{secciones.length} sección(es) configurada(s)</p>
          </div>
          {(canEdit() || isAdmin()) && (
            <button onClick={() => handleOpen()} className="flex items-center gap-2 px-6 py-3 bg-emerald-600 dark:bg-emerald-500 text-white font-semibold rounded-lg hover:bg-emerald-700 dark:hover:bg-emerald-600 shadow-md transition-all">
              <Plus className="w-5 h-5" /> Nueva Sección
            </button>
          )}
        </div>

        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input value={filtro} onChange={(e) => setFiltro(e.target.value)} placeholder="Buscar en las secciones..." className="w-full pl-12 py-3 pr-4 border-2 rounded-lg bg-white dark:bg-slate-900" />
          </div>
          <button onClick={loadSecciones} className="px-4 py-3 bg-slate-100 dark:bg-slate-900 rounded-lg"><RefreshCw className="w-5 h-5" /></button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(s => (
          <div key={s.id} className="group relative bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm hover:shadow-xl dark:hover:shadow-glow-md transition-all duration-300 overflow-hidden border border-slate-200 dark:border-slate-700">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="p-6 relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors break-all" title={s.nombre}>{s.nombre}</h3>
                  {s.descripcion && <p className="text-sm text-slate-600 dark:text-slate-400">{s.descripcion}</p>}
                  <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                    {s.prompt?.nombre && <span className="mr-4">Prompt: <span className="font-semibold text-blue-700 dark:text-blue-300">{s.prompt.nombre}</span></span>}
                    {s.estilo?.nombre && <span>Estilo: <span className="font-semibold text-emerald-700 dark:text-emerald-300">{s.estilo.nombre}</span></span>}
                  </div>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-bold ${s.activo ? 'bg-emerald-600 text-white' : 'bg-amber-600 text-white'}`}>{s.activo ? 'ACTIVO' : 'INACTIVO'}</span>
              </div>
              <div className="flex gap-2">
                {(isAdmin() || canEdit()) && (
                  <>
                    <button
                      onClick={() => handleOpen(s)}
                      className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-all text-sm"
                      title="Ver/Editar"
                    >
                      <Edit className="w-4 h-4" /> Ver
                    </button>
                    <button
                      onClick={() => handleToggle(s.id, s.activo)}
                      className={`px-3 py-2 rounded-lg transition-all text-sm flex items-center justify-center gap-2 ${s.activo ? 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800' : 'bg-amber-100 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 hover:bg-amber-200 dark:hover:bg-amber-800'}`}
                      title={s.activo ? 'Desactivar' : 'Activar'}
                    >
                      {s.activo ? <PowerOff className="w-4 h-4" /> : <Power className="w-4 h-4" />}
                    </button>
                    <button
                      onClick={() => handleDelete(s.id)}
                      className="px-3 py-2 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all text-sm flex items-center justify-center"
                      title="Eliminar"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

  {isModalOpen && <SeccionForm seccion={editing} onSave={handleClose} onCancel={handleClose} isOpen={isModalOpen} />}
    </div>
  );
};

export default SeccionesList;
