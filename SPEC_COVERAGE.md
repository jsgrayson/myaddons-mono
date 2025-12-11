# SkillWeaver
 - Complete DPS Spec Coverage

## Overview
This document provides a comprehensive summary of all 12 DPS specializations implemented in SkillWeaver, including their Hero Talent variants and key rotation priorities.

---

## Implemented Specs Summary

### 1. **Arms Warrior** (`WARRIOR_71`)
**Hero Talents:**
- **Slayer**: Execute-focused burst, mobility
- **Colossus**: Cleave damage, sustained bleeds

**File:** `sequences/Warrior.lua`

---

### 2. **Fury Warrior** (`WARRIOR_72`)
**Hero Talents:**
- **Slayer**: Enrage uptime, Execute windows
- **Mountain Thane**: Thunder Clap, Thunder Blast procs

**File:** `sequences/Warrior.lua`

---

### 3. **Destruction Warlock** (`WARLOCK_267`)
**Hero Talents:**
- **Diabolist**: Overlord summons, burst windows
- **Hellcaller**: Wither DoT, sustained damage

**File:** `sequences/Warlock.lua`

---

### 4. **Shadow Priest** (`PRIEST_258`)
**Hero Talents:**
- **Archon**: Halo synergy, burst damage
- **Voidweaver**: Void Torrent, entropic damage

**File:** `sequences/Priest.lua`

---

### 5. **Retribution Paladin** (`PALADIN_70`)
**Hero Talents:**
- **Templar**: Hammer of Light, big finishers
- **Herald of the Sun**: Dawnlight DoT, solar damage

**File:** `sequences/Paladin.lua`

---

### 6. **Balance Druid** (`DRUID_102`)
**Hero Talents:**
- **Elune's Chosen**: Fury of Elune, lunar/arcane focus
- **Keeper of the Grove**: Treants, sustained damage

**File:** `sequences/Druid.lua`

---

### 7. **Enhancement Shaman** (`SHAMAN_263`)
**Hero Talents:**
- **Stormbringer**: Tempest (Lightning Bolt replacement), nature damage
- **Totemic**: Surging Totem, totem synergy

**File:** `sequences/Shaman.lua`

---

### 8. **Windwalker Monk** (`MONK_269`)
**Hero Talents:**
- **Shado-Pan**: Flurry Strikes, shadow damage
- **Conduit of the Celestials**: Celestial Conduit, buff focus

**File:** `sequences/Monk.lua`

---

### 9. **Unholy Death Knight** (`DEATHKNIGHT_252`)
**Hero Talents:**
- **San'layn**: Vampiric Strike, disease focus
- **Rider of the Apocalypse**: Horsemen summons, mounted combat

**File:** `sequences/deathknight.lua`

---

### 10. **Subtlety Rogue** (`ROGUE_261`)
**Hero Talents:**
- **Trickster**: Unseen Blade, feint focus
- **Deathstalker**: Deathstalker's Mark, finisher burst

**File:** `sequences/Rogue.lua`

---

### 11. **Assassination Rogue** (`ROGUE_259`)
**Hero Talents:**
- **Fatebound**: Execute scaling (<35% HP), Envenom windows
- **Deathstalker**: Indiscriminate Carnage, bleed spreading

**File:** `sequences/Rogue.lua`

---

### 12. **Havoc Demon Hunter** (`DEMONHUNTER_577`)
**Hero Talents:**
- **Aldrachi Reaver**: Reaver's Glaive, Essence Break combos
- **Fel-Scarred**: Metamorphosis burst, Eye Beam synergy

**File:** `sequences/DemonHunter.lua`

---

## Validation Status
✅ All 12 specs cross-referenced with SimulationCraft APLs  
✅ Hero Talent logic documented in `TALENT_LOGIC.md`  
✅ Reference rotations available in `sequences/Reference_SimC.lua`  

## Next Steps
- In-game testing and validation
- Fine-tuning based on real-world performance
- Community feedback integration
