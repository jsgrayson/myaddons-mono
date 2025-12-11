-- BrannHelper.lua – Brann perk recommendation and auto‑selection

--[[
    This module provides:
    1. A static database of all Brann perks (auto‑generated from Wowhead/community data).
    2. Functions to evaluate the best perk for the current spec/content.
    3. UI helper for the minimap dropdown (one‑click apply / copy ID).
    4. Fallback handling when the API does not expose direct perk selection.
]]

SkillWeaver = SkillWeaver or {}
SkillWeaver.BrannPerks = {
    -- TWW Season 1 Brann Perks (Combat Curios)
    ["Idol of the Earthmother"] = {
        description = "Brann shields you when you take damage.",
        applicableSpecs = {"Protection Warrior", "Protection Paladin", "Guardian Druid", "Blood Death Knight", "Brewmaster Monk", "Vengeance Demon Hunter"},
        content = {"DELVE", "OPEN_WORLD"},
        score = 15.0, -- Top tier for tanks/solo
    },
    ["Amorphous Relic"] = {
        description = "Brann occasionally heals you or buffs your stats.",
        applicableSpecs = {"ALL"},
        content = {"DELVE", "OPEN_WORLD"},
        score = 12.0, -- Solid general choice
    },
    ["Time Lost Relic"] = {
        description = "Brann grants Bloodlust/Heroism effect occasionally.",
        applicableSpecs = {"ALL"},
        content = {"DELVE"},
        score = 18.0, -- Huge for Delves if no Lust class
    },
    ["Unbreakable Iron Idol"] = {
        description = "Brann taunts enemies off you when you fall below 40% HP.",
        applicableSpecs = {"Arms Warrior", "Fury Warrior", "Retribution Paladin", "Havoc Demon Hunter", "Survival Hunter", "Enhancement Shaman", "Windwalker Monk", "Feral Druid", "Unholy Death Knight", "Frost Death Knight", "Assassination Rogue", "Outlaw Rogue", "Subtlety Rogue"},
        content = {"DELVE"},
        score = 14.0, -- Lifesaver for squishy melee
    },
    ["Porcelain Arrowhead Idol"] = {
        description = "Brann's attacks apply a stacking debuff that increases damage taken.",
        applicableSpecs = {"ALL"},
        content = {"DELVE", "RAID"}, -- If Brann is active in Raid? (Usually not, but for completeness)
        score = 16.0, -- Best DPS increase
    },
    ["Streamlined Relic"] = {
        description = "Brann moves faster and loots for you.",
        applicableSpecs = {"ALL"},
        content = {"OPEN_WORLD"},
        score = 10.0, -- QoL
    },
    ["Light-Touched Idol"] = {
        description = "Brann heals you when you drop below 50%.",
        applicableSpecs = {"ALL"},
        content = {"DELVE"},
        score = 13.0, -- Good safety net
    }
}

-- Utility: check if a value exists in a table (array part)
local function tContains(tbl, val)
    for _, v in ipairs(tbl) do
        if v == val then return true end
    end
    return false
end

-- Determine the best perk for the current spec/content
function SkillWeaver.BrannHelper:BestPerkForCurrentSpec()
    local spec = GetSpecializationInfo(GetSpecialization())
    local content = ContentDetector:GetCurrentContent() -- e.g. "MYTHIC_PLUS"
    local bestPerk, bestScore = nil, -math.huge

    for perkName, perk in pairs(SkillWeaver.BrannPerks) do
        local specMatch = tContains(perk.applicableSpecs, "ALL") or tContains(perk.applicableSpecs, spec)
        local contentMatch = tContains(perk.content, content)
        
        if specMatch and contentMatch then
            if perk.score > bestScore then
                bestScore = perk.score
                bestPerk = perkName
            end
        end
    end
    return bestPerk, bestScore
end

-- Apply the best perk (direct API if available, otherwise copy ID)
function SkillWeaver.BrannHelper:ApplyBestPerk()
    local bestPerk = self:BestPerkForCurrentSpec()
    if not bestPerk then
        print("|cffff0000[SkillWeaver] No suitable Brann perk for this spec/content.|r")
        return
    end

    if C_Brann and C_Brann.SelectPerk then
        C_Brann.SelectPerk(bestPerk)
        print("|cff00ff00[SkillWeaver] Applied Brann perk:|r " .. bestPerk)
    else
        -- Fallback: copy perk name to clipboard for manual selection
        C_System.SetClipboard(bestPerk)
        print("|cffffd700[SkillWeaver] Perk ID copied to clipboard. Paste into Brann dialog.|r")
    end
end

-- UI hook for minimap dropdown (called from the main addon UI code)
function SkillWeaver.BrannHelper:PopulateMinimapMenu(menu)
    local bestPerk, _ = self:BestPerkForCurrentSpec()
    if not bestPerk then return end

    local info = UIDropDownMenu_CreateInfo()
    info.text = "Best Brann Perk: " .. bestPerk
    info.notCheckable = true
    info.disabled = true
    UIDropDownMenu_AddButton(info, 1)

    info = UIDropDownMenu_CreateInfo()
    info.text = "Apply Best Perk"
    info.notCheckable = true
    info.func = function() SkillWeaver.BrannHelper:ApplyBestPerk() end
    UIDropDownMenu_AddButton(info, 1)

    info = UIDropDownMenu_CreateInfo()
    info.text = "Copy Perk ID"
    info.notCheckable = true
    info.func = function() C_System.SetClipboard(bestPerk) end
    UIDropDownMenu_AddButton(info, 1)
end

-- Register the UI hook (assuming SkillWeaver.MinimapButton exists)
if SkillWeaver.MinimapButton then
    SkillWeaver.MinimapButton:AddSubMenu("Brann Perk Helper", function(menu) SkillWeaver.BrannHelper:PopulateMinimapMenu(menu) end)
end

-- End of BrannHelper.lua
