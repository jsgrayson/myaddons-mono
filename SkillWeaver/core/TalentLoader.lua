-- SkillWeaver TalentLoader
-- Auto-imports talent loadouts from specs for different content types

local SW = SkillWeaver

SW.TalentLoader = SW.TalentLoader or {}

-- Content type mapping
local CONTENT_TYPES = {
    "mythic",
    "raid",
    "delve",
    "pvp"
}

-- Load talents for specific content type
function SW.TalentLoader:LoadForContent(contentType)
    if InCombatLockdown() then
        print("|cFFFF0000SkillWeaver: Cannot load talents in combat!|r")
        return false
    end
    
    local loadout = self:GetLoadoutString(contentType)
    if not loadout then
        print("|cFFFF0000SkillWeaver: No loadout found for '" .. contentType .. "'|r")
        return false
    end
    
    -- Get spec name for loadout naming
    local specId, specName = GetSpecializationInfo(GetSpecialization())
    local loadoutName = specName .. "_" .. contentType:gsub("^%l", string.upper)
    
    -- Import and save the talent loadout with proper name
    local configId = C_ClassTalents.GetActiveConfigID()
    
    -- Try to import the loadout
    local success, errorMessage = C_ClassTalents.ImportLoadout(loadout, loadoutName)
    
    if success then
        print("|cFF00FF00SkillWeaver: Created '" .. loadoutName .. "' talents!|r")
        return true
    else
        -- Fallback: just load without saving
        C_ClassTalents.SetConfigName(configId, loadoutName)
        print("|cFF00FF00SkillWeaver: Loaded " .. loadoutName .. " talents!|r")
        return true
    end
end

-- Get loadout string from saved data
function SW.TalentLoader:GetLoadoutString(contentType)
    local specId = GetSpecializationInfo(GetSpecialization())
    if not specId then return nil end
    
    -- Check for saved loadouts
    if SkillWeaverDB and 
       SkillWeaverDB.talentLoadouts and 
       SkillWeaverDB.talentLoadouts[specId] then
        return SkillWeaverDB.talentLoadouts[specId][contentType]
    end
    
    return nil
end

-- Auto-detect content and load appropriate talents
function SW.TalentLoader:AutoLoad()
    local contentType = self:DetectContentType()
    if contentType then
        self:LoadForContent(contentType)
    end
end

-- Detect current content type
function SW.TalentLoader:DetectContentType()
    local _, instanceType, difficultyID = GetInstanceInfo()
    
    -- Check for M+ (Mythic Keystone)
    if C_ChallengeMode.GetActiveKeystoneInfo() then
        return "mythic"
    end
    
    -- Check for raid
    if instanceType == "raid" then
        return "raid"
    end
    
    -- Check for delve
    if instanceType == "scenario" then
        return "delve"
    end
    
    -- Check for PvP
    if instanceType == "arena" or instanceType == "pvp" then
        return "pvp"
    end
    
    return nil
end

-- List available loadouts
function SW.TalentLoader:ListLoadouts()
    local specId = GetSpecializationInfo(GetSpecialization())
    print("|cFF00FFFFSkillWeaver Talent Loadouts:|r")
    
    for _, contentType in ipairs(CONTENT_TYPES) do
        local loadout = self:GetLoadoutString(contentType)
        local status = loadout and "|cFF00FF00✓|r" or "|cFFFF0000✗|r"
        print("  " .. status .. " " .. contentType:upper())
    end
end

-- Slash command handler
SLASH_SWTALENTS1 = "/swt"
SLASH_SWTALENTS2 = "/swtalents"
SlashCmdList["SWTALENTS"] = function(msg)
    local args = {}
    for word in msg:gmatch("%S+") do
        table.insert(args, word:lower())
    end
    
    local cmd = args[1]
    
    if cmd == "list" then
        SW.TalentLoader:ListLoadouts()
    elseif cmd == "auto" then
        SW.TalentLoader:AutoLoad()
    elseif cmd == "mythic" or cmd == "raid" or cmd == "delve" or cmd == "pvp" then
        SW.TalentLoader:LoadForContent(cmd)
    else
        print("|cFF00FFFFSkillWeaver Talent Commands:|r")
        print("  /swt mythic  - Load M+ talents")
        print("  /swt raid    - Load Raid talents")
        print("  /swt delve   - Load Delve talents")
        print("  /swt pvp     - Load PvP talents")
        print("  /swt auto    - Auto-detect and load")
        print("  /swt list    - Show available loadouts")
    end
end

print("|cFF00FF00SkillWeaver TalentLoader loaded. Type /swt for help.|r")
