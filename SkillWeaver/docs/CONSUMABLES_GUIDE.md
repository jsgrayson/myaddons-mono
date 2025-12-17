# SkillWeaver Consumables System

## Overview
SkillWeaver includes an **optional** consumables system that can be toggled on/off via the minimap button or slash commands. When enabled, the addon will automatically use healing potions, healthstones, flasks, food, and augment runes based on your preferences.

**Default:** Consumables are **OFF** by default to avoid unexpected item usage.

---

## Minimap Button

### Icon Location
Look for the SkillWeaver icon on your minimap (green elemental shields icon).

### Controls
- **Left-Click:** Toggle consumables ON/OFF
- **Right-Click:** Open settings panel (coming soon)
- **Hover:** View current consumables status

### Status Indicator
The tooltip will show:
- Current ON/OFF status (green/red)
- List of active consumable types (if enabled)
- Health thresholds for potions/healthstones

---

## Slash Commands

### Basic Commands
```
/skillweaver consumables    (or /sw cons)   - Toggle consumables ON/OFF
/skillweaver settings       (or /sw config) - Open settings panel
/skillweaver minimap        (or /sw minimap)- Hide/show minimap button
/skillweaver help           (or /sw help)   - Show all commands
```

### Quick Aliases
```
/sw cons      - Toggle consumables
/sw           - Show help
```

---

## Consumable Types

### 1. **Healthstones** ✅
**When Used:** Health drops below 30% (default)  
**Item:** Warlock Healthstone (automatically detects)  
**Priority:** Highest (before healing potions)

**Configuration:**
- Toggle: `useHealthstones` (default: true)
- Threshold: `healthstoneThreshold` (default: 30%)

---

### 2. **Healing Potions** ✅
**When Used:** Health drops below 35% (default)  
**Supported Potions (The War Within):**
- Tempered Potion (primary, ID: 211880)
- Dreamwalker's Healing Potion (DF, ID: 207021)
- Potion of Withering Dreams (DF, ID: 207039)

**Configuration:**
- Toggle: `usePotions` (default: true)
- Threshold: `potionHealthThreshold` (default: 35%)

**Note:** Shares cooldown with combat potions - use wisely!

---

### 3. **Flasks** ✅
**When Used:** Pre-combat only (no flask buff detected)  
**Supported Flasks (The War Within):**
- Flask of Alchemical Chaos (ID: 212283) - Primary DPS
- Flask of Tempered Mastery (ID: 212284)
- Flask of Tempered Versatility (ID: 212285)
- Flask of Tempered Swiftness (ID: 212286)
- Flask of Saving Graces (ID: 212287) - Tank/Healer

**Configuration:**
- Toggle: `useFlasks` (default: true)

**Auto-Application:** Automatically applies before combat if missing

---

### 4. **Food Buffs** ✅
**When Used:** Pre-combat only (no "Well Fed" buff detected)  
**Supported Food (The War Within):**
- Feast of the Divine Day (AGI, ID: 222731)
- Feast of the Midnight Masquerade (INT, ID: 222730)
- Everything Stew (STR, ID: 222729)
- Individual stat foods (Chippy Tea, Marinated Tenderloins, etc.)

**Configuration:**
- Toggle: `useFood` (default: true)

**Auto-Application:** Automatically applies before combat if missing

---

### 5. **Augment Runes** ✅
**When Used:** Pre-combat only (no augment buff detected)  
**Supported Runes (The War Within):**
- Crystallized Augment Rune (ID: 224108) - Premium
- Algari Augment Rune (ID: 224107) - Budget

**Configuration:**
- Toggle: `useAugmentRunes` (default: true)

**Auto-Application:** Automatically applies before combat if missing

---

## How It Works

### Priority System

#### In Combat (Reactive)
1. **Healthstone** (if health < 30%)
2. **Healing Potion** (if health < 35% and healthstone on CD)

#### Pre-Combat (Proactive)
1. **Flask** (if no flask buff)
2. **Food** (if no Well Fed buff)
3. **Augment Rune** (if no augment buff)

### Auto-Detection
- Scans your bags for consumable items
- Checks for active buffs before using
- Prevents duplicate buff application
- Respects in-combat restrictions

### Safety Features
- **Default OFF:** Won't waste consumables unless you enable it
- **Buff Checking:** Won't use if you already have the buff
- **Combat Restrictions:** Flasks/food/runes only used pre-combat
- **Health Thresholds:** Potions/healthstones only when needed

---

## Configuration

### Current Settings (Default)
```lua
consumables = {
    enabled = false,              -- Toggle ON/OFF (default: OFF)
    
    -- Individual toggles
    useHealthstones = true,       -- Use healthstones
    usePotions = true,            -- Use healing potions
    useFlasks = true,             -- Use flasks
    useFood = true,               -- Use food buffs
    useAugmentRunes = true,       -- Use augment runes
    
    -- Thresholds
    potionHealthThreshold = 35,   -- Use healing potion at 35% health
    healthstoneThreshold = 30,    -- Use healthstone at 30% health
}
```

### Customization (Coming Soon)
Future updates will include a settings panel to customize:
- Individual consumable toggles
- Health thresholds for potions/healthstones
- Preferred flask/food/rune selection
- Minimap button position

---

## Integration with Rotations

### Condition Tokens
Rotations can check consumable status using these tokens:

```lua
-- Check if consumables are enabled
consumables_enabled

-- Check if specific consumable should be used
should_use_healthstone    -- Health < 30% and healthstone available
should_use_potion         -- Health < 35% and potion available
should_use_flask          -- No flask buff and out of combat
should_use_food           -- No food buff and out of combat
should_use_augment        -- No augment buff and out of combat
```

### Example Usage in Rotation
```lua
-- Emergency healing with consumables (if enabled)
{ command = "/use Healthstone", conditions = "should_use_healthstone" },
{ command = "/use Tempered Potion", conditions = "should_use_potion" },

-- Pre-combat buffs (if enabled)
{ command = "/use Flask of Alchemical Chaos", conditions = "should_use_flask" },
{ command = "/use Feast of the Divine Day", conditions = "should_use_food" },
{ command = "/use Crystallized Augment Rune", conditions = "should_use_augment" },
```

**Note:** These conditions automatically return `false` if consumables are disabled.

---

## Best Practices

### When to Enable Consumables
✅ **DO Enable:**
- Mythic+ high keys (when you need every edge)
- Mythic raiding progression
- High-stakes PvP (rated arenas, RBGs)
- Solo challenging content (Torghast, Mage Tower)

❌ **DON'T Enable:**
- Normal/Heroic dungeons (waste of gold)
- LFR/Normal raids (overkill)
- World questing (unnecessary)
- Leveling (too expensive)

### Cost Considerations
Consumables are expensive! Estimate per pull/hour:
- **Healing Potions:** ~100-500g each
- **Healthstones:** FREE (from Warlocks)
- **Flasks:** ~1000-3000g each (lasts 1 hour)
- **Food:** ~50-200g each (30min buff)
- **Augment Runes:** ~500-2000g each (30min buff)

**Budget:** Expect ~3000-5000g per hour of play with full consumables.

### Gold-Saving Tips
1. **Disable when not needed** (default behavior)
2. **Ask Warlocks for Healthstones** (free!)
3. **Buy cheaper DF consumables** for casual content
4. **Farm your own materials** if you have professions
5. **Only use augments for progression** (most expensive)

---

## Troubleshooting

### Consumables Not Working
1. **Check if enabled:** Left-click minimap button or `/sw cons`
2. **Check your bags:** Ensure you have the items
3. **Check buffs:** May already be buffed (no duplicate application)
4. **Check combat state:** Flasks/food/runes only work out of combat

### Minimap Button Not Visible
1. Run `/sw minimap` to show it
2. Check if hidden behind other addon icons
3. Drag it to a different position

### Wrong Consumables Being Used
1. **Settings panel coming soon** for individual selection
2. Temporarily: Remove unwanted consumables from bags
3. Disable specific types via code (advanced users)

---

## Technical Details

### Item Detection
- Scans bags (0-4) for specific item IDs
- Uses `C_Container.GetContainerItemID()`
- Automatically uses first match found

### Buff Detection
- Checks player buffs (UnitBuff)
- Compares against known spell IDs
- Generic "Well Fed" detection for food

### Performance
- Minimal CPU usage (only checks when needed)
- No continuous scanning in background
- Efficient bag search algorithm

---

## Future Enhancements

### Planned Features
- [ ] Full settings panel UI
- [ ] Per-character consumable preferences
- [ ] Preferred item selection (which flask, which food, etc.)
- [ ] Low stock warnings ("Flask running out in 5 min!")
- [ ] Usage statistics (gold spent, potions used, etc.)
- [ ] Smart mode (auto-enable in M+/raids, auto-disable elsewhere)
- [ ] Integration with WeakAuras/TellMeWhen

---

## FAQ

**Q: Will this waste my consumables?**  
A: No! It's OFF by default and only uses items when you explicitly enable it.

**Q: Can I choose which consumables to use?**  
A: Currently all are enabled. Settings panel coming soon for granular control.

**Q: Does it work with macros?**  
A: No, consumables are integrated into SkillWeaver rotations directly.

**Q: Can I change health thresholds?**  
A: Currently hardcoded. Settings panel will allow customization.

**Q: What if I run out of an item?**  
A: The addon will skip it and continue rotation normally.

**Q: Will it use cauldrons/feasts?**  
A: It will detect the buffs from cauldrons/feasts and not duplicate.

---

## Support

**Report Issues:**  
- GitHub: [SkillWeaver Issues](#)
- Discord: [SkillWeaver Community](#)

**Suggestions:**  
We're always looking to improve! Submit feature requests via GitHub.

---

**Remember:** Toggle consumables OFF when not needed to save gold! 💰
