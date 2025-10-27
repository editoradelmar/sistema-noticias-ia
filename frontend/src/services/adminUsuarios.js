/**
 * Servicio para administración de usuarios
 * Gestión completa de usuarios con jerarquía editorial
 */
import api from './api.js';

const adminUsuariosService = {
    // ==================== OBTENER USUARIOS ====================
    
    /**
     * Obtener lista de usuarios para administración
     * @param {Object} filtros - Filtros de búsqueda
     * @param {boolean} filtros.activosSolo - Solo usuarios activos
     * @param {string} filtros.role - Filtrar por role
     * @param {number} filtros.seccionId - Filtrar por sección
     * @param {number} filtros.supervisorId - Filtrar por supervisor
     * @param {string} filtros.search - Búsqueda en nombre/email
     * @returns {Promise<Array>} Lista de usuarios extendidos
     */
    async getUsuarios(filtros = {}) {
        const params = new URLSearchParams();
        
        if (filtros.activosOnly !== undefined) {
            params.append('activos_solo', filtros.activosOnly);
        }
        if (filtros.role) {
            params.append('role_filter', filtros.role);
        }
        if (filtros.seccionId) {
            params.append('seccion_id', filtros.seccionId);
        }
        if (filtros.supervisorId) {
            params.append('supervisor_id', filtros.supervisorId);
        }
        if (filtros.search) {
            params.append('search', filtros.search);
        }
        
        const queryString = params.toString();
        const url = queryString ? `/admin/usuarios?${queryString}` : '/admin/usuarios';
        
        const response = await api.get(url);
        return response.data;
    },

    /**
     * Obtener usuario específico por ID
     * @param {number} userId - ID del usuario
     * @returns {Promise<Object>} Usuario extendido
     */
    async getUsuario(userId) {
        const response = await api.get(`/admin/usuarios/${userId}`);
        return response.data;
    },

    /**
     * Obtener jerarquía organizacional completa
     * @returns {Promise<Array>} Estructura de árbol jerárquico
     */
    async getJerarquia() {
        const response = await api.get('/admin/jerarquia');
        return response.data;
    },

    // ==================== CREAR/ACTUALIZAR USUARIOS ====================

    /**
     * Crear nuevo usuario
     * @param {Object} usuarioData - Datos del usuario
     * @param {string} usuarioData.email - Email único
     * @param {string} usuarioData.username - Username único
     * @param {string} usuarioData.password - Contraseña
     * @param {string} usuarioData.nombre_completo - Nombre completo
     * @param {string} usuarioData.role - Role del usuario
     * @param {number} usuarioData.supervisor_id - ID del supervisor (opcional)
     * @param {Array<number>} usuarioData.secciones_asignadas - IDs de secciones
     * @param {number} usuarioData.limite_tokens_diario - Límite de tokens
     * @param {string} usuarioData.fecha_expiracion_acceso - Fecha en formato YYYY-MM-DD
     * @returns {Promise<Object>} Usuario creado
     */
    async crear(usuarioData) {
        const response = await api.post('/admin/usuarios', usuarioData);
        return response.data;
    },

    /**
     * Actualizar usuario existente
     * @param {number} userId - ID del usuario
     * @param {Object} usuarioData - Datos a actualizar (parciales)
     * @returns {Promise<Object>} Usuario actualizado
     */
    async actualizar(userId, usuarioData) {
        const response = await api.put(`/admin/usuarios/${userId}`, usuarioData);
        return response.data;
    },

    /**
     * Eliminar/desactivar usuario
     * @param {number} userId - ID del usuario
     * @param {boolean} forzar - Forzar eliminación física
     * @returns {Promise<Object>} Resultado de la operación
     */
    async eliminar(userId, forzar = false) {
        const params = forzar ? '?forzar=true' : '';
        const response = await api.delete(`/admin/usuarios/${userId}${params}`);
        return response.data;
    },

    // ==================== OPERACIONES ESPECIALES ====================

    /**
     * Resetear contraseña de usuario
     * @param {number} userId - ID del usuario
     * @param {string} nuevaPassword - Nueva contraseña
     * @returns {Promise<Object>} Resultado de la operación
     */
    async resetPassword(userId, nuevaPassword) {
        const response = await api.post(`/admin/usuarios/${userId}/reset-password?nueva_password=${encodeURIComponent(nuevaPassword)}`);
        return response.data;
    },

    /**
     * Activar/desactivar usuario
     * @param {number} userId - ID del usuario
     * @param {boolean} activo - Estado activo
     * @returns {Promise<Object>} Usuario actualizado
     */
    async toggleActivo(userId, activo) {
        return this.actualizar(userId, { is_active: activo });
    },

    /**
     * Cambiar supervisor de usuario
     * @param {number} userId - ID del usuario
     * @param {number|null} supervisorId - ID del nuevo supervisor (null para quitar)
     * @returns {Promise<Object>} Usuario actualizado
     */
    async cambiarSupervisor(userId, supervisorId) {
        return this.actualizar(userId, { supervisor_id: supervisorId });
    },

    /**
     * Asignar secciones a usuario
     * @param {number} userId - ID del usuario
     * @param {Array<number>} seccionesIds - IDs de secciones
     * @returns {Promise<Object>} Usuario actualizado
     */
    async asignarSecciones(userId, seccionesIds) {
        return this.actualizar(userId, { secciones_asignadas: seccionesIds });
    },

    // ==================== UTILIDADES ====================

    /**
     * Obtener lista de posibles supervisores para un usuario
     * @param {string} roleUsuario - Role del usuario actual
     * @param {Array} todosUsuarios - Lista completa de usuarios
     * @returns {Array} Usuarios que pueden ser supervisores
     */
    getPosiblesSupervisores(roleUsuario, todosUsuarios) {
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
    },

    /**
     * Validar estructura jerárquica
     * @param {Array} usuarios - Lista de usuarios
     * @returns {Object} Resultado de validación con errores
     */
    validarJerarquia(usuarios) {
        const errores = [];
        const usuariosMap = new Map(usuarios.map(u => [u.id, u]));

        usuarios.forEach(usuario => {
            // Verificar supervisor válido
            if (usuario.supervisor_id) {
                const supervisor = usuariosMap.get(usuario.supervisor_id);
                if (!supervisor) {
                    errores.push(`${usuario.username}: Supervisor con ID ${usuario.supervisor_id} no existe`);
                } else if (!supervisor.puede_supervisar) {
                    errores.push(`${usuario.username}: ${supervisor.username} no puede ser supervisor`);
                }
            }

            // Verificar ciclos en jerarquía
            const visitados = new Set();
            let actual = usuario;
            while (actual && actual.supervisor_id) {
                if (visitados.has(actual.id)) {
                    errores.push(`Ciclo detectado en jerarquía incluyendo a ${usuario.username}`);
                    break;
                }
                visitados.add(actual.id);
                actual = usuariosMap.get(actual.supervisor_id);
            }
        });

        return {
            valida: errores.length === 0,
            errores
        };
    },

    /**
     * Construir árbol jerárquico desde lista plana
     * @param {Array} usuarios - Lista de usuarios
     * @param {number|null} supervisorId - ID del supervisor (null para raíz)
     * @returns {Array} Árbol jerárquico
     */
    construirArbol(usuarios, supervisorId = null) {
        const subordinados = usuarios.filter(u => u.supervisor_id === supervisorId);
        
        return subordinados.map(usuario => ({
            ...usuario,
            subordinados: this.construirArbol(usuarios, usuario.id)
        }));
    },

    /**
     * Obtener usuarios que el usuario actual puede gestionar
     * @param {Object} usuarioActual - Usuario con sesión activa
     * @param {Array} todosUsuarios - Lista completa de usuarios
     * @returns {Array} Usuarios gestionables
     */
    getUsuariosGestionables(usuarioActual, todosUsuarios) {
        if (usuarioActual.role === 'admin') {
            return todosUsuarios;
        }
        
        if (usuarioActual.role === 'director') {
            return todosUsuarios.filter(u => u.role !== 'admin');
        }
        
        if (usuarioActual.role === 'jefe_seccion') {
            return todosUsuarios.filter(u => 
                u.supervisor_id === usuarioActual.id || u.id === usuarioActual.id
            );
        }
        
        return [usuarioActual];
    },

    // ==================== CONSTANTES ====================

    /**
     * Roles disponibles con sus niveles jerárquicos
     */
    ROLES: {
        admin: { label: 'Administrador Sistema', nivel: 1, puede_supervisar: true },
        director: { label: 'Director de Redacción', nivel: 2, puede_supervisar: true },
        jefe_seccion: { label: 'Jefe de Sección', nivel: 3, puede_supervisar: true },
        redactor: { label: 'Redactor', nivel: 4, puede_supervisar: false },
        viewer: { label: 'Visor', nivel: 5, puede_supervisar: false }
    },

    /**
     * Obtener información de un role
     * @param {string} role - Nombre del role
     * @returns {Object} Información del role
     */
    getRoleInfo(role) {
        return this.ROLES[role] || { label: role, nivel: 99, puede_supervisar: false };
    }
};

export default adminUsuariosService;