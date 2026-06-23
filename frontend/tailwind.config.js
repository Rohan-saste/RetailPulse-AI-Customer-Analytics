/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'sans-serif'],
      },
      colors: {
        background: '#F8FAFC',
        sidebar: '#0F172A',
        card: '#FFFFFF',
        textMain: '#1E293B',
        textMuted: '#94A3B8',
        accentBlue: '#3B82F6',
        accentGreen: '#10B981',
        accentPurple: '#8B5CF6',
        accentOrange: '#F59E0B'
      }
    },
  },
  plugins: [],
}
