# DPS Self-Healing Reference Guide

## Overview
This document details all self-healing abilities and talents available to DPS specializations for improved survivability.

---

## Warrior (Arms/Fury)

### Baseline Abilities
- **Victory Rush**: Instant heal after killing an enemy (free)
- **Rallying Cry**: 15% max health (raid-wide, 3min CD)
- **Ignore Pain**: Absorb damage (rage cost)

### Talents
- **Impending Victory**: Replaces Victory Rush, 30% health heal on demand (10 rage, 30s CD)
- **Second Wind**: Passive heal when < 35% health
- **Bitter Immunity**: Spell Reflect also heals

### Recommended Logic
```lua
-- Emergency healing
{ command = "/cast Impending Victory", conditions = "health < 50 and talent(Impending Victory)" },
{ command = "/cast Victory Rush", conditions = "health < 60 and buff:Victorious" },
{ command = "/cast Rallying Cry", conditions = "health < 40" },
```

---

## Paladin (Retribution)

### Baseline Abilities
- **Word of Glory**: Consumes 3 Holy Power for instant heal
- **Flash of Light**: Cast-time heal (mana cost)
- **Lay on Hands**: Full health emergency heal (10min CD)

### Talents
- **Selfless Healer**: Flash of Light instant after 3 Judgment casts
- **Divine Steed**: 2 charges mobility (can kite to heal)

### Recommended Logic
```lua
-- Emergency healing (Holy Power based)
{ command = "/cast Lay on Hands", conditions = "health < 20" },
{ command = "/cast Word of Glory", conditions = "health < 50 and holy_power >= 3" },
{ command = "/cast Flash of Light", conditions = "health < 40 and buff:Selfless Healer" },
{ command = "/cast Divine Shield", conditions = "health < 25" }, -- Immunity (can heal during)
```

---

## Demon Hunter (Havoc)

### Baseline Abilities
- **Consume Magic**: Purge/heal combo (10s CD)
- **Soul Cleave**: Heal from Soul Fragments (if talented)

### Talents
- **Soul Rending**: Leech during Metamorphosis
- **Demonic**: Metamorphosis extension (more leech time)

### Passive Healing
- **Soul Fragments**: Automatically consumed for healing
- **Leech**: Many abilities grant leech

### Recommended Logic
```lua
-- Passive healing, mostly automatic
{ command = "/cast Blur", conditions = "health < 50" }, -- DR, not heal
{ command = "/cast Darkness", conditions = "health < 35" }, -- 20% miss chance
{ command = "/cast Netherwalk", conditions = "health < 30" }, -- Immunity
```

---

## Rogue (All Specs)

### Baseline Abilities
- **Crimson Vial**: 25% health instant heal (30s CD, 20 energy)
- **Feint**: Damage reduction, not healing

### Talents
- **Leeching Poison**: Passive healing on poison application
- **Recuperator**: Heal per combo point spent

### Recommended Logic
```lua
-- Self-healing
{ command = "/cast Crimson Vial", conditions = "health < 50 and energy >= 20" },
{ command = "/cast Cloak of Shadows", conditions = "health < 35" }, -- Magic immunity
{ command = "/cast Evasion", conditions = "health < 40" }, -- Physical dodge
```

---

## Hunter (All Specs)

### Baseline Abilities
- **Exhilaration**: 30% health instant heal (2min CD)
- **Mend Pet**: Pet healing only

### Talents
- **Nature's Endurance**: Exhilaration extended duration
- **Born to be Wild**: Reduced Exhilaration CD (1.5min)
- **Survival of the Fittest**: 20% damage reduction (3min CD)

### Recommended Logic
```lua
-- Self-healing
{ command = "/cast Exhilaration", conditions = "health < 40" },
{ command = "/cast Aspect of the Turtle", conditions = "health < 30" }, -- Immunity
{ command = "/cast Survival of the Fittest", conditions = "health < 50 and talent(Survival of the Fittest)" },
```

---

## Warlock (Destruction)

### Baseline Abilities
- **Drain Life**: Channel (instant in some situations)
- **Healthstone**: 25% health instant (1hr CD)

### Talents
- **Mortal Coil**: Fear + heal (45s CD)
- **Dark Pact**: Sacrifice 20% health for absorb shield
- **Demon Skin**: Passive Soul Leech healing
- **Soul Link**: Pet shares damage taken

### Recommended Logic
```lua
-- Self-healing
{ command = "/cast Mortal Coil", conditions = "health < 50 and talent(Mortal Coil)" },
{ command = "/use Healthstone", conditions = "health < 35" },
{ command = "/cast Drain Life", conditions = "health < 60 and moving" },
{ command = "/cast Unending Resolve", conditions = "health < 40" }, -- DR, not heal
```

---

## Mage (All Specs)

### Baseline Abilities
- **Ice Block**: Immunity (heals to full with talents)

### Talents
- **Temporal Shield**: Absorb damage, heal back after
- **Blazing Barrier/Ice Barrier/Prismatic Barrier**: Absorb shields (not healing)

### Recommended Logic
```lua
-- Defensive (limited healing)
{ command = "/cast Ice Block", conditions = "health < 25" },
{ command = "/cast Alter Time", conditions = "health < 30 and talent(Alter Time)" }, -- Save health state
{ command = "/cast Temporal Shield", conditions = "health < 50 and talent(Temporal Shield)" },
```

---

## Shaman (Enhancement)

### Baseline Abilities
- **Healing Surge**: Fast heal (mana cost)
- **Astral Shift**: 40% damage reduction (90s CD)

### Talents
- **Nature's Swiftness**: Instant Healing Surge (1min CD)
- **Healing Stream Totem**: Passive healing over time
- **Earthen Wall Totem**: Absorb shield totem

### Recommended Logic
```lua
-- Self-healing
{ command = "/cast Nature's Swiftness", conditions = "health < 40 and talent(Nature's Swiftness)" },
{ command = "/cast Healing Surge", conditions = "health < 50 and buff:Nature's Swiftness" },
{ command = "/cast Healing Stream Totem", conditions = "health < 70 and talent(Healing Stream Totem)" },
{ command = "/cast Astral Shift", conditions = "health < 45" },
```

---

## Druid (Balance)

### Baseline Abilities
- **Regrowth**: Instant HoT + heal
- **Renewal**: 30% instant heal (90s CD, talent)
- **Barkskin**: 20% DR (1min CD)

### Talents
- **Restoration Affinity**: Access to Rejuvenation, Swiftmend
- **Ysera's Gift**: Passive heal over time

### Recommended Logic
```lua
-- Self-healing
{ command = "/cast Renewal", conditions = "health < 50 and talent(Renewal)" },
{ command = "/cast Regrowth", conditions = "health < 60" },
{ command = "/cast Rejuvenation", conditions = "health < 75 and talent(Restoration Affinity)" },
{ command = "/cast Swiftmend", conditions = "health < 45 and talent(Restoration Affinity)" },
{ command = "/cast Barkskin", conditions = "health < 40" },
```

---

## Monk (Windwalker)

### Baseline Abilities
- **Vivify**: Instant heal (mana/energy cost)
- **Fortifying Brew**: 20% max health + 20% DR (3min CD)

### Talents
- **Healing Elixir**: Passive heal when < 35% health
- **Diffuse Magic**: Magic damage reduction
- **Dampen Harm**: Reduces very large hits

### Recommended Logic
```lua
-- Self-healing
{ command = "/cast Fortifying Brew", conditions = "health < 50" },
{ command = "/cast Vivify", conditions = "health < 60 and chi >= 1" },
{ command = "/cast Touch of Karma", conditions = "health < 70" }, -- Absorb + damage
{ command = "/cast Diffuse Magic", conditions = "health < 40 and talent(Diffuse Magic)" },
```

---

## Priest (Shadow)

### Baseline Abilities
- **Flash Heal**: Fast heal (mana cost)
- **Dispersion**: 60% DR + resource regen (90s CD)
- **Vampiric Embrace**: 50% leech for 15s (2min CD)

### Talents
- **Vampiric Touch**: Passive healing from DoT damage
- **Shadow Word: Death**: Execute heal with talent

### Recommended Logic
```lua
-- Self-healing
{ command = "/cast [target=player] Vampiric Embrace", conditions = "health < 60" },
{ command = "/cast [target=player] Power Word: Shield", conditions = "health < 50" },
{ command = "/cast [target=player] Flash Heal", conditions = "health < 40" },
{ command = "/cast [target=player] Dispersion", conditions = "health < 30" },
```

---

## Death Knight (Unholy)

### Baseline Abilities
- **Death Strike**: Heal based on recent damage taken
- **Icebound Fortitude**: 30% DR (3min CD)
- **Anti-Magic Shell**: Absorb magic damage

### Talents
- **Death Pact**: 50% health instant (120s CD)
- **Rune Tap**: 40% DR for 4s (Blood only)

### Recommended Logic
```lua
-- Self-healing (DPS DK)
{ command = "/cast Death Strike", conditions = "health < 60 and runic_power >= 45" },
{ command = "/cast Death Pact", conditions = "health < 40 and talent(Death Pact)" },
{ command = "/cast Icebound Fortitude", conditions = "health < 35" },
{ command = "/cast Anti-Magic Shell", conditions = "health < 50" }, -- Magic only
```

---

## Implementation Priority

### High Priority (Significant Healing)
1. **Paladin**: Word of Glory (3 HP = 100k+ heal), Lay on Hands
2. **Hunter**: Exhilaration (30% instant)
3. **Warrior**: Impending Victory (30% instant)
4. **Rogue**: Crimson Vial (25% instant)
5. **Death Knight**: Death Strike (scales with damage taken)

### Medium Priority (Situational)
6. **Shaman**: Healing Surge (expensive but strong)
7. **Druid**: Regrowth/Renewal
8. **Monk**: Vivify, Fortifying Brew
9. **Priest**: Flash Heal, Vampiric Embrace

### Low Priority (Minimal/Passive)
10. **Warlock**: Drain Life, Healthstone
11. **Demon Hunter**: Soul Fragments (passive)
12. **Mage**: Ice Block (immunity, not heal)

---

## General Recommendations

1. **Threshold-Based**: Heal at 40-50% health to avoid wasting CDs
2. **Resource-Aware**: Don't starve DPS resources (Holy Power, Rage, Energy)
3. **Anti-Stacking**: Don't use multiple defensive/healing CDs simultaneously
4. **Content-Specific**:
   - **Solo**: Aggressive healing at 60-70% (safer)
   - **Raid**: Conservative healing at 30-40% (healers present)
   - **PvP**: Reactive healing at 50% (burst damage common)

---

## Next Steps

Apply these self-healing patterns to all DPS sequence files with appropriate conditions for:
- Solo play (Delves, questing)
- Raid environments (DPS focus, healer backup)
- PvP situations (aggressive self-sufficiency)
