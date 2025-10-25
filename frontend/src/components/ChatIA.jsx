import React, { useState, useEffect, useRef } from 'react';

// Defaults centralizados por variable de entorno
const DEFAULT_LLM_PROVEEDOR = import.meta.env.VITE_DEFAULT_LLM_PROVEEDOR || 'Google';
const DEFAULT_LLM_MODELO_ID = import.meta.env.VITE_DEFAULT_LLM_MODELO_ID || '';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { api } from '../services/api';
import { llmService } from '../services/maestros';

export default function ChatIA() {
  const { user } = useAuth();
  const { theme } = useTheme();
  const [mensaje, setMensaje] = useState('');
  const [conversacion, setConversacion] = useState([]);
  const [conversacionId, setConversacionId] = useState(() => localStorage.getItem('conversacionId') || null);
  const chatRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [llms, setLlms] = useState([]);
  const [llmId, setLlmId] = useState('');
  const [lastTokensUsed, setLastTokensUsed] = useState(0);
  const [currentDateTime, setCurrentDateTime] = useState('');

  // Actualizar fecha y hora cada segundo
  useEffect(() => {
    const updateDateTime = () => {
      const now = new Date();
      const fecha = now.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
      const hora = now.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      });
      setCurrentDateTime(`${fecha} - ${hora}`);
    };

    updateDateTime(); // Actualizar inmediatamente
    const interval = setInterval(updateDateTime, 1000); // Actualizar cada segundo

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    llmService.getActivos().then(data => {
      let lista = Array.isArray(data) ? data : (Array.isArray(data?.data) ? data.data : []);
      setLlms(lista);
      if (lista && lista.length > 0) {
        // Prioridad: modelo_id exacto, luego proveedor
        const byModelo = DEFAULT_LLM_MODELO_ID ? lista.find(l => l.modelo_id === DEFAULT_LLM_MODELO_ID) : null;
        const byProveedor = lista.find(l => l.proveedor === DEFAULT_LLM_PROVEEDOR);
        setLlmId(byModelo?.id || byProveedor?.id || lista[0].id);
      }
    });
    
    // Restaurar conversación desde localStorage como backup
    const savedConversacion = localStorage.getItem(`conversacion_${conversacionId}`);
    if (savedConversacion) {
      try {
        setConversacion(JSON.parse(savedConversacion));
      } catch (e) {
        console.warn('Error al cargar conversación guardada:', e);
      }
    }
    
    // Si hay conversacionId previa, restaurar historial del backend
    if (conversacionId) {
      api.getHistorialChat(conversacionId).then(historial => {
        const conversacionBackend = (historial || []).map(msg => ({
          rol: msg.role === 'user' ? 'usuario' : 'ia',
          texto: msg.content
        }));
        setConversacion(conversacionBackend);
        // Guardar en localStorage como backup
        localStorage.setItem(`conversacion_${conversacionId}`, JSON.stringify(conversacionBackend));
      });
    }
  }, []);

  const enviarMensaje = async (e) => {
    e.preventDefault();
    if (!mensaje.trim() || !llmId) return;
    setLoading(true);
    setError(null);
    
    // Mostrar mensaje del usuario de inmediato (optimista)
    setConversacion(prev => ([
      ...prev,
      { rol: 'usuario', texto: mensaje }
    ]));
    let nextConversacionId = conversacionId;
    try {
      // Enviar mensaje y obtener conversacionId actualizado
      const respuesta = await api.chatIA(mensaje, conversacionId, llmId);
      if (respuesta?.conversacion_id) nextConversacionId = respuesta.conversacion_id;
      if (respuesta?.tokens_usados) setLastTokensUsed(respuesta.tokens_usados);
      setConversacionId(nextConversacionId);
      localStorage.setItem('conversacionId', nextConversacionId);
      setMensaje('');
      // Obtener historial real del backend y mapearlo
      const historial = await api.getHistorialChat(nextConversacionId);
      const nuevaConversacion = (historial || []).map(msg => ({
        rol: msg.role === 'user' ? 'usuario' : 'ia',
        texto: msg.content
      }));
      setConversacion(nuevaConversacion);
      
      // Guardar en localStorage como backup
      localStorage.setItem(`conversacion_${nextConversacionId}`, JSON.stringify(nuevaConversacion));
    } catch (err) {
      setError('Error al comunicarse con el modelo IA. ' + (err?.message || ''));
    } finally {
      setLoading(false);
    }
  };

  // Scroll automático al último mensaje
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [conversacion, loading]);

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="bg-white dark:bg-slate-900 rounded-lg shadow-xl border border-slate-200 dark:border-slate-700 w-full max-w-3xl overflow-hidden">
        <div className="bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-700 dark:to-cyan-700 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11v2m0 4h.01M12 7h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <h2 className="text-2xl font-bold text-white">Asistente IA</h2>
            {llms.length > 0 && (
              <select
                className="ml-4 px-2 py-1 rounded bg-white/80 text-slate-800 text-sm font-semibold"
                value={llmId}
                onChange={e => setLlmId(e.target.value)}
                disabled={loading}
              >
                {llms.map(llm => (
                  <option key={llm.id} value={llm.id}>{llm.nombre} {llm.version ? `(${llm.version})` : ''}</option>
                ))}
              </select>
            )}
          </div>
          <button
            className="bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100 px-4 py-2 rounded font-bold hover:bg-slate-300 dark:hover:bg-slate-600 transition text-sm"
            onClick={() => {
              setConversacion([]);
              setMensaje('');
              if (conversacionId) {
                localStorage.removeItem(`conversacion_${conversacionId}`);
              }
              setConversacionId(null);
              localStorage.removeItem('conversacionId');
            }}
            title={`Limpiar conversación (${conversacion.length} mensajes)`}
          >
            Limpiar {conversacion.length > 0 && `(${conversacion.length})`}
          </button>
        </div>
        <div className="p-8">
          <div
            className="mb-6 h-[48vh] min-h-[350px] overflow-y-auto border rounded-lg p-6 pr-4 bg-slate-800 flex flex-col gap-4 justify-center items-center"
            id="chat-scroll"
            ref={chatRef}
            style={{ paddingRight: '1.5rem' }}
          >
            {conversacion.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full w-full">
                <svg xmlns="http://www.w3.org/2000/svg" className="w-16 h-16 text-blue-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11v2m0 4h.01M12 7h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <h3 className="text-2xl font-bold text-slate-100 mb-2">Asistente IA Listo</h3>
                <p className="text-slate-400">Consulte sobre noticias, análisis o preguntas generales.</p>
                <p className="text-slate-500 text-xs mt-2">💡 El historial se mantiene durante toda la sesión</p>
              </div>
            )}
            {conversacion.length > 20 && (
              <div className="w-full text-center mb-4">
                <div className="inline-block px-3 py-1 bg-yellow-600/20 text-yellow-300 rounded-full text-xs">
                  ⚠️ Conversación larga: Solo los últimos 20 mensajes van al LLM para optimizar respuestas
                </div>
              </div>
            )}
            {conversacion.length > 50 && (
              <div className="w-full text-center mb-2">
                <div className="inline-block px-3 py-1 bg-blue-600/20 text-blue-300 rounded-full text-xs">
                  💾 Historial guardado localmente • {conversacion.length} mensajes totales
                </div>
              </div>
            )}
            {conversacion.map((msg, idx) => (
              <div
                key={idx}
                className={`w-full flex ${msg.rol === 'usuario' ? 'justify-end' : 'justify-start'} items-end pr-2`}
              >
                {msg.rol === 'ia' && (
                  <div className="flex-shrink-0 mr-2 hidden sm:block">
                    <svg className="w-7 h-7 text-cyan-400 bg-slate-700 rounded-full p-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11v2m0 4h.01M12 7h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </div>
                )}
                <div
                  className={
                    msg.rol === 'usuario'
                      ? 'px-4 py-3 rounded-2xl max-w-[80vw] sm:max-w-md bg-blue-600 text-white text-right ml-8 shadow-md'
                      : 'px-4 py-3 rounded-2xl max-w-[80vw] sm:max-w-md bg-slate-100 dark:bg-slate-700 text-slate-900 dark:text-blue-200 text-left mr-8 border-l-4 border-blue-400 shadow-lg'
                  }
                >
                  <span className="break-words whitespace-pre-line">{msg.texto}</span>
                </div>
                {msg.rol === 'usuario' && (
                  <div className="flex-shrink-0 ml-2 hidden sm:block">
                    <svg className="w-7 h-7 text-white bg-blue-600 rounded-full p-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A13.937 13.937 0 0112 15c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="w-full flex justify-start pr-2">
                <div className="px-4 py-3 rounded-lg max-w-lg bg-slate-700 text-blue-300 opacity-70 animate-pulse">
                  <span>Pensando...</span>
                </div>
              </div>
            )}
          </div>
          <form onSubmit={enviarMensaje} className="flex gap-2 mt-4">
            <input
              type="text"
              className="flex-1 border-2 border-slate-300 dark:border-slate-600 rounded-lg px-4 py-3 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
              value={mensaje}
              onChange={e => setMensaje(e.target.value)}
              placeholder="Escriba su mensaje..."
              disabled={loading}
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-bold shadow transition disabled:opacity-50"
              disabled={loading || !mensaje.trim()}
            >Enviar</button>
          </form>
          <div className="flex justify-between items-center mt-2 text-xs text-slate-500">
            <div className="flex gap-4">
              {lastTokensUsed > 0 && <span>🎯 Última respuesta: {lastTokensUsed} tokens</span>}
              <span className="text-blue-400">📅 {currentDateTime}</span>
            </div>
            <div>
              {conversacion.length > 0 && <span>💬 {conversacion.length} mensajes</span>}
            </div>
          </div>
          {error && <div className="mt-2 text-red-600">{error}</div>}
        </div>
      </div>
    </div>
  );
}
