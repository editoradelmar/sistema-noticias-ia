import React, { useState } from 'react';
import { Shield, Sparkles, User, Settings, Users } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import UsuariosAdminCompleto from './admin/UsuariosAdminSimple';
import { getCopyright } from '../config/appConfig';

export default function Footer() {
  const { user, isAdmin } = useAuth();
  const [showAdminPanel, setShowAdminPanel] = useState(false);

  const getRoleBadge = () => {
    const badges = {
      admin: {
        color: 'bg-red-600 dark:bg-red-500',
        icon: Shield,
        text: 'Administrador',
      },
      editor: {
        color: 'bg-emerald-600 dark:bg-emerald-500',
        icon: Sparkles,
        text: 'Editor',
      },
      viewer: {
        color: 'bg-blue-600 dark:bg-blue-500',
        icon: User,
        text: 'Lector',
      },
    };
    const badge = badges[user?.role] || badges.viewer;
    const Icon = badge.icon;
    return (
      <div className={`flex items-center gap-2 px-3 py-1.5 ${badge.color} rounded-md text-white text-sm font-bold shadow-md dark:shadow-glow-sm`}>
        <Icon className="w-4 h-4" />
        <span>{badge.text}</span>
      </div>
    );
  };

  return (
    <>
      {/* Modal de Administración de Usuarios */}
      {showAdminPanel && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-slate-800 rounded-lg shadow-xl max-w-6xl w-full max-h-[85vh] overflow-hidden flex flex-col">
            <div className="flex items-center justify-between p-6 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
              <div className="flex items-center gap-3">
                <Users className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                  Administración de Usuarios
                </h2>
              </div>
              <button
                onClick={() => setShowAdminPanel(false)}
                className="text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 p-1 rounded-md hover:bg-slate-100 dark:hover:bg-slate-700"
              >
                <span className="sr-only">Cerrar</span>
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-6">
              <UsuariosAdminCompleto onClose={() => setShowAdminPanel(false)} />
            </div>
          </div>
        </div>
      )}

      <footer className="bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 shadow-inner dark:shadow-glow-sm py-6 mt-8">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-6">
            <div className="text-slate-500 dark:text-slate-400 text-sm text-center md:text-left">
              {getCopyright()}
            </div>
            
            {/* Panel de Administración - Solo para Admins */}
            {isAdmin() && (
              <button
                onClick={() => setShowAdminPanel(true)}
                className="flex items-center gap-2 px-3 py-1.5 bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 text-white text-sm font-medium rounded-md transition-colors shadow-md hover:shadow-lg"
                title="Administrar Usuarios"
              >
                <Settings className="w-4 h-4" />
                <span className="hidden sm:inline">Admin Panel</span>
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-4 bg-slate-900/90 border border-slate-700 rounded-xl px-6 py-3 shadow-lg">
            <div className="text-right mr-2">
              <p className="text-base font-bold text-white">
                {user?.nombre_completo || user?.username || 'Usuario'}
              </p>
              <p className="text-xs text-slate-300">{user?.email}</p>
            </div>
            {getRoleBadge()}
          </div>
        </div>
      </footer>
    </>
  );
}
