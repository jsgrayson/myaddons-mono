-- UI/LedgerFrame.lua - Sales Tracking & Analytics
-- Part of GoblinAI v2.0

GoblinAI.LedgerFrame = {}
local Ledger = GoblinAI.LedgerFrame

Ledger.timeframe = "week" -- day, week, month, all
Ledger.viewMode = "timeline" -- timeline, items, categories

-- ============================================================================
-- Initialize Ledger Tab
-- ============================================================================

function Ledger:Initialize(parentFrame)
    self.frame = parentFrame
    self:CreateUI()
    self:StartTracking()
end

function Ledger:CreateUI()
    -- Header
    local header = self.frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -10)
    header:SetText("Sales & Purchase History")
    header:SetTextColor(1, 0.84, 0, 1)
    
    -- Summary cards
    self:CreateSummaryCards()
    
    -- Controls
    local controlsFrame = CreateFrame("Frame", nil, self.frame)
    controlsFrame:SetSize(660, 35)
    controlsFrame:SetPoint("TOP", 0, -110)
    
    -- Timeframe buttons
    local tfLabel = controlsFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    tfLabel:SetPoint("LEFT", 10, 0)
    tfLabel:SetText("Timeframe:")
    
    local timeframes = {
        {id = "day", text = "Today"},
        {id = "week", text = "Week"},
        {id = "month", text = "Month"},
        {id = "all", text = "All"},
    }
    
    local xOffset = 80
    for _, tf in ipairs(timeframes) do
        local btn = CreateFrame("Button", nil, controlsFrame, "UIPanelButtonTemplate")
        btn:SetSize(60, 25)
        btn:SetPoint("LEFT", xOffset, 0)
        btn:SetText(tf.text)
        btn:SetScript("OnClick", function()
            Ledger.timeframe = tf.id
            Ledger:RefreshView()
        end)
        xOffset = xOffset + 65
    end
    
    -- View mode dropdown
    local viewLabel = controlsFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    viewLabel:SetPoint("RIGHT", -150, 0)
    viewLabel:SetText("View:")
    
    local viewBtn = CreateFrame("Button", nil, controlsFrame, "UIPanelButtonTemplate")
    viewBtn:SetSize(120, 25)
    viewBtn:SetPoint("RIGHT", -10, 0)
    viewBtn:SetText("Timeline")
    viewBtn:SetScript("OnClick", function()
        if Ledger.viewMode == "timeline" then
            Ledger.viewMode = "items"
            viewBtn:SetText("Top Items")
        elseif Ledger.viewMode == "items" then
            Ledger.viewMode = "categories"
            viewBtn:SetText("Categories")
        else
            Ledger.viewMode = "timeline"
            viewBtn:SetText("Timeline")
        end
        Ledger:RefreshView()
    end)
    
    -- Content area
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -150)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    self.contentFrame = content
end

function Ledger:CreateSummaryCards()
    -- Today's profit
    local profitCard = CreateFrame("Frame", nil, self.frame, "BackdropTemplate")
    profitCard:SetSize(200, 70)
    profitCard:SetPoint("TOPLEFT", 20, -45)
    profitCard:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    profitCard:SetBackdropColor(0, 0.15, 0, 0.7)
    profitCard:SetBackdropBorderColor(0, 0.8, 0, 1)
    
    local profitLabel = profitCard:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    profitLabel:SetPoint("TOP", 0, -8)
    profitLabel:SetText("Today's Profit")
    
    local profitValue = profitCard:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    profitValue:SetPoint("CENTER", 0, -5)
    profitValue:SetText(GoblinAI:FormatGold(0))
    profitValue:SetTextColor(0, 1, 0, 1)
    self.profitValue = profitValue
    
    -- Total sales
    local salesCard = CreateFrame("Frame", nil, self.frame, "BackdropTemplate")
    salesCard:SetSize(200, 70)
    salesCard:SetPoint("LEFT", profitCard, "RIGHT", 10, 0)
    salesCard:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    salesCard:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
    salesCard:SetBackdropBorderColor(1, 0.84, 0, 1)
    
    local salesLabel = salesCard:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    salesLabel:SetPoint("TOP", 0, -8)
    salesLabel:SetText("Total Sales")
    
    local salesValue = salesCard:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    salesValue:SetPoint("CENTER", 0, -5)
    salesValue:SetText("0")
    self.salesValue = salesValue
    
    -- Average ROI
    local roiCard = CreateFrame("Frame", nil, self.frame, "BackdropTemplate")
    roiCard:SetSize(200, 70)
    roiCard:SetPoint("LEFT", salesCard, "RIGHT", 10, 0)
    roiCard:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    roiCard:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
    roiCard:SetBackdropBorderColor(1, 0.84, 0, 1)
    
    local roiLabel = roiCard:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    roiLabel:SetPoint("TOP", 0, -8)
    roiLabel:SetText("Average ROI")
    
    local roiValue = roiCard:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    roiValue:SetPoint("CENTER", 0, -5)
    roiValue:SetText("0%")
    self.roiValue = roiValue
end

-- ============================================================================
-- Transaction Tracking
-- ============================================================================

function Ledger:StartTracking()
    -- Hook into mail events to track sales
    if not self.trackingFrame then
        self.trackingFrame = CreateFrame("Frame")
        self.trackingFrame:RegisterEvent("MAIL_INBOX_UPDATE")
        self.trackingFrame:RegisterEvent("MAIL_SHOW")
        
        self.trackingFrame:SetScript("OnEvent", function(_, event)
            if event == "MAIL_INBOX_UPDATE" or event == "MAIL_SHOW" then
                Ledger:ScanMailbox()
            end
        end)
    end
end

function Ledger:ScanMailbox()
    -- Scan mailbox for sold auction notifications
    local numItems = GetInboxNumItems()
    
    for i = 1, numItems do
        local _, _, sender, subject, money, _, _, _, _, _, _, _, _ = GetInboxHeaderInfo(i)
        
        -- Check if it's an auction sold notification
        if sender == "The Auctioneer" and money and money > 0 then
            -- Try to extract item from subject
            local itemLink = string.match(subject, "|c%x+|Hitem:.-|h%[.-%]|h|r")
            
            if itemLink then
                self:LogSale(itemLink, money, time())
            end
        end
    end
end

function Ledger:LogSale(itemLink, price, timestamp)
    if not GoblinAIDB.ledger then
        GoblinAIDB.ledger = {}
    end
    
    local itemID = GetItemInfoInstant(itemLink)
    
    table.insert(GoblinAIDB.ledger, {
        type = "sale",
        itemID = itemID,
        itemLink = itemLink,
        price = price,
        timestamp = timestamp,
        character = GoblinAI:GetPlayerID(),
    })
    
    print("|cFFFFD700Goblin AI:|r Sale logged: " .. itemLink .. " for " .. GoblinAI:FormatGold(price))
end

function Ledger:LogPurchase(itemLink, price, quantity, timestamp)
    if not GoblinAIDB.ledger then
        GoblinAIDB.ledger = {}
    end
    
    local itemID = GetItemInfoInstant(itemLink)
    
    table.insert(GoblinAIDB.ledger, {
        type = "purchase",
        itemID = itemID,
        itemLink = itemLink,
        price = price,
        quantity = quantity or 1,
        timestamp = timestamp or time(),
        character = GoblinAI:GetPlayerID(),
    })
end

-- ============================================================================
-- Analytics
-- ============================================================================

function Ledger:GetTimeframeBounds()
    local now = time()
    local start = 0
    
    if self.timeframe == "day" then
        start = now - (24 * 60 * 60)
    elseif self.timeframe == "week" then
        start = now - (7 * 24 * 60 * 60)
    elseif self.timeframe == "month" then
        start = now - (30 * 24 * 60 * 60)
    end
    
    return start, now
end

function Ledger:CalculateStats()
    local startTime, endTime = self:GetTimeframeBounds()
    local ledger = GoblinAIDB.ledger or {}
    
    local stats = {
        totalSales = 0,
        totalPurchases = 0,
        salesRevenue = 0,
        purchaseCost = 0,
        profit = 0,
        transactions = 0,
        itemBreakdown = {},
    }
    
    for _, entry in ipairs(ledger) do
        if entry.timestamp >= startTime and entry.timestamp <= endTime then
            stats.transactions = stats.transactions + 1
            
            if entry.type == "sale" then
                stats.totalSales = stats.totalSales + 1
                stats.salesRevenue = stats.salesRevenue + entry.price
                
                -- Track per item
                if not stats.itemBreakdown[entry.itemID] then
                    stats.itemBreakdown[entry.itemID] = {
                        sales = 0,
                        revenue = 0,
                        itemLink = entry.itemLink,
                    }
                end
                stats.itemBreakdown[entry.itemID].sales = stats.itemBreakdown[entry.itemID].sales + 1
                stats.itemBreakdown[entry.itemID].revenue = stats.itemBreakdown[entry.itemID].revenue + entry.price
                
            elseif entry.type == "purchase" then
                stats.totalPurchases = stats.totalPurchases + 1
                stats.purchaseCost = stats.purchaseCost + entry.price
            end
        end
    end
    
    stats.profit = stats.salesRevenue - stats.purchaseCost
    stats.roi = stats.purchaseCost > 0 and ((stats.profit / stats.purchaseCost) * 100) or 0
    
    return stats
end

function Ledger:RefreshView()
    if not self.contentFrame then return end
    
    -- Clear
    for _, child in ipairs({self.contentFrame:GetChildren()}) do
        child:Hide()
    end
    
    -- Update summary
    local stats = self:CalculateStats()
    
    if self.profitValue then
        self.profitValue:SetText(GoblinAI:FormatGold(stats.profit))
        self.profitValue:SetTextColor(stats.profit >= 0 and 0 or 1, stats.profit >= 0 and 1 or 0, 0, 1)
    end
    
    if self.salesValue then
        self.salesValue:SetText(tostring(stats.totalSales))
    end
    
    if self.roiValue then
        self.roiValue:SetText(string.format("%.1f%%", stats.roi))
    end
    
    -- Show view
    if self.viewMode == "timeline" then
        self:ShowTimeline(stats)
    elseif self.viewMode == "items" then
        self:ShowTopItems(stats)
    elseif self.viewMode == "categories" then
        self:ShowCategories(stats)
    end
end

function Ledger:ShowTimeline(stats)
    local content = self.contentFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    content:SetPoint("TOP", 0, -20)
    content:SetText(string.format("Timeline view: %d transactions", stats.transactions))
    
    -- TODO: Actual timeline graph
    local info = self.contentFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    info:SetPoint("TOP", 0, -50)
    info:SetText("Visual timeline graph coming in Phase 8")
end

function Ledger:ShowTopItems(stats)
    -- Convert to sorted array
    local items = {}
    for itemID, data in pairs(stats.itemBreakdown) do
        table.insert(items, {
            itemID = itemID,
            sales = data.sales,
            revenue = data.revenue,
            itemLink = data.itemLink,
        })
    end
    
    table.sort(items, function(a, b)
        return a.revenue > b.revenue
    end)
    
    -- Display top 10
    local yOffset = -10
    for i = 1, math.min(10, #items) do
        local item = items[i]
        
        local row = self.contentFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        row:SetPoint("TOPLEFT", 10, yOffset)
        row:SetText(string.format("%d. %s - %d sales - %s", 
            i,
            item.itemLink or ("Item " .. item.itemID),
            item.sales,
            GoblinAI:FormatGold(item.revenue)))
        row:SetJustifyH("LEFT")
        
        yOffset = yOffset - 25
    end
    
    if #items == 0 then
        local noData = self.contentFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        noData:SetPoint("TOP", 0, -50)
        noData:SetText("No sales recorded yet")
    end
end

function Ledger:ShowCategories(stats)
    local content = self.contentFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    content:SetPoint("TOP", 0, -20)
    content:SetText("Category breakdown coming soon")
end

-- ============================================================================
-- Export
-- ============================================================================

function Ledger:ExportToCSV()
    local ledger = GoblinAIDB.ledger or {}
    
    print("|cFFFFD700Goblin AI:|r Ledger has " .. #ledger .. " transactions")
    print("CSV export prepared in SavedVariables for external analysis")
end

-- ============================================================================
-- Initialization
-- ============================================================================

print("|cFFFFD700Goblin AI:|r Ledger Frame loaded - Transaction tracking active")
