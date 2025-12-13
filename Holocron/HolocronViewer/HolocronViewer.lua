-- HolocronViewer.lua (Native WoW API Version)
local addonName, addon = ...
print("|cff00ff00HolocronViewer:|r Native Core Loaded.")

-- NOTE: Global Init removed to force ADDON_LOADED usage

-- ============================================================================
-- FORMATTING
-- ============================================================================
local function FormatGold(amount)
    local gold = math.floor(amount / 10000)
    local silver = math.floor((amount % 10000) / 100)
    local copper = amount % 100
    return "|cffffd700" .. gold .. "g|r |cffc7c7cf" .. silver .. "s|r"
end

-- ============================================================================
-- DATA ENGINE
-- ============================================================================
local function SnapshotCurrentChar()
    if not HolocronViewerDB or not HolocronViewerDB.characters then return end
    
    local name = UnitName("player")
    local realm = GetRealmName()
    local key = name .. " - " .. realm
    
    local level = UnitLevel("player")
    local gold = GetMoney()
    local zone = GetZoneText()
    local _, classFilename = UnitClass("player")
    
    HolocronViewerDB.characters[key] = {
        name = name,
        realm = realm,
        class = classFilename,
        level = level,
        gold = gold,
        zone = zone,
        lastSeen = date("%Y-%m-%d %H:%M:%S")
    }
    -- print("|cff00ff00HolocronViewer:|r Snapshot Updated: "..key) 
end

-- ============================================================================
-- EVENTS
-- ============================================================================
local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("PLAYER_MONEY")
eventFrame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
eventFrame:RegisterEvent("PLAYER_LEVEL_UP")

eventFrame:SetScript("OnEvent", function(self, event, ...)
    if event == "ADDON_LOADED" and ... == addonName then
        HolocronViewerDB = HolocronViewerDB or {}
        
        -- SAFE MIGRATION
        if not HolocronViewerDB.version or HolocronViewerDB.version < 1 then
            HolocronViewerDB.version = 1
            HolocronViewerDB.characters = HolocronViewerDB.characters or {}
            HolocronViewerDB.profile = HolocronViewerDB.profile or { framePos = {"CENTER", UIParent, "CENTER", 0, 0} }
            print("|cff00ff00HolocronViewer:|r DB Migrated to v1.")
        else
            HolocronViewerDB.characters = HolocronViewerDB.characters or {}
            HolocronViewerDB.profile = HolocronViewerDB.profile or { framePos = {"CENTER", UIParent, "CENTER", 0, 0} }
        end
        
        SnapshotCurrentChar()
        print("|cff00ff00HolocronViewer:|r Loaded.")
        
    elseif event == "PLAYER_LOGIN" then
        addon:CreateMainFrame()
        
    elseif event == "PLAYER_MONEY" or event == "ZONE_CHANGED_NEW_AREA" or event == "PLAYER_LEVEL_UP" then
        SnapshotCurrentChar()
    end
end)

-- ============================================================================
-- UI Creation
-- ============================================================================
function addon:CreateMainFrame()
    if addon.Frame then return end
    
    local f = CreateFrame("Frame", "HolocronMainFrame", UIParent, "BackdropTemplate")
    addon.Frame = f
    f:SetSize(800, 600)
    
    local pos = HolocronViewerDB.profile.framePos
    
    local point, rel, relPoint, x, y = "CENTER", nil, "CENTER", 0, 0
    if type(pos) == "table" then
        point    = pos[1] or point
        rel      = pos[2]
        relPoint = pos[3] or relPoint
        x        = tonumber(pos[4]) or x
        y        = tonumber(pos[5]) or y
    end

    local relativeTo = UIParent
    
    -- Guard against corrupt 'rel' being a table (fix for SetPoint wrong object type)
    if type(rel) == "table" and not rel.GetObjectType then
        rel = "UIParent"
        -- Repair corrupt DB entry
        if HolocronViewerDB and HolocronViewerDB.profile and HolocronViewerDB.profile.framePos then
             HolocronViewerDB.profile.framePos[2] = "UIParent"
        end
    end

    if type(rel) == "string" then
        relativeTo = _G[rel] or UIParent
    elseif type(rel) == "table" and rel.GetObjectType then
        relativeTo = rel
    end

    f:ClearAllPoints()
    f:SetPoint(point, relativeTo, relPoint, x, y)
    
    f:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\DialogFrame\\UI-DialogBox-Border",
        tile = true, tileSize = 32, edgeSize = 32,
        insets = { left = 8, right = 8, top = 8, bottom = 8 }
    })
    f:SetBackdropColor(0, 0, 0, 0.9)
    f:SetBackdropBorderColor(1, 1, 1, 1)
    
    f:EnableMouse(true)
    f:SetMovable(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", function(self) self:StartMoving() end)
    f:SetScript("OnDragStop", function(self)
        self:StopMovingOrSizing()
        local point, relativeTo, relativePoint, x, y = self:GetPoint()
        -- Always save relativeTo as string "UIParent" or similar safe global
        -- Avoid saving the actual frame object which causes SetPoint crashes on load
        HolocronViewerDB.profile.framePos = {point, "UIParent", relativePoint, x, y}
    end)
    
    f:Hide()
    
    -- Title
    f.Title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    f.Title:SetPoint("TOP", 0, -15)
    f.Title:SetText("Holocron Viewer")

    -- Simple Content Display (Debugging Phase)
    f.ContentText = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    f.ContentText:SetPoint("CENTER", 0, 0)
    f.ContentText:SetText("Type /holo dump to see data status.")
end

-- ============================================================================
-- SLASH COMMANDS
-- ============================================================================
SLASH_HOLOCRON1 = "/holo"
SlashCmdList["HOLOCRON"] = function(msg)
    local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
    
    if cmd == "dump" then
        if not HolocronViewerDB then return end
        local c = 0
        if HolocronViewerDB.characters then
            for _ in pairs(HolocronViewerDB.characters) do c = c + 1 end
        end
        print("HOLO DUMP: Characters="..c)
        
    elseif cmd == "sanity" then
        if not HolocronViewerDB then return end
        local passed = true
        if not HolocronViewerDB.characters then 
            print("FAIL: Missing characters table")
            passed = false 
        end
        
        if passed then 
            print("|cff00FF00HOLO SANITY PASS|r") 
            print(string.format('SANITY_RESULT {"addon":"Holocron","status":"OK","checks":1,"failures":0}'))
        else 
            print("|cffrr0000HOLO SANITY FAIL|r") 
            print(string.format('SANITY_RESULT {"addon":"Holocron","status":"FAIL","checks":1,"failures":1}'))
        end
        
    elseif cmd == "resetdb" then
        HolocronViewerDB = {
            version = 1,
            characters = {},
            profile = { framePos = {"CENTER", UIParent, "CENTER", 0, 0} }
        }
        ReloadUI()
        
    else
        -- Toggle UI
        if not addon.Frame then addon:CreateMainFrame() end
        if addon.Frame:IsShown() then
            addon.Frame:Hide()
        else
            addon.Frame:Show()
        end
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
            SlashCmdList["HOLOCRON"]("")
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
                HolocronViewerDB.profile.framePos = {"CENTER", UIParent, "CENTER", 0, 0}
            end
        end
    })
    
    addon.optionsPanel = panel
end

-- Initialize Late
C_Timer.After(1, function()
    CreateMinimapButton()
    addon:CreateOptionsPanel()
end)
