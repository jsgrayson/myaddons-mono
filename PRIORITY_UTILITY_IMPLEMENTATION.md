# Priority-Adjusted Utility Implementation

## Critical Distinctions

### 1. DPS Healing Philosophy
**DPS should NOT be routine healers in groups - healers heal, DPS does damage**

```lua
-- DIRE EMERGENCY ONLY (life-saving, < 15-20% health)
-- Paladin
{ command = "/cast [target=mouseover,help,nodead][help] Lay on Hands", conditions = "in_group and ally_health < 15 and role ~= healer and range <= 40" },
{ command = "/cast [target=player] Word of Glory", conditions = "health < 35 and holy_power >= 3" }, -- Self only, lower threshold

-- Shaman  
{ command = "/cast [target=mouseover,help,nodead][help] Healing Surge", conditions = "in_group and ally_health < 15 and role ~= healer and buff:Maelstrom Weapon >= 10 and range <= 40" },

-- Druid
{ command = "/cast [target=mouseover,help,nodead][help] Swiftmend", conditions = "in_group and ally_health < 15 and role ~= healer and talent(Restoration Affinity) and range <= 40" },

-- Priest (Shadow)
{ command = "/cast [target=mouseover,help,nodead][help] Flash Heal", conditions = "in_group and ally_health < 15 and role ~= healer and range <= 40" },

-- Monk
{ command = "/cast [target=mouseover,help,nodead][help] Vivify", conditions = "in_group and ally_health < 15 and role ~= healer and chi >= 1 and range <= 40" },
```

**Rationale**: Healers should handle routine healing. DPS intervention only when someone is about to die.

---

### 2. Cleanse/Dispel - HIGH PRIORITY

**Movement impairments and dangerous debuffs should be removed immediately**

```lua
-- Self-cleanse (HIGH PRIORITY - before healing)
-- Paladin (Ret/Prot)
{ command = "/cast [target=player] Cleanse", conditions = "debuff_type == poison or debuff_type == disease or movement_impaired" },

-- Shaman
{ command = "/cast [target=player] Cleanse Spirit", conditions = "debuff_type == curse or (debuff_type == poison and talent(Cleanse Spirit))" },

-- Druid
{ command = "/cast [target=player] Remove Corruption", conditions = "debuff_type == curse or debuff_type == poison" },
{ command = "/cast [target=player] Natures Cure", conditions = "debuff_type == magic and talent(Restoration Affinity)" },

-- Monk
{ command = "/cast [target=player] Detox", conditions = "debuff_type == poison or debuff_type == disease" },

-- Mage
{ command = "/cast [target=player] Remove Curse", conditions = "debuff_type == curse" },

-- Priest
{ command = "/cast [target=player] Dispel Magic", conditions = "debuff_type == magic and dispellable" },
{ command = "/cast [target=player] Purify Disease", conditions = "debuff_type == disease" },

-- Movement impairment specific
-- Dwarf Racial
{ command = "/cast Stoneform", conditions = "movement_impaired or debuff_type == bleed or debuff_type == poison" },

-- Escape Artist (Gnome)
{ command = "/cast Escape Artist", conditions = "rooted or snared" },

-- Every Man for Himself (Human)
{ command = "/cast Every Man for Himself", conditions = "stunned or movement_impaired" },

-- Will of the Forsaken (Undead)
{ command = "/cast Will of the Forsaken", conditions = "feared or charmed or slept" },
```

**Ally cleanse (lower priority, not in combat)**
```lua
-- Out of combat cleanse
{ command = "/cast [target=mouseover,help,nodead][help] Cleanse", conditions = "not in_combat and in_group and ally_debuff == poison or ally_debuff == disease" },
```

---

### 3. Divine Shield - Role Aware Logic

**CRITICAL: Divine Shield drops ALL threat - NEVER use while tanking**

```lua
-- Paladin Retribution (DPS) - OK to use
{ command = "/cast [target=player] Divine Shield", conditions = "health < 20 and spec == retribution" },

-- Paladin Protection (Tank) - DO NOT USE
-- Omit entirely from tank rotations, or add explicit check:
{ command = "/cast [target=player] Divine Shield", conditions = "health < 15 and spec ~= protection and not role == tank" },

-- Use Ardent Defender or Guardian of Ancient Kings instead for tanks
{ command = "/cast Ardent Defender", conditions = "health < 30 and spec == protection" },
{ command = "/cast Guardian of Ancient Kings", conditions = "health < 35 and spec == protection and buff:Ardent Defender == 0" },
```

**Similar Aggro-Dropping Abilities:**
```lua
-- Vanish (Rogue) - drops threat
{ command = "/cast Vanish", conditions = "health < 20 and role ~= tank and threat > 100" },

-- Feign Death (Hunter) - drops threat
{ command = "/cast Feign Death", conditions = "threat > 90 and role ~= tank" },

-- Invisibility (Mage) - drops threat
{ command = "/cast Invisibility", conditions = "health < 25 and not in_combat and role ~= tank" },
```

---

### 4. Threat Reduction - HIGH PRIORITY for DPS

**DPS should actively manage threat to avoid pulling from tank**

```lua
-- Rogue: Feint (30% threat reduction, 6s duration)
{ command = "/cast Feint", conditions = "in_group and threat > 80 and in_combat" },

-- Priest: Fade (threat drop + 10% DR)
{ command = "/cast Fade", conditions = "in_group and threat > 85 and in_combat" },

-- Hunter: Misdirection (redirect threat to tank)
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank and threat > 70" },

-- Rogue: Tricks of the Trade (redirect threat to tank)
{ command = "/cast [target=focus] Tricks of the Trade", conditions = "in_group and focus_role == tank and cooldown:Tricks of the Trade == 0" },

-- Warrior: Challenging Shout (taunt - DPS should NOT use)
-- DO NOT INCLUDE in DPS rotations

-- Paladin: Hand of Salvation (threat reduction on ally - old ability, may not exist)
-- Check if exists in current version

-- Threat monitoring
-- Use early (70-80%) to prevent pulling, not reactively at 100%
```

**Proactive Threat Management:**
```lua
-- Open with threat redirect on tank
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank and pull_timer < 1" }, -- Hunter
{ command = "/cast [target=focus] Tricks of the Trade", conditions = "in_group and focus_role == tank and pull_timer < 1" }, -- Rogue

-- Maintain throughout fight
{ command = "/cast Feint", conditions = "in_group and in_combat and cooldown:Feint == 0" }, -- Rogue, use on CD in groups
```

---

## Revised Priority Order

### Priority 1: SURVIVAL (Personal)
1. Cleanse/dispel movement impairments (rooted, snared, dangerous debuffs)
2. Threat reduction (Feint, Fade) - prevent pulling
3. Interrupts (stop casts)
4. Major defensives (Shield Wall, Ice Block, etc.) at < 30% health
5. Self-healing at < 35% health

### Priority 2: GROUP SAFETY (Emergency Only)
6. Ally healing at < 15% health (DIRE EMERGENCY)
7. Battle rez on healer/tank (if dead)
8. Group defensive (Rallying Cry at raid_health < 50%)

### Priority 3: DPS SUPPORT
9. DPS cooldowns (on heroism or cooldown)
10. Racial abilities
11. Resource management

### Priority 4: UTILITY
12. Movement abilities (when out of range or in danger)
13. Pet management (if applicable)
14. Target management

---

## Role-Specific Logic Examples

### DPS Paladin (Retribution)
```lua
-- Cleanse first
{ command = "/cast [target=player] Cleanse", conditions = "debuff_type == poison or debuff_type == disease or movement_impaired" },

-- Ally emergency ONLY
{ command = "/cast [target=mouseover,help,nodead][help] Lay on Hands", conditions = "in_group and ally_health < 15 and range <= 40" },

-- Divine Shield OK (not tanking)
{ command = "/cast [target=player] Divine Shield", conditions = "health < 20" },

-- Self healing
{ command = "/cast [target=player] Word of Glory", conditions = "health < 40 and holy_power >= 3" },

-- Defensives
{ command = "/cast Shield of Vengeance", conditions = "health < 50" },

-- DPS rotation...
```

### Tank Paladin (Protection)
```lua
-- Cleanse
{ command = "/cast [target=player] Cleanse", conditions = "debuff_type == poison or debuff_type == disease" },

-- Tank defensives (NOT Divine Shield)
{ command = "/cast Ardent Defender", conditions = "health < 30 and buff:Guardian of Ancient Kings == 0" },
{ command = "/cast Guardian of Ancient Kings", conditions = "health < 35 and buff:Ardent Defender == 0" },

-- Self healing OK (tanking)
{ command = "/cast [target=player] Word of Glory", conditions = "health < 50 and holy_power >= 3" },

-- Tank rotation...
```

### DPS with Threat Management (Rogue)
```lua
-- Threat redirect (opener)
{ command = "/cast [target=focus] Tricks of the Trade", conditions = "in_group and focus_role == tank and pull_timer < 1" },

-- Cleanse
{ command = "/cast [target=player] Cloak of Shadows", conditions = "debuff_type == magic or dangerous_debuff" },

-- Threat reduction (active)
{ command = "/cast Feint", conditions = "in_group and threat > 75 and in_combat" },

-- Defensives
{ command = "/cast Evasion", conditions = "health < 40" },
{ command = "/cast Cloak of Shadows", conditions = "health < 30 and magic_damage_incoming" },

-- Self healing
{ command = "/cast Crimson Vial", conditions = "health < 35 and energy >= 20" },

-- NEVER heal allies (no healing abilities)

-- DPS rotation...
```

---

## Implementation Checklist

### Phase 1: Essentials (Implement First)
- [x] Interrupts (all classes)
- [ ] Cleanse/dispel (movement impairments, dangerous debuffs)
- [ ] Threat reduction (Feint, Fade, Misdirection, Tricks)
- [ ] Major defensives with role awareness
- [ ] Self-healing at dire thresholds

### Phase 2: Emergency Support
- [ ] Ally healing (< 15% only, life-saving)
- [ ] Divine Shield with role check (no tank usage)
- [ ] Racial abilities (cleanse, DR, CC breaks)

### Phase 3: Advanced
- [ ] Battle rez (combat rez classes)
- [ ] Group buffs (Rallying Cry, Power Infusion)
- [ ] Pet management
- [ ] Movement abilities

---

## Key Takeaways

1. **DPS healing = Emergency only** (< 15% health, life-saving)
2. **Cleanse > Heal** (remove impairments before healing)
3. **Threat management is DPS responsibility** (Feint/Fade proactively)
4. **Divine Shield drops aggro** (DPS/healer only, NEVER tanks)
5. **Role-aware logic** (different behaviors for tank vs DPS specs)
6. **Focus on survival, not being a healer** (DPS job is damage + survival)
