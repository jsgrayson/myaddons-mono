-- DeepPockets.lua
local addonName, addon = ...
print("DeepPockets: File Loading...")

DeepPocketsDB = DeepPocketsDB or {}
DeepPocketsDB.settings = DeepPocketsDB.settings or { uiScale = 1.0 }

-- Constants
local TILE_SIZE = 37
local PADDING = 5
local COLS = 10

-- UI Elements
addon.Frame = nil
addon.ScrollFrame = nil
addon.Grid = nil
addon.ItemButtons = {}
addon.Tabs = {}

-- Data
addon.BagItems = {}
addon.BankItems = {}
addon.WarbandItems = {}
addon.Sections = {}
addon.CurrentTab = "BAGS" -- BAGS, BANK, WARBAND

-- Event Frame
local f = CreateFrame("Frame")
f:RegisterEvent("ADDON_LOADED")
f:RegisterEvent("BAG_UPDATE")
f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:RegisterEvent("BANKFRAME_OPENED")
f:RegisterEvent("BANKFRAME_CLOSED")
f:RegisterEvent("PLAYERBANKSLOTS_CHANGED")
f:RegisterEvent("ZONE_CHANGED_NEW_AREA")
f:RegisterEvent("MERCHANT_SHOW")
f:RegisterEvent("AUCTION_HOUSE_SHOW")
f:RegisterEvent("MERCHANT_CLOSED")
f:RegisterEvent("AUCTION_HOUSE_CLOSED")
f:RegisterEvent("GET_ITEM_INFO_RECEIVED")
f:RegisterEvent("PLAYER_LOGOUT")
f:RegisterEvent("PLAYER_LEAVING_WORLD")
f:RegisterEvent("BAG_UPDATE_DELAYED")

-- Context Logic
addon.FilterMode = "ALL"

f:SetScript("OnEvent", function(self, event, ...)
    if event == "ADDON_LOADED" and ... == addonName then
        addon:InitUI()
        print("|cff00ff00DeepPockets|r Loaded. Premium Bag Interface Active.")
    elseif event == "BAG_UPDATE" or event == "PLAYER_ENTERING_WORLD" then
        if addon.Frame and addon.Frame:IsShown() then
            addon:ScanBags()
            if addon.CurrentTab == "BAGS" then addon:RenderGrid() end
        end
        -- DEBUG: Force save on login to test persistence
        if event == "PLAYER_ENTERING_WORLD" then
            C_Timer.After(5, function() addon:SaveData() end)
        end
    elseif event == "BANKFRAME_OPENED" then
        addon.Frame:Show()
        addon:SetTab("BANK")
    elseif event == "BANKFRAME_CLOSED" then
        addon:SetTab("BAGS")
    elseif event == "PLAYERBANKSLOTS_CHANGED" then
        if addon.CurrentTab == "BANK" then
            addon:ScanBank()
            addon:RenderGrid()
        end
    -- Context Events
    elseif event == "ZONE_CHANGED_NEW_AREA" then
        addon:CheckContext()
    elseif event == "MERCHANT_SHOW" then
        addon.FilterMode = "VENDOR"
        addon:RenderGrid()
    elseif event == "AUCTION_HOUSE_SHOW" then
        addon.FilterMode = "AH"
        addon:RenderGrid()
    elseif event == "MERCHANT_CLOSED" or event == "AUCTION_HOUSE_CLOSED" then
        addon:CheckContext() -- Revert to zone-based context
    elseif event == "GET_ITEM_INFO_RECEIVED" then
        -- Debounce this? For now just re-render if visible
        if addon.Frame and addon.Frame:IsShown() then
            -- We might need to re-scan if we stored nil classes
            addon:ScanBags() 
            addon:RenderGrid()
        end
    elseif event == "PLAYER_LOGOUT" or event == "PLAYER_LEAVING_WORLD" then
        addon:SaveData()
    elseif event == "BAG_UPDATE_DELAYED" then
        -- Aggressively hide default bags when they try to show
        if addon.Frame and addon.Frame:IsShown() then
            if ContainerFrameCombinedBags then ContainerFrameCombinedBags:Hide() end
            for i = 0, 12 do
                local bag = _G["ContainerFrame"..i]
                if bag and bag:IsShown() then bag:Hide() end
            end
        end
    end
end)

-- Manual Save Command
SLASH_DEEPPOCKETSSAVE1 = "/dpsave"
SlashCmdList["DEEPPOCKETSSAVE"] = function(msg)
    addon:SaveData()
end

-- Slash Command
SLASH_DEEPPOCKETS1 = "/dp"
SLASH_DEEPPOCKETS2 = "/deeppockets"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    if addon.Frame then
        if addon.Frame:IsShown() then
            addon.Frame:Hide()
        else
            addon.Frame:Show()
            addon:ScanBags()
            addon:RenderGrid()
        end
    else
        print("DeepPockets: UI not initialized yet.")
    end
end

function addon:SaveData()
    -- Force Scan before saving to ensure we have data
    addon:ScanBags()
    -- Bank/Warband only scannable if open, but we save what we have.
    
    local name, realm = UnitName("player"), GetRealmName()
    local key = name .. " - " .. realm
    
    -- Initialize DB structure if needed
    DeepPocketsDB.global = DeepPocketsDB.global or {}
    DeepPocketsDB.global.Inventory = DeepPocketsDB.global.Inventory or {}
    DeepPocketsDB.global.Characters = DeepPocketsDB.global.Characters or {}
    
    -- Save Character Info
    DeepPocketsDB.global.Characters[key] = {
        class = select(2, UnitClass("player")),
        level = UnitLevel("player"),
        race = UnitRace("player"),
        zone = GetZoneText(),
        timestamp = time()
    }
    
    -- Save Inventory
    -- We only save what we've scanned.
    DeepPocketsDB.global.Inventory[key] = DeepPocketsDB.global.Inventory[key] or {}
    
    -- Helper to merge tables
    local function MergeItems(source)
        if not source then return end
        for _, item in ipairs(source) do
            table.insert(DeepPocketsDB.global.Inventory[key], {
                id = item.id or GetItemInfoInstant(item.link),
                count = item.count,
                loc = (item.bag == -1) and "Bank" or "Bag", -- Simplified location
                link = item.link
            })
        end
    end
    
    -- Clear old data for this char to avoid dupes? 
    -- For MVP, let's just overwrite the list.
    DeepPocketsDB.global.Inventory[key] = {}
    MergeItems(addon.BagItems)
    MergeItems(addon.BankItems)
    MergeItems(addon.WarbandItems)
    
    print("DeepPockets: Data Saved for " .. key)
end

function addon:CheckContext()
    local _, instanceType = IsInInstance()
    if instanceType == "raid" or instanceType == "party" then
        addon.FilterMode = "RAID"
    else
        addon.FilterMode = "ALL"
    end
    addon:RenderGrid()
end

function addon:InitUI()
    -- Main Frame
    local f = CreateFrame("Frame", "DeepPocketsFrame", UIParent, "BackdropTemplate")
    f:SetSize(450, 550) -- Increased height for tabs
    f:SetPoint("BOTTOMRIGHT", UIParent, "BOTTOMRIGHT", -50, 50)
    f:SetBackdrop({
        bgFile = "Interface\\Tooltips\\UI-Tooltip-Background",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        tile = true, tileSize = 16, edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    f:SetBackdropColor(0, 0, 0, 0.9)
    f:EnableMouse(true)
    f:SetMovable(true)
    f:SetResizable(true)
    f:SetMinResize(300, 300)
    f:SetMaxResize(800, 900)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)
    f:Hide()
    
    -- Resize Grip
    local resizer = CreateFrame("Button", nil, f)
    resizer:SetSize(16, 16)
    resizer:SetPoint("BOTTOMRIGHT")
    resizer:SetNormalTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Up")
    resizer:SetHighlightTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Highlight")
    resizer:SetPushedTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Down")
    resizer:SetScript("OnMouseDown", function(self) f:StartSizing("BOTTOMRIGHT") end)
    resizer:SetScript("OnMouseUp", function(self) f:StopMovingOrSizing() end)
    
    -- Title
    f.Title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    f.Title:SetPoint("TOPLEFT", 10, -10)
    f.Title:SetText("DeepPockets")
    
    -- Close Button
    f.Close = CreateFrame("Button", nil, f, "UIPanelCloseButton")
    f.Close:SetPoint("TOPRIGHT", -5, -5)
    
    -- Search Box
    f.Search = CreateFrame("EditBox", nil, f, "InputBoxTemplate")
    f.Search:SetSize(150, 20)
    f.Search:SetPoint("TOPRIGHT", -30, -10)
    f.Search:SetAutoFocus(false)
    f.Search:SetScript("OnTextChanged", function(self)
        addon:RenderGrid() -- Re-render on search
    end)
    
    -- Tabs
    local function CreateTab(id, text, x)
        local tab = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
        tab:SetSize(80, 25)
        tab:SetPoint("TOPLEFT", x, -35)
        tab:SetText(text)
        tab:SetScript("OnClick", function() addon:SetTab(id) end)
        return tab
    end
    
    addon.Tabs["BAGS"] = CreateTab("BAGS", "Bags", 10)
    addon.Tabs["BANK"] = CreateTab("BANK", "Bank", 95)
    addon.Tabs["WARBAND"] = CreateTab("WARBAND", "Warband", 180)
    
    -- Scroll Frame
    local sf = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
    sf:SetPoint("TOPLEFT", 10, -70) -- Moved down for tabs
    sf:SetPoint("BOTTOMRIGHT", -30, 40)
    
    -- Content Frame (The Grid)
    local content = CreateFrame("Frame")
    content:SetSize(400, 800) -- Dynamic height later
    sf:SetScrollChild(content)
    addon.Grid = content
    addon.ScrollFrame = sf
    addon.Frame = f
    
    -- Footer: Scale Slider
    local burnBtn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    burnBtn:SetSize(100, 25)
    burnBtn:SetPoint("BOTTOMLEFT", 10, 10)
    burnBtn:SetText("Burn Trash")
    burnBtn:SetScript("OnClick", function()
        print("|cffff0000DeepPockets|r: Incinerator not yet linked to server.")
    end)
    
    local cleanupBtn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    cleanupBtn:SetSize(100, 25)
    cleanupBtn:SetPoint("LEFT", burnBtn, "RIGHT", 10, 0)
    cleanupBtn:SetText("Cleanup")
    cleanupBtn:SetScript("OnClick", function()
        addon:CleanupBags()
    end)
    
    local scaleLabel = f:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    scaleLabel:SetPoint("BOTTOMRIGHT", -120, 18)
    scaleLabel:SetText("Scale: 100%")
    
    local scaleSlider = CreateFrame("Slider", nil, f, "OptionsSliderTemplate")
    scaleSlider:SetPoint("BOTTOMRIGHT", -10, 10)
    scaleSlider:SetSize(100, 20)
    scaleSlider:SetMinMaxValues(0.5, 1.5)
    scaleSlider:SetValueStep(0.05)
    scaleSlider:SetValue(DeepPocketsDB.settings.uiScale or 1.0)
    scaleSlider:SetScript("OnValueChanged", function(self, value)
        f:SetScale(value)
        scaleLabel:SetText("Scale: " .. math.floor(value * 100) .. "%")
        DeepPocketsDB.settings.uiScale = value
    end)
    
    -- Apply saved scale
    f:SetScale(DeepPocketsDB.settings.uiScale or 1.0)
    
    -- Hooks for bag opening - HIDE DEFAULT BAGS
    hooksecurefunc("OpenAllBags", function()
        -- Hide default bags
        if ContainerFrameCombinedBags then ContainerFrameCombinedBags:Hide() end
        for i = 0, 12 do
            local bag = _G["ContainerFrame"..i]
            if bag then bag:Hide() end
        end
        -- Show DeepPockets
        f:Show()
        addon:ScanBags()
        addon:RenderGrid()
    end)
    
    hooksecurefunc("CloseAllBags", function()
        f:Hide()
    end)
    
    hooksecurefunc("ToggleAllBags", function() 
        if f:IsShown() then
            f:Hide()
        else
            -- Hide default bags
            if ContainerFrameCombinedBags then ContainerFrameCombinedBags:Hide() end
            for i = 0, 12 do
                local bag = _G["ContainerFrame"..i]
                if bag then bag:Hide() end
            end
            -- Show DeepPockets
            f:Show()
            addon:ScanBags()
            addon:RenderGrid()
        end
    end)
    
    addon:SetTab("BAGS")

    -- Add Destroy Tab Button (Moved from top level)
    if f then
        addon.Tabs["DESTROY"] = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
        addon.Tabs["DESTROY"]:SetSize(80, 25)
        addon.Tabs["DESTROY"]:SetPoint("TOPLEFT", 10, -65) -- Second Row
        addon.Tabs["DESTROY"]:SetText("Destroy")
        addon.Tabs["DESTROY"]:SetScript("OnClick", function() addon:SetTab("DESTROY") end)
    end
end

function addon:SetTab(tabId)
    addon.CurrentTab = tabId
    
    -- Update Tab Visuals
    for id, btn in pairs(addon.Tabs) do
        if id == tabId then
            btn:Disable() -- Selected
        else
            btn:Enable()
        end
    end
    
    -- Scan if needed
    if tabId == "BANK" then addon:ScanBank()
    elseif tabId == "WARBAND" then addon:ScanWarband()
    else addon:ScanBags() end
    
    addon:RenderGrid()
end

function addon:ScanBags()
    addon.BagItems = {}
    addon:ScanContainerRange(0, 4, addon.BagItems)
    addon:SortItems(addon.BagItems)
end

function addon:ScanBank()
    addon.BankItems = {}
    -- Bank (-1)
    addon:ScanContainerRange(-1, -1, addon.BankItems)
    -- Reagent Bank (-3)
    addon:ScanContainerRange(-3, -3, addon.BankItems)
    -- Bank Bags (5-11)
    addon:ScanContainerRange(5, 11, addon.BankItems)
    addon:SortItems(addon.BankItems)
end

function addon:ScanWarband()
    addon.WarbandItems = {}
    -- Warband Bank (13-17 usually, but let's be safe and check availability)
    -- Assuming 5 tabs for now
    addon:ScanContainerRange(13, 17, addon.WarbandItems)
    addon:SortItems(addon.WarbandItems)
end

function addon:ScanContainerRange(startID, endID, targetTable)
    for bag = startID, endID do
        -- Check if bag exists (for bank bags)
        local slots = C_Container.GetContainerNumSlots(bag)
        if slots > 0 then
            for slot = 1, slots do
                local info = C_Container.GetContainerItemInfo(bag, slot)
                if info then
                    -- Use GetItemInfoInstant for reliable ClassID (Synchronous)
                    local _, _, _, _, _, classID, subclassID = C_Item.GetItemInfoInstant(info.itemID)
                    local itemLink = info.hyperlink
                    local quality = select(3, GetItemInfo(itemLink)) or 1

                    table.insert(targetTable, {
                        bag = bag,
                        slot = slot,
                        texture = info.iconFileID,
                        count = info.stackCount,
                        quality = quality,
                        link = itemLink,
                        classID = classID or 15, -- Default to Misc
                        subclassID = subclassID or 0
                    })
                end
            end
        end
    end
end

function addon:SortItems(itemTable)
    table.sort(itemTable, function(a, b)
        if a.quality ~= b.quality then
            return a.quality > b.quality
        end
        return (a.link or "") < (b.link or "")
    end)
end

function addon:CleanupBags()
    print("DeepPockets: Sorting items...")
    if addon.CurrentTab == "BAGS" then
        if C_Container.SortBags then C_Container.SortBags() end
    elseif addon.CurrentTab == "BANK" then
        if C_Container.SortBankBags then C_Container.SortBankBags() end
    elseif addon.CurrentTab == "WARBAND" then
        if C_Container.SortAccountBankBags then C_Container.SortAccountBankBags() end
    end
    
    -- Re-scan after a short delay to update UI
    C_Timer.After(1, function() 
        if addon.CurrentTab == "BANK" then addon:ScanBank()
        elseif addon.CurrentTab == "WARBAND" then addon:ScanWarband()
        else addon:ScanBags() end
        addon:RenderGrid()
    end)
end

function addon:RenderGrid()
    -- Select Data Source
    local dataSource = addon.BagItems
    if addon.CurrentTab == "BANK" then dataSource = addon.BankItems
    elseif addon.CurrentTab == "WARBAND" then dataSource = addon.WarbandItems end

    -- Hide all existing buttons
    for _, btn in pairs(addon.ItemButtons) do
        btn:Hide()
    end
    -- Hide all headers
    if not addon.Headers then addon.Headers = {} end
    for _, header in pairs(addon.Headers) do header:Hide() end
    
    local query = addon.Frame.Search:GetText():lower()
    
    -- Categorize by ClassID
    local sections = {} 
    local sectionOrder = {
        "Consumable", "Weapon", "Armor", "Trade Goods", "Quest", 
        "Gem", "Reagent", "Recipe", "Item Enhancement", "Battle Pets",
        "Miscellaneous", "Junk", "Other", "Uncategorized"
    }
    
    -- print("DP Debug: Rendering " .. #dataSource .. " items...")
    
    -- Map ClassIDs to Section Names
    local CLASS_MAP = {
        [0] = "Consumable",
        [1] = "Container",
        [2] = "Weapon",
        [3] = "Gem",
        [4] = "Armor",
        [5] = "Reagent",
        [6] = "Projectile",
        [7] = "Trade Goods",
        [8] = "Item Enhancement",
        [9] = "Recipe",
        [10] = "Money",
        [11] = "Quiver",
        [12] = "Quest",
        [13] = "Key",
        [14] = "Permanent",
        [15] = "Miscellaneous",
        [16] = "Glyph",
        [17] = "Battle Pets",
        [18] = "WoW Token",
        [19] = "Profession"
    }
    
    -- Contextual Filters (Updated keys)
    local VISIBILITY_RULES = {
        ["ALL"] = nil,
        ["RAID"] = { ["Consumable"] = true, ["Weapon"] = true, ["Armor"] = true },
        ["AH"] = { ["Trade Goods"] = true, ["Weapon"] = true, ["Armor"] = true, ["Recipe"] = true },
        ["VENDOR"] = { ["Junk"] = true, ["Quest"] = false }
    }
    
    local currentRules = VISIBILITY_RULES[addon.FilterMode or "ALL"]
    
    for _, item in ipairs(dataSource) do
        local name = GetItemInfo(item.link) or ""
        local matchesQuery = (query == "") or name:lower():find(query)
        
        if matchesQuery then
            -- Ensure classID is never nil
            local classID = item.classID or 15  -- Default to Miscellaneous
            local cat = CLASS_MAP[classID] or "Miscellaneous"
            
            -- Special overrides
            if item.quality == 0 then 
                cat = "Junk"
            elseif classID == 12 then
                cat = "Quest"
            end
            
            -- Apply Context Filter
            local isVisible = true
            if currentRules then
                if addon.FilterMode == "VENDOR" then
                    isVisible = true
                else
                    isVisible = currentRules[cat]
                end
            end
            
            if isVisible then
                if not sections[cat] then sections[cat] = {} end
                table.insert(sections[cat], item)
            end
        end
    end
    
    -- DEBUG: Print section counts
    -- for k, v in pairs(sections) do
    --    print("DP Debug: Section " .. k .. " has " .. #v .. " items.")
    -- end
    
    -- DEBUG: On-screen section count
    if not addon.DebugLabel then
        addon.DebugLabel = addon.Grid:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
        addon.DebugLabel:SetPoint("TOP", addon.Grid, "TOP", 0, -5)
    end
    local sectionCount = 0
    for _ in pairs(sections) do sectionCount = sectionCount + 1 end
    addon.DebugLabel:SetText("Sections: " .. sectionCount)
    addon.DebugLabel:Show()
    
    -- Render Sections
    local yOffset = 10
    local headerIdx = 1
    local btnIdx = 1
    
    for _, catName in ipairs(sectionOrder) do
        local items = sections[catName]
        if items and #items > 0 then
            -- Create/Reuse Header
            local header = addon.Headers[headerIdx]
            if not header then
                header = addon.Grid:CreateFontString(nil, "OVERLAY", "GameFontNormal")
                header:SetJustifyH("LEFT")
                addon.Headers[headerIdx] = header
            end
            header:SetText(catName)
            header:SetPoint("TOPLEFT", 5, -yOffset)
            header:Show()
            headerIdx = headerIdx + 1
            
            yOffset = yOffset + 20 -- Header height
            
            local col, row = 0, 0
            
            for _, item in ipairs(items) do
                local btn = addon.ItemButtons[btnIdx]
                if not btn then
                    btn = CreateFrame("Button", nil, addon.Grid)
                    btn:SetSize(TILE_SIZE, TILE_SIZE)
                    
                    -- Create texture
                    btn.icon = btn:CreateTexture(nil, "ARTWORK")
                    btn.icon:SetAllPoints()
                    
                    -- Count text
                    btn.count = btn:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
                    btn.count:SetPoint("BOTTOMRIGHT", -2, 2)
                    
                    -- Tooltip
                    btn:SetScript("OnEnter", function(self)
                        if self.itemLink then
                            GameTooltip:SetOwner(self, "ANCHOR_RIGHT")
                            GameTooltip:SetHyperlink(self.itemLink)
                            GameTooltip:Show()
                        end
                    end)
                    btn:SetScript("OnLeave", function() GameTooltip:Hide() end)
                    
                    -- Right-click support
                    btn:RegisterForClicks("LeftButtonUp", "RightButtonUp")
                    btn:SetScript("OnClick", function(self, button)
                        if button == "RightButton" and self.bag and self.slot then
                            C_Container.UseContainerItem(self.bag, self.slot)
                        end
                    end)
                    
                    addon.ItemButtons[btnIdx] = btn
                end
                
                -- Set data
                btn.itemLink = item.link
                btn.bag = item.bag
                btn.slot = item.slot
                btn.icon:SetTexture(item.texture)
                btn.count:SetText(item.count > 1 and item.count or "")
                
                -- Position
                local x = col * (TILE_SIZE + PADDING)
                local y = -yOffset - (row * (TILE_SIZE + PADDING))
                btn:SetPoint("TOPLEFT", x, y)
                btn:Show()
                
                -- Glow if new (Mock logic: if quality > 3)
                if item.quality >= 4 then
                    ActionButton_ShowOverlayGlow(btn)
                else
                    ActionButton_HideOverlayGlow(btn)
                end
                
                col = col + 1
                if col >= COLS then
                    col = 0
                    row = row + 1
                end
                btnIdx = btnIdx + 1
            end
            
            -- Move Y down for next section
            if col > 0 then row = row + 1 end
            yOffset = yOffset + (row * (TILE_SIZE + PADDING)) + 10
        end
    end
    
    addon.Grid:SetHeight(yOffset + 50)
end

-- --- GOBLIN MODULE (Native Auctioneer) ---
addon.GoblinInstructions = {} -- Loaded from SavedVariables ideally, or mocked for now

function addon:LoadGoblinInstructions()
    -- Mock Data (In real app, this comes from SavedVariables injected by Python)
    addon.GoblinInstructions = {
        [198765] = { min = 360000, normal = 450000, max = 675000 }, -- Draconium Ore (45g)
        [194820] = { min = 120000, normal = 150000, max = 225000 }, -- Hochenblume (15g)
    }
end

function addon:ScanGoblin()
    addon.GoblinItems = {}
    -- Scan bags for items we have instructions for
    for bag = 0, 4 do
        for slot = 1, C_Container.GetContainerNumSlots(bag) do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info then
                local id = info.itemID
                if addon.GoblinInstructions[id] then
                    table.insert(addon.GoblinItems, {
                        bag = bag,
                        slot = slot,
                        id = id,
                        texture = info.iconFileID,
                        count = info.stackCount,
                        link = info.hyperlink,
                        pricing = addon.GoblinInstructions[id]
                    })
                end
            end
        end
    end
end

function addon:RenderGoblin()
    -- Hide standard grid buttons
    for _, btn in pairs(addon.ItemButtons) do btn:Hide() end
    for _, header in pairs(addon.Headers) do header:Hide() end
    
    local yOffset = 10
    
    -- Header
    local header = addon.Headers[1]
    if not header then
        header = addon.Grid:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        addon.Headers[1] = header
    end
    header:SetText("Goblin Auctioneer - Ready to Post")
    header:SetPoint("TOPLEFT", 5, -yOffset)
    header:Show()
    yOffset = yOffset + 30
    
    -- Render List
    for i, item in ipairs(addon.GoblinItems) do
        local btn = addon.ItemButtons[i]
        if not btn then
            btn = CreateFrame("Button", nil, addon.Grid, "UIPanelButtonTemplate")
            btn:SetSize(350, 40)
            addon.ItemButtons[i] = btn
        end
        
        -- Custom Button Style for List View
        btn:SetSize(350, 40)
        btn:SetText("   " .. item.link .. " x" .. item.count .. "  |  " .. GetCoinTextureString(item.pricing.normal))
        btn:SetPoint("TOPLEFT", 10, -yOffset)
        
        -- Icon
        if not btn.icon then
            btn.icon = btn:CreateTexture(nil, "ARTWORK")
            btn.icon:SetSize(32, 32)
            btn.icon:SetPoint("LEFT", 4, 0)
        end
        btn.icon:SetTexture(item.texture)
        
        -- Post Handler
        btn:SetScript("OnClick", function()
            -- Select Item
            C_Container.PickupContainerItem(item.bag, item.slot)
            ClickAuctionSellItemButton()
            
            -- Post (Requires Hardware Event usually, so we might just stage it)
            -- C_AuctionHouse.PostItem(item.location, duration, quantity, bid, buyout)
            -- For Classic/Retail diffs, we'll assume standard API or macro requirement.
            -- Simulating "Click to Stage" for now.
            
            print("|cff00ff00Goblin:|r Staged " .. item.link .. " at " .. GetCoinTextureString(item.pricing.normal))
            
            -- In a real automated addon, we'd use C_AuctionHouse.PostItem if protected allows,
            -- or we populate the frame and let user click "Create Auction".
            -- Since PostItem is protected, we populate the UI.
            
            if AuctionHouseFrame and AuctionHouseFrame.ItemSellFrame then
                AuctionHouseFrame.ItemSellFrame:SetItem(item.location) -- Pseudo-code for retail
                AuctionHouseFrame.ItemSellFrame.PriceInput:SetAmount(item.pricing.normal)
            end
        end)
        
        btn:Show()
        yOffset = yOffset + 45
    end
    
    addon.Grid:SetHeight(yOffset + 50)
end



-- --- MAIL MODULE (The Mailman) ---
addon.MailInstructions = {}

function addon:LoadMailInstructions()
    -- Mock Data (In real app, injected by Python)
    addon.MailInstructions = {
        [198765] = { target = "Main", keep = 0, reason = "Blacksmithing" }, -- Draconium Ore
        [194820] = { target = "Alt-A", keep = 0, reason = "Alchemy" },      -- Hochenblume
        [200111] = { target = "BankAlt", keep = 0, reason = "Storage" },    -- Resonant Crystal
    }
end

function addon:ScanMail()
    addon.MailItems = {}
    for bag = 0, 4 do
        for slot = 1, C_Container.GetContainerNumSlots(bag) do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info then
                local id = info.itemID
                if addon.MailInstructions[id] then
                    table.insert(addon.MailItems, {
                        bag = bag,
                        slot = slot,
                        id = id,
                        texture = info.iconFileID,
                        count = info.stackCount,
                        link = info.hyperlink,
                        instruction = addon.MailInstructions[id]
                    })
                end
            end
        end
    end
end

function addon:RenderMail()
    -- Hide standard grid buttons
    for _, btn in pairs(addon.ItemButtons) do btn:Hide() end
    for _, header in pairs(addon.Headers) do header:Hide() end
    
    local yOffset = 10
    
    -- Header
    local header = addon.Headers[1]
    if not header then
        header = addon.Grid:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        addon.Headers[1] = header
    end
    header:SetText("The Mailman - Outbox")
    header:SetPoint("TOPLEFT", 5, -yOffset)
    header:Show()
    yOffset = yOffset + 30
    
    -- Render List
    for i, item in ipairs(addon.MailItems) do
        local btn = addon.ItemButtons[i]
        if not btn then
            btn = CreateFrame("Button", nil, addon.Grid, "UIPanelButtonTemplate")
            btn:SetSize(350, 40)
            addon.ItemButtons[i] = btn
        end
        
        -- Custom Button Style
        btn:SetSize(350, 40)
        btn:SetText("   " .. item.link .. " x" .. item.count .. "  ->  " .. item.instruction.target)
        btn:SetPoint("TOPLEFT", 10, -yOffset)
        
        -- Icon
        if not btn.icon then
            btn.icon = btn:CreateTexture(nil, "ARTWORK")
            btn.icon:SetSize(32, 32)
            btn.icon:SetPoint("LEFT", 4, 0)
        end
        btn.icon:SetTexture(item.texture)
        
        -- Click to Send Single
        btn:SetScript("OnClick", function()
            -- Logic to send single item
            -- Requires opening mail frame, setting recipient, attaching item, sending.
            -- Complex in Lua without library, but we can simulate the intent.
            print("|cff00ff00Mailman:|r Sending " .. item.link .. " to " .. item.instruction.target)
        end)
        
        btn:Show()
        yOffset = yOffset + 45
    end
    
    -- "Send All" Button (Mock)
    local sendAllBtn = addon.ItemButtons[#addon.MailItems + 1]
    if not sendAllBtn then
        sendAllBtn = CreateFrame("Button", nil, addon.Grid, "UIPanelButtonTemplate")
        addon.ItemButtons[#addon.MailItems + 1] = sendAllBtn
    end
    sendAllBtn:SetSize(150, 30)
    sendAllBtn:SetText("Send All")
    sendAllBtn:SetPoint("TOPLEFT", 10, -yOffset)
    sendAllBtn:SetScript("OnClick", function()
        print("|cff00ff00Mailman:|r Processing " .. #addon.MailItems .. " mail tasks...")
    end)
    sendAllBtn:Show()
    
    addon.Grid:SetHeight(yOffset + 100)
end



-- --- DESTROY MODULE (The Destroyer) ---
addon.DestroyInstructions = {}

function addon:LoadDestroyInstructions()
    -- Mock Data
    addon.DestroyInstructions = {
        [123456] = { action = "Disenchant", macro = "/cast Disenchant\n/use item:123456", profit = 5 },
        -- [194820] = { action = "Mill", macro = "/cast Milling\n/use item:194820", profit = -5 }, -- Filtered out by backend
        [198765] = { action = "Prospect", macro = "/cast Prospecting\n/use item:198765", profit = 15 },
    }
end

function addon:ScanDestroy()
    addon.DestroyItems = {}
    for bag = 0, 4 do
        for slot = 1, C_Container.GetContainerNumSlots(bag) do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info then
                local id = info.itemID
                if addon.DestroyInstructions[id] then
                    table.insert(addon.DestroyItems, {
                        bag = bag,
                        slot = slot,
                        id = id,
                        texture = info.iconFileID,
                        count = info.stackCount,
                        link = info.hyperlink,
                        instruction = addon.DestroyInstructions[id]
                    })
                end
            end
        end
    end
end

function addon:RenderDestroy()
    -- Hide standard grid buttons
    for _, btn in pairs(addon.ItemButtons) do btn:Hide() end
    for _, header in pairs(addon.Headers) do header:Hide() end
    
    local yOffset = 10
    
    -- Header
    local header = addon.Headers[1]
    if not header then
        header = addon.Grid:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        addon.Headers[1] = header
    end
    header:SetText("The Destroyer - Processing Queue")
    header:SetPoint("TOPLEFT", 5, -yOffset)
    header:Show()
    yOffset = yOffset + 30
    
    -- Render List
    for i, item in ipairs(addon.DestroyItems) do
        local btn = addon.ItemButtons[i]
        if not btn then
            btn = CreateFrame("Button", nil, addon.Grid, "UIPanelButtonTemplate")
            btn:SetSize(350, 40)
            addon.ItemButtons[i] = btn
        end
        
        -- Custom Button Style
        btn:SetSize(350, 40)
        
        local profitText = ""
        if item.instruction.profit then
            if item.instruction.profit > 0 then
                profitText = " (|cff00ff00+" .. item.instruction.profit .. "g|r)"
            else
                profitText = " (|cffff0000" .. item.instruction.profit .. "g|r)"
            end
        end
        
        btn:SetText("   " .. item.link .. " x" .. item.count .. "  ->  " .. item.instruction.action .. profitText)
        btn:SetPoint("TOPLEFT", 10, -yOffset)
        
        -- Icon
        if not btn.icon then
            btn.icon = btn:CreateTexture(nil, "ARTWORK")
            btn.icon:SetSize(32, 32)
            btn.icon:SetPoint("LEFT", 4, 0)
        end
        btn.icon:SetTexture(item.texture)
        
        -- Click to Process Single (Mock)
        btn:SetScript("OnClick", function()
            print("|cff00ff00Destroyer:|r Processing " .. item.link)
        end)
        
        btn:Show()
        yOffset = yOffset + 45
    end
    
    -- "Spam Button" (The Big Button)
    -- This button should perform the action on the FIRST item in the list.
    -- In a real addon, this would be a SecureActionButtonTemplate with attributes set dynamically.
    
    local spamBtn = addon.ItemButtons[#addon.DestroyItems + 1]
    if not spamBtn then
        spamBtn = CreateFrame("Button", nil, addon.Grid, "UIPanelButtonTemplate") -- SecureActionButtonTemplate needed for real cast
        addon.ItemButtons[#addon.DestroyItems + 1] = spamBtn
    end
    spamBtn:SetSize(200, 50)
    spamBtn:SetText("DESTROY NEXT")
    spamBtn:SetPoint("TOPLEFT", 10, -yOffset)
    
    if #addon.DestroyItems > 0 then
        local nextItem = addon.DestroyItems[1]
        spamBtn:SetScript("OnClick", function()
            print("|cff00ff00Destroyer:|r Casting " .. nextItem.instruction.action .. " on " .. nextItem.link)
            -- In real code: SetAttribute("macrotext", nextItem.instruction.macro)
        end)
        spamBtn:Enable()
    else
        spamBtn:SetText("Queue Empty")
        spamBtn:Disable()
    end
    
    spamBtn:Show()
    
    addon.Grid:SetHeight(yOffset + 100)
end






-- --- TOOLTIP INTELLIGENCE ---
addon.Recommendations = {}

function addon:LoadRecommendations()
    -- Mock Data (Injected by Python)
    addon.Recommendations = {
        [198765] = { action = "Prospect", profit = 15, reason = "Materials worth more" }, -- Draconium Ore
        [123456] = { action = "Disenchant", profit = 5, reason = "Materials worth more" }, -- Green Bracers
        [194820] = { action = "Sell", profit = 0, reason = "Market Value" }, -- Hochenblume
    }
end

-- Hook Tooltip
GameTooltip:HookScript("OnTooltipSetItem", function(tooltip)
    local _, link = tooltip:GetItem()
    if not link then return end
    
    local id = GetItemInfoInstant(link)
    if not id then return end
    
    -- Ensure recommendations are loaded
    if not next(addon.Recommendations) then addon:LoadRecommendations() end
    
    local rec = addon.Recommendations[id]
    if rec then
        local color = "|cffffffff" -- White
        if rec.profit > 0 then color = "|cff00ff00" end -- Green
        
        tooltip:AddLine(" ")
        tooltip:AddLine("|cff00ff00Goblin Advice:|r " .. rec.action .. " (" .. rec.reason .. ")")
        if rec.profit > 0 then
            tooltip:AddLine("Potential Profit: " .. color .. "+" .. rec.profit .. "g|r")
        end
        tooltip:Show()
    end
end)


