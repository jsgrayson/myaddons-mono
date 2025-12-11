# SkillWeaver - Advanced WoW Rotation Addon

**One-button gameplay with intelligent priority logic, automatic interrupts, and scraped rotations from Icy Veins.**

## Features

### 🎮 One-Button Gameplay
- **Spam a single button** to execute your entire rotation
- Separate macros for **Single Target** (`SW_ST`) and **AoE** (`SW_AoE`)
- **Controller support** with ConsolePort-friendly targeting

### 🧠 Advanced Logic Engine
- **Boolean conditions**: `AND`, `OR`, `NOT`, parentheses
- **Priority execution**: First valid condition wins (like SimC)
- **Safe Mode failover**: Auto-degrades for Blizzard API restrictions
- **Rich conditionals**: `rage > 40`, `holypower >= 3`, `buff:Name`, `health < 30`, etc.

### 🌐 Web Scraper
- **Auto-import rotations** from Icy Veins
- **Multi-mode support**: Raid, Mythic+, PvP
- **Logic parsing**: Converts guide text like "if Rage > 40" into actual conditions
- **Talent strings**: Auto-extract and apply talent builds

### 🛡️ Interrupt Database
- **Smart interrupts** for 22+ dungeons (M+ Season + Timewalking)
- **Priority system**: Must-kick vs optional spells
- **Auto-scrapes** from dungeon guides
- **Zero-thought kicks**: Just spam your button, addon handles it

### 🎯 Visual Overlay
- **Shows next spell** with icon and cooldown
- **Movable** overlay (`/swoverlay`)
- **Real-time updates** as you spam
- **Movable** overlay (`/swoverlay`)

### 🧠 Smart Content System (New!)
- **Auto-Detects Content**: Raid, Mythic+, Delve, PvP, Open World.
- **Smart Recommendations**: Suggests best Spec, Talents, and Gear for current content.
- **One-Click Apply**: Instantly import talents and equip gear.
- **Advanced Automation**:
  - **Auto-Trinkets**: Uses DPS/Defensive trinkets intelligently.
  - **Auto-Racials**: Syncs racials with cooldowns.
  - **Loss of Control**: Auto-uses trinket/racial to break stuns/fears.
  - **Battle Res**: Smart auto-res for Tank > Healer > DPS.
  - **Stock Manager**: Warns when potions/healthstones are low.
- **See [SMART_CONTENT_SYSTEM.md](SMART_CONTENT_SYSTEM.md) for full guide.**

### 💾 Sample Sequences
- **Priest** (Disc/Holy): Healer with mouseover logic
- **Warrior** (Arms/Fury): DPS with Rage + auto-interrupts
- **Paladin** (Prot/Ret/Holy): Tank/DPS/Healer with defensive checks

## Installation

1. **Clone or download** this repo
2. **Copy** the `skillweaver` folder to `World of Warcraft\_retail_\Interface\AddOns\`
3. **Rename** to `SkillWeaver` (no lowercase 's')
4. **Install Python deps** (for scraper): `pip install -r scraper/requirements.txt`

## Quick Start

### 1. Run the Scrapers (One-Time Setup)
```bash
cd skillweaver
python3 scraper/scraper.py           # Rotations & Talents
python3 scraper/interrupt_scraper.py # Interrupt database
```

### 2. In-Game Setup
```
/reload
/sw
```

### 3. Create Your Macros
1. Select **Mode** (Raid, Mythic+, etc.)
2. Select **Variant** (Balanced, Safe, Scraped)
3. Click **"Load Sequence"**
4. Click **"Create ST Macro"** and **"Create AoE Macro"**
5. **Drag** `SW_ST` and `SW_AoE` to your bars

### 4. Play!
**Spam the macro**. That's it. The addon handles:
- Rotation priority
- Resource checks
- Cooldown management
- Automatic interrupts
- Defensive cooldowns

## Slash Commands

| Command | Description |
|---------|-------------|
| `/sw` | Open main UI |
| `/swtalents` | Open Talent Viewer |
| `/swoverlay` | Toggle rotation overlay |
| `/reload` | Reload addon after scraping |

## Scraper Usage

### Update Rotations
```bash
python3 scraper/scraper.py
```
- Scrapes Icy Veins for current rotation priorities
- Extracts talent import strings
- Generates `sequences/Generated_Scraped.lua`

### Update Interrupts
```bash
python3 scraper/interrupt_scraper.py
```
- Scrapes dungeon/raid guides for interrupt priorities
- Covers M+ Season, Timewalking, Raids
- Generates `db/Interrupts.lua`

### Automation (Optional)
**Weekly updates via cron (Mac/Linux):**
```bash
0 0 * * 0 cd /path/to/skillweaver && python3 scraper/scraper.py
```

**Task Scheduler (Windows):**
- Run `scraper.py` every Sunday at midnight

## Creating Custom Sequences

Edit `sequences/YourClass.lua`:

```lua
SkillWeaver.Sequences["WARRIOR_71"] = {
    ["Raid"] = {
        ["Custom"] = {
            type = "Priority",  -- or "Sequential"
            st = {
                { command = "/cast Pummel", conditions = "should_interrupt" },
                { command = "/cast Execute", conditions = "target:health < 20" },
                { command = "/cast Mortal Strike", conditions = "rage > 30" },
                { command = "/cast Slam", conditions = "true" },
            },
            aoe = {
                { command = "/cast Whirlwind", conditions = "true" },
                { command = "/cast Cleave", conditions = "true" },
            },
            steps = {}
        }
    }
}
```

## Condition Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `rage` | Current Rage | `rage > 40` |
| `energy` | Current Energy | `energy >= 60` |
| `holypower` | Current Holy Power | `holypower >= 3` |
| `combopoints` | Current Combo Points | `combopoints == 5` |
| `health` | Player health % | `health < 30` |
| `target:health` | Target health % | `target:health < 20` |
| `buff:Name` | Has buff | `buff:Bloodlust` |
| `debuff:Name` | Target has debuff | `debuff:Rend` |
| `cooldown:Spell` | Spell CD remaining | `cooldown:Execute == 0` |
| `moving` | Player is moving | `moving == 0` |
| `in_combat` | In combat | `in_combat` |
| `should_interrupt` | Target casting priority spell | `should_interrupt` |

## Logic Operators

- `AND` / `and` / `&&`
- `OR` / `or` / `||`
- `NOT` / `not` / `!`
- Parentheses: `(rage > 40 and buff:Enrage) or health < 30`

## Controller Support

**DPS/Tank:** Sequences use standard targeting
```lua
{ command = "/cast [help][target=player] Flash Heal" }
```

**Healing (Enhanced mode):**
```
# Auto-targets lowest HP ally
/click SkillWeaverButton_ST
```

**Healing (Standard mode):**
- Use ConsolePort's "Target Nearest Friendly Player" (bind to shoulder button)
- OR: D-pad to cycle frames
- Then spam heal button - it uses `[help]` fallback

Perfect for controller play!

## File Structure

```
skillweaver/
├── core/               # Core addon logic
├── engine/             # Condition parser, sequence engine
├── ui/                 # User interface
├── sequences/          # Rotation definitions
├── db/                 # Interrupt database
├── scraper/            # Python scrapers
│   ├── scraper.py              # Rotation scraper
│   ├── interrupt_scraper.py    # Interrupt scraper
│   └── requirements.txt
└── SkillWeaver.toc     # Addon manifest
```

## FAQ

**Q: Do I need to run the scraper every week?**  
A: No, but it's recommended to stay current with meta changes.

**Q: Can I use this for PvP?**  
A: Yes! The scraper includes PvP rotations (when available).

**Q: Does this work with other addons?**  
A: Yes, it's fully compatible with WeakAuras, GSE, etc.

**Q: What if I don't have Python?**  
A: You can use the addon without scrapers. Just use the built-in Priest/Warrior/Paladin sequences.

**Q: Is this against ToS?**  
A: No. It uses Blizzard's SecureActionButton API, just like GSE.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Add your spec's sequence to `sequences/`
4. Submit a PR

## License

MIT License - See LICENSE file

## Credits

- **Inspired by**: GSE (GnomeSequencer Enhanced)
- **Data sources**: Icy Veins, Wowhead
- **Built with**: Lua, Python, BeautifulSoup

---

**Happy spamming!** 🎮