/** @type {import('tailwindcss').Config} */

// tailwind.config.js
module.exports = {
  content: [
    './templates/**/*.html',
    './**/*.html',
    './static/src/**/*.css'
  ],
  
  theme: {
    extend: {
      colors: {
        mint: '#D1F0E1',
        peach: '#FFE0CC',
        pink: '#FFD6E0',
        beige: '#FAF3E0',
        dark: '#222',
        greenish: '#75C9A5', // для акцентов
      }
    },
  },
  plugins: [],
}
