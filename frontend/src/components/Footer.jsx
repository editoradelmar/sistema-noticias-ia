import React from 'react';
import { Shield, Sparkles, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Footer() {
  const { user } = useAuth();

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
    <footer className="bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 shadow-inner dark:shadow-glow-sm py-6 mt-8">
      <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="text-slate-500 dark:text-slate-400 text-sm text-center md:text-left">
          &copy; {new Date().getFullYear()} Sistema de Noticias IA. Todos los derechos reservados.
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
  );
}
