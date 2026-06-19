/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0B0D17',
          card: '#121626',
          cardHover: '#181C2E',
          border: '#1F243B',
          surface: 'rgba(18, 22, 38, 0.7)',
        },
        severity: {
          stable: '#10B981',
          elevated: '#F59E0B',
          high: '#EF4444',
          critical: '#B91C1C',
          emergency: '#8B5CF6',
        },
        brand: {
          primary: '#3B82F6',
          secondary: '#0EA5E9',
          accent: '#6366F1'
        }
      },
      boxShadow: {
        'tactical': '0 4px 20px -2px rgba(0, 0, 0, 0.5)',
        'glow-stable': '0 0 15px rgba(16, 185, 129, 0.3)',
        'glow-elevated': '0 0 15px rgba(245, 158, 11, 0.3)',
        'glow-high': '0 0 20px rgba(239, 68, 68, 0.4)',
        'glow-critical': '0 0 25px rgba(185, 28, 28, 0.6)',
        'glow-emergency': '0 0 30px rgba(139, 92, 246, 0.6)',
        'glass': 'inset 0 1px 0 0 rgba(255, 255, 255, 0.05)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-fast': 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'radar-sweep': 'radar 4s linear infinite',
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
      },
      keyframes: {
        radar: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        }
      }
    },
  },
  plugins: [],
}
