local addonName, addonTable = ...

-- ============================================================================
-- CONSTANTS & STATE
-- ============================================================================
local FRAME_POOL = {}
local CATEGORIES = {
    "Equipment",
    "Consumable",
    "Trade Goods",
    "Quest",
    "Junk",
    "Miscellaneous"
}
local currentSearch = ""

-- ============================================================================
-- HELPERS
-- ============================================================================
local function GetButton()
    -- Simple frame pool recycler
    local btn = tremove(FRAME_POOL)
    if not btn then
        btn = CreateFrame("Button", nil, DeepPocketsFrame.Inset.Scroll.Child, "DeepPocketsItemTemplate")
    end
    btn:Show()
    return btn
end

local function RecycleButtons()
    local child = DeepPocketsFrame.Inset.Scroll.Child
    local children = {child:GetChildren()}
    for _, btn in ipairs(children) do
        btn:Hide()
        tinsert(FRAME_POOL, btn)
    end
end

local function FormatGold(amount)
    local gold = math.floor(amount / 10000)
    local silver = math.floor((amount % 10000) / 100)
    local copper = amount % 100
    return "|cffffd700" .. gold .. "g|r |cffc7c7cf" .. silver .. "s|r"
end

-- ============================================================================
-- CATEGORIZATION LOGIC
-- ============================================================================
local function GetCategory(itemID, quality, classID, subClassID)
    if quality == 0 then return "Junk" end
    if classID == 12 then return "Quest" end -- Quest Items
    if classID == 2 or classID == 4 then return "Equipment" end -- Weapons & Armor
    if classID == 0 then return "Consumable" end -- Consumables
    if classID == 7 then return "Trade Goods" end -- Trade Goods
    return "Miscellaneous"
end

-- ============================================================================
-- CORE: SCAN & RENDER
-- ============================================================================
local function UpdateBags()
    RecycleButtons()
    
    local buckets = {}
    for _, cat in ipairs(CATEGORIES) do buckets[cat] = {} end
    
    local totalSlots = 0
    local usedSlots = 0
    
    -- 1. SCAN BAGS
    for bag = 0, 4 do
        local slots = C_Container.GetContainerNumSlots(bag)
        totalSlots = totalSlots + slots
        for slot = 1, slots do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info then
                usedSlots = usedSlots + 1
                local _, _, quality, _, _, classID, subClassID = GetItemInfo(info.itemID)
                
                -- Filter by Search
                local match = true
                if currentSearch ~= "" then
                    local name = GetItemInfo(info.itemID)
                    if not name or not string.find(string.lower(name), string.lower(currentSearch), 1, true) then
                        match = false
                    end
                end
                
                if match then
                    local cat = GetCategory(info.itemID, quality, classID, subClassID)
                    tinsert(buckets[cat], {
                        bag = bag,
                        slot = slot,
                        icon = info.iconFileID,
                        count = info.stackCount,
                        quality = quality,
                        link = info.hyperlink
                    })
                end
            end
        end
    end
    
    -- 2. RENDER GRID
    local child = DeepPocketsFrame.Inset.Scroll.Child
    local yOffset = -10
    local ROW_SIZE = 10 -- Items per row
    local BTN_SIZE = 40
    
    for _, catName in ipairs(CATEGORIES) do
        local items = buckets[catName]
        if #items > 0 then
            
            -- Draw Category Header (Simulated with a label button for now if we wanted, skipping for clean grid)
            -- Ideally we'd put a text header here, but for v0.1 we'll just group them visually.
            
            local col = 0
            for i, item in ipairs(items) do
                local btn = GetButton()
                btn.Icon:SetTexture(item.icon)
                btn.Count:SetText(item.count > 1 and item.count or "")
                
                -- Quality Border
                if item.quality and item.quality > 1 then
                    local r, g, b = GetItemQualityColor(item.quality)
                    btn.Border:SetVertexColor(r, g, b)
                    btn.Border:Show()
                else
                    btn.Border:Hide()
                end
                
                -- Store data for OnClick/Tooltip
                btn.bagID = item.bag
                btn.slotID = item.slot
                
                -- Position
                btn:SetPoint("TOPLEFT", 10 + (col * BTN_SIZE), yOffset)
                
                col = col + 1
                if col >= ROW_SIZE then
                    col = 0
                    yOffset = yOffset - BTN_SIZE
                end
            end
            
            -- Add spacing between categories
            if col > 0 then yOffset = yOffset - BTN_SIZE end
            yOffset = yOffset - 10 
        end
    end
    
    -- Update Stats
    DeepPocketsFrame.Footer.SlotsText:SetText("Slots: " .. usedSlots .. "/" .. totalSlots)
    DeepPocketsFrame.Footer.GoldText:SetText(FormatGold(GetMoney()))
end

-- ============================================================================
-- INIT & EVENTS
-- ============================================================================
local function OnEvent(self, event, ...)
    if event == "PLAYER_LOGIN" then
        -- Hook Search
        DeepPocketsFrame.Header.SearchBox:SetScript("OnTextChanged", function(self)
            currentSearch = self:GetText()
            UpdateBags()
        end)
        
        -- Hook Sort
        DeepPocketsFrame.Header.SortButton:SetScript("OnClick", function()
            C_Container.SortBags() -- Uses default WoW sort API
        end)
        
        UpdateBags()
        
    elseif event == "BAG_UPDATE" or event == "PLAYER_MONEY" then
        if DeepPocketsFrame:IsShown() then
            UpdateBags()
        end
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("BAG_UPDATE")
eventFrame:RegisterEvent("PLAYER_MONEY")
eventFrame:SetScript("OnEvent", OnEvent)

-- Toggle Command
SLASH_DEEPPOCKETS1 = "/dp"
SLASH_DEEPPOCKETS2 = "/deeppockets"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    if DeepPocketsFrame:IsShown() then DeepPocketsFrame:Hide() else DeepPocketsFrame:Show(); UpdateBags() end
end
