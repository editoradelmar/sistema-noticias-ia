import React, { useState, useEffect } from 'react';
import { 
  ArrowLeft, 
  Edit, 
  Archive, 
  Trash2, 
  FileText, 
  TrendingUp, 
  Calendar,
  Sparkles,
  Zap,
  RefreshCw
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { api } from '../services/api';
import { seccionService } from '../services/maestros';

export default function ProyectoDetalle({ proyecto, onClose, onEditar, onActualizar }) {
  const [secciones, setSecciones] = useState([]);
  useEffect(() => {
    seccionService.getAll({ activo: true })
      .then(data => {
        const seccionesOrdenadas = (data || []).sort((a, b) => 
          a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' })
        );
        setSecciones(seccionesOrdenadas);
      });
  }, []);

  function getSeccionInfo(seccion_id) {
    if (!seccion_id) return { nombre: 'Sin sección', color: 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200' };
    const sec = secciones.find(s => s.id === seccion_id);
    return sec
      ? { nombre: sec.nombre, color: `bg-[${sec.color}] text-white` }
      : { nombre: 'Sin sección', color: 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200' };
  }
  const { token, canEdit, isAdmin } = useAuth();
  const { isDark } = useTheme();
  const [noticias, setNoticias] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarDatos();
  }, [proyecto.id]);

  const cargarDatos = async () => {
    setLoading(true);
    try {
      const [noticiasData, statsData] = await Promise.all([
        api.getNoticias(proyecto.id),
        api.getProyectoStats(proyecto.id, token)
      ]);
      setNoticias(noticiasData);
      setStats(statsData);
    } catch (error) {
      console.error('Error al cargar datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const generarResumen = async (noticiaId) => {
    try {
      await api.generarResumen(noticiaId);
      await cargarDatos();
    } catch (error) {
      alert(error.message);
    }
  };

  const eliminarNoticia = async (id) => {
    if (!confirm('¿Eliminar esta noticia del proyecto?')) return;
    
    try {
      await api.eliminarNoticia(id, token);
      await cargarDatos();
    } catch (error) {
      alert(error.message);
    }
  };

  const estadoColors = {
    activo: 'bg-emerald-600 dark:bg-emerald-500',
    archivado: 'bg-amber-600 dark:bg-amber-500',
    eliminado: 'bg-red-600 dark:bg-red-500'
  };

  return (
    <div className="space-y-6">
      {/* Header del Proyecto */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md overflow-hidden border border-slate-200 dark:border-slate-700">
        <div className="bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-700 dark:to-cyan-700 p-8">
          <div className="flex items-start justify-between mb-4">
            <button
              onClick={onClose}
              className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg font-medium transition-all"
            >
              <ArrowLeft className="w-5 h-5" />
              Volver
            </button>

            {canEdit() && (
              <div className="flex gap-2">
                <button
                  onClick={onEditar}
                  className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg font-medium transition-all"
                >
                  <Edit className="w-5 h-5" />
                  Editar
                </button>
              </div>
            )}
          </div>

          <div className="flex items-start gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-3">
                <h1 className="text-4xl font-bold text-white">
                  {proyecto.nombre}
                </h1>
                <span className={`px-3 py-1 ${estadoColors[proyecto.estado]} text-white text-sm font-bold rounded-md shadow-md`}>
                  {proyecto.estado.toUpperCase()}
                </span>
              </div>

              {proyecto.descripcion && (
                <p className="text-blue-100 dark:text-cyan-100 text-lg leading-relaxed">
                  {proyecto.descripcion}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Estadísticas */}
        {stats && (
          <div className="p-6 bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-700">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <StatCard
                icon={FileText}
                label="Total Noticias"
                value={stats.total_noticias}
                color="blue"
              />
              <StatCard
                icon={TrendingUp}
                label="Secciones"
                value={Object.keys(stats.noticias_por_seccion || {}).length}
                color="emerald"
              />
              <StatCard
                icon={Calendar}
                label="Creado"
                value={new Date(proyecto.created_at).toLocaleDateString()}
                color="cyan"
                isDate
              />
              <StatCard
                icon={Sparkles}
                label="Última Act."
                value={stats.ultima_actualizacion 
                  ? new Date(stats.ultima_actualizacion).toLocaleDateString()
                  : 'N/A'}
                color="violet"
                isDate
              />
            </div>

            {/* Distribución por sección */}
            {stats.noticias_por_seccion && Object.keys(stats.noticias_por_seccion).length > 0 && (
              <div className="mt-6">
                <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">
                  Distribución por Sección:
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                  {Object.entries(stats.noticias_por_seccion).map(([secId, count]) => {
                    const info = getSeccionInfo(Number(secId));
                    return (
                      <div
                        key={secId}
                        className={`p-3 rounded-lg border text-center ${info.color}`}
                      >
                        <p className="text-2xl font-bold">{count}</p>
                        <p className="text-xs capitalize mt-1">{info.nombre}</p>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Noticias del Proyecto */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
            Noticias del Proyecto
          </h2>
          <button
            onClick={cargarDatos}
            className="px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-all"
          >
            <RefreshCw className="w-5 h-5" />
          </button>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center h-64">
            <RefreshCw className="w-16 h-16 text-blue-600 dark:text-blue-400 animate-spin" />
            <p className="text-lg font-semibold text-slate-700 dark:text-slate-300 mt-4">
              Cargando noticias...
            </p>
          </div>
        ) : noticias.length === 0 ? (
          <div className="text-center py-20">
            <FileText className="w-24 h-24 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
            <p className="text-xl font-bold text-slate-500 dark:text-slate-400">
              No hay noticias en este proyecto
            </p>
            <p className="text-slate-400 dark:text-slate-500 mt-2">
              Crea noticias y vincúlalas a este proyecto para comenzar
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {noticias.map((noticia) => (
              <NoticiaCard
                key={noticia.id}
                noticia={noticia}
                onGenerarResumen={generarResumen}
                onEliminar={eliminarNoticia}
                canDelete={canEdit()}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Componente de tarjeta de estadística
function StatCard({ icon: Icon, label, value, color, isDate = false }) {
  const colors = {
    blue: 'bg-blue-600 dark:bg-blue-500',
    emerald: 'bg-emerald-600 dark:bg-emerald-500',
    cyan: 'bg-cyan-600 dark:bg-cyan-500',
    violet: 'bg-violet-600 dark:bg-violet-500'
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
      <div className="flex items-center gap-3 mb-2">
        <div className={`p-2 ${colors[color]} rounded-lg`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
        <p className="text-sm font-semibold text-slate-600 dark:text-slate-400">
          {label}
        </p>
      </div>
      <p className={`text-2xl font-bold ${isDate ? 'text-sm' : ''} text-slate-900 dark:text-slate-100`}>
        {value}
      </p>
    </div>
  );
}

// Componente de tarjeta de noticia
function NoticiaCard({ noticia, onGenerarResumen, onEliminar, canDelete }) {
  const [loading, setLoading] = useState(false);
  const [secciones, setSecciones] = useState([]);
  useEffect(() => {
    seccionService.getAll({ activo: true })
      .then(data => {
        const seccionesOrdenadas = (data || []).sort((a, b) => 
          a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' })
        );
        setSecciones(seccionesOrdenadas);
      });
  }, []);
  function getSeccionInfo(seccion_id) {
    if (!seccion_id) return { nombre: 'Sin sección', color: 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200' };
    const sec = secciones.find(s => s.id === seccion_id);
    return sec
      ? { nombre: sec.nombre, color: `bg-[${sec.color}] text-white` }
      : { nombre: 'Sin sección', color: 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200' };
  }
  const handleResumen = async () => {
    setLoading(true);
    await onGenerarResumen(noticia.id);
    setLoading(false);
  };
  const info = getSeccionInfo(noticia.seccion_id);
  return (
    <div className="group relative bg-slate-50 dark:bg-slate-900/50 rounded-lg p-5 border border-slate-200 dark:border-slate-700 hover:border-blue-500 dark:hover:bg-blue-400 transition-all duration-300">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
            {noticia.titulo}
          </h3>
          <div className="flex items-center gap-2 mb-2">
            <span className={`px-2 py-1 rounded text-xs font-bold ${info.color}`}>
              {info.nombre.toUpperCase()}
            </span>
            <span className="text-xs text-slate-500 dark:text-slate-400">
              {noticia.fecha}
            </span>
          </div>
        </div>
        {canDelete && (
          <button
            onClick={() => onEliminar(noticia.id)}
            className="p-2 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>
      <p className="text-sm text-slate-700 dark:text-slate-300 mb-3 line-clamp-3">
        {noticia.contenido}
      </p>
      {noticia.resumen_ia && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3 mb-3">
          <div className="flex items-center gap-2 mb-1">
            <Sparkles className="w-3 h-3 text-blue-600 dark:text-blue-400" />
            <span className="text-xs font-bold text-blue-700 dark:text-blue-400">RESUMEN IA</span>
          </div>
          <p className="text-xs text-slate-700 dark:text-slate-300">
            {noticia.resumen_ia}
          </p>
        </div>
      )}
      {/* Botón Generar Resumen comentado temporalmente
      <button
        onClick={handleResumen}
        disabled={loading}
        className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 dark:bg-blue-500 text-white text-sm font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 disabled:opacity-50 transition-all"
      >
        {loading ? (
          <>
            <RefreshCw className="w-4 h-4 animate-spin" />
            Generando...
          </>
        ) : (
          <>
            <Zap className="w-4 h-4" />
            {noticia.resumen_ia ? 'Regenerar' : 'Generar'} Resumen
          </>
        )}
      </button>
      */}
    </div>
  );
}
