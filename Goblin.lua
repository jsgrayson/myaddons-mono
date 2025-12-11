local addonName, addonTable = ...
GoblinDB = GoblinDB or {}
GoblinDB.history = GoblinDB.history or {}
GoblinDB.goldLog = GoblinDB.goldLog or {}

local lastGold = 0
local currentTab = 1
local auctionItems = {} -- Stores scan results

-- ============================================================================
-- FORMATTING
-- ============================================================================
local function FormatGold(amount)
    local gold = math.floor(amount / 10000)
    local silver = math.floor((amount % 10000) / 100)
    local copper = amount % 100
    local str = ""
    if gold > 0 then str = str .. "|cffffd700" .. gold .. "g|r " end
    if silver > 0 then str = str .. "|cffc7c7cf" .. silver .. "s|r " end
    str = str .. "|cffb87333" .. copper .. "c|r"
    return str
end

-- ============================================================================
-- DASHBOARD LOGIC
-- ============================================================================
local function UpdateDashboard()
    local currentGold = GetMoney()
    GoblinFrame.Content.Dashboard.GoldCard.Value:SetText(FormatGold(currentGold))
    
    local logString = ""
    for i = #GoblinDB.goldLog, math.max(1, #GoblinDB.goldLog - 20), -1 do
        logString = logString .. GoblinDB.goldLog[i] .. "\n"
    end
    GoblinFrame.Content.Dashboard.LedgerScroll.Child.LogText:SetText(logString)
    GoblinFrame.Content.Dashboard.LedgerScroll.Child.LogText:SetWidth(550)
end

local function OnMoneyChange()
    local currentGold = GetMoney()
    local diff = currentGold - lastGold
    lastGold = currentGold
    if diff == 0 then return end
    
    local entry = (diff > 0) and "|cff00ff00[IN]|r " .. FormatGold(diff) or "|cffff0000[OUT]|r " .. FormatGold(math.abs(diff))
    entry = date("%H:%M:%S") .. " " .. entry
    table.insert(GoblinDB.goldLog, entry)
    UpdateDashboard()
end

-- ============================================================================
-- AUCTION LOGIC (The TSM Part)
-- ============================================================================

local function RunPostScan()
    -- SIMULATED SCAN: In a real addon, this would check Bag items against AH prices.
    -- For v0.1, we will scan your bags for Trade Goods and mock a price.
    
    wipe(auctionItems)
    print("|cffb87333Goblin:|r Scanning Bags for auctionables...")
    
    for bag = 0, 4 do
        for slot = 1, C_Container.GetContainerNumSlots(bag) do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info then
                local _, _, rarity, _, _, classType = GetItemInfo(info.itemID)
                -- If it's trade goods or better than poor quality
                if rarity and rarity > 1 then
                    -- Mock pricing logic (random gold value for demo)
                    local mockPrice = math.random(1000, 50000) 
                    
                    tinsert(auctionItems, {
                        name = info.itemName,
                        icon = info.iconFileID,
                        count = info.stackCount,
                        price = mockPrice
                    })
                end
            end
        end
    end
    
    Goblin_UpdateAuctionList()
    print("|cffb87333Goblin:|r Scan Complete. Found " .. #auctionItems .. " items.")
end

function Goblin_UpdateAuctionList()
    local scrollFrame = GoblinFrame.Content.Auctioning.ListScroll
    local buttons = scrollFrame.buttons 
    local offset = HybridScrollFrame_GetOffset(scrollFrame) 
    local numItems = #auctionItems

    for i = 1, #buttons do
        local button = buttons[i]
        local index = offset + i 
        
        if index <= numItems then
            local item = auctionItems[index]
            button:Show()
            button.Name:SetText(item.name)
            button.Icon:SetTexture(item.icon)
            button.Qty:SetText("x" .. item.count)
            button.Price:SetText(FormatGold(item.price))
        else
            button:Hide()
        end
    end
    HybridScrollFrame_Update(scrollFrame, numItems * 20, scrollFrame:GetHeight())
end

-- ============================================================================
-- NAVIGATION
-- ============================================================================
local navItems = {
    {name="Dashboard", icon="Interface\\Icons\\inv_misc_coin_02", frame="Dashboard"},
    {name="Auctioning", icon="Interface\\Icons\\inv_misc_hammer_01", frame="Auctioning"},
    {name="Ledger", icon="Interface\\Icons\\inv_misc_book_11", frame="Dashboard"}, -- Placeholder
    {name="Crafting", icon="Interface\\Icons\\trade_engineering", frame="Dashboard"}, -- Placeholder
}

local function SwitchTab(id)
    currentTab = id
    
    -- Hide all content frames first
    GoblinFrame.Content.Dashboard:Hide()
    GoblinFrame.Content.Auctioning:Hide()
    
    -- Show the selected one
    local frameName = navItems[id].frame
    GoblinFrame.Content[frameName]:Show()
    
    print("Goblin: Viewing " .. navItems[id].name)
end

local function InitNav()
    local sb = GoblinFrame.Sidebar
    for i, data in ipairs(navItems) do
        local btn = sb["Nav"..i]
        if btn then
            btn.Label:SetText(data.name)
            btn.Icon:SetTexture(data.icon)
            btn.id = i
        end
    end
end

function Goblin_NavClick(self)
    SwitchTab(self.id)
end

-- ============================================================================
-- INIT
-- ============================================================================
local function OnEvent(self, event, ...)
    if event == "PLAYER_LOGIN" then
        lastGold = GetMoney()
        InitNav()
        UpdateDashboard()
        
        -- Setup Hybrid Scroll for Auctioning
        local scrollFrame = GoblinFrame.Content.Auctioning.ListScroll
        HybridScrollFrame_CreateButtons(scrollFrame, "GoblinAuctionRowTemplate")
        scrollFrame.update = Goblin_UpdateAuctionList
        
        -- Setup Scan Button
        GoblinFrame.Content.Auctioning.ScanButton:SetScript("OnClick", RunPostScan)
        
    elseif event == "PLAYER_MONEY" then
        OnMoneyChange()
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PLAYER_MONEY")
eventFrame:SetScript("OnEvent", OnEvent)

SLASH_GOBLIN1 = "/goblin"
SlashCmdList["GOBLIN"] = function(msg)
    if GoblinFrame:IsShown() then GoblinFrame:Hide() else GoblinFrame:Show() end
end
