// Servicio para manejar métricas de valor periodístico
import axiosInstance from './api.js';

class MetricasService {
  /**
   * Obtiene las métricas de una noticia específica
   * @param {number} noticiaId - ID de la noticia
   * @returns {Promise<Object|null>} Métricas de la noticia o null si no existen
   */
  async obtenerMetricasNoticia(noticiaId) {
    try {
      console.log(`🔍 MetricasService: Obteniendo métricas para noticia ${noticiaId}`);
      const response = await axiosInstance.get(`/metricas/noticia/${noticiaId}`);
      console.log(`✅ MetricasService: Métricas obtenidas exitosamente`, response.data);
      return response.data;
    } catch (error) {
      console.log(`❌ MetricasService: Error obteniendo métricas`, {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        url: error.config?.url
      });
      
      if (error.response?.status === 404 || error.response?.status === 403) {
        // No hay métricas o no es admin - devolver null sin error
        console.log(`ℹ️ MetricasService: Sin métricas disponibles (404/403 es normal)`);
        return null;
      }
      console.error('Error obteniendo métricas de noticia:', error);
      throw error;
    }
  }

  // Obtener estadísticas generales (solo admins)
  async obtenerEstadisticasGenerales() {
    try {
      const response = await axiosInstance.get('/metricas/estadisticas');
      return response.data;
    } catch (error) {
      console.error('Error obteniendo estadísticas generales:', error);
      throw error;
    }
  }
}

export default new MetricasService();