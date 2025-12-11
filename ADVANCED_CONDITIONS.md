# Advanced Condition Tokens Reference

## Phase 1: Talent Detection ✅
```lua
talent(SpellName)        -- Check if regular talent is active
pvptalent(SpellName)     -- Check if PvP talent is active (for PvP sequences)
```

**Example:**
```lua
{command = "/cast Avatar", conditions = "talent(Avatar) and heroism"}
{command = "/cast Gladiator's Medallion", conditions = "pvptalent(Gladiator's Medallion)"}
```

## Phase 2: Advanced Conditions ✅

### Resource Forecasting
Predict future resources to avoid capping:

```lua
rage_in(seconds)         -- Predicted rage in X seconds
energy_in(seconds)       -- Predicted energy in X seconds
rage_deficit             -- How much rage until cap (100 - current)
energy_deficit           -- How much energy until cap
```

**Example:**
```lua
-- Spend rage before capping
{command = "/cast Execute", conditions = "rage >= 40 or rage_in(3) >= 95"}

-- Pool energy for burst
{command = "/cast Eviscerate", conditions = "energy >= 50 or energy_deficit < 20"}
```

### Combat Context
Intelligent decision making based on fight state:

```lua
combat_time              -- Seconds in combat
time_to_die              -- Estimated seconds until target dies (999 if unknown)
ttd                      -- Alias for time_to_die
time_to_execute          -- Estimated seconds until execute range (20%)
```

**Example:**
```lua
-- Hold cooldown if fight is short
{command = "/cast Avatar", conditions = "time_to_die > 30 and heroism"}

-- Use cooldown in execute phase
{command = "/cast Recklessness", conditions = "time_to_execute < 15"}
```

### Burst Window Detection
```lua
heroism                  -- Any lust buff active (Heroism, Bloodlust, Time Warp, etc.)
bloodlust                -- Alias for heroism
```

**Example:**
```lua
-- Stack cooldowns during lust
{command = "/cast Avatar", conditions = "heroism"}
{command = "/cast Warbreaker", conditions = "heroism and buff:Avatar > 0"}
```

## Phase 3: SimC APL (Coming Soon)
- Import SimulationCraft APLs
- Auto-update from theorycrafting
- Complex conditionals

## Full Example: Intelligent Arms Warrior

```lua
st = {
    -- BURST: Auto-detect talent and stack cooldowns
    {command = "/cast Avatar", conditions = "talent(Avatar) and (heroism or target_health < 20)"},
    {command = "/cast Warbreaker", conditions = "talent(Warbreaker) and heroism"},
    
    -- RESOURCE: Prevent rage capping
    {command = "/cast Execute", conditions = "rage >= 40 or rage_in(3) >= 95"},
    {command = "/cast Mortal Strike", conditions = "rage >= 30"},
    
    -- DEFENSIVES: Anti-stacking
    {command = "/cast Die by the Sword", conditions = "health < 30"},
    
    -- INTERRUPTS
    {command = "/cast Pummel", conditions = "should_interrupt"},
},
```

## PvP Sequences

Use `pvptalent()` for PvP-specific abilities:

```lua
["PvP"] = {
    ["Arena"] = {
        type = "Priority",
        st = {
            -- PvP talents
            {command = "/cast Gladiator's Medallion", conditions = "pvptalent(Gladiator's Medallion) and debuff:Stun > 0"},
            {command = "/cast Storm Bolt", conditions = "pvptalent(Storm Bolt)"},
            
            -- Regular rotation
            {command = "/cast Mortal Strike", conditions = "true"},
        }
    }
}
```

## Token Compatibility

All tokens work together:

```lua
-- Complex condition combining multiple systems
{
    command = "/cast Bladestorm",
    conditions = "talent(Bladestorm) and heroism and enemies >= 3 and rage_deficit < 40 and time_to_die > 10"
}
```

**Reads as:** "Use Bladestorm if we have it talented, during Heroism, with 3+ enemies, we won't cap rage, and the fight will last long enough to matter."

## Performance Notes

- Talent detection cached (1 second)
- Combat tracking updates every 0.5 seconds
- Resource forecasting is instant (no API calls)
- All tokens are lightweight for in-combat use
