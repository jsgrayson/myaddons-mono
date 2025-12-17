# Advanced Logic Optimizations

## Overview
This document details the advanced logic optimizations applied to SkillWeaver DPS rotations beyond the baseline SimC integration.

---

## Fury Warrior Optimizations

### Resource Pooling
**Problem**: Simple rage > threshold conditions don't account for buff windows or execute phases.

**Solution**: Implemented intelligent resource pooling:
```lua
-- Maintain Enrage uptime as top priority
{ command = "/cast Rampage", conditions = "buff:Enrage == 0" }

-- Pool rage during Recklessness for maximum damage
{ command = "/cast Rampage", conditions = "rage >= 115 and talent(Reckless Abandon) and buff:Recklessness" }

-- Dump rage to avoid capping
{ command = "/cast Rampage", conditions = "rage >= 100" }
```

### Execute Window Optimization
**Problem**: Execute/Sudden Death procs not prioritized correctly based on buff expiration.

**Solution**: Added buff-aware Execute priority:
```lua
-- Dump Sudden Death stacks before capping
{ command = "/cast Execute", conditions = "buff:Sudden Death and charges:Sudden Death > 1" }

-- Use expiring Sudden Death buffs
{ command = "/cast Execute", conditions = "buff:Sudden Death and buff:Sudden Death < 2" }

-- Prevent Ashen Juggernaut waste
{ command = "/cast Execute", conditions = "buff:Ashen Juggernaut and buff:Ashen Juggernaut < 2" }
```

### Cooldown Coordination
**Problem**: Major cooldowns used without regard to Enrage uptime (primary damage multiplier).

**Solution**: Synchronized cooldowns with Enrage:
```lua
-- Champions Spear: Wait for Enrage and Bladestorm cooldown
{ command = "/cast Champions Spear", conditions = "buff:Enrage and cooldown:Bladestorm > 2" }

-- Ravager: Only during Enrage
{ command = "/cast Ravager", conditions = "buff:Enrage" }

-- Thunderous Roar: Only during Enrage
{ command = "/cast Thunderous Roar", conditions = "buff:Enrage" }

-- Odyns Fury: During Enrage or with Titanic Rage talent
{ command = "/cast Odyns Fury", conditions = "buff:Enrage or talent(Titanic Rage)" }
```

### Bloodthirst/Bloodcraze Optimization
**Problem**: Bloodthirst used without considering Bloodcraze stacks or execute scenarios.

**Solution**: Prioritize Bloodthirst intelligently:
```lua
-- Prioritize Bloodthirst with Bloodcraze stacks or during execute
{ command = "/cast Bloodthirst", conditions = "buff:Bloodcraze >= 2 or target_health < 35 and talent(Vicious Contempt)" }

-- Charge dump for Raging Blow
{ command = "/cast Raging Blow", conditions = "charges:Raging Blow > 1" }
```

### Mountain Thane Specific
**Problem**: Thunder Blast proc not prioritized, Thunder Clap used randomly.

**Solution**: Added Thunder Blast priority and smart Thunder Clap usage:
```lua
-- Thunder Blast takes priority (replaces Thunder Clap when procced)
{ command = "/cast Thunder Blast", conditions = "buff:Thunder Blast" }

-- Thunder Clap generates stacks
{ command = "/cast Thunder Clap", conditions = "true" }

-- Coordinate with Meat Cleaver in AoE
{ command = "/cast Thunder Clap", conditions = "buff:Whirlwind == 0 or talent(Meat Cleaver)" }
```

---

## Optimization Principles

### 1. **Buff/Debuff Window Awareness**
Rotations now track buff/debuff expiration and prioritize abilities accordingly:
- Execute with expiring Sudden Death (< 2 seconds)
- Bloodthirst with Bloodcraze stacks (>= 2)
- Cooldowns synchronized with primary damage buffs (Enrage, Avatar, etc.)

### 2. **Resource Forecasting**
Intelligent resource management prevents waste:
- Dump charges before capping (Raging Blow, Sudden Death)
- Pool resources during major cooldowns (Rampage during Recklessness)
- Maintain core buffs (Enrage) as absolute priority

### 3. **Cooldown Coordination**
Major cooldowns synchronized for maximum impact:
- All major damage cooldowns during Enrage uptime
- Champions Spear delayed if Bladestorm imminent
- Execute priority during specific buff windows

### 4. **Talent-Specific Logic**
Optimization varies by talent choice:
- **Slayer**: Execute focus, Bladestorm priority
- **Mountain Thane**: Thunder Blast priority, Thunder Clap for stacks
- **Reckless Abandon**: Higher rage pooling threshold (115 vs 100)
- **Vicious Contempt**: Bloodthirst priority during execute

---

## Impact
These optimizations bring SkillWeaver rotations closer to theoretical maximum DPS by:
1. **Reducing resource waste** (capped resources, expired buffs)
2. **Maximizing burst windows** (cooldown synchronization)
3. **Improving ability priority** (buff-aware logic)
4. **Adapting to talent choices** (spec-specific optimizations)

All changes maintain readability while incorporating SimC-level sophistication.
