--========================================================--
-- SkillWeaver - Advanced Modular Sequence Database Loader
--========================================================--

local ADDON_NAME, SkillWeaver = ...

SkillWeaver.Sequences = SkillWeaver.Sequences or {}

local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end

------------------------------------------------------------
-- Utility: safe include of class files
------------------------------------------------------------
local function Include(path)
    local ok, result = pcall(function() 
        return SkillWeaver.Loader(path)
    end)
    if ok then return result end
    print("|cffFF6666SkillWeaver: Failed loading|r", path)
    return nil
end

------------------------------------------------------------
-- Class map → file names
------------------------------------------------------------
local CLASS_MAP = {
    HUNTER      = "hunter",
    WARRIOR     = "warrior",
    PALADIN     = "paladin",
    DEATHKNIGHT = "deathknight",
    DEMONHUNTER = "demonhunter",
    ROGUE       = "rogue",
    DRUID       = "druid",
    SHAMAN      = "shaman",
    MAGE        = "mage",
    PRIEST      = "priest",
    WARLOCK     = "warlock",
    MONK        = "monk",
    EVOKER      = "evoker",
}

------------------------------------------------------------
-- Main Load Function
------------------------------------------------------------
function SkillWeaver:LoadSequenceDB()
    local _, class = UnitClass("player")
    class = class:upper()

    local filename = CLASS_MAP[class]
    if not filename then
        print("|cffFF6666SkillWeaver: Unknown class. No rotations loaded.|r")
        return
    end

    local fullpath = "skillweaver/sequences/" .. filename

    local data = Include(fullpath)
    if not data then
        print("|cffFF6666SkillWeaver: No data loaded for class|r", class)
        return
    end

    -- Merge into global database
    for specKey, specData in pairs(data) do
        SkillWeaver.Sequences[specKey] = specData
    end

    print("|cff4af2f8SkillWeaver|r: Loaded rotations for |cff66CCFF" .. class .. "|r")
end

------------------------------------------------------------
-- Auto-load on player login
------------------------------------------------------------
hooksecurefunc(SkillWeaver, "OnPlayerLogin", function()
    SkillWeaver:LoadSequenceDB()
end)
