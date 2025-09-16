module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        peach: "#FFDAB9",
        peachDark: "#FFB88C",
        orange: {
          300: "#FFB347",
        },
        pink: "#F9E5EF",
        lavender: "#E6E6FA",
        purple: "#B39DDB",
        grayText: "#6B7280",
      },
      fontFamily: {
        sans: ["Quicksand", "Nunito", "Arial", "sans-serif"],
      },
      borderRadius: {
        xl: "1.5rem",
        full: "9999px",
      },
    },
  },
  plugins: [],
}
