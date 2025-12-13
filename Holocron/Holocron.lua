local addonName, addonTable = ...
-- ============================================================================
-- DATA SNAPSHOT ENGINE
-- ============================================================================
local function SnapshotCurrentChar()
    if not HolocronDB or not HolocronDB.characters then return end
    
    local name = UnitName("player")
    local realm = GetRealmName()
    local key = name .. " - " .. realm
    
    local level = UnitLevel("player")
    local gold = GetMoney()
    local zone = GetZoneText()
    local _, classFilename = UnitClass("player")
    
    -- Save to Database (Namespaced)
    HolocronDB.characters[key] = {
        name = name,
        realm = realm,
        class = classFilename,
        level = level,
        gold = gold,
        zone = zone,
        lastSeen = date("%Y-%m-%d %H:%M:%S")
    }
    
    -- print("|cff00ccffHolocron:|r Data updated for " .. key)
end

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
    if not selectedKey or not HolocronDB.characters[selectedKey] then return end
    
    local data = HolocronDB.characters[selectedKey]
    local f = HolocronFrame.Content.Data
    
    f.NameText:SetText(data.name .. " (" .. data.realm .. ")")
    
    local color = C_ClassColor.GetClassColor(data.class)
    if color then f.NameText:SetTextColor(color.r, color.g, color.b) end
    
    f.LevelText:SetText("Level " .. data.level)
    f.GoldText:SetText("Wealth: " .. FormatGold(data.gold))
    f.LocationText:SetText("Location: " .. data.zone)
    f.LastSeenText:SetText("Last Updated: " .. data.lastSeen)
end

local function InitDropdown(self, level, menuList)
    local info = UIDropDownMenu_CreateInfo()
    
    if HolocronDB and HolocronDB.characters then
        for key, data in pairs(HolocronDB.characters) do
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
end

-- ============================================================================
-- INIT & EVENTS
-- ============================================================================

local function OnEvent(self, event, ...)
    if event == "ADDON_LOADED" then
        local name = ...
        if name == addonName then
            HolocronDB = HolocronDB or {}
            
            -- SAFE MIGRATION (v1)
            -- If version missing, perform flat -> nested migration
            if not HolocronDB.version or HolocronDB.version < 1 then
                local chars = {}
                -- Extract existing data (filter out noise)
                for k, v in pairs(HolocronDB) do
                    if type(v) == "table" and v.name and v.realm then
                        chars[k] = v
                    end
                end
                
                -- Wipe & Re-init
                wipe(HolocronDB)
                HolocronDB.version = 1
                HolocronDB.settings = { debug = false }
                HolocronDB.characters = chars
                
                print("|cff00ccffHolocron:|r Database Migrated to v1.")
            else
                -- Integrity Assurance
                HolocronDB.characters = HolocronDB.characters or {}
            end
            
            -- Initial Snapshot
            SnapshotCurrentChar()
            print("|cff00ccffHolocron:|r Loaded.")
        end

    elseif event == "PLAYER_LOGIN" then
        -- Default: Select current player
        local name = UnitName("player")
        local realm = GetRealmName()
        selectedKey = name .. " - " .. realm
        
        UIDropDownMenu_Initialize(HolocronFrame.Content.Header.CharSelect, InitDropdown)
        UIDropDownMenu_SetSelectedName(HolocronFrame.Content.Header.CharSelect, selectedKey)
        UIDropDownMenu_SetText(HolocronFrame.Content.Header.CharSelect, selectedKey)
        
        UpdateDisplay()
        
    elseif event == "PLAYER_MONEY" or event == "ZONE_CHANGED_NEW_AREA" or event == "PLAYER_LEVEL_UP" then
        SnapshotCurrentChar()
        local currentKey = UnitName("player") .. " - " .. GetRealmName()
        if selectedKey == currentKey then UpdateDisplay() end
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PLAYER_MONEY")
eventFrame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
eventFrame:RegisterEvent("PLAYER_LEVEL_UP")
eventFrame:SetScript("OnEvent", OnEvent)

-- ============================================================================
-- SLASH COMMANDS
-- ============================================================================
SLASH_HOLOCRON1 = "/holocron"
SLASH_HOLOCRON2 = "/holo"
SlashCmdList["HOLOCRON"] = function(msg)
    local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
    
    if cmd == "dump" then
        if not HolocronDB then return end
        local c = 0
        if HolocronDB.characters then
            for _ in pairs(HolocronDB.characters) do c = c + 1 end
        end
        print("HOLO DUMP: Characters="..c)
        
    elseif cmd == "sanity" then
        if not HolocronDB then return end
        local passed = true
        if not HolocronDB.characters then 
            print("FAIL: Missing characters table")
            passed = false 
        else
            for k, v in pairs(HolocronDB.characters) do
                if not v.name or not v.realm then
                    print("FAIL: Invalid char entry: "..k)
                    passed = false
                end
            end
        end
        
        if passed then print("|cff00FF00HOLO SANITY PASS|r") else print("|cffrr0000HOLO SANITY FAIL|r") end
        
    elseif cmd == "resetdb" then
        HolocronDB = {
            version = 1,
            settings = { debug = false },
            characters = {}
        }
        ReloadUI()
        
    else
        if HolocronFrame:IsShown() then HolocronFrame:Hide() else HolocronFrame:Show() end
    end
end
