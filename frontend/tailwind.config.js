/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        corpBlue: "#0F4C81",
        corpNavy: "#1A2B49",
        corpGold: "#C9A227",
        bgAlt1: "#F4F6F8",
        bgAlt2: "#EEF2F7",
        cardBg: "#F8FAFC",
        cardBorder: "#DCE3EA",
        corpTextDark: "#1E293B",
        corpTextLight: "#334155",
      },
    },
  },
  plugins: [],
}