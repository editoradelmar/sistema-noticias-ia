// Servicios API para Sistema de Maestros - Fase 6
import api from './api';

// ==================== LLM MAESTRO ====================

export const llmService = {
  // Listar todos los LLMs
  getAll: async (params = {}) => {
    const { data } = await api.get('/llm-maestro/', { params });
    return data;
  },

  // Listar solo LLMs activos
  getActivos: async () => {
    const { data } = await api.get('/llm-maestro/activos');
    return data;
  },

  // Obtener un LLM por ID (sin API key)
  getById: async (id) => {
    const { data } = await api.get(`/llm-maestro/${id}`);
    return data;
  },

  // Obtener LLM con API key (solo admin)
  getByIdWithKey: async (id) => {
    const { data } = await api.get(`/llm-maestro/${id}/with-key`);
    return data;
  },

  // Crear nuevo LLM
  create: async (llmData) => {
    const { data } = await api.post('/llm-maestro/', llmData);
    return data;
  },

  // Actualizar LLM
  update: async (id, llmData) => {
    const { data } = await api.put(`/llm-maestro/${id}`, llmData);
    return data;
  },

  // Eliminar LLM
  delete: async (id) => {
    await api.delete(`/llm-maestro/${id}`);
  },

  // Activar/Desactivar LLM
  toggleActivo: async (id) => {
    const { data } = await api.patch(`/llm-maestro/${id}/toggle-activo`);
    return data;
  },

  // Resetear tokens diarios
  resetTokens: async (id) => {
    const { data } = await api.post(`/llm-maestro/${id}/reset-tokens`);
    return data;
  },

  // Probar conexión
  testConnection: async (id) => {
    const { data } = await api.post(`/llm-maestro/${id}/test-connection`);
    return data;
  }
};

// ==================== PROMPTS ====================

export const promptService = {
  getAll: async (params = {}) => {
    const { data } = await api.get('/prompts/', { params });
    return data;
  },

  getActivos: async () => {
    const { data } = await api.get('/prompts/activos');
    return data;
  },

  getById: async (id) => {
    const { data } = await api.get(`/prompts/${id}`);
    return data;
  },

  create: async (promptData) => {
    const { data } = await api.post('/prompts/', promptData);
    return data;
  },

  update: async (id, promptData) => {
    const { data } = await api.put(`/prompts/${id}`, promptData);
    return data;
  },

  delete: async (id) => {
    await api.delete(`/prompts/${id}`);
  },

  toggleActivo: async (id, activoActual) => {
    const { data } = await api.put(`/prompts/${id}`, { activo: !activoActual });
    return data;
  },

  validar: async (id, variablesTest) => {
    const { data } = await api.post(`/prompts/${id}/validar`, variablesTest);
    return data;
  }
};

// ==================== ESTILOS ====================

export const estiloService = {
  getAll: async (params = {}) => {
    const { data } = await api.get('/estilos/', { params });
    return data;
  },

  getActivos: async () => {
    const { data } = await api.get('/estilos/activos');
    return data;
  },

  getById: async (id) => {
    const { data } = await api.get(`/estilos/${id}`);
    return data;
  },

  create: async (estiloData) => {
    const { data } = await api.post('/estilos/', estiloData);
    return data;
  },

  update: async (id, estiloData) => {
    const { data } = await api.put(`/estilos/${id}`, estiloData);
    return data;
  },

  delete: async (id) => {
    await api.delete(`/estilos/${id}`);
  },

  toggleActivo: async (id, activoActual) => {
    const { data } = await api.put(`/estilos/${id}`, { activo: !activoActual });
    return data;
  }
};

// ==================== SECCIONES ====================

export const seccionService = {
  getAll: async (params = {}) => {
    const { data } = await api.get('/secciones/', { params });
    return data;
  },

  getActivas: async () => {
    const { data } = await api.get('/secciones/activas');
    return data;
  },

  getById: async (id, conRelaciones = true) => {
    const { data } = await api.get(`/secciones/${id}`, {
      params: { con_relaciones: conRelaciones }
    });
    return data;
  },

  create: async (seccionData) => {
    const { data } = await api.post('/secciones/', seccionData);
    return data;
  },

  update: async (id, seccionData) => {
    const { data } = await api.put(`/secciones/${id}`, seccionData);
    return data;
  },

  delete: async (id) => {
    await api.delete(`/secciones/${id}`);
  },

  toggleActivo: async (id, activoActual) => {
    const { data } = await api.put(`/secciones/${id}`, { activo: !activoActual });
    return data;
  }
};

// ==================== SALIDAS ====================

export const salidaService = {
  getAll: async (params = {}) => {
    const { data } = await api.get('/salidas/', { params });
    return data;
  },

  getActivas: async () => {
    const { data } = await api.get('/salidas/activas');
    return data;
  },

  getById: async (id) => {
    const { data } = await api.get(`/salidas/${id}`);
    return data;
  },

  create: async (salidaData) => {
    const { data } = await api.post('/salidas/', salidaData);
    return data;
  },

  update: async (id, salidaData) => {
    const { data } = await api.put(`/salidas/${id}`, salidaData);
    return data;
  },

  delete: async (id) => {
    await api.delete(`/salidas/${id}`);
  },

  toggleActivo: async (id, activoActual) => {
    const { data } = await api.put(`/salidas/${id}`, { activo: !activoActual });
    return data;
  }
};

// ==================== CONSTANTES ====================

export const TIPOS_SALIDA = [
  { value: 'print', label: 'Impreso', icon: '📰' },
  { value: 'digital', label: 'Digital/Web', icon: '💻' },
  { value: 'social', label: 'Redes Sociales', icon: '📱' },
  { value: 'email', label: 'Email/Newsletter', icon: '📧' },
  { value: 'podcast', label: 'Audio/Podcast', icon: '🎙️' }
];

// CATEGORIAS_PROMPT eliminado

export const TIPOS_ESTILO = [
  { value: 'tono', label: 'Tono' },
  { value: 'formato', label: 'Formato' },
  { value: 'estructura', label: 'Estructura' },
  { value: 'longitud', label: 'Longitud' }
];
