local SW = SkillWeaver
SW.UI = SW.UI or {}

function SW.UI:InitMinimap()
    if self.minimapButton then return end

    -- 1. Create the Button Frame
    -- We keep the 31x31 size because it aligns perfectly with the border texture
    local b = CreateFrame("Button", "SkillWeaver_MinimapButton", Minimap)
    b:SetSize(31, 31) 
    b:SetFrameStrata("MEDIUM")
    b:SetFrameLevel(Minimap:GetFrameLevel() + 10)
    b:EnableMouse(true)
    b:RegisterForDrag("LeftButton")

    -- 2. Visual Assets (KEEPING THE FIX THAT WORKED)
    
    -- Background
    local bg = b:CreateTexture(nil, "BACKGROUND")
    bg:SetTexture("Interface\\Minimap\\UI-Minimap-Background")
    bg:SetSize(25, 25)
    bg:SetPoint("CENTER", b, "CENTER", 0, 1)
    bg:SetVertexColor(0.1, 0.1, 0.1, 1)

    -- Class Icon
    local icon = b:CreateTexture(nil, "ARTWORK")
    icon:SetSize(21, 21)
    icon:SetPoint("CENTER", b, "CENTER", 0, 1)
    local _, classFilename = UnitClass("player")
    icon:SetTexture("Interface\\Icons\\ClassIcon_" .. (classFilename or "WARRIOR"))
    
    -- Mask (Circle Cut)
    local mask = b:CreateMaskTexture()
    mask:SetTexture("Interface\\CharacterFrame\\TempPortraitAlphaMask")
    mask:SetSize(21, 21)
    mask:SetPoint("CENTER", b, "CENTER", 0, 1)
    icon:AddMaskTexture(mask)

    -- Border (Gold Ring)
    -- This specific combination (Size 52 + Point TL,0,0) is what fixed the picture alignment
    local border = b:CreateTexture(nil, "OVERLAY")
    border:SetTexture("Interface\\Minimap\\MiniMap-TrackingBorder")
    border:SetSize(52, 52)
    border:SetPoint("TOPLEFT", b, "TOPLEFT", 0, 0) 

    -- Highlight
    local highlight = b:CreateTexture(nil, "HIGHLIGHT")
    highlight:SetTexture("Interface\\Minimap\\UI-Minimap-ZoomButton-Highlight")
    highlight:SetBlendMode("ADD")
    highlight:SetSize(32, 32)
    highlight:SetPoint("CENTER", b, "CENTER", 0, 1)

    -- 3. Position Logic (REVERTED TO SAFE CENTER MATH)
    
    local function UpdatePosition(angle)
        -- FIXED: Radius 105 pushes it distinctly outside the map (Standard map radius is ~70-80)
        local r = 105 
        
        -- Simple, unbreakable Center-to-Center math
        local x = math.cos(angle) * r
        local y = math.sin(angle) * r
        
        b:ClearAllPoints()
        b:SetPoint("CENTER", Minimap, "CENTER", x, y)
        
        -- Save the angle
        if not SkillWeaverDB.ui then SkillWeaverDB.ui = { minimap = {} } end
        if not SkillWeaverDB.ui.minimap then SkillWeaverDB.ui.minimap = {} end
        SkillWeaverDB.ui.minimap.angle = angle
    end

    -- Initial Position
    local savedAngle = SkillWeaverDB.ui and SkillWeaverDB.ui.minimap and SkillWeaverDB.ui.minimap.angle
    UpdatePosition(savedAngle or -0.785) -- Default to roughly 45 degrees

    -- 4. Drag Scripts (Standard Atan2)
    
    b:SetScript("OnDragStart", function(self)
        self:LockHighlight()
        self.isDragging = true
        self:SetScript("OnUpdate", function()
            local mx, my = Minimap:GetCenter()
            local px, py = GetCursorPosition()
            local scale = Minimap:GetEffectiveScale()
            
            -- Normalize cursor to effective scale
            px, py = px / scale, py / scale
            
            -- Calculate angle relative to Minimap Center
            local angle = math.atan2(py - my, px - mx)
            
            UpdatePosition(angle)
        end)
    end)
    
    b:SetScript("OnDragStop", function(self)
        self:UnlockHighlight()
        self.isDragging = false
        self:SetScript("OnUpdate", nil)
    end)

    -- 5. Click Interactions
    b:RegisterForClicks("LeftButtonUp", "RightButtonUp")
    b:SetScript("OnClick", function(self, button)
        if self.isDragging then return end

        if button == "LeftButton" then
            if SW.UI and SW.UI.TogglePanel then SW.UI:TogglePanel() end
        else
            if SW.UI and SW.UI.ToggleMenu then SW.UI:ToggleMenu(self) end
        end
    end)

    -- 6. Tooltip
    b:SetScript("OnEnter", function(self)
        local centerX = UIParent:GetCenter()
        local buttonX = self:GetCenter()
        
        GameTooltip:SetOwner(self, "ANCHOR_NONE")
        if buttonX and centerX and buttonX > centerX then
            GameTooltip:SetPoint("RIGHT", self, "LEFT", -5, 0)
        else
            GameTooltip:SetPoint("LEFT", self, "RIGHT", 5, 0)
        end

        GameTooltip:SetText("|cFF00B4FFSkillWeaver|r")
        GameTooltip:AddLine("Left-Click: Open Panel", 1, 1, 1)
        GameTooltip:AddLine("Right-Click: Menu", 1, 1, 1)
        GameTooltip:Show()
    end)
    b:SetScript("OnLeave", function() GameTooltip:Hide() end)

    self.minimapButton = b
end