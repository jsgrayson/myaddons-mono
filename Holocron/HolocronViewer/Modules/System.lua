-- HolocronViewer System Module
local addonName, addon = ...
local System = {}
addon.System = System

function System:Create(parent)
    local frame = CreateFrame("Frame", nil, parent)
    frame:SetAllPoints()
    
    local title = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    title:SetPoint("TOPLEFT", 20, -20)
    title:SetText("System Status")
    
    -- Status Indicators
    local statusFrame = CreateFrame("Frame", nil, frame, "BackdropTemplate")
    statusFrame:SetSize(560, 150)
    statusFrame:SetPoint("TOP", 0, -60)
    statusFrame:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    statusFrame:SetBackdropColor(0.1, 0.1, 0.1, 0.5)
    statusFrame:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
    
    local function CreateStatusRow(label, yOffset)
        local lbl = statusFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        lbl:SetPoint("TOPLEFT", 20, yOffset)
        lbl:SetText(label)
        
        local val = statusFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        val:SetPoint("TOPRIGHT", -20, yOffset)
        val:SetText("Unknown")
        
        return val
    end
    
    self.backendStatus = CreateStatusRow("Backend Connection:", -20)
    self.syncStatus = CreateStatusRow("Sync Tool:", -50)
    self.lastUpdate = CreateStatusRow("Last Update:", -80)
    self.version = CreateStatusRow("Addon Version:", -110)
    
    self.version:SetText(GetAddOnMetadata(addonName, "Version") or "1.0")
    
    return frame
end

function System:Update(data)
    if not self.backendStatus then return end
    
    self.backendStatus:SetText(data.connected and "|cFF00FF00Connected|r" or "|cFFFF0000Disconnected|r")
    self.syncStatus:SetText(data.syncActive and "|cFF00FF00Active|r" or "|cFFFF0000Inactive|r")
    self.lastUpdate:SetText(date("%H:%M:%S"))
end
