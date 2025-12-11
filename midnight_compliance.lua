-- Midnight Compliance Module
-- Handles "Secret Values" introduced in Patch 12.0
-- Ensures the addon remains functional without violating API restrictions.

MidnightCompliance = {}

-- Registry of known secret variables/functions
MidnightCompliance.Secrets = {
    ["UnitHealth"] = true,
    ["UnitPower"] = true,
    ["UnitAura"] = true,
    ["GetSpellCooldown"] = true,
    ["IsUsableSpell"] = true
}

-- Check if a variable/function is a known secret source
function MidnightCompliance.IsSecret(name)
    return MidnightCompliance.Secrets[name] or false
end

-- Safely retrieve a value, returning a fallback if restricted
-- @param func: The function to call (e.g., UnitHealth)
-- @param ...: Arguments for the function
-- @return: The result of the function call, or a safe fallback
function MidnightCompliance.SafeGet(func, fallback, ...)
    -- In a real environment, we would check pcall status or restricted flags
    -- For now, we wrap in pcall to catch "Script too complex" or "Forbidden" errors
    
    local status, result = pcall(func, ...)
    
    if status then
        -- If the result is a "Secret" userdata (Patch 12.0 specific), we might need to handle it
        -- For now, assume if pcall succeeds, we got a value
        return result
    else
        -- Log the restriction (optional, avoid spam)
        -- print("MidnightCompliance: Restricted call to " .. tostring(func))
        return fallback
    end
end

-- Register a new secret source
function MidnightCompliance.RegisterSecret(name)
    MidnightCompliance.Secrets[name] = true
end

-- Example wrapper for UnitHealth
function MidnightCompliance.UnitHealth(unit)
    -- Fallback to 100% health if restricted (to keep rotation spinning)
    -- Or 0 if we want to be conservative
    return MidnightCompliance.SafeGet(UnitHealth, 100, unit)
end

-- Example wrapper for UnitPower
function MidnightCompliance.UnitPower(unit, powerType)
    return MidnightCompliance.SafeGet(UnitPower, 0, unit, powerType)
end
