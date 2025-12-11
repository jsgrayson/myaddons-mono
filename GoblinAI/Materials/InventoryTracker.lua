-- Materials/InventoryTracker.lua - Track materials across all storage

GoblinAI.InventoryTracker = {}
local Tracker = GoblinAI.InventoryTracker

Tracker.trackedMaterials = {}

function Tracker:Initialize()
    self:RegisterEvents()
    self:UpdateAllInventories()
end

function Tracker:RegisterEvents()
    if not self.frame then
        self.frame = CreateFrame("Frame")
    end
    
    self.frame:RegisterEvent("BAG_UPDATE")
    self.frame:RegisterEvent("PLAYERBANKSLOTS_CHANGED")
    
    self.frame:SetScript("OnEvent", function(_, event, ...)
        if event == "BAG_UPDATE" or event == "PLAYERBANKSLOTS_CHANGED" then
            Tracker:UpdateAllInventories()
        end
    end)
end

function Tracker:UpdateAllInventories()
    self.inventory = {
        bags = self:ScanBags(),
        bank = self:ScanBank(),
        warbank = self:ScanWarbank(),
        totalByItem = {}
    }
    
    -- Aggregate totals
    for location, items in pairs(self.inventory) do
        if type(items) == "table" and location ~= "totalByItem" then
            for itemID, count in pairs(items) do
                self.inventory.totalByItem[itemID] = (self.inventory.totalByItem[itemID] or 0) + count
            end
        end
    end
end

function Tracker:ScanBags()
    local items = {}
    
    for bag = 0, NUM_BAG_SLOTS do
        for slot = 1, C_Container.GetContainerNumSlots(bag) or 0 do
            local itemInfo = C_Container.GetContainerItemInfo(bag, slot)
            if itemInfo and itemInfo.itemID then
                items[itemInfo.itemID] = (items[itemInfo.itemID] or 0) + (itemInfo.stackCount or 1)
            end
        end
    end
    
    return items
end

function Tracker:ScanBank()
    local items = {}
    
    if not IsPlayerInBankingRange() then
        return items
    end
    
    -- Bank bags
    for bag = NUM_BAG_SLOTS + 1, NUM_BAG_SLOTS + NUM_BANKBAGSLOTS do
        for slot = 1, C_Container.GetContainerNumSlots(bag) or 0 do
            local itemInfo = C_Container.GetContainerItemInfo(bag, slot)
            if itemInfo and itemInfo.itemID then
                items[itemInfo.itemID] = (items[itemInfo.itemID] or 0) + (itemInfo.stackCount or 1)
            end
        end
    end
    
    return items
end

function Tracker:ScanWarbank()
    local items = {}
    
    -- Warbank scanning (Retail 10.2+)
    -- This is a simplified version - full implementation would use Warbank API
    if C_Bank and C_Bank.CanUseBank and C_Bank.CanUseBank() then
        -- Warbank tab scanning would go here
        -- Placeholder for now
    end
    
    return items
end

function Tracker:GetItemCount(itemID)
    if not self.inventory then
        self:UpdateAllInventories()
    end
    
    return self.inventory.totalByItem[itemID] or 0
end

function Tracker:GetItemLocations(itemID)
    if not self.inventory then
        self:UpdateAllInventories()
    end
    
    local locations = {}
    
    if self.inventory.bags[itemID] then
        table.insert(locations, string.format("Bags: %d", self.inventory.bags[itemID]))
    end
    
    if self.inventory.bank[itemID] then
        table.insert(locations, string.format("Bank: %d", self.inventory.bank[itemID]))
    end
    
    if self.inventory.warbank[itemID] then
        table.insert(locations, string.format("Warbank: %d", self.inventory.warbank[itemID]))
    end
    
    return locations
end

function Tracker:GenerateShoppingList(requiredMaterials)
    local shoppingList = {}
    
    for itemID, needed in pairs(requiredMaterials) do
        local have = self:GetItemCount(itemID)
        local toBuy = math.max(0, needed - have)
        
        if toBuy > 0 then
            table.insert(shoppingList, {
                itemID = itemID,
                needed = needed,
                have = have,
                toBuy = toBuy
            })
        end
    end
    
    return shoppingList
end

function Tracker:GetWealthSummary()
    local gold = GetMoney()
    
    -- Estimate inventory value (would need market prices)
    local inventoryValue = 0
    -- This would integrate with auction data to estimate value
    
    return {
        gold = gold,
        inventoryValue = inventoryValue,
        totalWealth = gold + inventoryValue
    }
end
