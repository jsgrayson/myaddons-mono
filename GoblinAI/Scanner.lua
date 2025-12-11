-- Scanner.lua - Enhanced AH Scanning with Progress & History
-- Part of GoblinAI v2.0

GoblinAI.Scanner = {}
local Scanner = GoblinAI.Scanner

Scanner.isScanning = false
Scanner.scanProgress = 0
Scanner.totalItems = 0
Scanner.currentPage = 0
Scanner.scanData = {}
Scanner.categories = {}

-- ============================================================================
-- Scan Categories (For filtered scanning)
-- ============================================================================

Scanner.CATEGORIES = {
    ALL = {name = "All Items", filter = nil},
    TRADE_GOODS = {name = "Trade Goods", classID = 7},
    CONSUMABLES = {name = "Consumables", classID = 0},
    WEAPONS = {name = "Weapons", classID = 2},
    ARMOR = {name = "Armor", classID = 4},
    RECIPES = {name = "Recipes", classID = 9},
    GEMS = {name = "Gems", classID = 3},
    ENCHANTS = {name = "Enchantments", classID = 8},
    PETS = {name = "Battle Pets", classID = 17},
}

Scanner.selectedCategory = "ALL"

-- ============================================================================
-- Progress UI
-- ============================================================================

function Scanner:CreateProgressUI()
    if self.progressFrame then return end
    
    -- Progress Frame
    local frame = CreateFrame("Frame", "GoblinAIScanProgress", UIParent, "BackdropTemplate")
    frame:SetSize(400, 100)
    frame:SetPoint("TOP", 0, -100)
    frame:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
        edgeFile = "Interface\\DialogFrame\\UI-DialogBox-Border",
        tile = true, tileSize = 32, edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    frame:SetBackdropColor(0, 0, 0, 0.9)
    frame:Hide()
    
    -- Title
    frame.title = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    frame.title:SetPoint("TOP", 0, -10)
    frame.title:SetText("Scanning Auction House...")
    frame.title:SetTextColor(1, 0.84, 0, 1)
    
    -- Progress Bar Background
    frame.progressBg = frame:CreateTexture(nil, "BACKGROUND")
    frame.progressBg:SetSize(360, 20)
    frame.progressBg:SetPoint("TOP", 0, -35)
    frame.progressBg:SetColorTexture(0.2, 0.2, 0.2, 0.8)
    
    -- Progress Bar
    frame.progressBar = frame:CreateTexture(nil, "ARTWORK")
    frame.progressBar:SetSize(0, 20)
    frame.progressBar:SetPoint("LEFT", frame.progressBg, "LEFT", 0, 0)
    frame.progressBar:SetColorTexture(1, 0.84, 0, 0.8)
    
    -- Progress Text
    frame.progressText = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    frame.progressText:SetPoint("CENTER", frame.progressBg, "CENTER")
    frame.progressText:SetText("0 / 0 (0%)")
    
    -- Status Text
    frame.statusText = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    frame.statusText:SetPoint("TOP", frame.progressBg, "BOTTOM", 0, -10)
    frame.statusText:SetText("Initializing scan...")
    
    -- Cancel Button
    frame.cancelBtn = CreateFrame("Button", nil, frame, "UIPanelButtonTemplate")
    frame.cancelBtn:SetSize(80, 22)
    frame.cancelBtn:SetPoint("BOTTOM", 0, 10)
    frame.cancelBtn:SetText("Cancel")
    frame.cancelBtn:SetScript("OnClick", function()
        Scanner:StopScan()
    end)
    
    self.progressFrame = frame
end

function Scanner:UpdateProgress(current, total, status)
    if not self.progressFrame then return end
    
    local percent = total > 0 and (current / total) or 0
    
    -- Update bar
    self.progressFrame.progressBar:SetWidth(360 * percent)
    
    -- Update text
    self.progressFrame.progressText:SetText(string.format("%s / %s (%.0f%%)", 
        GoblinAI:FormatNumber(current), 
        GoblinAI:FormatNumber(total), 
        percent * 100))
    
    -- Update status
    if status then
        self.progressFrame.statusText:SetText(status)
    end
end

function Scanner:ShowProgress()
    self:CreateProgressUI()
    self.progressFrame:Show()
end

function Scanner:HideProgress()
    if self.progressFrame then
        self.progressFrame:Hide()
    end
end

-- ============================================================================
-- Enhanced Scanning
-- ============================================================================

function Scanner:StartScan(category)
    if self.isScanning then
        print("|cFFFF0000Goblin AI:|r Scan already in progress")
        return
    end
    
    if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
        print("|cFFFF0000Goblin AI:|r You must be at the auction house!")
        return
    end
    
    self.isScanning = true
    self.scanProgress = 0
    self.scanData = {}
    self.selectedCategory = category or "ALL"
    
    print("|cFFFFD700Goblin AI:|r Starting AH scan" .. 
          (category and category ~= "ALL" and (" - " .. self.CATEGORIES[category].name) or "") .. "...")
    
    -- Show progress UI
    self:ShowProgress()
    self:UpdateProgress(0, 1, "Initializing...")
    
    -- Start scanning
    self:ScanAllItems()
end

function Scanner:ScanAllItems()
    -- Build search query
    local searchTerms = {
        sorts = {},
        searchString = "",
        filters = {}
    }
    
    -- Add category filter if selected
    if self.selectedCategory ~= "ALL" then
        local cat = self.CATEGORIES[self.selectedCategory]
        if cat and cat.classID then
            table.insert(searchTerms.filters, {
                category = cat.classID
            })
        end
    end
    
    -- Use Blizzard's browse search
    C_AuctionHouse.SendBrowseQuery(searchTerms)
    
    -- Register for results
    self:RegisterEvents()
end

function Scanner:RegisterEvents()
    if not self.frame then
        self.frame = CreateFrame("Frame")
    end
    
    self.frame:RegisterEvent("AUCTION_HOUSE_BROWSE_RESULTS_UPDATED")
    self.frame:RegisterEvent("AUCTION_HOUSE_BROWSE_RESULTS_ADDED")
    
    self.frame:SetScript("OnEvent", function(_, event, ...)
        if event == "AUCTION_HOUSE_BROWSE_RESULTS_UPDATED" then
            Scanner:OnBrowseResultsUpdated()
        elseif event == "AUCTION_HOUSE_BROWSE_RESULTS_ADDED" then
            Scanner:OnBrowseResultsAdded(...)
        end
    end)
end

function Scanner:OnBrowseResultsUpdated()
    local numResults = C_AuctionHouse.GetNumBrowseResults()
    
    -- Update total items estimate
    if self.totalItems == 0 then
        self.totalItems = numResults
    end
    
    -- Process results
    for i = 1, numResults do
        local result = C_AuctionHouse.GetBrowseResultInfo(i)
        if result and result.itemKey then
            self:ProcessItem(result)
        end
    end
    
    self.scanProgress = numResults
    
    -- Update UI
    self:UpdateProgress(self.scanProgress, self.totalItems, 
                        string.format("Scanned %d items...", self.scanProgress))
end

function Scanner:OnBrowseResultsAdded(addedResults)
    if not addedResults then return end
    
    for _, result in ipairs(addedResults) do
        if result and result.itemKey then
            self:ProcessItem(result)
            self.scanProgress = self.scanProgress + 1
        end
    end
    
    self:UpdateProgress(self.scanProgress, self.totalItems, 
                        string.format("Scanned %d items...", self.scanProgress))
end

function Scanner:ProcessItem(result)
    local itemKey = result.itemKey
    if not itemKey or not itemKey.itemID then return end
    
    local itemID = itemKey.itemID
    
    -- Get pricing
    local minBid = result.minBid or 0
    local buyout = result.buyoutAmount or 0
    local price = buyout > 0 and buyout or minBid
    
    if price == 0 then return end
    
    -- Check if we already have this item in scan data
    local existingEntry = nil
    for _, entry in ipairs(self.scanData) do
        if entry.item_id == itemID then
            existingEntry = entry
            break
        end
    end
    
    if existingEntry then
        -- Update if this is cheaper
        if price < existingEntry.price then
            existingEntry.price = price
        end
        existingEntry.quantity = existingEntry.quantity + (result.quantity or 1)
        existingEntry.sellers = existingEntry.sellers + 1
    else
        -- Add new entry
        table.insert(self.scanData, {
            item_id = itemID,
            price = price,
            quantity = result.quantity or 1,
            sellers = 1,
            timestamp = time(),
            item_level = itemKey.itemLevel or 0,
            battle_pet_species = itemKey.battlePetSpeciesID or 0,
        })
    end
end

function Scanner:StopScan()
    self.isScanning = false
    
    if self.frame then
        self.frame:UnregisterAllEvents()
    end
    
    -- Hide progress
    self:HideProgress()
    
    -- Save scan data
    self:SaveScanData()
    
    print(string.format("|cFFFFD700Goblin AI:|r Scan complete! %s items scanned", 
                        GoblinAI:FormatNumber(#self.scanData)))
end

-- ============================================================================
-- Price History & Data Management
-- ============================================================================

function Scanner:SaveScanData()
    if not GoblinAIDB.scans then
        GoblinAIDB.scans = {}
    end
    
    local scanEntry = {
        timestamp = time(),
        character = GoblinAI:GetPlayerID(),
        realm = GetRealmName(),
        faction = UnitFactionGroup("player"),
        category = self.selectedCategory,
        data = self.scanData,
        item_count = #self.scanData,
    }
    
    table.insert(GoblinAIDB.scans, scanEntry)
    
    -- Keep only last 30 scans
    while #GoblinAIDB.scans > 30 do
        table.remove(GoblinAIDB.scans, 1)
    end
    
    -- Update price history
    self:UpdatePriceHistory()
    
    print("|cFFFFD700Goblin AI:|r Scan data saved to SavedVariables")
end

function Scanner:UpdatePriceHistory()
    if not GoblinAIDB.priceHistory then
        GoblinAIDB.priceHistory = {}
    end
    
    local currentTime = time()
    
    -- Update history for each scanned item
    for _, item in ipairs(self.scanData) do
        local itemID = item.item_id
        
        if not GoblinAIDB.priceHistory[itemID] then
            GoblinAIDB.priceHistory[itemID] = {}
        end
        
        -- Add price point
        table.insert(GoblinAIDB.priceHistory[itemID], {
            timestamp = currentTime,
            price = item.price,
            quantity = item.quantity,
        })
        
        -- Keep only last 30 days of data
        local cutoff = currentTime - (30 * 24 * 60 * 60)
        local history = GoblinAIDB.priceHistory[itemID]
        
        local newHistory = {}
        for _, point in ipairs(history) do
            if point.timestamp >= cutoff then
                table.insert(newHistory, point)
            end
        end
        
        GoblinAIDB.priceHistory[itemID] = newHistory
    end
end

function Scanner:GetPriceHistory(itemID, days)
    if not GoblinAIDB.priceHistory or not GoblinAIDB.priceHistory[itemID] then
        return nil
    end
    
    days = days or 7
    local cutoff = time() - (days * 24 * 60 * 60)
    local history = {}
    
    for _, point in ipairs(GoblinAIDB.priceHistory[itemID]) do
        if point.timestamp >= cutoff then
            table.insert(history, point)
        end
    end
    
    return history
end

function Scanner:GetAveragePrice(itemID, days)
    local history = self:GetPriceHistory(itemID, days)
    if not history or #history == 0 then return nil end
    
    local total = 0
    for _, point in ipairs(history) do
        total = total + point.price
    end
    
    return total / #history
end

function Scanner:GetPriceTrend(itemID, days)
    local history = self:GetPriceHistory(itemID, days)
    if not history or #history < 2 then return 0 end
    
    -- Simple trend: compare first vs last
    local first = history[1].price
    local last = history[#history].price
    
    return ((last - first) / first) -- Decimal percentage
end

-- ============================================================================
-- Scan Comparison
-- ============================================================================

function Scanner:GetLastScan()
    if GoblinAIDB.scans and #GoblinAIDB.scans > 0 then
        return GoblinAIDB.scans[#GoblinAIDB.scans]
    end
    return nil
end

function Scanner:CompareScanToHistory(itemID)
    -- Get current scan price
    local currentPrice = nil
    for _, item in ipairs(self.scanData) do
        if item.item_id == itemID then
            currentPrice = item.price
            break
        end
    end
    
    if not currentPrice then return nil end
    
    -- Get historical average
    local avgPrice = self:GetAveragePrice(itemID, 7)
    if not avgPrice then return nil end
    
    local difference = currentPrice - avgPrice
    local percentChange = (difference / avgPrice)
    
    return {
        current = currentPrice,
        average = avgPrice,
        difference = difference,
        percent = percentChange,
        isDeal = (percentChange < -0.15), -- 15% below average
    }
end

-- ============================================================================
-- Auto-Scan Scheduler
-- ============================================================================

function Scanner:StartAutoScan()
    if self.autoScanTimer then
        return -- Already running
    end
    
    local interval = GoblinAIDB.settings.scanInterval or 300
    
    self.autoScanTimer = C_Timer.NewTicker(interval, function()
        if AuctionHouseFrame and AuctionHouseFrame:IsShown() and GoblinAIDB.settings.autoScan then
            Scanner:StartScan()
        end
    end)
    
    print("|cFFFFD700Goblin AI:|r Auto-scan enabled (every " .. interval .. "s)")
end

function Scanner:StopAutoScan()
    if self.autoScanTimer then
        self.autoScanTimer:Cancel()
        self.autoScanTimer = nil
        print("|cFFFFD700Goblin AI:|r Auto-scan disabled")
    end
end

-- ============================================================================
-- Initialization
-- ============================================================================

-- Create progress UI on load
Scanner:CreateProgressUI()

print("|cFFFFD700Goblin AI:|r Scanner loaded - Enhanced scanning with history tracking")
