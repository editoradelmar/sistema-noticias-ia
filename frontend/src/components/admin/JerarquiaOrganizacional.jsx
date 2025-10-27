/**
 * Vista de Árbol Organizacional
 * Muestra la jerarquía editorial completa en formato de árbol
 */
import React, { useState, useEffect } from 'react';
import { 
    Users, ChevronDown, ChevronRight, Crown, UserCheck, Edit, Eye,
    Briefcase, Target, Calendar, Plus, Trash2, RotateCcw
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext.jsx';
import adminUsuariosService from '../../services/adminUsuarios.js';
import Toast from '../Toast.jsx';

const JerarquiaOrganizacional = ({ onEditUser, onCreateUser }) => {
    const { user, isAdmin } = useAuth();
    
    const [arbolJerarquico, setArbolJerarquico] = useState([]);
    const [todosUsuarios, setTodosUsuarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [nodosExpandidos, setNodosExpandidos] = useState(new Set());
    const [selectedUserId, setSelectedUserId] = useState(null);

    // ==================== EFFECTS ====================

    useEffect(() => {
        cargarJerarquia();
    }, []);

    const cargarJerarquia = async () => {
        try {
            setLoading(true);
            setError('');
            
            // Usar endpoint disponible en lugar del servicio admin
            const token = localStorage.getItem('token');
            const response = await fetch('/api/auth/users', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (!response.ok) {
                throw new Error('Error cargando usuarios');
            }
            
            const usuarios = await response.json();
            setTodosUsuarios(usuarios);
            
            // Construir árbol jerárquico
            const arbol = adminUsuariosService.construirArbol(usuarios);
            setArbolJerarquico(arbol);
            
            // Expandir todos los nodos por defecto
            const todosIds = new Set(usuarios.map(u => u.id));
            setNodosExpandidos(todosIds);
            
        } catch (err) {
            console.error('Error cargando jerarquía:', err);
            setError('Error cargando la estructura organizacional');
        } finally {
            setLoading(false);
        }
    };

    // ==================== HANDLERS ====================

    const toggleNodo = (userId) => {
        const nuevosExpandidos = new Set(nodosExpandidos);
        if (nuevosExpandidos.has(userId)) {
            nuevosExpandidos.delete(userId);
        } else {
            nuevosExpandidos.add(userId);
        }
        setNodosExpandidos(nuevosExpandidos);
    };

    const expandirTodos = () => {
        const todosIds = new Set(todosUsuarios.map(u => u.id));
        setNodosExpandidos(todosIds);
    };

    const contraerTodos = () => {
        setNodosExpandidos(new Set());
    };

    const handleSelectUser = (userId) => {
        setSelectedUserId(selectedUserId === userId ? null : userId);
    };

    const handleCambiarSupervisor = async (usuarioId, nuevoSupervisorId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/auth/users/${usuarioId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ supervisor_id: nuevoSupervisorId })
            });
            
            if (!response.ok) {
                throw new Error('Error actualizando supervisor');
            }
            
            Toast.success('Supervisor actualizado correctamente');
            cargarJerarquia(); // Recargar para mostrar cambios
        } catch (err) {
            Toast.error(err.message || 'Error cambiando supervisor');
        }
    };

    // ==================== RENDER UTILS ====================

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

    const getRoleColor = (role) => {
        const colors = {
            admin: 'text-purple-600 bg-purple-100 dark:bg-purple-900/20 dark:text-purple-400',
            director: 'text-blue-600 bg-blue-100 dark:bg-blue-900/20 dark:text-blue-400',
            jefe_seccion: 'text-green-600 bg-green-100 dark:bg-green-900/20 dark:text-green-400',
            redactor: 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20 dark:text-yellow-400',
            viewer: 'text-gray-600 bg-gray-100 dark:bg-gray-900/20 dark:text-gray-400'
        };
        return colors[role] || colors.viewer;
    };

    const canManageUser = (targetUser) => {
        if (user.role === 'admin') return true;
        if (user.role === 'director' && targetUser.role !== 'admin') return true;
        if (user.role === 'jefe_seccion' && targetUser.supervisor_id === user.id) return true;
        return targetUser.id === user.id;
    };

    // ==================== RENDER COMPONENTS ====================

    const UsuarioNodo = ({ usuario, nivel = 0, esUltimo = false, prefijo = '' }) => {
        const RoleIcon = getRoleIcon(usuario.role);
        const tieneSubordinados = usuario.subordinados && usuario.subordinados.length > 0;
        const estaExpandido = nodosExpandidos.has(usuario.id);
        const estaSeleccionado = selectedUserId === usuario.id;
        
        return (
            <div className="relative">
                {/* Líneas de conexión */}
                {nivel > 0 && (
                    <div className="absolute left-4 top-0 bottom-0 w-px bg-gray-300 dark:bg-gray-600"></div>
                )}
                
                {/* Nodo del usuario */}
                <div className={`relative flex items-center p-3 rounded-lg mb-2 transition-all ${
                    estaSeleccionado 
                        ? 'bg-blue-50 dark:bg-blue-900/30 border-2 border-blue-300 dark:border-blue-600' 
                        : 'hover:bg-gray-50 dark:hover:bg-gray-700 border border-transparent'
                }`}>
                    {/* Línea horizontal */}
                    {nivel > 0 && (
                        <div className="absolute left-4 top-1/2 w-4 h-px bg-gray-300 dark:bg-gray-600"></div>
                    )}
                    
                    {/* Indentación */}
                    <div style={{ marginLeft: `${nivel * 24}px` }} className="flex items-center space-x-3 flex-1">
                        {/* Botón de expansión */}
                        {tieneSubordinados ? (
                            <button
                                onClick={() => toggleNodo(usuario.id)}
                                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
                            >
                                {estaExpandido ? (
                                    <ChevronDown className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                                ) : (
                                    <ChevronRight className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                                )}
                            </button>
                        ) : (
                            <div className="w-6"></div>
                        )}
                        
                        {/* Avatar y rol */}
                        <div className={`p-2 rounded-full ${getRoleColor(usuario.role)}`}>
                            <RoleIcon className="h-4 w-4" />
                        </div>
                        
                        {/* Información del usuario */}
                        <div 
                            className="flex-1 cursor-pointer" 
                            onClick={() => handleSelectUser(usuario.id)}
                        >
                            <div className="flex items-center justify-between">
                                <div>
                                    <div className="font-medium text-gray-900 dark:text-white">
                                        {usuario.nombre_completo || usuario.username}
                                    </div>
                                    <div className="text-sm text-gray-500 dark:text-gray-400">
                                        {usuario.email} • {adminUsuariosService.getRoleInfo(usuario.role).label}
                                    </div>
                                    {usuario.secciones_nombres && usuario.secciones_nombres.length > 0 && (
                                        <div className="flex flex-wrap gap-1 mt-1">
                                            {usuario.secciones_nombres.slice(0, 3).map((seccion, index) => (
                                                <span 
                                                    key={index}
                                                    className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300"
                                                >
                                                    {seccion}
                                                </span>
                                            ))}
                                            {usuario.secciones_nombres.length > 3 && (
                                                <span className="text-xs text-gray-500">
                                                    +{usuario.secciones_nombres.length - 3} más
                                                </span>
                                            )}
                                        </div>
                                    )}
                                </div>
                                
                                <div className="flex items-center space-x-2">
                                    <div className="text-right text-xs text-gray-500 dark:text-gray-400">
                                        <div>ID: {usuario.id}</div>
                                        {tieneSubordinados && (
                                            <div className="text-blue-600 dark:text-blue-400">
                                                {usuario.subordinados.length} subordinado{usuario.subordinados.length !== 1 ? 's' : ''}
                                            </div>
                                        )}
                                    </div>
                                    
                                    {/* Indicador de estado */}
                                    <div className={`w-3 h-3 rounded-full ${
                                        usuario.is_active ? 'bg-green-500' : 'bg-red-500'
                                    }`} title={usuario.is_active ? 'Activo' : 'Inactivo'}>
                                    </div>
                                </div>
                            </div>
                            
                            {/* Panel de detalles expandido */}
                            {estaSeleccionado && (
                                <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                        <div>
                                            <div className="font-medium text-gray-700 dark:text-gray-300">Límite Tokens</div>
                                            <div className="text-gray-600 dark:text-gray-400 flex items-center">
                                                <Target className="h-3 w-3 mr-1" />
                                                {usuario.limite_tokens_diario?.toLocaleString() || '10,000'}/día
                                            </div>
                                        </div>
                                        
                                        {usuario.fecha_expiracion_acceso && (
                                            <div>
                                                <div className="font-medium text-gray-700 dark:text-gray-300">Expira</div>
                                                <div className="text-gray-600 dark:text-gray-400 flex items-center">
                                                    <Calendar className="h-3 w-3 mr-1" />
                                                    {new Date(usuario.fecha_expiracion_acceso).toLocaleDateString()}
                                                </div>
                                            </div>
                                        )}
                                        
                                        <div>
                                            <div className="font-medium text-gray-700 dark:text-gray-300">Noticias</div>
                                            <div className="text-gray-600 dark:text-gray-400 flex items-center">
                                                <Briefcase className="h-3 w-3 mr-1" />
                                                {usuario.noticias_count || 0} creadas
                                            </div>
                                        </div>
                                    </div>
                                    
                                    {/* Acciones */}
                                    {canManageUser(usuario) && (
                                        <div className="flex items-center space-x-2 mt-3">
                                            <button
                                                onClick={() => onEditUser && onEditUser(usuario)}
                                                className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 text-sm flex items-center space-x-1"
                                            >
                                                <Edit className="h-3 w-3" />
                                                <span>Editar</span>
                                            </button>
                                            
                                            {usuario.supervisor_id && (
                                                <button
                                                    onClick={() => handleCambiarSupervisor(usuario.id, null)}
                                                    className="text-orange-600 hover:text-orange-800 dark:text-orange-400 dark:hover:text-orange-300 text-sm flex items-center space-x-1"
                                                >
                                                    <RotateCcw className="h-3 w-3" />
                                                    <span>Quitar supervisor</span>
                                                </button>
                                            )}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
                
                {/* Subordinados */}
                {tieneSubordinados && estaExpandido && (
                    <div className="ml-6">
                        {usuario.subordinados.map((subordinado, index) => (
                            <UsuarioNodo 
                                key={subordinado.id}
                                usuario={subordinado}
                                nivel={nivel + 1}
                                esUltimo={index === usuario.subordinados.length - 1}
                                prefijo={prefijo + (esUltimo ? '  ' : '│ ')}
                            />
                        ))}
                    </div>
                )}
            </div>
        );
    };

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
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
                <div className="text-red-800 dark:text-red-200">
                    <strong>Error:</strong> {error}
                </div>
                <button 
                    onClick={cargarJerarquia}
                    className="mt-2 text-red-600 hover:text-red-800 text-sm underline"
                >
                    Reintentar
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="bg-gradient-to-r from-green-600 to-blue-600 rounded-lg p-6 text-white">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <Users className="h-8 w-8" />
                        <div>
                            <h1 className="text-2xl font-bold">Jerarquía Organizacional</h1>
                            <p className="text-green-100">
                                Estructura editorial completa - {todosUsuarios.length} usuarios
                            </p>
                        </div>
                    </div>
                    
                    <div className="flex space-x-3">
                        <button
                            onClick={contraerTodos}
                            className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm transition-colors"
                        >
                            Contraer Todo
                        </button>
                        <button
                            onClick={expandirTodos}
                            className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm transition-colors"
                        >
                            Expandir Todo
                        </button>
                        {isAdmin() && onCreateUser && (
                            <button
                                onClick={onCreateUser}
                                className="bg-white text-green-600 hover:bg-green-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center space-x-2"
                            >
                                <Plus className="h-4 w-4" />
                                <span>Agregar Usuario</span>
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Estadísticas rápidas */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {Object.entries(adminUsuariosService.ROLES).map(([role, info]) => {
                    const count = todosUsuarios.filter(u => u.role === role).length;
                    return (
                        <div key={role} className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
                            <div className="flex items-center space-x-3">
                                <div className={`p-2 rounded-lg ${getRoleColor(role)}`}>
                                    {React.createElement(getRoleIcon(role), { className: "h-5 w-5" })}
                                </div>
                                <div>
                                    <div className="text-2xl font-bold text-gray-900 dark:text-white">{count}</div>
                                    <div className="text-sm text-gray-600 dark:text-gray-400">{info.label}s</div>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Árbol jerárquico */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
                <div className="p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Estructura Jerárquica
                    </h3>
                    
                    {arbolJerarquico.length === 0 ? (
                        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                            <Users className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                            <p>No se encontró estructura jerárquica</p>
                            <p className="text-sm mt-2">Los usuarios sin supervisor aparecen como raíz</p>
                        </div>
                    ) : (
                        <div className="space-y-2">
                            {arbolJerarquico.map(usuario => (
                                <UsuarioNodo key={usuario.id} usuario={usuario} />
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Nota informativa */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <div className="flex items-start space-x-3">
                    <Users className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="text-blue-800 dark:text-blue-200 text-sm">
                        <strong>Navegación:</strong>
                        <ul className="mt-2 space-y-1 list-disc list-inside">
                            <li>Click en un usuario para ver sus detalles completos</li>
                            <li>Click en las flechas para expandir/contraer subordinados</li>
                            <li>Los círculos de color indican el estado: verde = activo, rojo = inactivo</li>
                            <li>Los badges muestran las secciones asignadas a cada usuario</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default JerarquiaOrganizacional;