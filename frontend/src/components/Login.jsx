import React, { useState } from 'react';
import { LogIn, Mail, Lock, Loader2, AlertCircle, Sun, Moon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export default function Login({ onSwitchToRegister }) {
  const { login } = useAuth();
  const { theme, toggleTheme, isDark } = useTheme();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(formData.email, formData.password);

    if (!result.success) {
      setError(result.error || 'Login failed');
      setLoading(false);
    }
  };

  const quickLogin = async (email, password) => {
    setFormData({ email, password });
    setError('');
    setLoading(true);
    const result = await login(email, password);
    if (!result.success) {
      setError(result.error);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 dark:from-black dark:via-slate-900 dark:to-black p-4 transition-colors duration-300">
      {/* Efectos de fondo */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-96 h-96 bg-blue-600 rounded-full blur-3xl opacity-20 dark:opacity-10 animate-pulse"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-600 rounded-full blur-3xl opacity-20 dark:opacity-10 animate-pulse delay-1000"></div>
      </div>

      <div className="relative w-full max-w-md">
        {/* Toggle de tema flotante */}
        <div className="absolute -top-16 right-0">
          <button
            onClick={toggleTheme}
            className="p-3 bg-white/10 dark:bg-white/5 backdrop-blur-lg text-white rounded-lg hover:bg-white/20 dark:hover:bg-white/10 transition-all duration-300 border border-white/20 dark:border-white/10"
            title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          >
            {isDark ? (
              <Sun className="w-6 h-6 text-yellow-400" />
            ) : (
              <Moon className="w-6 h-6 text-blue-300" />
            )}
          </button>
        </div>

        {/* Card Principal */}
        <div className="bg-white/95 dark:bg-slate-900/95 backdrop-blur-xl rounded-lg shadow-2xl dark:shadow-glow-lg p-8 border border-white/30 dark:border-slate-700">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-block p-4 bg-gradient-to-br from-blue-600 to-cyan-600 dark:from-blue-500 dark:to-cyan-500 rounded-lg shadow-lg dark:shadow-glow-md mb-4">
              <LogIn className="w-12 h-12 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
              Bienvenido nuevamente
            </h2>
            <p className="text-slate-600 dark:text-slate-400 mt-2">Inicie sesión en su cuenta</p>
          </div>

          {/* Error Alert */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-lg flex items-start gap-3 animate-fadeIn">
              <AlertCircle className="w-5 h-5 text-red-500 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-red-800 dark:text-red-400 font-semibold text-sm">Error de inicio de sesión</p>
                <p className="text-red-600 dark:text-red-500 text-sm">{error}</p>
              </div>
            </div>
          )}
          {/* Formulario */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email */}
            <div>
              <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
                Correo electrónico
              </label>
              <div className="relative">
                <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5" />
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full pl-12 pr-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 transition-all duration-300"
                  placeholder="correo@ejemplo.com"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">
                Contraseña
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 dark:text-slate-500 w-5 h-5" />
                <input
                  type="password"
                  required
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full pl-12 pr-4 py-3 border-2 border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-blue-500 dark:focus:border-blue-400 transition-all duration-300"
                  placeholder="••••••••"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-500 dark:to-cyan-500 text-white font-bold rounded-lg hover:from-blue-700 hover:to-cyan-700 dark:hover:from-blue-600 dark:hover:to-cyan-600 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg dark:shadow-glow-md hover:shadow-xl dark:hover:shadow-glow-lg transform hover:scale-[1.02] transition-all duration-300 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Ingresando...</span>
                </>
              ) : (
                <>
                  <LogIn className="w-5 h-5" />
                  <span>Ingresar</span>
                </>
              )}
            </button>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white dark:bg-slate-900 text-slate-500 dark:text-slate-400 font-medium">o</span>
            </div>
          </form>

          {/* Register Link */}
          <div className="text-center">
            <p className="text-slate-600 dark:text-slate-400">
              ¿No posee una cuenta?{' '}
              <button
                type="button"
                onClick={onSwitchToRegister}
                className="font-bold text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors"
              >
                Regístrese aquí
              </button>
            </p>
          </div>

          {/* Quick Login (Development) */}
          <div className="mt-6 pt-6 border-t-2 border-slate-100 dark:border-slate-800">
            <p className="text-xs text-slate-500 dark:text-slate-500 text-center mb-3">Acceso rápido (Desarrollo)</p>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => quickLogin('admin@sistema.com', 'admin123456')}
                disabled={loading}
                className="px-3 py-2 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 text-xs font-bold rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 disabled:opacity-50 transition-colors border border-red-200 dark:border-red-800"
              >
                Administrador
              </button>
              <button
                type="button"
                onClick={() => quickLogin('editor@sistema.com', 'editor123')}
                disabled={loading}
                className="px-3 py-2 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 text-xs font-bold rounded-lg hover:bg-emerald-100 dark:hover:bg-emerald-900/30 disabled:opacity-50 transition-colors border border-emerald-200 dark:border-emerald-800"
              >
                Editor
              </button>
              <button
                type="button"
                onClick={() => quickLogin('viewer@sistema.com', 'viewer123')}
                disabled={loading}
                className="px-3 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 text-xs font-bold rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 disabled:opacity-50 transition-colors border border-blue-200 dark:border-blue-800"
              >
                Lector
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-white/90 dark:text-slate-400 text-sm mt-6 font-medium">
          News System with AI v2.1.0
        </p>
      </div>
    </div>
  );
}
