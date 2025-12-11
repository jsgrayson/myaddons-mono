# Pet Management Implementation Guide

## Classes Requiring Pet Management

### Total: 7 Specs (not 3!)
1. **Hunter** - Beast Mastery, Marksmanship, Survival
2. **Warlock** - Destruction, Affliction, Demonology
3. **Death Knight** - Unholy

---

## Hunter Pet Management (3 specs)

### Core Pet Features
```lua
-- Pet summon (out of combat)
{ command = "/cast Call Pet 1", conditions = "not pet_exists and not in_combat" },
{ command = "/cast Revive Pet", conditions = "pet_dead and not in_combat" },

-- Pet health management
{ command = "/cast Mend Pet", conditions = "pet_exists and pet_health < 60" },

-- Pet attack coordination
{ command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
{ command = "/petfollow", conditions = "pet_exists and not in_combat" },
```

### Misdirection Logic (Solo vs Group)
**KEY FEATURE:** Misdirection target changes based on solo/group status

```lua
-- Solo: Misdirect to pet (tank pet)
{ command = "/cast [target=pet] Misdirection", conditions = "not in_group and pet_exists and cooldown:Misdirection == 0" },

-- Group: Misdirect to focus (tank)
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank and cooldown:Misdirection == 0" },

-- Pull opener (group priority)
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank and pull_timer < 1" },
{ command = "/cast [target=pet] Misdirection", conditions = "not in_group and pet_exists and pull_timer < 1" },
```

### Pet Abilities
```lua
-- Primal Rage (pet lust - Ferocity pet)
{ command = "/cast [pet] Primal Rage", conditions = "in_group and pet_specialization == Ferocity and not heroism" },

-- Master's Call (movement freedom)
{ command = "/cast [target=player] Master's Call", conditions = "rooted or snared" },
{ command = "/cast [target=mouseover,help] Master's Call", conditions = "in_group and ally_rooted" },
```

---

## Warlock Pet Management (3 specs)

### Pet Summon & Selection
```lua
-- Default pet summon (Imp for Destruction, varies by spec)
{ command = "/cast Summon Imp", conditions = "not pet_exists and not in_combat" }, -- Destruction
{ command = "/cast Summon Voidwalker", conditions = "not pet_exists and not in_combat and solo" }, -- Tank pet solo
{ command = "/cast Summon Felhunter", conditions = "not pet_exists and not in_combat and in_group" }, -- DPS pet groups
```

### **CRITICAL: Pet Taunt Management**
**Voidwalker Threatening Presence MUST be toggled based on group status**

```lua
-- Enable taunt when solo (tank pet)
{ command = "/cast [pet] Threatening Presence", conditions = "pet_exists and not in_group and not pet:buff:Threatening Presence and pet_name == Voidwalker" },

-- Disable taunt when in group (avoid pulling from tank)
{ command = "/cast [pet] Threatening Presence", conditions = "pet_exists and in_group and pet:buff:Threatening Presence and pet_name == Voidwalker" },
```

**Why This Matters:**
- Solo: Voidwalker should taunt (tank for you)
- Group: Voidwalker taunt pulls aggro from real tank = BAD

### Pet Health Management
```lua
-- Health Funnel (heal pet out of combat)
{ command = "/cast Health Funnel", conditions = "pet_exists and pet_health < 40 and health > 60 and not in_combat" },
```

### Pet Abilities
```lua
-- Pet interrupt (Spell Lock - all pets except Imp/Voidwalker)
{ command = "/cast [pet] Spell Lock", conditions = "should_interrupt and pet_exists" },

-- Felguard stun (Axe Toss)
{ command = "/cast [pet] Axe Toss", conditions = "should_interrupt and cooldown:Spell Lock > 0 and pet_name == Felguard" },

-- Pet attack
{ command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
```

---

## Death Knight Pet Management (Unholy)

### Ghoul Summon
```lua
-- Raise Dead (permanent pet for Unholy)
{ command = "/cast Raise Dead", conditions = "not pet_exists and not in_combat" },

-- Pet attack
{ command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },
```

### Pet Abilities
```lua
-- Gnaw (pet interrupt/stun)
{ command = "/cast [pet] Gnaw", conditions = "should_interrupt and cooldown:Mind Freeze > 0 and pet_exists" },

-- Dark Transformation (ghoul buff)
{ command = "/cast Dark Transformation", conditions = "pet_exists" },
```

---

## Priority Ordering

### Standard Pet Management Priority
```lua
-- 1. Pet Summon (out of combat, not exists)
{ command = "/cast <Summon Pet>", conditions = "not pet_exists and not in_combat" },

-- 2. Pet Taunt Management (Warlock Voidwalker ONLY)
{ command = "/cast [pet] Threatening Presence", conditions = "<taunt toggle logic>" },

-- 3. Pet Attack Coordination
{ command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },

-- 4. Pet Health (out of combat)
{ command = "/cast Mend Pet", conditions = "pet_exists and pet_health < 60" }, -- Hunter
{ command = "/cast Health Funnel", conditions = "pet_exists and pet_health < 40 and not in_combat" }, -- Warlock

-- 5. Pet Abilities (situational)
{ command = "/cast [pet] <Interrupt>", conditions = "should_interrupt" },
```

---

## Implementation Checklist

### Hunter (3 specs) - TO DO
- [ ] Beast Mastery: Misdirection (pet solo, focus group), Mend Pet, pet attack
- [ ] Marksmanship: Similar to BM
- [ ] Survival: Similar to BM

### Warlock (3 specs) - DONE (Destruction)
- [x] Destruction: Taunt toggle, Spell Lock, Health Funnel, pet summon
- [ ] Affliction: Similar to Destruction
- [ ] Demonology: Enhanced pet focus, Demonic Tyrant coordination

### Death Knight (1 spec) - DONE (Unholy)
- [x] Unholy: Raise Dead, Gnaw interrupt, Dark Transformation

---

## Advanced Pet Features

### Hunter-Specific
```lua
-- Pet specialization swap (out of combat)
{ command = "/cast Call Pet 1", conditions = "pet_spec_needed == Ferocity and pet_spec ~= Ferocity" },
{ command = "/cast Call Pet 2", conditions = "pet_spec_needed == Tenacity and pet_spec ~= Tenacity" },
```

### Warlock-Specific
```lua
-- Pre-cast Soulstone on healer
{ command = "/cast [target=focus] Soulstone", conditions = "not in_combat and in_group and focus_role == healer and not buff:Soulstone" },

-- Summon Infernal/Doomguard (temporary pets)
{ command = "/cast Summon Infernal", conditions = "heroism or target_health < 20" },
```

### DK-Specific
```lua
-- Army of the Dead (temporary ghouls)
{ command = "/cast Army of the Dead", conditions = "heroism or pull_timer < 2" },

-- Gargoyle (temporary pet)
{ command = "/cast Summon Gargoyle", conditions = "talent(Summon Gargoyle)" },
```

---

## Condition Variables Needed

```lua
-- Pet existence
pet_exists, pet_dead, pet_health, pet_attacking

-- Pet details
pet_name (Voidwalker, Felguard, Imp, etc.)
pet_specialization (Ferocity, Tenacity, Cunning)

-- Pet buffs
pet:buff:Threatening Presence
pet:buff:Growl (Hunter pet taunt)

-- Group context
in_group, focus_role
solo (not in_group)
```

---

## Common Mistakes to Avoid

1. **Forgetting pet taunt toggle on Warlock** - Voidwalker will pull aggro in groups
2. **Not checking pet_exists before pet commands** - Errors if no pet
3. **Misdirection to pet in groups** - Should go to tank, not pet
4. **Pet heal during combat** - Wastes resources (Mend Pet exception for Hunter)
5. **Not summoning pet before pull** - DPS loss

---

## Next Steps

1. Create Hunter sequence files (BM, MM, Survival)
2. Implement Hunter Misdirection logic (solo vs group)
3. Add pet management to Affliction and Demonology Warlocks
4. Test pet taunt toggle in groups vs solo
5. Verify Gnaw interrupt works correctly for DK
