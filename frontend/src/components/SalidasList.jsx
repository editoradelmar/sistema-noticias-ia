import { useState, useEffect } from 'react';
import { salidaService } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import SalidaForm from './SalidaForm';
import { Search, Plus, RefreshCw, Edit, Trash2, Power, PowerOff } from 'lucide-react';

const SalidasList = () => {
  const [salidas, setSalidas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const { isAdmin, canEdit } = useAuth();

  useEffect(() => { loadSalidas(); }, []);

  const loadSalidas = async () => {
    setLoading(true);
    try {
      const data = await salidaService.getAll();
      let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
      setSalidas(lista);
    } catch (err) {
      alert('Error cargando salidas');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (s = null) => { setEditing(s); setIsModalOpen(true); };
  const handleClose = (reload = false) => { setIsModalOpen(false); setEditing(null); if (reload) loadSalidas(); };

  const handleToggle = async (id, activoActual) => {
    try {
      await salidaService.toggleActivo(id, activoActual);
      loadSalidas();
    } catch (err) {
      alert('Error al cambiar estado: ' + (err?.response?.data?.detail || err.message));
    }
  };
  const handleDelete = async (id) => { if (!isAdmin()) { alert('No autorizado'); return; } if (!confirm('Eliminar salida?')) return; try { await salidaService.delete(id); loadSalidas(); } catch (err) { alert('Error al eliminar'); } };

  const filtered = salidas.filter(s => (s?.nombre || '').toLowerCase().includes(filtro.toLowerCase()) || (s?.descripcion || '').toLowerCase().includes(filtro.toLowerCase()));

  if (loading) return (
    <div className="p-8 text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando salidas...</p>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Salidas</h2>
            <p className="text-slate-600 dark:text-slate-400">Gestiona los canales y tipos de salida</p>
          </div>
          {(canEdit() || isAdmin()) && (
            <button onClick={() => handleOpen()} className="flex items-center gap-2 px-6 py-3 bg-emerald-600 dark:bg-emerald-500 text-white font-semibold rounded-lg hover:bg-emerald-700 dark:hover:bg-emerald-600 shadow-md transition-all">
              <Plus className="w-5 h-5" /> Nueva Salida
            </button>
          )}
        </div>
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input value={filtro} onChange={(e) => setFiltro(e.target.value)} placeholder="Buscar en las salidas..." className="w-full pl-12 py-3 pr-4 border-2 rounded-lg bg-white dark:bg-slate-900" />
          </div>
          <button onClick={loadSalidas} className="px-4 py-3 bg-slate-100 dark:bg-slate-900 rounded-lg"><RefreshCw className="w-5 h-5" /></button>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(s => (
          <div key={s.id} className="group relative bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm hover:shadow-xl dark:hover:shadow-glow-md transition-all duration-300 overflow-hidden border border-slate-200 dark:border-slate-700">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="p-6 relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{s.nombre}</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">{s.descripcion}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-bold ${s.activo ? 'bg-emerald-600 text-white' : 'bg-amber-600 text-white'}`}>{s.activo ? 'ACTIVO' : 'INACTIVO'}</span>
              </div>
              <div className="flex gap-2">
                {(isAdmin() || canEdit()) && (
                  <>
                    <button onClick={() => handleOpen(s)} className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-all">
                      <Edit className="w-4 h-4" /> Ver
                    </button>
                    <button onClick={() => handleToggle(s.id, s.activo)} className="px-3 py-2 bg-slate-100 dark:bg-slate-900 rounded-lg" title={s.activo ? 'Desactivar' : 'Activar'}>{s.activo ? <PowerOff className="w-4 h-4" /> : <Power className="w-4 h-4" />}</button>
                    <button onClick={() => handleOpen(s)} className="px-3 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 rounded-lg" title="Editar"><Edit className="w-4 h-4" /></button>
                    <button onClick={() => handleDelete(s.id)} className="px-3 py-2 bg-red-50 dark:bg-red-900/20 text-red-600 rounded-lg" title="Eliminar"><Trash2 className="w-4 h-4" /></button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      {isModalOpen && <SalidaForm salida={editing} onSave={handleClose} onCancel={handleClose} />}
    </div>
  );
};

export default SalidasList;
