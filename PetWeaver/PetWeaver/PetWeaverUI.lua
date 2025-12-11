local addonName, addon = ...

-- UI State
PetWeaverUI = PetWeaverUI or {}
local UI = PetWeaverUI

UI.settings = {
    autoLoad = true,
    mapMarkers = true,
    notifications = true,
    uiScale = 1.0,
    showOnlyReady = false
}

-- Main Frame Creation
function UI:CreateMainFrame()
    if self.mainFrame then
        return self.mainFrame
    end
    
    local frame = CreateFrame("Frame", "PetWeaverMainFrame", UIParent, "BasicFrameTemplateWithInset")
    frame:SetSize(750, 550)
    frame:SetPoint("CENTER")
    frame:SetMovable(true)
    frame:EnableMouse(true)
    frame:RegisterForDrag("LeftButton")
    frame:SetScript("OnDragStart", frame.StartMoving)
    frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
    frame:SetClampedToScreen(true)
    frame:Hide()
    
    -- Title
    frame.title = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    frame.title:SetPoint("TOPLEFT", 15, -5)
    frame.title:SetText("PetWeaver")
    
    -- Settings Button
    frame.settingsBtn = CreateFrame("Button", nil, frame)
    frame.settingsBtn:SetSize(24, 24)
    frame.settingsBtn:SetPoint("TOPRIGHT", -35, -5)
    frame.settingsBtn:SetNormalTexture("Interface\\Icons\\Trade_Engineering")
    frame.settingsBtn:SetHighlightTexture("Interface\\Buttons\\UI-Common-MouseHilight")
    frame.settingsBtn:SetScript("OnClick", function()
        UI:ShowSettings()
    end)
    
    -- Queue Manager button
    local queueBtn = CreateFrame("Button", nil, frame)
    queueBtn:SetSize(24, 24)
    queueBtn:SetPoint("RIGHT", frame.settingsBtn, "LEFT", -5, 0) -- Adjusted point to place it to the left of settingsBtn
    queueBtn:SetNormalTexture("Interface\\Buttons\\UI-GuildButton-PublicNote-Up")
    queueBtn:SetPushedTexture("Interface\\Buttons\\UI-GuildButton-PublicNote-Down")
    queueBtn:SetHighlightTexture("Interface\\Buttons\\UI-Common-MouseHilight")
    queueBtn:SetScript("OnClick", function()
        self:ShowQueue()
    end)
    queueBtn:SetScript("OnEnter", function(self)
        GameTooltip:SetOwner(self, "ANCHOR_RIGHT")
        GameTooltip:SetText("Queue Manager", 1, 1, 1)
        GameTooltip:AddLine("Leveling & Gathering Queues", 1, 1, 1)
        GameTooltip:Show()
    end)
    queueBtn:SetScript("OnLeave", function() GameTooltip:Hide() end)
    
    -- Help Button
    frame.helpBtn = CreateFrame("Button", nil, frame)
    frame.helpBtn:SetSize(24, 24)
    frame.helpBtn:SetPoint("RIGHT", queueBtn, "LEFT", -5, 0) -- Adjusted point to place it to the left of queueBtn
    frame.helpBtn:SetNormalTexture("Interface\\Common\\help-i")
    frame.helpBtn:SetHighlightTexture("Interface\\Buttons\\UI-Common-MouseHilight")
    frame.helpBtn:SetScript("OnClick", function()
        print("|cff00ff00PetWeaver Help:|r Use the left panel to browse encounters. Click any encounter to view team details on the right.")
    end)
    
    self.mainFrame = frame
    return frame
end

function UI:Toggle()
    if not self.mainFrame then
        self:CreateMainFrame()
    end
    
    if self.mainFrame:IsShown() then
        self.mainFrame:Hide()
    else
        self.mainFrame:Show()
        if self.browser then
            self.browser:Refresh()
        end
    end
end

function UI:Show()
    if not self.mainFrame then
        self:CreateMainFrame()
    end
    self.mainFrame:Show()
    if self.browser then
        self.browser:Refresh()
    end
end

function UI:Hide()
    if self.mainFrame then
        self.mainFrame:Hide()
    end
end

function UI:ShowQueue()
    if self.queuePanel and self.queuePanel.Toggle then
        self.queuePanel:Toggle()
    else
        print("|cff00ff00PetWeaver:|r Queue panel not loaded yet")
    end
end

function UI:ShowSettings()
    if self.settingsPanel and self.settingsPanel.Show then
        self.settingsPanel:Show()
    else
        print("|cff00ff00PetWeaver Settings:|r Settings panel not loaded yet")
    end
end


-- Initialize
local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:SetScript("OnEvent", function(self, event, loadedAddon)
    if loadedAddon == addonName then
        -- Initialize main frame
        PetWeaverUI:CreateMainFrame()
        
        -- Create browser and details panels
        if PetWeaverUI.browser.Create then
            PetWeaverUI.browser:Create(PetWeaverUI.mainFrame)
        end
        
        if PetWeaverUI.detailsPanel.Create then
            PetWeaverUI.detailsPanel:Create(PetWeaverUI.mainFrame)
        end
        
        -- Initialize settings panel
        if PetWeaverUI.settingsPanel.Create then
            PetWeaverUI.settingsPanel:Create()
        end
        
        -- Initialize queue panel
        if PetWeaverUI.queuePanel.Create then
            PetWeaverUI.queuePanel:Create()
        end
        
        -- Create minimap button
        if PetWeaverUI.minimapButton.Create then
            PetWeaverUI.minimapButton:Create()
            PetWeaverUI.minimapButton:Show()
        end
        
        print("|cff00ff00PetWeaver UI:|r Loaded successfully!")
        print("|cff00ff00Commands:|r /pw show | /pw capture | /pw toggle")
        print("|cff00ff00Tip:|r Click minimap button to open UI, check encounters for queue")
    end
end)



