local addonName, addon = ...
local UI = PetWeaverUI

-- Details Panel
UI.detailsPanel = UI.detailsPanel or {}
local Details = UI.detailsPanel

function Details:Create(parent)
    local frame = CreateFrame("Frame", nil, parent)
    frame:SetPoint("TOPLEFT", parent, "TOPLEFT", 260, -35)
    frame:SetPoint("BOTTOMRIGHT", parent, "BOTTOMRIGHT", -10, 10)
    
    -- Encounter Name
    local name = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    name:SetPoint("TOPLEFT", 10, -10)
    name:SetText("Select an Encounter")
    frame.encounterName = name
    
    -- Status Badge
    local status = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    status:SetPoint("LEFT", name, "RIGHT", 10, 0)
    status:SetText("")
    frame.statusBadge = status
    
    -- Metadata (expansion, zone, etc.)
    local metadata = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    metadata:SetPoint("TOPLEFT", name, "BOTTOMLEFT", 0, -3)
    metadata:SetText("")
    metadata:SetTextColor(0.7, 0.7, 0.7)
    frame.metadata = metadata
    
    -- Description
    local desc = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    desc:SetPoint("TOPLEFT", metadata, "BOTTOMLEFT", 0, -5)
    desc:SetWidth(450)
    desc:SetJustifyH("LEFT")
    desc:SetText("")
    frame.description = desc
    
    -- Strategy Selector (if multiple strategies available)
    local stratSelector = CreateFrame("Frame", nil, frame)
    stratSelector:SetSize(450, 25)
    stratSelector:SetPoint("TOPLEFT", desc, "BOTTOMLEFT", 0, -5)
    stratSelector:Hide() -- Hidden by default
    
    local stratLabel = stratSelector:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    stratLabel:SetPoint("LEFT", 0, 0)
    stratLabel:SetText("|cff00ffffStrategy:|r")
    
    local prevBtn = CreateFrame("Button", nil, stratSelector, "GameMenuButtonTemplate")
    prevBtn:SetSize(25, 22)
    prevBtn:SetPoint("LEFT", stratLabel, "RIGHT", 5, 0)
    prevBtn:SetText("<")
    prevBtn:SetNormalFontObject("GameFontNormal")
    stratSelector.prevBtn = prevBtn
    
    local stratName = stratSelector:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    stratName:SetPoint("LEFT", prevBtn, "RIGHT", 5, 0)
    stratName:SetText("Default Strategy (1/1)")
    stratSelector.name = stratName
    
    local nextBtn = CreateFrame("Button", nil, stratSelector, "GameMenuButtonTemplate")
    nextBtn:SetSize(25, 22)
    nextBtn:SetPoint("LEFT", stratName, "RIGHT", 5, 0)
    nextBtn:SetText(">")
    nextBtn:SetNormalFontObject("GameFontNormal")
    stratSelector.nextBtn = nextBtn
    
    local stratTags = stratSelector:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    stratTags:SetPoint("LEFT", nextBtn, "RIGHT", 10, 0)
    stratTags:SetText("")
    stratTags:SetTextColor(0.4, 1, 0.4)
    stratSelector.tags = stratTags
    
    frame.stratSelector = stratSelector
    
    -- Team Header
    local teamHeader = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    teamHeader:SetPoint("TOPLEFT", desc, "BOTTOMLEFT", 0, -20)
    teamHeader:SetText("|cff00ffff🐾 Team:|r")
    
    -- Pet Slots (3)
    frame.petSlots = {}
    for i = 1, 3 do
        frame.petSlots[i] = self:CreatePetSlot(frame, i)
        if i == 1 then
            frame.petSlots[i]:SetPoint("TOPLEFT", teamHeader, "BOTTOMLEFT", 0, -10)
        else
            frame.petSlots[i]:SetPoint("TOP", frame.petSlots[i-1], "BOTTOM", 0, -5)
        end
    end
    
    -- Script Display
    local scriptHeader = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    scriptHeader:SetPoint("TOPLEFT", frame.petSlots[3], "BOTTOMLEFT", 0, -20)
    scriptHeader:SetText("|cff00ffff📜 Battle Script:|r")
    
    local scriptScroll = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
    scriptScroll:SetPoint("TOPLEFT", scriptHeader, "BOTTOMLEFT", 0, -5)
    scriptScroll:SetPoint("BOTTOMRIGHT", frame, "BOTTOMRIGHT", -25, 45)
    scriptScroll:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        tile = true, tileSize = 16, edgeSize = 12,
        insets = { left = 3, right = 3, top = 3, bottom = 3 }
    })
    
    local scriptText = CreateFrame("Frame", nil, scriptScroll)
    scriptText:SetSize(440, 1)
    scriptScroll:SetScrollChild(scriptText)
    
    scriptText.text = scriptText:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    scriptText.text:SetPoint("TOPLEFT", 5, -5)
    scriptText.text:SetWidth(420)
    scriptText.text:SetJustifyH("LEFT")
    scriptText.text:SetText("")
    
    frame.scriptText = scriptText.text
    frame.scriptScroll = scriptScroll
    
    -- Buttons
    local loadBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    loadBtn:SetSize(120, 30)
    loadBtn:SetPoint("BOTTOMLEFT", frame, "BOTTOMLEFT", 10, 5)
    loadBtn:SetText("Load Team")
    loadBtn:SetNormalFontObject("GameFontNormal")
    loadBtn:SetScript("OnClick", function()
        if self.currentEncounter then
            addon:LoadTeam(self.currentEncounter)
        end
    end)
    frame.loadBtn = loadBtn
    
    local copyBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    copyBtn:SetSize(100, 30)
    copyBtn:SetPoint("LEFT", loadBtn, "RIGHT", 10, 0)
    copyBtn:SetText("Copy Script")
    copyBtn:SetNormalFontObject("GameFontNormal")
    copyBtn:SetScript("OnClick", function()
        if self.currentScript then
            -- Will need a copy-to-clipboard solution
            print("|cff00ff00PetWeaver:|r Script copied to chat (use /copy)")
            print(self.currentScript)
        end
    end)
    frame.copyBtn = copyBtn
    
    local exportBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    exportBtn:SetSize(120, 30)
    exportBtn:SetPoint("LEFT", copyBtn, "RIGHT", 10, 0)
    exportBtn:SetText("Export Missing")
    exportBtn:SetNormalFontObject("GameFontNormal")
    exportBtn:SetScript("OnClick", function()
        if self.currentEncounter then
            local data = PetWeaverDB[self.currentEncounter]
            if data then
                local analysis = UI.analyzer:AnalyzeTeam(data.pet1, data.pet2, data.pet3)
                if #analysis.missingPets > 0 and UI.mapHelper then
                    UI.mapHelper:ExportMissingPetsList(analysis.missingPets)
                else
                    print("|cff00ff00PetWeaver:|r No missing pets for this encounter!")
                end
            end
        end
    end)
    frame.exportBtn = exportBtn
    
    -- Mark Complete Button
    local completeBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    completeBtn:SetSize(100, 30)
    completeBtn:SetPoint("BOTTOMRIGHT", frame, "BOTTOMRIGHT", -10, 5)
    completeBtn:SetText("✓ Complete")
    completeBtn:SetNormalFontObject("GameFontNormal")
    completeBtn:SetScript("OnClick", function()
        if self.currentEncounter and UI.progressTracker then
            UI.progressTracker:MarkCompleted(self.currentEncounter)
            -- Refresh browser to show checkmark
            if UI.browser then UI.browser:Refresh() end
            self:ShowEncounter(self.currentEncounter) -- Refresh details
        end
    end)
    frame.completeBtn = completeBtn
    
    -- Show Substitutions Button
    local subsBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    subsBtn:SetSize(100, 30)
    subsBtn:SetPoint("RIGHT", completeBtn, "LEFT", -10, 0)
    subsBtn:SetText("Alternatives")
    subsBtn:SetNormalFontObject("GameFontNormal")
    subsBtn:SetScript("OnClick", function()
        if self.currentEncounter and UI.petSubstitution then
            local data = PetWeaverDB[self.currentEncounter]
            if data then
                local suggestions = UI.petSubstitution:SuggestTeam(data.pet1, data.pet2, data.pet3)
                UI.petSubstitution:ShowSuggestions(self.currentEncounter, suggestions)
            end
        end
    end)
    frame.subsBtn = subsBtn
    
    -- Validate Team Button
    local validateBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    validateBtn:SetSize(90, 30)
    validateBtn:SetPoint("RIGHT", subsBtn, "LEFT", -10, 0)
    validateBtn:SetText("Validate")
    validateBtn:SetNormalFontObject("GameFontNormal")
    validateBtn:SetScript("OnClick", function()
        if self.currentEncounter and UI.teamValidator then
            local data = PetWeaverDB[self.currentEncounter]
            if data then
                local validation = UI.teamValidator:ValidateTeam(data.pet1, data.pet2, data.pet3)
                UI.teamValidator:ShowValidation(validation, self.currentEncounter)
            end
        end
    end)
    frame.validateBtn = validateBtn
    
    self.frame = frame
    return frame
end

function Details:CreatePetSlot(parent, slotNum)
    local slot = CreateFrame("Frame", nil, parent)
    slot:SetSize(450, 40)
    
    -- Icon
    local icon = slot:CreateTexture(nil, "ARTWORK")
    icon:SetSize(36, 36)
    icon:SetPoint("LEFT", 5, 0)
    icon:SetTexture("Interface\\Icons\\INV_Pet_BabyBlizzardBear") -- Default
    slot.icon = icon
    
    -- Icon border
    local iconBorder = slot:CreateTexture(nil, "OVERLAY")
    iconBorder:SetSize(40, 40)
    iconBorder:SetPoint("CENTER", icon, "CENTER")
    iconBorder:SetTexture("Interface\\PetBattles\\PetBattle-LevelRing")
    slot.iconBorder = iconBorder
    
    -- Name
    local name = slot:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    name:SetPoint("LEFT", icon, "RIGHT", 10, 8)
    name:SetText("Pet Name")
    slot.name = name
    
    -- Level/Quality
    local info = slot:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    info:SetPoint("LEFT", icon, "RIGHT", 10, -8)
    info:SetText("[25] (Rare, H/H)")
    slot.info = info
    
    -- Status Icon
    local status = slot:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    status:SetPoint("RIGHT", -5, 0)
    status:SetText("|cff00ff00✓|r")
    slot.status = status
    
    -- Action Button (Find on Map)
    local mapBtn = CreateFrame("Button", nil, slot, "GameMenuButtonTemplate")
    mapBtn:SetSize(90, 20)
    mapBtn:SetPoint("RIGHT", status, "LEFT", -10, 0)
    mapBtn:SetText("Find on Map")
    mapBtn:SetNormalFontObject("GameFontNormalSmall")
    mapBtn:Hide() -- Hidden by default
    slot.mapBtn = mapBtn
    
    return slot
end


function Details:ShowEncounter(encounterName)
    self.currentEncounter = encounterName
    
    -- Get current strategy (supports multiple strategies)
    local strategy = UI.strategyManager and UI.strategyManager:GetCurrentStrategy(encounterName)
    if not strategy then
        -- Fallback to old format
        local data = PetWeaverDB[encounterName]
        if not data then return end
        strategy = {
            name = "Default Strategy",
            pet1 = data.pet1,
            pet2 = data.pet2,
            pet3 = data.pet3,
            script = data.script,
            tags = {}
        }
    end
    
    self.currentScript = strategy.script
    
    -- Analyze team
    local analysis = UI.analyzer:AnalyzeTeam(strategy.pet1, strategy.pet2, strategy.pet3)
    local statusIcon, statusText = UI.analyzer:GetStatusIcon(analysis)
    
    -- Set encounter name and status
    self.frame.encounterName:SetText(encounterName)
    self.frame.statusBadge:SetText(statusText)
    
    -- Set metadata (expansion, zone, category, difficulty)
    if UI.strategyManager then
        local meta = UI.strategyManager:GetEncounterMetadata(encounterName)
        self.frame.metadata:SetText(string.format("%s | %s | %s | %s", 
            meta.expansion or "Unknown",
            meta.zone or "Unknown", 
            meta.category or "Unknown",
            meta.difficulty or "Unknown"
        ))
    else
        self.frame.metadata:SetText("")
    end
    
    -- Set description
    self.frame.description:SetText("Battle strategy from Xu-Fu's Pet Guide")
    
    -- Strategy selector
    if UI.strategyManager then
        local strategies = UI.strategyManager:GetStrategies(encounterName)
        if #strategies > 1 then
            self.frame.stratSelector:Show()
            local currentIndex = UI.strategyManager.selectedStrategies[encounterName] or 1
            self.frame.stratSelector.name:SetText(string.format("%s (%d/%d)", 
                strategy.name, currentIndex, #strategies))
            
            -- Strategy tags
            if strategy.tags and #strategy.tags > 0 then
                self.frame.stratSelector.tags:SetText("[" .. table.concat(strategy.tags, ", ") .. "]")
            else
                self.frame.stratSelector.tags:SetText("")
            end
            
            -- Wire up buttons
            self.frame.stratSelector.prevBtn:SetScript("OnClick", function()
                UI.strategyManager:PreviousStrategy(encounterName)
                self:ShowEncounter(encounterName) -- Refresh
            end)
            
            self.frame.stratSelector.nextBtn:SetScript("OnClick", function()
                UI.strategyManager:NextStrategy(encounterName)
                self:ShowEncounter(encounterName) -- Refresh
            end)
        else
            self.frame.stratSelector:Hide()
        end
    else
        self.frame.stratSelector:Hide()
    end
    
    -- Set pets with smart analysis
    local petIDs = {strategy.pet1, strategy.pet2, strategy.pet3}
    for i, petID in ipairs(petIDs) do
        if petID and petID ~= 0 then
            local speciesName, icon = C_PetJournal.GetPetInfoBySpeciesID(petID)
            local owned, petInfo = UI.analyzer:CheckPetOwnership(petID)
            
            -- Set pet icon
            if icon then
                self.frame.petSlots[i].icon:SetTexture(icon)
            end
            
            if owned and petInfo then
                -- Owned pet - show details
                local qualityText = UI.analyzer:GetQualityText(petInfo.quality)
                local breedText = UI.analyzer:GetBreedText(petInfo.guid)
                
                self.frame.petSlots[i].name:SetText(speciesName or "Unknown Pet")
                self.frame.petSlots[i].info:SetText(
                    string.format("[%d] %s (%s)", petInfo.level, qualityText, breedText)
                )
                
                if petInfo.level < 25 then
                    self.frame.petSlots[i].status:SetText("|cfffff000⚠|r")
                else
                    self.frame.petSlots[i].status:SetText("|cff00ff00✓|r")
                end
                
                -- Hide map button for owned pets
                self.frame.petSlots[i].mapBtn:Hide()
            else
                -- Missing pet - show how to get it
                local source = UI.analyzer:GetPetSource(petID)
                
                self.frame.petSlots[i].name:SetText((speciesName or "Unknown") .. " |cffff0000(Missing)|r")
                
                if source.type == "wild" then
                    self.frame.petSlots[i].info:SetText(
                        string.format("📍 %s - %s", source.zone, source.coords)
                    )
                elseif source.type == "vendor" then
                    self.frame.petSlots[i].info:SetText(
                        string.format("💰 Vendor: %s", source.notes)
                    )
                else
                    self.frame.petSlots[i].info:SetText(source.notes)
                end
                
                self.frame.petSlots[i].status:SetText("|cffff0000✗|r")
                
                -- Show map button and connect it
                if UI.settings.mapMarkers and UI.mapHelper then
                    self.frame.petSlots[i].mapBtn:Show()
                    self.frame.petSlots[i].mapBtn:SetScript("OnClick", function()
                        UI.mapHelper:AddWaypoint(petID, speciesName)
                    end)
                else
                    self.frame.petSlots[i].mapBtn:Hide()
                end
            end
        end
    end
    
    -- Set script
    if strategy.script then
        local formatted = strategy.script:gsub("\r\n", "\n"):gsub("\r", "\n")
        self.frame.scriptText:SetText(formatted)
    end
    
    -- Export missing pets if any
    if #analysis.missingPets > 0 and UI.mapHelper then
        -- Could auto-export here if desired
    end
end

