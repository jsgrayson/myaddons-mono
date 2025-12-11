# Backup Interrupt Reference

## Classes with Backup Interrupts (Stuns)

### Warrior
- **Primary**: Pummel (8yd, 15s CD)
- **Backup**: Storm Bolt (20yd, 30s CD) - Talent, also stuns
```lua
{ command = "/cast Pummel", conditions = "should_interrupt and range <= 8" },
{ command = "/cast Storm Bolt", conditions = "should_interrupt and cooldown:Pummel > 0 and talent(Storm Bolt) and range <= 20" },
```

### Paladin (Retribution)
- **Primary**: Rebuke (10yd, 15s CD)
- **Backup**: Hammer of Justice (10yd, 60s CD) - Stun, not true interrupt
- **Backup**: Blinding Light (10yd, 90s CD) - Talent, AoE disorient
```lua
{ command = "/cast Rebuke", conditions = "should_interrupt and range <= 10" },
{ command = "/cast Hammer of Justice", conditions = "should_interrupt and cooldown:Rebuke > 0 and range <= 10" },
```

### Monk (Windwalker)
- **Primary**: Spear Hand Strike (8yd, 15s CD)
- **Backup**: Leg Sweep (8yd, 60s CD) - AoE stun
- **Backup**: Paralysis (20yd, 45s CD) - Incapacitate
```lua
{ command = "/cast Spear Hand Strike", conditions = "should_interrupt and range <= 8" },
{ command = "/cast Leg Sweep", conditions = "should_interrupt and cooldown:Spear Hand Strike > 0 and range <= 8" },
```

### Death Knight
- **Primary**: Mind Freeze (15yd, 15s CD)
- **Backup**: Asphyxiate (30yd, 45s CD) - Stun
```lua
{ command = "/cast Mind Freeze", conditions = "should_interrupt and range <= 15" },
{ command = "/cast Asphyxiate", conditions = "should_interrupt and cooldown:Mind Freeze > 0 and range <= 30" },
```

### Druid (Balance/Feral)
- **Primary**: Skull Bash (melee, 15s CD)
- **Backup**: Mighty Bash (8yd, 60s CD) - Talent, stun
- **Backup**: Solar Beam (40yd, 60s CD) - Balance, AoE silence
```lua
{ command = "/cast Skull Bash", conditions = "should_interrupt and range <= 8" },
{ command = "/cast Mighty Bash", conditions = "should_interrupt and cooldown:Skull Bash > 0 and talent(Mighty Bash) and range <= 8" },
{ command = "/cast Solar Beam", conditions = "should_interrupt and cooldown:Skull Bash > 0 and spec == balance and range <= 40" },
```

### Demon Hunter
- **Primary**: Disrupt (20yd, 15s CD)
- **Backup**: Chaos Nova (8yd, 60s CD) - AoE stun
- **Backup**: Fel Eruption (30yd, 30s CD) - Talent, single stun
```lua
{ command = "/cast Disrupt", conditions = "should_interrupt and range <= 20" },
{ command = "/cast Fel Eruption", conditions = "should_interrupt and cooldown:Disrupt > 0 and talent(Fel Eruption) and range <= 30" },
```

---

## Classes WITHOUT Backup Interrupts

### Rogue
- **Primary**: Kick (8yd, 15s CD)
- **NO BACKUP** (Kidney Shot is a stun but NOT an interrupt)
```lua
{ command = "/cast Kick", conditions = "should_interrupt and range <= 8" },
-- Kidney Shot does NOT interrupt, skip
```

### Shaman (Enhancement)
- **Primary**: Wind Shear (30yd, 12s CD)
- **NO BACKUP** (Capacitor Totem is AoE stun but not an interrupt)
```lua
{ command = "/cast Wind Shear", conditions = "should_interrupt and range <= 30" },
```

### Hunter
- **Primary**: Counter Shot (40yd, 24s CD)
- **NO BACKUP** (Intimidation is a stun but NOT an interrupt)
```lua
{ command = "/cast Counter Shot", conditions = "should_interrupt and range <= 40" },
```

### Mage
- **Primary**: Counterspell (40yd, 24s CD)
- **NO BACKUP** (Dragon's Breath/Ring of Frost are CC, not interrupts)
```lua
{ command = "/cast Counterspell", conditions = "should_interrupt and range <= 40" },
```

### Warlock
- **Primary**: Spell Lock (Pet, 40yd, 24s CD)
- **Backup**: Axe Toss (Felguard, 30yd, 30s CD) - Stun interrupt with Felguard
```lua
{ command = "/cast [pet] Spell Lock", conditions = "should_interrupt and range <= 40" },
{ command = "/cast [pet] Axe Toss", conditions = "should_interrupt and cooldown:Spell Lock > 0 and pet_name == Felguard and range <= 30" },
```

### Priest (Shadow)
- **Primary**: Silence (30yd, 45s CD)
- **Backup**: Psychic Horror (30yd, 60s CD) - Talent, stun+disarm
```lua
{ command = "/cast Silence", conditions = "should_interrupt and range <= 30" },
{ command = "/cast Psychic Horror", conditions = "should_interrupt and cooldown:Silence > 0 and talent(Psychic Horror) and range <= 30" },
```

---

## Priority Pattern

```lua
-- Universal backup interrupt pattern
{ command = "/cast <Primary Interrupt>", conditions = "should_interrupt and range <= <range>" },
{ command = "/cast <Backup Stun/Interrupt>", conditions = "should_interrupt and cooldown:<Primary> > 0 and <conditions> and range <= <range>" },
```

### Important Notes:
1. **Backup interrupts should check primary CD** (`cooldown:Primary > 0`)
2. **Backup interrupts may require talents** (`talent(Storm Bolt)`)
3. **Some "stuns" do NOT interrupt** (Kidney Shot, Intimidation)
4. **AoE interrupts have situational use** (Solar Beam, Chaos Nova)
5. **Pet interrupts need pet checks** (`pet_name == Felguard`)

---

## Implementation Status

### ✅ Implemented
- Warrior: Pummel + Storm Bolt

### 🔄 To Implement
- Paladin: Rebuke + Hammer of Justice
- Monk: Spear Hand Strike + Leg Sweep
- Death Knight: Mind Freeze + Asphyxiate
- Druid: Skull Bash + Mighty Bash/Solar Beam
- Demon Hunter: Disrupt + Fel Eruption
- Warlock: Spell Lock + Axe Toss
- Priest: Silence + Psychic Horror
- Rogue: Kick (no backup)
- Shaman: Wind Shear (no backup)
- Hunter: Counter Shot (no backup)
- Mage: Counterspell (no backup)
