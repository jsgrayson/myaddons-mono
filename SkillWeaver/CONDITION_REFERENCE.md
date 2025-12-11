# Condition Syntax Quick Reference

## Overview
This document provides a quick reference for the condition syntax used in SkillWeaver rotation sequences.

## Common Condition Patterns

### Resource Checks
```lua
conditions = "rage >= 40"
conditions = "energy > 50"
conditions = "chi >= 3"
conditions = "combo_points >= 5"
conditions = "fury >= 40"
conditions = "runic_power > 70"
```

### Buff Checks
```lua
conditions = "buff:Enrage"  -- Buff active
conditions = "buff:Slice and Dice < 5"  -- Buff expiring soon
conditions = "buff:Maelstrom Weapon >= 10"  -- Stack count
conditions = "buff:Overpower > 0"  -- Buff present
conditions = "buff:Shadow Dance == 0"  -- Buff absent
```

### Debuff Checks
```lua
conditions = "debuff:Colossus Smash"  -- Debuff on target
conditions = "debuff:Virulent Plague"  -- Disease/DoT active
conditions = "not debuff:Virulent Plague"  -- Debuff absent
```

### Target Health
```lua
conditions = "target_health < 20"  -- Execute range
conditions = "target_health < 35"  -- Fatebound execute
conditions = "target_health > 35"  -- Avoid execute range
```

### Cooldown Checks
```lua
conditions = "cooldown:Colossus Smash <= gcd"  -- Nearly ready
conditions = "cooldown:Empower Rune Weapon == 0"  -- Available
```

### Charge/Stack Checks
```lua
conditions = "charges:Shadow Dance > 0"  -- Has charges
conditions = "charges:Elemental Blast > 0"  -- Can cast
conditions = "wounds >= 4"  -- Festering Wounds stacks
conditions = "souls >= 4"  -- Soul Fragment count
```

### Talent/Hero Talent Checks
```lua
conditions = "talent:Juggernaut"  -- Talent selected
conditions = "heroism"  -- Heroism/Bloodlust active
```

### State Checks
```lua
conditions = "stealthed"  -- Stealth active
conditions = "moving"  -- Player moving
conditions = "true"  -- Always cast
```

### Advanced Patterns
```lua
-- Combo conditions
conditions = "buff:Maelstrom Weapon >= 5 and charges:Elemental Blast > 0"

-- Previous GCD (DH specific)
conditions = "prev_gcd:Eye Beam"

-- Complex logic
conditions = "combo_points >= 5 and buff:Rupture < 5"
conditions = "runic_power > 70 or buff:Sudden Doom"
```

## Condition Evaluation
Conditions are evaluated by `SkillWeaver.Engine.ConditionParser.Evaluate()` which parses the string and checks game state in real-time.

## Best Practices
1. **Be Specific**: Use precise thresholds (e.g., `>= 5` vs `> 4`)
2. **Combine Wisely**: Use `and`/`or` for complex conditions
3. **Order Matters**: Higher priority abilities should appear first in rotation
4. **Test In-Game**: Always validate condition logic against actual gameplay

## See Also
- `ADVANCED_CONDITIONS.md` for engine internals
- `TALENT_LOGIC.md` for Hero Talent implementation
- `sequences/Reference_SimC.lua` for SimC-based examples
