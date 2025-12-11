--========================================================--
-- SkillWeaver - Resource Checking & SafeMode (Updated)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local RC = {}
SkillWeaver.Engine.ResourceCheck = RC

local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end

-- WoW API
local UnitPower      = UnitPower
local UnitPowerMax   = UnitPowerMax
local GetRuneCooldown = GetRuneCooldown

------------------------------------------------------------
-- Resource Enum Mapping
-- (Safe across expansions)
------------------------------------------------------------
RC.TYPES = {
    RAGE           = 1,
    FOCUS          = 2,
    ENERGY         = 3,
    COMBO_POINTS   = 4,
    RUNES          = 5,
    RUNIC_POWER    = 6,
    SOUL_SHARDS    = 7,
    ASTRAL_POWER   = 8,
    HOLY_POWER     = 9,
    MAELSTROM      = 11,
    INSANITY       = 13,
    ARCANE_CHARGES = 16,
    ESSENCE        = 19,
}

------------------------------------------------------------
-- SAFEMODE: Minimal Resource Logic
--  - Always returns basic values
--  - No prediction
--  - No sweeping or multi-slot analysis
------------------------------------------------------------

local function SafeGet(resource)
    local r = resource:lower()

    -- Basic safe returns using UnitPower only
    if r == "rage"           then return UnitPower("player", RC.TYPES.RAGE) end
    if r == "focus"          then return UnitPower("player", RC.TYPES.FOCUS) end
    if r == "energy"         then return UnitPower("player", RC.TYPES.ENERGY) end
    if r == "runicpower"     then return UnitPower("player", RC.TYPES.RUNIC_POWER) end
    if r == "mana"           then return UnitPower("player", 0) end
    if r == "holypower"      then return UnitPower("player", RC.TYPES.HOLY_POWER) end
    if r == "insanity"       then return UnitPower("player", RC.TYPES.INSANITY) end
    if r == "maelstrom"      then return UnitPower("player", RC.TYPES.MAELSTROM) end
    if r == "astralpower"    then return UnitPower("player", RC.TYPES.ASTRAL_POWER) end
    if r == "essence"        then return UnitPower("player", RC.TYPES.ESSENCE) end
    if r == "combo" or r == "combo_points" then
        return UnitPower("player", RC.TYPES.COMBO_POINTS)
    end
    if r == "soulshards" then
        return UnitPower("player", RC.TYPES.SOUL_SHARDS)
    end

    -- Unknown resource → return zero to avoid crashes
    return 0
end

------------------------------------------------------------
-- FULL ENGINE: Advanced Resource Logic
------------------------------------------------------------

local function FullGet(resource)
    local r = resource:lower()

    if r == "rage"           then return UnitPower("player", RC.TYPES.RAGE) end
    if r == "focus"          then return UnitPower("player", RC.TYPES.FOCUS) end
    if r == "energy"         then return UnitPower("player", RC.TYPES.ENERGY) end
    if r == "runicpower"     then return UnitPower("player", RC.TYPES.RUNIC_POWER) end
    if r == "mana"           then return UnitPower("player", 0) end
    if r == "holypower"      then return UnitPower("player", RC.TYPES.HOLY_POWER) end
    if r == "chi"            then return UnitPower("player", RC.TYPES.CHI) end
    if r == "insanity"       then return UnitPower("player", RC.TYPES.INSANITY) end
    if r == "maelstrom"      then return UnitPower("player", RC.TYPES.MAELSTROM) end
    if r == "astralpower"    then return UnitPower("player", RC.TYPES.ASTRAL_POWER) end
    if r == "essence"        then return UnitPower("player", RC.TYPES.ESSENCE) end
    if r == "arcanecharges"  then return UnitPower("player", RC.TYPES.ARCANE_CHARGES) end
    if r == "combo" or r == "combo_points" then
        return UnitPower("player", RC.TYPES.COMBO_POINTS)
    end

    if r == "soulshards" then
        return UnitPower("player", RC.TYPES.SOUL_SHARDS)
    end

    return 0
end

------------------------------------------------------------
-- GET RESOURCE PUBLIC WRAPPER
------------------------------------------------------------

function RC:Get(resource)
    if SAFE() then return SafeGet(resource) end
    if RESTRICT() then return SafeGet(resource) end -- fallback
    return FullGet(resource)
end

------------------------------------------------------------
-- Get Max Resource (Safe Mode: Same API, harmless)
------------------------------------------------------------

function RC:GetMax(resource)
    local r = resource:lower()

    if r == "rage"           then return UnitPowerMax("player", RC.TYPES.RAGE) end
    if r == "focus"          then return UnitPowerMax("player", RC.TYPES.FOCUS) end
    if r == "energy"         then return UnitPowerMax("player", RC.TYPES.ENERGY) end
    if r == "runicpower"     then return UnitPowerMax("player", RC.TYPES.RUNIC_POWER) end
    if r == "mana"           then return UnitPowerMax("player", 0) end
    if r == "holypower"      then return UnitPowerMax("player", RC.TYPES.HOLY_POWER) end
    if r == "insanity"       then return UnitPowerMax("player", RC.TYPES.INSANITY) end
    if r == "maelstrom"      then return UnitPowerMax("player", RC.TYPES.MAELSTROM) end
    if r == "astralpower"    then return UnitPowerMax("player", RC.TYPES.ASTRAL_POWER) end
    if r == "essence"        then return UnitPowerMax("player", RC.TYPES.ESSENCE) end
    if r == "combo" or r == "combo_points" then
        return UnitPowerMax("player", RC.TYPES.COMBO_POINTS)
    end
    if r == "soulshards" then
        return UnitPowerMax("player", RC.TYPES.SOUL_SHARDS)
    end

    return 0
end

------------------------------------------------------------
-- Rune Count (SAFE MODE: Return a simplified value)
------------------------------------------------------------

function RC:GetRuneCount()
    if SAFE() or RESTRICT() then
        -- Return conservative default: assume 1 rune available
        return 1
    end

    local ready = 0
    for i = 1, 6 do
        local start, duration = GetRuneCooldown(i)
        if start == 0 then ready = ready + 1 end
    end
    return ready
end

------------------------------------------------------------
-- Prediction Disabled for Midnight
------------------------------------------------------------

function RC:Predict(resource, ms)
    -- Midnight: NEVER allow prediction logic
    if SAFE() or RESTRICT() then
        return RC:Get(resource)
    end

    -- Full Engine (future expansion allowed safely)
    return RC:Get(resource)
end

------------------------------------------------------------
-- Bind into Engine
------------------------------------------------------------

function SkillWeaver.Engine:ResolveResource(term)
    return RC:Get(term)
end

return RC
