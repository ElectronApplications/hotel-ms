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
          "disabled-light": "#D8D8D8",
          "disabled-dark": "#4C4C4C",
          "disabled-content-light": "#909090",
          "disabled-content-dark": "#8D8D8D",
        },
        secondary: {
          light: "#D0D0D0",
          dark: "#4A4A4A",
          "active-light": "#909090",
          "active-dark": "#5A5A5A",
          "content-light": colors.black,
          "content-dark": colors.gray[100],
          "disabled-light": "#D8D8D8",
          "disabled-dark": "#4C4C4C",
          "disabled-content-light": "#909090",
          "disabled-content-dark": "#8D8D8D",
        },
        placeholder: {
          light: "#9CA3AF",
          dark: "#72767D",
        },
        link: {
          light: colors.blue[500],
          dark: colors.blue[400],
        },
      },
    },
  },
  plugins: [],
};
