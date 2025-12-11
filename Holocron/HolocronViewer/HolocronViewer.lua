-- HolocronViewer.lua (Native WoW API Version)
local addonName, addon = ...
print("|cff00ff00HolocronViewer:|r Native Core Loaded.")

-- 1. SavedVariables Setup (Top Level Default)
HolocronViewerDB = HolocronViewerDB or {
    profile = { framePos = {"CENTER", UIParent, "CENTER", 0, 0} }
}

-- 2. Event Handling
local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("ADDON_LOADED")

eventFrame:SetScript("OnEvent", function(self, event, ...)
    if event == "PLAYER_LOGIN" then
        print("|cff00ff00HolocronViewer:|r PLAYER_LOGIN. Initializing...")
        addon:CreateMainFrame()
    elseif event == "ADDON_LOADED" and ... == addonName then
        print("|cff00ff00HolocronViewer:|r ADDON_LOADED. DB Loaded.")
        HolocronViewerDB = HolocronViewerDB or { profile = { framePos = {"CENTER", UIParent, "CENTER", 0, 0} } }
    end
end)

-- 3. UI Creation
function addon:CreateMainFrame()
    print("|cff00ff00HolocronViewer:|r CreateMainFrame called.")
    if addon.Frame then 
        print("|cff00ff00HolocronViewer:|r Frame already exists.")
        return 
    end
    
    -- Main Frame with BackdropTemplate
    local f = CreateFrame("Frame", "HolocronMainFrame", UIParent, "BackdropTemplate")
    addon.Frame = f -- Assign IMMEDIATELY
    print("|cff00ff00HolocronViewer:|r Frame Created: " .. tostring(f))
    
    f:SetSize(800, 600)
    
    -- Safe SetPoint (Force CENTER for debug)
    f:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
    print("|cff00ff00HolocronViewer:|r Point Set to CENTER.")
    
    -- Backdrop Configuration
    if not f.SetBackdrop then
        print("|cff00ff00HolocronViewer:|r Mixing in BackdropTemplate...")
        Mixin(f, BackdropTemplateMixin)
    end
    
    f:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\DialogFrame\\UI-DialogBox-Border",
        tile = true, tileSize = 32, edgeSize = 32,
        insets = { left = 8, right = 8, top = 8, bottom = 8 }
    })
    f:SetBackdropColor(0, 0, 0, 0.9)
    f:SetBackdropBorderColor(1, 1, 1, 1)
    print("|cff00ff00HolocronViewer:|r Backdrop Set.")
    
    f:EnableMouse(true)
    f:SetMovable(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", function(self) self:StartMoving() end)
    f:SetScript("OnDragStop", function(self)
        self:StopMovingOrSizing()
        local point, _, relativePoint, x, y = self:GetPoint()
        HolocronViewerDB.profile.framePos = {point, relativePoint, x, y}
    end)
    
    f:Hide()
    
    -- Title
    f.Title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    f.Title:SetPoint("TOP", 0, -15)
    f.Title:SetText("Holocron Viewer")
    
    -- Content Placeholder
    local sf = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
    sf:SetPoint("TOPLEFT", 10, -40)
    sf:SetPoint("BOTTOMRIGHT", -30, 10)
    
    local content = CreateFrame("Frame")
    content:SetSize(750, 1000)
    sf:SetScrollChild(content)
    
    local text = content:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    text:SetPoint("TOPLEFT", 10, -10)
    text:SetText("Holocron Database:\n\n1. Item A\n2. Item B\n3. Item C\n\n(Real data connection pending...)")
    text:SetJustifyH("LEFT")
    
    print("|cff00ff00HolocronViewer:|r UI Initialized Successfully.")
end

-- 4. Slash Commands
SLASH_HOLOCRON1 = "/holo"
SlashCmdList["HOLOCRON"] = function(msg)
    print("|cff00ff00HolocronViewer:|r Slash Command /holo received.")
    if not addon.Frame then addon:CreateMainFrame() end
    
    if addon.Frame:IsShown() then
        addon.Frame:Hide()
    else
        addon.Frame:Show()
    end
end

-- Create Minimap Button
local function CreateMinimapButton()
    if not _G["HolocronMinimap-1.0"] then return end
    
    local MinimapLib = _G["HolocronMinimap-1.0"]
    addon.minimapButton = MinimapLib:CreateMinimapButton("HolocronViewer", {
        icon = "Interface\\Icons\\INV_Misc_Book_11",
        tooltip = "Holocron Viewer",
        tooltipText = "View inventory and character data",
        db = HolocronViewerDB.profile,
        OnLeftClick = function() 
            if addon.Frame then
                if addon.Frame:IsShown() then
                    addon.Frame:Hide()
                else
                    addon.Frame:Show()
                end
            end
        end,
        OnRightClick = function() 
            if addon.optionsPanel then
                InterfaceOptionsFrame_OpenToCategory(addon.optionsPanel)
                InterfaceOptionsFrame_OpenToCategory(addon.optionsPanel)
            end
        end
    })
end

-- Create Options Panel
function addon:CreateOptionsPanel()
    local OptionsLib = _G["HolocronOptions-1.0"]
    if not OptionsLib then return end
    
    local panel = OptionsLib:CreateOptionsPanel("HolocronViewer", {
        title = "Holocron Viewer",
        subtitle = "Central hub for character data and progression tracking"
    })
    
    panel:AddHeader("General")
    
    panel:AddCheckbox({
        name = "Show Minimap Button",
        get = function() return not HolocronViewerDB.profile.minimapHidden end,
        set = function(val) 
            HolocronViewerDB.profile.minimapHidden = not val
            if addon.minimapButton then
                if val then addon.minimapButton:Show()
                else addon.minimapButton:Hide() end
            end
        end
    })
    
    panel:AddButton({
        name = "Reset Window Position",
        callback = function()
            if addon.Frame then
                addon.Frame:ClearAllPoints()
                addon.Frame:SetPoint("CENTER")
                HolocronViewerDB.profile.framePos = {"CENTER", "CENTER", 0, 0}
            end
        end
    })
    
    addon.optionsPanel = panel
end

-- Initialize
C_Timer.After(1, function()
    CreateMinimapButton()
    addon:CreateOptionsPanel()
end)
