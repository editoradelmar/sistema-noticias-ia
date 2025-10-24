import React, { useState } from 'react';
import { Newspaper, LogOut, Sun, Moon, Folder, Settings, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';


export default function Header({ vista, setVista }) {
  const { user, logout, isAdmin, canEdit } = useAuth();
  const { theme, toggleTheme, isDark } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);

  // Botones de navegación (reutilizables)
  const navButtons = (
    <>
      <button
        onClick={() => { setVista('noticias'); setMenuOpen(false); }}
        className={`px-5 py-2.5 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 ${
          vista === 'noticias'
            ? 'bg-blue-600 dark:bg-blue-500 text-white shadow-md dark:shadow-glow-sm'
            : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
        }`}
      >
        Noticias
      </button>
      {canEdit() && (
        <button
          onClick={() => { setVista('crear'); setMenuOpen(false); }}
          className={`px-5 py-2.5 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 ${
            vista === 'crear'
              ? 'bg-emerald-600 dark:bg-emerald-500 text-white shadow-md dark:shadow-glow-sm'
              : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
          }`}
        >
          Crear
        </button>
      )}
      <button
        onClick={() => { setVista('proyectos'); setMenuOpen(false); }}
        className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 ${
          vista === 'proyectos'
            ? 'bg-violet-600 dark:bg-violet-500 text-white shadow-md dark:shadow-glow-sm'
            : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
        }`}
      >
        <Folder className="w-4 h-4" />
        Proyectos
      </button>
      <button
        onClick={() => { setVista('chat'); setMenuOpen(false); }}
        className={`px-5 py-2.5 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 ${
          vista === 'chat'
            ? 'bg-cyan-600 dark:bg-cyan-500 text-white shadow-md dark:shadow-glow-sm'
            : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
        }`}
      >
        Chat IA
      </button>
      {isAdmin() && (
        <button
          onClick={() => { setVista('maestros'); setMenuOpen(false); }}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 ${
            vista === 'maestros'
              ? 'bg-orange-600 dark:bg-orange-500 text-white shadow-md dark:shadow-glow-sm'
              : 'bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800'
          }`}
        >
          <Settings className="w-4 h-4" />
          Maestros
        </button>
      )}
    </>
  );

  return (
    <header className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 shadow-md dark:shadow-glow-sm sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo y título */}
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-br from-blue-600 to-cyan-600 dark:from-blue-500 dark:to-cyan-500 rounded-lg shadow-lg dark:shadow-glow-md transform hover:rotate-6 transition-transform duration-300">
              <Newspaper className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-black text-slate-900 dark:text-slate-100">
                Sistema de Noticias <span className="text-blue-600 dark:text-blue-400">IA</span>
              </h1>
              <p className="text-xs font-semibold text-slate-600 dark:text-slate-400 flex items-center gap-2">
                <Sparkles className="w-3 h-3 text-cyan-500 dark:text-cyan-400" />
                FastAPI + React + Multi Modelo
              </p>
            </div>
          </div>

          {/* Botón hamburguesa en móvil */}
          <div className="flex items-center gap-4">
            <button
              className="md:hidden p-3 rounded-lg bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 focus:outline-none"
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label="Abrir menú"
            >
              {/* Icono hamburguesa */}
              <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            {/* Menú de navegación (escritorio) */}
            <div className="hidden md:flex gap-2">
              {navButtons}
            </div>

            {/* Toggle de tema y logout (siempre visibles) */}
            <button
              onClick={toggleTheme}
              className="p-3 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 transition-all duration-300 transform hover:scale-110 border border-slate-200 dark:border-slate-700"
              title={isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
            >
              {isDark ? (
                <Sun className="w-5 h-5 text-yellow-500" />
              ) : (
                <Moon className="w-5 h-5 text-blue-600" />
              )}
            </button>
            <button
              onClick={logout}
              className="p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-600 hover:text-white dark:hover:bg-red-600 transition-all duration-300 transform hover:scale-110 border border-red-200 dark:border-red-800"
              title="Cerrar sesión"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Menú móvil: panel lateral */}
      {menuOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 md:hidden" onClick={() => setMenuOpen(false)}>
          <nav
            className="absolute top-0 right-0 w-64 h-full bg-white dark:bg-slate-800 shadow-lg dark:shadow-glow-md p-6 flex flex-col gap-4 animate-slideDown"
            onClick={e => e.stopPropagation()}
          >
            <button
              className="self-end mb-4 p-2 rounded hover:bg-slate-200 dark:hover:bg-slate-700"
              onClick={() => setMenuOpen(false)}
              aria-label="Cerrar menú"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            {navButtons}
          </nav>
        </div>
      )}
    </header>
  );
}
