DeepPockets = DeepPockets or {}
local addonName = ...
DeepPockets.name = addonName

-- 1. DB Initialization
local function InitDB()
    DeepPocketsDB = DeepPocketsDB or {
        version = 1,
        chars = {}
    }
    local db = DeepPocketsDB
    
    local charKey = UnitName("player") .. "-" .. GetRealmName()
    db.chars[charKey] = db.chars[charKey] or {
        lastScan = 0,
        bags = {}
    }
    return db.chars[charKey]
end

-- 2. Scanning Logic (Retail Safe)
local function ScanBags()
    local charDB = InitDB()
    local total = 0
    
    for bag = 0, 4 do
        local bagStr = tostring(bag)
        charDB.bags[bagStr] = charDB.bags[bagStr] or {}
        local bagTable = charDB.bags[bagStr]
        wipe(bagTable) -- Clear old data for this bag
        
        local numSlots = C_Container.GetContainerNumSlots(bag) or 0
        for slot = 1, numSlots do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info and info.hyperlink then
                local link = info.hyperlink
                local itemID = info.itemID
                local count = info.stackCount or 1
                local icon = info.iconFileID
                local quality = info.quality
                
                -- Lazy GetItemInfo (safe fallbacks)
                local name = C_Item.GetItemNameByID(itemID) or tostring(itemID)
                local _, _, _, _, _, _, _, _, equipLoc, _, _, classID, subClassID = GetItemInfo(link)
                
                -- itemRecord
                bagTable[tostring(slot)] = {
                    itemID = itemID,
                    link = link,
                    count = count,
                    icon = icon,
                    quality = quality,
                    name = name,
                    classID = classID or 0,
                    subClassID = subClassID or 0,
                    equipLoc = equipLoc or "",
                    -- dpCategory = nil -- Optional placeholder
                }
                total = total + 1
            end
        end
    end
    
    charDB.lastScan = time()
    return total
end

-- 3. Slash Commands
SLASH_DEEPPOCKETS1 = "/dp"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    msg = tostring(msg or ""):lower()
    local cmd = msg:match("^(%S+)") or ""

    if cmd == "scan" then
        local count = ScanBags()
        print("|cffDAA520DeepPockets|r: Scanned " .. count .. " items.")
    elseif cmd == "dump" then
        local charDB = InitDB()
        local bagCount = 0
        local itemCount = 0
        for b, slots in pairs(charDB.bags) do
            for _ in pairs(slots) do itemCount = itemCount + 1 end
            bagCount = bagCount + 1
        end
        print("|cffDAA520DeepPockets|r: Items=" .. itemCount .. " in " .. bagCount .. " bags. LastScan=" .. (charDB.lastScan or "Never"))
    elseif cmd == "sanity" then
         print("|cffDAA520DeepPockets|r: Sanity check OK. Version=" .. (DeepPocketsDB and DeepPocketsDB.version or "nil"))
    elseif cmd == "resetdb" then
        DeepPocketsDB = nil
        InitDB()
        print("|cffDAA520DeepPockets|r: DB Reset.")
    else
        print("|cffDAA520DeepPockets|r: /dp scan | dump | sanity | resetdb")
    end
end

-- 4. Event Handling (Minimal)
local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("PLAYER_LOGIN")

f:SetScript("OnEvent", function(_, event, arg1)
    if event == "ADDON_LOADED" and arg1 == addonName then
        InitDB()
    elseif event == "PLAYER_LOGIN" then
        print("|cffDAA520DeepPockets|r: Backend initialized.")
    end
end)
