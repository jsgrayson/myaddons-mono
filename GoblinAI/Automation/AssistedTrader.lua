-- Automation/AssistedTrader.lua - Minimal effort trading workflow

GoblinAI.AssistedTrader = {}
local Trader = GoblinAI.AssistedTrader

Trader.queue = {}
Trader.isProcessing = false

function Trader:QueueItem(opportunity)
    table.insert(self.queue, opportunity)
    print("|cFF00FF00Goblin AI|r: Added " .. (opportunity.itemName or "item") .. " to trading queue.")
    self:UpdateUI()
end

function Trader:ExecuteNext()
    if #self.queue == 0 then
        print("|cFFFF0000Goblin AI|r: Queue is empty!")
        return
    end

    local opp = self.queue[1]
    self:ProcessOpportunity(opp)
end

function Trader:ProcessOpportunity(opp)
    -- 1. Open AH if not open
    if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
        print("|cFFFF0000Goblin AI|r: Please open the Auction House.")
        return
    end

    -- 2. Search for item
    print("|cFF00FF00Goblin AI|r: Searching for " .. (opp.itemName or opp.itemID) .. "...")
    
    -- Use C_AuctionHouse to search
    local itemKey = C_AuctionHouse.MakeItemKey(opp.itemID)
    C_AuctionHouse.SendBrowseQuery({
        searchString = opp.itemName,
        sorts = {
            { sortOrder = Enum.AuctionHouseSortOrder.Price, reverseSort = false }
        },
        filters = {}
    })

    -- 3. Hook into search results to auto-select
    -- Note: Actual "Buy" click MUST be hardware event per ToS.
    -- We can select the item and fill the buyout button, but user must click "Buy".
    
    self:RegisterSearchListener(opp)
end

function Trader:RegisterSearchListener(opp)
    if not self.frame then self.frame = CreateFrame("Frame") end
    
    self.frame:RegisterEvent("AUCTION_HOUSE_BROWSE_RESULTS_UPDATED")
    self.frame:SetScript("OnEvent", function()
        self.frame:UnregisterEvent("AUCTION_HOUSE_BROWSE_RESULTS_UPDATED")
        
        -- Find the specific auction matching our price criteria
        local results = C_AuctionHouse.GetBrowseResults()
        for _, result in ipairs(results) do
            if result.itemKey.itemID == opp.itemID then
                local price = result.buyoutAmount or result.minBid
                if price <= opp.maxBuyPrice then
                    -- Found it!
                    print("|cFF00FF00Goblin AI|r: Found deal! Price: " .. GoblinAI:FormatGold(price))
                    print("|cFF00FF00Goblin AI|r: CLICK BUY NOW!")
                    
                    -- In a real addon, we might highlight the row or show a big "BUY" button overlay
                    -- For now, we just notify.
                    
                    -- Remove from queue after "success" (or user manually removes)
                    table.remove(self.queue, 1)
                    return
                end
            end
        end
        
        print("|cFFFF0000Goblin AI|r: Could not find item at target price.")
    end)
end

function Trader:UpdateUI()
    -- Update queue display if visible
end
