local addonName, addon = ...
local UI = PetWeaverUI

-- Minimap Button
UI.minimapButton = UI.minimapButton or {}
local MinimapBtn = UI.minimapButton

function MinimapBtn:Create()
    local button = CreateFrame("Button", "PetWeaverMinimapButton", Minimap)
    button:SetSize(32, 32)
    button:SetFrameStrata("MEDIUM")
    button:SetFrameLevel(8)
    button:SetClampedToScreen(true)
    button:SetMovable(true)
    button:EnableMouse(true)
    button:RegisterForDrag("LeftButton")
    button:RegisterForClicks("LeftButtonUp", "RightButtonUp")
    
    -- Icon
    local icon = button:CreateTexture(nil, "BACKGROUND")
    icon:SetSize(20, 20)
    icon:SetPoint("CENTER", 0, 1)
    icon:SetTexture("Interface\\Icons\\INV_Pet_BabyBlizzardBear")
    button.icon = icon
    
    -- Border
    local overlay = button:CreateTexture(nil, "OVERLAY")
    overlay:SetSize(53, 53)
    overlay:SetPoint("TOPLEFT", 0, 0)
    overlay:SetTexture("Interface\\Minimap\\MiniMap-TrackingBorder")
    button.overlay = overlay
    
    -- Highlight
    button:SetHighlightTexture("Interface\\Minimap\\UI-Minimap-ZoomButton-Highlight")
    
    -- Position
    button:SetPoint("TOPLEFT", Minimap, "TOPLEFT", -15, -45)
    
    -- Tooltip
    button:SetScript("OnEnter", function(self)
        GameTooltip:SetOwner(self, "ANCHOR_LEFT")
        GameTooltip:SetText("|cff00ff00PetWeaver|r", 1, 1, 1)
        GameTooltip:AddLine("Left-click: Toggle UI", 1, 1, 1)
        GameTooltip:AddLine("Right-click: Settings", 1, 1, 1)
        GameTooltip:AddLine("Drag to move", 0.7, 0.7, 0.7)
        GameTooltip:Show()
    end)
    
    button:SetScript("OnLeave", function(self)
        GameTooltip:Hide()
    end)
    
    -- Click handler
    button:SetScript("OnClick", function(self, btn)
        if btn == "LeftButton" then
            PetWeaverUI:Toggle()
        elseif btn == "RightButton" then
            PetWeaverUI:ShowSettings()
        end
    end)
    
    -- Dragging
    button:SetScript("OnDragStart", function(self)
        self:LockHighlight()
        self:SetScript("OnUpdate", MinimapBtn.OnUpdate)
    end)
    
    button:SetScript("OnDragStop", function(self)
        self:UnlockHighlight()
        self:SetScript("OnUpdate", nil)
    end)
    
    self.button = button
    return button
end

function MinimapBtn:OnUpdate()
    local mx, my = Minimap:GetCenter()
    local px, py = GetCursorPosition()
    local scale = Minimap:GetEffectiveScale()
    
    px, py = px / scale, py / scale
    
    local angle = math.atan2(py - my, px - mx)
    MinimapBtn.button:SetPoint("TOPLEFT", Minimap, "TOPLEFT", 
        52 - (80 * cos(angle)), 
        (80 * sin(angle)) - 52)
end

function MinimapBtn:Show()
    if self.button then
        self.button:Show()
    end
end

function MinimapBtn:Hide()
    if self.button then
        self.button:Hide()
    end
end
