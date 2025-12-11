--========================================================--
-- SkillWeaver - Battle Res Logic
-- Automatically prioritizes battle resurrection targets
-- Priority: Tank > Healer > DPS
--========================================================--

local BattleRes = {}
SkillWeaver.BattleRes = BattleRes

-- Settings
BattleRes.enabled = true -- Default: enabled

-- Battle Res Spell IDs by Class
local BATTLE_RES_SPELLS = {
    ["DEATHKNIGHT"] = 61999, -- Raise Ally
    ["DRUID"] = 20484,       -- Rebirth
    ["PALADIN"] = 391054,    -- Intercession
    -- Warlock Soulstone is pre-cast only, not handled here
}

-- Role Priority (lower = higher priority)
local ROLE_PRIORITY = {
    ["TANK"] = 1,
    ["HEALER"] = 2,
    ["DAMAGER"] = 3,
    ["NONE"] = 4
}

------------------------------------------------------------
-- Check if player has a battle res spell available
------------------------------------------------------------
function BattleRes:HasBattleRes()
    local _, class = UnitClass("player")
    local spellID = BATTLE_RES_SPELLS[class]
    
    if not spellID then
        return false, nil
    end
    
    -- Check if spell is known
    if not IsPlayerSpell(spellID) then
        return false, nil
    end
    
    -- Check cooldown
    local start, duration = GetSpellCooldown(spellID)
    if start > 0 and duration > 1.5 then -- On CD (ignore GCD)
        return false, nil
    end
    
    -- Check if in combat (battle res only works in combat)
    if not UnitAffectingCombat("player") then
        return false, nil
    end
    
    return true, spellID
end

------------------------------------------------------------
-- Get best resurrection target
-- Returns: unitID, role, name
------------------------------------------------------------
function BattleRes:GetBestResTarget()
    -- Check if enabled via Settings
    if not SkillWeaver.Settings or not SkillWeaver.Settings.utilities.autoBattleRes then
        return nil
    end
    
    local available, spellID = self:HasBattleRes()
    if not available then
        return nil
    end
    
    local candidates = {}
    
    -- Scan party/raid members
    local numMembers = IsInRaid() and GetNumGroupMembers() or GetNumSubgroupMembers()
    local prefix = IsInRaid() and "raid" or "party"
    
    for i = 1, numMembers do
        local unit = prefix .. i
        
        -- Check if unit is dead and in range
        if UnitIsDead(unit) and not UnitIsGhost(unit) then
            local role = UnitGroupRolesAssigned(unit)
            local name = UnitName(unit)
            local priority = ROLE_PRIORITY[role] or ROLE_PRIORITY["NONE"]
            
            -- Check range (40 yards for most battle res)
            if IsSpellInRange(GetSpellInfo(spellID), unit) == 1 then
                table.insert(candidates, {
                    unit = unit,
                    role = role,
                    name = name,
                    priority = priority
                })
            end
        end
    end
    
    -- Sort by priority
    table.sort(candidates, function(a, b)
        return a.priority < b.priority
    end)
    
    -- Return best target
    if #candidates > 0 then
        local best = candidates[1]
        return best.unit, best.role, best.name
    end
    
    return nil
end

------------------------------------------------------------
-- Get resolved battle res spell name for casting
------------------------------------------------------------
function BattleRes:GetSpellName()
    local _, class = UnitClass("player")
    local spellID = BATTLE_RES_SPELLS[class]
    
    if spellID then
        return GetSpellInfo(spellID)
    end
    
    return nil
end

return BattleRes
