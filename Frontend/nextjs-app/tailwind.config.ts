import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0f172a', // slate-900
        muted: '#f1f5f9',   // slate-100
        brand: '#2563eb',   // blue-600
        warn: '#fef3c7',    // amber-100
        warnBorder: '#f59e0b', // amber-500
      },
      boxShadow: {
        card: '0 2px 10px rgba(0,0,0,0.05)'
      }
    },
  },
  plugins: [],
}
export default config
