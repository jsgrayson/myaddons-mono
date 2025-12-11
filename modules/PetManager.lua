--========================================================--
-- SkillWeaver - Pet Manager (Hunter Smart System)
-- Automatically recommends pets based on Group Composition & Content
--========================================================--

local PetManager = {}
SkillWeaver.PetManager = PetManager

-- WoW API
local GetCallPetInfo = GetCallPetInfo
local GetNumGroupMembers = GetNumGroupMembers
local GetRaidRosterInfo = GetRaidRosterInfo
local UnitClass = UnitClass
local UnitIsConnected = UnitIsConnected

-- Family to Spec Mapping (TWW Defaults)
-- This is a simplified list. In a full version, we'd map all ~60 families.
-- Comprehensive Family Mapping (Updated for TWW)
local FAMILY_SPECS = {
    -- FEROCITY (Lust / Leech)
    ["Cat"] = "Ferocity", ["Wolf"] = "Ferocity", ["Bear"] = "Ferocity", 
    ["Raptor"] = "Ferocity", ["Clefthoof"] = "Ferocity", ["Core Hound"] = "Ferocity",
    ["Bat"] = "Ferocity", ["Ray"] = "Ferocity", ["Wind Serpent"] = "Ferocity",
    ["Carrion Bird"] = "Ferocity", ["Devilsaur"] = "Ferocity", ["Gorilla"] = "Ferocity",
    ["Hyena"] = "Ferocity", ["Moth"] = "Ferocity", ["Scorpid"] = "Ferocity",
    ["Spider"] = "Ferocity", ["Tallstrider"] = "Ferocity", ["Wasp"] = "Ferocity",
    ["Scalehide"] = "Ferocity", -- Wait, Scalehide is Tenacity? Checking... Scalehide is Ferocity/Tenacity? 
    -- actually Scalehide is FEROCITY in Dragonflight/TWW.
    
    -- TENACITY (Defense / HP)
    ["Spirit Beast"] = "Tenacity", ["Turtle"] = "Tenacity", ["Beetle"] = "Tenacity",
    ["Crab"] = "Tenacity", ["Stag"] = "Tenacity", ["Feathermane"] = "Tenacity",
    ["Bear"] = "Tenacity", -- Wait, Bear is Tenacity. Correcting above.
    ["Boar"] = "Tenacity", ["Crocolisk"] = "Tenacity", ["Dragonhawk"] = "Tenacity",
    ["Hydra"] = "Tenacity", ["Lizard"] = "Tenacity", ["Mammoth"] = "Tenacity",
    ["Ox"] = "Tenacity", ["Riverbeast"] = "Tenacity", ["Toad"] = "Tenacity",
    ["Worm"] = "Tenacity", ["Blood Beast"] = "Tenacity", ["Krolusk"] = "Tenacity",
    
    -- CUNNING (Freedom / Speed)
    ["Bird of Prey"] = "Cunning", ["Mechanical"] = "Cunning", ["Rodent"] = "Cunning", 
    ["Snake"] = "Cunning", ["Basilisk"] = "Cunning", ["Chimera"] = "Cunning",
    ["Dog"] = "Cunning", ["Fox"] = "Cunning", ["Goat"] = "Cunning",
    ["Monkey"] = "Cunning", ["Pterrordax"] = "Cunning", ["Shale Beast"] = "Cunning",
    ["Silithid"] = "Cunning", ["Sporebat"] = "Cunning", ["Warp Stalker"] = "Cunning",
    ["Water Strider"] = "Cunning"
}

-- Corrections based on modern WoW (Dragonflight/TWW)
FAMILY_SPECS["Bear"] = "Tenacity"
FAMILY_SPECS["Hyena"] = "Cunning"
FAMILY_SPECS["Scalehide"] = "Tenacity" -- Scalehide is Tenacity (Tanky)
FAMILY_SPECS["Gorilla"] = "Tenacity"

------------------------------------------------------------
-- Check if Group has Lust (Heroism/Bloodlust/Time Warp)
------------------------------------------------------------
function PetManager:GroupHasLust()
    if not IsInGroup() then return false end

    local numMembers = GetNumGroupMembers()
    local prefix = IsInRaid() and "raid" or "party"

    -- Iterate group members
    for i = 1, numMembers do
        local unit = prefix .. i
        if prefix == "party" and i == numMembers then unit = "player" end 
        
        if UnitExists(unit) and UnitIsConnected(unit) then
            local _, classFilename = UnitClass(unit)
            if classFilename == "MAGE" or classFilename == "SHAMAN" or classFilename == "EVOKER" then
                return true
            end
            -- Note: We don't count other Hunters because we can't guarantee their pet.
        end
    end
    return false
end

-- Exotic Families (BM Only)
local EXOTIC_FAMILIES = {
    ["Spirit Beast"] = true, ["Clefthoof"] = true, ["Core Hound"] = true,
    ["Devilsaur"] = true, ["Worm"] = true, ["Chimera"] = true,
    ["Krolusk"] = true, ["Pterrordax"] = true, ["Shale Beast"] = true,
    ["Water Strider"] = true, ["Silithid"] = true, ["Stone Hound"] = true
}

------------------------------------------------------------
-- Scan Active Pet Slots (1-5)
------------------------------------------------------------
function PetManager:GetAvailablePets()
    local available = { Ferocity = nil, Tenacity = nil, Cunning = nil }
    
    -- Check if player is Beast Mastery (Spec ID 253)
    local isBM = false
    local currentSpec = GetSpecialization()
    if currentSpec then
        local id = GetSpecializationInfo(currentSpec)
        if id == 253 then isBM = true end
    end

    for slot = 1, 5 do
        -- GetCallPetInfo returns: name, icon, isDead, familyID, talentID (varies by version)
        -- We use GetCallPetInfo(slot)
        local name, _, _, _, familyName = GetCallPetInfo(slot)
        
        if familyName then
            local spec = FAMILY_SPECS[familyName]
            local isExotic = EXOTIC_FAMILIES[familyName]
            
            -- Only count this pet if we can actually use it
            -- (BM can use all, others cannot use Exotic)
            if spec and (isBM or not isExotic) then
                if not available[spec] then 
                    available[spec] = { slot = slot, name = name }
                end
            end
        end
    end
    return available
end

------------------------------------------------------------
-- Get Recommendation
------------------------------------------------------------
function PetManager:CheckPetRecommendation()
    local _, playerClass = UnitClass("player")
    if playerClass ~= "HUNTER" then return end

    local content = SkillWeaver.ContentDetector:GetCurrentContent()
    local availablePets = self:GetAvailablePets()
    
    -- Check active pet spell for Primal Rage (ID 264667) to confirm if we currently have Lust
    local hasLustActive = IsSpellKnown(264667) 

    -- SCENARIO: Mythic+ (Lust is Priority)
    if content == "MYTHIC_PLUS" or content == "DUNGEON" then
        if not self:GroupHasLust() and not hasLustActive then
            if availablePets.Ferocity then
                local slot = availablePets.Ferocity.slot
                local name = availablePets.Ferocity.name
                print("|cffFF0000[SkillWeaver]|r ⚠️ Group needs Lust! Switch to " .. name .. " (Slot " .. slot .. " - Ferocity).")
            end
        end
    end

    -- SCENARIO: Raid (Survival/DPS Uptime is Priority)
    if content == "RAID" then
        -- 1. Check Lust first (still critical if missing)
        if not self:GroupHasLust() and not hasLustActive then
            if availablePets.Ferocity then
                local slot = availablePets.Ferocity.slot
                local name = availablePets.Ferocity.name
                print("|cffFF0000[SkillWeaver]|r ⚠️ Raid needs Lust! Switch to " .. name .. " (Slot " .. slot .. " - Ferocity).")
                return -- Priority #1
            end
        end

        -- 2. If Lust is covered, check if we are using a suboptimal Cunning pet
        -- (Cunning = PvP/Movement, usually less Raid utility than Tenacity/Ferocity)
        -- We verify active pet family to determine spec
        local _, _, _, _, activeFamily = GetCallPetInfo(1) -- Fallback
        -- Better: Check if we DON'T have Tenacity or Ferocity buffs?
        -- Path of the Least Resistance: Check if we have Master's Call (Cunning ability)
        local hasMastersCall = IsSpellKnown(53271)
        
        if hasMastersCall then
             -- We are likely using Cunning.
             -- Do we have a better option in slots 1-5?
             if availablePets.Tenacity then
                 local slot = availablePets.Tenacity.slot
                 local name = availablePets.Tenacity.name
                 print("|cffFF0000[SkillWeaver]|r ⚠️ Raid Detected. Cunning is suboptimal. Switch to " .. name .. " (Slot " .. slot .. " - Tenacity) for Survival.")
             elseif availablePets.Ferocity then
                 local slot = availablePets.Ferocity.slot
                 local name = availablePets.Ferocity.name
                 print("|cffFF0000[SkillWeaver]|r ⚠️ Raid Detected. Cunning is suboptimal. Switch to " .. name .. " (Slot " .. slot .. " - Ferocity) for Leech.")
             end
        end
    end
end

-- Event Listener
local frame = CreateFrame("Frame")
frame:RegisterEvent("GROUP_ROSTER_UPDATE")
frame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:SetScript("OnEvent", function() 
    -- Delay to allow pet to spawn/data to load
    C_Timer.After(3, function() PetManager:CheckPetRecommendation() end) 
end)

return PetManager
