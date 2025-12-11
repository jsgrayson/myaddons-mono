local addonName, addonTable = ...
HolocronDB = HolocronDB or {}
local charList = {} -- cache for sorting

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
-- SNAPSHOT ENGINE
-- ============================================================================
local function SnapshotCurrentChar()
    local name = UnitName("player")
    local realm = GetRealmName()
    local key = name .. " - " .. realm
    
    local _, classFilename = UnitClass("player")
    
    HolocronDB[key] = {
        name = name,
        realm = realm,
        level = UnitLevel("player"),
        gold = GetMoney(),
        zone = GetZoneText(),
        class = classFilename,
        lastSeen = date("%Y-%m-%d %H:%M:%S")
    }
    print("|cff00ccffHolocron:|r Snapshot saved for " .. name)
end

-- ============================================================================
-- GRID DISPLAY LOGIC
-- ============================================================================
local function RebuildCharList()
    wipe(charList)
    local totalGold = 0
    
    for key, data in pairs(HolocronDB) do
        tinsert(charList, data)
        totalGold = totalGold + (data.gold or 0)
    end
    
    -- Sort by Level Descending, then Name
    table.sort(charList, function(a,b)
        if a.level ~= b.level then return a.level > b.level end
        return a.name < b.name
    end)
    
    -- Update Footer
    HolocronFrame.Content.Footer.TotalGold:SetText("Total Account Wealth: " .. FormatGold(totalGold))
end

function Holocron_UpdateGrid()
    local scrollFrame = HolocronFrame.Content.Scroll
    local buttons = scrollFrame.buttons
    local offset = HybridScrollFrame_GetOffset(scrollFrame)
    local numItems = #charList

    for i = 1, #buttons do
        local button = buttons[i]
        local index = offset + i
        
        if index <= numItems then
            local data = charList[index]
            button:Show()
            
            button.Name:SetText(data.name)
            
            -- Class Color
            if data.class then
                local color = C_ClassColor.GetClassColor(data.class)
                if color then button.Name:SetTextColor(color.r, color.g, color.b) end
            end
            
            button.Level:SetText(data.level)
            button.Zone:SetText(data.zone or "Unknown")
            button.Gold:SetText(FormatGold(data.gold or 0))
        else
            button:Hide()
        end
    end
    HybridScrollFrame_Update(scrollFrame, numItems * 20, scrollFrame:GetHeight())
end

-- ============================================================================
-- INIT
-- ============================================================================
local function OnEvent(self, event, ...)
    if event == "PLAYER_LOGIN" then
        SnapshotCurrentChar()
        
        -- Setup Scroll Frame
        local scrollFrame = HolocronFrame.Content.Scroll
        HybridScrollFrame_CreateButtons(scrollFrame, "HolocronCharRowTemplate")
        scrollFrame.update = Holocron_UpdateGrid
        
        RebuildCharList()
        Holocron_UpdateGrid()
        
    elseif event == "PLAYER_MONEY" or event == "PLAYER_LEVEL_UP" or event == "ZONE_CHANGED_NEW_AREA" then
        SnapshotCurrentChar()
        if HolocronFrame:IsShown() then
            RebuildCharList()
            Holocron_UpdateGrid()
        end
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PLAYER_MONEY")
eventFrame:RegisterEvent("PLAYER_LEVEL_UP")
eventFrame:RegisterEvent("ZONE_CHANGED_NEW_AREA")
eventFrame:SetScript("OnEvent", OnEvent)

SLASH_HOLOCRON1 = "/holocron"
SlashCmdList["HOLOCRON"] = function(msg)
    if HolocronFrame:IsShown() then HolocronFrame:Hide() else HolocronFrame:Show(); RebuildCharList(); Holocron_UpdateGrid() end
end
