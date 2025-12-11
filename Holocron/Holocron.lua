local addonName, addonTable = ...
HolocronDB = HolocronDB or {}

-- ============================================================================
-- DATA SNAPSHOT ENGINE
-- ============================================================================
-- This function runs automatically to save the current character's state.
local function SnapshotCurrentChar()
    local name = UnitName("player")
    local realm = GetRealmName()
    local key = name .. " - " .. realm
    
    local level = UnitLevel("player")
    local gold = GetMoney()
    local zone = GetZoneText()
    local _, classFilename = UnitClass("player")
    
    -- Save to Database
    HolocronDB[key] = {
        name = name,
        realm = realm,
        level = level,
        gold = gold,
        zone = zone,
        class = classFilename,
        lastSeen = date("%Y-%m-%d %H:%M:%S")
    }
    
    print("|cff00ccffHolocron:|r Data updated for " .. key)
end

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
-- UI LOGIC
-- ============================================================================

local selectedKey = nil

local function UpdateDisplay()
    if not selectedKey or not HolocronDB[selectedKey] then return end
    
    local data = HolocronDB[selectedKey]
    local f = HolocronFrame.Content.Data
    
    -- Update Text Fields
    f.NameText:SetText(data.name .. " (" .. data.realm .. ")")
    
    -- Class Color Name
    local color = C_ClassColor.GetClassColor(data.class)
    if color then f.NameText:SetTextColor(color.r, color.g, color.b) end
    
    f.LevelText:SetText("Level " .. data.level)
    f.GoldText:SetText("Wealth: " .. FormatGold(data.gold))
    f.LocationText:SetText("Location: " .. data.zone)
    f.LastSeenText:SetText("Last Updated: " .. data.lastSeen)
end

-- DROPDOWN MENU LOGIC
local function InitDropdown(self, level, menuList)
    local info = UIDropDownMenu_CreateInfo()
    
    for key, data in pairs(HolocronDB) do
        info.text = key
        info.func = function() 
            selectedKey = key
            UIDropDownMenu_SetSelectedName(HolocronFrame.Content.Header.CharSelect, key)
            UpdateDisplay()
        end
        info.checked = (key == selectedKey)
        UIDropDownMenu_AddButton(info)
    end
end

-- ============================================================================
-- INIT
-- ============================================================================

local function OnEvent(self, event, ...)
    if event == "PLAYER_LOGIN" then
        -- 1. Initialize DB
        SnapshotCurrentChar()
        
        -- 2. Select current player by default
        local name = UnitName("player")
        local realm = GetRealmName()
        selectedKey = name .. " - " .. realm
        
        -- 3. Setup Dropdown
        UIDropDownMenu_Initialize(HolocronFrame.Content.Header.CharSelect, InitDropdown)
        UIDropDownMenu_SetSelectedName(HolocronFrame.Content.Header.CharSelect, selectedKey)
        UIDropDownMenu_SetText(HolocronFrame.Content.Header.CharSelect, selectedKey)
        
        -- 4. Initial Draw
        UpdateDisplay()
        
    elseif event == "PLAYER_MONEY" or event == "ZONE_CHANGED_NEW_AREA" or event == "PLAYER_LEVEL_UP" then
        -- Update data on changes
        SnapshotCurrentChar()
        
        -- If viewing self, update display immediately
        local currentKey = UnitName("player") .. " - " .. GetRealmName()
        if selectedKey == currentKey then UpdateDisplay() end
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PLAYER_MONEY")
eventFrame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
eventFrame:RegisterEvent("PLAYER_LEVEL_UP")
eventFrame:SetScript("OnEvent", OnEvent)

SLASH_HOLOCRON1 = "/holocron"
SlashCmdList["HOLOCRON"] = function(msg)
    if HolocronFrame:IsShown() then HolocronFrame:Hide() else HolocronFrame:Show() end
end
