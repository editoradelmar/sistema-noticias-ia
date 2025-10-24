import { useState, useEffect } from 'react';
import { promptService } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import PromptForm from './PromptForm';
import { Search, Plus, RefreshCw, Power, PowerOff, Edit, Trash2, Eye } from 'lucide-react';

const PromptsList = () => {
  const [prompts, setPrompts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const { isAdmin, canEdit } = useAuth();

  useEffect(() => {
    loadPrompts();
  }, []);

  const loadPrompts = async () => {
    setLoading(true);
    try {
      const data = await promptService.getAll();
  let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
  setPrompts(lista);
    } catch (err) {
      console.error(err);
      alert('Error cargando prompts');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (p = null) => {
    setEditing(p);
    setIsModalOpen(true);
  };

  const handleClose = (reload = false) => {
    // Si el argumento es un objeto Prompt con id, reabrir el formulario con ese objeto
    if (reload && reload.id) {
      setEditing(reload);
      setIsModalOpen(true);
      loadPrompts();
      return;
    }
    setIsModalOpen(false);
    setEditing(null);
    if (reload) loadPrompts();
  };

  const handleDelete = async (id) => {
    if (!isAdmin()) { alert('No autorizado'); return; }
    if (!confirm('Eliminar prompt?')) return;
    try { await promptService.delete(id); loadPrompts(); } catch (err) { alert('Error al eliminar'); }
  };

  const handleToggle = async (id, activoActual) => {
    try {
      await promptService.toggleActivo(id, activoActual);
      loadPrompts();
    } catch (err) {
      alert('Error cambiando estado: ' + (err?.response?.data?.detail || err.message));
    }
  };

  const filtered = prompts.filter(p => p.nombre.toLowerCase().includes(filtro.toLowerCase()));

  if (loading) return <div className="p-8 text-center">Cargando...</div>;

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Prompts</h2>
            <p className="text-slate-600 dark:text-slate-400">Gestiona los prompts reutilizables</p>
          </div>

          {(canEdit() || isAdmin()) && (
            <button onClick={() => handleOpen()} className="flex items-center gap-2 px-6 py-3 bg-emerald-600 dark:bg-emerald-500 text-white font-semibold rounded-lg hover:bg-emerald-700 dark:hover:bg-emerald-600 shadow-md transition-all">
              <Plus className="w-5 h-5" /> Nuevo Prompt
            </button>
          )}
        </div>

        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input value={filtro} onChange={(e) => setFiltro(e.target.value)} placeholder="Buscar en los prompts..." className="w-full pl-12 py-3 pr-4 border-2 rounded-lg bg-white dark:bg-slate-900" />
          </div>
          <button onClick={loadPrompts} className="px-4 py-3 bg-slate-100 dark:bg-slate-900 rounded-lg"><RefreshCw className="w-5 h-5" /></button>
        </div>
      </div>


      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(p => (
          <div key={p.id} className="group relative bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm hover:shadow-xl dark:hover:bg-slate-800 transition-all duration-300 overflow-hidden border border-slate-200 dark:border-slate-700">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="p-6 relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{p.nombre}</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">{p.descripcion}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-bold ${p.activo ? 'bg-emerald-600 text-white' : 'bg-amber-600 text-white'}`}>{p.activo ? 'ACTIVO' : 'INACTIVO'}</span>
              </div>
              <div className="flex gap-2">
                {(isAdmin() || canEdit()) && (
                  <>
                    <button onClick={() => handleOpen(p)} className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-all">
                      <Search className="w-4 h-4" />
                      Ver
                    </button>
                    <button onClick={() => handleToggle(p.id, p.activo)} title={p.activo ? 'Desactivar' : 'Activar'} className="px-3 py-2 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all">
                      {p.activo ? <PowerOff className="w-4 h-4" /> : <Power className="w-4 h-4" />}
                    </button>
                    <button onClick={() => handleOpen(p)} title="Editar" className="px-3 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-600 hover:text-white dark:hover:bg-blue-600 transition-all">
                      <Edit className="w-4 h-4" />
                    </button>
                    <button onClick={() => handleDelete(p.id)} title="Eliminar" className="px-3 py-2 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {isModalOpen && <PromptForm prompt={editing} onSave={handleClose} onCancel={handleClose} />}
    </div>
  );
};

export default PromptsList;
