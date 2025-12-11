local addonName, addon = ...
local UI = PetWeaverUI

-- Settings Panel
UI.settingsPanel = UI.settingsPanel or {}
local Settings = UI.settingsPanel

function Settings:Create(parent)
    local frame = CreateFrame("Frame", "PetWeaverSettingsFrame", UIParent, "BasicFrameTemplateWithInset")
    frame:SetSize(400, 350)
    frame:SetPoint("CENTER")
    frame:SetMovable(true)
    frame:EnableMouse(true)
    frame:RegisterForDrag("LeftButton")
    frame:SetScript("OnDragStart", frame.StartMoving)
    frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
    frame:SetClampedToScreen(true)
    frame:Hide()
    
    frame.title = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    frame.title:SetPoint("TOPLEFT", 15, -5)
    frame.title:SetText("PetWeaver Settings")
    
    local yOffset = -35
    
    -- Auto-Load Toggle
    local autoLoadLabel = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    autoLoadLabel:SetPoint("TOPLEFT", 20, yOffset)
    autoLoadLabel:SetText("Auto-Load Teams on Target:")
    
    local autoLoadCheck = CreateFrame("CheckButton", nil, frame, "UICheckButtonTemplate")
    autoLoadCheck:SetPoint("LEFT", autoLoadLabel, "RIGHT", 10, 0)
    autoLoadCheck:SetChecked(UI.settings.autoLoad)
    autoLoadCheck:SetScript("OnClick", function(self)
        UI.settings.autoLoad = self:GetChecked()
        addon.autoLoadEnabled = UI.settings.autoLoad
        print("|cff00ff00PetWeaver:|r Auto-load " .. (UI.settings.autoLoad and "enabled" or "disabled"))
    end)
    
    yOffset = yOffset - 35
    
    -- Map Markers Toggle
    local mapMarkersLabel = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    mapMarkersLabel:SetPoint("TOPLEFT", 20, yOffset)
    mapMarkersLabel:SetText("Auto Map Markers:")
    
    local mapMarkersCheck = CreateFrame("CheckButton", nil, frame, "UICheckButtonTemplate")
    mapMarkersCheck:SetPoint("LEFT", mapMarkersLabel, "RIGHT", 10, 0)
    mapMarkersCheck:SetChecked(UI.settings.mapMarkers)
    mapMarkersCheck:SetScript("OnClick", function(self)
        UI.settings.mapMarkers = self:GetChecked()
        print("|cff00ff00PetWeaver:|r Map markers " .. (UI.settings.mapMarkers and "enabled" or "disabled"))
    end)
    
    yOffset = yOffset - 35
    
    -- Notifications Toggle
    local notifLabel = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    notifLabel:SetPoint("TOPLEFT", 20, yOffset)
    notifLabel:SetText("Chat Notifications:")
    
    local notifCheck = CreateFrame("CheckButton", nil, frame, "UICheckButtonTemplate")
    notifCheck:SetPoint("LEFT", notifLabel, "RIGHT", 10, 0)
    notifCheck:SetChecked(UI.settings.notifications)
    notifCheck:SetScript("OnClick", function(self)
        UI.settings.notifications = self:GetChecked()
        print("|cff00ff00PetWeaver:|r Notifications " .. (UI.settings.notifications and "enabled" or "disabled"))
    end)
    
    yOffset = yOffset - 35
    
    -- Show Only Ready Filter
    local filterLabel = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    filterLabel:SetPoint("TOPLEFT", 20, yOffset)
    filterLabel:SetText("Show Only Ready Teams:")
    
    local filterCheck = CreateFrame("CheckButton", nil, frame, "UICheckButtonTemplate")
    filterCheck:SetPoint("LEFT", filterLabel, "RIGHT", 10, 0)
    filterCheck:SetChecked(UI.settings.showOnlyReady)
    filterCheck:SetScript("OnClick", function(self)
        UI.settings.showOnlyReady = self:GetChecked()
        if UI.browser and UI.browser.Refresh then
            UI.browser:Refresh()
        end
        print("|cff00ff00PetWeaver:|r Filter " .. (UI.settings.showOnlyReady and "enabled" or "disabled"))
    end)
    
    yOffset = yOffset - 50
    
    -- Info section
    local infoHeader = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    infoHeader:SetPoint("TOPLEFT", 20, yOffset)
    infoHeader:SetText("Commands:")
    
    yOffset = yOffset - 25
    
    local commands = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    commands:SetPoint("TOPLEFT", 20, yOffset)
    commands:SetWidth(360)
    commands:SetJustifyH("LEFT")
    commands:SetText(
        "/pw show - Open UI\n" ..
        "/pw toggle - Toggle auto-load\n" ..
        "/pw capture - Load capture team\n" ..
        "/pw [Encounter] - Load specific team"
    )
    
    -- Close button
    local closeBtn = CreateFrame("Button", nil, frame, "GameMenuButtonTemplate")
    closeBtn:SetSize(100, 30)
    closeBtn:SetPoint("BOTTOM", 0, 15)
    closeBtn:SetText("Close")
    closeBtn:SetNormalFontObject("GameFontNormal")
    closeBtn:SetScript("OnClick", function()
        frame:Hide()
    end)
    
    self.frame = frame
    return frame
end

function Settings:Show()
    if not self.frame then
        self:Create()
    end
    self.frame:Show()
end

function Settings:Hide()
    if self.frame then
        self.frame:Hide()
    end
end
