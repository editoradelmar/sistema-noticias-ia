import { useState, useEffect } from 'react';
import { FileText, Loader2, RefreshCw, Trash2 } from 'lucide-react';
import { generacionService } from '../services/generacion';

const SalidasNoticia = ({ noticiaId }) => {
  const [salidas, setSalidas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState(null);

  useEffect(() => {
    cargarSalidas();
  }, [noticiaId]);

  const cargarSalidas = async () => {
    try {
      setLoading(true);
      const data = await generacionService.obtenerSalidasNoticia(noticiaId);
      setSalidas(data);
      if (data.length > 0 && !activeTab) {
        setActiveTab(data[0].id);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEliminar = async (salidaId) => {
    if (!confirm('¿Eliminar esta salida generada?')) return;
    
    try {
      await generacionService.eliminarSalida(salidaId);
      await cargarSalidas();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const getSalidaActiva = () => {
    return salidas.find(s => s.id === activeTab);
  };

  const getSalidaIcon = (tipo) => {
    const icons = {
      print: '📰',
      digital: '💻',
      social: '📱',
      email: '📧',
      podcast: '🎙️'
    };
    return icons[tipo] || '📤';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  if (salidas.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600 dark:text-gray-400">
          No hay salidas generadas para esta noticia
        </p>
      </div>
    );
  }

  const salidaActiva = getSalidaActiva();

  return (
    <div className="space-y-4">
      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <div className="flex space-x-2 overflow-x-auto">
          {salidas.map(salida => (
            <button
              key={salida.id}
              onClick={() => setActiveTab(salida.id)}
              className={`
                flex items-center gap-2 px-4 py-2 border-b-2 transition-colors whitespace-nowrap
                ${activeTab === salida.id
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                }
              `}
            >
              <span className="text-xl">{getSalidaIcon(salida.salida?.tipo_salida)}</span>
              <span className="font-medium">{salida.salida?.nombre}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Contenido de la salida activa */}
      {salidaActiva && (
        <div className="space-y-4">
          {/* Metadatos */}
          <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 space-y-2 text-sm">
            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <p className="text-gray-600 dark:text-gray-400">
                  🤖 <strong>LLM:</strong> {salidaActiva.llm_usado?.nombre}
                </p>
                {salidaActiva.prompt_usado && (
                  <p className="text-gray-600 dark:text-gray-400">
                    📝 <strong>Prompt:</strong> {salidaActiva.prompt_usado.nombre}
                  </p>
                )}
                {salidaActiva.estilo_usado && (
                  <p className="text-gray-600 dark:text-gray-400">
                    🎨 <strong>Estilo:</strong> {salidaActiva.estilo_usado.nombre}
                  </p>
                )}
                <p className="text-gray-600 dark:text-gray-400">
                  ⚡ <strong>Tokens:</strong> {salidaActiva.tokens_usados?.toLocaleString() || 'N/A'}
                </p>
                <p className="text-gray-600 dark:text-gray-400">
                  ⏱️ <strong>Tiempo:</strong> {salidaActiva.tiempo_generacion_ms ? `${(salidaActiva.tiempo_generacion_ms / 1000).toFixed(2)}s` : 'N/A'}
                </p>
              </div>
              <button
                onClick={() => handleEliminar(salidaActiva.id)}
                className="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
                title="Eliminar salida"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Contenido generado */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
            <div className="prose dark:prose-invert max-w-none">
              <div className="whitespace-pre-wrap text-gray-900 dark:text-gray-100">
                {salidaActiva.contenido_generado}
              </div>
            </div>
          </div>

          {/* Botón copiar */}
          <div className="flex justify-end">
            <button
              onClick={() => {
                navigator.clipboard.writeText(salidaActiva.contenido_generado);
                alert('Contenido copiado al portapapeles');
              }}
              className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              📋 Copiar contenido
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SalidasNoticia;
