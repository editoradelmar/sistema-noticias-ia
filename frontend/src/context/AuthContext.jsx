import React, { createContext, useState, useContext, useEffect } from 'react';
import axiosInstance, { api } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Cargar usuario del localStorage al iniciar
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  // Login
  const login = async (email, password) => {
    try {
      // OAuth2 form data
      const formData = new URLSearchParams();
      formData.append('username', email); // OAuth2 usa 'username' pero mandamos el email
      formData.append('password', password);

  const response = await fetch(`${axiosInstance.defaults.baseURL.replace(/\/$/, '')}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error en el login');
      }

      const data = await response.json();
      
      // Guardar token y usuario
      setToken(data.access_token);
      setUser(data.user);
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      return { success: true };
    } catch (error) {
      console.error('Error en login:', error);
      return { success: false, error: error.message };
    }
  };

  // Register
  const register = async (email, username, password, nombre_completo = '') => {
    try {
  const response = await fetch(`${axiosInstance.defaults.baseURL.replace(/\/$/, '')}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          username,
          password,
          nombre_completo,
          role: 'viewer' // Por defecto viewer
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error en el registro');
      }

      const data = await response.json();
      
      // Auto-login después del registro
      return await login(email, password);
    } catch (error) {
      console.error('Error en register:', error);
      return { success: false, error: error.message };
    }
  };

  // Logout
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  // Verificar si el usuario tiene permiso
  const hasRole = (roles) => {
    if (!user) return false;
    if (typeof roles === 'string') {
      return user.role === roles;
    }
    return roles.includes(user.role);
  };

  // Puede crear/editar noticias
  const canEdit = () => {
    return hasRole(['admin', 'editor']);
  };

  // Es admin
  const isAdmin = () => {
    return hasRole('admin');
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    hasRole,
    canEdit,
    isAdmin,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
};
