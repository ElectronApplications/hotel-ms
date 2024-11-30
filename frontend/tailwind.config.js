/** @type {import('tailwindcss').Config} */

import defaultTheme from "tailwindcss/defaultTheme";
import colors from "tailwindcss/colors";

export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["InterVariable", ...defaultTheme.fontFamily.sans],
      },
      colors: {
        background: {
          light: "#F6F3E9",
          dark: "#242424",
          "content-light": colors.black,
          "content-dark": colors.white,
        },
        surface: {
          light: colors.white,
          dark: "#353535",
          "content-light": colors.black,
          "content-dark": colors.white,
        },
        primary: {
          light: colors.orange[500],
          dark: colors.orange[600],
          "active-light": colors.orange[600],
          "active-dark": colors.orange[700],
          "content-light": colors.white,
          "content-dark": colors.gray[100],
        },
        secondary: {
          light: "#D0D0D0",
          dark: "#4A4A4A",
          "active-light": "#909090",
          "active-dark": "#5A5A5A",
          "content-light": colors.black,
          "content-dark": colors.gray[100],
        },
      },
    },
  },
  plugins: [],
};
