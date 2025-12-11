local addonName, addon = ...
local Holocron = addon.Holocron
local Codex = {}
addon.Codex = Codex

-- ============================================================================
-- Codex Module
-- ============================================================================

function Codex:Create(parent)
    local frame = CreateFrame("Frame", nil, parent)
    frame:SetAllPoints()
    frame:Hide()
    
    -- Title
    local title = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    title:SetPoint("TOPLEFT", 10, -10)
    title:SetText("The Codex: Campaign Tracker")
    
    -- Scroll Frame for Quest List
    local scrollFrame = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
    scrollFrame:SetPoint("TOPLEFT", 10, -50)
    scrollFrame:SetPoint("BOTTOMRIGHT", -30, 10)
    
    local content = CreateFrame("Frame", nil, scrollFrame)
    content:SetSize(500, 500) 
    scrollFrame:SetScrollChild(content)
    frame.content = content
    
    self.frame = frame
    self:Render()
    
    return frame
end

function Codex:Render()
    if not self.frame then return end
    local content = self.frame.content
    
    -- Clear existing children (simple way: hide them and reuse or just recreate for MVP)
    -- For MVP, let's just create new ones and assume we don't leak too much memory on frequent refreshes
    -- Ideally we'd use a pool.
    if self.buttons then
        for _, btn in pairs(self.buttons) do btn:Hide() end
    end
    self.buttons = {}
    
    if not CodexDB or not CodexDB.QuestCoords then
        local msg = content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        msg:SetPoint("TOPLEFT", 10, -10)
        msg:SetText("No Codex Data Loaded. Run export_codex_data.py")
        return
    end
    
    -- Filter Missing Quests
    local missingQuests = {}
    for qID, info in pairs(CodexDB.QuestCoords) do
        -- Check if NOT completed
        local completed = C_QuestLog.IsQuestFlaggedCompleted(qID)
        -- Check if NOT active
        local active = C_QuestLog.IsOnQuest(qID)
        
        if not completed and not active then
            table.insert(missingQuests, {id = qID, info = info})
        end
    end
    
    -- Sort by ID
    table.sort(missingQuests, function(a,b) return a.id < b.id end)
    
    local yOffset = 0
    for i, q in ipairs(missingQuests) do
        local btn = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
        btn:SetSize(400, 30)
        btn:SetPoint("TOPLEFT", 0, -yOffset)
        btn:SetText(q.info.title)
        
        btn:SetScript("OnClick", function()
            self:SetQuestWaypoint(q.id)
        end)
        
        table.insert(self.buttons, btn)
        yOffset = yOffset + 35
    end
    
    content:SetHeight(yOffset + 20)
end

-- ============================================================================
-- Navigation Logic
-- ============================================================================

function Codex:SetQuestWaypoint(questID)
    local qID = tonumber(questID)
    
    -- Case 1: Active Quest
    if C_QuestLog.IsOnQuest(qID) then
        C_SuperTrack.SetSuperTrackedQuestID(qID)
        print("|cff00ffffHolocron:|r Tracking active quest objectives.")
        return
    end

    -- Case 2: Missing Quest
    if not CodexDB or not CodexDB.QuestCoords then return end
    
    local info = CodexDB.QuestCoords[qID]
    if info then
        local uiMapPoint = UiMapPoint.CreateFromCoordinates(info.mapID, info.x, info.y)
        C_Map.SetUserWaypoint(uiMapPoint)
        C_SuperTrack.SetSuperTrackedUserWaypoint(true)
        print("|cff00ffffHolocron:|r Navigation set to start of: " .. info.title)
    else
        print("|cff00ffffHolocron:|r No coordinates found for Quest ID " .. qID)
    end
end

-- Hook into Quest Log
local function HookQuestLog()
    if not QuestMapFrame then return end
    
    local btn = CreateFrame("Button", "HolocronNavBtn", QuestMapFrame.DetailsFrame, "UIPanelButtonTemplate")
    btn:SetSize(100, 22)
    btn:SetPoint("TOPRIGHT", QuestMapFrame.DetailsFrame, "TOPRIGHT", -10, -35)
    btn:SetText("Show Waypoint")
    btn:Hide()
    
    btn:SetScript("OnClick", function()
        local questID = QuestMapFrame.DetailsFrame.questID
        if questID then
            Codex:SetQuestWaypoint(questID)
        end
    end)
    
    hooksecurefunc("QuestMapFrame_ShowQuestDetails", function(questID)
        if CodexDB and CodexDB.QuestCoords and CodexDB.QuestCoords[questID] then
            btn:Show()
        else
            btn:Hide()
        end
    end)
end

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:SetScript("OnEvent", function()
    HookQuestLog()
end)
