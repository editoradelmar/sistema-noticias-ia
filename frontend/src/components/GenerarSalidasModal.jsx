import { useState, useEffect } from 'react';
import { X, Zap, Loader2, CheckCircle, XCircle } from 'lucide-react';
import { llmService, salidaService } from '../services/maestros';
import { generacionService } from '../services/generacion';

const GenerarSalidasModal = ({ noticia, onClose, onSuccess }) => {
  const [llms, setLlms] = useState([]);
  const [salidas, setSalidas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generando, setGenerando] = useState(false);
  const [resultado, setResultado] = useState(null);
  
  const [form, setForm] = useState({
    llm_id: '',
    salidas_ids: [],
    regenerar: false
  });

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    try {
      const [llmsData, salidasData] = await Promise.all([
        llmService.getActivos(),
        salidaService.getAll()
      ]);
      setLlms(llmsData);
      setSalidas(salidasData);
      
      // Seleccionar primer LLM por defecto
      if (llmsData.length > 0) {
        setForm(prev => ({ ...prev, llm_id: llmsData[0].id }));
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSalida = (salidaId) => {
    setForm(prev => ({
      ...prev,
      salidas_ids: prev.salidas_ids.includes(salidaId)
        ? prev.salidas_ids.filter(id => id !== salidaId)
        : [...prev.salidas_ids, salidaId]
    }));
  };

  const handleGenerar = async () => {
    if (!form.llm_id || form.salidas_ids.length === 0) {
      alert('Selecciona un LLM y al menos una salida');
      return;
    }

    setGenerando(true);
    setResultado(null);

    try {
      const resultado = await generacionService.generarSalidas({
        noticia_id: noticia.id,
        ...form
      });
      
      setResultado(resultado);
      
      // Notificar éxito después de 2 segundos
      setTimeout(() => {
        onSuccess && onSuccess(resultado);
      }, 2000);
      
    } catch (err) {
      alert('Error al generar: ' + (err.response?.data?.detail || err.message));
    } finally {
      setGenerando(false);
    }
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
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-8">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500 mx-auto" />
          <p className="mt-4 text-gray-600 dark:text-gray-400">Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-start p-6 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Zap className="w-6 h-6 text-yellow-500" />
              Generar Salidas con IA
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {noticia.titulo}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Resultado */}
          {resultado && (
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5" />
                <div className="flex-1">
                  <h3 className="font-semibold text-green-900 dark:text-green-100">
                    ✅ Generación Completada
                  </h3>
                  <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                    {resultado.salidas_generadas.length} salida(s) generada(s)
                  </p>
                  <div className="text-xs text-green-600 dark:text-green-400 mt-2 space-y-1">
                    <p>⚡ Tokens usados: {resultado.total_tokens.toLocaleString()}</p>
                    <p>⏱️ Tiempo: {(resultado.tiempo_total_ms / 1000).toFixed(2)}s</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Selector de LLM */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              🤖 Modelo LLM
            </label>
            <select
              value={form.llm_id}
              onChange={(e) => setForm({ ...form, llm_id: parseInt(e.target.value) })}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
              disabled={generando}
            >
              {llms.map(llm => (
                <option key={llm.id} value={llm.id}>
                  {llm.nombre} ({llm.proveedor})
                </option>
              ))}
            </select>
          </div>

          {/* Selector de Salidas */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
              📤 Selecciona Salidas ({form.salidas_ids.length} seleccionadas)
            </label>
            <div className="grid grid-cols-2 gap-3">
              {salidas.map(salida => (
                <button
                  key={salida.id}
                  onClick={() => handleToggleSalida(salida.id)}
                  disabled={generando || !salida.activo}
                  className={`
                    p-4 rounded-lg border-2 text-left transition-all
                    ${form.salidas_ids.includes(salida.id)
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                    }
                    ${!salida.activo ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-2xl">{getSalidaIcon(salida.tipo_salida)}</span>
                    <span className="font-semibold text-gray-900 dark:text-white">
                      {salida.nombre}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {salida.tipo_salida}
                  </p>
                </button>
              ))}
            </div>
          </div>

          {/* Opción Regenerar */}
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="regenerar"
              checked={form.regenerar}
              onChange={(e) => setForm({ ...form, regenerar: e.target.checked })}
              disabled={generando}
              className="w-4 h-4 text-blue-600"
            />
            <label htmlFor="regenerar" className="text-sm text-gray-700 dark:text-gray-300">
              Regenerar si ya existen
            </label>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-3 p-6 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onClose}
            disabled={generando}
            className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
          >
            Cancelar
          </button>
          <button
            onClick={handleGenerar}
            disabled={generando || !form.llm_id || form.salidas_ids.length === 0}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {generando ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Generando...
              </>
            ) : (
              <>
                <Zap className="w-4 h-4" />
                Generar
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default GenerarSalidasModal;
