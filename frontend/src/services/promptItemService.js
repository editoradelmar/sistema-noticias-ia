// Servicio para manejo granular de items de Prompt
import api from './api';

export const promptItemService = {
  // Listar items por prompt
  getByPrompt: async (promptId) => {
    const { data } = await api.get(`/prompt-items/by-prompt/${promptId}`);
    return data;
  },

  // Crear nuevo item
  create: async (itemData) => {
    // Filtrar solo campos válidos
    const allowedFields = ['prompt_id', 'nombre_archivo', 'contenido', 'orden'];
    const cleanData = {};
    for (const key of allowedFields) {
      if (itemData.hasOwnProperty(key)) {
        cleanData[key] = itemData[key];
      }
    }
    const { data } = await api.post('/prompt-items/', cleanData);
    return data;
  },

  // Actualizar item
  update: async (itemId, itemData) => {
    const { data } = await api.put(`/prompt-items/${itemId}`, itemData);
    return data;
  },

  // Eliminar item
  delete: async (itemId) => {
    await api.delete(`/prompt-items/${itemId}`);
  }
};
