/**
 * Configuración centralizada de la aplicación frontend
 * Maneja variables de entorno y configuración del sistema
 */

// Variables de entorno con defaults
const getEnvVar = (name, defaultValue = '') => {
  return import.meta.env[name] || defaultValue;
};

// Configuración de la aplicación
export const appConfig = {
  // Información de la aplicación
  APP_NAME: getEnvVar('VITE_APP_NAME', 'Sistema de Noticias con IA'),
  VERSION: getEnvVar('VITE_APP_VERSION', '2.4.0'),
  DESCRIPTION: getEnvVar('VITE_APP_DESCRIPTION', 'Sistema profesional de gestión de noticias con IA'),
  
  // Información del autor/empresa
  COMPANY: getEnvVar('VITE_COMPANY', 'Editor del Mar SA'),
  AUTHOR: getEnvVar('VITE_AUTHOR', 'Hector Romero'),
  EMAIL: getEnvVar('VITE_EMAIL', 'hromero@eluniversal.com.co'),
  
  // URLs y APIs
    // Resolver la URL base de la API con esta prioridad:
    // 1. Variable de entorno VITE_API_BASE_URL (si está definida)
    // 2. Si la app se sirve desde un host público (p.ej. ngrok) usar el origin actual
    // 3. Por defecto usar http://localhost:8000
    API_BASE_URL: (() => {
      const env = getEnvVar('VITE_API_BASE_URL', '');
      if (env && env.trim() !== '') return env;
      try {
        if (typeof window !== 'undefined' && window.location && window.location.hostname) {
          const hn = window.location.hostname;
          // Si no es un host local, asumir que la API está disponible en el mismo origin
          if (hn !== 'localhost' && !hn.startsWith('127.') && hn !== '') {
            return `${window.location.protocol}//${window.location.host}`;
          }
        }
      } catch (e) {
        // entorno de build/server donde window no existe
      }
      return 'http://localhost:8000';
    })(),
  
  // Configuración de desarrollo
  IS_DEVELOPMENT: import.meta.env.MODE === 'development',
  IS_PRODUCTION: import.meta.env.MODE === 'production',
  
  // Configuración de la UI
  THEME: {
    DEFAULT_MODE: getEnvVar('VITE_DEFAULT_THEME', 'light'), // 'light', 'dark', 'auto'
    LOGO_URL: getEnvVar('VITE_LOGO_URL', ''),
  },
  
  // Límites y configuración
  LIMITS: {
    MAX_FILE_SIZE: parseInt(getEnvVar('VITE_MAX_FILE_SIZE', '10485760')), // 10MB
    MAX_CONTENT_LENGTH: parseInt(getEnvVar('VITE_MAX_CONTENT_LENGTH', '10000')),
    PAGINATION_DEFAULT: parseInt(getEnvVar('VITE_PAGINATION_DEFAULT', '12')),
  },
  
  // Features flags
  FEATURES: {
    ADMIN_PANEL: getEnvVar('VITE_FEATURE_ADMIN_PANEL', 'true') === 'true',
    METRICS: getEnvVar('VITE_FEATURE_METRICS', 'false') === 'true',
    DRAG_DROP: getEnvVar('VITE_FEATURE_DRAG_DROP', 'true') === 'true',
    QUICK_LOGIN: getEnvVar('VITE_FEATURE_QUICK_LOGIN', 'true') === 'true',
  },
  
  // Información de build
  BUILD_INFO: {
    BUILD_TIME: getEnvVar('VITE_BUILD_TIME', new Date().toISOString()),
    GIT_COMMIT: getEnvVar('VITE_GIT_COMMIT', 'unknown'),
    BUILD_NUMBER: getEnvVar('VITE_BUILD_NUMBER', '1'),
  }
};

// Función helper para obtener el nombre completo de la app
export const getAppTitle = () => {
  return `${appConfig.APP_NAME} v${appConfig.VERSION}`;
};

// Función helper para obtener información del copyright
export const getCopyright = () => {
  const year = new Date().getFullYear();
  return `© ${year} ${appConfig.COMPANY}. Todos los derechos reservados.`;
};

// Función helper para verificar si una feature está habilitada
export const isFeatureEnabled = (featureName) => {
  return appConfig.FEATURES[featureName] || false;
};

// Exportar configuración por defecto
export default appConfig;

// Logging de configuración en desarrollo
if (appConfig.IS_DEVELOPMENT) {
  console.group('🔧 Configuración de la Aplicación');
  console.log('📦 Aplicación:', getAppTitle());
  console.log('🏢 Empresa:', appConfig.COMPANY);
  console.log('🌐 API Base:', appConfig.API_BASE_URL);
  console.log('🎨 Tema:', appConfig.THEME.DEFAULT_MODE);
  console.log('🚀 Features:', appConfig.FEATURES);
  console.groupEnd();
}