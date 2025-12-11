-- HolocronViewer Goblin Module
local addonName, addon = ...
local Goblin = {}
addon.Goblin = Goblin

function Goblin:Create(parent)
    local frame = CreateFrame("Frame", nil, parent)
    frame:SetAllPoints()
    
    local title = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    title:SetPoint("TOPLEFT", 20, -20)
    title:SetText("Goblin Market Intelligence")
    
    -- Prediction List
    local scroll = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
    scroll:SetSize(560, 400)
    scroll:SetPoint("TOP", 0, -60)
    
    local content = CreateFrame("Frame", nil, scroll)
    content:SetSize(560, 1)
    scroll:SetScrollChild(content)
    
    self.content = content
    self.frame = frame
    
    -- Initial Mock Data
    self:Update({
        predictions = {
            {event = "Patch 11.2.7", impact = "High", items = "Herbs, Flasks", confidence = "85%"},
            {event = "Mage Buffs", impact = "Medium", items = "Intellect Potions", confidence = "72%"},
        }
    })
    
    return frame
end

function Goblin:Update(data)
    if not self.content then return end
    
    -- Clear existing
    for _, child in ipairs({self.content:GetChildren()}) do
        child:Hide()
    end
    
    local predictions = data.predictions or {}
    
    for i, pred in ipairs(predictions) do
        local row = CreateFrame("Frame", nil, self.content, "BackdropTemplate")
        row:SetSize(540, 60)
        row:SetPoint("TOPLEFT", 0, -((i-1)*65))
        row:SetBackdrop({
            bgFile = "Interface\\Buttons\\WHITE8X8",
            edgeFile = "Interface\\Buttons\\WHITE8X8",
            edgeSize = 1,
        })
        row:SetBackdropColor(0.15, 0.15, 0.15, 0.8)
        row:SetBackdropBorderColor(0.4, 0.4, 0.4, 1)
        
        local event = row:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
        event:SetPoint("TOPLEFT", 10, -10)
        event:SetText(pred.event)
        
        local details = row:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        details:SetPoint("TOPLEFT", 10, -35)
        details:SetText("Impact: " .. pred.impact .. " | Items: " .. pred.items)
        
        local conf = row:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
        conf:SetPoint("RIGHT", -20, 0)
        conf:SetText(pred.confidence)
        conf:SetTextColor(0, 1, 0)
    end
end
