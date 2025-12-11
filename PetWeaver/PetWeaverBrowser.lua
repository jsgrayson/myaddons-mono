local addonName, addon = ...
local UI = PetWeaverUI

-- Encounter Browser Panel
UI.browser = UI.browser or {}
local Browser = UI.browser

Browser.buttons = {}
Browser.selectedEncounters = {}  -- Track selected encounters for queue
function Browser:Create(parent)
    local frame = CreateFrame("Frame", nil, parent)
    frame:SetPoint("TOPLEFT", parent, "TOPLEFT", 10, -35)
    frame:SetPoint("BOTTOMLEFT", parent, "BOTTOMLEFT", 10, 10)
    frame:SetWidth(240)
    
    -- Search Box
    local searchBox = CreateFrame("EditBox", nil, frame, "SearchBoxTemplate")
    searchBox:SetSize(220, 20)
    searchBox:SetPoint("TOPLEFT", 0, 0)
    searchBox:SetAutoFocus(false)
    searchBox:SetScript("OnTextChanged", function(self)
        Browser:FilterEncounters(self:GetText())
    end)
    frame.searchBox = searchBox
    
    -- Filter Dropdown
    local filterBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    filterBtn:SetSize(70, 20)
    filterBtn:SetPoint("LEFT", searchBox, "RIGHT", 5, 0)
    filterBtn:SetText("Filter ▼")
    filterBtn:SetNormalFontObject("GameFontNormalSmall")
    
    -- Create filter menu
    local filterMenu = CreateFrame("Frame", "PetWeaverFilterMenu", frame, "UIDropDownMenuTemplate")
    filterBtn:SetScript("OnClick", function(self)
        local menu = {
            {text = "Show All", func = function() Browser:SetFilter("all") end},
            {text = "Ready Only", func = function() Browser:SetFilter("ready") end},
            {text = "Missing Pets", func = function() Browser:SetFilter("missing") end},
            {text = "Favorites", func = function() Browser:SetFilter("favorites") end},
            {text = "Completed", func = function() Browser:SetFilter("completed") end},
            {text = "─────────", isTitle = true},
            {text = "Shadowlands", func = function() Browser:SetFilter("Shadowlands") end},
            {text = "Dragonflight", func = function() Browser:SetFilter("Dragonflight") end},
            {text = "The War Within", func = function() Browser:SetFilter("The War Within") end}
        }
        EasyMenu(menu, filterMenu, "cursor", 0 , 0, "MENU")
    end)
    frame.filterBtn = filterBtn
    
    Browser.currentFilter = "all"  -- Track active filter
    
    -- Scroll Frame
    local scrollFrame = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
    scrollFrame:SetPoint("TOPLEFT", searchBox, "BOTTOMLEFT", 0, -10)
    scrollFrame:SetPoint("BOTTOMRIGHT", frame, "BOTTOMRIGHT", -25, 35)
    
    local scrollChild = CreateFrame("Frame", nil, scrollFrame)
    scrollChild:SetSize(200, 1)
    scrollFrame:SetScrollChild(scrollChild)
    
    frame.scrollFrame = scrollFrame
    frame.scrollChild = scrollChild
    
    -- Stats Display
    local stats = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    stats:SetPoint("BOTTOMLEFT", frame, "BOTTOMLEFT", 5, 5)
    stats:SetText("|cff00ff00139 Ready|r | 143 Total")
    frame.stats = stats
    
    self.frame = frame
    self.buttons = {}
    self:Refresh()
    
    return frame
end

function Browser:Refresh()
    -- Clear existing buttons
    for _, btn in ipairs(self.buttons) do
        btn:Hide()
        btn:SetParent(nil)
    end
    self.buttons = {}
    
    if not PetWeaverDB then return end
    
    -- Group encounters by expansion (simplified categorization)
    local groups = {
        ["The War Within"] = {},
        ["Dragonflight"] = {},
        ["Shadowlands"] = {},
        ["Battle for Azeroth"] = {},
        ["Legion"] = {},
        ["Warlords of Draenor"] = {},
        ["Mists of Pandaria"] = {},
        ["Other"] = {}
    }
    
    -- Categorize encounters (this is simplified - ideally from data)
    for encounterName, data in pairs(PetWeaverDB) do
        -- Simple categorization based on name patterns
        -- In production, this would come from the scraped data
        local category = "Other"
        
        if encounterName:match("War Within") or encounterName:match("Undermine") then
            category = "The War Within"
        elseif encounterName:match("Dragon") or encounterName:match("Forbidden") then
            category = "Dragonflight"
        elseif encounterName:match("Shadow") or encounterName:match("Maldraxxus") then
            category = "Shadowlands"
        elseif encounterName:match("Pandaria") or encounterName:match("Timeless") then
            category = "Mists of Pandaria"
        end
        
        table.insert(groups[category], encounterName)
    end
    
    local yOffset = 0
    local readyCount = 0
    local totalCount = 0
    
    -- Display each expansion group
    for _, expName in ipairs({"The War Within", "Dragonflight", "Shadowlands", "Battle for Azeroth", "Legion", "Warlords of Draenor", "Mists of Pandaria", "Other"}) do
        local encounters = groups[expName]
        
        if #encounters > 0 then
            -- Create expansion header
            local header = self:CreateHeader(expName, yOffset)
            table.insert(self.buttons, header)
            yOffset = yOffset - 25
            
            -- Sort encounters alphabetically
            table.sort(encounters)
            
            -- Create encounter buttons
            for _, encounterName in ipairs(encounters) do
                -- Apply filter
                local shouldShow = true
                local data = PetWeaverDB[encounterName]
                
                if self.currentFilter and self.currentFilter ~= "all" then
                    if self.currentFilter == "ready" and data then
                        local analysis = UI.analyzer:AnalyzeTeam(data.pet1, data.pet2, data.pet3)
                        shouldShow = analysis.ready and analysis.avgLevel >= 24
                    elseif self.currentFilter == "missing" and data then
                        local analysis = UI.analyzer:AnalyzeTeam(data.pet1, data.pet2, data.pet3)
                        shouldShow = not analysis.ready
                    elseif self.currentFilter == "favorites" then
                        shouldShow = UI.progressTracker and UI.progressTracker:IsFavorite(encounterName)
                    elseif self.currentFilter == "completed" then
                        shouldShow = UI.progressTracker and UI.progressTracker:IsCompleted(encounterName)
                    elseif self.currentFilter then
                        -- Expansion filter
                        shouldShow = encounterName:match(self.currentFilter)
                    end
                end
                
                if shouldShow then
                    local btn = self:CreateEncounterButton(encounterName, yOffset)
                    table.insert(self.buttons, btn)
                    
                    -- Count ready encounters
                    if data then
                        local analysis = UI.analyzer:AnalyzeTeam(data.pet1, data.pet2, data.pet3)
                        if analysis.ready and analysis.avgLevel >= 24 then
                            readyCount = readyCount + 1
                        end
                        totalCount = totalCount + 1
                    end
                    
                    yOffset = yOffset - 22
                end
            end
        end
    end
    
    -- Update stats
    self.frame.stats:SetText(string.format("|cff00ff00%d Ready|r | %d Total", readyCount, totalCount))
    
    self.frame.scrollChild:SetHeight(math.abs(yOffset))
end

function Browser:CreateHeader(text, yOffset)
    local header = CreateFrame("Button", nil, self.frame.scrollChild)
    header:SetSize(200, 20)
    header:SetPoint("TOPLEFT", 5, yOffset)
    
    local label = header:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    label:SetPoint("LEFT", 5, 0)
    label:SetText("|cffffd700📂 " .. text .. "|r")
    
    return header
end

function Browser:CreateEncounterButton(name, yOffset)
    local btn = CreateFrame("Button", nil, self.frame.scrollChild)
    btn:SetSize(200, 20)
    btn:SetPoint("TOPLEFT", 15, yOffset)
    btn:SetNormalFontObject("GameFontHighlight")
    btn:SetHighlightFontObject("GameFontNormal")
    
    -- Selection checkbox
    local checkbox = CreateFrame("CheckButton", nil, btn, "UICheckButtonTemplate")
    checkbox:SetSize(18, 18)
    checkbox:SetPoint("LEFT", -18, 0)
    checkbox:SetScript("OnClick", function(self)
        if self:GetChecked() then
            Browser.selectedEncounters[name] = true
        else
            Browser.selectedEncounters[name] = nil
        end
    end)
    btn.checkbox = checkbox
    
    -- Favorite star (clickable)
    local favBtn = CreateFrame("Button", nil, btn)
    favBtn:SetSize(16, 16)
    favBtn:SetPoint("RIGHT", -25, 0)
    local isFav = UI.progressTracker and UI.progressTracker:IsFavorite(name)
    favBtn:SetText(isFav and "⭐" or "☆")
    favBtn:SetNormalFontObject("GameFontNormal")
    favBtn:SetScript("OnClick", function(self)
        if UI.progressTracker then
            local nowFav = UI.progressTracker:ToggleFavorite(name)
            self:SetText(nowFav and "⭐" or "☆")
        end
    end)
    favBtn:SetScript("OnEnter", function(self)
        GameTooltip:SetOwner(self, "ANCHOR_RIGHT")
        GameTooltip:SetText(isFav and "Remove from Favorites" or "Add to Favorites")
        GameTooltip:Show()
    end)
    favBtn:SetScript("OnLeave", function() GameTooltip:Hide() end)
    btn.favBtn = favBtn
    
    -- Completion checkmark
    local completeIcon = btn:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    completeIcon:SetPoint("RIGHT", favBtn, "LEFT", -5, 0)
    if UI.progressTracker and UI.progressTracker:IsCompleted(name) then
        local count = UI.progressTracker:GetCompletionCount(name)
        completeIcon:SetText(count > 1 and string.format("|cff00ff00✓%d|r", count) or "|cff00ff00✓|r")
    else
        completeIcon:SetText("")
    end
    btn.completeIcon = completeIcon
    
    -- Get team data and analyze
    local data = PetWeaverDB[name]
    if data then
        local analysis = UI.analyzer:AnalyzeTeam(data.pet1, data.pet2, data.pet3)
        local statusIcon = UI.analyzer:GetStatusIcon(analysis)
        
        -- Filter if needed
        if UI.settings.showOnlyReady and not analysis.ready then
            btn:Hide()
            return btn
        end
        
        btn:SetText(statusIcon .. " " .. name)
        
        -- Tooltip
        btn:SetScript("OnEnter", function(self)
            GameTooltip:SetOwner(self, "ANCHOR_RIGHT")
            GameTooltip:SetText(name, 1, 1, 1)
            
            -- Show team pets
            GameTooltip:AddLine(" ")
            GameTooltip:AddLine("Team:", 0.5, 1, 0.5)
            
            local petIDs = {data.pet1, data.pet2, data.pet3}
            for i, petID in ipairs(petIDs) do
                if petID and petID ~= 0 then
                    local speciesName = C_PetJournal.GetPetInfoBySpeciesID(petID)
                    local owned = UI.analyzer:CheckPetOwnership(petID)
                    local color = owned and "|cff00ff00" or "|cffff0000"
                    GameTooltip:AddLine(color .. (speciesName or "Unknown") .. "|r", 1, 1, 1)
                end
            end
            
            -- Show completion count if any
            if UI.progressTracker and UI.progressTracker:IsCompleted(name) then
                local count = UI.progressTracker:GetCompletionCount(name)
                GameTooltip:AddLine(" ")
                GameTooltip:AddLine(string.format("Completed %d time(s)", count), 0.5, 1, 0.5)
            end
            
            GameTooltip:Show()
        end)
        
        btn:SetScript("OnLeave", function(self)
            GameTooltip:Hide()
        end)
    else
        btn:SetText("? " .. name)
    end
    
    btn:SetNormalTexture("Interface\\QuestFrame\\UI-QuestTitleHighlight")
    btn:GetNormalTexture():SetAlpha(0)
    btn:SetHighlightTexture("Interface\\QuestFrame\\UI-QuestTitleHighlight")
    
    btn:SetScript("OnClick", function()
        UI.detailsPanel:ShowEncounter(name)
    end)
    
    return btn
end

function Browser:SetFilter(filter)
    self.currentFilter = filter
    print("|cff00ff00PetWeaver:|r Filter: " .. filter)
    self:Refresh()
end

function Browser:GetSelectedEncounters()
    local selected = {}
    for encounterName, _ in pairs(self.selectedEncounters) do
        table.insert(selected, encounterName)
    end
    return selected
end

function Browser:ClearSelection()
    self.selectedEncounters = {}
    -- Uncheck all checkboxes
    for _, btn in ipairs(self.buttons) do
        if btn.checkbox then
            btn.checkbox:SetChecked(false)
        end
    end
end


function Browser:FilterEncounters(searchText)
    if searchText == "" then
        self:Refresh()
        return
    end
    
    -- Filter logic here
    -- For now, just refresh
    self:Refresh()
end
