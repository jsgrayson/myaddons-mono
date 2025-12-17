# Comprehensive Utility & Support Implementation Guide

## Overview
Beyond DPS rotation optimization, this guide covers ALL utility, defensive, support, and quality-of-life features that should be included in comprehensive sequences.

---

## 1. Interrupts & Crowd Control

### Interrupts (Priority: HIGH)
**All classes have interrupts - MUST be included**

```lua
-- Universal pattern
{ command = "/cast <Interrupt>", conditions = "should_interrupt and range <= <max_range>" }
```

**By Class:**
- **Warrior**: Pummel (8yd)
- **Paladin**: Rebuke (10yd)
- **Death Knight**: Mind Freeze (15yd)
- **Demon Hunter**: Disrupt (20yd)
- **Rogue**: Kick (8yd)
- **Monk**: Spear Hand Strike (8yd)
- **Druid**: Skull Bash (melee) / Solar Beam (40yd, AoE silence)
- **Shaman**: Wind Shear (30yd)
- **Hunter**: Counter Shot (40yd)
- **Mage**: Counterspell (40yd)
- **Warlock**: Spell Lock (pet, 40yd)
- **Priest**: Silence (30yd, Shadow only)

### Stuns & CC
```lua
-- Short stuns (3-5s)
{ command = "/cast Storm Bolt", conditions = "enemies_nearby >= 2 or priority_target" }, -- Warrior
{ command = "/cast Hammer of Justice", conditions = "enemies_nearby >= 2" }, -- Paladin
{ command = "/cast Asphyxiate", conditions = "enemies_nearby >= 2" }, -- DK
{ command = "/cast Leg Sweep", conditions = "enemies_nearby >= 3 and range <= 8" }, -- Monk

-- Long CC (10s+)
{ command = "/cast Polymorph", conditions = "not in_combat and target_type == humanoid" }, -- Mage
{ command = "/cast Sap", conditions = "not in_combat and stealthed" }, -- Rogue
{ command = "/cast Freezing Trap", conditions = "not in_combat" }, -- Hunter
```

---

## 2. Defensive Cooldowns

### Major Defensives (30-60% DR or Immunity)
```lua
-- Immunities (100% damage prevention)
{ command = "/cast Ice Block", conditions = "health < 25" }, -- Mage
{ command = "/cast Divine Shield", conditions = "health < 20" }, -- Paladin
{ command = "/cast Deterrence", conditions = "health < 30" }, -- Hunter (old)
{ command = "/cast Aspect of the Turtle", conditions = "health < 30" }, -- Hunter

-- Major DR (40-60%)
{ command = "/cast Shield Wall", conditions = "health < 35" }, -- Warrior
{ command = "/cast Icebound Fortitude", conditions = "health < 35" }, -- DK
{ command = "/cast Barkskin", conditions = "health < 40" }, -- Druid
{ command = "/cast Dispersion", conditions = "health < 30" }, -- Priest
{ command = "/cast Astral Shift", conditions = "health < 40" }, -- Shaman
{ command = "/cast Blur", conditions = "health < 45" }, -- DH
{ command = "/cast Evasion", conditions = "health < 40" }, -- Rogue (physical only)
{ command = "/cast Fortifying Brew", conditions = "health < 40" }, -- Monk
```

### Anti-Stacking Logic
```lua
-- Don't stack major defensives
{ command = "/cast Shield Wall", conditions = "health < 35 and buff:Last Stand == 0" },
{ command = "/cast Last Stand", conditions = "health < 30 and buff:Shield Wall == 0" },
```

---

## 3. Dispels & Cleanse

### Magic Dispels
```lua
-- Self dispel
{ command = "/cast [target=player] Dispel Magic", conditions = "debuff_type == magic and dispellable" }, -- Priest
{ command = "/cast [target=player] Cleanse", conditions = "debuff_type == poison or debuff_type == disease" }, -- Paladin
{ command = "/cast [target=player] Cleanse Spirit", conditions = "debuff_type == curse" }, -- Shaman
{ command = "/cast [target=player] Remove Curse", conditions = "debuff_type == curse" }, -- Mage

-- Ally dispel (in groups)
{ command = "/cast [target=mouseover,help,nodead][help] Cleanse", conditions = "in_group and ally_debuff == poison or ally_debuff == disease and range <= 40" },
{ command = "/cast [target=mouseover,help,nodead][help] Purify", conditions = "in_group and ally_debuff == magic and range <= 40" }, -- Priest
```

### Poison/Disease Removal
- **Paladin**: Cleanse (poison, disease)
- **Shaman**: Cleanse Spirit (curse, poison - with talent)
- **Druid**: Remove Corruption (curse, poison)
- **Monk**: Detox (poison, disease)
- **Mage**: Remove Curse

---

## 4. Movement & Mobility

### Charges & Dashes
```lua
-- Gap closers
{ command = "/cast Charge", conditions = "range > 10 and range <= 25" }, -- Warrior
{ command = "/cast Heroic Leap", conditions = "range > 15 or dangerous_ground" }, -- Warrior
{ command = "/cast Wild Charge", conditions = "range > 10" }, -- Druid
{ command = "/cast Roll", conditions = "moving and charges:Roll > 0" }, -- Monk
{ command = "/cast Fel Rush", conditions = "range > 15 or moving" }, -- DH
{ command = "/cast Blink", conditions = "in_combat and dangerous_ground" }, -- Mage
{ command = "/cast Sprint", conditions = "in_combat and moving" }, -- Rogue
{ command = "/cast Disengage", conditions = "range < 10 or dangerous_ground" }, -- Hunter (backward)
```

### Speed Buffs
```lua
{ command = "/cast Divine Steed", conditions = "moving and charges:Divine Steed > 0" }, -- Paladin
{ command = "/cast Pursuit of Justice", conditions = "moving" }, -- Paladin passive
{ command = "/cast Aspect of the Cheetah", conditions = "moving and not in_combat" }, -- Hunter
{ command = "/cast Shadowstep", conditions = "range > 15 and range <= 25" }, -- Rogue
{ command = "/cast Tiger's Lust", conditions = "moving and slowed" }, -- Monk
```

---

## 5. Threat Management

### Threat Reduction
```lua
-- DPS threat drops
{ command = "/cast Feint", conditions = "threat > 80" }, -- Rogue
{ command = "/cast Fade", conditions = "threat > 85" }, -- Priest
{ command = "/cast Invisibility", conditions = "threat > 90 and not in_combat" }, -- Mage
```

### Threat Redirect
```lua
-- Help tank
{ command = "/cast [target=focus] Tricks of the Trade", conditions = "in_group and focus_role == tank" }, -- Rogue
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank" }, -- Hunter
```

---

## 6. Group Utility & Buffs

### Raid-Wide Buffs
```lua
-- Cooldown buffs (use on heroism or high damage phases)
{ command = "/cast Rallying Cry", conditions = "in_group and (heroism or raid_health < 60)" }, -- Warrior, 15% max HP
{ command = "/cast [target=focus] Power Infusion", conditions = "in_group and focus_role == dps and heroism" }, -- Priest, 20% haste
{ command = "/cast Blessing of Sacrifice", conditions = "in_group and ally_health < 25 and range <= 40" }, -- Paladin, redirect damage
{ command = "/cast Innervate", conditions = "in_group and ally_mana < 20 and ally_role == healer" }, -- Druid, mana regen
{ command = "/cast [target=focus] Bloodlust", conditions = "in_group and boss_health < 30 or boss_phase == burn" }, -- Shaman/Mage, heroism
```

### Passive Buffs (Pre-combat)
```lua
-- Apply before pull
{ command = "/cast Battle Shout", conditions = "not in_combat and not buff:Battle Shout" }, -- Warrior, 5% AP
{ command = "/cast Arcane Intellect", conditions = "not in_combat and not buff:Arcane Intellect" }, -- Mage, 5% Int
{ command = "/cast Power Word: Fortitude", conditions = "not in_combat and not buff:Power Word: Fortitude" }, -- Priest, 5% Stam
{ command = "/cast Mark of the Wild", conditions = "not in_combat and not buff:Mark of the Wild" }, -- Druid, 3% versatility
```

---

## 7. Battle Resurrection

### Combat Rez Abilities
```lua
-- Save for healers/tanks (priority)
{ command = "/cast [target=mouseover,dead][target=dead] Rebirth", conditions = "in_combat and in_group and ally_dead and (ally_role == healer or ally_role == tank)" }, -- Druid
{ command = "/cast [target=mouseover,dead][target=dead] Raise Ally", conditions = "in_combat and in_group and ally_dead and (ally_role == healer or ally_role == tank)" }, -- Death Knight
{ command = "/cast [target=mouseover,dead][target=dead] Intercession", conditions = "in_combat and in_group and ally_dead and (ally_role == healer or ally_role == tank)" }, -- Paladin

-- Pre-cast Soulstone (Warlock)
{ command = "/cast [target=focus] Soulstone", conditions = "not in_combat and in_group and focus_role == healer" },
```

---

## 8. Consumables

### Potions
```lua
-- DPS potions (pre-pot + combat)
{ command = "/use Elemental Potion of Ultimate Power", conditions = "not in_combat and pull_timer < 3" }, -- Pre-pot
{ command = "/use Elemental Potion of Ultimate Power", conditions = "in_combat and (heroism or boss_health < 30)" }, -- Combat pot

-- Healing potions
{ command = "/use Refreshing Healing Potion", conditions = "health < 35 and cooldown:healing_potion == 0" },

-- Healthstone (Warlock)
{ command = "/use Healthstone", conditions = "health < 30" },
```

### Food Buffs
```lua
-- Out of combat
{ command = "/use Grand Banquet of the Kalu'ak", conditions = "not in_combat and not buff:Well Fed and not moving" },
```

---

## 9. Racial Abilities

### DPS Racials
```lua
-- Offensive (use on cooldown with heroism)
{ command = "/cast Blood Fury", conditions = "heroism or cooldown:main_cooldown == 0" }, -- Orc
{ command = "/cast Berserking", conditions = "heroism or cooldown:main_cooldown == 0" }, -- Troll
{ command = "/cast Fireblood", conditions = "heroism or cooldown:main_cooldown == 0" }, -- Dark Iron Dwarf
{ command = "/cast Ancestral Call", conditions = "heroism or cooldown:main_cooldown == 0" }, -- Mag'har Orc
{ command = "/cast Bag of Tricks", conditions = "cooldown:Bag of Tricks == 0" }, -- Vulpera

-- Utility
{ command = "/cast Arcane Torrent", conditions = "resource < 20 or should_interrupt" }, -- Blood Elf (interrupt + resource)
{ command = "/cast Gift of the Naaru", conditions = "health < 50" }, -- Draenei (heal)
{ command = "/cast Stoneform", conditions = "health < 40 or debuff_type == bleed" }, -- Dwarf (DR + cleanse)
{ command = "/cast Will to Survive", conditions = "cc_duration > 2" }, -- Human (break CC)
{ command = "/cast Escape Artist", conditions = "rooted or snared" }, -- Gnome
{ command = "/cast Bull Rush", conditions = "range > 10" }, -- Tauren (charge)
```

---

## 10. Pet Management

### Hunter Pets
```lua
-- Pet commands
{ command = "/cast Mend Pet", conditions = "pet_health < 60 and pet_exists" },
{ command = "/cast Revive Pet", conditions = "pet_dead and not in_combat" },
{ command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
{ command = "/petfollow", conditions = "pet_exists and not in_combat" },

-- Pet abilities
{ command = "/cast [pet] Growl", conditions = "pet_exists and solo and not pet:buff:Growl" }, -- Tank pet
{ command = "/cast [pet] Primal Rage", conditions = "pet_exists and in_group and not heroism" }, -- Pet lust
```

### Warlock Pets
```lua
-- Pet management
{ command = "/cast Summon Imp", conditions = "not pet_exists and not in_combat" },
{ command = "/cast Health Funnel", conditions = "pet_health < 40 and health > 60" },
{ command = "/cast [pet] Spell Lock", conditions = "should_interrupt" }, -- Pet interrupt

-- Combat pets
{ command = "/cast Summon Doomguard", conditions = "heroism" }, -- Burst pet
```

### Death Knight Pets
```lua
-- Ghoul control
{ command = "/cast Raise Dead", conditions = "not pet_exists" },
{ command = "/cast [pet] Gnaw", conditions = "should_interrupt or stun_needed" },
{ command = "/cast Dark Transformation", conditions = "pet_exists and cooldown:Dark Transformation == 0" },
```

---

## 11. Loss of Control Prevention

### CC Breaks
```lua
-- PvP trinket (universal)
{ command = "/use 13", conditions = "cc_type == stun or cc_type == fear or cc_type == incapacitate and cc_duration > 2" }, -- Trinket slot 1
{ command = "/use 14", conditions = "cc_type == stun or cc_type == fear or cc_type == incapacitate and cc_duration > 2" }, -- Trinket slot 2

-- Class-specific
{ command = "/cast Will of the Forsaken", conditions = "cc_type == fear or cc_type == charm or cc_type == sleep" }, -- Undead racial
{ command = "/cast Every Man for Himself", conditions = "cc_type == stun" }, -- Human racial
{ command = "/cast Icebound Fortitude", conditions = "cc_type == stun" }, -- DK (also breaks stun)
```

---

## 12. Target Management

### Auto-Targeting
```lua
-- Target switching
{ command = "/targetenemy [noexists][dead]", conditions = "not target_exists or target_dead" },
{ command = "/cleartarget [help]", conditions = "target_friendly" },

-- Focus management
{ command = "/focus [target=boss1]", conditions = "not focus_exists and boss_exists" },
{ command = "/clearfocus [target=focus,dead]", conditions = "focus_dead" },

-- Priority targets
{ command = "/target Blood Beast", conditions = "priority_add_exists" }, -- Example
```

### Mouseover Macros
```lua
-- Already covered in healing section, but also for utility
{ command = "/cast [target=mouseover,harm,nodead][] Sap", conditions = "not in_combat" },
{ command = "/cast [target=mouseover,harm,nodead][] Polymorph", conditions = "not in_combat" },
```

---

## 13. Environmental & Situational

### Dangerous Ground Detection
```lua
-- Leave bad stuff
{ command = "/cast Heroic Leap", conditions = "dangerous_ground" },
{ command = "/cast Transcendence: Transfer", conditions = "dangerous_ground and charges > 0" }, -- Monk
{ command = "/cast Fel Rush", conditions = "dangerous_ground" },
```

### Line of Sight
```lua
-- Abilities that require LoS
{ command = "/cast Mind Blast", conditions = "range <= 40 and line_of_sight" },
```

---

## 14. UI & Automation

### Auto-Loot
```lua
-- Auto-loot corpses
{ command = "/loot", conditions = "target_lootable and range <= 5" },
```

### Auto-Accept Quests
```lua
-- Auto quest helper (use with caution)
{ command = "/click GossipTitleButton1", conditions = "gossip_available" },
{ command = "/click QuestFrameAcceptButton", conditions = "quest_available" },
```

---

## 15. PvP-Specific

### Burst Macros
```lua
-- All CDs at once for burst window
{ command = "/cast Avatar", conditions = "pvp_burst_macro" },
{ command = "/cast Recklessness", conditions = "pvp_burst_macro" },
{ command = "/cast Spear of Bastion", conditions = "pvp_burst_macro" },
{ command = "/use 13", conditions = "pvp_burst_macro" }, -- On-use trinket
```

### Target Arena Players
```lua
-- Arena targeting
{ command = "/target arena1", conditions = "in_arena and arena1_role == healer" },
{ command = "/target arena2", conditions = "in_arena and arena2_role == healer" },
```

---

## Implementation Priority

### Phase 1: Essential (MUST HAVE)
1. Interrupts (all classes)
2. Major defensive cooldowns
3. Self-healing
4. Threat management (Feign/Fade if applicable)

### Phase 2: High Value
5. Movement abilities (charges, blinks)
6. Dispels (if available)
7. Racial abilities (DPS racials)
8. Pet management (pet classes)

### Phase 3: Group Content
9. Ally emergency healing
10. Group buffs (Rallying Cry, Power Infusion)
11. Battle rez (combat rez classes)
12. Threat redirect (Tricks, Misdirection)

### Phase 4: Quality of Life
13. CC abilities
14. Consumables (potions, healthstone)
15. Auto-targeting
16. Environmental awareness

---

## Condition Variables Needed

To implement all of this, the engine needs to support:

```lua
-- Health
health, ally_health, raid_health, pet_health

-- Resources
rage, energy, mana, holy_power, chi, combo_points, astral_power, etc.

-- Range
range (target distance)

-- Buffs/Debuffs
buff:<name>, debuff:<name>, debuff_type, cc_type, cc_duration

-- Group
in_group, in_raid, in_party, in_arena
ally_role, focus_role

-- Combat
in_combat, heroism, pull_timer, boss_health, boss_phase

-- Target
target_exists, target_dead, target_attackable, target_lootable
target_type, priority_target, priority_add_exists

-- Pet
pet_exists, pet_dead, pet_health, pet_attacking

-- Environment
dangerous_ground, line_of_sight, moving

-- Threat
threat (percentage to tank)

-- Cooldowns
cooldown:<ability>

-- Misc
should_interrupt, dispellable, stealthed
```

---

This comprehensive guide covers **everything** beyond basic DPS that should be considered for a complete rotation addon.
