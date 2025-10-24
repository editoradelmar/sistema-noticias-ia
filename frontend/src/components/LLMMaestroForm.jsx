import { useState, useEffect } from 'react';

// Obtener proveedor/modelo/url_api default desde variables de entorno
const DEFAULT_LLM_PROVEEDOR = import.meta.env.VITE_DEFAULT_LLM_PROVEEDOR || 'Google';
const DEFAULT_LLM_MODELO_ID = import.meta.env.VITE_DEFAULT_LLM_MODELO_ID || '';
const DEFAULT_LLM_URL_API = import.meta.env.VITE_DEFAULT_LLM_URL_API || 'https://generativelanguage.googleapis.com/v1beta/models/';
import { llmService } from '../services/maestros';
import { X, Save, Bot, AlertCircle } from 'lucide-react';

const LLMMaestroForm = ({ llm, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    proveedor: DEFAULT_LLM_PROVEEDOR,
    modelo_id: DEFAULT_LLM_MODELO_ID,
    api_key: '',
    url_api: DEFAULT_LLM_URL_API, // Por defecto desde variable de entorno
    costo_entrada: 0,
    costo_salida: 0,
    limite_diario_tokens: 1000000,
    activo: true,
  });
  const [proveedores, setProveedores] = useState([]);
  // Cargar proveedores únicos desde la base de datos
  useEffect(() => {
    const fetchProveedores = async () => {
      try {
        const llms = await llmService.getAll();
        // Extraer proveedores únicos
        const unique = Array.from(new Set(llms.map(l => l.proveedor)));
        setProveedores(unique);
      } catch (err) {
        setProveedores([]);
      }
    };
    fetchProveedores();
  }, []);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (llm) {
      setFormData({
        nombre: llm.nombre || '',
        proveedor: llm.proveedor || DEFAULT_LLM_PROVEEDOR,
        modelo_id: llm.modelo_id || DEFAULT_LLM_MODELO_ID,
        api_key: '', // Siempre vacío por seguridad
        url_api: llm.url_api || DEFAULT_LLM_URL_API,
        costo_entrada: llm.costo_entrada || 0,
        costo_salida: llm.costo_salida || 0,
        limite_diario_tokens: llm.limite_diario_tokens || 1000000,
        activo: llm.activo !== undefined ? llm.activo : true,
      });
    } else {
      // Pre-rellenar URL API para el proveedor por defecto
      setFormData(prev => ({ ...prev, url_api: DEFAULT_LLM_URL_API }));
    }
  }, [llm]);

  const handleChange = async (e) => {
    const { name, value, type, checked } = e.target;
    const newFormData = {
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    };

    // Si cambia el proveedor, sugerir la URL API del primer modelo activo de ese proveedor
    if (name === 'proveedor') {
      try {
        const llms = await llmService.getAll({ proveedor: value, activo: true });
        if (llms.length > 0) {
          newFormData.url_api = llms[0].url_api;
        } else {
          newFormData.url_api = '';
        }
      } catch {
        newFormData.url_api = '';
      }
    }
    setFormData(newFormData);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.nombre || !formData.modelo_id || !formData.url_api) {
      setError('Nombre, Modelo ID y URL API son obligatorios.');
      return;
    }
    if (!llm && !formData.api_key) {
      setError('API Key es obligatoria al crear un nuevo modelo.');
      return;
    }

    setLoading(true);
    setError('');

    const dataToSave = {
        ...formData,
        costo_entrada: parseFloat(formData.costo_entrada) || 0,
        costo_salida: parseFloat(formData.costo_salida) || 0,
        limite_diario_tokens: parseInt(formData.limite_diario_tokens, 10) || 0,
    };
    
    onSave(dataToSave, setLoading, setError);
  };

  const inputClasses = "w-full px-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-colors";
  const labelClasses = "block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2";

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50 p-4 backdrop-blur-sm">
      <div className="w-full max-w-3xl mx-auto">
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl dark:shadow-glow-md overflow-hidden border border-slate-200 dark:border-slate-700">
          {/* Header */}
          <div className="bg-gradient-to-r from-slate-700 to-slate-900 dark:from-slate-800 dark:to-black p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-white/20 dark:bg-black/20 rounded-lg backdrop-blur-sm">
                  <Bot className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">
                    {llm ? 'Editar' : 'Nuevo'} Modelo LLM
                  </h2>
                  <p className="text-slate-300 dark:text-slate-400 text-sm">
                    {llm ? 'Actualiza la configuración del modelo' : 'Añade un nuevo proveedor de IA al sistema'}
                  </p>
                </div>
              </div>
              <button
                onClick={onCancel}
                className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition-all"
              >
                <X className="w-6 h-6 text-white" />
              </button>
            </div>
          </div>

          {/* Formulario */}
          <form onSubmit={handleSubmit} className="p-8 space-y-6 max-h-[70vh] overflow-y-auto">
            {error && (
              <div className="flex items-start gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
              </div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className={labelClasses}>Nombre *</label>
                <input type="text" name="nombre" value={formData.nombre} onChange={handleChange} className={inputClasses} required />
              </div>
              <div>
                <label className={labelClasses}>Proveedor *</label>
                <select name="proveedor" value={formData.proveedor} onChange={handleChange} className={inputClasses}>
                  <option value="" disabled>Seleccione un proveedor</option>
                  {proveedores.map(p => (
                    <option key={p} value={p}>{p}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className={labelClasses}>Modelo ID *</label>
              <input type="text" name="modelo_id" value={formData.modelo_id} onChange={handleChange} className={inputClasses} placeholder="Ej: claude-3-sonnet-20240229" required />
            </div>

            <div>
              <label className={labelClasses}>URL API *</label>
              <input type="text" name="url_api" value={formData.url_api} onChange={handleChange} className={inputClasses} placeholder="URL del endpoint del API" required />
            </div>

            <div>
              <label className={labelClasses}>API Key {llm ? '(Opcional)' : '*'}</label>
              <input type="password" name="api_key" value={formData.api_key} onChange={handleChange} className={inputClasses} placeholder={llm ? 'Dejar en blanco para no cambiar' : 'Introduce tu clave de API'} required={!llm} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className={labelClasses}>Costo Entrada</label>
                <input type="number" name="costo_entrada" step="0.000001" value={formData.costo_entrada} onChange={handleChange} className={inputClasses} />
              </div>
              <div>
                <label className={labelClasses}>Costo Salida</label>
                <input type="number" name="costo_salida" step="0.000001" value={formData.costo_salida} onChange={handleChange} className={inputClasses} />
              </div>
              <div>
                <label className={labelClasses}>Límite Tokens Diario</label>
                <input type="number" name="limite_diario_tokens" value={formData.limite_diario_tokens} onChange={handleChange} className={inputClasses} />
              </div>
            </div>

            <div className="flex items-center pt-2">
              <input type="checkbox" name="activo" checked={formData.activo} onChange={handleChange} className="h-5 w-5 text-blue-600 border-slate-300 dark:border-slate-600 rounded focus:ring-blue-500 bg-slate-100 dark:bg-slate-700" />
              <label className="ml-3 text-sm font-medium text-slate-700 dark:text-slate-300">Activo</label>
            </div>

            
            {/* Botones */}
            <div className="flex gap-4 pt-4">
              <button type="button" onClick={onCancel} className="flex-1 px-6 py-3 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 font-semibold rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all border border-slate-300 dark:border-slate-700">
                Cancelar
              </button>
              <button type="submit" disabled={loading} className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed shadow-md dark:shadow-glow-sm transition-all">
                {loading ? (
                  <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> Guardando...</>
                ) : (
                  <><Save className="w-5 h-5" /> {llm ? 'Actualizar' : 'Crear Modelo'}</>
                )}
              </button>
            </div>
          </form>

          {/* Info adicional */}
          <div className="bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-700 p-6">
            <h3 className="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">💡 Consejos:</h3>
            <ul className="space-y-2 text-sm text-slate-600 dark:text-slate-400">
              <li className="flex items-start gap-2"><span className="text-blue-600 dark:text-blue-400 font-bold">•</span><span>El **Modelo ID** debe ser el identificador exacto que usa el proveedor (ej: `gpt-4-turbo`).</span></li>
              <li className="flex items-start gap-2"><span className="text-blue-600 dark:text-blue-400 font-bold">•</span><span>Los costos se calculan por cada 1,000 tokens. Usa `.` como separador decimal.</span></li>
              <li className="flex items-start gap-2"><span className="text-blue-600 dark:text-blue-400 font-bold">•</span><span>La **URL API** cambia según el proveedor. El sistema sugiere una al seleccionar el proveedor.</span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LLMMaestroForm;
