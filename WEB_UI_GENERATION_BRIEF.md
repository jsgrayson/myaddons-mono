# AI Studio Prompt: MyAddons Web UI Generation

## DIRECT PROMPT (Copy this exactly)

---

**ROLE**: You are an elite UI/UX designer specializing in dark-themed gaming interfaces.

**TASK**: Generate 5 complete web dashboards for a World of Warcraft addon suite. Each must:
1. Use the MIDNIGHT BASE THEME (dark backgrounds, NOT the accent colors as backgrounds)
2. Use accent colors ONLY for highlights, borders, buttons, and glows
3. Generate ALL visual assets using image generation (backgrounds, icons, logos)
4. Create stunning, premium dark-mode interfaces

**CRITICAL**: The PRIMARY color is ALWAYS dark. Accents are used sparingly for emphasis.

---

## MANDATORY STYLESHEET (Apply to ALL projects)

```css
/* ==========================================================================
   MIDNIGHT BASE THEME - ALL APPS SHARE THIS
   ========================================================================== */

:root {
  /* --- PRIMARY COLORS (DARK - Use these for backgrounds) --- */
  --bg-void: #050709;           /* Deepest black - page background */
  --bg-night: #0a0e17;          /* Dark blue-black - main sections */
  --bg-surface: #111827;        /* Elevated cards/panels */
  --bg-elevated: #1e293b;       /* Hover states, active items */
  
  /* --- TEXT COLORS --- */
  --text-primary: #f1f5f9;      /* Main text - almost white */
  --text-secondary: #94a3b8;    /* Muted text - slate gray */
  --text-muted: #64748b;        /* Very muted - timestamps, hints */
  
  /* --- BORDERS & DIVIDERS --- */
  --border-subtle: #1e293b;     /* Subtle borders */
  --border-visible: #334155;    /* Visible borders */
  
  /* --- SHADOWS & GLOWS --- */
  --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
  --shadow-glow: 0 0 30px var(--accent-glow);
  
  /* --- GLASS EFFECT --- */
  --glass-bg: rgba(17, 24, 39, 0.8);
  --glass-blur: blur(12px);
}

/* Base styles */
body {
  background: linear-gradient(135deg, var(--bg-void) 0%, var(--bg-night) 100%);
  color: var(--text-primary);
  font-family: 'Inter', -apple-system, sans-serif;
  min-height: 100vh;
}

/* Glass panels */
.panel {
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
}

/* Accent usage - ONLY for these elements */
.button-primary {
  background: var(--accent-primary);
  color: white;
}
.accent-border {
  border-color: var(--accent-primary);
}
.accent-glow {
  box-shadow: var(--shadow-glow);
}
.accent-text {
  color: var(--accent-primary);
}
```

---

## PROJECT 1: DeepPockets (Arcane Vault)

**Accent Override:**
```css
:root {
  --accent-primary: #8b5cf6;
  --accent-secondary: #a855f7;
  --accent-glow: rgba(139, 92, 246, 0.3);
}
```

**GENERATE THESE ASSETS:**
1. Background: Dark stone vault with glowing purple arcane runes/cracks
2. Logo: Treasure chest with purple magic emanating from it
3. Icons: Magical rune-styled icons for categories (armor, weapons, consumables, gems)
4. Decorations: Floating purple particles, arcane circles

**UI Description:**
- Inventory grid with item cards
- Sidebar with category filters
- Search bar with purple glow focus state
- The background is DARK with purple ACCENTS only

---

## PROJECT 2: PetWeaver (Nature's Grimoire)

**Accent Override:**
```css
:root {
  --accent-primary: #10b981;
  --accent-secondary: #fbbf24;
  --accent-glow: rgba(16, 185, 129, 0.3);
}
```

**GENERATE THESE ASSETS:**
1. Background: Dark enchanted forest at night with green fireflies
2. Logo: Woven nature book/grimoire with emerald vines
3. Icons: Pet family icons (Beast, Magic, Undead, Dragon, etc.)
4. Decorations: Floating leaves, gentle particle effects

**UI Description:**
- Pet collection grid with animated cards
- Codex-style navigation (book pages)
- Rarity indicators with colored borders
- The background is DARK with green/gold ACCENTS only

---

## PROJECT 3: Goblin (Fel-Green Marketpunk)

**Accent Override:**
```css
:root {
  --accent-primary: #22c55e;
  --accent-secondary: #ca8a04;
  --accent-glow: rgba(34, 197, 94, 0.3);
}
```

**GENERATE THESE ASSETS:**
1. Background: Dark goblin workshop with gears, pipes, fel-green glow
2. Logo: Mechanical goblin head with green glowing eyes
3. Icons: Gold coins, market charts, auction hammer
4. Decorations: Steam/smoke effects, rotating gears

**UI Description:**
- Market price ticker
- Profit/loss indicators
- Steampunk-styled data tables
- The background is DARK with green/brass ACCENTS only

---

## PROJECT 4: Holocron (Astral Observatory)

**Accent Override:**
```css
:root {
  --accent-primary: #3b82f6;
  --accent-secondary: #94a3b8;
  --accent-glow: rgba(59, 130, 246, 0.3);
}
```

**GENERATE THESE ASSETS:**
1. Background: Cosmic void with distant stars and nebulae
2. Logo: Floating blue crystal holocron
3. Icons: Constellation-style navigation icons
4. Decorations: Star particles, holographic grids

**UI Description:**
- Large search bar (search-first interface)
- Data preview cards with holographic borders
- Star-field parallax background
- The background is DARK with blue/silver ACCENTS only

---

## PROJECT 5: SkillWeaver (Blood Moon Combat)

**Accent Override:**
```css
:root {
  --accent-primary: #ef4444;
  --accent-secondary: #f97316;
  --accent-glow: rgba(239, 68, 68, 0.3);
}
```

**GENERATE THESE ASSETS:**
1. Background: Dark battlefield under blood-red moon
2. Logo: Crossed swords with crimson glow
3. Icons: Class icons (Warrior, Mage, Rogue, etc.)
4. Decorations: Embers, war-torn aesthetic

**UI Description:**
- Status dashboard with connection indicators
- Spec selector grid
- Priority list editor
- The background is DARK with red/orange ACCENTS only

---

## QUALITY REQUIREMENTS

✅ **DO:**
- Make backgrounds DARK (#0a0e17 base)
- Use accents for highlights, buttons, borders, glows
- Generate unique backgrounds for each project
- Create glassmorphism panels
- Add subtle animations

❌ **DON'T:**
- Use accent colors as background colors
- Leave placeholder images
- Make it look "light mode"
- Use generic Bootstrap/default styling

---

## OUTPUT FORMAT

For each project, generate:
1. `index.html` - Complete page
2. `styles.css` - Full stylesheet with midnight base
3. Generated assets (SVG or describe for image generation)
4. Preview description

START WITH PROJECT 1: DeepPockets
