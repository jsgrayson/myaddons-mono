-- tests/SimContext.lua
local Sim = {}

Sim.now = 0
Sim.spellCD = {}        -- spell -> remaining seconds
Sim.buffs = {}          -- buffName -> true/false
Sim.resources = { runicPower = 0 }

function GetTime() return Sim.now end

function GetSpellCooldown(spell)
  local rem = Sim.spellCD[spell] or 0
  if rem <= 0 then return 0, 0, 1 end
  -- simulate: started (now-rem), duration rem
  return (Sim.now - 0.01), rem + 0.01, 1
end

function GetSpellCharges(spell)
    -- Mock charges: {current, max, start, duration}
    -- Default 1/1
    return 1, 1, 0, 0 
end

function UnitPower(unit, type) 
    return Sim.resources.runicPower or 0 
end

function IsSpellInRange(spell, unit)
    return 1
end

function UnitExists(unit)
    return true
end

function UnitCanAttack(unit)
    return true
end

function UnitIsUnit(u1, u2)
    return u1 == u2
end

function AuraUtil_FindAuraByName(name, unit)
    if Sim.buffs[name] then
        return name, nil, 1, nil, 10, Sim.now + 10, nil, nil, nil, spellID 
    end
    return nil
end

-- Mock global AuraUtil
AuraUtil = {
    FindAuraByName = AuraUtil_FindAuraByName
}

-- Casting/channeling stubs
function UnitCastingInfo(unit) return nil end
function UnitChannelInfo(unit) return nil end

return Sim
