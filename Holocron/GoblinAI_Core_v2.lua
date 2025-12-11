-- Core.lua - GoblinAI v2.0 - TSM Replacement with AI Intelligence
-- Author: Holocron
-- Modern UI framework with full auction house automation

print("GoblinAI: Loading v2.0...")

-- ============================================================================
-- Namespace & Initialization
-- ============================================================================

GoblinAI = GoblinAI or {}
local addon = GoblinAI

addon.version = "2.0.0"
addon.isInitialized = false

-- ============================================================================
-- Style System (PetWeaver-inspired)
-- ============================================================================

local theme, bgKey = Holocron:GetTheme("GoblinAI")
local LSM = LibStub("LibSharedMedia-3.0")
local bgFile = LSM and LSM:Fetch("background", bgKey) or "Interface\\DialogFrame\\UI-DialogBox-Background"
local borderFile = LSM and LSM:Fetch("border", "Holocron Glow") or "Interface\\DialogFrame\\UI-DialogBox-Border"

local STYLE = {
    colors = {
        background = {0, 0, 0, 0.9},
        border = {theme.r, theme.g, theme.b, 1}, -- Cyber Green
        tabActive = {theme.r, theme.g, theme.b, 1},
        tabInactive = {0.1, 0.1, 0.1, 0.8},
        header = {theme.r, theme.g, theme.b, 1},
        text = {1, 1, 1, 1},
        profit = {0, 1, 0, 1},
        loss = {1, 0, 0, 1},
        warning = {1, 0.5, 0, 1},
    },
    fonts = {
        title = "GameFontNormalHuge",
        header = "GameFontNormalLarge",
        text = "GameFontHighlight",
        small = "GameFontNormalSmall",
    }
}

-- ============================================================================
-- Saved Variables
-- ============================================================================

local defaultSettings = {
    enabled = true,
    autoScan = true,
    scanInterval = 300,
    maxSpendPerItem = 50000,
    showMinimap = true,
    notificationSound = true,
    useBackend = false,
    framePos = {},
    currentTab = "Dashboard",
}

function addon:InitializeDB()
    if not GoblinAIDB then
        GoblinAIDB = {
            scans = {},
            characters = {},
            opportunities = {},
            groups = {},
            operations = {},
            ledger = {},
            shoppingLists = {},
            settings = {},
            lastUpdate = 0,
        }
    end
    
    -- Merge with defaults
    for k, v in pairs(defaultSettings) do
        if GoblinAIDB.settings[k] == nil then
            GoblinAIDB.settings[k] = v
        end
    end
    
    -- Ensure all tables exist
    GoblinAIDB.scans = GoblinAIDB.scans or {}
    GoblinAIDB.characters = GoblinAIDB.characters or {}
    GoblinAIDB.opportunities = GoblinAIDB.opportunities or {}
    GoblinAIDB.groups = GoblinAIDB.groups or {}
    GoblinAIDB.operations = GoblinAIDB.operations or {}
    GoblinAIDB.ledger = GoblinAIDB.ledger or {}
    GoblinAIDB.shoppingLists = GoblinAIDB.shoppingLists or {}
end

-- ============================================================================
-- Utility Functions
-- ============================================================================

function addon:CreateStyledButton(parent, text, width, height)
    local btn = CreateFrame("Button", nil, parent, "UIPanelButtonTemplate")
    btn:SetSize(width or 100, height or 25)
    btn:SetText(text)
    return btn
end

function addon:CreateScrollFrame(parent, width, height)
    local scroll = CreateFrame("ScrollFrame", nil, parent, "UIPanelScrollFrameTemplate")
    scroll:SetSize(width, height)
    
    local content = CreateFrame("Frame", nil, scroll)
    content:SetSize(width - 20, 1)
    scroll:SetScrollChild(content)
    
    scroll.content = content
    return scroll
end

function addon:GetPlayerID()
    return UnitName("player") .. "-" .. GetRealmName()
end

function addon:FormatGold(copper)
    if not copper or copper == 0 then return "|cFFFFFFFF0|cFFEDA55Fg|r" end
    
    local gold = floor(copper / 10000)
    local silver = floor((copper % 10000) / 100)
    local remaining = copper % 100
    
    local result = ""
    if gold > 0 then
        result = result .. "|cFFFFD700" .. addon:FormatNumber(gold) .. "|cFFEDA55Fg|r "
    end
    if silver > 0 or gold > 0 then
        result = result .. "|cFFC0C0C0" .. silver .. "|cFFEDA55Fs|r "
    end
    if remaining > 0 or (gold == 0 and silver == 0) then
        result = result .. "|cFFCD7F32" .. remaining .. "|cFFEDA55Fc|r"
    end
    
    return result
end

function addon:FormatNumber(num)
    local formatted = tostring(num)
    while true do  
        formatted, k = string.gsub(formatted, "^(-?%d+)(%d%d%d)", '%1,%2')
        if k == 0 then break end
    end
    return formatted
end

function addon:FormatPercent(value)
    return string.format("%.1f%%", value * 100)
end

-- ============================================================================
-- Main Frame & Tab System
-- ============================================================================

local MainFrame = CreateFrame("Frame", "GoblinAIMainFrame", UIParent, "BackdropTemplate")
MainFrame:SetSize(700, 600)
MainFrame:SetPoint("CENTER")
MainFrame:SetBackdrop({
    bgFile = bgFile,
    edgeFile = borderFile,
    tile = false, tileSize = 0, edgeSize = 16,
    insets = { left = 4, right = 4, top = 4, bottom = 4 }
})
MainFrame:SetBackdropColor(1, 1, 1, 1) -- Texture provides color
MainFrame:SetBackdropBorderColor(theme.r, theme.g, theme.b, 1)
MainFrame:EnableMouse(true)
MainFrame:SetMovable(true)
MainFrame:RegisterForDrag("LeftButton")
MainFrame:SetScript("OnDragStart", MainFrame.StartMoving)
MainFrame:SetScript("OnDragStop", function(self)
    self:StopMovingOrSizing()
    local point, _, relativePoint, x, y = self:GetPoint()
    GoblinAIDB.settings.framePos = {point, relativePoint, x, y}
end)
MainFrame:Hide()

-- Restore saved position
if GoblinAIDB and GoblinAIDB.settings and GoblinAIDB.settings.framePos[1] then
    MainFrame:ClearAllPoints()
    MainFrame:SetPoint(unpack(GoblinAIDB.settings.framePos))
end

-- Close Button
local closeBtn = CreateFrame("Button", nil, MainFrame, "UIPanelCloseButton")
closeBtn:SetPoint("TOPRIGHT", -5, -5)

-- Title
local title = MainFrame:CreateFontString(nil, "OVERLAY", STYLE.fonts.title)
title:SetPoint("TOP", 0, -15)
title:SetText("Goblin AI")
title:SetTextColor(unpack(STYLE.colors.header))

-- Version
local versionText = MainFrame:CreateFontString(nil, "OVERLAY", STYLE.fonts.small)
versionText:SetPoint("TOP", title, "BOTTOM", 0, -2)
versionText:SetText("v2.0 - TSM Replacement")
versionText:SetTextColor(0.7, 0.7, 0.7, 1)

-- ============================================================================
-- Tab System
-- ============================================================================

local Tabs = {}
local TabContent = {}
local ActiveTab = nil

local function CreateTab(name, index)
    local tab = CreateFrame("Button", nil, MainFrame)
    tab:SetSize(110, 28)
    tab:SetPoint("TOPLEFT", 10 + (index * 115), -60)
    
    tab.bg = tab:CreateTexture(nil, "BACKGROUND")
    tab.bg:SetAllPoints()
    tab.bg:SetColorTexture(unpack(STYLE.colors.tabInactive))
    
    tab.text = tab:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
    tab.text:SetPoint("CENTER")
    tab.text:SetText(name)
    
    tab.name = name
    tab:SetScript("OnClick", function()
        GoblinAI_SwitchTab(name)
    end)
    
    Tabs[name] = tab
    return tab
end

function GoblinAI_SwitchTab(tabName)
    -- Deactivate all tabs
    for name, tab in pairs(Tabs) do
        tab.bg:SetColorTexture(unpack(STYLE.colors.tabInactive))
        if TabContent[name] then
            TabContent[name]:Hide()
        end
    end
    
    -- Activate selected tab
    if Tabs[tabName] then
        Tabs[tabName].bg:SetColorTexture(unpack(STYLE.colors.tabActive))
        if TabContent[tabName] then
            TabContent[tabName]:Show()
        end
        ActiveTab = tabName
        if GoblinAIDB and GoblinAIDB.settings then
            GoblinAIDB.settings.currentTab = tabName
        end
    end
end

-- Create tabs
CreateTab("Dashboard", 0)
CreateTab("Shopping", 1)
CreateTab("Posting", 2)
CreateTab("Crafting", 3)
CreateTab("Ledger", 4)
CreateTab("Settings", 5)

-- Save reference
addon.MainFrame = MainFrame
addon.SwitchTab = GoblinAI_SwitchTab

-- ============================================================================
-- Dashboard Tab
-- ============================================================================

local DashboardTab = CreateFrame("Frame", nil, MainFrame)
DashboardTab:SetPoint("TOPLEFT", 15, -95)
DashboardTab:SetPoint("BOTTOMRIGHT", -15, 15)
TabContent["Dashboard"] = DashboardTab

local dashTitle = DashboardTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
dashTitle:SetPoint("TOP", 0, -10)
dashTitle:SetText("Portfolio Overview")
dashTitle:SetTextColor(unpack(STYLE.colors.header))

-- Portfolio value card
local portfolioCard = CreateFrame("Frame", nil, DashboardTab, "BackdropTemplate")
portfolioCard:SetSize(320, 100)
portfolioCard:SetPoint("TOP", 0, -40)
portfolioCard:SetBackdrop({
    bgFile = "Interface\\Buttons\\WHITE8X8",
    edgeFile = "Interface\\Buttons\\WHITE8X8",
    edgeSize = 1,
})
portfolioCard:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
portfolioCard:SetBackdropBorderColor(unpack(STYLE.colors.header))

local portfolioLabel = portfolioCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
portfolioLabel:SetPoint("TOP", 0, -10)
portfolioLabel:SetText("Total Portfolio Value")

local portfolioValue = portfolioCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.title)
portfolioValue:SetPoint("CENTER", 0, -5)
portfolioValue:SetText(addon:FormatGold(0))

-- Today's profit card
local profitCard = CreateFrame("Frame", nil, DashboardTab, "BackdropTemplate")
profitCard:SetSize(150, 80)
profitCard:SetPoint("TOPLEFT", 20, -160)
profitCard:SetBackdrop({
    bgFile = "Interface\\Buttons\\WHITE8X8",
    edgeFile = "Interface\\Buttons\\WHITE8X8",
    edgeSize = 1,
})
profitCard:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
profitCard:SetBackdropBorderColor(0, 1, 0, 1)

local profitLabel = profitCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.small)
profitLabel:SetPoint("TOP", 0, -8)
profitLabel:SetText("Today's Profit")

local profitValue = profitCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
profitValue:SetPoint("CENTER", 0, -5)
profitValue:SetText(addon:FormatGold(0))
profitValue:SetTextColor(0, 1, 0, 1)

-- Active auctions card
local auctionsCard = CreateFrame("Frame", nil, DashboardTab, "BackdropTemplate")
auctionsCard:SetSize(150, 80)
auctionsCard:SetPoint("LEFT", profitCard, "RIGHT", 10, 0)
auctionsCard:SetBackdrop({
    bgFile = "Interface\\Buttons\\WHITE8X8",
    edgeFile = "Interface\\Buttons\\WHITE8X8",
    edgeSize = 1,
})
auctionsCard:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
auctionsCard:SetBackdropBorderColor(unpack(STYLE.colors.header))

local auctionsLabel = auctionsCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.small)
auctionsLabel:SetPoint("TOP", 0, -8)
auctionsLabel:SetText("Active Auctions")

local auctionsValue = auctionsCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.title)
auctionsValue:SetPoint("CENTER", 0, -5)
auctionsValue:SetText("0")

-- Pending sales card
local salesCard = CreateFrame("Frame", nil, DashboardTab, "BackdropTemplate")
salesCard:SetSize(150, 80)
salesCard:SetPoint("LEFT", auctionsCard, "RIGHT", 10, 0)
salesCard:SetBackdrop({
    bgFile = "Interface\\Buttons\\WHITE8X8",
    edgeFile = "Interface\\Buttons\\WHITE8X8",
    edgeSize = 1,
})
salesCard:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
salesCard:SetBackdropBorderColor(unpack(STYLE.colors.header))

local salesLabel = salesCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.small)
salesLabel:SetPoint("TOP", 0, -8)
salesLabel:SetText("Pending Sales")

local salesValue = salesCard:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
salesValue:SetPoint("CENTER", 0, -5)
salesValue:SetText(addon:FormatGold(0))

-- Quick actions
local quickActionsLabel = DashboardTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
quickActionsLabel:SetPoint("TOPLEFT", 20, -260)
quickActionsLabel:SetText("Quick Actions")
quickActionsLabel:SetTextColor(unpack(STYLE.colors.header))

local scanBtn = addon:CreateStyledButton(DashboardTab, "Scan AH", 120, 30)
scanBtn:SetPoint("TOPLEFT", 20, -285)
scanBtn:SetScript("OnClick", function()
    if AuctionHouseFrame and AuctionHouseFrame:IsShown() then
        if GoblinAI.Scanner then
            GoblinAI.Scanner:StartScan()
        end
    else
        print("|cFFFF0000Goblin AI:|r You must be at the auction house!")
    end
end)

local oppBtn = addon:CreateStyledButton(DashboardTab, "View Opportunities", 150, 30)
oppBtn:SetPoint("LEFT", scanBtn, "RIGHT", 10, 0)
oppBtn:SetScript("OnClick", function()
    GoblinAI_SwitchTab("Shopping")
end)

local postBtn = addon:CreateStyledButton(DashboardTab, "Post Auctions", 120, 30)
postBtn:SetPoint("LEFT", oppBtn, "RIGHT", 10, 0)
postBtn:SetScript("OnClick", function()
    GoblinAI_SwitchTab("Posting")
end)

-- ============================================================================
-- Shopping Tab (Placeholder)
-- ============================================================================

local ShoppingTab = CreateFrame("Frame", nil, MainFrame)
ShoppingTab:SetPoint("TOPLEFT", 15, -95)
ShoppingTab:SetPoint("BOTTOMRIGHT", -15, 15)
TabContent["Shopping"] = ShoppingTab

local shopTitle = ShoppingTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
shopTitle:SetPoint("TOP", 0, -10)
shopTitle:SetText("Shopping & Deals")
shopTitle:SetTextColor(unpack(STYLE.colors.header))

local shopPlaceholder = ShoppingTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
shopPlaceholder:SetPoint("CENTER")
shopPlaceholder:SetText("Shopping features coming in Phase 3!")

-- ================================================================ ============
-- Posting Tab (Placeholder)
-- ============================================================================

local PostingTab = CreateFrame("Frame", nil, MainFrame)
PostingTab:SetPoint("TOPLEFT", 15, -95)
PostingTab:SetPoint("BOTTOMRIGHT", -15, 15)
TabContent["Posting"] = PostingTab

local postTitle = PostingTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
postTitle:SetPoint("TOP", 0, -10)
postTitle:SetText("Groups & Posting")
postTitle:SetTextColor(unpack(STYLE.colors.header))

local postPlaceholder = PostingTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
postPlaceholder:SetPoint("CENTER")
postPlaceholder:SetText("Posting features coming in Phase 4!")

-- ============================================================================
-- Crafting Tab (Placeholder)
-- ============================================================================

local CraftingTab = CreateFrame("Frame", nil, MainFrame)
CraftingTab:SetPoint("TOPLEFT", 15, -95)
CraftingTab:SetPoint("BOTTOMRIGHT", -15, 15)
TabContent["Crafting"] = CraftingTab

local craftTitle = CraftingTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
craftTitle:SetPoint("TOP", 0, -10)
craftTitle:SetText("Crafting Profitability")
craftTitle:SetTextColor(unpack(STYLE.colors.header))

local craftPlaceholder = CraftingTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
craftPlaceholder:SetPoint("CENTER")
craftPlaceholder:SetText("Crafting features coming in Phase 5!")

-- ============================================================================
-- Ledger Tab (Placeholder)
-- ============================================================================

local LedgerTab = CreateFrame("Frame", nil, MainFrame)
LedgerTab:SetPoint("TOPLEFT", 15, -95)
LedgerTab:SetPoint("BOTTOMRIGHT", -15, 15)
TabContent["Ledger"] = LedgerTab

local ledgerTitle = LedgerTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
ledgerTitle:SetPoint("TOP", 0, -10)
ledgerTitle:SetText("Sales & Purchase History")
ledgerTitle:SetTextColor(unpack(STYLE.colors.header))

local ledgerPlaceholder = LedgerTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
ledgerPlaceholder:SetPoint("CENTER")
ledgerPlaceholder:SetText("Ledger features coming in Phase 7!")

-- ============================================================================
-- Settings Tab
-- ============================================================================

local SettingsTab = CreateFrame("Frame", nil, MainFrame)
SettingsTab:SetPoint("TOPLEFT", 15, -95)
SettingsTab:SetPoint("BOTTOMRIGHT", -15, 15)
TabContent["Settings"] = SettingsTab

local settingsTitle = SettingsTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
settingsTitle:SetPoint("TOP", 0, -10)
settingsTitle:SetText("Settings")
settingsTitle:SetTextColor(unpack(STYLE.colors.header))

-- Auto-scan checkbox
local autoScanCheck = CreateFrame("CheckButton", nil, SettingsTab, "UICheckButtonTemplate")
autoScanCheck:SetPoint("TOPLEFT", 10, -40)
autoScanCheck:SetChecked(GoblinAIDB.settings.autoScan)
autoScanCheck.text = autoScanCheck:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
autoScanCheck.text:SetPoint("LEFT", autoScanCheck, "RIGHT", 5, 0)
autoScanCheck.text:SetText("Auto-scan on AH open")
autoScanCheck:SetScript("OnClick", function(self)
    GoblinAIDB.settings.autoScan = self:GetChecked()
end)

-- Backend toggle
local backendCheck = CreateFrame("CheckButton", nil, SettingsTab, "UICheckButtonTemplate")
backendCheck:SetPoint("TOPLEFT", 10, -70)
backendCheck:SetChecked(GoblinAIDB.settings.useBackend)
backendCheck.text = backendCheck:CreateFontString(nil, "OVERLAY", STYLE.fonts.text)
backendCheck.text:SetPoint("LEFT", backendCheck, "RIGHT", 5, 0)
backendCheck.text:SetText("Enable AI Backend (Requires server running)")
backendCheck:SetScript("OnClick", function(self)
    GoblinAIDB.settings.useBackend = self:GetChecked()
    print("Goblin AI: Backend " .. (GoblinAIDB.settings.useBackend and "enabled" or "disabled"))
end)

-- Info section
local infoHeader = SettingsTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.header)
infoHeader:SetPoint("TOPLEFT", 10, -120)
infoHeader:SetText("About Goblin AI")
infoHeader:SetTextColor(unpack(STYLE.colors.header))

local infoText = SettingsTab:CreateFontString(nil, "OVERLAY", STYLE.fonts.small)
infoText:SetPoint("TOPLEFT", 10, -145)
infoText:SetText("Version: 2.0.0\n\nA complete TradeSkillMaster replacement\nwith AI-powered market intelligence.\n\nFeatures:\n• Real-time AH scanning\n• AI deal detection\n• Crafting profitability\n• Portfolio tracking\n• Automated posting\n\nby Holocron")
infoText:SetWidth(650)
infoText:SetJustifyH("LEFT")

-- ============================================================================
-- Event Handlers
-- ============================================================================

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PLAYER_LOGOUT")
eventFrame:RegisterEvent("AUCTION_HOUSE_SHOW")
eventFrame:RegisterEvent("AUCTION_HOUSE_CLOSED")

eventFrame:SetScript("OnEvent", function(self, event, arg1)
    if event == "ADDON_LOADED" and arg1 == "GoblinAI" then
        addon:InitializeDB()
        print("|cFFFFD700Goblin AI|r v" .. addon.version .. " loaded. Type /goblin to open.")
        
    elseif event == "PLAYER_LOGIN" then
        -- Update character data
        if GoblinAI.CharacterData then
            GoblinAI.CharacterData:Update()
        end
        
        addon.isInitialized = true
        
    elseif event == "PLAYER_LOGOUT" then
        GoblinAIDB.lastUpdate = time()
        
    elseif event == "AUCTION_HOUSE_SHOW" then
        if GoblinAIDB.settings.autoScan and GoblinAI.Scanner then
            C_Timer.After(2, function()
                print("|cFFFFD700Goblin AI|r: Starting AH scan...")
                GoblinAI.Scanner:StartScan()
            end)
        end
        
    elseif event == "AUCTION_HOUSE_CLOSED" then
        if GoblinAI.Scanner then
            GoblinAI.Scanner:StopScan()
        end
    end
end)

-- ============================================================================
-- Slash Commands
-- ============================================================================

SLASH_GOBLIN1 = "/goblin"
SLASH_GOBLIN2 = "/gai"

SlashCmdList["GOBLIN"] = function(msg)
    local cmd = msg:lower():trim()
    
    if cmd == "" or cmd == "show" then
        MainFrame:Show()
        GoblinAI_SwitchTab(GoblinAIDB.settings.currentTab or "Dashboard")
        
    elseif cmd == "hide" then
        MainFrame:Hide()
        
    elseif cmd == "scan" then
        if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
            print("|cFFFF0000Error:|r You must be at the auction house!")
        elseif GoblinAI.Scanner then
            GoblinAI.Scanner:StartScan()
        end
        
    else
        if MainFrame:IsShown() then
            MainFrame:Hide()
        else
            MainFrame:Show()
            GoblinAI_SwitchTab(GoblinAIDB.settings.currentTab or "Dashboard")
        end
    end
end

-- ============================================================================
-- Initialization
-- ============================================================================

GoblinAI_SwitchTab(defaultSettings.currentTab)

print("|cFFFFD700Goblin AI|r: Core loaded - Modern UI Framework active")
