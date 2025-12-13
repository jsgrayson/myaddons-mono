-- ============================================================================
-- NAMESPACE & CONSTANTS
-- ============================================================================
DeepPockets = DeepPockets or {}
local addonName, addonTable = ...
local FRAME_POOL = {}
local CATEGORIES = {
    "Equipment", "Consumable", "Quest", "Trade Goods", "Gem", "Item Enhancement", 
    "Battle Pets", "Container", "Account", "Junk", "Miscellaneous"
}
-- ============================================================================
-- STATE
-- ============================================================================
local currentSearch = ""
local currentTab = "ALL" -- ALL, BAGS, REAGENT
local currentSort = "QUALITY" -- QUALITY, NAME, ID
local selectedItem = nil
local updateTimer = nil
local collapsedCategories = {} -- Key: Category Name, Value: true (collapsed)

-- ============================================================================
-- HELPERS
-- ============================================================================
local function EnsureUI()
    if DeepPocketsFrame and DeepPocketsFrame.Inset and DeepPocketsFrame.Inset.Scroll and DeepPocketsFrame.Inset.Scroll.Child then
        return true
    end
    return false
end


local function GetButton()
    if not EnsureUI() then return nil end
    local btn = tremove(FRAME_POOL)
    if not btn then
        btn = CreateFrame("Button", nil, DeepPocketsFrame.Inset.Scroll.Child, "DeepPocketsItemTemplate")
        btn:RegisterForClicks("LeftButtonUp", "RightButtonUp")
        btn:SetScript("OnEnter", function(self)
            GameTooltip:SetOwner(self, "ANCHOR_RIGHT")
            if self.bagID and self.slotID then
                GameTooltip:SetBagItem(self.bagID, self.slotID)
                GameTooltip:Show()
            end
            -- Clear New Item Glow on Hover?
            -- if self.itemData and self.itemData.isNew then 
            --    DeepPocketsDB.seen_items[self.itemData.id] = true
            --    self.NewGlow:Hide()
            -- end
        end)
        btn:SetScript("OnLeave", function(self) GameTooltip:Hide() end)
        btn:SetScript("OnClick", function(self, button)
            if button == "LeftButton" then
                if IsShiftKeyDown() then
                     -- Chat Link
                    if self.itemData and self.itemData.link then
                        ChatEdit_InsertLink(self.itemData.link)
                    end
                else
                    DeepPockets:SelectItem(self.itemData)
                    PlaySound(SOUNDKIT.IG_MAINMENU_OPTION_CHECKBOX_ON)
                end
            else
                if self.bagID and self.slotID then
                     UseContainerItem(self.bagID, self.slotID)
                end
            end
        end)
    end
    btn:Show()
    return btn
end

local HEADER_POOL = {}
local function GetHeader(text)
    local header = tremove(HEADER_POOL)
    if not header then
        header = CreateFrame("Button", nil, DeepPocketsFrame.Inset.Scroll.Child, "DeepPocketsCategoryHeaderTemplate")
        header:SetScript("OnClick", function(self)
            local cat = self.Text:GetText()
            collapsedCategories[cat] = not collapsedCategories[cat]
            DeepPockets:UpdateUI()
        end)
    end
    header.Text:SetText(text)
    header:Show()
    return header
end

local function RecycleFrames()
    local child = DeepPocketsFrame.Inset.Scroll.Child
    local children = {child:GetChildren()}
    for _, f in ipairs(children) do
        f:Hide()
        if f:GetAttribute("type") == "header" or f.Text then -- Loose check for header
             tinsert(HEADER_POOL, f)
        else
             tinsert(FRAME_POOL, f)
        end
    end
end

local function FormatGold(amount)
    local gold = math.floor(amount / 10000)
    local silver = math.floor((amount % 10000) / 100)
    local copper = amount % 100
    return "|cffffd700" .. gold .. "g|r |cffc7c7cf" .. silver .. "s|r |cffeda55f" .. copper .. "c|r"
end

-- ============================================================================
-- CATEGORY LOGIC
-- ============================================================================
function DeepPockets:GetCategoryForItem(itemID, quality, classID, subClassID)
    if not itemID then return "Miscellaneous" end
    
    -- Safety: If classID is missing, try Instant lookup
    if not classID or classID == -1 then
         local id, type, subType, equipLoc, icon, classID_i, subClassID_i = GetItemInfoInstant(itemID)
         if classID_i then 
             classID = classID_i 
             subClassID = subClassID_i
         end
    end

    -- Logic
    if quality == 0 then return "Junk" end
    if classID == 12 then return "Quest" end
    if classID == 2 or classID == 4 then return "Equipment" end
    if classID == 0 then return "Consumable" end
    if classID == 7 then return "Trade Goods" end
    if classID == 3 then return "Gem" end
    if classID == 8 then return "Item Enhancement" end
    if classID == 15 then return "Miscellaneous" end
    if classID == 17 then return "Battle Pets" end
    
    -- Fallbacks
    if classID == 1 then return "Container" end
    if classID == 5 or classID == 13 then return "Account" end
    
    return "Miscellaneous"
end


-- ============================================================================
-- CORE LOGIC
-- ============================================================================

-- ============================================================================
-- CORE LOGIC
-- ============================================================================

function DeepPockets:RebuildIndex()
    local db = DeepPocketsDB or {}
    local inv = db.inventory or {}
    
    -- Reset Indices
    db.index = { by_item = {}, by_category = {} }
    for _, cat in ipairs(CATEGORIES) do db.index.by_category[cat] = {} end
    
    for i, slotData in ipairs(inv) do
        -- CATEGORIZE HERE (Not in Scan)
        local cat = DeepPockets:GetCategoryForItem(slotData.id, slotData.quality, slotData.classID, slotData.subClassID)
        
        -- 1. Index by Category
        if not db.index.by_category[cat] then
             db.index.by_category["Miscellaneous"] = db.index.by_category["Miscellaneous"] or {}
             table.insert(db.index.by_category["Miscellaneous"], slotData)
        else
             table.insert(db.index.by_category[cat], slotData)
        end
        
        -- 2. Index by Item (Totals)
        local id = slotData.id
        if id then
            local entry = db.index.by_item[id]
            if not entry then
                entry = { total = 0, name = slotData.name, icon = slotData.icon, quality = slotData.quality }
                db.index.by_item[id] = entry
            end
            entry.total = entry.total + (slotData.count or 1)
        end
    end
end

function DeepPockets:ComputeDelta()
    local db = DeepPocketsDB or {}
    local inventory = db.inventory or {}
    local delta = db.delta
    local now = time()
    
    -- Clean expired
    for key, expiry in pairs(delta.expire_at) do
        if now > expiry then
            delta.is_new[key] = nil
            delta.expire_at[key] = nil
        end
    end
    
    for _, item in ipairs(inventory) do
        -- Key: Bag:Slot (e.g. "0:1")
        local key = item.bag .. ":" .. item.slot
        local prev = delta.last_seen[key]
        
        local isNew = false
        if not prev then
            isNew = true
        elseif prev.id ~= item.id then
            isNew = true
        elseif (item.count or 1) > (prev.count or 0) then
            isNew = true
        end
        
        if isNew then
            delta.is_new[key] = true
            delta.expire_at[key] = now + 600 -- 10 mins
        end
        
        -- Update Last Seen Snapshot
        delta.last_seen[key] = { id = item.id, count = item.count }
        
        -- Inject into item data for rendering
        item.isNew = delta.is_new[key]
    end
end

-- Pure Scanner: Captures Raw Slot Data Only
function DeepPockets:ScanBags()
    local inventoryData = {}
    local totalSlots = 0
    local usedSlots = 0
    
    for bag = 0, 5 do
        local slots = C_Container.GetContainerNumSlots(bag)
        totalSlots = totalSlots + slots
        for slot = 1, slots do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info and info.itemID then
                usedSlots = usedSlots + 1
                local itemID = info.itemID
                local count = info.stackCount or 1
                
                -- Attempt to get info (Cached or fallback)
                local itemName, itemLink, quality, _, _, classID, subClassID = GetItemInfo(itemID)
                if not quality then 
                     -- Fallback (Uncached)
                     quality = -1 
                     classID = -1
                     subClassID = -1
                     itemName = "Item " .. itemID
                end
                
                -- NOTE: No Categorization here. Pure Data.
                tinsert(inventoryData, {
                    id = itemID,
                    name = itemName,
                    count = count,
                    quality = quality,
                    classID = classID,
                    subClassID = subClassID,
                    icon = info.iconFileID,
                    bag = bag,
                    slot = slot,
                    link = itemLink,
                    loc = (bag == -1) and "Bank" or "Bag"
                })
            end
        end
    end

    if DeepPocketsDB then
        DeepPocketsDB.inventory = inventoryData
        DeepPocketsDB.meta = DeepPocketsDB.meta or {}
        DeepPocketsDB.meta.last_scan = time()
        DeepPocketsDB.meta.last_scan_items = #inventoryData
        DeepPocketsDB.meta.slots_used = usedSlots
        DeepPocketsDB.meta.slots_total = totalSlots
        
        -- PIPELINE:
        DeepPockets:ComputeDelta()    -- 1. Calculate New Items
        DeepPockets:RebuildIndex()    -- 2. Build UI Indices (Categorize Loop)
    end

    if DeepPocketsFrame and DeepPocketsFrame:IsShown() then
        self:UpdateUI()
    end
    
    return #inventoryData
end

function DeepPockets:UpdateUI()
    if not DeepPocketsFrame or not DeepPocketsFrame:IsShown() then return end
    
    local db = DeepPocketsDB
    local index = db and db.index
    local debug = db and db.settings and db.settings.debug
    
    -- SAFETY FALLBACK: Index Missing but Inventory Exists?
    if (not index or not index.by_category) or (not next(index.by_category)) then
        if db and db.inventory and #db.inventory > 0 then
             if debug then print("DP: Index empty. Triggering Rebuild...") end
             DeepPockets:RebuildIndex()
             index = db.index -- Refresh ref
        end
    end
    
    if debug then
        print("DP UPDATE: Using Index")
    end

    if not index or not index.by_category then return end
    
    local buckets = {}
    for _, cat in ipairs(CATEGORIES) do buckets[cat] = {} end
    
    -- Iterate Pre-Indexed Categories
    for catName, items in pairs(index.by_category) do
         if buckets[catName] then -- Only process valid categories
             for _, item in ipairs(items) do
                 local match = true
                 -- 1. Search Filter
                 if currentSearch ~= "" then
                      if not item.name or not string.find(string.lower(item.name), string.lower(currentSearch), 1, true) then
                          match = false
                      end
                 end
                 -- 2. Tab Filter (Bag/Bank/Reagent)
                 if currentTab == "BAGS" and item.bag > 4 then match = false end
                 if currentTab == "REAGENT" and item.bag ~= 5 then match = false end
                 -- if currentTab == "BANK" ... (Not fully implemented yet)
                 
                 if match then
                     tinsert(buckets[catName], item)
                 end
             end
         end
    end
    
    -- Sorting
    for _, cat in ipairs(CATEGORIES) do
        table.sort(buckets[cat], function(a, b)
            if currentSort == "QUALITY" then
                if a.quality ~= b.quality then return a.quality > b.quality end
            end
            return (a.name or "") < (b.name or "")
        end)
    end
    
    self:Render(buckets)
end

function DeepPockets:SelectItem(item)
    if selectedItem == item and item ~= nil then 
        -- Deselect if clicking same
        selectedItem = nil 
    else
        selectedItem = item
    end

    local details = DeepPocketsFrame.Details
    local inset = DeepPocketsFrame.Inset
    
    if selectedItem then
        -- Show Details, Shrink Inset
        details:Show()
        inset:SetPoint("BOTTOMRIGHT", -260, 30) -- Make room for 250px panel + margins
        
        -- Update Content
        details.Title:SetText(selectedItem.name or "Unknown")
        details.Icon:SetTexture(selectedItem.icon)
        local color = "|cffffffff"
        if selectedItem.quality then
            local r, g, b, hex = GetItemQualityColor(selectedItem.quality)
            details.Title:SetTextColor(r, g, b)
        end
        
        local info = "Count: " .. selectedItem.count .. "\n" ..
                     "Type: " .. (selectedItem.category or "Misc") .. "\n" ..
                     "Bag: " .. selectedItem.bag .. " Slot: " .. selectedItem.slot .. "\n" ..
                     "ID: " .. selectedItem.id
        details.Info:SetText(info)
        details.GoblinBtn:Enable()
    else
        -- Hide Details, Expand Inset
        details:Hide()
        inset:SetPoint("BOTTOMRIGHT", -10, 30)
    end
end

function DeepPockets:Render(buckets)
    if not DeepPocketsFrame.Inset.Scroll.Child then
        print("DP ERROR: Scroll Child missing!")
        return 
    end

    RecycleFrames()
    local yOffset = -5
    -- Visual Polish: Reduce columns slightly (10/16 -> 9/15) + Increase Gap
    local ROW_SIZE = DeepPocketsFrame.Details:IsShown() and 9 or 15 
    if ROW_SIZE < 1 then ROW_SIZE = 1 end

    local BTN_SIZE = 40
    local GAP = 6 -- Increased spacing
    local MARGIN = 10
    local totalRendered = 0
    
    for _, catName in ipairs(CATEGORIES) do
        local items = buckets[catName]
        if items and #items > 0 then
             -- Render Header
             local header = GetHeader(catName)
             header:SetPoint("TOPLEFT", 10, yOffset)
             header:SetPoint("RIGHT", -10, 0)
             -- Header Text Polish
             header.Text:SetText(catName .. " (" .. #items .. ")")

             yOffset = yOffset - 24 - GAP
             
             if not collapsedCategories[catName] then
                 local col = 0
                 local startY = yOffset
                 
                 for i, item in ipairs(items) do
                    totalRendered = totalRendered + 1
                    local btn = GetButton()
                    
                    if item.icon then btn.Icon:SetTexture(item.icon) else btn.Icon:SetTexture("Interface\\Icons\\INV_Misc_QuestionMark") end
                    btn.Count:SetText(item.count > 1 and item.count or "")
                    
                    if item.quality and item.quality > 1 then
                        local r, g, b = GetItemQualityColor(item.quality)
                        btn.Border:SetVertexColor(r, g, b)
                        btn.Border:Show()
                    else
                        btn.Border:Hide()
                    end
                    
                    if item.isNew then btn.NewGlow:Show() else btn.NewGlow:Hide() end

                    btn.bagID = item.bag
                    btn.slotID = item.slot
                    btn.itemData = item 
                    
                    -- Pos
                    local xPos = MARGIN + (col * (BTN_SIZE + GAP))
                    btn:SetPoint("TOPLEFT", xPos, yOffset)
                    
                    col = col + 1
                    if col >= ROW_SIZE then
                        col = 0
                        yOffset = yOffset - (BTN_SIZE + GAP)
                    end
                 end
                 if col > 0 then yOffset = yOffset - (BTN_SIZE + GAP) end
                 yOffset = yOffset - 5 -- Padding after section
             end
        end
    end
    
    -- Resize Scroll Child
    local height = math.abs(yOffset) + 50
    DeepPocketsFrame.Inset.Scroll.Child:SetHeight(height)
    
    local db = DeepPocketsDB
    if db and db.settings and db.settings.debug then
         print("DP RENDER: Rendered " .. totalRendered .. " buttons.")
    end
    
    -- Update Stats
    local meta = DeepPocketsDB.meta
    if meta then
        DeepPocketsFrame.Footer.SlotsText:SetText("Slots: " .. (meta.slots_used or "?") .. "/" .. (meta.slots_total or "?"))
    end
    DeepPocketsFrame.Footer.GoldText:SetText(FormatGold(GetMoney()))
end

-- ============================================================================
-- EVENTS
-- ============================================================================
local function OnEvent(self, event, ...)
    if event == "ADDON_LOADED" then
        local name = ...
        if name == addonName then
            DeepPocketsDB = DeepPocketsDB or {}
            
            -- SAFE MIGRATION (No Wipe)
            if not DeepPocketsDB.version or DeepPocketsDB.version < 1 then
                 DeepPocketsDB.version = 1
                 DeepPocketsDB.settings = DeepPocketsDB.settings or { debug = false, uiScale = 1.0, enabled = true }
                 DeepPocketsDB.inventory = DeepPocketsDB.inventory or {}
                 DeepPocketsDB.index = DeepPocketsDB.index or { by_item = {}, by_category = {} }
                 DeepPocketsDB.delta = DeepPocketsDB.delta or { last_seen = {}, is_new = {}, expire_at = {} }
                 DeepPocketsDB.meta = DeepPocketsDB.meta or {}
                 print("|cffDAA520DeepPockets|r: Database Migrated to v1.")
            else
                 -- Ensure tables exist even if version matches (integrity)
                 DeepPocketsDB.index = DeepPocketsDB.index or { by_item = {}, by_category = {} }
                 DeepPocketsDB.delta = DeepPocketsDB.delta or { last_seen = {}, is_new = {}, expire_at = {} }
                 DeepPocketsDB.settings = DeepPocketsDB.settings or { debug = false, uiScale = 1.0, enabled = true }
            end

            print("|cffDAA520DeepPockets|r: Loaded.")
        end
    elseif event == "PLAYER_LOGIN" then
        -- ====================================================================
        -- INPUT OWNERSHIP: B KEY HOOK (with Enable/Disable Safety)
        -- ====================================================================
        DeepPockets:RefreshKeybinds()
        
        -- ====================================================================
        -- UI INITIALIZATION
        -- ====================================================================
        if DeepPocketsFrame.Header and DeepPocketsFrame.Header.SearchBox then
            DeepPocketsFrame.Header.SearchBox:SetScript("OnTextChanged", function(self)
                currentSearch = self:GetText()
                DeepPockets:UpdateUI() 
            end)
            
            -- ESC clears search or closes DP
            DeepPocketsFrame.Header.SearchBox:SetScript("OnEscapePressed", function(self)
                if currentSearch ~= "" then
                    self:SetText("")
                    currentSearch = ""
                    DeepPockets:UpdateUI()
                else
                    DeepPockets:CloseUI()
                end
                self:ClearFocus()
            end)
        end
        
        if DeepPocketsFrame.Header.TabAll then
            DeepPocketsFrame.Header.TabAll:SetScript("OnClick", function() currentTab = "ALL"; DeepPockets:UpdateUI() end)
            DeepPocketsFrame.Header.TabBags:SetScript("OnClick", function() currentTab = "BAGS"; DeepPockets:UpdateUI() end)
            DeepPocketsFrame.Header.TabReagent:SetScript("OnClick", function() currentTab = "REAGENT"; DeepPockets:UpdateUI() end)
        end
        
        DeepPockets:ScanBags()
        
    elseif event == "BAG_UPDATE_DELAYED" then
        if updateTimer then updateTimer:Cancel() end
        updateTimer = C_Timer.NewTimer(0.25, function() DeepPockets:ScanBags() end)
        
    elseif event == "PLAYER_MONEY" then
         -- Gold live update (UI-only, no rescan)
         if DeepPocketsFrame and DeepPocketsFrame.Footer and DeepPocketsFrame.Footer.GoldText then
             DeepPocketsFrame.Footer.GoldText:SetText(FormatGold(GetMoney()))
         end
         
    elseif event == "PLAYER_LOGOUT" then
        if DeepPocketsDB then
             DeepPocketsDB.meta.last_logout = time()
        end
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PLAYER_LOGOUT")
eventFrame:RegisterEvent("BAG_UPDATE_DELAYED")
eventFrame:RegisterEvent("PLAYER_MONEY")
eventFrame:SetScript("OnEvent", OnEvent)

-- ============================================================================
-- BAG REPLACEMENT LOGIC
-- ============================================================================

function DeepPockets:RefreshKeybinds()
    -- Clear any existing override bindings first (prevent duplicates on /reload)
    if DeepPocketsFrame then
        ClearOverrideBindings(DeepPocketsFrame)
    end
    
    -- Only set override if DeepPockets is enabled
    if DeepPocketsDB and DeepPocketsDB.settings and DeepPocketsDB.settings.enabled then
        if not DeepPocketsFrame then
            print("|cffDAA520DeepPockets|r: Error - Frame not ready for keybind setup")
            return
        end
        
        -- Create toggle button if it doesn't exist
        if not _G["DeepPocketsToggleButton"] then
            local toggleBtn = CreateFrame("Button", "DeepPocketsToggleButton", UIParent)
            toggleBtn:SetScript("OnClick", function()
                DeepPockets:Toggle()
            end)
        end
        
        -- Set B key override
        SetOverrideBindingClick(DeepPocketsFrame, true, "B", "DeepPocketsToggleButton")
    end
end

function DeepPockets:CloseUI()
    DeepPocketsFrame:Hide()
    
    -- Restore Blizzard Bags (proper cleanup)
    for i=1, NUM_CONTAINER_FRAMES do
        local f = _G["ContainerFrame"..i]
        if f then
            f:EnableMouse(true)
            f:SetAlpha(1)
            -- Don't force show, let Blizzard UI handle visibility
        end
    end
end

function DeepPockets:OpenUI()
    -- Check if DeepPockets is enabled (allow user to disable it)
    if DeepPocketsDB and DeepPocketsDB.settings and DeepPocketsDB.settings.enabled == false then
        -- Fallback to Blizzard bags
        ToggleAllBags()
        return
    end
    
    DeepPocketsFrame:Show()
    DeepPocketsFrame:SetFrameStrata("HIGH")
    DeepPocketsFrame:SetFrameLevel(200)
    CloseAllBags()
    
    -- Aggressive Hide Blizzard Bags & Steal Input
    for i=1, NUM_CONTAINER_FRAMES do
        local f = _G["ContainerFrame"..i]
        if f then
            f:Hide()
            f:EnableMouse(false)
            f:SetAlpha(0)
        end
    end
    
    -- Auto-focus search box
    if DeepPocketsFrame.Header and DeepPocketsFrame.Header.SearchBox then
        DeepPocketsFrame.Header.SearchBox:SetFocus()
    end
    
    local db = DeepPocketsDB
    if not db or not db.inventory or #db.inventory == 0 then
        -- Force scan if empty
        DeepPockets:ScanBags()
    else
        DeepPockets:UpdateUI()
    end
end

function DeepPockets:Toggle()
    if DeepPocketsFrame:IsShown() then
        DeepPockets:CloseUI()
    else
        DeepPockets:OpenUI()
    end
end

-- Hook Blizzard Bag Functions
local function HookBagToggle()
    if not IsShiftKeyDown() then
        DeepPockets:Toggle()
    end
end

hooksecurefunc("ToggleAllBags", function()
    if not IsShiftKeyDown() then
        DeepPockets:Toggle()
    end
end)

hooksecurefunc("OpenAllBags", function()
    if not IsShiftKeyDown() then
        DeepPockets:OpenUI()
    end
end)

-- Slash Command Handler
SLASH_DEEPPOCKETS1 = "/dp"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
    
    if cmd == "scan" then
        local count = DeepPockets:ScanBags()
        print("|cffDAA520DeepPockets|r: Scanned " .. count .. " items (Pipeline Triggered).")
        
    elseif cmd == "refresh" then
        if DeepPocketsDB and DeepPocketsDB.index then
             DeepPockets:UpdateUI()
             print("|cffDAA520DeepPockets|r: Refreshed UI from Index.")
        else
             print("|cffDAA520DeepPockets|r: No index found. Run /dp scan first.")
        end
        
    elseif cmd == "debug" then
        if DeepPocketsDB and DeepPocketsDB.settings then
            if arg == "on" then DeepPocketsDB.settings.debug = true
            elseif arg == "off" then DeepPocketsDB.settings.debug = false
            else DeepPocketsDB.settings.debug = not DeepPocketsDB.settings.debug end
            print("|cffDAA520DeepPockets|r: Debug Mode is now " .. (DeepPocketsDB.settings.debug and "ON" or "OFF"))
        end
        
    elseif cmd == "resetdb" then
        DeepPocketsDB = {
             version = 1,
             settings = { debug = false, uiScale = 1.0, enabled = true },
             inventory = {},
             index = { by_item = {}, by_category = {} },
             delta = { last_seen = {}, is_new = {}, expire_at = {} },
             meta = {}
        }
        ReloadUI() -- Force reload to ensure clean state
        
    elseif cmd == "dump" then
        if not DeepPocketsDB then return end
        local inv = DeepPocketsDB.inventory and #DeepPocketsDB.inventory or 0
        local cats = DeepPocketsDB.index and DeepPocketsDB.index.by_category and 0 or 0
        if DeepPocketsDB.index and DeepPocketsDB.index.by_category then
            for _ in pairs(DeepPocketsDB.index.by_category) do cats = cats + 1 end
        end
        local newItems = 0
        if DeepPocketsDB.delta and DeepPocketsDB.delta.is_new then
            for _ in pairs(DeepPocketsDB.delta.is_new) do newItems = newItems + 1 end
        end
        print("DP DUMP: Inv="..inv..", Cats="..cats..", New="..newItems..", Money="..GetMoney())

    elseif cmd == "rebuild" then
        DeepPockets:RebuildIndex()
        DeepPockets:UpdateUI()
        print("|cffDAA520DeepPockets|r: Index Rebuilt & UI Updated.")

    elseif cmd == "sanity" then
        if not DeepPocketsDB then return end
        local passed = true
        
        -- Check 1: Count Consistency
        local invCount = DeepPocketsDB.inventory and #DeepPocketsDB.inventory or 0
        local indexCount = 0
        if DeepPocketsDB.index and DeepPocketsDB.index.by_category then
            for _, list in pairs(DeepPocketsDB.index.by_category) do
                indexCount = indexCount + #list
            end
        end
        if invCount ~= indexCount then 
            print("FAIL: InvCount("..invCount..") != IndexCount("..indexCount..")")
            passed = false 
        end
        
        -- Check 2: Duplicates
        local slots = {}
        if DeepPocketsDB.inventory then
            for _, item in ipairs(DeepPocketsDB.inventory) do
                local key = item.bag..":"..item.slot
                if slots[key] then
                    print("FAIL: Duplicate Slot Key " .. key)
                    passed = false
                    break
                end
                slots[key] = true
            end
        end
        
        -- Check 3: Integrity
        if DeepPocketsDB.index and DeepPocketsDB.index.by_category and DeepPocketsDB.index.by_item then
            for cat, items in pairs(DeepPocketsDB.index.by_category) do
                for _, item in ipairs(items) do
                    if item.id and not DeepPocketsDB.index.by_item[item.id] then
                         print("FAIL: Item " .. item.name .. " (" .. item.id .. ") missing from Totals Index.")
                         passed = false
                    end
                end
            end
        end
        
        if passed then
            print("|cff00FF00DP SANITY PASS|r")
            print(string.format('SANITY_RESULT {"addon":"DeepPockets","status":"OK","checks":3,"failures":0}'))
        else
            print("|cffrr0000DP SANITY FAIL|r")
            print(string.format('SANITY_RESULT {"addon":"DeepPockets","status":"FAIL","checks":3,"failures":1}')) -- Simplified failure count
        end
        
    else
        DeepPockets:Toggle()
    end
end
