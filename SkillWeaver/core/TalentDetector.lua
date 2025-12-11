local ADDON_NAME, SkillWeaver = ...

--[[
    TalentDetector.lua
    
    Automatically detects active talents using C_Traits API.
    Enables sequences to adapt to player's talent build without manual selection.
    
    Usage:
        SkillWeaver.TalentDetector:HasTalent("Avatar")  -- Returns true/false
        SkillWeaver.TalentDetector:GetActiveTalents()   -- Returns table of all active talents
]]

SkillWeaver.TalentDetector = {}
local TalentDetector = SkillWeaver.TalentDetector

-- Cache for talent lookups (updated on TRAIT_CONFIG_UPDATED)
TalentDetector.cache = {}
TalentDetector.lastUpdate = 0

--[[
    Check if a specific talent is active
    @param talentName string - Name of the talent to check
    @return boolean - True if talent is active
]]
function TalentDetector:HasTalent(talentName)
    if not talentName then return false end
    
    -- Use cache if recent (< 1 second old)
    local now = GetTime()
    if self.cache[talentName] ~= nil and (now - self.lastUpdate) < 1 then
        return self.cache[talentName]
    end
    
    -- Refresh cache if stale
    if (now - self.lastUpdate) >= 1 then
        self:RefreshCache()
    end
    
    return self.cache[talentName] or false
end

--[[
    Check if PvP talent is active (separate from regular talents)
    @param talentName string - Name of PvP talent
    @return boolean - True if PvP talent is active
]]
function TalentDetector:HasPvPTalent(talentName)
    if not talentName or not C_SpecializationInfo then return false end
    
    -- Check each PvP talent slot (usually 3 slots)
    for i = 1, 3 do
        local slotInfo = C_SpecializationInfo.GetPvpTalentSlotInfo(i)
        if slotInfo and slotInfo.selectedTalent then
            local talentID = slotInfo.selectedTalent
            local _, name = GetPvpTalentInfoByID(talentID)
            if name == talentName then
                return true
            end
        end
    end
    
    return false
end

--[[
    Refresh the talent cache by scanning active config
    Uses C_Traits API (Dragonflight+) with fallbacks for API changes
]]
function TalentDetector:RefreshCache()
    self.cache = {}
    self.lastUpdate = GetTime()
    
    -- Check if modern API exists (future-proof for Midnight changes)
    if not C_ClassTalents or not C_ClassTalents.GetActiveConfigID then
        -- Fallback: Try legacy API or disable feature gracefully
        print("SkillWeaver: Talent detection API unavailable. Using default sequences.")
        return
    end
    
    -- Get active talent config
    local configID = C_ClassTalents.GetActiveConfigID()
    if not configID then return end
    
    -- Safely get config info (API might change in Midnight)
    local success, configInfo = pcall(C_Traits.GetConfigInfo, configID)
    if not success or not configInfo then
        print("SkillWeaver: Talent API changed. Please update addon.")
        return
    end
    
    -- Scan all trees in the config (includes Hero talents in Midnight)
    for _, treeID in ipairs(configInfo.treeIDs or {}) do
        local success, nodes = pcall(C_Traits.GetTreeNodes, treeID)
        if success and nodes then
            for _, nodeID in ipairs(nodes) do
                local nodeSuccess, nodeInfo = pcall(C_Traits.GetNodeInfo, configID, nodeID)
                
                -- Check if talent has points allocated
                if nodeSuccess and nodeInfo and nodeInfo.currentRank and nodeInfo.currentRank > 0 then
                    -- Get entry info for the active talent
                    if nodeInfo.activeEntry and nodeInfo.activeEntry.entryID then
                        local entrySuccess, entryInfo = pcall(C_Traits.GetEntryInfo, configID, nodeInfo.activeEntry.entryID)
                        if entrySuccess and entryInfo and entryInfo.definitionID then
                            local defSuccess, definitionInfo = pcall(C_Traits.GetDefinitionInfo, entryInfo.definitionID)
                            if defSuccess and definitionInfo and definitionInfo.spellID then
                                -- Get spell name
                                local spellName = GetSpellInfo(definitionInfo.spellID)
                                if spellName then
                                    self.cache[spellName] = true
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end

--[[
    Get all active talents as a table
    @return table - Table with talent names as keys, true as values
]]
function TalentDetector:GetActiveTalents()
    local now = GetTime()
    if (now - self.lastUpdate) >= 1 then
        self:RefreshCache()
    end
    
    return self.cache
end

--[[
    Print all active talents (for debugging)
]]
function TalentDetector:PrintActiveTalents()
    self:RefreshCache()
    
    print("=== Active Talents ===")
    local count = 0
    for talentName, _ in pairs(self.cache) do
        print("  - " .. talentName)
        count = count + 1
    end
    print("Total: " .. count .. " talents")
end

-- Register for talent changes
local frame = CreateFrame("Frame")
frame:RegisterEvent("TRAIT_CONFIG_UPDATED")
frame:RegisterEvent("ACTIVE_TALENT_GROUP_CHANGED")
frame:RegisterEvent("PLAYER_SPECIALIZATION_CHANGED")

frame:SetScript("OnEvent", function(self, event)
    -- Refresh talent cache when talents change
    TalentDetector:RefreshCache()
end)

-- Slash command for debugging
SLASH_SWTALENTS1 = "/swtalents"
SlashCmdList["SWTALENTS"] = function()
    TalentDetector:PrintActiveTalents()
end
