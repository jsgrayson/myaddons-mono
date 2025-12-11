/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx,js,jsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          base: '#07070b',
          panel: '#151320',
          panelSoft: '#1d1a2a'
        },
        ember: {
          light: '#ffcc66',
          mid: '#f39c37',
          deep: '#d66b1b'
        },
        arcane: {
          light: '#8fd7ff',
          mid: '#6ccfff',
          deep: '#2f6f9f'
        },
        pet: {
          beast: '#D37A2C',
          mechanical: '#91A2C9',
          dragonkin: '#A864D3',
          magic: '#6CB0F7',
          undead: '#8E8E8E',
          aquatic: '#4FB7A1',
          flying: '#F0D36C',
          humanoid: '#C67F59',
          critter: '#C9C67A'
        }
      },
      boxShadow: {
        ember: '0 0 30px rgba(243,156,55,0.45)',
        emberSoft: '0 0 18px rgba(243,156,55,0.25)',
        arcane: '0 0 30px rgba(111,207,255,0.45)'
      },
      backgroundImage: {
        'ember-gradient':
          'radial-gradient(circle at 10% 0%, rgba(243,156,55,0.22), transparent 60%), radial-gradient(circle at 90% 100%, rgba(111,207,255,0.23), transparent 55%)',
        'ember-vignette':
          'radial-gradient(circle at center, transparent 0, rgba(0,0,0,0.8) 70%)'
      },
      fontFamily: {
        title: ['"Cinzel Decorative"', 'serif'],
        body: ['system-ui', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace']
      }
    }
  },
  plugins: [],
};
