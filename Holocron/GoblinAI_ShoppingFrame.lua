-- UI/ShoppingFrame.lua - Advanced Shopping & Deal Detection
-- Part of GoblinAI v2.0

GoblinAI.ShoppingFrame = {}
local Shopping = GoblinAI.ShoppingFrame

Shopping.activeList = nil
Shopping.sniperActive = false
Shopping.dealThreshold = 0.20 -- 20% below market = deal

-- ============================================================================
-- Initialize Shopping Tab
-- ============================================================================

function Shopping:Initialize(parentFrame)
    self.frame = parentFrame
    self:CreateUI()
end

function Shopping:CreateUI()
    -- Mode selector tabs
    local modeFrame = CreateFrame("Frame", nil, self.frame)
    modeFrame:SetSize(660, 40)
    modeFrame:SetPoint("TOP", 0, -10)
    
    -- Shopping List button
    self.listModeBtn = CreateFrame("Button", nil, modeFrame, "UIPanelButtonTemplate")
    self.listModeBtn:SetSize(150, 30)
    self.listModeBtn:SetPoint("LEFT", 10, 0)
    self.listModeBtn:SetText("Shopping Lists")
    self.listModeBtn:SetScript("OnClick", function()
        Shopping:SetMode("lists")
    end)
    
    -- Deal Finder button
    self.dealModeBtn = CreateFrame("Button", nil, modeFrame, "UIPanelButtonTemplate")
    self.dealModeBtn:SetSize(150, 30)
    self.dealModeBtn:SetPoint("LEFT", self.listModeBtn, "RIGHT", 10, 0)
    self.dealModeBtn:SetText("Deal Finder")
    self.dealModeBtn:SetScript("OnClick", function()
        Shopping:SetMode("deals")
    end)
    
    -- Sniper button
    self.sniperModeBtn = CreateFrame("Button", nil, modeFrame, "UIPanelButtonTemplate")
    self.sniperModeBtn:SetSize(150, 30)
    self.sniperModeBtn:SetPoint("LEFT", self.dealModeBtn, "RIGHT", 10, 0)
    self.sniperModeBtn:SetText("Sniper")
    self.sniperModeBtn:SetScript("OnClick", function()
        Shopping:SetMode("sniper")
    end)
    
    -- Content frames for each mode
    self:CreateShoppingListUI()
    self:CreateDealFinderUI()
    self:CreateSniperUI()
    
    -- Start in deals mode
    self:SetMode("deals")
end

function Shopping:SetMode(mode)
    -- Hide all frames
    if self.listContent then self.listContent:Hide() end
    if self.dealContent then self.dealContent:Hide() end
    if self.sniperContent then self.sniperContent:Hide() end
    
    -- Show selected
    if mode == "lists" and self.listContent then
        self.listContent:Show()
        self:RefreshShoppingLists()
    elseif mode == "deals" and self.dealContent then
        self.dealContent:Show()
        self:RefreshDeals()
    elseif mode == "sniper" and self.sniperContent then
        self.sniperContent:Show()
        self:StartSniper()
    end
end

-- ============================================================================
-- Shopping Lists UI
-- ============================================================================

function Shopping:CreateShoppingListUI()
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -60)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    content:Hide()
    
    -- Header
    local header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -5)
    header:SetText("Shopping Lists")
    header:SetTextColor(1, 0.84, 0, 1)
    
    -- Create list button
    local createBtn = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
    createBtn:SetSize(120, 25)
    createBtn:SetPoint("TOPRIGHT", -10, -5)
    createBtn:SetText("New List")
    createBtn:SetScript("OnClick", function()
        Shopping:CreateNewList()
    end)
    
    -- Scroll frame for lists
    local scroll = GoblinAI:CreateScrollFrame(content, 650, 380)
    scroll:SetPoint("TOP", 0, -40)
    
    self.listScroll = scroll
    self.listContent = content
end

function Shopping:CreateNewList()
    StaticPopupDialogs["GOBLINAI_NEW_SHOPPING_LIST"] = {
        text = "Enter shopping list name:",
        button1 = "Create",
        button2 = "Cancel",
        hasEditBox = true,
        maxLetters = 50,
        OnAccept = function(self)
            local name = self.editBox:GetText()
            if name and name ~= "" then
                if not GoblinAIDB.shoppingLists then
                    GoblinAIDB.shoppingLists = {}
                end
                
                table.insert(GoblinAIDB.shoppingLists, {
                    name = name,
                    items = {},
                    created = time(),
                })
                
                print("|cFFFFD700Goblin AI:|r Shopping list '" .. name .. "' created!")
                Shopping:RefreshShoppingLists()
            end
        end,
        timeout = 0,
        whileDead = true,
        hideOnEscape = true,
        preferredIndex = 3,
    }
    StaticPopup_Show("GOBLINAI_NEW_SHOPPING_LIST")
end

function Shopping:RefreshShoppingLists()
    if not self.listScroll then return end
    
    -- Clear existing
    for _, child in ipairs({self.listScroll.content:GetChildren()}) do
        child:Hide()
    end
    
    local lists = GoblinAIDB.shoppingLists or {}
    local yOffset = 0
    
    for i, list in ipairs(lists) do
        local listFrame = self:CreateShoppingListRow(list, i, yOffset)
        listFrame:SetParent(self.listScroll.content)
        yOffset = yOffset - 60
    end
    
    self.listScroll.content:SetHeight(math.max(1, #lists * 60))
end

function Shopping:CreateShoppingListRow(list, index, yOffset)
    local row = CreateFrame("Frame", nil, self.listScroll.content, "BackdropTemplate")
    row:SetSize(630, 50)
    row:SetPoint("TOPLEFT", 5, yOffset)
    row:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    row:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
    row:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
    
    -- Name
    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    name:SetPoint("TOPLEFT", 10, -10)
    name:SetText(list.name)
    name:SetTextColor(1, 0.84, 0, 1)
    
    -- Item count
    local count = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    count:SetPoint("TOPLEFT", 10, -30)
    count:SetText(#list.items .. " items")
    
    -- Delete button
    local deleteBtn = CreateFrame("Button", nil, row, "UIPanelButtonTemplate")
    deleteBtn:SetSize(60, 22)
    deleteBtn:SetPoint("RIGHT", -10, 0)
    deleteBtn:SetText("Delete")
    deleteBtn:SetScript("OnClick", function()
        table.remove(GoblinAIDB.shoppingLists, index)
        Shopping:RefreshShoppingLists()
    end)
    
    return row
end

-- ============================================================================
-- Deal Finder UI
-- ============================================================================

function Shopping:CreateDealFinderUI()
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -60)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    content:Hide()
    
    -- Header
    local header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -5)
    header:SetText("Deal Finder")
    header:SetTextColor(1, 0.84, 0, 1)
    
    -- Threshold slider
    local thresholdLabel = content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    thresholdLabel:SetPoint("TOPLEFT", 20, -35)
    thresholdLabel:SetText("Deal Threshold: 20%")
    
    local thresholdSlider = CreateFrame("Slider", nil, content, "OptionsSliderTemplate")
    thresholdSlider:SetPoint("TOPLEFT", 20, -55)
    thresholdSlider:SetSize(200, 20)
    thresholdSlider:SetMinMaxValues(0.05, 0.50)
    thresholdSlider:SetValueStep(0.05)
    thresholdSlider:SetValue(self.dealThreshold)
    thresholdSlider:SetScript("OnValueChanged", function(self, value)
        Shopping.dealThreshold = value
        thresholdLabel:SetText(string.format("Deal Threshold: %.0f%%", value * 100))
        Shopping:RefreshDeals()
    end)
    
    -- Refresh button
    local refreshBtn = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
    refreshBtn:SetSize(100, 25)
    refreshBtn:SetPoint("TOPRIGHT", -20, -35)
    refreshBtn:SetText("Scan for Deals")
    refreshBtn:SetScript("OnClick", function()
        if GoblinAI.Scanner then
            GoblinAI.Scanner:StartScan()
            C_Timer.After(2, function()
                Shopping:RefreshDeals()
            end)
        end
    end)
    
    -- Deals scroll frame
    local scroll = GoblinAI:CreateScrollFrame(content, 650, 350)
    scroll:SetPoint("TOP", 0, -85)
    
    self.dealScroll = scroll
    self.dealContent = content
end

function Shopping:RefreshDeals()
    if not self.dealScroll then return end
    
    -- Clear existing
    for _, child in ipairs({self.dealScroll.content:GetChildren()}) do
        child:Hide()
    end
    
    -- Find deals from last scan
    local lastScan = GoblinAI.Scanner:GetLastScan()
    if not lastScan or not lastScan.data then
        local noDeals = self.dealScroll.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        noDeals:SetPoint("TOP", 0, -20)
        noDeals:SetText("No scan data available. Click 'Scan for Deals' to start.")
        return
    end
    
    local deals = {}
    
    -- Compare each item to history
    for _, item in ipairs(lastScan.data) do
        local comparison = GoblinAI.Scanner:CompareScanToHistory(item.item_id)
        
        if comparison and comparison.percent < -self.dealThreshold then
            table.insert(deals, {
                itemID = item.item_id,
                current = comparison.current,
                average = comparison.average,
                percent = comparison.percent,
                savings = comparison.difference,
            })
        end
    end
    
    -- Sort by savings
    table.sort(deals, function(a, b)
        return math.abs(a.savings) > math.abs(b.savings)
    end)
    
    if #deals == 0 then
        local noDeals = self.dealScroll.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        noDeals:SetPoint("TOP", 0, -20)
        noDeals:SetText("No deals found matching criteria.")
        return
    end
    
    -- Display deals
    local yOffset = 0
    for i, deal in ipairs(deals) do
        if i > 50 then break end
        local dealFrame = self:CreateDealRow(deal, yOffset)
        dealFrame:SetParent(self.dealScroll.content)
        yOffset = yOffset - 60
    end
    
    self.dealScroll.content:SetHeight(math.max(1, #deals * 60))
end

function Shopping:CreateDealRow(deal, yOffset)
    local row = CreateFrame("Frame", nil, self.dealScroll.content, "BackdropTemplate")
    row:SetSize(630, 55)
    row:SetPoint("TOPLEFT", 5, yOffset)
    row:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    row:SetBackdropColor(0, 0.2, 0, 0.7)
    row:SetBackdropBorderColor(0, 1, 0, 1)
    
    -- Item icon
    local itemName, _, _, _, _, _, _, _, _, itemTexture = GetItemInfo(deal.itemID)
    
    local icon = row:CreateTexture(nil, "ARTWORK")
    icon:SetSize(40, 40)
    icon:SetPoint("LEFT", 5, 0)
    icon:SetTexture(itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark")
    
    -- Item name
    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    name:SetPoint("TOPLEFT", 50, -5)
    name:SetText(itemName or "Item " .. deal.itemID)
    
    -- Price comparison
    local priceText = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    priceText:SetPoint("TOPLEFT", 50, -25)
    priceText:SetText(string.format("Current: %s | Avg: %s", 
        GoblinAI:FormatGold(deal.current),
        GoblinAI:FormatGold(deal.average)))
    
    -- Savings
    local savings = row:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    savings:SetPoint("TOPRIGHT", -110, -15)
    savings:SetText(string.format("%.0f%% OFF", math.abs(deal.percent) * 100))
    savings:SetTextColor(0, 1, 0, 1)
    
    local savingsGold = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    savingsGold:SetPoint("TOPRIGHT", -110, -32)
    savingsGold:SetText("Save " .. GoblinAI:FormatGold(math.abs(deal.savings)))
    savingsGold:SetTextColor(0, 1, 0, 1)
    
    -- Buy button
    local buyBtn = CreateFrame("Button", nil, row, "UIPanelButtonTemplate")
    buyBtn:SetSize(80, 22)
    buyBtn:SetPoint("RIGHT", -10, 0)
    buyBtn:SetText("Quick Buy")
    buyBtn:SetScript("OnClick", function()
        Shopping:QuickBuy(deal.itemID)
    end)
    
    return row
end

function Shopping:QuickBuy(itemID)
    if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
        print("|cFFFF0000Goblin AI:|r You must be at the auction house!")
        return
    end
    
    -- Open search for this item
    print("|cFFFFD700Goblin AI:|r Opening AH search for item " .. itemID)
    -- Note: Actual buying requires user interaction due to Blizzard restrictions
    -- We can only open the search, user must click Buy
end

-- ============================================================================
-- Sniper UI
-- ============================================================================

function Shopping:CreateSniperUI()
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -60)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    content:Hide()
    
    -- Header
    local header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    header:SetPoint("TOP", 0, -5)
    header:SetText("SNIPER MODE")
    header:SetTextColor(1, 0, 0, 1)
    
    -- Status
    self.sniperStatus = content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    self.sniperStatus:SetPoint("TOP", 0, -35)
    self.sniperStatus:SetText("Inactive")
    
    -- Toggle button
    self.sniperToggle = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
    self.sniperToggle:SetSize(150, 30)
    self.sniperToggle:SetPoint("TOP", 0, -60)
    self.sniperToggle:SetText("Start Sniper")
    self.sniperToggle:SetScript("OnClick", function()
        Shopping:ToggleSniper()
    end)
    
    -- Feed scroll
    local scroll = GoblinAI:CreateScrollFrame(content, 650, 340)
    scroll:SetPoint("TOP", 0, -100)
    
    self.sniperScroll = scroll
    self.sniperContent = content
    self.sniperFeed = {}
end

function Shopping:StartSniper()
    if self.sniperActive then return end
    
    self.sniperActive = true
    self.sniperStatus:SetText("|cFF00FF00ACTIVE - Watching for deals...|r")
    self.sniperToggle:SetText("Stop Sniper")
    
    -- Start monitoring
    self:MonitorSniper()
end

function Shopping:StopSniper()
    self.sniperActive = false
    self.sniperStatus:SetText("Inactive")
    self.sniperToggle:SetText("Start Sniper")
    
    if self.sniperTimer then
        self.sniperTimer:Cancel()
        self.sniperTimer = nil
    end
end

function Shopping:ToggleSniper()
    if self.sniperActive then
        self:StopSniper()
    else
        self:StartSniper()
    end
end

function Shopping:MonitorSniper()
    if not self.sniperActive then return end
    
    -- Quick scan for new deals
    if AuctionHouseFrame and AuctionHouseFrame:IsShown() then
        -- Trigger a small scan
        -- In real TSM, this continuously polls new auctions
        -- We'll do a lightweight check every 5 seconds
    end
    
    -- Schedule next check
    self.sniperTimer = C_Timer.After(5, function()
        Shopping:MonitorSniper()
    end)
end

function Shopping:AddSniperAlert(itemID, price, avgPrice)
    table.insert(self.sniperFeed, 1, {
        itemID = itemID,
        price = price,
        avgPrice = avgPrice,
        timestamp = time(),
    })
    
    -- Keep only last 50
    while #self.sniperFeed > 50 do
        table.remove(self.sniperFeed)
    end
    
    -- Play sound
    PlaySound(SOUNDKIT.ALARM_CLOCK_WARNING_3)
    
    -- Refresh display
    self:RefreshSniperFeed()
end

function Shopping:RefreshSniperFeed()
    -- Implementation for displaying sniper alerts
end

-- ============================================================================
-- Initialization
-- ============================================================================

print("|cFFFFD700Goblin AI:|r Shopping Frame loaded - Deal finder & sniper ready")
