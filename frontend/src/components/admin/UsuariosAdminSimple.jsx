/**
 * Administrador de Usuarios Completo con Jerarquía Editorial
 * Versión actualizada con funcionalidades avanzadas
 */
import React, { useState, useEffect } from 'react';
import { 
    Users, Plus, Edit, Trash2, Settings, Search, Filter, 
    TreePine, UserPlus, Eye, Crown, Target
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext.jsx';
import UsuarioAdminForm from './UsuarioAdminForm.jsx';
import JerarquiaOrganizacional from './JerarquiaOrganizacional.jsx';

const UsuariosAdminCompleto = ({ onClose }) => {
    const { user, isAdmin } = useAuth();
    const [usuarios, setUsuarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    
    // Estados de vistas
    const [vistaActual, setVistaActual] = useState('lista'); // 'lista', 'jerarquia', 'form'
    const [usuarioEditar, setUsuarioEditar] = useState(null);
    const [filtros, setFiltros] = useState({
        search: '',
        role: '',
        activos: true
    });

    useEffect(() => {
        cargarUsuarios();
    }, [filtros]);

    const cargarUsuarios = async () => {
        try {
            setLoading(true);
            setError('');
            
            // Usar la API básica de auth que ya sabemos que funciona
            const response = await fetch('/api/auth/users', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Error cargando usuarios');
            }
            
            let data = await response.json();
            
            // Aplicar filtros
            if (filtros.search) {
                const search = filtros.search.toLowerCase();
                data = data.filter(u => 
                    u.nombre_completo?.toLowerCase().includes(search) ||
                    u.username.toLowerCase().includes(search) ||
                    u.email.toLowerCase().includes(search)
                );
            }
            
            if (filtros.role) {
                data = data.filter(u => u.role === filtros.role);
            }
            
            if (filtros.activos) {
                data = data.filter(u => u.is_active);
            }
            
            setUsuarios(data);
        } catch (err) {
            console.error('Error:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateUser = () => {
        setUsuarioEditar(null);
        setVistaActual('form');
    };

    const handleEditUser = (usuario) => {
        setUsuarioEditar(usuario);
        setVistaActual('form');
    };

    const handleFormSave = (usuarioGuardado) => {
        cargarUsuarios(); // Recargar lista
        setVistaActual('lista'); // Volver a la lista
        setUsuarioEditar(null);
    };

    const handleFormClose = () => {
        setVistaActual('lista');
        setUsuarioEditar(null);
    };

    const handleFiltroChange = (campo, valor) => {
        setFiltros(prev => ({
            ...prev,
            [campo]: valor
        }));
    };

    // ==================== RENDER FUNCIONES ====================

    const renderNavigacion = () => (
        <div className="flex items-center space-x-4 mb-6">
            <button
                onClick={() => setVistaActual('lista')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                    vistaActual === 'lista'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
            >
                <Users className="h-4 w-4" />
                <span>Lista de Usuarios</span>
            </button>
            
            <button
                onClick={() => setVistaActual('jerarquia')}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                    vistaActual === 'jerarquia'
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
            >
                <TreePine className="h-4 w-4" />
                <span>Jerarquía</span>
            </button>
            
            {isAdmin() && (
                <button
                    onClick={handleCreateUser}
                    className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors ml-auto"
                >
                    <UserPlus className="h-4 w-4" />
                    <span>Crear Usuario</span>
                </button>
            )}
        </div>
    );

    const renderFiltros = () => (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Buscar
                    </label>
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Nombre, email o username..."
                            value={filtros.search}
                            onChange={(e) => handleFiltroChange('search', e.target.value)}
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        />
                    </div>
                </div>
                
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
                        <option value="admin">Administrador</option>
                        <option value="director">Director</option>
                        <option value="jefe_seccion">Jefe de Sección</option>
                        <option value="redactor">Redactor</option>
                        <option value="viewer">Visor</option>
                    </select>
                </div>
                
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Estado
                    </label>
                    <label className="flex items-center space-x-2 p-2">
                        <input
                            type="checkbox"
                            checked={filtros.activos}
                            onChange={(e) => handleFiltroChange('activos', e.target.checked)}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="text-sm text-gray-700 dark:text-gray-300">Solo activos</span>
                    </label>
                </div>
            </div>
        </div>
    );

    const renderListaUsuarios = () => (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Usuarios Registrados ({usuarios.length})
                </h3>
                
                {usuarios.length === 0 ? (
                    <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                        <Users className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                        <p>No se encontraron usuarios con los filtros aplicados</p>
                    </div>
                ) : (
                    <div className="max-h-96 overflow-y-auto space-y-4 pr-2">
                        {usuarios.map((usuario) => (
                            <div 
                                key={usuario.id} 
                                className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                            >
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center space-x-4">
                                        <div className="h-10 w-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold flex-shrink-0">
                                            {(usuario.nombre_completo || usuario.username).charAt(0).toUpperCase()}
                                        </div>
                                        
                                        <div className="min-w-0 flex-1">
                                            <h4 className="font-medium text-gray-900 dark:text-white truncate">
                                                {usuario.nombre_completo || usuario.username}
                                            </h4>
                                            <div className="text-sm text-gray-500 dark:text-gray-400 truncate">
                                                {usuario.email} • @{usuario.username}
                                            </div>
                                            <div className="flex items-center space-x-2 mt-1 flex-wrap">
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                                    usuario.role === 'admin' 
                                                        ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300'
                                                        : usuario.role === 'director'
                                                        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                                                        : usuario.role === 'jefe_seccion'
                                                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                                                        : usuario.role === 'redactor'
                                                        ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
                                                        : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
                                                }`}>
                                                    {usuario.role === 'admin' && <Crown className="h-3 w-3 mr-1" />}
                                                    {usuario.role}
                                                </span>
                                                {usuario.is_active ? (
                                                    <span className="text-green-500 text-sm">● Activo</span>
                                                ) : (
                                                    <span className="text-red-500 text-sm">● Inactivo</span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div className="flex items-center space-x-4 flex-shrink-0 ml-4">
                                        <div className="text-right text-sm text-gray-500 dark:text-gray-400">
                                            <div>ID: {usuario.id}</div>
                                            {usuario.last_login && (
                                                <div>
                                                    Último: {new Date(usuario.last_login).toLocaleDateString()}
                                                </div>
                                            )}
                                        </div>
                                        
                                        {isAdmin() && (
                                            <button
                                                onClick={() => handleEditUser(usuario)}
                                                className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 p-2 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20"
                                                title="Editar usuario"
                                            >
                                                <Edit className="h-4 w-4" />
                                            </button>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );

    // ==================== RENDER PRINCIPAL ====================

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                <div className="text-red-800 dark:text-red-200">
                    <strong>Error:</strong> {error}
                </div>
                <button 
                    onClick={cargarUsuarios}
                    className="mt-2 text-red-600 hover:text-red-800 text-sm underline"
                >
                    Reintentar
                </button>
            </div>
        );
    }

    // Renderizar formulario
    if (vistaActual === 'form') {
        return (
            <UsuarioAdminForm
                usuario={usuarioEditar}
                onSave={handleFormSave}
                onClose={handleFormClose}
            />
        );
    }

    // Renderizar jerarquía
    if (vistaActual === 'jerarquia') {
        return (
            <div>
                {renderNavigacion()}
                <JerarquiaOrganizacional
                    onEditUser={handleEditUser}
                    onCreateUser={handleCreateUser}
                />
            </div>
        );
    }

    // Renderizar lista (vista por defecto)
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
                                Gestión completa con jerarquía editorial
                            </p>
                        </div>
                    </div>
                    <div className="text-right">
                        <p className="text-sm text-blue-100">Usuario actual:</p>
                        <p className="font-semibold">{user?.nombre_completo || user?.username}</p>
                        <p className="text-xs text-blue-200">Role: {user?.role}</p>
                    </div>
                </div>
            </div>

            {/* Navegación */}
            {renderNavigacion()}

            {/* Filtros */}
            {renderFiltros()}

            {/* Lista de usuarios */}
            {renderListaUsuarios()}

            {/* Estado del sistema */}
            <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 dark:text-white mb-3">Estado del Sistema</h4>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
                    <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{usuarios.length}</div>
                        <div className="text-gray-600 dark:text-gray-400">Total Usuarios</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">
                            {usuarios.filter(u => u.is_active).length}
                        </div>
                        <div className="text-gray-600 dark:text-gray-400">Activos</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">
                            {usuarios.filter(u => u.role === 'admin').length}
                        </div>
                        <div className="text-gray-600 dark:text-gray-400">Administradores</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">
                            {usuarios.filter(u => u.role === 'redactor').length}
                        </div>
                        <div className="text-gray-600 dark:text-gray-400">Redactores</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UsuariosAdminCompleto;