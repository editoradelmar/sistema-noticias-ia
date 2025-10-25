// Servicio para manejo granular de items de Estilo
import api from './api';

export const estiloItemService = {
  // Listar items por estilo
  getByEstilo: async (estiloId) => {
    const { data } = await api.get(`/estilo-items/by-estilo/${estiloId}`);
    return data;
  },

  // Crear nuevo item
  create: async (itemData) => {
    // Filtrar solo campos válidos
    const allowedFields = ['estilo_id', 'nombre_archivo', 'contenido', 'orden'];
    const cleanData = {};
    for (const key of allowedFields) {
      if (itemData.hasOwnProperty(key)) {
        cleanData[key] = itemData[key];
      }
    }
    const { data } = await api.post('/estilo-items/', cleanData);
    return data;
  },

  // Actualizar item
  update: async (itemId, itemData) => {
    const { data } = await api.put(`/estilo-items/${itemId}`, itemData);
    return data;
  },

  // Eliminar item
  delete: async (itemId) => {
    await api.delete(`/estilo-items/${itemId}`);
  }
};