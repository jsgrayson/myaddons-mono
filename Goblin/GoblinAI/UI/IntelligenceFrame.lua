-- UI/IntelligenceFrame.lua - Display AI insights and market intelligence

GoblinAI.IntelligenceFrame = {}
local IntelFrame = GoblinAI.IntelligenceFrame

function IntelFrame:Initialize()
    self:CreateUI()
end

function IntelFrame:CreateUI()
    -- Main Frame (Modern)
    self.frame = CreateFrame("Frame", "GoblinAIIntelligenceFrame", UIParent, "BackdropTemplate")
    self.frame:SetSize(700, 500)
    self.frame:SetPoint("CENTER")
    self.frame:SetMovable(true)
    self.frame:EnableMouse(true)
    self.frame:RegisterForDrag("LeftButton")
    self.frame:SetScript("OnDragStart", self.frame.StartMoving)
    self.frame:SetScript("OnDragStop", self.frame.StopMovingOrSizing)
    self.frame:Hide()
    
    -- Backdrop
    self.frame:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8x8",
        edgeFile = "Interface\\Buttons\\WHITE8x8",
        tile = false, tileSize = 0, edgeSize = 1,
        insets = { left = 0, right = 0, top = 0, bottom = 0 }
    })
    self.frame:SetBackdropColor(0.1, 0.1, 0.1, 0.95)
    self.frame:SetBackdropBorderColor(0, 0, 0, 1)

    -- Header
    self.frame.header = self.frame:CreateTexture(nil, "BACKGROUND")
    self.frame.header:SetColorTexture(0.15, 0.15, 0.15, 1)
    self.frame.header:SetPoint("TOPLEFT", 1, -1)
    self.frame.header:SetPoint("TOPRIGHT", -1, -1)
    self.frame.header:SetHeight(30)

    -- Title
    self.frame.title = self.frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    self.frame.title:SetPoint("LEFT", self.frame.header, "LEFT", 10, 0)
    self.frame.title:SetText("Goblin AI - Market Intelligence")
    self.frame.title:SetTextColor(1, 0.8, 0) -- Gold color

    -- Close Button
    local close = CreateFrame("Button", nil, self.frame, "UIPanelCloseButton")
    close:SetPoint("TOPRIGHT", 2, 2)

    -- Tabs
    self.tabs = {}
    self:CreateTab(1, "Market Overview", self.ShowOverview)
    self:CreateTab(2, "Cross-Realm", self.ShowCrossRealm)
    self:CreateTab(3, "Predictions", self.ShowPredictions)

    -- Content Area
    self.content = CreateFrame("Frame", nil, self.frame)
    self.content:SetPoint("TOPLEFT", 10, -60)
    self.content:SetPoint("BOTTOMRIGHT", -10, 10)
    
    -- Default to Overview
    self:ShowOverview()
end

function IntelFrame:CreateTab(id, text, onClick)
    local tab = CreateFrame("Button", nil, self.frame, "BackdropTemplate")
    tab:SetSize(120, 25)
    tab:SetPoint("TOPLEFT", 15 + ((id-1) * 125), -35)
    
    tab:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8x8",
        edgeFile = "Interface\\Buttons\\WHITE8x8",
        tile = false, tileSize = 0, edgeSize = 1,
        insets = { left = 0, right = 0, top = 0, bottom = 0 }
    })
    tab:SetBackdropColor(0.2, 0.2, 0.2, 1)
    tab:SetBackdropBorderColor(0, 0, 0, 1)
    
    tab.text = tab:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    tab.text:SetPoint("CENTER")
    tab.text:SetText(text)
    
    tab:SetScript("OnClick", function()
        -- Reset all tabs
        for _, t in pairs(self.tabs) do
            t:SetBackdropColor(0.2, 0.2, 0.2, 1)
            t.text:SetTextColor(1, 0.82, 0)
        end
        -- Highlight selected
        tab:SetBackdropColor(0.3, 0.3, 0.3, 1)
        tab.text:SetTextColor(1, 1, 1)
        onClick(self)
    end)
    
    self.tabs[id] = tab
end

function IntelFrame:ShowOverview()
    self:ClearContent()
    
    local title = self.content:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    title:SetPoint("TOPLEFT", 0, 0)
    title:SetText("Market Overview - " .. GetRealmName())
    
    -- Stats Grid (Mockup)
    self:CreateStatBox("Market Health", "Bullish", 0, -40)
    self:CreateStatBox("Gold Velocity", "High", 150, -40)
    self:CreateStatBox("Top Category", "Herbs", 300, -40)
    
    -- Recent Alerts
    local alertsTitle = self.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    alertsTitle:SetPoint("TOPLEFT", 0, -100)
    alertsTitle:SetText("Recent AI Alerts:")
    
    -- Mock Alerts
    self:CreateAlertRow(1, "⚠️ High Volatility detected in Draconic Augment Rune market", -120)
    self:CreateAlertRow(2, "✅ Khaz Algar Ore prices stabilizing above 50g", -145)
    self:CreateAlertRow(3, "ℹ️ Darkmoon Faire approaching - Stock up on flour", -170)
end

function IntelFrame:ShowCrossRealm()
    self:ClearContent()
    
    local title = self.content:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    title:SetPoint("TOPLEFT", 0, 0)
    title:SetText("Cross-Realm Arbitrage")
    
    local desc = self.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    desc:SetPoint("TOPLEFT", 0, -25)
    desc:SetText("Top transfer opportunities from " .. GetRealmName())
    
    -- Headers
    self:CreateHeader("Item", 0, -60)
    self:CreateHeader("Target Realm", 200, -60)
    self:CreateHeader("Profit", 400, -60)
    
    -- Mock Data (would come from SavedVariables)
    self:CreateArbitrageRow(1, "Draconic Augment Rune", "Area 52", "15,000g", -85)
    self:CreateArbitrageRow(2, "Khaz Algar Ore", "Illidan", "4,500g", -110)
    self:CreateArbitrageRow(3, "Algari Weaverline", "Stormrage", "2,200g", -135)
end

function IntelFrame:ShowPredictions()
    self:ClearContent()
    
    local title = self.content:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    title:SetPoint("TOPLEFT", 0, 0)
    title:SetText("Price Predictions (Next 24h)")
    
    -- Mock Chart Placeholder
    local chartBg = self.content:CreateTexture(nil, "BACKGROUND")
    chartBg:SetColorTexture(0.1, 0.1, 0.1, 0.5)
    chartBg:SetPoint("TOPLEFT", 0, -40)
    chartBg:SetSize(600, 200)
    
    local chartText = self.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    chartText:SetPoint("CENTER", chartBg, "CENTER", 0, 0)
    chartText:SetText("[Price Chart Visualization Would Go Here]")
end

function IntelFrame:ClearContent()
    self.content:Hide()
    self.content = CreateFrame("Frame", nil, self.frame)
    self.content:SetPoint("TOPLEFT", 20, -70)
    self.content:SetPoint("BOTTOMRIGHT", -20, 20)
    self.content:Show()
end

-- Helper Functions
function IntelFrame:CreateStatBox(label, value, x, y)
    local box = CreateFrame("Frame", nil, self.content, "BackdropTemplate")
    box:SetSize(140, 50)
    box:SetPoint("TOPLEFT", x, y)
    box:SetBackdrop({
        bgFile = "Interface\\Tooltips\\UI-Tooltip-Background",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        tile = true, tileSize = 16, edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    box:SetBackdropColor(0, 0, 0, 0.5)
    
    local l = box:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    l:SetPoint("TOP", 0, -8)
    l:SetText(label)
    
    local v = box:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    v:SetPoint("BOTTOM", 0, 8)
    v:SetText(value)
end

function IntelFrame:CreateAlertRow(index, text, y)
    local row = self.content:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    row:SetPoint("TOPLEFT", 10, y)
    row:SetText(text)
end

function IntelFrame:CreateHeader(text, x, y)
    local h = self.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    h:SetPoint("TOPLEFT", x, y)
    h:SetText(text)
end

function IntelFrame:CreateArbitrageRow(index, item, realm, profit, y)
    local row = CreateFrame("Frame", nil, self.content)
    row:SetSize(600, 20)
    row:SetPoint("TOPLEFT", 0, y)
    
    local i = row:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    i:SetPoint("LEFT", 0, 0)
    i:SetText(item)
    
    local r = row:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    r:SetPoint("LEFT", 200, 0)
    r:SetText(realm)
    
    local p = row:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    p:SetPoint("LEFT", 400, 0)
    p:SetText(profit)
    p:SetTextColor(0, 1, 0)
end

function IntelFrame:Toggle()
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
    end
end
