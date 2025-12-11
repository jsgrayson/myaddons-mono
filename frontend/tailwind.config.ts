import type { Config } from 'tailwindcss';

export default {
    content: [
        "./index.html",
        "./*.{js,ts,jsx,tsx}",
        "./components/**/*.{js,ts,jsx,tsx}",
        "./services/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Theme: Arcane (Default/Hub)
                'arcane-bg': '#0f0c29',
                'arcane-glass': 'rgba(48, 43, 99, 0.6)',
                'arcane-border': '#00d2ff',
                'arcane-text': '#e0e7ff',

                // Theme: Industrial (DeepPockets)
                'industrial-bg': '#1a1a1a',
                'industrial-glass': 'rgba(30, 30, 30, 0.8)',
                'industrial-border': '#ff8c00', // Dark Orange
                'industrial-text': '#f5f5f5',

                // Theme: Cyber (GoblinAI)
                'cyber-bg': '#000000',
                'cyber-glass': 'rgba(0, 0, 0, 0.9)',
                'cyber-border': '#00ff00', // Neon Green
                'cyber-text': '#00ff41',

                // Theme: Druid (PetWeaver)
                'druid-bg': '#0a1a0a',
                'druid-glass': 'rgba(20, 40, 20, 0.7)',
                'druid-border': '#50c878', // Emerald
                'druid-text': '#f0e6d2', // Parchment

                // Theme: Titan (SkillWeaver)
                'titan-bg': '#0c1424',
                'titan-glass': 'rgba(20, 40, 80, 0.7)',
                'titan-border': '#d4af37', // Gold
                'titan-text': '#cfe2f3',

                // Legacy/Shared
                'azeroth-gold': '#d4af37',
                'rarity-legendary': '#ff8000',
                'rarity-epic': '#a335ee',
                'rarity-rare': '#0070dd',
                'resource-health': '#2ecc71',
                'resource-mana': '#3498db',
            },
            fontFamily: {
                'warcraft': ['Beaufort', 'serif'], // Placeholder for WoW font
                'mono': ['"Fira Code"', 'monospace'],
                'sans': ['Inter', 'sans-serif'],
            },
            boxShadow: {
                'glow-gold': '0 0 10px rgba(212, 175, 55, 0.5)',
                'glow-arcane': '0 0 10px rgba(0, 210, 255, 0.5)',
                'inset': 'inset 0 0 10px rgba(0,0,0,0.5)',
            },
            animation: {
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            }
        },
    },
    plugins: [],
} satisfies Config;
