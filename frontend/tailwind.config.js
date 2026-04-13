module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        secondary: '#9B1B30',
        accent: '#DC143C',
        dark: '#2D1018',
        'dark-light': '#3E1A24',
        cream: '#FAF8F5',
        'cream-dark': '#F0ECE6',
        'cream-darker': '#E5DFD8',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03)',
        'card': '0 1px 3px rgba(0,0,0,0.06), 0 8px 24px -4px rgba(45,16,24,0.06)',
        'elevated': '0 4px 6px -1px rgba(0,0,0,0.06), 0 12px 40px -4px rgba(45,16,24,0.1)',
        'modal': '0 24px 48px -12px rgba(0,0,0,0.25)',
      },
      borderRadius: {
        'xl': '0.875rem',
        '2xl': '1rem',
        '3xl': '1.25rem',
      },
    },
  },
  plugins: [],
}
