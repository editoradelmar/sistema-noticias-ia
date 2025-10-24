import React, { useState, useEffect } from 'react';
import { Folder, Plus, Archive, Trash2, Eye, Edit, RefreshCw, Search, TrendingUp, FileText } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { api } from '../services/api';
import ProyectoForm from './ProyectoForm';
import ProyectoDetalle from './ProyectoDetalle';

export default function ProyectosList() {
  const { token, isAdmin, canEdit } = useAuth();
  const { isDark } = useTheme();
  const [proyectos, setProyectos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('');
  const [estadoFiltro, setEstadoFiltro] = useState('activo');
  const [mostrarForm, setMostrarForm] = useState(false);
  const [proyectoEditar, setProyectoEditar] = useState(null);
  const [proyectoDetalle, setProyectoDetalle] = useState(null);

  useEffect(() => {
    cargarProyectos();
  }, [estadoFiltro]);

  const cargarProyectos = async () => {
    setLoading(true);
    try {
      const data = await api.getProyectos(estadoFiltro, token);
      // Robustecer: si la respuesta no es array, intenta extraer el array o usa []
      let lista = Array.isArray(data)
        ? data
        : (Array.isArray(data?.data) ? data.data : []);
      setProyectos(lista);
    } catch (error) {
      console.error('Error al cargar proyectos:', error);
      setProyectos([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCrear = () => {
    setProyectoEditar(null);
    setMostrarForm(true);
  };

  const handleEditar = (proyecto) => {
    setProyectoEditar(proyecto);
    setMostrarForm(true);
  };

  const handleVerDetalle = async (proyecto) => {
    try {
      const detalle = await api.getProyecto(proyecto.id, token);
      setProyectoDetalle(detalle);
    } catch (error) {
      alert(error.message);
    }
  };

  const handleArchivar = async (id) => {
    if (!confirm('¿Archivar este proyecto? Podrás restaurarlo después.')) return;
    
    try {
      await api.archivarProyecto(id, token);
      await cargarProyectos();
    } catch (error) {
      alert(error.message);
    }
  };

  const handleRestaurar = async (id) => {
    try {
      await api.restaurarProyecto(id, token);
      await cargarProyectos();
    } catch (error) {
      alert(error.message);
    }
  };

  const handleEliminar = async (id) => {
    const confirmacion = confirm(
      'ADVERTENCIA: ¿Eliminar permanentemente este proyecto?\n\n' +
      'Esta acción NO se puede deshacer. Todas las noticias asociadas quedarán sin proyecto.\n\n' +
      '¿Estás seguro?'
    );
    
    if (!confirmacion) return;

    try {
      await api.eliminarProyecto(id, true, token);
      await cargarProyectos();
    } catch (error) {
      alert(error.message);
    }
  };

  const handleFormClose = async (actualizado) => {
    setMostrarForm(false);
    setProyectoEditar(null);
    if (actualizado) {
      await cargarProyectos();
    }
  };

  const proyectosFiltrados = proyectos.filter(p =>
    p.nombre.toLowerCase().includes(filtro.toLowerCase()) ||
    (p.descripcion && p.descripcion.toLowerCase().includes(filtro.toLowerCase()))
  );

  // Si está mostrando el detalle de un proyecto
  if (proyectoDetalle) {
    return (
      <ProyectoDetalle
        proyecto={proyectoDetalle}
        onClose={() => setProyectoDetalle(null)}
        onEditar={() => {
          handleEditar(proyectoDetalle);
          setProyectoDetalle(null);
        }}
        onActualizar={cargarProyectos}
      />
    );
  }

  // Si está mostrando el formulario
  if (mostrarForm) {
    return (
      <ProyectoForm
        proyecto={proyectoEditar}
        onClose={handleFormClose}
      />
    );
  }

  // Vista principal de lista
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-600 dark:bg-blue-500 rounded-lg">
              <Folder className="w-8 h-8 text-white" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
                Proyectos
              </h2>
              <p className="text-slate-600 dark:text-slate-400">
                Gestiona tus proyectos y noticias vinculadas
              </p>
            </div>
          </div>

          {canEdit() && (
            <button
              onClick={handleCrear}
              className="flex items-center gap-2 px-6 py-3 bg-emerald-600 dark:bg-emerald-500 text-white font-semibold rounded-lg hover:bg-emerald-700 dark:hover:bg-emerald-600 shadow-md dark:shadow-glow-sm transition-all transform hover:scale-105"
            >
              <Plus className="w-5 h-5" />
              Nuevo Proyecto
            </button>
          )}
        </div>

        {/* Filtros */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5" />
            <input
              type="text"
              placeholder="Buscar en los proyectos..."
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="w-full pl-12 pr-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-all"
            />
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => setEstadoFiltro('activo')}
              className={`px-4 py-3 rounded-lg font-semibold transition-all ${
                estadoFiltro === 'activo'
                  ? 'bg-blue-600 dark:bg-blue-500 text-white shadow-md dark:shadow-glow-sm'
                  : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
              }`}
            >
              Activos
            </button>
            <button
              onClick={() => setEstadoFiltro('archivado')}
              className={`px-4 py-3 rounded-lg font-semibold transition-all ${
                estadoFiltro === 'archivado'
                  ? 'bg-blue-600 dark:bg-blue-500 text-white shadow-md dark:shadow-glow-sm'
                  : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
              }`}
            >
              Archivados
            </button>
            <button
              onClick={cargarProyectos}
              className="px-4 py-3 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all"
            >
              <RefreshCw className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Lista de proyectos */}
      {loading ? (
        <div className="flex flex-col items-center justify-center h-96">
          <RefreshCw className="w-20 h-20 text-blue-600 dark:text-blue-400 animate-spin" />
          <p className="text-2xl font-bold text-slate-700 dark:text-slate-300 mt-4">
            Cargando proyectos...
          </p>
        </div>
      ) : proyectosFiltrados.length === 0 ? (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md p-20 text-center border border-slate-200 dark:border-slate-700">
          <Folder className="w-32 h-32 text-slate-300 dark:text-slate-600 mx-auto mb-6" />
          <p className="text-2xl font-bold text-slate-500 dark:text-slate-400 mb-4">
            {filtro ? 'No se encontraron proyectos' : 'No hay proyectos'}
          </p>
          {canEdit() && !filtro && (
            <button
              onClick={handleCrear}
              className="mt-4 px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 shadow-md dark:shadow-glow-sm transition-all"
            >
              Crear primer proyecto
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {proyectosFiltrados.map((proyecto) => (
            <ProyectoCard
              key={proyecto.id}
              proyecto={proyecto}
              onEditar={handleEditar}
              onVerDetalle={handleVerDetalle}
              onArchivar={handleArchivar}
              onRestaurar={handleRestaurar}
              onEliminar={handleEliminar}
              canEdit={canEdit()}
              isAdmin={isAdmin()}
              estadoActual={estadoFiltro}
              token={token}
            />
          ))}
        </div>
      )}
    </div>
  );
}

// Componente de tarjeta individual
function ProyectoCard({ 
  proyecto, 
  onEditar, 
  onVerDetalle, 
  onArchivar, 
  onRestaurar,
  onEliminar, 
  canEdit, 
  isAdmin,
  estadoActual,
  token
}) {
  const { isDark } = useTheme();
  const [stats, setStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(false);

  useEffect(() => {
    cargarStats();
  }, [proyecto.id, token]);

  const cargarStats = async () => {
    setLoadingStats(true);
    try {
      const data = await api.getProyectoStats(proyecto.id, token);
      setStats(data);
    } catch (error) {
      console.error('Error al cargar stats:', error);
    } finally {
      setLoadingStats(false);
    }
  };

  const estadoColors = {
    activo: 'bg-emerald-600 dark:bg-emerald-500 text-white',
    archivado: 'bg-amber-600 dark:bg-amber-500 text-white',
    eliminado: 'bg-red-600 dark:bg-red-500 text-white'
  };

  return (
    <div className="group relative bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm hover:shadow-xl dark:hover:shadow-glow-md transition-all duration-300 overflow-hidden border border-slate-200 dark:border-slate-700">
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      
      <div className="p-6 relative z-10">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                {proyecto.nombre}
              </h3>
              <span className={`px-2 py-1 rounded text-xs font-bold ${estadoColors[proyecto.estado]}`}>
                {proyecto.estado.toUpperCase()}
              </span>
            </div>
            {proyecto.descripcion && (
              <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2">
                {proyecto.descripcion}
              </p>
            )}
          </div>
        </div>

        {/* Stats */}
        {loadingStats ? (
          <div className="py-4 text-center">
            <RefreshCw className="w-6 h-6 text-blue-500 animate-spin mx-auto" />
          </div>
        ) : stats && (
          <div className="bg-slate-50 dark:bg-slate-900/50 rounded-lg p-4 mb-4 border border-slate-200 dark:border-slate-700">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                <span className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                  Noticias
                </span>
              </div>
              <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {stats.total_noticias}
              </span>
            </div>
            
            {stats.total_noticias > 0 && (
              <div className="space-y-1">
                {Object.entries(stats.noticias_por_seccion || {}).map(([sec, count]) => (
                  <div key={sec} className="flex justify-between text-xs">
                    <span className="text-slate-600 dark:text-slate-400 capitalize">{sec}</span>
                    <span className="font-semibold text-slate-700 dark:text-slate-300">{count}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Fechas */}
        <div className="text-xs text-slate-500 dark:text-slate-400 mb-4 space-y-1">
          <div>Creado: {new Date(proyecto.created_at).toLocaleDateString()}</div>
          {proyecto.updated_at && (
            <div>Actualizado: {new Date(proyecto.updated_at).toLocaleDateString()}</div>
          )}
        </div>

        {/* Acciones */}
        <div className="flex gap-2">
          <button
            onClick={() => onVerDetalle(proyecto)}
            className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-all text-sm font-semibold"
          >
            <Eye className="w-4 h-4" />
            Ver
          </button>

          {canEdit && estadoActual === 'activo' && (
            <>
              <button
                onClick={() => onEditar(proyecto)}
                className="px-3 py-2 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all"
                title="Editar"
              >
                <Edit className="w-4 h-4" />
              </button>
              <button
                onClick={() => onArchivar(proyecto.id)}
                className="px-3 py-2 bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 rounded-lg hover:bg-amber-600 hover:text-white dark:hover:bg-amber-600 transition-all"
                title="Archivar"
              >
                <Archive className="w-4 h-4" />
              </button>
            </>
          )}

          {canEdit && estadoActual === 'archivado' && (
            <button
              onClick={() => onRestaurar(proyecto.id)}
              className="px-3 py-2 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 rounded-lg hover:bg-emerald-600 hover:text-white dark:hover:bg-emerald-600 transition-all"
              title="Restaurar"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          )}

          {isAdmin && (
            <button
              onClick={() => onEliminar(proyecto.id)}
              className="px-3 py-2 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all"
              title="Eliminar permanentemente"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
