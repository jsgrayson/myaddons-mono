-- Core.lua - Main addon initialization and event handling

-- Create addon namespace
GoblinAI = {}
local addon = GoblinAI

-- Version info
addon.version = "1.0.0"
addon.isInitialized = false

-- Default settings
local defaultSettings = {
    enabled = true,
    autoScan = true,
    scanInterval = 300, -- 5 minutes
    maxSpendPerItem = 50000, -- 500 gold
    showMinimap = true,
    notificationSound = true
}

-- Initialize database
function addon:InitializeDB()
    if not GoblinAIDB then
        GoblinAIDB = {
            scans = {},
            characters = {},
            opportunities = {},
            settings = CopyTable(defaultSettings),
            lastUpdate = 0
        }
    end
    
    -- Ensure all tables exist
    GoblinAIDB.scans = GoblinAIDB.scans or {}
    GoblinAIDB.characters = GoblinAIDB.characters or {}
    GoblinAIDB.opportunities = GoblinAIDB.opportunities or {}
    GoblinAIDB.settings = GoblinAIDB.settings or CopyTable(defaultSettings)
end

-- Event frame
local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PLAYER_LOGOUT")
eventFrame:RegisterEvent("AUCTION_HOUSE_SHOW")
eventFrame:RegisterEvent("AUCTION_HOUSE_CLOSED")

-- Event handler
eventFrame:SetScript("OnEvent", function(self, event, ...)
    if event == "ADDON_LOADED" then
        local addonName = ...
        if addonName == "GoblinAI" then
            addon:OnAddonLoaded()
        end
    elseif event == "PLAYER_LOGIN" then
        addon:OnPlayerLogin()
    elseif event == "PLAYER_LOGOUT" then
        addon:OnPlayerLogout()
    elseif event == "AUCTION_HOUSE_SHOW" then
        addon:OnAuctionHouseOpened()
    elseif event == "AUCTION_HOUSE_CLOSED" then
        addon:OnAuctionHouseClosed()
    end
end)

-- Addon loaded
function addon:OnAddonLoaded()
    self:InitializeDB()
    print("|cFF00FF00Goblin AI|r v" .. self.version .. " loaded. Type /goblin for commands.")
end

-- Player login
function addon:OnPlayerLogin()
    -- Update character data
    if GoblinAI.CharacterData then
        GoblinAI.CharacterData:Update()
    end
    
    -- Load opportunities if available
    if GoblinAIDB.opportunities and #GoblinAIDB.opportunities > 0 then
        print("|cFF00FF00Goblin AI|r: " .. #GoblinAIDB.opportunities .. " opportunities loaded!")
    end
    
    self.isInitialized = true
end

-- Player logout
function addon:OnPlayerLogout()
    -- Data is automatically saved via SavedVariables
    GoblinAIDB.lastUpdate = time()
end

-- AH opened
function addon:OnAuctionHouseOpened()
    if GoblinAIDB.settings.autoScan and GoblinAI.Scanner then
        C_Timer.After(2, function()
            print("|cFF00FF00Goblin AI|r: Starting AH scan...")
            GoblinAI.Scanner:StartScan()
        end)
    end
end

-- AH closed
function addon:OnAuctionHouseClosed()
    if GoblinAI.Scanner then
        GoblinAI.Scanner:StopScan()
    end
end

-- Slash commands
SLASH_GOBLIN1 = "/goblin"
SLASH_GOBLIN2 = "/gai"
SlashCmdList["GOBLIN"] = function(msg)
    local cmd = msg:lower():trim()
    
    if cmd == "" or cmd == "help" then
        print("|cFF00FF00Goblin AI Commands:|r")
        print("  /goblin opportunities - Show flip opportunities")
        print("  /goblin scan - Scan auction house")
        print("  /goblin materials - Show material tracker")
        print("  /goblin crafting - Show crafting queue")
        print("  /goblin settings - Open settings")
        print("  /goblin export - Export scan data")
        
    elseif cmd == "opportunities" or cmd == "opp" then
        if GoblinAI.OpportunityFrame then
            GoblinAI.OpportunityFrame:Toggle()
        end
        
    elseif cmd == "scan" then
        if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
            print("|cFFFF0000Error:|r You must be at the auction house!")
        elseif GoblinAI.Scanner then
            GoblinAI.Scanner:StartScan()
        end
        
    elseif cmd == "materials" or cmd == "mats" then
        if GoblinAI.MaterialsFrame then
            GoblinAI.MaterialsFrame:Toggle()
        end
        
    elseif cmd == "crafting" or cmd == "craft" then
        if GoblinAI.CraftingQueue then
            GoblinAI.CraftingQueue:Toggle()
        end
        
    elseif cmd == "export" then
        print("|cFF00FF00Goblin AI|r: Scan data saved to SavedVariables.")
        print("File location: WTF/Account/YOURNAME/SavedVariables/GoblinAI.lua")
        print("Upload this file to your Goblin server for analysis.")
        
    elseif cmd == "settings" then
        print("|cFF00FF00Goblin AI Settings:|r")
        print("  Auto-scan: " .. tostring(GoblinAIDB.settings.autoScan))
        print("  Scan interval: " .. GoblinAIDB.settings.scanInterval .. "s")
        -- Settings are managed via the Web Portal and synced to SavedVariables.
        -- See backend/ui/templates/config.html
        
    else
        print("|cFFFF0000Unknown command.|r Type /goblin help for commands.")
    end
end

-- Utility: Get player identifier
function addon:GetPlayerID()
    return UnitName("player") .. "-" .. GetRealmName()
end

-- Utility: Format gold
function addon:FormatGold(copper)
    if not copper or copper == 0 then return "0g" end
    
    local gold = floor(copper / 10000)
    local silver = floor((copper % 10000) / 100)
    local copper = copper % 100
    
    if gold > 0 then
        return string.format("%dg %ds %dc", gold, silver, copper)
    elseif silver > 0 then
        return string.format("%ds %dc", silver, copper)
    else
        return string.format("%dc", copper)
    end
end

-- Utility: Format number with commas
function addon:FormatNumber(num)
    local formatted = tostring(num)
    while true do  
        formatted, k = string.gsub(formatted, "^(-?%d+)(%d%d%d)", '%1,%2')
        if k == 0 then break end
    end
    return formatted
end
