import React from 'react';
import { useAuth } from '../context/AuthContext';

const MetricasValor = ({ metricas }) => {
  const { user, isAdmin } = useAuth();

  // Debug logs
  console.log('🔍 MetricasValor Debug:', {
    isAdmin: isAdmin(),
    puede_ver_metricas: user?.puede_ver_metricas,
    hasMetricas: !!metricas,
    metricas: metricas
  });

  // Mostrar solo si es admin o el usuario tiene permiso explícito
  if (!isAdmin() && !user?.puede_ver_metricas) {
    console.log('❌ Usuario no tiene permiso para ver métricas, ocultando métricas');
    return null;
  }

  if (!metricas) {
    console.log('❌ No hay métricas para mostrar');
    return null;
  }

  console.log('✅ Mostrando métricas:', metricas);

  return (
    <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border border-green-200 dark:border-green-700 rounded-lg p-4 mt-4">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <h3 className="text-sm font-semibold text-green-700 dark:text-green-300">
          📈 Métricas de Valor Periodístico (Admin)
        </h3>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
        {/* ROI Principal */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-green-100 dark:border-green-800">
          <div className="text-green-600 dark:text-green-400 font-medium">ROI</div>
          <div className="text-lg font-bold text-green-700 dark:text-green-300">
            {metricas.roi_porcentaje}%
          </div>
        </div>

        {/* Tiempo Ahorrado */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-blue-100 dark:border-blue-800">
          <div className="text-blue-600 dark:text-blue-400 font-medium">Ahorro Tiempo</div>
          <div className="text-lg font-bold text-blue-700 dark:text-blue-300">
            {metricas.ahorro_tiempo_minutos} min
          </div>
        </div>

        {/* Ahorro de Costo */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-amber-100 dark:border-amber-800">
          <div className="text-amber-600 dark:text-amber-400 font-medium">Ahorro $</div>
          <div className="text-lg font-bold text-amber-700 dark:text-amber-300">
            ${metricas.ahorro_costo}
          </div>
        </div>

        {/* Productividad */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-purple-100 dark:border-purple-800">
          <div className="text-purple-600 dark:text-purple-400 font-medium">Velocidad</div>
          <div className="text-lg font-bold text-purple-700 dark:text-purple-300">
            {metricas.velocidad_palabras_por_segundo} p/s
          </div>
        </div>

        {/* Eficiencia */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-indigo-100 dark:border-indigo-800">
          <div className="text-indigo-600 dark:text-indigo-400 font-medium">Eficiencia</div>
          <div className="text-lg font-bold text-indigo-700 dark:text-indigo-300">
            {metricas.eficiencia_temporal}%
          </div>
        </div>

        {/* Calidad */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-rose-100 dark:border-rose-800">
          <div className="text-rose-600 dark:text-rose-400 font-medium">Calidad IA</div>
          <div className="text-lg font-bold text-rose-700 dark:text-rose-300">
            {(metricas.porcentaje_contenido_aprovechable * 100).toFixed(0)}%
          </div>
        </div>

        {/* Tokens */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-gray-100 dark:border-gray-700">
          <div className="text-gray-600 dark:text-gray-400 font-medium">Tokens</div>
          <div className="text-lg font-bold text-gray-700 dark:text-gray-300">
            {metricas.tokens_total?.toLocaleString() || 'N/A'}
          </div>
        </div>

        {/* Costo Generación */}
        <div className="bg-white dark:bg-gray-800 rounded-md p-2 border border-teal-100 dark:border-teal-800">
          <div className="text-teal-600 dark:text-teal-400 font-medium">Costo IA</div>
          <div className="text-lg font-bold text-teal-700 dark:text-teal-300">
            ${metricas.costo_generacion}
          </div>
        </div>
      </div>

      {/* Información adicional */}
      {metricas.tiempo_generacion_total && (
        <div className="mt-3 pt-2 border-t border-green-200 dark:border-green-700">
          <div className="flex justify-between text-xs text-green-600 dark:text-green-400">
            <span>⏱️ Tiempo total: {metricas.tiempo_generacion_total}s</span>
            <span>🎯 Salidas: {metricas.cantidad_salidas_generadas}</span>
            <span>🤖 Modelo: {metricas.modelo_usado}</span>
          </div>
        </div>
      )}

      {/* Indicador de valor */}
      <div className="mt-2 text-xs text-center">
        {metricas.roi_porcentaje > 200 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-full">
            🚀 Alto Valor - Excelente ROI
          </span>
        )}
        {metricas.roi_porcentaje >= 100 && metricas.roi_porcentaje <= 200 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full">
            ✅ Buen Valor - ROI Positivo
          </span>
        )}
        {metricas.roi_porcentaje < 100 && metricas.roi_porcentaje > 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300 rounded-full">
            ⚠️ ROI Moderado
          </span>
        )}
        {metricas.roi_porcentaje <= 0 && (
          <span className="inline-flex items-center gap-1 px-2 py-1 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-full">
            📉 Revisar Eficiencia
          </span>
        )}
      </div>
    </div>
  );
};

export default MetricasValor;