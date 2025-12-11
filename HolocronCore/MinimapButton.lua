-- MinimapButton.lua
-- Shared minimap button library for Holocron addons

local LIBRARY_NAME = "HolocronMinimap-1.0"
local LIBRARY_VERSION = 1

if not LibStub then LibStub = {} end 
local lib = LibStub:NewLibrary and LibStub:NewLibrary(LIBRARY_NAME, LIBRARY_VERSION)
if not lib then
    -- Fallback if LibStub not available
    lib = {}
    _G[LIBRARY_NAME] = lib
end

-- Create a minimap button
function lib:CreateMinimapButton(addonName, config)
    config = config or {}
    
    local button = CreateFrame("Button", addonName .. "MinimapButton", Minimap)
    button:SetSize(31, 31)
    button:SetFrameStrata("MEDIUM")
    button:SetFrameLevel(8)
    button:RegisterForClicks("LeftButtonUp", "RightButtonUp")
    button:RegisterForDrag("LeftButton")
    button:SetHighlightTexture("Interface\\Minimap\\UI-Minimap-ZoomButton-Highlight")
    
    -- Icon
    local icon = button:CreateTexture(nil, "BACKGROUND")
    icon:SetSize(20, 20)
    icon:SetPoint("CENTER", 0, 1)
    icon:SetTexture(config.icon or "Interface\\Icons\\INV_Misc_QuestionMark")
    button.icon = icon
    
    -- Border
    local overlay = button:CreateTexture(nil, "OVERLAY")
    overlay:SetSize(53, 53)
    overlay:SetTexture("Interface\\Minimap\\MiniMap-TrackingBorder")
    overlay:SetPoint("TOPLEFT")
    
    -- Dragging
    local angle = config.angle or 180
    button.angle = angle
    button.db = config.db or {} -- SavedVariables reference
    
    button:SetScript("OnDragStart", function(self)
        self:LockHighlight()
        self.isDragging = true
    end)
    
    button:SetScript("OnDragStop", function(self)
        self:UnlockHighlight()
        self.isDragging = false
        if self.db then
            self.db.minimapAngle = self.angle
        end
    end)
    
    button:SetScript("OnUpdate", function(self)
        if self.isDragging then
            local mx, my = Minimap:GetCenter()
            local px, py = GetCursorPosition()
            local scale = Minimap:GetEffectiveScale()
            px, py = px / scale, py / scale
            
            local angle = math.atan2(py - my, px - mx)
            self.angle = math.deg(angle)
            self:UpdatePosition()
        end
    end)
    
    -- Click handlers
    button:SetScript("OnClick", function(self, btn)
        if btn == "LeftButton" then
            if config.OnLeftClick then
                config.OnLeftClick(self)
            end
        elseif btn == "RightButton" then
            if config.OnRightClick then
                config.OnRightClick(self)
            end
        end
    end)
    
    button:SetScript("OnEnter", function(self)
        GameTooltip:SetOwner(self, "ANCHOR_LEFT")
        GameTooltip:SetText(config.tooltip or addonName, 1, 1, 1)
        if config.tooltipText then
            GameTooltip:AddLine(config.tooltipText, nil, nil, nil, true)
        end
        GameTooltip:AddLine(" ")
        GameTooltip:AddLine("|cff00ff00Left-Click:|r Toggle", 0.7, 0.7, 0.7)
        GameTooltip:AddLine("|cff00ff00Right-Click:|r Options", 0.7, 0.7, 0.7)
        GameTooltip:AddLine("|cff00ff00Drag:|r Move", 0.7, 0.7, 0.7)
        GameTooltip:Show()
    end)
    
    button:SetScript("OnLeave", function(self)
        GameTooltip:Hide()
    end)
    
    -- Position update function
    function button:UpdatePosition()
        local x = math.cos(math.rad(self.angle)) * 80
        local y = math.sin(math.rad(self.angle)) * 80
        self:SetPoint("CENTER", Minimap, "CENTER", x, y)
    end
    
    -- Initial position
    if config.db and config.db.minimapAngle then
        button.angle = config.db.minimapAngle
    end
    button:UpdatePosition()
    
    -- Show/Hide functions
    function button:Toggle()
        if self:IsShown() then
            self:Hide()
            if self.db then
                self.db.minimapHidden = true
            end
        else
            self:Show()
            if self.db then
                self.db.minimapHidden = false
            end
        end
    end
    
    -- Load saved visibility
    if config.db and config.db.minimapHidden then
        button:Hide()
    else
        button:Show()
    end
    
    return button
end

return lib
