/**
 * Lista de Usuarios para Administración
 * Gestión completa de usuarios con jerarquía editorial
 */
import React, { useState, useEffect } from 'react';
import { Users, Plus, Search, Filter, Eye, Edit, Trash2, Key, AlertTriangle, CheckCircle, XCircle, Crown, UserCheck } from 'lucide-react';
import adminUsuariosService from '../../services/adminUsuarios.js';
import { seccionService } from '../../services/maestros.js';
import { useAuth } from '../../context/AuthContext.jsx';

const UsuariosAdminList = () => {
    const { user, isAdmin, canEdit } = useAuth();
    
    // Estados principales
    const [usuarios, setUsuarios] = useState([]);
    const [secciones, setSecciones] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    
    // Estados de notificaciones
    const [notification, setNotification] = useState(null);
    
    // Estados de UI
    const [showForm, setShowForm] = useState(false);
    const [showJerarquia, setShowJerarquia] = useState(false);
    const [usuarioEditar, setUsuarioEditar] = useState(null);
    const [confirmDelete, setConfirmDelete] = useState(null);
    
    // Estados de filtros
    const [filtros, setFiltros] = useState({
        activosOnly: true,
        role: '',
        seccionId: '',
        supervisorId: '',
        search: ''
    });
    
    const [showFiltros, setShowFiltros] = useState(false);

    // ==================== EFFECTS ====================

    useEffect(() => {
        cargarDatos();
    }, [filtros]);

    // Auto-hide notification after 5 seconds
    useEffect(() => {
        if (notification) {
            const timer = setTimeout(() => {
                setNotification(null);
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [notification]);

    // ==================== UTILS ====================

    const showNotification = (message, type = 'success') => {
        setNotification({ message, type });
    };

    const cargarDatos = async () => {
        try {
            setLoading(true);
            setError('');

            const [usuariosData, seccionesData] = await Promise.all([
                adminUsuariosService.getUsuarios(filtros),
                seccionService.getAll()
            ]);

            setUsuarios(usuariosData);
            setSecciones(seccionesData);
        } catch (err) {
            console.error('Error cargando datos:', err);
            setError(err.response?.data?.detail || 'Error cargando usuarios');
        } finally {
            setLoading(false);
        }
    };

    // ==================== HANDLERS ====================

    const handleCreate = () => {
        setUsuarioEditar(null);
        setShowForm(true);
    };

    const handleEdit = (usuario) => {
        setUsuarioEditar(usuario);
        setShowForm(true);
    };

    const handleDelete = async (usuario) => {
        if (!confirmDelete) {
            setConfirmDelete(usuario);
            return;
        }

        try {
            await adminUsuariosService.eliminar(usuario.id, false);
            showNotification(`Usuario ${usuario.username} desactivado`, 'success');
            cargarDatos();
        } catch (err) {
            showNotification(err.response?.data?.detail || 'Error eliminando usuario', 'error');
        } finally {
            setConfirmDelete(null);
        }
    };

    const handleToggleActivo = async (usuario) => {
        try {
            await adminUsuariosService.toggleActivo(usuario.id, !usuario.is_active);
            Toast.success(`Usuario ${usuario.is_active ? 'desactivado' : 'activado'}`);
            cargarDatos();
        } catch (err) {
            Toast.error(err.response?.data?.detail || 'Error cambiando estado');
        }
    };

    const handleResetPassword = async (usuario) => {
        const nuevaPassword = prompt(`Nueva contraseña para ${usuario.username}:`);
        if (!nuevaPassword || nuevaPassword.length < 6) {
            Toast.error('Contraseña debe tener al menos 6 caracteres');
            return;
        }

        try {
            await adminUsuariosService.resetPassword(usuario.id, nuevaPassword);
            Toast.success(`Contraseña reseteada para ${usuario.username}`);
        } catch (err) {
            Toast.error(err.response?.data?.detail || 'Error reseteando contraseña');
        }
    };

    const handleFiltroChange = (campo, valor) => {
        setFiltros(prev => ({
            ...prev,
            [campo]: valor
        }));
    };

    const clearFiltros = () => {
        setFiltros({
            activosOnly: true,
            role: '',
            seccionId: '',
            supervisorId: '',
            search: ''
        });
    };

    // ==================== UTILS ====================

    const getRoleIcon = (role) => {
        const icons = {
            admin: Crown,
            director: UserCheck,
            jefe_seccion: Users,
            redactor: Edit,
            viewer: Eye
        };
        return icons[role] || Users;
    };

    const getRoleBadgeColor = (role) => {
        const colors = {
            admin: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
            director: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
            jefe_seccion: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
            redactor: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
            viewer: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
        };
        return colors[role] || colors.viewer;
    };

    const getSupervizorInfo = (usuario) => {
        if (!usuario.supervisor_id) return null;
        const supervisor = usuarios.find(u => u.id === usuario.supervisor_id);
        return supervisor ? supervisor.nombre_completo : 'Supervisor no encontrado';
    };

    const canManageUser = (targetUser) => {
        if (user.role === 'admin') return true;
        if (user.role === 'director' && targetUser.role !== 'admin') return true;
        if (user.role === 'jefe_seccion' && targetUser.supervisor_id === user.id) return true;
        return targetUser.id === user.id;
    };

    // ==================== RENDER ====================

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <Users className="h-8 w-8" />
                        <div>
                            <h1 className="text-2xl font-bold">Administración de Usuarios</h1>
                            <p className="text-blue-100">
                                Gestión completa de usuarios y jerarquía editorial
                            </p>
                        </div>
                    </div>
                    <div className="flex space-x-3">
                        <button
                            onClick={() => setShowJerarquia(true)}
                            className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                        >
                            <Users className="h-4 w-4" />
                            <span>Ver Jerarquía</span>
                        </button>
                        {canEdit() && (
                            <button
                                onClick={handleCreate}
                                className="bg-white text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg flex items-center space-x-2 font-medium transition-colors"
                            >
                                <Plus className="h-4 w-4" />
                                <span>Nuevo Usuario</span>
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Filtros */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Filtros y Búsqueda
                    </h3>
                    <button
                        onClick={() => setShowFiltros(!showFiltros)}
                        className="text-blue-600 hover:text-blue-800 flex items-center space-x-1"
                    >
                        <Filter className="h-4 w-4" />
                        <span>{showFiltros ? 'Ocultar' : 'Mostrar'} Filtros</span>
                    </button>
                </div>

                {/* Búsqueda rápida */}
                <div className="mb-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Buscar por nombre, email o username..."
                            value={filtros.search}
                            onChange={(e) => handleFiltroChange('search', e.target.value)}
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        />
                    </div>
                </div>

                {/* Filtros avanzados */}
                {showFiltros && (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        {/* Estado activo */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Estado
                            </label>
                            <select
                                value={filtros.activosOnly ? 'true' : 'false'}
                                onChange={(e) => handleFiltroChange('activosOnly', e.target.value === 'true')}
                                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="true">Solo Activos</option>
                                <option value="false">Todos</option>
                            </select>
                        </div>

                        {/* Role */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Role
                            </label>
                            <select
                                value={filtros.role}
                                onChange={(e) => handleFiltroChange('role', e.target.value)}
                                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="">Todos los roles</option>
                                {Object.entries(adminUsuariosService.ROLES).map(([role, info]) => (
                                    <option key={role} value={role}>{info.label}</option>
                                ))}
                            </select>
                        </div>

                        {/* Sección */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Sección
                            </label>
                            <select
                                value={filtros.seccionId}
                                onChange={(e) => handleFiltroChange('seccionId', e.target.value)}
                                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="">Todas las secciones</option>
                                {secciones.map(seccion => (
                                    <option key={seccion.id} value={seccion.id}>
                                        {seccion.nombre}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Supervisor */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Supervisor
                            </label>
                            <select
                                value={filtros.supervisorId}
                                onChange={(e) => handleFiltroChange('supervisorId', e.target.value)}
                                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                <option value="">Todos los supervisores</option>
                                {usuarios.filter(u => u.puede_supervisar).map(supervisor => (
                                    <option key={supervisor.id} value={supervisor.id}>
                                        {supervisor.nombre_completo}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                )}

                {/* Botón limpiar filtros */}
                {(filtros.search || filtros.role || filtros.seccionId || filtros.supervisorId || !filtros.activosOnly) && (
                    <div className="mt-4 flex justify-end">
                        <button
                            onClick={clearFiltros}
                            className="text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 text-sm flex items-center space-x-1"
                        >
                            <XCircle className="h-4 w-4" />
                            <span>Limpiar Filtros</span>
                        </button>
                    </div>
                )}
            </div>

            {/* Lista simplificada de usuarios */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
                <div className="p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Usuarios ({usuarios.length})
                    </h3>
                    
                    {usuarios.length === 0 ? (
                        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                            <Users className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                            <p>No se encontraron usuarios con los filtros aplicados</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {usuarios.map((usuario) => {
                                const supervisor = getSupervizorInfo(usuario);
                                
                                return (
                                    <div key={usuario.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center space-x-4">
                                                <div className="h-10 w-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold">
                                                    {usuario.nombre_completo ? usuario.nombre_completo.charAt(0).toUpperCase() : usuario.username.charAt(0).toUpperCase()}
                                                </div>
                                                
                                                <div>
                                                    <div className="flex items-center space-x-2">
                                                        <h4 className="font-medium text-gray-900 dark:text-white">
                                                            {usuario.nombre_completo || usuario.username}
                                                        </h4>
                                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleBadgeColor(usuario.role)}`}>
                                                            {adminUsuariosService.getRoleInfo(usuario.role).label}
                                                        </span>
                                                        {usuario.is_active ? (
                                                            <CheckCircle className="h-4 w-4 text-green-500" />
                                                        ) : (
                                                            <XCircle className="h-4 w-4 text-red-500" />
                                                        )}
                                                    </div>
                                                    <div className="text-sm text-gray-500 dark:text-gray-400">
                                                        {usuario.email} • @{usuario.username}
                                                    </div>
                                                    {supervisor && (
                                                        <div className="text-xs text-gray-400">
                                                            Supervisor: {supervisor}
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                            
                                            <div className="flex items-center space-x-2">
                                                <div className="text-right text-sm text-gray-500 dark:text-gray-400 mr-4">
                                                    <div>Noticias: {usuario.noticias_count}</div>
                                                    <div>Secciones: {usuario.secciones_nombres?.length || 0}</div>
                                                </div>
                                                
                                                {canManageUser(usuario) && (
                                                    <div className="flex items-center space-x-2">
                                                        <button
                                                            onClick={() => handleEdit(usuario)}
                                                            className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300"
                                                            title="Editar usuario"
                                                        >
                                                            <Edit className="h-4 w-4" />
                                                        </button>
                                                        
                                                        <button
                                                            onClick={() => handleResetPassword(usuario)}
                                                            className="text-yellow-600 hover:text-yellow-900 dark:text-yellow-400 dark:hover:text-yellow-300"
                                                            title="Resetear contraseña"
                                                        >
                                                            <Key className="h-4 w-4" />
                                                        </button>

                                                        <button
                                                            onClick={() => handleToggleActivo(usuario)}
                                                            className={`${usuario.is_active ? 'text-red-600 hover:text-red-900' : 'text-green-600 hover:text-green-900'}`}
                                                            title={usuario.is_active ? 'Desactivar' : 'Activar'}
                                                        >
                                                            {usuario.is_active ? <XCircle className="h-4 w-4" /> : <CheckCircle className="h-4 w-4" />}
                                                        </button>

                                                        {isAdmin() && usuario.role !== 'admin' && (
                                                            <button
                                                                onClick={() => handleDelete(usuario)}
                                                                className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                                                                title="Eliminar usuario"
                                                            >
                                                                <Trash2 className="h-4 w-4" />
                                                            </button>
                                                        )}
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            </div>

            {/* Modal de confirmación de eliminación */}
            {confirmDelete && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
                        <div className="flex items-center space-x-3 mb-4">
                            <AlertTriangle className="h-8 w-8 text-red-500" />
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                                Confirmar Eliminación
                            </h3>
                        </div>
                        
                        <p className="text-gray-600 dark:text-gray-400 mb-6">
                            ¿Está seguro que desea desactivar al usuario <strong>{confirmDelete.username}</strong>?
                            Esta acción se puede revertir posteriormente.
                        </p>
                        
                        <div className="flex space-x-3 justify-end">
                            <button
                                onClick={() => setConfirmDelete(null)}
                                className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={() => handleDelete(confirmDelete)}
                                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                            >
                                Desactivar Usuario
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {error && (
                <div className="fixed bottom-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded z-50">
                    {error}
                </div>
            )}
        </div>
    );
};

export default UsuariosAdminList;