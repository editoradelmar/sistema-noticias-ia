import axios from 'axios';
import { appConfig } from '../config/appConfig.js';

// Usar configuración centralizada de appConfig.js
const API_BASE = `${appConfig.API_BASE_URL}/api`;

console.log('🔧 API Base URL configurada:', API_BASE);

// Crear instancia de axios
const axiosInstance = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true'  // Omitir advertencia de ngrok
  }
});

// Interceptor para agregar token a todas las solicitudes
axiosInstance.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.url, 'Base:', config.baseURL);
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔐 Token agregado');
    } else {
      console.log('⚠️ No hay token');
    }
    // Asegurar header de ngrok en todas las solicitudes
    config.headers['ngrok-skip-browser-warning'] = 'true';
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores globalmente
axiosInstance.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ API Error:', error.response?.status, error.response?.data, 'URL:', error.config?.url);
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
  },

  // Usuarios
  getUsuarios: async (activosSolo = true) => {
    const params = { activos_solo: activosSolo };
    const { data } = await axiosInstance.get('/auth/users', { params });
    return data;
  }
};
