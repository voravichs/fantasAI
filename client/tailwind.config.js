/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        header: '#ba69a6',
      },
      fontFamily: {
        'title': ["Black Chancery", "serif"],
      },
      fontSize: {
        'title': '10rem'
      }
    },
  },
  plugins: [],
}