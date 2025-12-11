-- Settings.lua
-- Settings panel for DeepPockets

local _, addon = ...
addon.Settings = {}
local Settings = addon.Settings

-- Create settings panel
function Settings:CreatePanel()
    if Settings.panel then return Settings.panel end
    
    local panel = CreateFrame("Frame", "DeepPocketsSettingsPanel", UIParent, "BackdropTemplate")
    panel:SetSize(400, 450)
    panel:SetPoint("CENTER")
    panel:SetBackdrop({
        bgFile = "Interface\\ChatFrame\\ChatFrameBackground",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        tile = true, tileSize = 16, edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    panel:SetBackdropColor(0, 0, 0, 0.9)
    panel:SetBackdropBorderColor(0.6, 0.6, 0.6, 1)
    panel:SetFrameStrata("DIALOG")
    panel:EnableMouse(true)
    panel:SetMovable(true)
    panel:RegisterForDrag("LeftButton")
    panel:SetScript("OnDragStart", function(self) self:StartMoving() end)
    panel:SetScript("OnDragStop", function(self) self:StopMovingOrSizing() end)
    panel:Hide()
    
    -- Title
    local title = panel:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOP", 0, -15)
    title:SetText("DeepPockets Settings")
    
    -- Close Button
    local closeBtn = CreateFrame("Button", nil, panel, "UIPanelCloseButton")
    closeBtn:SetPoint("TOPRIGHT", -5, -5)
    
    -- UI Scale Slider
    local scaleSlider = CreateFrame("Slider", "DeepPocketsScaleSlider", panel, "OptionsSliderTemplate")
    scaleSlider:SetPoint("TOPLEFT", 20, -60)
    scaleSlider:SetMinMaxValues(0.5, 2.0)
    scaleSlider:SetValue(DeepPocketsDB.settings.uiScale or 1.0)
    scaleSlider:SetValueStep(0.1)
    scaleSlider:SetObeyStepOnDrag(true)
    _G[scaleSlider:GetName().."Low"]:SetText("50%")
    _G[scaleSlider:GetName().."High"]:SetText("200%")
    _G[scaleSlider:GetName().."Text"]:SetText("UI Scale")
    
    scaleSlider:SetScript("OnValueChanged", function(self, value)
        DeepPocketsDB.settings.uiScale = value
        if addon.Frame then
            addon.Frame:SetScale(value)
        end
        _G[self:GetName().."Text"]:SetText(string.format("UI Scale: %.1f", value))
    end)
    
    -- Columns Slider
    local colsSlider = CreateFrame("Slider", "DeepPocketsColumnsSlider", panel, "OptionsSliderTemplate")
    colsSlider:SetPoint("TOPLEFT", 20, -120)
    colsSlider:SetMinMaxValues(5, 15)
    colsSlider:SetValue(DeepPocketsDB.settings.columns or 10)
    colsSlider:SetValueStep(1)
    colsSlider:SetObeyStepOnDrag(true)
    _G[colsSlider:GetName().."Low"]:SetText("5")
    _G[colsSlider:GetName().."High"]:SetText("15")
    _G[colsSlider:GetName().."Text"]:SetText("Columns")
    
    colsSlider:SetScript("OnValueChanged", function(self, value)
        DeepPocketsDB.settings.columns = value
        if addon.Frame and addon.Frame:IsShown() then
            addon:RenderGrid()
        end
        _G[self:GetName().."Text"]:SetText(string.format("Columns: %d", value))
    end)
    
    -- Show Category Headers Checkbox
    local categoryCheck = CreateFrame("CheckButton", "DeepPocketsCategoryCheck", panel, "UICheckButtonTemplate")
    categoryCheck:SetPoint("TOPLEFT", 20, -180)
    categoryCheck:SetSize(24, 24)
    _G[categoryCheck:GetName().."Text"]:SetText("Show Category Headers")
    categoryCheck:SetChecked(DeepPocketsDB.settings.showCategories ~= false)
    categoryCheck:SetScript("OnClick", function(self)
        DeepPocketsDB.settings.showCategories = self:GetChecked()
        if addon.Frame and addon.Frame:IsShown() then
            addon:RenderGrid()
        end
    end)
    
    -- Replace Default Bags Checkbox
    local replaceBagsCheck = CreateFrame("CheckButton", "DeepPocketsReplaceBagsCheck", panel, "UICheckButtonTemplate")
    replaceBagsCheck:SetPoint("TOPLEFT", 20, -210)
    replaceBagsCheck:SetSize(24, 24)
    _G[replaceBagsCheck:GetName().."Text"]:SetText("Replace Default Bags (B key)")
    replaceBagsCheck:SetChecked(DeepPocketsDB.settings.replaceBags ~= false)
    replaceBagsCheck:SetScript("OnClick", function(self)
        DeepPocketsDB.settings.replaceBags = self:GetChecked()
        print("|cff00ff00DeepPockets:|r Bag replacement " .. (self:GetChecked() and "enabled" or "disabled"))
    end)
    
    -- Show Item Count Checkbox
    local itemCountCheck = CreateFrame("CheckButton", "DeepPocketsItemCountCheck", panel, "UICheckButtonTemplate")
    itemCountCheck:SetPoint("TOPLEFT", 20, -240)
    itemCountCheck:SetSize(24, 24)
    _G[itemCountCheck:GetName().."Text"]:SetText("Show Item Counts")
    itemCountCheck:SetChecked(DeepPocketsDB.settings.showItemCount ~= false)
    itemCountCheck:SetScript("OnClick", function(self)
        DeepPocketsDB.settings.showItemCount = self:GetChecked()
        if addon.Frame and addon.Frame:IsShown() then
            addon:RenderGrid()
        end
    end)
    
    -- Auto-Sort Checkbox
    local autoSortCheck = CreateFrame("CheckButton", "DeepPocketsAutoSortCheck", panel, "UICheckButtonTemplate")
    autoSortCheck:SetPoint("TOPLEFT", 20, -270)
    autoSortCheck:SetSize(24, 24)
    _G[autoSortCheck:GetName().."Text"]:SetText("Auto-Sort Items")
    autoSortCheck:SetChecked(DeepPocketsDB.settings.autoSort or false)
    autoSortCheck:SetScript("OnClick", function(self)
        DeepPocketsDB.settings.autoSort = self:GetChecked()
    end)
    
    -- Reset Position Button
    local resetPosBtn = CreateFrame("Button", nil, panel, "UIPanelButtonTemplate")
    resetPosBtn:SetSize(150, 25)
    resetPosBtn:SetPoint("BOTTOM", panel, "BOTTOM", 0, 60)
    resetPosBtn:SetText("Reset Position")
    resetPosBtn:SetScript("OnClick", function()
        if addon.Frame then
            addon.Frame:ClearAllPoints()
            addon.Frame:SetPoint("BOTTOMRIGHT", UIParent, "BOTTOMRIGHT", -50, 50)
            print("|cff00ff00DeepPockets:|r Position reset")
        end
    end)
    
    -- Reset Defaults Button
    local resetBtn = CreateFrame("Button", nil, panel, "UIPanelButtonTemplate")
    resetBtn:SetSize(150, 25)
    resetBtn:SetPoint("BOTTOM", panel, "BOTTOM", 0, 20)
    resetBtn:SetText("Reset to Defaults")
    resetBtn:SetScript("OnClick", function()
        DeepPocketsDB.settings = {
            uiScale = 1.0,
            columns = 10,
            showCategories = true,
            replaceBags = true,
            showItemCount = true,
            autoSort = false
        }
        scaleSlider:SetValue(1.0)
        colsSlider:SetValue(10)
        categoryCheck:SetChecked(true)
        replaceBagsCheck:SetChecked(true)
        itemCountCheck:SetChecked(true)
        autoSortCheck:SetChecked(false)
        
        if addon.Frame then
            addon.Frame:SetScale(1.0)
            addon:RenderGrid()
        end
        
        print("|cff00ff00DeepPockets:|r Settings reset to defaults")
    end)
    
    Settings.panel = panel
    return panel
end

-- Toggle settings panel
function Settings:Toggle()
    local panel = Settings:CreatePanel()
    if panel:IsShown() then
        panel:Hide()
    else
        panel:Show()
    end
end

-- Add settings button to main frame
function Settings:AddButtonToFrame(mainFrame)
    if mainFrame.settingsBtn then return end
    
    local btn = CreateFrame("Button", nil, mainFrame, "UIPanelButtonTemplate")
    btn:SetSize(70, 22)
    btn:SetPoint("TOPRIGHT", mainFrame, "TOPRIGHT", -30, -8)
    btn:SetText("Settings")
    btn:SetScript("OnClick", function()
        Settings:Toggle()
    end)
    
    mainFrame.settingsBtn = btn
end
