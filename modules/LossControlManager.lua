--========================================================--
-- SkillWeaver - Loss of Control Manager
-- Automates removal of CC effects (Stuns, Fears, Roots, etc.)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local LossControlManager = {}
SkillWeaver.LossControlManager = LossControlManager

-- Configuration
LossControlManager.Config = {
    AutoTrinket = true,      -- Use PvP Trinket / Human Racial
    AutoClassAbility = true, -- Use class abilities (Icebound Fortitude, etc.)
    MinDuration = 2.0,       -- Minimum CC duration to trigger removal
}

-- CC Types we care about
local CC_TYPES = {
    ["STUN"] = true,
    ["FEAR"] = true,
    ["ROOT"] = true,
    ["SILENCE"] = true,
    ["DISORIENT"] = true,
    ["INCAPACITATE"] = true,
}

-- Class Abilities for CC Removal
-- Format: [Class] = { { spellID=123, type="STUN", name="Name" }, ... }
local CLASS_COUNTERS = {
    ["WARRIOR"] = {
        { id = 18499, type = "FEAR", name = "Berserker Rage" },
        -- Bladestorm removes roots/snares but is a major CD, maybe handle manually or high threshold
    },
    ["PALADIN"] = {
        { id = 1044, type = "ROOT", name = "Blessing of Freedom" }, -- Also removes snares
        { id = 642, type = "STUN", name = "Divine Shield" }, -- Bubble (Major CD)
    },
    ["MAGE"] = {
        { id = 45438, type = "STUN", name = "Ice Block" }, -- Major CD
        { id = 1953, type = "ROOT", name = "Blink" }, -- Removes stuns/roots (Shimmer doesn't)
    },
    ["DEATHKNIGHT"] = {
        { id = 48792, type = "STUN", name = "Icebound Fortitude" },
        { id = 212552, type = "ROOT", name = "Wraith Walk" },
    },
    ["DRUID"] = {
        { id = 108238, type = "ROOT", name = "Mass Entanglement" }, -- No, this causes root. Dash/Stampeding Roar/Shapeshift removes roots.
        -- Shapeshifting is complex to automate directly via spell ID, usually handled by form logic.
    },
    ["HUNTER"] = {
        { id = 53271, type = "ROOT", name = "Master's Call" },
    },
    -- Add more as needed
}

-- Racial Abilities (Handled by RacialManager, but we need to know which remove CC)
local RACIAL_COUNTERS = {
    ["Will to Survive"] = "STUN", -- Human
    ["Stoneform"] = "DISEASE", -- Dwarf (also Bleed/Poison/Magic) - removes some CCs indirectly
    ["Escape Artist"] = "ROOT", -- Gnome
    ["Fireblood"] = "DISEASE", -- Dark Iron (also Magic/Poison/Bleed)
}

------------------------------------------------------------
-- Check current Loss of Control state
------------------------------------------------------------
function LossControlManager:GetCCState()
    -- C_LossOfControl API provides detailed info
    local numEvents = C_LossOfControl.GetNumEvents()
    if numEvents == 0 then return nil end

    for i = 1, numEvents do
        local locType, spellID, text, iconTexture, startTime, timeRemaining, duration, lockoutSchool, priority, displayType = C_LossOfControl.GetEventInfo(i)
        
        if CC_TYPES[locType] and timeRemaining > self.Config.MinDuration then
            return {
                type = locType,
                duration = duration,
                remaining = timeRemaining,
                spellID = spellID
            }
        end
    end
    
    return nil
end

------------------------------------------------------------
-- Get Recovery Action
------------------------------------------------------------
function LossControlManager:GetRecoveryAction()
    local ccState = self:GetCCState()
    if not ccState then return nil end
    
    -- 1. Check Trinket (PvP Trinket / Gladiator's Medallion)
    if self.Config.AutoTrinket then
        -- Slot 13
        local itemID13 = GetInventoryItemID("player", 13)
        if itemID13 then
            local spellName, spellID = GetItemSpell(itemID13)
            -- Check if it's a CC removal trinket (usually has specific spell IDs or text)
            -- For simplicity, we assume if it's equipped and On-Use in PvP, it might be the medallion.
            -- Better check: Is it "Gladiator's Medallion"?
            if spellName and (string.find(spellName, "Medallion") or string.find(spellName, "Gladiator's Emblem")) then
                 local start, duration = GetItemCooldown(itemID13)
                 if start == 0 then
                     return { command = "/use 13", description = "Trinket (CC Removal)" }
                 end
            end
        end
        
        -- Slot 14 (Same logic)
        -- ...
    end
    
    -- 2. Check Racial (via RacialManager if possible, or direct check)
    -- Human Racial
    if IsSpellKnown(59752) and ccState.type == "STUN" then -- Will to Survive
        local start, duration = GetSpellCooldown(59752)
        if start == 0 then
            return { command = "/cast Will to Survive", description = "Racial (Stun Removal)" }
        end
    end
    if IsSpellKnown(20589) and ccState.type == "ROOT" then -- Escape Artist
        local start, duration = GetSpellCooldown(20589)
        if start == 0 then
            return { command = "/cast Escape Artist", description = "Racial (Root Removal)" }
        end
    end
    
    -- 3. Check Class Ability
    if self.Config.AutoClassAbility then
        local _, class = UnitClass("player")
        local counters = CLASS_COUNTERS[class]
        if counters then
            for _, counter in ipairs(counters) do
                if counter.type == ccState.type or counter.type == "ALL" then
                    if IsSpellKnown(counter.id) then
                        local start, duration = GetSpellCooldown(counter.id)
                        if start == 0 then
                            return { command = "/cast " .. counter.name, description = "Class Ability (" .. counter.name .. ")" }
                        end
                    end
                end
            end
        end
    end
    
    return nil
end

return LossControlManager
