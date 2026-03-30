module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        secondary: '#9B1B30',    // Burgundy
        accent: '#DC143C',       // Bright red
        dark: '#4A1C2A',         // Dark burgundy
        cream: '#F0EBE4',        // Warm off-white (main content)
        'cream-dark': '#E5DED5', // Slightly darker warm white (inner cards)
      }
    },
  },
  plugins: [],
}
