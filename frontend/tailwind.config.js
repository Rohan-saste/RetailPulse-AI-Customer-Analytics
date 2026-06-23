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
        primary: '#2563EB',
        success: '#22C55E',
        warning: '#F59E0B',
        danger: '#EF4444',
        background: '#F1F5F9',
        card: '#FFFFFF',
        textMain: '#0F172A',
        textMuted: '#64748B',
        borderLine: '#E2E8F0',
        sidebar: '#0F172A'
      }
    },
  },
  plugins: [],
}
