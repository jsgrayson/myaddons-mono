--========================================================--
-- SkillWeaver - Advanced Pet Logic
-- Handles complex pet interactions: Soulstone, Pet Recovery, Support
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local AdvancedPetLogic = {}
SkillWeaver.AdvancedPetLogic = AdvancedPetLogic

-- Configuration
AdvancedPetLogic.Config = {
    AutoSoulstone = true,    -- Warlock: Auto SS Healer > Tank
    AutoPetRecovery = true,  -- Hunter/Warlock: Auto revive/call if pet dies
    SupportMode = true,      -- Use pet utility on party members (e.g. Singe Magic on Healer)
}

------------------------------------------------------------
-- Warlock: Auto Soulstone Logic
------------------------------------------------------------
function AdvancedPetLogic:GetSoulstoneAction()
    local _, class = UnitClass("player")
    if class ~= "WARLOCK" then return nil end
    
    -- Check SS availability
    local ssID = 20707
    if not IsSpellKnown(ssID) then return nil end
    local start, duration = GetSpellCooldown(ssID)
    if start > 0 and duration > 1.5 then return nil end
    
    -- Logic: Maintain SS on Healer (Priority 1) or Tank (Priority 2)
    -- Only cast if target doesn't have it and is alive (Pre-combat / Combat maintenance)
    
    if not IsInGroup() then
        -- Solo: SS self if not active
        if not UnitBuff("player", "Soulstone") then
            return { command = "/cast [@player] Soulstone", description = "Auto Soulstone (Self)" }
        end
        return nil
    end
    
    -- Group Logic
    local target = nil
    local healer = SkillWeaver.HealingHelper:GetHealerUnit() -- Assuming we add this helper or iterate
    local tank = SkillWeaver.HealingHelper:GetTankUnit()
    
    -- Simple iteration if helpers don't exist yet
    if not healer or not tank then
        local prefix = IsInRaid() and "raid" or "party"
        for i = 1, GetNumGroupMembers() do
            local unit = prefix .. i
            if unit == "party0" then unit = "player" end
            local role = UnitGroupRolesAssigned(unit)
            if role == "HEALER" then healer = unit end
            if role == "TANK" then tank = unit end
        end
    end
    
    -- Priority: Healer > Tank
    if healer and UnitExists(healer) and not UnitIsDeadOrGhost(healer) then
        if not UnitBuff(healer, "Soulstone") then
            return { command = "/cast [@" .. healer .. "] Soulstone", description = "Auto Soulstone (Healer)" }
        end
    elseif tank and UnitExists(tank) and not UnitIsDeadOrGhost(tank) then
        if not UnitBuff(tank, "Soulstone") then
            return { command = "/cast [@" .. tank .. "] Soulstone", description = "Auto Soulstone (Tank)" }
        end
    end
    
    return nil
end

------------------------------------------------------------
-- Hunter/Warlock: Pet Recovery
------------------------------------------------------------
function AdvancedPetLogic:GetRecoveryAction()
    if not self.Config.AutoPetRecovery then return nil end
    if UnitIsDeadOrGhost("player") then return nil end -- Can't summon if dead
    
    local _, class = UnitClass("player")
    if class ~= "HUNTER" and class ~= "WARLOCK" then return nil end
    
    -- Check if pet exists and is alive
    if UnitExists("pet") and not UnitIsDead("pet") then return nil end
    
    -- Pet is missing or dead
    if class == "HUNTER" then
        -- 1. Try Revive Pet (if dead body exists)
        -- WoW API `UnitIsDead("pet")` works if the corpse is there. 
        -- If despawned, it returns false/nil for UnitExists.
        -- Revive Pet works for both dead and despawned-dead pets usually.
        
        if not UnitExists("pet") then
            -- Call Pet 1 (Primary)
            -- TODO: Check which slot was last active? Default to 1.
            return { command = "/cast Call Pet 1", description = "Recover Pet (Call)" }
        else
            -- Exists but dead
            return { command = "/cast Revive Pet", description = "Recover Pet (Revive)" }
        end
        
    elseif class == "WARLOCK" then
        -- Fel Domination (Instant summon) check
        local fdID = 333889
        local instant = IsSpellKnown(fdID) and GetSpellCooldown(fdID) == 0
        
        -- Summon Felguard (Demo) or Imp/Felhunter depending on spec
        -- Simplified: Summon last used or default
        local spec = GetSpecialization()
        local summonSpell = "Summon Imp"
        if spec == 2 then summonSpell = "Summon Felguard" end -- Demonology
        
        if instant then
            return { command = "/cast Fel Domination\n/cast " .. summonSpell, description = "Instant Pet Recovery" }
        else
            -- Hard cast (only if safe? Or just recommend it)
            return { command = "/cast " .. summonSpell, description = "Pet Recovery (Hard Cast)" }
        end
    end
    
    return nil
end

return AdvancedPetLogic
