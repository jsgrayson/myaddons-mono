# SkillWeaver Minimap Button - Feature Toggles

## Overview
The SkillWeaver minimap button provides quick access to toggle optional features on/off without reloading your UI.

---

## Current Features

### ✅ **Always Active (FREE - Can't Disable)**
These features are always on because they're free or essential:

1. **Healthstones** 💚
   - FREE from Warlocks
   - Auto-use at < 30% health
   - **Why always on:** No cost, no downside

2. **Interrupts** 🛡️
   - Auto-interrupt enemy casts
   - **Why always on:** Essential for all content

3. **Defensives** 🛡️
   - Auto-use based on health thresholds
   - **Why always on:** Prevents deaths

4. **Self-Healing** ❤️
   - Class abilities (Victory Rush, Death Strike, etc.)
   - **Why always on:** Free abilities

5. **Threat Management** ⚠️
   - Feint, Fade, Tricks, Misdirection
   - **Why always on:** Prevents pulling aggro

---

### 🔄 **Toggleable Features (Costs Gold or Situational)**

#### 1. Paid Consumables 💰
**Current Control:** Left-click minimap button  
**Default:** OFF

**Includes:**
- Healing Potions (~500g each)
- Flasks (~2000g, 1hr)
- Food Buffs (~200g, 30min)
- Augment Runes (~1500g, 30min)

**When to Enable:**
- Mythic+ high keys
- Mythic raids
- Rated PvP
- Solo progression content

**When to Disable:**
- Normal/Heroic dungeons
- World quests
- Leveling
- Gold farming

---

### 🚀 **Planned Toggleable Features**

#### 2. Auto-Interrupts 🎯
**Planned Control:** Shift + Left-click  
**Default:** ON

**Why Toggle:**
- Some mechanics require NOT interrupting
- Specific raid strats may need manual control
- Tank interrupts for threat generation

**Use Cases:**
- Disable: Sanguine Depths (specific mechanics)
- Enable: Everything else

---

#### 3. Emergency Ally Healing 🩹
**Planned Control:** Ctrl + Left-click  
**Default:** ON

**Why Toggle:**
- May inflate DPS healing done (pad meters)
- Pure DPS parse mode (no healing)
- Personal preference

**Use Cases:**
- Disable: Parsing for logs
- Enable: Actual prog/survival

---

#### 4. Pet Auto-Management 🐕
**Planned Control:** Alt + Left-click  
**Default:** ON

**Includes:**
- Auto Growl toggle (solo vs group)
- Auto Misdirection (pet vs tank)
- Auto pet summon/attack

**Why Toggle:**
- Manual pet control preferred
- Specific pet positioning needed
- PvP manual control

**Use Cases:**
- Disable: Manual pet control, PvP arenas
- Enable: Everything else

---

#### 5. Utility Mode (All Utilities) 🛠️
**Planned Control:** Shift + Right-click  
**Default:** ON

**Includes:**
- All cleanse/dispel
- All movement abilities
- All group utilities
- Threat management

**Why Toggle:**
- Pure DPS parsing (no utility overhead)
- Skip utility for maximum DPS

**Use Cases:**
- Disable: Parsing sims, testing pure DPS
- Enable: Actual gameplay

---

#### 6. Defensive Mode (Playstyle) 🛡️
**Planned Control:** Ctrl + Right-click  
**Default:** BALANCED

**Modes:**
- **Aggressive:** Lower defensive thresholds (more DPS uptime)
- **Balanced:** Default thresholds
- **Defensive:** Higher defensive thresholds (safer)

**Why Toggle:**
- Adjust for content difficulty
- Personal skill level
- Gear quality

**Use Cases:**
- Aggressive: Overgeared farm content
- Balanced: Normal progression
- Defensive: Under-geared or learning

---

#### 7. Rotation Complexity 🎮
**Planned Control:** Alt + Right-click  
**Default:** ADVANCED

**Modes:**
- **Simple:** Basic rotation (easier, ~90% DPS)
- **Advanced:** Full rotation (harder, 100% DPS)
- **SimC:** Simulation Craft APL (hardest, 100%+ DPS with perfect play)

**Why Toggle:**
- Skill level adjustment
- Learning mode vs. performance mode
- Simplify when tired/distracted

**Use Cases:**
- Simple: Learning spec, casual content
- Advanced: Normal gameplay
- SimC: Parse attempts, high-end content

---

## Minimap Button Controls (Planned)

### Click Combinations
| **Action** | **Feature** | **Default** |
|-----------|-------------|------------|
| Left-Click | Toggle Paid Consumables | OFF |
| Right-Click | Open Settings Panel | - |
| Shift + Left | Toggle Auto-Interrupts | ON |
| Ctrl + Left | Toggle Ally Healing | ON |
| Alt + Left | Toggle Pet Auto-Management | ON |
| Shift + Right | Toggle All Utilities | ON |
| Ctrl + Right | Cycle Defensive Mode | BALANCED |
| Alt + Right | Cycle Rotation Complexity | ADVANCED |

---

## Visual Feedback

### Icon States (Planned)
- **Green Glow:** Consumables ON
- **Red Glow:** Consumables OFF
- **Pulsing:** Feature disabled that's normally on
- **Border Color:** Defensive mode (green = safe, yellow = balanced, red = aggressive)

### Status Display
- Minimap button tooltip shows all toggle states
- Chat feedback when toggling (with sound)
- On-screen notification for important toggles

---

## Slash Commands

### Current
```
/sw consumables    - Toggle paid consumables
/sw minimap        - Hide/show button
/sw help           - Show commands
```

### Planned
```
/sw interrupt      - Toggle auto-interrupts
/sw healing        - Toggle emergency ally healing
/sw pet            - Toggle pet auto-management
/sw utilities      - Toggle all utilities
/sw defensive      - Set defensive mode (aggressive/balanced/defensive)
/sw rotation       - Set rotation complexity (simple/advanced/simc)
/sw status         - Show all current toggle states
```

---

## Why These Features?

### Prioritization Logic

**Always On (No Toggle Needed):**
- FREE features (healthstones, class abilities)
- Core survival (interrupts, defensives)
- Essential mechanics (threat management)

**Toggleable (User Choice):**
- EXPENSIVE features (consumables cost gold)
- SITUATIONAL features (ally healing for parsing)
- PREFERENCE features (rotation complexity)

---

## User Recommendations

### For Most Players
**Keep Default:**
- ✅ Healthstones: ON (always)
- ✅ Interrupts: ON (always)
- ✅ Defensives: ON (always)
- ❌ Paid Consumables: OFF (enable for progression)
- ✅ Ally Healing: ON (helpful)
- ✅ Pet Management: ON (if applicable)

### For Hardcore Players
**Optimize:**
- ✅ Paid Consumables: ON (during prog, OFF during farm)
- ✅ SimC Rotation: ON (maximum DPS)
- 🔶 Defensive Mode: Aggressive (if comfortable)
- ❌ Ally Healing: OFF (pure DPS meters)

### For Casual Players
**Simplify:**
- ❌ Paid Consumables: OFF (save gold)
- ✅ Simple Rotation: ON (easier)
- 🛡️ Defensive Mode: Defensive (safer)
- ✅ All Utilities: ON (helpful)

---

## Future Enhancements

### Planned UI Improvements
1. **Visual Settings Panel**
   - Checkboxes for each toggle
   - Sliders for thresholds
   - Dropdown for modes

2. **Profiles**
   - "Mythic Raid" profile (all ON, aggressive)
   - "Casual" profile (consumables OFF, simple rotation)
   - "Gold Farm" profile (everything OFF except core)

3. **Smart Auto-Toggle**
   - Auto-enable consumables in M+ 15+
   - Auto-disable in normal dungeons
   - Profile per content type

4. **Usage Statistics**
   - Track gold spent on consumables
   - Count interrupts performed
   - Healing done to allies

---

## FAQ

**Q: Why can't I disable healthstones?**  
A: They're FREE from Warlocks! No reason not to use them.

**Q: Will I waste gold if I forget to disable consumables?**  
A: No - they're OFF by default. You must explicitly enable them.

**Q: Can I have different settings per character?**  
A: Currently globalSettings. Per-character planned for future.

**Q: What's the performance impact?**  
A: Minimal. Toggles just change condition checks (microseconds).

**Q: Can I macro the toggles?**  
A: Yes! Use `/sw consumables` etc. in macros.

---

**Summary:** Start with defaults, enable paid consumables only when needed, adjust other toggles based on preference and content difficulty. 🎯
