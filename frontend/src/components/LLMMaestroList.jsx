import React, { useState, useEffect } from 'react';
import { llmService } from '../services/maestros';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import LLMMaestroForm from './LLMMaestroForm';
import { Plus, Bot, RefreshCw, Search, Power, PowerOff, Edit, Trash2, Eye } from 'lucide-react';

export default function LLMMaestroList() {
  const { isAdmin, canEdit } = useAuth();
  const { isDark } = useTheme();
  const [llms, setLlms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingLlm, setEditingLlm] = useState(null);

  useEffect(() => {
    cargarLLMs();
  }, []);

  const cargarLLMs = async () => {
    setLoading(true);
    try {
      const data = await llmService.getAll();
  let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
  setLlms(lista);
    } catch (err) {
      console.error('Error al cargar los modelos LLM:', err);
      alert('Error al cargar los modelos LLM.');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (id) => {
    try {
      await llmService.toggleActivo(id);
      cargarLLMs();
    } catch (err) {
      alert('Error al cambiar el estado: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleOpenModal = (llm = null) => {
    setEditingLlm(llm);
    setIsModalOpen(true);
  };

  const handleCloseModal = (updated = false) => {
    setIsModalOpen(false);
    setEditingLlm(null);
    if (updated) cargarLLMs();
  };

  const handleSave = async (llmData, setLoadingForm, setErrorForm) => {
    setLoadingForm(true);
    setErrorForm('');
    try {
      if (editingLlm) {
        const dataToUpdate = { ...llmData };
        if (!dataToUpdate.api_key) delete dataToUpdate.api_key;
        await llmService.update(editingLlm.id, dataToUpdate);
      } else {
        await llmService.create(llmData);
      }
      handleCloseModal(true);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message;
      console.error(err);
      setErrorForm(errorMessage);
    } finally {
      setLoadingForm(false);
    }
  };

  const handleDelete = async (id) => {
    if (!isAdmin()) {
      alert('No tienes permisos para realizar esta acción.');
      return;
    }
    if (!confirm('ADVERTENCIA: ¿Eliminar permanentemente este modelo LLM?\n\nEsta acción NO se puede deshacer.')) return;
    try {
      await llmService.delete(id);
      cargarLLMs();
    } catch (err) {
      alert('Error al eliminar: ' + (err.response?.data?.detail || err.message));
    }
  };

  const llmsFiltrados = llms.filter(llm =>
    llm.nombre.toLowerCase().includes(filtro.toLowerCase()) ||
    llm.modelo_id.toLowerCase().includes(filtro.toLowerCase()) ||
    llm.proveedor.toLowerCase().includes(filtro.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Modelos LLM</h2>
            <p className="text-slate-600 dark:text-slate-400">Gestione los modelos de lenguaje utilizados por el sistema</p>
          </div>

          {(canEdit() || isAdmin()) && (
            <button
              onClick={() => handleOpenModal()}
              className="flex items-center gap-2 px-6 py-3 bg-emerald-600 dark:bg-emerald-500 text-white font-semibold rounded-lg hover:bg-emerald-700 dark:hover:bg-emerald-600 shadow-md dark:shadow-glow-sm transition-all transform hover:scale-105"
            >
              <Plus className="w-5 h-5" />
              Nuevo modelo LLM
            </button>
          )}
        </div>

        {/* Filtro y Recargar */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar modelos LLM..."
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="w-full pl-12 pr-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-all"
            />
          </div>
          <button
            onClick={cargarLLMs}
            className="px-4 py-3 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Lista de LLMs */}
      {loading ? (
        <div className="flex flex-col items-center justify-center h-96 bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md p-20 border border-slate-200 dark:border-slate-700">
          <RefreshCw className="w-20 h-20 text-blue-600 dark:text-blue-400 animate-spin" />
          <p className="text-2xl font-bold text-slate-700 dark:text-slate-300 mt-4">Cargando modelos LLM...</p>
        </div>
      ) : llmsFiltrados.length === 0 ? (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md p-20 text-center border border-slate-200 dark:border-slate-700">
          <Bot className="w-32 h-32 text-slate-300 dark:text-slate-600 mx-auto mb-6" />
          <p className="text-2xl font-bold text-slate-500 dark:text-slate-400 mb-4">{filtro ? 'No se encontraron modelos LLM' : 'No existen modelos LLM configurados'}</p>
          {isAdmin() && !filtro && (
            <button onClick={() => handleOpenModal()} className="mt-4 px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 shadow-md dark:shadow-glow-sm transition-all">Crear el primer modelo LLM</button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {llmsFiltrados.map((llm) => (
            <LLMMaestroCard
              key={llm.id}
              llm={llm}
              onVer={handleOpenModal}
              onEditar={handleOpenModal}
              onEliminar={handleDelete}
              onToggle={handleToggle}
              isAdmin={isAdmin}
            />
          ))}
        </div>
      )}

      {isModalOpen && <LLMMaestroForm llm={editingLlm} onSave={handleSave} onCancel={handleCloseModal} />}
    </div>
  );
}

// Componente de tarjeta individual para LLM
function LLMMaestroCard({ llm, onEditar, onEliminar, onToggle, isAdmin }) {
  const { isDark } = useTheme();

  const estadoColors = { activo: 'bg-emerald-600 dark:bg-emerald-500 text-white', inactivo: 'bg-amber-600 dark:bg-amber-500 text-white' };

  return (
    <div className="group relative bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm hover:shadow-xl dark:hover:shadow-glow-md transition-all duration-300 overflow-hidden border border-slate-200 dark:border-slate-700">
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      <div className="p-6 relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{llm.nombre}</h3>
              <span className={`px-2 py-1 rounded text-xs font-bold ${llm.activo ? estadoColors.activo : estadoColors.inactivo}`}>{llm.activo ? 'ACTIVO' : 'INACTIVO'}</span>
            </div>
            <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2">{llm.proveedor} • {llm.modelo_id}</p>
          </div>
        </div>

        <div className="bg-slate-50 dark:bg-slate-900/50 rounded-lg p-4 mb-4 border border-slate-200 dark:border-slate-700">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2"><span className="text-sm font-semibold text-slate-700 dark:text-slate-300">Tokens usados hoy</span></div>
            <span className="text-xl font-bold text-blue-600 dark:text-blue-400">{llm.tokens_usados_hoy.toLocaleString()}{llm.limite_diario_tokens ? ` / ${llm.limite_diario_tokens.toLocaleString()}` : ''}</span>
          </div>
          {llm.costo_entrada !== null && llm.costo_salida !== null && (
            <div className="space-y-1 text-xs text-slate-600 dark:text-slate-400">
              <div className="flex justify-between"><span>Costo de entrada (1K):</span><span className="font-semibold">${llm.costo_entrada}</span></div>
              <div className="flex justify-between"><span>Costo de salida (1K):</span><span className="font-semibold">${llm.costo_salida}</span></div>
            </div>
          )}
        </div>

        {isAdmin() && (
          <div className="flex gap-2">
            <button
              onClick={() => onVer(llm)}
              className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-all text-sm font-semibold"
            >
              <Search className="w-4 h-4" />
              Ver detalles
            </button>

            <button
              onClick={() => onToggle(llm.id)}
              className="px-3 py-2 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all"
              title={llm.activo ? 'Desactivar modelo' : 'Activar modelo'}
            >
              {llm.activo ? <PowerOff className="w-4 h-4" /> : <Power className="w-4 h-4" />}
            </button>

            <button
              onClick={() => onEditar(llm)}
              className="px-3 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-600 hover:text-white dark:hover:bg-blue-600 transition-all"
              title="Editar modelo"
            >
              <Edit className="w-4 h-4" />
            </button>

            <button
              onClick={() => onEliminar(llm.id)}
              className="px-3 py-2 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all"
              title="Eliminar modelo permanentemente"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
}