# Emergency Ally Healing & Range Check Implementation Guide

## Overview
This guide details how to implement emergency ally healing in raid/group situations and proper range validation for all abilities.

---

## Emergency Ally Healing Pattern

### General Pattern
```lua
-- Priority: Life-saving ally heals > Self-heals > DPS
{ command = "/cast [target=mouseover,help,nodead][help] <Heal>", conditions = "in_group and ally_health < <threshold> and <resource_check> and range <= <max_range>" },
{ command = "/cast [target=player] <Heal>", conditions = "health < <threshold> and <resource_check>" },
```

### Targeting Priority
1. **Mouseover** (if friendly, alive, and in range)
2. **Current target** (if friendly)
3. **Self** (fallback)

---

## Classes with Ally Healing

### 1. **Paladin (Retribution)**
**Emergency Heals:**
- Lay on Hands: ally_health < 15% (10min CD)
- Word of Glory: ally_health < 30% (3 Holy Power)
- Flash of Light: ally_health < 25% (with Selfless Healer buff)

**Implementation:**
```lua
{ command = "/cast [target=mouseover,help,nodead][help] Lay on Hands", conditions = "in_group and ally_health < 15 and range <= 40" },
{ command = "/cast [target=mouseover,help,nodead][help] Word of Glory", conditions = "in_group and ally_health < 30 and holy_power >= 3 and range <= 40" },
```

**Range:** 40 yards

---

### 2. **Shaman (Enhancement)**
**Emergency Heals:**
- Healing Surge: ally_health < 20% (10 Maelstrom Weapon stacks preferred)
- Healing Stream Totem: ally_health < 50% (passive AoE heal)
- Chain Heal: ally_health < 30% (in AoE situations)

**Implementation:**
```lua
{ command = "/cast [target=mouseover,help,nodead][help] Healing Surge", conditions = "in_group and ally_health < 20 and buff:Maelstrom Weapon >= 10 and range <= 40" },
{ command = "/cast Healing Stream Totem", conditions = "in_group and ally_health < 50" },
```

**Range:** 40 yards

---

### 3. **Druid (Balance)**
**Emergency Heals:**
- Swiftmend: ally_health < 25% (requires Restoration Affinity)
- Regrowth: ally_health < 35%
- Rejuvenation: ally_health < 50% (if Restoration Affinity)

**Implementation:**
```lua
{ command = "/cast [target=mouseover,help,nodead][help] Swiftmend", conditions = "in_group and ally_health < 25 and talent(Restoration Affinity) and range <= 40" },
{ command = "/cast [target=mouseover,help,nodead][help] Regrowth", conditions = "in_group and ally_health < 35 and range <= 40" },
```

**Range:** 40 yards

---

### 4. **Priest (Shadow)**
**Emergency Heals:**
- Flash Heal: ally_health < 25%
- Power Word: Shield: ally_health < 30%
- Vampiric Embrace: raid-wide when ally_health < 40%

**Implementation:**
```lua
{ command = "/cast [target=mouseover,help,nodead][help] Flash Heal", conditions = "in_group and ally_health < 25 and range <= 40" },
{ command = "/cast [target=mouseover,help,nodead][help] Power Word: Shield", conditions = "in_group and ally_health < 30 and range <= 40" },
{ command = "/cast Vampiric Embrace", conditions = "in_group and ally_health < 40" }, -- Raid-wide
```

**Range:** 40 yards

---

### 5. **Monk (Windwalker)**
**Emergency Heals:**
- Vivify: ally_health < 30% (1 Chi cost)
- Fortifying Brew: self only

**Implementation:**
```lua
{ command = "/cast [target=mouseover,help,nodead][help] Vivify", conditions = "in_group and ally_health < 30 and chi >= 1 and range <= 40" },
```

**Range:** 40 yards

---

### 6. **Warlock (All Specs)**
**Ally Support:**
- Soulstone: Pre-cast on healer/tank (resurrection)
- Healthstone: Distribute before combat

**Implementation:**
```lua
{ command = "/cast [target=mouseover,help,nodead][help] Soulstone", conditions = "not combat and in_group and range <= 100" },
```

**Range:** 100 yards (Soulstone)

---

## Range Validation by Ability Type

### Melee Abilities (8 yards)
```lua
-- Warrior
{ command = "/cast Mortal Strike", conditions = "range <= 8" },
{ command = "/cast Bloodthirst", conditions = "range <= 8" },
{ command = "/cast Execute", conditions = "range <= 8" },

-- Rogue
{ command = "/cast Mutilate", conditions = "range <= 8" },
{ command = "/cast Sinister Strike", conditions = "range <= 8" },
{ command = "/cast Backstab", conditions = "range <= 8" },

-- Demon Hunter
{ command = "/cast Chaos Strike", conditions = "range <= 8" },
{ command = "/cast Blade Dance", conditions = "range <= 8" },

-- Monk
{ command = "/cast Tiger Palm", conditions = "range <= 8" },
{ command = "/cast Blackout Kick", conditions = "range <= 8" },

-- Shaman
{ command = "/cast Stormstrike", conditions = "range <= 8" },
{ command = "/cast Lava Lash", conditions = "range <= 8" },
```

### Short Range Abilities (10-15 yards)
```lua
-- Paladin
{ command = "/cast Final Verdict", conditions = "range <= 10" },
{ command = "/cast Wake of Ashes", conditions = "range <= 12" },

-- Warrior
{ command = "/cast Whirlwind", conditions = "range <= 10" },
{ command = "/cast Cleave", conditions = "range <= 10" },
```

### Medium Range Abilities (30 yards)
```lua
-- Hunter: Most abilities
{ command = "/cast Aimed Shot", conditions = "range <= 40" },

-- Paladin
{ command = "/cast Judgment", conditions = "range <= 30" },
{ command = "/cast Hammer of Wrath", conditions = "range <= 30" },

-- Warlock
{ command = "/cast Chaos Bolt", conditions = "range <= 40" },
```

### Long Range Abilities (40+ yards)
```lua
-- Mage
{ command = "/cast Fireball", conditions = "range <= 40" },
{ command = "/cast Frostbolt", conditions = "range <= 40" },

-- Priest
{ command = "/cast Mind Blast", conditions = "range <= 40" },

-- Druid
{ command = "/cast Wrath", conditions = "range <= 40" },
{ command = "/cast Starfire", conditions = "range <= 40" },

-- Shaman
{ command = "/cast Lightning Bolt", conditions = "range <= 40" },

-- Healing abilities
{ command = "/cast Healing Surge", conditions = "range <= 40" },
{ command = "/cast Flash Heal", conditions = "range <= 40" },
```

---

## Conditional Logic for Groups

### Detection Patterns
```lua
-- In any group (party or raid)
conditions = "in_group and ally_health < 30"

-- Raid only
conditions = "in_raid and ally_health < 25"

-- Party only
conditions = "in_party and ally_health < 30"

-- Not in group (solo)
conditions = "not in_group"
```

### Ally Health Tracking
```lua
-- Lowest ally health
ally_health < 20  -- Critical
ally_health < 30  -- Emergency
ally_health < 50  -- Warning

-- Mouseover targeting
[target=mouseover,help,nodead]  -- Hover to heal
[help]  -- Current target if friendly
[target=player]  -- Self-cast
```

---

## Resource-Aware Healing

### Holy Power (Paladin)
```lua
-- Don't waste Holy Power on small heals
{ command = "/cast Word of Glory", conditions = "ally_health < 30 and holy_power >= 3" }
-- Emergency: use at 1-2 HP if critical
{ command = "/cast Word of Glory", conditions = "ally_health < 15 and holy_power >= 1" }
```

### Maelstrom Weapon (Shaman)
```lua
-- Prefer 10 stacks for instant cast
{ command = "/cast Healing Surge", conditions = "ally_health < 20 and buff:Maelstrom Weapon >= 10" }
-- Emergency: 5+ stacks acceptable
{ command = "/cast Healing Surge", conditions = "ally_health < 15 and buff:Maelstrom Weapon >= 5" }
```

### Chi (Monk)
```lua
-- Reserve 1 Chi for emergency heals
{ command = "/cast Vivify", conditions = "ally_health < 30 and chi >= 1" }
```

### Mana (Casters)
```lua
-- Mana check for healers
{ command = "/cast Flash Heal", conditions = "ally_health < 25 and mana > 20" }
```

---

## Anti-Spam Logic

### Cooldown Awareness
```lua
-- Don't spam heals, check cooldown status
{ command = "/cast Lay on Hands", conditions = "ally_health < 15 and cooldown:Lay on Hands == 0" }

-- Charge system
{ command = "/cast Healing Stream Totem", conditions = "ally_health < 50 and charges:Healing Stream Totem > 0" }
```

### Buff Tracking
```lua
-- Don't overheal with HoTs
{ command = "/cast Rejuvenation", conditions = "ally_health < 50 and not buff:Rejuvenation@ally" }

-- Shield stacking
{ command = "/cast Power Word: Shield", conditions = "ally_health < 30 and not buff:Power Word: Shield@ally" }
```

---

## Implementation Priority

### Phase 1: Life-Savers (< 20% health)
- Paladin: Lay on Hands
- Shaman: Healing Surge (10 stacks)
- Priest: Flash Heal
- Monk: Vivify

### Phase 2: Emergency (20-30% health)
- Paladin: Word of Glory
- Druid: Swiftmend, Regrowth
- Priest: Power Word: Shield

### Phase 3: Preventive (30-50% health)
- Shaman: Healing Stream Totem
- Druid: Rejuvenation
- Priest: Vampiric Embrace (raid-wide)

---

## Testing Recommendations

1. **Solo**: Verify self-healing works without group
2. **Party**: Test mouseover healing on allies
3. **Raid**: Ensure raid-wide heals activate appropriately
4. **Range**: Validate abilities respect distance requirements
5. **Resources**: Confirm healing doesn't starve DPS resources excessively
