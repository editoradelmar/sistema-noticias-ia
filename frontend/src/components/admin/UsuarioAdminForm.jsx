/**
 * Formulario de Edición de Usuarios con Jerarquía Editorial
 * Permite gestionar roles, supervisores, secciones asignadas y límites
 */
import React, { useState, useEffect } from 'react';
import { 
    Users, Save, X, AlertCircle, Eye, EyeOff, Crown, UserCheck, 
    Edit, Calendar, Shield, Settings, Target, Briefcase 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext.jsx';
import { seccionService } from '../../services/maestros.js';
import Toast from '../Toast.jsx';

// Implementaciones locales temporales para roles y validaciones
const localRoles = {
    admin: { label: 'Administrador Sistema', nivel: 1, puede_supervisar: true },
    director: { label: 'Director de Redacción', nivel: 2, puede_supervisar: true },
    jefe_seccion: { label: 'Jefe de Sección', nivel: 3, puede_supervisar: true },
    redactor: { label: 'Redactor', nivel: 4, puede_supervisar: false },
    viewer: { label: 'Visor', nivel: 5, puede_supervisar: false }
};

const getRoleInfo = (role) => {
    return localRoles[role] || { label: role, nivel: 99, puede_supervisar: false };
    //return localRoles[role] || { label: role, puede_supervisar: false };
};

const getPosiblesSupervisores = (roleUsuario, todosUsuarios) => {
    const jerarquia = {
        'redactor': ['jefe_seccion', 'director', 'admin'],
        'jefe_seccion': ['director', 'admin'],
        'director': ['admin'],
        'admin': [],
        'viewer': ['jefe_seccion', 'director', 'admin']
    };

    const rolesValidos = jerarquia[roleUsuario] || [];
    
    return todosUsuarios.filter(usuario => 
        rolesValidos.includes(usuario.role) && usuario.is_active
    );
};

const UsuarioAdminForm = ({ usuario, onSave, onClose }) => {
    const { user, isAdmin } = useAuth();
    
    // Implementaciones temporales de funciones de adminUsuarios
    const adminUsuariosServiceTemp = {
        ROLES: {
            admin: { label: 'Administrador Sistema', nivel: 1, puede_supervisar: true },
            director: { label: 'Director de Redacción', nivel: 2, puede_supervisar: true },
            jefe_seccion: { label: 'Jefe de Sección', nivel: 3, puede_supervisar: true },
            redactor: { label: 'Redactor', nivel: 4, puede_supervisar: false },
            viewer: { label: 'Visor', nivel: 5, puede_supervisar: false }
        },
        getRoleInfo: (role) => {
            return adminUsuariosServiceTemp.ROLES[role] || { label: role, nivel: 99, puede_supervisar: false };
            //return adminUsuariosServiceTemp.ROLES[role] || { label: role, puede_supervisar: false };
        },
        getPosiblesSupervisores: (roleUsuario, todosUsuarios) => {
            const jerarquia = {
                'redactor': ['jefe_seccion', 'director', 'admin'],
                'jefe_seccion': ['director', 'admin'],
                'director': ['admin'],
                'admin': [],
                'viewer': ['jefe_seccion', 'director', 'admin']
            };
            const rolesValidos = jerarquia[roleUsuario] || [];
            return todosUsuarios.filter(usuario => 
                rolesValidos.includes(usuario.role) && usuario.is_active
            );
        }
    };
    
    // Estados del formulario
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        nombre_completo: '',
        role: 'redactor',
        supervisor_id: null,
        secciones_asignadas: [],
        limite_tokens_diario: 10000,
        fecha_expiracion_acceso: '',
        is_active: true,
        password: '' // Solo para nuevos usuarios
    });
    
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [validationErrors, setValidationErrors] = useState({});
    
    // Datos auxiliares
    const [secciones, setSecciones] = useState([]);
    const [posiblesSupervisores, setPosiblesSupervisores] = useState([]);
    const [todosUsuarios, setTodosUsuarios] = useState([]);

    // ==================== EFFECTS ====================

    useEffect(() => {
        cargarDatosIniciales();
        if (usuario) {
            cargarDatosUsuario();
        }
    }, [usuario]);

    useEffect(() => {
        // Actualizar posibles supervisores cuando cambia el role
        actualizarPosiblesSupervisores();
    }, [formData.role, todosUsuarios]);

    const cargarDatosIniciales = async () => {
        try {
            const [seccionesData, usuariosData] = await Promise.all([
                seccionService.getAll(),
                fetch('/api/auth/users', {
                    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
                }).then(res => res.json())
            ]);
            
            setSecciones(seccionesData);
            setTodosUsuarios(usuariosData);
        } catch (err) {
            console.error('Error cargando datos:', err);
            setError('Error cargando datos del formulario');
        }
    };

    const cargarDatosUsuario = () => {
        if (!usuario) return;
        
        setFormData({
            email: usuario.email || '',
            username: usuario.username || '',
            nombre_completo: usuario.nombre_completo || '',
            role: usuario.role || 'redactor',
            supervisor_id: usuario.supervisor_id || null,
            secciones_asignadas: usuario.secciones_asignadas || [],
            limite_tokens_diario: usuario.limite_tokens_diario || 10000,
            fecha_expiracion_acceso: usuario.fecha_expiracion_acceso || '',
            is_active: usuario.is_active !== undefined ? usuario.is_active : true,
            password: '' // Siempre vacío para edición
        });
    };

    const actualizarPosiblesSupervisores = () => {
        if (!formData.role || !todosUsuarios.length) return;
        
        const supervisores = getPosiblesSupervisores(formData.role, todosUsuarios);
        
        // Excluir al usuario actual de la lista de supervisores
        const supervisoresFiltrados = usuario 
            ? supervisores.filter(s => s.id !== usuario.id)
            : supervisores;
        
        setPosiblesSupervisores(supervisoresFiltrados);
        
        // Si el supervisor actual ya no es válido, limpiarlo
        if (formData.supervisor_id) {
            const supervisorValido = supervisoresFiltrados.find(s => s.id === formData.supervisor_id);
            if (!supervisorValido) {
                setFormData(prev => ({ ...prev, supervisor_id: null }));
            }
        }
    };

    // ==================== HANDLERS ====================

    const handleInputChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
        
        // Limpiar error de validación para este campo
        if (validationErrors[field]) {
            setValidationErrors(prev => ({
                ...prev,
                [field]: null
            }));
        }
    };

    const handleSeccionToggle = (seccionId) => {
        setFormData(prev => ({
            ...prev,
            secciones_asignadas: prev.secciones_asignadas.includes(seccionId)
                ? prev.secciones_asignadas.filter(id => id !== seccionId)
                : [...prev.secciones_asignadas, seccionId]
        }));
    };

    const validateForm = () => {
        const errors = {};
        
        // Validaciones básicas
        if (!formData.email.trim()) {
            errors.email = 'Email es requerido';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            errors.email = 'Email no es válido';
        }
        
        if (!formData.username.trim()) {
            errors.username = 'Username es requerido';
        } else if (formData.username.length < 3) {
            errors.username = 'Username debe tener al menos 3 caracteres';
        }
        
        if (!formData.nombre_completo.trim()) {
            errors.nombre_completo = 'Nombre completo es requerido';
        }
        
        // Validación de contraseña para nuevos usuarios
        if (!usuario && !formData.password) {
            errors.password = 'Contraseña es requerida para nuevos usuarios';
        } else if (!usuario && formData.password.length < 6) {
            errors.password = 'Contraseña debe tener al menos 6 caracteres';
        }
        
        // Validaciones jerárquicas
        if (formData.role === 'jefe_seccion' && formData.secciones_asignadas.length === 0) {
            errors.secciones_asignadas = 'Jefe de sección debe tener al menos una sección asignada';
        }
        
        if (formData.limite_tokens_diario < 1000 || formData.limite_tokens_diario > 100000) {
            errors.limite_tokens_diario = 'Límite debe estar entre 1,000 y 100,000 tokens';
        }
        
        setValidationErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            Toast.error('Por favor corrige los errores en el formulario');
            return;
        }
        
        setLoading(true);
        setError('');
        
        try {
            const token = localStorage.getItem('token');
            const url = usuario 
                ? `/api/auth/users/${usuario.id}` 
                : '/api/auth/register';
            
            const method = usuario ? 'PUT' : 'POST';
            
            // Preparar datos para envío
            const dataToSend = { ...formData };
            
            // Si no hay contraseña, no la enviamos en actualizaciones
            if (usuario && !dataToSend.password) {
                delete dataToSend.password;
            }
            
            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(dataToSend)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error en la operación');
            }
            
            const result = await response.json();
            
            if (usuario) {
                Toast.success(`Usuario ${result.username} actualizado correctamente`);
            } else {
                Toast.success(`Usuario ${result.username} creado correctamente`);
            }
            
            if (onSave) {
                onSave(result);
            }
            
        } catch (err) {
            console.error('Error guardando usuario:', err);
            const message = err.message || 'Error guardando usuario';
            setError(message);
            Toast.error(message);
        } finally {
            setLoading(false);
        }
    };

    // ==================== RENDER UTILS ====================

    const getRoleInfo = (role) => {
        const roles = {
            admin: { label: 'Administrador Sistema', nivel: 1, puede_supervisar: true },
            director: { label: 'Director de Redacción', nivel: 2, puede_supervisar: true },
            jefe_seccion: { label: 'Jefe de Sección', nivel: 3, puede_supervisar: true },
            redactor: { label: 'Redactor', nivel: 4, puede_supervisar: false },
            viewer: { label: 'Visor', nivel: 5, puede_supervisar: false }
        };
        return roles[role] || { label: 'Sin rol', puede_supervisar: false };
    };

    const getSupervisorNombre = (supervisorId) => {
        const supervisor = todosUsuarios.find(u => u.id === supervisorId);
        return supervisor ? supervisor.nombre_completo : 'No encontrado';
    };

    const getSeccionNombre = (seccionId) => {
        const seccion = secciones.find(s => s.id === seccionId);
        return seccion ? seccion.nombre : 'Sección no encontrada';
    };

    // ==================== RENDER ====================

    return (
        <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white mb-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <Users className="h-8 w-8" />
                        <div>
                            <h1 className="text-2xl font-bold">
                                {usuario ? 'Editar Usuario' : 'Crear Nuevo Usuario'}
                            </h1>
                            <p className="text-blue-100">
                                {usuario 
                                    ? `Modificando: ${usuario.nombre_completo || usuario.username}`
                                    : 'Configurar roles, jerarquía y permisos'
                                }
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="text-white/70 hover:text-white p-2 rounded-lg hover:bg-white/10"
                    >
                        <X className="h-6 w-6" />
                    </button>
                </div>
            </div>

            {error && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
                    <div className="flex items-center space-x-2 text-red-800 dark:text-red-200">
                        <AlertCircle className="h-5 w-5" />
                        <span>{error}</span>
                    </div>
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Información Básica */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
                        <Edit className="h-5 w-5 text-blue-600" />
                        <span>Información Básica</span>
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Email *
                            </label>
                            <input
                                type="email"
                                value={formData.email}
                                onChange={(e) => handleInputChange('email', e.target.value)}
                                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                                    validationErrors.email ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                                }`}
                                placeholder="usuario@empresa.com"
                            />
                            {validationErrors.email && (
                                <p className="text-red-500 text-sm mt-1">{validationErrors.email}</p>
                            )}
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Username *
                            </label>
                            <input
                                type="text"
                                value={formData.username}
                                onChange={(e) => handleInputChange('username', e.target.value.toLowerCase())}
                                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                                    validationErrors.username ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                                }`}
                                placeholder="usuario"
                            />
                            {validationErrors.username && (
                                <p className="text-red-500 text-sm mt-1">{validationErrors.username}</p>
                            )}
                        </div>

                        <div className="md:col-span-2">
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Nombre Completo *
                            </label>
                            <input
                                type="text"
                                value={formData.nombre_completo}
                                onChange={(e) => handleInputChange('nombre_completo', e.target.value)}
                                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                                    validationErrors.nombre_completo ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                                }`}
                                placeholder="Nombre y apellidos del usuario"
                            />
                            {validationErrors.nombre_completo && (
                                <p className="text-red-500 text-sm mt-1">{validationErrors.nombre_completo}</p>
                            )}
                        </div>

                        {!usuario && (
                            <div className="md:col-span-2">
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                    Contraseña *
                                </label>
                                <div className="relative">
                                    <input
                                        type={showPassword ? 'text' : 'password'}
                                        value={formData.password}
                                        onChange={(e) => handleInputChange('password', e.target.value)}
                                        className={`w-full px-3 py-2 pr-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                                            validationErrors.password ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                                        }`}
                                        placeholder="Contraseña segura (mínimo 6 caracteres)"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                    >
                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>
                                {validationErrors.password && (
                                    <p className="text-red-500 text-sm mt-1">{validationErrors.password}</p>
                                )}
                            </div>
                        )}
                    </div>
                </div>

                {/* Roles y Jerarquía */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
                        <Crown className="h-5 w-5 text-purple-600" />
                        <span>Roles y Jerarquía Editorial</span>
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Role en el Sistema *
                            </label>
                            <select
                                value={formData.role}
                                onChange={(e) => handleInputChange('role', e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                                disabled={!isAdmin() && formData.role === 'admin'}
                            >
                                {Object.entries(localRoles).map(([role, info]) => (
                                    <option key={role} value={role} disabled={!isAdmin() && role === 'admin'}>
                                        {info.label} {/* (Nivel {info.nivel}) */}
                                    </option>
                                ))}
                            </select>
                            <p className="text-sm text-gray-500 mt-1">
                                {getRoleInfo(formData.role).label} - 
                                {getRoleInfo(formData.role).puede_supervisar ? ' Puede supervisar' : ' No puede supervisar'}
                            </p>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Supervisor Directo
                            </label>
                            <select
                                value={formData.supervisor_id || ''}
                                onChange={(e) => handleInputChange('supervisor_id', e.target.value ? parseInt(e.target.value) : null)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                                disabled={formData.role === 'admin'}
                            >
                                <option value="">Sin supervisor</option>
                                {posiblesSupervisores.map(supervisor => (
                                    <option key={supervisor.id} value={supervisor.id}>
                                        {supervisor.nombre_completo} ({supervisor.role})
                                    </option>
                                ))}
                            </select>
                            {formData.supervisor_id && (
                                <p className="text-sm text-green-600 mt-1">
                                    Reporta a: {getSupervisorNombre(formData.supervisor_id)}
                                </p>
                            )}
                        </div>
                    </div>
                </div>

                {/* Secciones Asignadas */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
                        <Briefcase className="h-5 w-5 text-green-600" />
                        <span>Secciones Asignadas</span>
                    </h3>
                    
                    <div className="space-y-2">
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                            Selecciona las secciones que puede gestionar este usuario:
                        </p>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                            {secciones.map(seccion => (
                                <label
                                    key={seccion.id}
                                    className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
                                        formData.secciones_asignadas.includes(seccion.id)
                                            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                                            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                                    }`}
                                >
                                    <input
                                        type="checkbox"
                                        checked={formData.secciones_asignadas.includes(seccion.id)}
                                        onChange={() => handleSeccionToggle(seccion.id)}
                                        className="mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                    />
                                    <div>
                                        <div className="font-medium text-gray-900 dark:text-white">
                                            {seccion.nombre}
                                        </div>
                                        {seccion.descripcion && (
                                            <div className="text-sm text-gray-500 dark:text-gray-400">
                                                {seccion.descripcion}
                                            </div>
                                        )}
                                    </div>
                                </label>
                            ))}
                        </div>
                        
                        {validationErrors.secciones_asignadas && (
                            <p className="text-red-500 text-sm mt-2">{validationErrors.secciones_asignadas}</p>
                        )}
                        
                        {formData.secciones_asignadas.length > 0 && (
                            <div className="mt-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Secciones seleccionadas:
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {formData.secciones_asignadas.map(seccionId => (
                                        <span
                                            key={seccionId}
                                            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
                                        >
                                            {getSeccionNombre(seccionId)}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Configuración y Límites */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
                        <Settings className="h-5 w-5 text-orange-600" />
                        <span>Configuración y Límites</span>
                    </h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Límite Diario de Tokens IA
                            </label>
                            <div className="relative">
                                <input
                                    type="number"
                                    min="1000"
                                    max="100000"
                                    step="1000"
                                    value={formData.limite_tokens_diario}
                                    onChange={(e) => handleInputChange('limite_tokens_diario', parseInt(e.target.value) || 1000)}
                                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white ${
                                        validationErrors.limite_tokens_diario ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'
                                    }`}
                                />
                                <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                                    <Target className="h-4 w-4" />
                                </div>
                            </div>
                            {validationErrors.limite_tokens_diario && (
                                <p className="text-red-500 text-sm mt-1">{validationErrors.limite_tokens_diario}</p>
                            )}
                            <p className="text-sm text-gray-500 mt-1">
                                Entre 1,000 y 100,000 tokens por día
                            </p>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                                Fecha de Expiración de Acceso
                            </label>
                            <div className="relative">
                                <input
                                    type="date"
                                    value={formData.fecha_expiracion_acceso}
                                    onChange={(e) => handleInputChange('fecha_expiracion_acceso', e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                                />
                                <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                                    <Calendar className="h-4 w-4" />
                                </div>
                            </div>
                            <p className="text-sm text-gray-500 mt-1">
                                Opcional. El usuario perderá acceso en esta fecha.
                            </p>
                        </div>

                        <div className="md:col-span-2">
                            <label className="flex items-center space-x-3">
                                <input
                                    type="checkbox"
                                    checked={formData.is_active}
                                    onChange={(e) => handleInputChange('is_active', e.target.checked)}
                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                />
                                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Usuario activo
                                </span>
                            </label>
                            <p className="text-sm text-gray-500 mt-1 ml-7">
                                Los usuarios inactivos no pueden iniciar sesión en el sistema
                            </p>
                        </div>
                    </div>
                </div>

                {/* Botones de acción */}
                <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
                    <button
                        type="button"
                        onClick={onClose}
                        className="px-6 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 font-medium"
                        disabled={loading}
                    >
                        Cancelar
                    </button>
                    <button
                        type="submit"
                        disabled={loading}
                        className="flex items-center space-x-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-colors"
                    >
                        <Save className="h-4 w-4" />
                        <span>
                            {loading 
                                ? (usuario ? 'Actualizando...' : 'Creando...') 
                                : (usuario ? 'Actualizar Usuario' : 'Crear Usuario')
                            }
                        </span>
                    </button>
                </div>
            </form>
        </div>
    );
};

export default UsuarioAdminForm;