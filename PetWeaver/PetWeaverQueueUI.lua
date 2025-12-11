local addonName, addon = ...
local UI = PetWeaverUI

-- Queue Panel UI
UI.queuePanel = UI.queuePanel or {}
local QueuePanel = UI.queuePanel

function QueuePanel:Create()
    local frame = CreateFrame("Frame", "PetWeaverQueuePanel", UIParent, "BasicFrameTemplateWithInset")
    frame:SetSize(600, 500)
    frame:SetPoint("CENTER")
    frame:Hide()
    frame:SetMovable(true)
    frame:EnableMouse(true)
    frame:RegisterForDrag("LeftButton")
    frame:SetScript("OnDragStart", frame.StartMoving)
    frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
    
    frame.title = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    frame.title:SetPoint("TOP", 0, -5)
    frame.title:SetText("Queue Manager")
    
    -- Mode tabs
    local levelingTab = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    levelingTab:SetSize(150, 30)
    levelingTab:SetPoint("TOPLEFT", 20, -30)
    levelingTab:SetText("Leveling Queue")
    levelingTab:SetScript("OnClick", function()
        self:ShowLevelingMode()
    end)
    frame.levelingTab = levelingTab
    
    local gatheringTab = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    gatheringTab:SetSize(150, 30)
    gatheringTab:SetPoint("LEFT", levelingTab, "RIGHT", 10, 0)
    gatheringTab:SetText("Gathering Queue")
    gatheringTab:SetScript("OnClick", function()
        self:ShowGatheringMode()
    end)
    frame.gatheringTab = gatheringTab
    
    -- Content frame (switching based on mode)
    local content = CreateFrame("Frame", nil, frame)
    content:SetPoint("TOPLEFT", 20, -70)
    content:SetPoint("BOTTOMRIGHT", -20, 40)
    frame.content = content
    
    -- Status text
    local status = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    status:SetPoint("BOTTOM", 0, 10)
    status:SetText("Select encounters to generate queue")
    frame.status = status
    
    self.frame = frame
    return frame
end

function QueuePanel:ShowLevelingMode()
    if not self.frame then return end
    
    -- Clear content
    self.frame.content:Hide()
    self.frame.content = CreateFrame("Frame", nil, self.frame)
    self.frame.content:SetPoint("TOPLEFT", 20, -70)
    self.frame.content:SetPoint("BOTTOMRIGHT", -20, 40)
    
    -- Instructions
    local instructions = self.frame.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    instructions:SetPoint("TOP", 0, -10)
   

 instructions:SetText("Select encounters from the browser, then click 'Generate Leveling Queue'")
    instructions:SetWidth(540)
    
    -- Generate button
    local generateBtn = CreateFrame("Button", nil, self.frame.content, "GameMenuButtonTemplate")
    generateBtn:SetSize(200, 35)
    generateBtn:SetPoint("TOP", 0, -40)
    generateBtn:SetText("Generate Leveling Queue")
    generateBtn:SetScript("OnClick", function()
        self:GenerateLevelingQueue()
    end)
    
    -- Queue display (scroll frame)
    local scrollFrame = CreateFrame("ScrollFrame", nil, self.frame.content, "UIPanelScrollFrameTemplate")
    scrollFrame:SetPoint("TOPLEFT", 10, -90)
    scrollFrame:SetPoint("BOTTOMRIGHT", -30, 10)
    
    local scrollChild = CreateFrame("Frame", nil, scrollFrame)
    scrollChild:SetSize(520, 1)
    scrollFrame:SetScrollChild(scrollChild)
    self.frame.content.scrollChild = scrollChild
    
    self.frame.content:Show()
end

function QueuePanel:ShowGatheringMode()
    if not self.frame then return end
    
    -- Clear content
    self.frame.content:Hide()
    self.frame.content = CreateFrame("Frame", nil, self.frame)
    self.frame.content:SetPoint("TOPLEFT", 20, -70)
    self.frame.content:SetPoint("BOTTOMRIGHT", -20, 40)
    
    -- Instructions
    local instructions = self.frame.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    instructions:SetPoint("TOP", 0, -10)
    instructions:SetText("Select encounters from the browser, then click 'Generate Gathering Queue'")
    instructions:SetWidth(540)
    
    -- Generate button
    local generateBtn = CreateFrame("Button", nil, self.frame.content, "GameMenuButtonTemplate")
    generateBtn:SetSize(200, 35)
    generateBtn:SetPoint("TOP", 0, -40)
    generateBtn:SetText("Generate Gathering Queue")
    generateBtn:SetScript("OnClick", function()
        self:GenerateGatheringQueue()
    end)
    
    -- Queue display (scroll frame)
    local scrollFrame = CreateFrame("ScrollFrame", nil, self.frame.content, "UIPanelScrollFrameTemplate")
    scrollFrame:SetPoint("TOPLEFT", 10, -90)
    scrollFrame:SetPoint("BOTTOMRIGHT", -30, 10)
    
    local scrollChild = CreateFrame("Frame", nil, scrollFrame)
    scrollChild:SetSize(520, 1)
    scrollFrame:SetScrollChild(scrollChild)
    self.frame.content.scrollChild = scrollChild
    
    self.frame.content:Show()
end

function QueuePanel:GenerateLevelingQueue()
    -- Get selected encounters from browser
    local selectedEncounters = UI.browser:GetSelectedEncounters()
    
    if not selectedEncounters or #selectedEncounters == 0 then
        self.frame.status:SetText("|cffff0000No encounters selected! Check encounters in the browser.|r")
        return
    end
    
    -- Generate queue
    local queue = UI.queueManager:GenerateLevelingQueueForEncounters(selectedEncounters)
    
    if #queue == 0 then
        self.frame.status:SetText("|cff00ff00All pets are ready! No leveling needed.|r")
        return
    end
    
    -- Display queue
    self:DisplayLevelingQueue(queue)
    self.frame.status:SetText(string.format("|cff00ff00Queue generated: %d pets to level|r", #queue))
end

function QueuePanel:DisplayLevelingQueue(queue)
    local scrollChild = self.frame.content.scrollChild
    if not scrollChild then return end
    
    -- Clear existing
    for _, child in ipairs({scrollChild:GetChildren()}) do
        child:Hide()
        child:SetParent(nil)
    end
    
    local yOffset = 0
    
    for i, item in ipairs(queue) do
        local petFrame = CreateFrame("Frame", nil, scrollChild, "BackdropTemplate")
        petFrame:SetSize(500, 80)
        petFrame:SetPoint("TOP", 0, yOffset)
        petFrame:SetBackdrop({
            bgFile = "Interface/Tooltips/UI-Tooltip-Background",
            edgeFile = "Interface/Tooltips/UI-Tooltip-Border",
            tile = true, tileSize = 16, edgeSize = 16,
            insets = { left = 4, right = 4, top = 4, bottom = 4 }
        })
        petFrame:SetBackdropColor(0.1, 0.1, 0.1, 0.8)
        
        -- Pet name and level
        local petName = petFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        petName:SetPoint("TOPLEFT", 10, -10)
        petName:SetText(string.format("%s (Level %d) - Priority: %d", item.pet.name, item.pet.currentLevel, item.priority))
        
        -- Needed for
        local needed = petFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
        needed:SetPoint("TOPLEFT", 10, -30)
        needed:SetText("Needed for: " .. table.concat(item.pet.neededFor, ", "))
        needed:SetWidth(480)
        needed:SetJustifyH("LEFT")
        
        -- Leveling encounters
        local encounters = petFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
        encounters:SetPoint("TOPLEFT", 10, -50)
        encounters:SetText("|cff00ff00Level at:|r " .. table.concat(item.encounters, ", "))
        encounters:SetWidth(480)
        encounters:SetJustifyH("LEFT")
        
        yOffset = yOffset - 85
    end
    
    scrollChild:SetHeight(math.abs(yOffset))
end

function QueuePanel:GenerateGatheringQueue()
    -- Get selected encounters from browser
    local selectedEncounters = UI.browser:GetSelectedEncounters()
    
    if not selectedEncounters or #selectedEncounters == 0 then
        self.frame.status:SetText("|cffff0000No encounters selected! Check encounters in the browser.|r")
        return
    end
    
    -- Generate queue
    local route = UI.queueManager:GenerateGatheringQueueForEncounters(selectedEncounters)
    
    if #route == 0 then
        self.frame.status:SetText("|cff00ff00No missing pets! You're ready for all selected encounters.|r")
        return
    end
    
    -- Display route
    self:DisplayGatheringQueue(route)
    
    local totalPets = 0
    for _, stop in ipairs(route) do
        totalPets = totalPets + stop.count
    end
    self.frame.status:SetText(string.format("|cff00ff00Route generated: %d pets in %d zones|r", totalPets, #route))
end

function QueuePanel:DisplayGatheringQueue(route)
    local scrollChild = self.frame.content.scrollChild
    if not scrollChild then return end
    
    -- Clear existing
    for _, child in ipairs({scrollChild:GetChildren()}) do
        child:Hide()
        child:SetParent(nil)
    end
    
    local yOffset = 0
    
    for i, stop in ipairs(route) do
        -- Zone header
        local zoneFrame = CreateFrame("Frame", nil, scrollChild, "BackdropTemplate")
        zoneFrame:SetSize(500, 40)
        zoneFrame:SetPoint("TOP", 0, yOffset)
        zoneFrame:SetBackdrop({
            bgFile = "Interface/Tooltips/UI-Tooltip-Background",
            edgeFile = "Interface/Tooltips/UI-Tooltip-Border",
            tile = true, tileSize = 16, edgeSize = 16,
            insets = { left = 4, right = 4, top = 4, bottom = 4 }
        })
        zoneFrame:SetBackdropColor(0.2, 0.3, 0.4, 0.9)
        
        local zoneName = zoneFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        zoneName:SetPoint("LEFT", 10, 0)
        zoneName:SetText(string.format("%s - %s (%d pets)", stop.continent, stop.zone, stop.count))
        
        -- Waypoint button
        local waypointBtn = CreateFrame("Button", nil, zoneFrame, "GameMenuButtonTemplate")
        waypointBtn:SetSize(120, 25)
        waypointBtn:SetPoint("RIGHT", -10, 0)
        waypointBtn:SetText("Set Waypoints")
        waypointBtn:SetNormalFontObject("GameFontNormalSmall")
        waypointBtn:SetScript("OnClick", function()
            UI.queueManager:SetWaypointsForZone(stop)
        end)
        
        yOffset = yOffset - 45
        
        -- Pets in zone
        for j, pet in ipairs(stop.pets) do
            local petFrame = CreateFrame("Frame", nil, scrollChild)
            petFrame:SetSize(480, 20)
            petFrame:SetPoint("TOPLEFT", 20, yOffset)
            
            local petText = petFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
            petText:SetPoint("LEFT", 0, 0)
            local coords = pet.location and string.format("(%0.1f, %0.1f)", pet.location.x, pet.location.y) or "(No coords)"
            petText:SetText(string.format("• %s %s - Needed for %d encounters", pet.name, coords, pet.priority))
            petText:SetWidth(480)
            petText:SetJustifyH("LEFT")
            
            yOffset = yOffset - 22
        end
        
        yOffset = yOffset - 10
    end
    
    scrollChild:SetHeight(math.abs(yOffset))
end

function QueuePanel:Show()
    if self.frame then
        self.frame:Show()
        self:ShowLevelingMode() -- Default to leveling mode
    end
end

function QueuePanel:Hide()
    if self.frame then
        self.frame:Hide()
    end
end

function QueuePanel:Toggle()
    if self.frame and self.frame:IsShown() then
        self:Hide()
    else
        self:Show()
    end
end
