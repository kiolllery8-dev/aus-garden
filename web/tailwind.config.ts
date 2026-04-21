import type { Config } from 'tailwindcss';

export default {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        cream: '#FAF6EF',
        sand: '#F1E9D9',
        moss: '#6B7A4F',
        forest: '#3F4A2E',
        clay: '#C89B6B',
        ink: '#2A2A28',
      },
      fontFamily: {
        serif: ['"Noto Serif TC"', 'Georgia', 'serif'],
        sans: ['"Noto Sans TC"', 'system-ui', 'sans-serif'],
      },
      container: {
        center: true,
        padding: '1.25rem',
      },
    },
  },
  plugins: [],
} satisfies Config;
