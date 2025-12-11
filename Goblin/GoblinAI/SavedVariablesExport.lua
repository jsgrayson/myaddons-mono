-- SavedVariablesExport.lua - Format and export data for server processing

GoblinAI.SavedVariablesExport = {}
local Export = GoblinAI.SavedVariablesExport

function Export:GenerateExportData()
    local exportData = {
        version = GoblinAI.version,
        timestamp = time(),
        character = UnitName("player") .. "-" .. GetRealmName(),
        realm = GetRealmName(),
        faction = UnitFactionGroup("player"),
        
        -- Latest scan data
        lastScan = GoblinAI.Scanner:GetLastScan(),
        
        -- Character info
        characterData = GoblinAI.CharacterData:GetCurrentCharacter(),
        
        -- Inventory (materials tracking)
        inventory = self:GetInventorySnapshot(),
        
        -- Active auctions
        activeAuctions = self:GetActiveAuctions(),
        
        -- Settings
        settings = GoblinAIDB.settings
    }
    
    return exportData
end

function Export:GetInventorySnapshot()
    local inventory = {
        bags = {},
        bank = {},
        warbank = {}
    }
    
    -- Scan bags
    for bag = 0, NUM_BAG_SLOTS do
        for slot = 1, C_Container.GetContainerNumSlots(bag) or 0 do
            local itemInfo = C_Container.GetContainerItemInfo(bag, slot)
            if itemInfo then
                local itemID = itemInfo.itemID
                local count = itemInfo.stackCount or 1
                
                inventory.bags[itemID] = (inventory.bags[itemID] or 0) + count
            end
        end
    end
    
    -- Bank (if opened)
    if IsPlayerInBankingRange() then
        for bag = NUM_BAG_SLOTS + 1, NUM_BAG_SLOTS + NUM_BANKBAGSLOTS do
            for slot = 1, C_Container.GetContainerNumSlots(bag) or 0 do
                local itemInfo = C_Container.GetContainerItemInfo(bag, slot)
                if itemInfo then
                    local itemID = itemInfo.itemID
                    local count = itemInfo.stackCount or 1
                    
                    inventory.bank[itemID] = (inventory.bank[itemID] or 0) + count
                end
            end
        end
    end
    
    -- Warbank (Retail 10.2+)
    if C_Bank and C_Bank.FetchDepositedMoney then
        -- Warbank API available
        -- Would need to implement Warbank scanning
        -- This is a placeholder
    end
    
    return inventory
end

function Export:GetActiveAuctions()
    -- Get our active auctions from AH
    -- This requires AH to be open
    local auctions = {}
    
    if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
        return auctions
    end
    
    -- Use C_AuctionHouse to get owned auctions
    local numAuctions = C_AuctionHouse.GetNumOwnedAuctions()
    
    for i = 1, numAuctions do
        local info = C_AuctionHouse.GetOwnedAuctionInfo(i)
        if info then
            table.insert(auctions, {
                auctionID = info.auctionID,
                itemID = info.itemKey.itemID,
                quantity = info.quantity,
                price = info.buyoutAmount or info.bidAmount,
                timeLeft = info.timeLeftSeconds
            })
        end
    end
    
    return auctions
end

function Export:SaveToFile()
    -- Data is automatically saved via SavedVariables
    -- User exports WTF/Account/ACCOUNT/SavedVariables/GoblinAI.lua
    print("|cFF00FF00Goblin AI|r: Data ready for export!")
    print("|cFF00FF00Goblin AI|r: File location: WTF/Account/" .. select(1, BNGetInfo()) .. "/SavedVariables/GoblinAI.lua")
end

function Export:CompressData(data)
    -- Optional: Compress large datasets
    -- For now, just return as-is
    -- Could implement LZW compression in Lua if needed
    return data
end
