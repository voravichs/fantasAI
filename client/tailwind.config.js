/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
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