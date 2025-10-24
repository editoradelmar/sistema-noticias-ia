import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { generacionService } from '../services/generacion';
import { seccionService } from '../services/maestros';
import NoticiaForm from './NoticiaForm';
import NoticiaGeneracionVista from '../NoticiaGeneracionVista';
import { useAuth } from '../context/AuthContext';

export default function NoticiasList() {
  const [secciones, setSecciones] = useState([]);
  useEffect(() => {
    seccionService.getAll({ activo: true }).then(data => setSecciones(data || []));
  }, []);

  function getSeccionInfo(seccion_id) {
    if (!seccion_id) return { nombre: 'Sin sección', color: '#64748b', textColor: '#fff' };
    const sec = secciones.find(s => s.id === seccion_id);
    if (sec && sec.color) {
      // Contraste simple: si el color es claro, texto oscuro; si es oscuro, texto blanco
      const hex = sec.color.replace('#', '');
      const r = parseInt(hex.substring(0,2), 16);
      const g = parseInt(hex.substring(2,4), 16);
      const b = parseInt(hex.substring(4,6), 16);
      const luminance = (0.299*r + 0.587*g + 0.114*b) / 255;
      const textColor = luminance > 0.6 ? '#222' : '#fff';
      return { nombre: sec.nombre, color: sec.color, textColor };
    }
    return { nombre: 'Sin sección', color: '#64748b', textColor: '#fff' };
  }
  const [noticias, setNoticias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState("");
  const [estadoFiltro, setEstadoFiltro] = useState('activo');
  const [editNoticia, setEditNoticia] = useState(null);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [loadingEdit, setLoadingEdit] = useState(false);
  const { token, isAdmin, canEdit } = useAuth();

  const noticiasFiltradas = noticias.filter(n =>
    n.titulo.toLowerCase().includes(filtro.toLowerCase()) ||
    n.contenido.toLowerCase().includes(filtro.toLowerCase())
  );

  useEffect(() => {
    fetchNoticias();
  }, [estadoFiltro]);

  const fetchNoticias = async () => {
    setLoading(true);
    try {
      // Suponiendo que api.getNoticias puede recibir un filtro de estado
      const noticiasResp = await api.getNoticias({ estado: estadoFiltro });
      let lista = Array.isArray(noticiasResp)
        ? noticiasResp
        : (Array.isArray(noticiasResp?.data) ? noticiasResp.data : []);
      setNoticias(lista);
    } catch (err) {
      console.error("Error al obtener noticias:", err);
      setNoticias([]);
    } finally {
      setLoading(false);
    }
  };

  const regenerarResumen = async (noticia) => {
    setLoading(true);
    try {
      if (!noticia.llm_id) {
        alert('No se puede regenerar: la noticia no tiene un modelo LLM asignado.');
        return;
      }
      await generacionService.regenerarTodo(noticia.id, noticia.llm_id);
      await fetchNoticias();
    } catch (err) {
      console.error("Error al regenerar salidas:", err);
      alert('Error al regenerar salidas: ' + (err?.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleEditar = async noticia => {
    setLoadingEdit(true);
    try {
      // Obtener noticia completa por ID (incluye salidas_ids)
      const data = await api.getNoticia(noticia.id);
      setEditNoticia(data);
    } catch (err) {
      alert('Error al cargar la noticia para edición');
    } finally {
      setLoadingEdit(false);
    }
  };

  const handleEliminar = async noticiaId => {
    if (!window.confirm('¿Eliminar esta noticia? Esta acción no se puede deshacer.')) return;
    setLoading(true);
    try {
      await api.eliminarNoticia(noticiaId, token);
      await fetchNoticias();
    } catch (err) {
      alert('Error al eliminar noticia');
    } finally {
      setLoading(false);
    }
  };

  const handleFormClose = async actualizado => {
    setEditNoticia(null);
    setMostrarForm(false);
    if (actualizado) await fetchNoticias();
  };

  const handleCrear = () => {
    setEditNoticia(null);
    setMostrarForm(true);
  };

  if (loadingEdit) {
    return (
      <div className="flex flex-col items-center justify-center h-96">
        <div className="w-20 h-20 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-2xl font-bold text-slate-700 dark:text-slate-300 mt-4">Cargando noticia...</p>
      </div>
    );
  }

  if (editNoticia) {
    // Renderizar el layout de dos paneles para edición
    return <NoticiaGeneracionVista noticiaId={editNoticia.id} onVolverLista={handleFormClose} />;
  }

  if (mostrarForm) {
    // Muestra el flujo de generación de dos paneles en modo creación
    return <NoticiaGeneracionVista onVolverLista={handleFormClose} />;
  }

  if (loading) return (
    <div className="flex flex-col items-center justify-center h-96">
      <RefreshCw className="w-20 h-20 text-blue-600 dark:text-blue-400 animate-spin" />
      <p className="text-2xl font-bold text-slate-700 dark:text-slate-300 mt-4">Cargando noticias...</p>
    </div>
  );

  if (noticias.length === 0) return (
    <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md p-20 text-center border border-slate-200 dark:border-slate-700">
      <FileText className="w-32 h-32 text-slate-300 dark:text-slate-600 mx-auto mb-6" />
      <p className="text-2xl font-bold text-slate-500 dark:text-slate-400 mb-4">No se han encontrado noticias registradas.</p>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header unificado estilo proyectos */}
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm p-6 border border-slate-200 dark:border-slate-700 mb-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-600 dark:bg-blue-500 rounded-lg">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">Noticias</h2>
              <p className="text-slate-600 dark:text-slate-400">
                Consulta y gestiona las noticias generadas por IA y manualmente
              </p>
            </div>
          </div>
          {canEdit() && (
            <button
              onClick={handleCrear}
              className="flex items-center gap-2 px-6 py-3 bg-emerald-600 dark:bg-emerald-500 text-white font-semibold rounded-lg hover:bg-emerald-700 dark:hover:bg-emerald-600 shadow-md dark:shadow-glow-sm transition-all transform hover:scale-105"
            >
              <FileText className="w-5 h-5" />
              Nueva Noticia
            </button>
          )}
        </div>
        {/* Filtros y buscador */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5" />
            <input
              type="text"
              value={filtro}
              onChange={e => setFiltro(e.target.value)}
              placeholder="Buscar en las noticias..."
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
              onClick={fetchNoticias}
              className="px-4 py-3 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all"
            >
              <RefreshCw className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Lista de noticias estilo tarjetas proyectos */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {noticiasFiltradas.map(noticia => (
          <div key={noticia.id} className="group relative bg-white dark:bg-slate-800 rounded-lg shadow-lg dark:shadow-glow-sm hover:shadow-xl dark:hover:shadow-glow-md transition-all duration-300 overflow-hidden border border-slate-200 dark:border-slate-700">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div className="p-6 relative z-10 flex flex-col gap-3">
              <div className="flex items-center gap-2 mb-2">
                <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors flex items-center gap-2">
                  {noticia.titulo}
                  <span className={`px-2 py-1 rounded text-xs font-bold ml-2 ${noticia.estado === 'activo' ? 'bg-emerald-600 dark:bg-emerald-500 text-white' : 'bg-amber-600 dark:bg-amber-500 text-white'}`}>{noticia.estado === 'activo' ? 'ACTIVO' : 'INACTIVO'}</span>
                </h3>
              </div>
              <div className="flex items-center gap-2 mb-2">
                {/* Estado de la noticia con icono */}
                {(() => {
                  const info = getSeccionInfo(noticia.seccion_id);
                  return (
                    <span
                      className="px-2 py-1 rounded text-xs font-bold border border-slate-200 dark:border-slate-700 shadow-sm"
                      style={{ backgroundColor: info.color, color: info.textColor }}
                    >
                      {info.nombre.toUpperCase()}
                    </span>
                  );
                })()}
                <span className="text-xs text-slate-400 font-mono tracking-tight">
                  {(new Date(noticia.fecha)).toLocaleDateString()}
                </span>
              </div>
              <p className="text-slate-700 dark:text-slate-200 mb-2 text-lg leading-relaxed line-clamp-3 drop-shadow-sm">
                {noticia.contenido}
              </p>
              {noticia.resumen_ia && (
                <div className="bg-blue-900 border-2 border-blue-600 rounded-xl p-5 mb-3 flex flex-col gap-2 shadow-lg">
                  <span className="text-xs font-bold text-blue-300 flex items-center gap-2 tracking-wide">
                    <FileText className="inline w-4 h-4 mr-1" />
                    Resumen IA
                  </span>
                  <p className="text-xs text-blue-100 mt-1 drop-shadow-sm">{noticia.resumen_ia}</p>
                </div>
              )}
              <div className="flex items-center gap-2 mt-1">
                <button
                  className="flex items-center gap-2 w-[230px] py-2 px-0 bg-blue-600 dark:bg-blue-500 text-white font-bold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 text-base transition-all shadow-md dark:shadow-glow-sm justify-center"
                  onClick={() => regenerarResumen(noticia)}
                  type="button"
                >
                  <RefreshCw className="w-5 h-5" />
                  <span className="font-bold">Regenerar</span>
                </button>
                <div className="flex items-center gap-2 ml-auto">
                  {/* Cambiar estado */}
                  {canEdit() && (
                    <button
                      className={`p-2 rounded-lg transition-all ${noticia.estado === 'activo' ? 'bg-slate-100 dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 hover:bg-slate-200 dark:hover:bg-slate-800' : 'bg-slate-100 dark:bg-slate-900 text-amber-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-800'}`}
                      title={noticia.estado === 'activo' ? 'Desactivar' : 'Activar'}
                      onClick={() => handleToggleEstado(noticia)}
                    >
                      {noticia.estado === 'activo' ? <Power className="w-4 h-4" /> : <PowerOff className="w-4 h-4" />}
                    </button>
                  )}
                  {/* Editar */}
                  {canEdit() && (
                    <button
                      className="p-2 bg-slate-800 dark:bg-slate-900 text-slate-200 dark:text-slate-300 rounded-lg hover:bg-slate-700 dark:hover:bg-slate-800 transition-all"
                      title="Editar noticia"
                      onClick={() => handleEditar(noticia)}
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                  )}
                  {/* Eliminar */}
                  {isAdmin() && (
                    <button
                      className="p-2 bg-red-900/20 text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all"
                      title="Eliminar noticia"
                      onClick={() => handleEliminar(noticia.id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
// Etiqueta colorida para categoría
    </div>
  );
}
import { RefreshCw, FileText, Edit, Trash2, Search, Power, PowerOff } from 'lucide-react';
// Cambiar estado activo/inactivo de la noticia
async function handleToggleEstado(noticia) {
  try {
    // Usar el método correcto del servicio
  // Si está activo, lo pasamos a archivado (INACTIVO); si no, lo pasamos a activo
  await api.actualizarNoticia(noticia.id, { estado: noticia.estado === 'activo' ? 'archivado' : 'activo' });
    window.location.reload(); // fallback para recargar la lista
  } catch (err) {
    alert('Error al cambiar el estado: ' + (err?.response?.data?.detail || err.message));
  }
}
