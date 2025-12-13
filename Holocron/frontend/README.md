# Holocron Command Center - React Frontend

Modern WoW-themed dashboard UI built with React, TypeScript, and Tailwind CSS.

## Features

- **WoW-Inspired Design**: Professional UI with Warcraft aesthetics (gold accents, rarity colors, titan panels)
- **AI Oracle Integration**: Gemini-powered chat assistant with arcane theming
- **Real-time Dashboard**: KPI cards, damage meters, activity logs
- **Responsive Layout**: Character sheet sidebar + main content area
- **Component-Based**: Modular React components for easy maintenance

## Tech Stack

- **React 18** + **TypeScript** for type-safe components
- **Vite** for fast dev server and optimized builds
- **Tailwind CSS** for utility-first styling
- **Gemini API** for AI chat functionality

## Project Structure

```
frontend/
├── index.html              # Main HTML with Tailwind config
├── main.tsx                # React entry point
├── App.tsx                 # Main application shell
├── types.ts                # TypeScript definitions
├── vite.config.ts          # Vite configuration (proxy to Flask)
├── components/
│   ├── Icons.tsx           # SVG icon components
│   ├── DashboardView.tsx   # Main dashboard view
│   └── AiAssistantView.tsx # AI chat interface
└── services/
    └── geminiService.ts    # Gemini API integration
```

## Getting Started

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Gemini API (Optional)

Edit `services/geminiService.ts` and add your Gemini API key:

```typescript
const API_KEY = 'YOUR_GEMINI_API_KEY_HERE';
```

### 3. Start Development Server

```bash
npm run dev
```

Frontend runs on **http://localhost:3000** with API proxy to Flask backend on port 5005.

### 4. Build for Production

```bash
npm run build
```

## Backend Integration

The Vite config proxies `/api/*` requests to the Flask backend (`http://localhost:8003`).

**Example**: `fetch('/api/goblin')` → `http://localhost:8003/api/goblin`

Make sure your Flask server (`server.py`) is running on port 5005 for API calls to work.

## Components

### DashboardView
- **KPI Cards**: Gold reserves, guild roster, raid progress, uptime
- **Damage Meter**: Styled as WoW combat logs
- **Activity Feed**: Recent events in chat log format

### AiAssistantView
- **Gemini Chat**: AI-powered assistant with arcane Oracle theme
- **Real-time Messaging**: Send/receive with loading states
- **Keyboard Support**: Enter to send, auto-scroll

### Icons
15+ custom SVG components: Dashboard, Settings, Sword, Shield, Gem, Sparkles, etc.

## WoW Theme System

### Colors
- **Rarity**: Common (white), Uncommon (green), Rare (blue), Epic (purple), Legendary (orange)
- **Resources**: Health (green), Mana (blue), Rage (red), Energy (yellow)
- **Azeroth**: Gold primary (#ffd100), dark backgrounds

### Typography
- **Cinzel**: Warcraft-style titles
- **Rajdhani**: Display text
- **Inter**: Body text

### Custom Styles
- `.wow-panel`: Glass-morphism titan panels
- `.wow-card`: Item tooltip-style cards
- `.text-shadow`: Dark glow effects
- `.bar-gloss`: Resource bar gradients

## Next Steps

1. **Connect Live Data**: Replace mock data with real API calls
2. **Add More Views**: Combat log, settings panel
3. **Enhance AI**: Add context-aware responses for game data
4. **Optimize**: Code splitting, lazy loading

## Notes

- The frontend is a **complete rewrite** from Jinja2 templates → modern React
- Designed to integrate seamlessly with existing Flask backend
- WoW aesthetic is production-ready with animations and polish
