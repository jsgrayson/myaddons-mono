-- HolocronViewer Dashboard Module
local addonName, addon = ...
local Dashboard = {}
addon.Dashboard = Dashboard

function Dashboard:Create(parent)
    local frame = CreateFrame("Frame", nil, parent)
    frame:SetAllPoints()
    
    -- Title
    local title = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    title:SetPoint("TOPLEFT", 20, -20)
    title:SetText("Holocron Dashboard")
    
    -- Summary Cards Container
    local cardContainer = CreateFrame("Frame", nil, frame)
    cardContainer:SetSize(560, 120)
    cardContainer:SetPoint("TOP", 0, -60)
    
    -- Helper to create cards
    local function CreateCard(name, label, value, xOffset)
        local card = CreateFrame("Frame", nil, cardContainer, "BackdropTemplate")
        card:SetSize(170, 100)
        card:SetPoint("LEFT", xOffset, 0)
        card:SetBackdrop({
            bgFile = "Interface\\Buttons\\WHITE8X8",
            edgeFile = "Interface\\Buttons\\WHITE8X8",
            edgeSize = 1,
        })
        card:SetBackdropColor(0.1, 0.1, 0.1, 0.5)
        card:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
        
        local lbl = card:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        lbl:SetPoint("TOP", 0, -15)
        lbl:SetText(label)
        lbl:SetTextColor(0.7, 0.7, 0.7)
        
        local val = card:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
        val:SetPoint("CENTER", 0, 5)
        val:SetText(value)
        
        frame[name] = val
        return card
    end
    
    CreateCard("totalGold", "Total Gold", "---", 0)
    CreateCard("portfolioVal", "Portfolio Value", "---", 195)
    CreateCard("activeAlerts", "Active Alerts", "0", 390)
    
    -- Recent Activity List
    local listHeader = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    listHeader:SetPoint("TOPLEFT", 20, -200)
    listHeader:SetText("Recent System Activity")
    
    local scroll = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
    scroll:SetSize(540, 250)
    scroll:SetPoint("TOPLEFT", 20, -230)
    
    local content = CreateFrame("Frame", nil, scroll)
    content:SetSize(540, 1)
    scroll:SetScrollChild(content)
    
    frame.activityLog = content
    
    self.frame = frame
    return frame
end

function Dashboard:Update(data)
    if not self.frame then return end
    
    if data.gold then
        self.frame.totalGold:SetText(GetCoinTextureString(data.gold))
    end
    
    if data.portfolio then
        self.frame.portfolioVal:SetText(GetCoinTextureString(data.portfolio))
    end
    
    if data.alerts then
        self.frame.activeAlerts:SetText(data.alerts)
    end
end
