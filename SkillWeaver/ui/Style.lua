-- SkillWeaver UI Styling - Runic Arcane Theme
local SW = SkillWeaver
SW.UI = SW.UI or {}
SW.UI.Style = {}

-- Arcane color palette
SW.UI.Style.Colors = {
    arcane = {0.3, 0.85, 1.0, 1.0},      -- Bright cyan
    arcaneDim = {0.2, 0.6, 0.8, 0.8},    -- Dimmed cyan
    arcaneDark = {0.1, 0.3, 0.4, 0.6},   -- Dark cyan
    slate = {0.08, 0.08, 0.12, 0.97},    -- Background
    slateBorder = {0.25, 0.65, 0.85, 0.9}, -- Border
    textGlow = {0.4, 0.85, 1.0, 1.0},    -- Title text
    textDim = {0.5, 0.5, 0.6, 1.0},      -- Subtitle
}

-- Style a button with arcane glow on hover
function SW.UI.Style:ApplyArcaneButton(btn)
    if not btn then return end
    
    -- Store original colors
    btn.originalR, btn.originalG, btn.originalB = 0.3, 0.3, 0.4
    
    -- Override normal texture colors
    local normalTex = btn:GetNormalTexture()
    if normalTex then
        normalTex:SetVertexColor(0.2, 0.4, 0.5, 0.9)
    end
    
    -- Hover effect: cyan glow
    btn:HookScript("OnEnter", function(self)
        local tex = self:GetNormalTexture()
        if tex then tex:SetVertexColor(0.3, 0.7, 0.9, 1.0) end
        
        local fs = self:GetFontString()
        if fs then fs:SetTextColor(0.5, 1.0, 1.0, 1.0) end
    end)
    
    btn:HookScript("OnLeave", function(self)
        local tex = self:GetNormalTexture()
        if tex then tex:SetVertexColor(0.2, 0.4, 0.5, 0.9) end
        
        local fs = self:GetFontString()
        if fs then fs:SetTextColor(1.0, 1.0, 1.0, 1.0) end
    end)
end

-- Apply theme to SkillWeaverFrame after it loads
function SW.UI.Style:ApplyTheme()
    local frame = SkillWeaverFrame
    if not frame then return end
    
    -- Style buttons
    if frame.ImportButton then
        self:ApplyArcaneButton(frame.ImportButton)
    end
    if frame.PopulateButton then
        self:ApplyArcaneButton(frame.PopulateButton)
    end
    if frame.BindButton then
        self:ApplyArcaneButton(frame.BindButton)
    end
    
    -- Style dropdown
    local drop = frame.ContentDropdown
    if drop and drop:GetName() then
        local dropName = drop:GetName()
        local left = _G[dropName .. "Left"]
        local middle = _G[dropName .. "Middle"]
        local right = _G[dropName .. "Right"]
        
        if left then left:SetVertexColor(0.3, 0.6, 0.8, 0.8) end
        if middle then middle:SetVertexColor(0.3, 0.6, 0.8, 0.8) end
        if right then right:SetVertexColor(0.3, 0.6, 0.8, 0.8) end
    end
end

-- Hook into frame show to apply styling
local function OnFrameShow()
    SW.UI.Style:ApplyTheme()
end

-- Register for first show
local loader = CreateFrame("Frame")
loader:RegisterEvent("ADDON_LOADED")
loader:SetScript("OnEvent", function(self, event, addon)
    if addon == "SkillWeaver" then
        C_Timer.After(0.1, function()
            if SkillWeaverFrame then
                SkillWeaverFrame:HookScript("OnShow", OnFrameShow)
                -- Apply immediately if already visible
                if SkillWeaverFrame:IsShown() then
                    OnFrameShow()
                end
            end
        end)
        self:UnregisterEvent("ADDON_LOADED")
    end
end)
