-- ContentDetector.lua – Automatically detects current game content type

SkillWeaver = SkillWeaver or {}
SkillWeaver.ContentDetector = {}
local ContentDetector = SkillWeaver.ContentDetector

-- Detect current content type
function ContentDetector:GetCurrentContent()
    if IsInInstance() then
        local name, instanceType, difficulty, difficultyName, maxPlayers = GetInstanceInfo()
        
        if instanceType == "party" then
            -- Mythic+ Detection
            local level, affixes, wasEnergized = C_ChallengeMode.GetActiveKeystoneInfo()
            if level then
                return "MYTHIC_PLUS", level, affixes
            else
                return "DUNGEON", difficulty
            end
        elseif instanceType == "raid" then
            return "RAID", difficulty, maxPlayers
        elseif instanceType == "pvp" or instanceType == "arena" then
            return "PVP", instanceType
        end
    elseif C_PlayerInfo and C_PlayerInfo.IsPlayerInWorld and C_PlayerInfo.IsPlayerInWorld() then
        -- Check for Delves (The War Within)
        if C_Scenario and C_Scenario.IsInScenario() then
            local scenarioType = C_Scenario.GetScenarioType()
            -- LE_SCENARIO_TYPE_DELVE is likely 3 or similar in TWW, checking generic scenario for now
            -- Ideally we check specific IDs or wait for constant
            if scenarioType == LE_SCENARIO_TYPE_DELVE or scenarioType == 3 then 
                return "DELVE", C_Scenario.GetDifficultyLevel()
            end
        end
        return "OPEN_WORLD"
    end
    
    return "OPEN_WORLD" -- Fallback
end

-- Initialize
function ContentDetector:Initialize()
    local frame = CreateFrame("Frame")
    frame:RegisterEvent("PLAYER_ENTERING_WORLD")
    frame:RegisterEvent("CHALLENGE_MODE_START")
    frame:RegisterEvent("ENCOUNTER_START")
    frame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
    
    frame:SetScript("OnEvent", function(self, event)
        local content, level = ContentDetector:GetCurrentContent()
        -- Optional: Fire a custom event or callback here
        -- SkillWeaver:TriggerEvent("CONTENT_CHANGED", content, level)
    end)
    
    print("|cff00FF00SkillWeaver|r: Content Detector initialized.")
end

return ContentDetector
