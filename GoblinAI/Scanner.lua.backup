-- Scanner.lua - Auction house scanning (ToS-compliant)

GoblinAI.Scanner = {}
local Scanner = GoblinAI.Scanner

Scanner.isScanning = false
Scanner.scanProgress = 0
Scanner.totalItems = 0
Scanner.currentPage = 0

function Scanner:StartScan()
    if self.isScanning then
        print("|cFFFF0000Goblin AI|r: Scan already in progress")
        return
    end
    
    if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
        print("|cFFFF0000Goblin AI|r: You must be at the auction house!")
        return
    end
    
    self.isScanning = true
    self.scanProgress = 0
    self.scanData = {}
    
    print("|cFF00FF00Goblin AI|r: Starting AH scan...")
    
    -- Use modern Blizzard AH API (C_AuctionHouse)
    self:ScanAllItems()
end

function Scanner:ScanAllItems()
    -- Use Blizzard's browse search
    C_AuctionHouse.SendBrowseQuery({
        sorts = {},
        searchString = "",
        filters = {}
    })
    
    -- Hook result events
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
    
    for i = 1, numResults do
        local itemKey = C_AuctionHouse.GetBrowseResultInfo(i)
        if itemKey then
            self:ProcessItem(itemKey, i)
        end
    end
    
    self.scanProgress = numResults
    print(string.format("|cFF00FF00Goblin AI|r: Scanned %d items...", numResults))
end

function Scanner:OnBrowseResultsAdded(addedResults)
    -- Process additional results
    for _, result in ipairs(addedResults) do
        self:ProcessItem(result.itemKey, result.index)
    end
end

function Scanner:ProcessItem(itemKey, index)
    local itemID = itemKey.itemID
    
    -- Get item info
    local itemInfo = C_AuctionHouse.GetItemKeyInfo(itemKey)
    if not itemInfo then return end
    
    -- Get lowest price for this item
    local searchResults = C_AuctionHouse.GetBrowseResults()
    local lowestPrice = nil
    local totalQuantity = 0
    local numSellers = 0
    
    for _, result in ipairs(searchResults) do
        if result.itemKey.itemID == itemID then
            local minBid = result.minBid or 0
            local buyout = result.buyoutAmount or 0
            local price = buyout > 0 and buyout or minBid
            
            if not lowestPrice or price < lowestPrice then
                lowestPrice = price
            end
            
            totalQuantity = totalQuantity + (result.quantity or 0)
            numSellers = numSellers + 1
        end
    end
    
    -- Store in scan data
    if lowestPrice and lowestPrice > 0 then
        table.insert(self.scanData, {
            item_id = itemID,
            price = lowestPrice,
            quantity = totalQuantity,
            sellers = numSellers,
            timestamp = time()
        })
    end
end

function Scanner:StopScan()
    self.isScanning = false
    
    if self.frame then
        self.frame:UnregisterAllEvents()
    end
    
    -- Save to SavedVariables
    self:SaveScanData()
    
    print(string.format("|cFF00FF00Goblin AI|r: Scan complete! %d items scanned", #self.scanData))
end

function Scanner:SaveScanData()
    if not GoblinAIDB.scans then
        GoblinAIDB.scans = {}
    end
    
    local scanEntry = {
        timestamp = time(),
        character = UnitName("player") .. "-" .. GetRealmName(),
        realm = GetRealmName(),
        faction = UnitFactionGroup("player"),
        data = self.scanData,
        item_count = #self.scanData
    }
    
    table.insert(GoblinAIDB.scans, scanEntry)
    
    -- Keep only last 7 scans
    while #GoblinAIDB.scans > 7 do
        table.remove(GoblinAIDB.scans, 1)
    end
    
    print("|cFF00FF00Goblin AI|r: Scan data saved to SavedVariables")
end

function Scanner:GetLastScan()
    if GoblinAIDB.scans and #GoblinAIDB.scans > 0 then
        return GoblinAIDB.scans[#GoblinAIDB.scans]
    end
    return nil
end
