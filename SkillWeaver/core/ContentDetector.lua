local ADDON_NAME, SkillWeaver = ...

local ContentDetector = {}
SkillWeaver.ContentDetector = ContentDetector

-- State
ContentDetector.CurrentType = "OPEN_WORLD" -- Default
ContentDetector.Difficulty = 0

-- Constants
local TYPE_OPEN_WORLD = "OPEN_WORLD"
local TYPE_DUNGEON = "DUNGEON"
local TYPE_MYTHIC_PLUS = "MYTHIC_PLUS"
local TYPE_RAID = "RAID"
local TYPE_PVP = "PVP"
local TYPE_ARENA = "ARENA"
local TYPE_DELVE = "DELVE" -- War Within Feature

function ContentDetector:Detect()
    local _, instanceType, difficultyID, _, _, _, _, instanceID = GetInstanceInfo()
    self.Difficulty = difficultyID
    
    -- Default
    local newType = TYPE_OPEN_WORLD
    
    if instanceType == "party" then
        if difficultyID == 8 then
            newType = TYPE_MYTHIC_PLUS
        else
            newType = TYPE_DUNGEON
        end
    elseif instanceType == "raid" then
        newType = TYPE_RAID
    elseif instanceType == "pvp" then
        newType = TYPE_PVP
    elseif instanceType == "arena" then
        newType = TYPE_ARENA
    elseif instanceType == "scenario" then
        -- Delves are likely scenarios in 11.0
        -- We can refine this check later with specific Map IDs if needed
        newType = TYPE_DELVE 
    end
    
    -- Check for Open World PvP (War Mode)?
    -- C_PvP.IsWarModeDesired()
    
    if self.CurrentType ~= newType then
        print("SkillWeaver: Content Changed -> " .. newType)
        self.CurrentType = newType
        
        -- Trigger Profile Update if needed
        if SkillWeaver.OnContentChanged then
            SkillWeaver:OnContentChanged(newType)
        end
    end
end

-- Event Handling
local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
frame:RegisterEvent("CHALLENGE_MODE_START")
frame:SetScript("OnEvent", function()
    ContentDetector:Detect()
end)

-- Public API for Conditions
function ContentDetector:IsType(checkType)
    return self.CurrentType == checkType
end

function ContentDetector:IsMythicPlus()
    return self.CurrentType == TYPE_MYTHIC_PLUS
end

function ContentDetector:IsRaid()
    return self.CurrentType == TYPE_RAID
end

function ContentDetector:IsPvP()
    return self.CurrentType == TYPE_PVP or self.CurrentType == TYPE_ARENA
end

return ContentDetector
