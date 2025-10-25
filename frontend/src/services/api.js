import axios from 'axios';

// Cambia esta IP por la IP real de tu servidor backend en la LAN

// Permite alternar entre ngrok, localhost y IP local según entorno
const API_BASE =
  import.meta.env.VITE_API_BASE ||
  'http://172.17.100.64:8000/api';

// Ejemplo para desarrollo local:
// VITE_API_BASE=http://localhost:8000/api
// VITE_API_BASE=http://172.17.100.64:8000/api
// VITE_API_BASE=https://credible-kodiak-one.ngrok-free.app/api

// Crear instancia de axios
const axiosInstance = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para agregar token a todas las solicitudes
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores globalmente
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Exportar instancia de axios como default
export default axiosInstance;

// También exportar API helper para compatibilidad con código antiguo
export const api = {
  // Obtener historial de conversación IA
  getHistorialChat: async (conversacionId) => {
    if (!conversacionId) return [];
    try {
      const { data } = await axiosInstance.get(`/ai/conversaciones/${conversacionId}`);
      return data.mensajes || [];
    } catch {
      return [];
    }
  },
  actualizarNoticia: async (id, data, token) => {
    const { data: result } = await axiosInstance.put(`/noticias/${id}`, data);
    return result;
  },
  // Noticias
  getNoticias: async (filtros = {}) => {
    // filtros puede incluir: proyecto_id, estado, limite, etc.
    const params = { limite: 100, ...filtros };
    const { data } = await axiosInstance.get('/noticias/', { params });
    return data;
  },

  // Obtener noticia individual por ID
  getNoticia: async (id) => {
    const { data } = await axiosInstance.get(`/noticias/${id}`);
    return data;
  },

  crearNoticia: async (data, token) => {
    const { data: result } = await axiosInstance.post('/noticias/', data);
    return result;
  },

  eliminarNoticia: async (id, token) => {
    const { data } = await axiosInstance.delete(`/noticias/${id}`);
    return data;
  },

  generarResumen: async (noticiaId) => {
    const { data } = await axiosInstance.post(`/ai/resumir/${noticiaId}`);
    return data;
  },

  chatIA: async (mensaje, conversacionId = null, llmId = null, contexto = null) => {
    const payload = { mensaje };
    if (conversacionId) payload.conversacion_id = conversacionId;
    if (llmId) payload.llm_id = llmId;
    if (contexto) payload.contexto = contexto;
    const { data } = await axiosInstance.post('/ai/chat', payload);
    return data;
  },

  seedData: async () => {
    const { data } = await axiosInstance.post('/noticias/seed');
    return data;
  },

  // Proyectos
  getProyectos: async (estado = null, token = null) => {
    const params = estado 
      ? { estado, limite: 100 }
      : { limite: 100 };
    const { data } = await axiosInstance.get('/proyectos/', { params });
    return data;
  },

  getProyecto: async (id, token = null) => {
    const { data } = await axiosInstance.get(`/proyectos/${id}`);
    return data;
  },

  crearProyecto: async (data, token) => {
    const { data: result } = await axiosInstance.post('/proyectos/', data);
    return result;
  },

  actualizarProyecto: async (id, data, token) => {
    const { data: result } = await axiosInstance.put(`/proyectos/${id}`, data);
    return result;
  },

  eliminarProyecto: async (id, permanente, token) => {
    const { data } = await axiosInstance.delete(`/proyectos/${id}`, {
      params: { permanente }
    });
    return data;
  },

  archivarProyecto: async (id, token) => {
    const { data } = await axiosInstance.post(`/proyectos/${id}/archivar`);
    return data;
  },

  restaurarProyecto: async (id, token) => {
    const { data } = await axiosInstance.post(`/proyectos/${id}/restaurar`);
    return data;
  },

  getProyectoStats: async (id, token = null) => {
    const { data } = await axiosInstance.get(`/proyectos/${id}/stats`);
    return data;
  }
};
