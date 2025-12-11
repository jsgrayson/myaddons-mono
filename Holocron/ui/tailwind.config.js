/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                rust: {
                    base: '#d35400',
                    dark: '#a04000',
                    orange: '#d35400', // Primary Brand
                },
                gold: {
                    DEFAULT: '#b8860b', // Dark Gold/Brass
                    text: '#fcd34d',   // Gold text for numbers
                },
                oil: {
                    black: '#1a1a1a', // Oil Black
                },
                hazard: {
                    green: '#39ff14', // Slime Green
                    red: '#ff003c',   // Explosion Red
                    white: '#e5e7eb', // Dirty White
                }
            },
            fontFamily: {
                vt323: ['"VT323"', 'monospace'],
                heading: ['"Black Ops One"', 'cursive'],
                subheading: ['"Chakra Petch"', 'sans-serif'],
                mono: ['"Share Tech Mono"', 'monospace'],
            },
            animation: {
                'shimmer': 'shimmer 2s infinite linear',
                'ticker-vertical': 'tickerVertical 10s linear infinite',
            },
            keyframes: {
                tickerVertical: {
                    '0%': { transform: 'translateY(0)' },
                    '100%': { transform: 'translateY(-50%)' }
                }
            }
        },
    },
    plugins: [],
}
