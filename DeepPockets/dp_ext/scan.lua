-- dp_ext/scan.lua
local ADDON_NAME, ns = ...
local DP = _G.DeepPockets
DP.Scanner = {}

local ItemKey = DP.Util.ItemKey
local SafeCall = DP.Util.SafeCall

-- Simple category map for now, can be expanded later
local function GetCategory(classID, subClassID, link)
    if not classID then return "Miscellaneous" end
    -- Basic mapping based on item class
    if classID == Enum.ItemClass.Consumable then return "Consumable" end
    if classID == Enum.ItemClass.Tradegoods then return "Trade Goods" end
    if classID == Enum.ItemClass.Questitem then return "Quest" end
    if classID == Enum.ItemClass.Weapon then return "Equipment" end
    if classID == Enum.ItemClass.Armor then return "Equipment" end
    if classID == Enum.ItemClass.Gem then return "Gem" end
    return "Miscellaneous"
end

function DP.Scanner.ScanBags()
    DP.Migrate.Ensure()
    local db = DeepPocketsDB
    
    -- We don't wipe the whole table, we update distinct slots.
    -- But for clean state during full scan, wiping might be safer or we track seen keys.
    -- Spec implies we just scan into it. Let's wipe for correctness on full scan.
    wipe(db.inventory)

    local total = 0
    for bag = 0, 4 do
        local numSlots = C_Container.GetContainerNumSlots(bag) or 0
        for slot = 1, numSlots do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info and info.hyperlink then
                local itemID = info.itemID
                local count = info.stackCount or 1
                local quality = info.quality
                local icon = info.iconFileID
                local link = info.hyperlink
                
                -- Fallback name
                local name = C_Item.GetItemNameByID(itemID) or tostring(itemID)
                
                -- Get Class/Subclass safely
                local _, _, _, _, _, _, _, _, _, _, _, classID, subClassID = GetItemInfo(link)
                
                local key = ItemKey(bag, slot)
                local category = GetCategory(classID, subClassID, link)

                db.inventory[key] = {
                    itemKey = key,
                    bag = bag,
                    slot = slot,
                    itemID = itemID,
                    link = link,
                    name = name,
                    icon = icon,
                    count = count,
                    quality = quality,
                    classID = classID,
                    subClassID = subClassID,
                    category = category,
                    lastSeen = time()
                }
                total = total + 1
            end
        end
    end

    db.meta.lastScan = time()
    return total
end
