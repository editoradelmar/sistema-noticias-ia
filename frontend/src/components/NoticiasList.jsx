import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { generacionService } from '../services/generacion';
import { seccionService } from '../services/maestros';
import NoticiaForm from './NoticiaForm';
import NoticiaGeneracionVista from '../NoticiaGeneracionVista';
import { useAuth } from '../context/AuthContext';
import { RefreshCw, FileText, Edit, Trash2, Search, Power, PowerOff, Grid, List, Calendar, User, Filter, ChevronDown, ChevronUp, SortAsc, SortDesc } from 'lucide-react';

export default function NoticiasList() {
  const [secciones, setSecciones] = useState([]);
  const [usuarios, setUsuarios] = useState([]); // Lista de usuarios para filtros
  
  useEffect(() => {
    // Cargar secciones ordenadas alfabéticamente
    seccionService.getAll({ activo: true })
      .then(data => {
        const seccionesOrdenadas = (data || []).sort((a, b) => 
          a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' })
        );
        setSecciones(seccionesOrdenadas);
      });
    
    // Cargar usuarios para el dropdown de filtros
    api.getUsuarios(true).then(data => setUsuarios(data || [])).catch(err => {
      console.error('Error al cargar usuarios:', err);
      setUsuarios([]);
    });
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
  const [vistaActual, setVistaActual] = useState('lista'); // 'tarjetas' o 'lista' - Por defecto: lista
  
  // Nuevos filtros avanzados
  const [filtroUsuario, setFiltroUsuario] = useState('');
  const [filtroSeccion, setFiltroSeccion] = useState('');
  const [filtroFechaDesde, setFiltroFechaDesde] = useState('');
  const [filtroFechaHasta, setFiltroFechaHasta] = useState('');
  const [ordenamiento, setOrdenamiento] = useState('fecha_desc'); // fecha_desc, fecha_asc, titulo_asc, titulo_desc
  const [mostrarFiltrosAvanzados, setMostrarFiltrosAvanzados] = useState(false);
  
  const { token, isAdmin, canEdit } = useAuth();

  // Función de filtrado y ordenamiento avanzado
  const noticiasFiltradas = noticias.filter(n => {
    // Filtro de texto básico
    const cumpleFiltroTexto = n.titulo.toLowerCase().includes(filtro.toLowerCase()) ||
                             n.contenido.toLowerCase().includes(filtro.toLowerCase());
    
    // Filtro por usuario/autor - usa usuario_id como fuente de verdad
    const cumpleFiltroUsuario = !filtroUsuario || 
                               n.usuario_id === parseInt(filtroUsuario);
    
    // Filtro por sección
    const cumpleFiltroSeccion = !filtroSeccion || 
                               n.seccion_id === parseInt(filtroSeccion);
    
    // Filtro por fecha desde
    const cumpleFiltroFechaDesde = !filtroFechaDesde || 
                                  new Date(n.fecha) >= new Date(filtroFechaDesde);
    
    // Filtro por fecha hasta
    const cumpleFiltroFechaHasta = !filtroFechaHasta || 
                                  new Date(n.fecha) <= new Date(filtroFechaHasta + 'T23:59:59');
    
    return cumpleFiltroTexto && cumpleFiltroUsuario && cumpleFiltroSeccion && 
           cumpleFiltroFechaDesde && cumpleFiltroFechaHasta;
  }).sort((a, b) => {
    // Ordenamiento
    switch (ordenamiento) {
      case 'fecha_desc':
        return new Date(b.fecha) - new Date(a.fecha);
      case 'fecha_asc':
        return new Date(a.fecha) - new Date(b.fecha);
      case 'titulo_asc':
        return a.titulo.localeCompare(b.titulo);
      case 'titulo_desc':
        return b.titulo.localeCompare(a.titulo);
      default:
        return new Date(b.fecha) - new Date(a.fecha); // Por defecto: más recientes primero
    }
  });

  // Ya no necesitamos extraer usuarios de las noticias, usamos la lista cargada
  // const usuariosUnicos = [...new Set(noticias.map(n => n.autor_nombre).filter(Boolean))].sort();

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
        <div className="space-y-4">
          {/* Fila principal de filtros */}
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
                title="Refrescar"
              >
                <RefreshCw className="w-5 h-5" />
              </button>
              {/* Botón de filtros avanzados */}
              <button
                onClick={() => setMostrarFiltrosAvanzados(!mostrarFiltrosAvanzados)}
                className={`px-4 py-3 rounded-lg font-semibold transition-all flex items-center gap-2 ${
                  mostrarFiltrosAvanzados
                    ? 'bg-blue-600 dark:bg-blue-500 text-white shadow-md dark:shadow-glow-sm'
                    : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
                }`}
                title="Filtros avanzados"
              >
                <Filter className="w-4 h-4" />
                {mostrarFiltrosAvanzados ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
              {/* Botones de cambio de vista */}
              <div className="flex bg-slate-100 dark:bg-slate-900 rounded-lg p-1">
                <button
                  onClick={() => setVistaActual('tarjetas')}
                  className={`p-2 rounded-md transition-all ${
                    vistaActual === 'tarjetas'
                      ? 'bg-blue-600 dark:bg-blue-500 text-white shadow-sm'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
                  }`}
                  title="Vista de tarjetas"
                >
                  <Grid className="w-5 h-5" />
                </button>
                <button
                  onClick={() => setVistaActual('lista')}
                  className={`p-2 rounded-md transition-all ${
                    vistaActual === 'lista'
                      ? 'bg-blue-600 dark:bg-blue-500 text-white shadow-sm'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'
                  }`}
                  title="Vista de lista"
                >
                  <List className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Filtros avanzados (colapsables) */}
          {mostrarFiltrosAvanzados && (
            <div className="bg-slate-50 dark:bg-slate-900/50 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                {/* Filtro por usuario */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                    Usuario/Autor
                  </label>
                  <select
                    value={filtroUsuario}
                    onChange={e => setFiltroUsuario(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  >
                    <option value="">Todos los usuarios</option>
                    {usuarios.map(usuario => (
                      <option key={usuario.id} value={usuario.id}>
                        {usuario.username} ({usuario.nombre_completo})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Filtro por sección */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                    Sección
                  </label>
                  <select
                    value={filtroSeccion}
                    onChange={e => setFiltroSeccion(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  >
                    <option value="">Todas las secciones</option>
                    {secciones.map(seccion => (
                      <option key={seccion.id} value={seccion.id}>{seccion.nombre}</option>
                    ))}
                  </select>
                </div>

                {/* Filtro fecha desde */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                    Fecha desde
                  </label>
                  <input
                    type="date"
                    value={filtroFechaDesde}
                    onChange={e => setFiltroFechaDesde(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  />
                </div>

                {/* Filtro fecha hasta */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                    Fecha hasta
                  </label>
                  <input
                    type="date"
                    value={filtroFechaHasta}
                    onChange={e => setFiltroFechaHasta(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  />
                </div>

                {/* Ordenamiento */}
                <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                    Ordenar por
                  </label>
                  <select
                    value={ordenamiento}
                    onChange={e => setOrdenamiento(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  >
                    <option value="fecha_desc">📅 Más recientes</option>
                    <option value="fecha_asc">📅 Más antiguas</option>
                    <option value="titulo_asc">🔤 Título A-Z</option>
                    <option value="titulo_desc">🔤 Título Z-A</option>
                  </select>
                </div>
              </div>
              
              {/* Botón limpiar filtros */}
              <div className="mt-4 flex justify-end">
                <button
                  onClick={() => {
                    setFiltroUsuario('');
                    setFiltroSeccion('');
                    setFiltroFechaDesde('');
                    setFiltroFechaHasta('');
                    setOrdenamiento('fecha_desc');
                    setFiltro('');
                  }}
                  className="px-4 py-2 bg-slate-600 dark:bg-slate-700 text-white text-sm rounded-lg hover:bg-slate-700 dark:hover:bg-slate-600 transition-all"
                >
                  Limpiar filtros
                </button>
              </div>
            </div>
          )}
        </div>
        </div>

      {/* Indicador de resultados */}
      <div className="flex items-center justify-between py-3 px-4 bg-slate-50 dark:bg-slate-900/50 rounded-lg border border-slate-200 dark:border-slate-700">
        <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
          <FileText className="w-4 h-4" />
          <span>
            Mostrando <span className="font-bold text-slate-900 dark:text-slate-100">{noticiasFiltradas.length}</span> de{' '}
            <span className="font-bold">{noticias.length}</span> noticias
            {(filtro || filtroUsuario || filtroSeccion || filtroFechaDesde || filtroFechaHasta) && (
              <span className="text-blue-600 dark:text-blue-400 ml-1">(filtradas)</span>
            )}
          </span>
        </div>
        <div className="text-xs text-slate-500 dark:text-slate-400">
          Ordenado por: {
            ordenamiento === 'fecha_desc' ? '📅 Más recientes' :
            ordenamiento === 'fecha_asc' ? '📅 Más antiguas' :
            ordenamiento === 'titulo_asc' ? '🔤 Título A-Z' :
            '🔤 Título Z-A'
          }
        </div>
      </div>

      {/* Lista de noticias - Vista condicional */}
      {vistaActual === 'tarjetas' ? (
        // Vista de tarjetas (actual)
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
                    {(new Date(noticia.fecha)).toLocaleString('es-ES', {
                      year: 'numeric',
                      month: '2-digit',
                      day: '2-digit',
                      hour: '2-digit',
                      minute: '2-digit',
                      hour12: true
                    })}
                  </span>
                </div>
                <p className="text-slate-700 dark:text-slate-200 mb-2 text-lg leading-relaxed overflow-hidden" style={{
                  display: '-webkit-box',
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: 'vertical'
                }}>
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
      ) : (
        // Vista de lista (nueva)
        <div className="space-y-2">
          {noticiasFiltradas.map(noticia => (
            <div key={noticia.id} className="group bg-white dark:bg-slate-800 rounded-lg shadow-sm dark:shadow-glow-sm hover:shadow-md dark:hover:shadow-glow-md transition-all duration-200 border border-slate-200 dark:border-slate-700">
              <div className="p-3">
                <div className="flex items-center justify-between">
                  {/* Contenido principal */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-1">
                      <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors truncate">
                        {noticia.titulo}
                      </h3>
                      <span className={`px-2 py-0.5 rounded text-xs font-bold whitespace-nowrap ${noticia.estado === 'activo' ? 'bg-emerald-600 dark:bg-emerald-500 text-white' : 'bg-amber-600 dark:bg-amber-500 text-white'}`}>
                        {noticia.estado === 'activo' ? 'ACTIVO' : 'INACTIVO'}
                      </span>
                      {(() => {
                        const info = getSeccionInfo(noticia.seccion_id);
                        return (
                          <span
                            className="px-2 py-0.5 rounded text-xs font-bold border border-slate-200 dark:border-slate-700 shadow-sm whitespace-nowrap"
                            style={{ backgroundColor: info.color, color: info.textColor }}
                          >
                            {info.nombre.toUpperCase()}
                          </span>
                        );
                      })()}
                    </div>
                    <p className="text-slate-600 dark:text-slate-300 text-sm truncate">
                      {noticia.contenido}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-slate-500 dark:text-slate-400 mt-1">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        {(new Date(noticia.fecha)).toLocaleString('es-ES', {
                          year: 'numeric',
                          month: '2-digit',
                          day: '2-digit',
                          hour: '2-digit',
                          minute: '2-digit',
                          hour12: true
                        })}
                      </span>
                      {noticia.autor_nombre && (
                        <span className="flex items-center gap-1">
                          <User className="w-3 h-3" />
                          {noticia.autor_nombre}
                        </span>
                      )}
                      {noticia.resumen_ia && (
                        <span className="flex items-center gap-1 text-blue-500 dark:text-blue-400">
                          <FileText className="w-3 h-3" />
                          Con resumen IA
                        </span>
                      )}
                    </div>
                  </div>
                  
                  {/* Acciones */}
                  <div className="flex items-center gap-1 ml-4">
                    {/* Cambiar estado */}
                    {canEdit() && (
                      <button
                        className={`p-1.5 rounded-lg transition-all ${noticia.estado === 'activo' ? 'bg-slate-100 dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 hover:bg-slate-200 dark:hover:bg-slate-800' : 'bg-slate-100 dark:bg-slate-900 text-amber-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-800'}`}
                        title={noticia.estado === 'activo' ? 'Desactivar' : 'Activar'}
                        onClick={() => handleToggleEstado(noticia)}
                      >
                        {noticia.estado === 'activo' ? <Power className="w-4 h-4" /> : <PowerOff className="w-4 h-4" />}
                      </button>
                    )}
                    {/* Editar */}
                    {canEdit() && (
                      <button
                        className="p-1.5 bg-slate-800 dark:bg-slate-900 text-slate-200 dark:text-slate-300 rounded-lg hover:bg-slate-700 dark:hover:bg-slate-800 transition-all"
                        title="Editar noticia"
                        onClick={() => handleEditar(noticia)}
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                    )}
                    {/* Eliminar */}
                    {isAdmin() && (
                      <button
                        className="p-1.5 bg-red-900/20 text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all"
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
      )}
    </div>
  );

  // Cambiar estado activo/inactivo de la noticia
  async function handleToggleEstado(noticia) {
    try {
      // Usar el método correcto del servicio
      // Si está activo, lo pasamos a archivado (INACTIVO); si no, lo pasamos a activo
      await api.actualizarNoticia(noticia.id, { estado: noticia.estado === 'activo' ? 'archivado' : 'activo' }, token);
      fetchNoticias(); // Recargar la lista
    } catch (err) {
      alert('Error al cambiar el estado: ' + (err?.response?.data?.detail || err.message));
    }
  }
}
