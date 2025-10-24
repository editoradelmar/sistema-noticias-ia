// Servicio de Generación IA
import api from './api';

export const generacionService = {
  /**
   * Generar contenido para múltiples salidas
   * @param {Object} data - { noticia_id, salidas_ids[], llm_id, prompt_id?, estilo_id?, regenerar? }
   */
  generarSalidas: async (data) => {
    const response = await api.post('/generar/salidas', data);
    return response.data;
  },

  /**
   * Generar contenido para una sola salida
   */
  generarSalidaIndividual: async (params) => {
    const { noticia_id, salida_id, llm_id, prompt_id, estilo_id, regenerar } = params;
    const response = await api.post('/generar/salida-individual', null, {
      params: { noticia_id, salida_id, llm_id, prompt_id, estilo_id, regenerar }
    });
    return response.data;
  },

  /**
   * Obtener todas las salidas generadas de una noticia
   */
  obtenerSalidasNoticia: async (noticia_id) => {
    const response = await api.get(`/generar/noticia/${noticia_id}/salidas`);
    return response.data;
  },

  /**
   * Eliminar una salida generada
   */
  eliminarSalida: async (noticia_salida_id) => {
    await api.delete(`/generar/salida/${noticia_salida_id}`);
  },

  /**
   * Regenerar todas las salidas de una noticia
   */

  regenerarTodo: async (noticia_id, llm_id) => {
    const response = await api.post(`/generar/regenerar-todo/${noticia_id}`, null, {
      params: { llm_id }
    });
    return response.data;
  },

  /**
   * Actualizar una salida generada (título/contenido)
   * @param {number} noticia_salida_id
   * @param {Object} data - { titulo, contenido_generado }
   */
  updateSalida: async (noticia_salida_id, data) => {
    const response = await api.put(`/generar/salida/${noticia_salida_id}`, data);
    return response.data;
  }
};

export default generacionService;
