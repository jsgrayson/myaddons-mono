# Talent-Aware Sequence Logic

## Overview
Talents can fundamentally change rotations. The scraper attempts to parse talent-specific logic from guides, but manual sequences should also consider talents.

## Examples of Talent-Dependent Logic

### Warrior Arms - Avatar
```lua
-- Only use if talented (check if ability exists)
{ command = "/cast Avatar", conditions = "cooldown:Avatar == 0" }
```

### Warrior Protection - Bolster
```lua
-- Last Stand grants Shield Block charges if Bolster is talented
{ command = "/cast Last Stand", conditions = "health < 30 and buff:Shield Block == 0" }
```

### Paladin Retribution - Crusade vs Divine Storm
```lua
-- Different finishers based on talent choice
{ command = "/cast Crusade", conditions = "holypower >= 3" },  -- If talented
{ command = "/cast Divine Storm", conditions = "holypower >= 3 and enemies >= 2" },  -- Default AoE
{ command = "/cast Templar's Verdict", conditions = "holypower >= 3" },  -- Default ST
```

### Priest Shadow - Void Eruption vs Dark Ascension
```lua
{ command = "/cast Dark Ascension", conditions = "cooldown:Dark Ascension == 0" },  -- If talented
{ command = "/cast Void Eruption", conditions = "true" },  -- Default
```

## Anti-Stacking Defensives

### Problem
Using multiple major defensives simultaneously wastes cooldowns.

### Solution
Check if other defensives are active:

```lua
-- Warrior Protection
{ command = "/cast Last Stand", conditions = "health < 30 and buff:Shield Wall == 0 and cooldown:Shield Wall > 0" },
{ command = "/cast Shield Wall", conditions = "health < 40 and buff:Last Stand == 0 and cooldown:Last Stand > 0" },

-- Paladin Protection  
{ command = "/cast Ardent Defender", conditions = "health < 30 and buff:Guardian of Ancient Kings == 0" },
{ command = "/cast Guardian of Ancient Kings", conditions = "health < 35 and buff:Ardent Defender == 0" },

-- Death Knight Blood
{ command = "/cast Vampiric Blood", conditions = "health < 50 and buff:Icebound Fortitude == 0" },
{ command = "/cast Icebound Fortitude", conditions = "health < 40 and buff:Vampiric Blood == 0" },
```

## DPS Burst Windows (Stack Cooldowns)

### Problem
Unlike tanks, DPS should **stack** offensive cooldowns during burst windows to maximize damage.

### Burst Windows
1. **Heroism/Bloodlust** - 40 second buff, use ALL cooldowns
2. **Execute Range** - Target below 20-35% health
3. **Raid Damage Phases** - Boss specific (requires manual timing)

### Solution
Stack cooldowns during burst windows:

```lua
-- Warrior Arms
{ command = "/cast Avatar", conditions = "(heroism or target_health < 20) and cooldown:Avatar == 0" },
{ command = "/cast Warbreaker", conditions = "(heroism or target_health < 20) and cooldown:Warbreaker == 0" },
{ command = "/cast Bladestorm", conditions = "heroism and cooldown:Bladestorm == 0" },

-- Warrior Fury
{ command = "/cast Recklessness", conditions = "(heroism or target_health < 35) and cooldown:Recklessness == 0" },
{ command = "/cast Odyns Fury", conditions = "heroism and cooldown:Odyns Fury == 0" },

-- Mage Fire
{ command = "/cast Combustion", conditions = "heroism and cooldown:Combustion == 0" },
{ command = "/cast Fire Blast", conditions = "buff:Combustion > 0" },

-- Rogue Assassination
{ command = "/cast Vendetta", conditions = "(heroism or target_health < 35) and cooldown:Vendetta == 0" },
{ command = "/cast Vanish", conditions = "buff:Vendetta > 0 and cooldown:Vanish == 0" },
```

### Execute Range by Class
Different classes have different execute thresholds:

- Warrior: 20% (Execute), 35% (Fury with Sudden Death)
- Hunter: 20% (Kill Shot)
- Mage: 30% (Fire with Searing Touch)
- Rogue: 35% (Assassination with Blindside)

```lua
{ command = "/cast Execute", conditions = "target_health < 20" },
{ command = "/cast Kill Shot", conditions = "target_health < 20" },
```

### Smart Cooldown Usage

**Hold for Heroism (if close):**
```lua
-- Don't use big cooldowns if lust is coming soon
{ command = "/cast Avatar", conditions = "heroism or cooldown:Heroism > 60" }
```

**This requires knowing fight timings - best left to manual play or WeakAuras.**

### Recommendation

For automated sequences:
1. **Always stack during Heroism** - Safe bet
2. **Always use in Execute range** - Good damage
3. **Don't hold too long** - Use cooldowns ~every 2 minutes even without Heroism

## Combining Conditions

Use `and` to combine talent checks, health, and buff checks:

```lua
{
    command = "/cast Bladestorm",
    conditions = "enemies >= 3 and cooldown:Bladestorm == 0 and buff:Die by the Sword == 0"
}
```

## Talent Detection (Advanced)

WoW doesn't have a direct "talent check" condition, but you can:

1. **Cooldown check**: If cooldown exists, talent is active
   ```lua
   cooldown:Avatar == 0  -- Returns nil if not talented, 0+ if talented
   ```

2. **Ability check**: Try to cast and fail silently
   ```lua
   /cast [talent:X/Y] SpellName  -- WoW macro syntax (not ConditionParser)
   ```

3. **Manual configuration**: Create separate sequence variants per talent build
   - "Raid_Avatar" vs "Raid_Thunderous_Roar"
   - User selects based on their talents

## Recommendation for Comprehensive Coverage

Create multiple sequence variants for popular talent combinations:

```lua
SkillWeaver.Sequences["WARRIOR_71"] = {
    ["Raid"] = {
        ["Avatar"] = { ... },      -- Avatar talent build
        ["Bladestorm"] = { ... },  -- Bladestorm talent build
        ["Balanced"] = { ... }     -- Works with both
    }
}
```

Users select which variant matches their talents.

## Warrior Hero Talents (The War Within)

Hero Talents add a new layer of complexity. We can detect them by checking for their signature abilities or passives.

### Arms Warrior
- **Slayer**: Focuses on Execute damage and mobility.
    - *Signature*: `Slayer's Dominance` (Passive) or `Bladestorm` variants.
    - *Logic*: Prioritize `Execute` and `Mortal Strike`.
- **Colossus**: Focuses on size, durability, and Demolish.
    - *Signature*: `Demolish` (Active Ability).
    - *Logic*: Prioritize `Demolish` and `Colossus Smash`.

### Fury Warrior
- **Slayer**: Similar to Arms, focuses on Execute.
    - *Signature*: `Slayer's Dominance`.
    - *Logic*: Prioritize `Execute` (Sudden Death procs) and `Rampage`.
- **Mountain Thane**: Focuses on Thunder Clap and Lightning.
    - *Signature*: `Thunder Blast` (Passive/Proc) or `Lightning Strikes`.
    - *Logic*: Prioritize `Thunder Clap` (which becomes `Thunder Blast`) and `Bloodthirst`.

### Protection Warrior
- **Mountain Thane**: Thunder Clap focus.
- **Colossus**: Demolish focus.

### Destruction Warlock
- **Diabolist**: Focuses on summoning demons and heavy Chaos Bolts.
    - *Signature*: `Diabolic Ritual` (Passive) or `Overlord`.
    - *Logic*: Prioritize `Chaos Bolt` and `Shadowburn` (Execute).
- **Hellcaller**: Focuses on Wither (Immolate upgrade) and instant damage.
    - *Signature*: `Wither` (Replaces Immolate).
    - *Logic*: Prioritize `Cataclysm` and `Channel Demonfire`.

### Shadow Priest
- **Archon**: Focuses on Void Eruption and sustained damage.
    - *Signature*: `Halo` (Archon version) or `Power Surge`.
    - *Logic*: Prioritize `Void Eruption` and `Mind Blast`.
- **Voidweaver**: Focuses on Entropic Rift and Void Torrent.
    - *Signature*: `Entropic Rift` (Passive/Proc).
    - *Logic*: Prioritize `Void Torrent` and `Devouring Plague`.

### Retribution Paladin
- **Templar**: Focuses on Hammer of Light and big finishers.
    - *Signature*: `Hammer of Light` (Replaces Wake of Ashes).
    - *Logic*: Prioritize `Hammer of Light` and `Templar's Verdict`.
- **Herald of the Sun**: Focuses on Dawnlight (DoT) and Solar Beam.
    - *Signature*: `Dawnlight` (Passive).
    - *Logic*: Prioritize `Wake of Ashes` (applies Dawnlight) and `Divine Storm` (spreads it).

### Balance Druid
- **Elune's Chosen**: Focuses on Arcane/Lunar spells and Fury of Elune.
    - *Signature*: `Fury of Elune` (Active) or `New Moon`.
    - *Logic*: Prioritize `Fury of Elune` and `Full Moon`.
- **Keeper of the Grove**: Focuses on Treants and sustained damage.
    - *Signature*: `Force of Nature` (Active).
    - *Logic*: Prioritize `Force of Nature` and `Starfall`.

### Enhancement Shaman
- **Stormbringer**: Focuses on Tempest (Lightning Bolt upgrade) and nature damage.
    - *Signature*: `Tempest` (Replaces Lightning Bolt).
    - *Logic*: Prioritize `Tempest` and `Stormstrike`.
- **Totemic**: Focuses on Surging Totem and totem synergy.
    - *Signature*: `Surging Totem` (Active).
    - *Logic*: Prioritize `Surging Totem` and `Lava Lash`.

### Windwalker Monk
- **Shado-Pan**: Focuses on Flurry Charges and shadow damage.
    - *Signature*: `Flurry Strikes` (Passive).
    - *Logic*: Prioritize `Fists of Fury` and `Rising Sun Kick` to trigger Flurries.
- **Conduit of the Celestials**: Focuses on Celestial Conduit and buffs.
    - *Signature*: `Celestial Conduit` (Active).
    - *Logic*: Prioritize `Celestial Conduit` and `Tiger Palm`.

### Unholy Death Knight
- **San'layn**: Focuses on Vampiric Strike and disease.
    - *Signature*: `Vampiric Strike` (Replaces Scourge Strike/Clawing Shadows).
    - *Logic*: Prioritize `Vampiric Strike` and `Dark Transformation`.
- **Rider of the Apocalypse**: Focuses on mounted combat and Horsemen.
    - *Signature*: `Rider's Champion` (Passive).
    - *Logic*: Prioritize `Apocalypse` (summons Horsemen) and `Death Coil`.

### Subtlety Rogue
- **Trickster**: Focuses on Unseen Blade and feints.
    - *Signature*: `Unseen Blade` (Passive).
    - *Logic*: Prioritize `Shadowstrike` and `Eviscerate`.
- **Deathstalker**: Focuses on Deathstalker's Mark and finishers.
    - *Signature*: `Deathstalker's Mark` (Applied by Shadowstrike).
    - *Logic*: Prioritize `Darkest Night` (finisher buff) and `Eviscerate`.

### Assassination Rogue
- **Fatebound**: Focuses on execute damage and Envenom windows.
    - *Signature*: `Fatebound Coin` (Passive execute scaling).
    - *Logic*: Prioritize `Envenom` and `Kingsbane`, burst during execute phase (<35% HP).
- **Deathstalker**: Focuses on bleed spreading and Indiscriminate Carnage.
    - *Signature*: `Deathstalker's Mark` (Applied by abilities).
    - *Logic*: Prioritize `Indiscriminate Carnage` (AoE bleed spread), maintain `Rupture` and `Garrote`.

### Havoc Demon Hunter
- **Aldrachi Reaver**: Focuses on Glaive combos and Essence Break.
    - *Signature*: `Reaver's Glaive` (Active combo ability).
    - *Logic*: Prioritize `Essence Break` (debuff) after `Eye Beam`, then `Reaver's Glaive`.
- **Fel-Scarred**: Focuses on Metamorphosis burst and Eye Beam.
    - *Signature*: `Demonic` (Passive Meta extension).
    - *Logic*: Prioritize `Metamorphosis` during burst, use `Eye Beam` to trigger Demonic/Fel-Scarred buffs.




