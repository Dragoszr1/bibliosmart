module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Golden and burgundy to bright red theme
        primary: '#D4AF37',      // Golden
        secondary: '#9B1B30',    // Burgundy
        accent: '#DC143C',       // Bright red
        dark: '#4A1C2A',         // Dark burgundy
        gold: '#FFD700',         // Bright gold
        cream: '#F0EBE4',        // Warm off-white (main content)
        'cream-dark': '#E5DED5', // Slightly darker warm white (inner cards)
      }
    },
  },
  plugins: [],
}
