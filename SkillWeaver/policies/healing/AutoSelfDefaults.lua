-- policies/healing/AutoSelfDefaults.lua
-- Defaults for automatic self-defense triggers.
-- Used if the SpecProfile doesn't have a specific 'auto' block in its SELF table.

local D = {}

-- Generic DPS
D.DPS = {
    enabled = true,
    healthBelow = 35,
}

-- Generic Healer
D.HEALER = {
    enabled = true,
    healthBelow = 45,
}

-- Generic Tank
D.TANK = {
    enabled = true,
    healthBelow = 55,
    incomingDamage = true, -- Placeholder logic
}

-- Helpers to resolve based on spec role
function D:GetDefaultsForSpec(specKey)
    -- Healers
    if specKey == "SHAMAN_264" or specKey == "DRUID_105" or specKey == "PALADIN_65" 
       or specKey == "PRIEST_256" or specKey == "PRIEST_257" or specKey == "MONK_270" or specKey == "EVOKER_1468" then
        return D.HEALER
    end

    -- Tanks
    if specKey == "DEATHKNIGHT_250" or specKey == "DEMONHUNTER_581" or specKey == "DRUID_104"
       or specKey == "MONK_268" or specKey == "PALADIN_66" or specKey == "WARRIOR_73" then
        return D.TANK
    end

    -- Everyone else: DPS
    return D.DPS
end

return D
