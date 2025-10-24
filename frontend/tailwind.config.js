/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Habilita dark mode con clase 'dark'
  theme: {
    extend: {
      colors: {
        // Colores personalizados para el tema
        primary: {
          light: '#0066FF',
          DEFAULT: '#0052cc',
          dark: '#3b82f6',
        },
        secondary: {
          light: '#06b6d4',
          DEFAULT: '#0891b2',
          dark: '#22d3ee',
        },
        accent: {
          blue: '#0066FF',
          cyan: '#06b6d4',
          steel: '#475569',
        },
        dark: {
          bg: '#0f172a',
          card: '#1e293b',
          border: '#334155',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Monaco', 'Courier New', 'monospace'],
      },
      boxShadow: {
        'glow-sm': '0 0 10px rgba(59, 130, 246, 0.3)',
        'glow-md': '0 0 20px rgba(59, 130, 246, 0.4)',
        'glow-lg': '0 0 30px rgba(59, 130, 246, 0.5)',
        'neon': '0 0 5px rgba(59, 130, 246, 0.8), 0 0 10px rgba(59, 130, 246, 0.6)',
      },
      animation: {
        'fadeIn': 'fadeIn 0.3s ease-out',
        'slideDown': 'slideDown 0.3s ease-out',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
