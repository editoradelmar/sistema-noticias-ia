import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0', // Permitir conexiones externas
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '172.17.100.64',
      '192.168.0.100',
      '192.168.1.100',
      'woodcock-still-tetra.ngrok-free.app'
    ],
    proxy: {
      // Proxy para evitar CORS en desarrollo
      '/api': {
        target: 'http://172.17.100.64:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    // Optimización para producción
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'icons': ['lucide-react']
        }
      }
    }
  }
})