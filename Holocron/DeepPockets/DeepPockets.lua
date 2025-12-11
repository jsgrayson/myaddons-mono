-- DeepPockets.lua (Native WoW API Version)
local addonName, addon = ...
print("!!! DEEPPOCKETS FILE LOADED !!!")
print("|cff00ff00DeepPockets:|r Native Core Loaded.")

-- Constants
local TILE_SIZE = 40
local PADDING = 5
local COLS = 10

-- 1. SavedVariables Setup
DeepPocketsDB = DeepPocketsDB or {
    settings = { uiScale = 1.0, customCategories = {} }
}

-- 2. Event Handling
local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("BAG_UPDATE")

eventFrame:SetScript("OnEvent", function(self, event, ...)
    elseif event == "PLAYER_LOGIN" then
        print("|cff00ff00DeepPockets:|r PLAYER_LOGIN. Ready (Lazy Load).")
        
        -- Create minimap button
        if _G["HolocronMinimap-1.0"] then
            local MinimapLib = _G["HolocronMinimap-1.0"]
            addon.minimapButton = MinimapLib:CreateMinimapButton("DeepPockets", {
                icon = "Interface\\Icons\\INV_Misc_Bag_08",
                tooltip = "DeepPockets",
                tooltipText = "Smart bag management",
                db = DeepPocketsDB.settings,
                OnLeftClick = function() addon:Toggle() end,
                OnRightClick = function() 
                    if addon.Settings then
                        addon.Settings:Toggle()
                    end
                end
            })
        end
        
        -- Create options panel
        if _G["HolocronOptions-1.0"] then
            addon:CreateOptionsPanel()
        end
    elseif event == "ADDON_LOADED" and ... == addonName then
        -- DB is loaded here
        DeepPocketsDB = DeepPocketsDB or {}
        DeepPocketsDB.settings = DeepPocketsDB.settings or { uiScale = 1.0 }
    elseif event == "BAG_UPDATE" then
        if addon.Frame and addon.Frame:IsShown() then
            addon:ScanBags()
            addon:RenderGrid()
        end
    end
end)

-- 3. UI Creation (Module 3: Frames and Widgets)
function addon:InitUI()
    print("DEBUG: Entering InitUI")
    if addon.Frame then 
        print("DEBUG: Frame already exists")
        return 
    end
    
    -- Main Frame (Simple Texture, No Backdrop Template)
    local f = CreateFrame("Frame", "DeepPocketsFrame", UIParent)
    addon.Frame = f
    
    f:SetSize(450, 550)
    f:SetPoint("BOTTOMRIGHT", UIParent, "BOTTOMRIGHT", -50, 50)
    
    -- Theme Setup
    local theme, bgKey = Holocron:GetTheme("DeepPockets")
    local LSM = LibStub("LibSharedMedia-3.0")

    -- Main Backdrop (Glass)
    f.bg = f:CreateTexture(nil, "BACKGROUND")
    f.bg:SetAllPoints()
    if LSM then
        f.bg:SetTexture(LSM:Fetch("background", bgKey))
    else
        f.bg:SetColorTexture(0.05, 0.05, 0.05, 0.95)
    end
    
    -- Border (Theme Color)
    if not f.Border then
        f.Border = CreateFrame("Frame", nil, f, "BackdropTemplate")
        f.Border:SetAllPoints()
        f.Border:SetBackdrop({
            edgeFile = "Interface\\AddOns\\HolocronCore\\Media\\Border_Glow.tga",
            edgeSize = 16,
        })
        f.Border:SetBackdropBorderColor(theme.r, theme.g, theme.b, 1)
    end
    
    f:EnableMouse(true)
    f:SetMovable(true)
    f:SetResizable(true)
    f:SetResizeBounds(300, 300, 800, 900)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", function(self) self:StartMoving() end)
    f:SetScript("OnDragStop", function(self) self:StopMovingOrSizing() end)
    
    f:Hide()
    
    -- Close Button
    f.Close = CreateFrame("Button", nil, f, "UIPanelCloseButton")
    f.Close:SetPoint("TOPRIGHT", -5, -5)
    
    -- Title
    f.Title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    f.Title:SetPoint("TOPLEFT", 10, -10)
    f.Title:SetText("DeepPockets")
    
    -- ScrollFrame for items
    local scrollFrame = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
    scrollFrame:SetPoint("TOPLEFT", 10, -35)
    scrollFrame:SetPoint("BOTTOMRIGHT", -30, 10)
    
    -- ScrollChild (container for item buttons)
    local scrollChild = CreateFrame("Frame", nil, scrollFrame)
    scrollChild:SetSize(400, 2000) -- Height will be adjusted based on item count
    scrollFrame:SetScrollChild(scrollChild)
    
    addon.ScrollChild = scrollChild
    addon.ScrollFrame = scrollFrame
    
    -- Content Placeholder (will be hidden once items load)
    local content = scrollChild:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    content:SetPoint("CENTER")
    content:SetText("DeepPockets\n\nPress 'b' or click bags to load")
    
    -- STATUS TEXT (On Main Frame)
    addon.StatusText = f:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    addon.StatusText:SetPoint("BOTTOM", f, "BOTTOM", 0, 5)
    addon.StatusText:SetText("Ready")
    
    -- Add search/filter UI
    if addon.SearchFilter then
        addon.SearchFilter:CreateUI(f)
    end
    
    -- Add settings button
    if addon.Settings then
        addon.Settings:AddButtonToFrame(f)
    end
    
    print("|cff00ff00DeepPockets:|r UI Initialized.")
end

-- 4. Slash Commands
SLASH_DEEPPOCKETS1 = "/dp"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    print("|cff00ff00DeepPockets:|r Slash Command Received.")
    
    local status, err = pcall(function()
        addon:InitUI()
        if addon.Frame then
            if addon.Frame:IsShown() then
                addon.Frame:Hide()
            else
                addon.Frame:Show()
                -- addon:ScanBags() -- Lazy scan on open
            end
        end
    end)
    
    if not status then
        print("|cff0000ffDeepPockets Error:|r " .. tostring(err))
    end
end

-- 5. Keybind (Opens with 'b' key)
BINDING_HEADER_DEEPPOCKETS = "DeepPockets"
BINDING_NAME_DEEPPOCKETS_TOGGLE = "Toggle DeepPockets"

function addon:Toggle()
    addon:InitUI()
    if addon.Frame then
        if addon.Frame:IsShown() then
            addon.Frame:Hide()
        else
            addon.Frame:Show()
            addon:ScanBags()
            addon:RenderGrid()
        end
    end
end

-- Hook into Blizzard bag toggle
hooksecurefunc("ToggleBag", function(id)
    -- Intercept bag opens and show DeepPockets instead
    if id == 0 then -- Main backpack
        addon:Toggle()
        -- Close Blizzard bags
        for i = 0, 4 do
            CloseBag(i)
        end
    end
end)

-- 6. Bag Scanning
addon.BagItems = {}
addon.ItemButtons = {}
addon.CategoryHeaders = {}

function addon:ScanBags()
    wipe(addon.BagItems)
    
    for bag = 0, 4 do
        local numSlots = C_Container.GetContainerNumSlots(bag)
        for slot = 1, numSlots do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info then
                -- Get item details for categorization
                local itemName, itemLink, itemQuality, itemLevel, itemMinLevel, itemType, itemSubType = GetItemInfo(info.hyperlink)
                
                table.insert(addon.BagItems, {
                    bag = bag,
                    slot = slot,
                    icon = info.iconFileID,
                    count = info.stackCount,
                    quality = info.quality,
                    link = info.hyperlink,
                    id = info.itemID,
                    type = itemType or "Other",
                    subtype = itemSubType or ""
                })
            end
        end
    end
end

-- Helper: Categorize items
local function CategorizeItems(items)
    local categories = {}
    local categoryOrder = {"Quest", "Consumable", "Trade Goods", "Equipment", "Junk", "Other"}
    
    -- Initialize categories
    for _, cat in ipairs(categoryOrder) do
        categories[cat] = {}
    end
    
    -- Sort items into categories
    for _, item in ipairs(items) do
        if item.quality == 0 then
            table.insert(categories["Junk"], item)
        elseif item.type == "Quest" or item.type == "Questline" then
            table.insert(categories["Quest"], item)
        elseif item.type == "Consumable" then
            table.insert(categories["Consumable"], item)
        elseif item.type == "Trade Goods" or item.type == "Tradeskill" then
            table.insert(categories["Trade Goods"], item)
        elseif item.type == "Armor" or item.type == "Weapon" then
            table.insert(categories["Equipment"], item)
        else
            table.insert(categories["Other"], item)
        end
    end
    
    return categories, categoryOrder
end

-- 7. Grid Rendering with Categories
function addon:RenderGrid()
    if not addon.Frame or not addon.ScrollChild then return end
    if not addon.Frame:IsShown() then return end
    
    -- Clear existing UI
    for _, btn in pairs(addon.ItemButtons) do
        btn:Hide()
    end
    for _, header in pairs(addon.CategoryHeaders) do
        header:Hide()
    end
    
    -- Apply search/filter
    local filteredItems = addon.BagItems
    if addon.SearchFilter then
        filteredItems = addon.SearchFilter:ApplyFilters(filteredItems)
    end
    
    local categories, categoryOrder = CategorizeItems(filteredItems)
    
    -- Get dynamic columns setting
    local cols = (DeepPocketsDB.settings and DeepPocketsDB.settings.columns) or COLS
    local showCategories = (DeepPocketsDB.settings and DeepPocketsDB.settings.showCategories) ~= false
    
    local yOffset = -10
    local buttonIndex = 1
    
    for _, categoryName in ipairs(categoryOrder) do
        local items = categories[categoryName]
        
        if #items > 0 then
            -- Category Header
            local header = addon.CategoryHeaders[categoryName]
            if not header then
                header = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
                addon.CategoryHeaders[categoryName] = header
            end
            header:SetPoint("TOPLEFT", addon.ScrollChild, "TOPLEFT", 5, yOffset)
            header:SetText(categoryName .. " (" .. #items .. ")")
            header:Show()
            yOffset = yOffset - 25
            
            -- Items in grid
            local row, col = 0, 0
            for _, item in ipairs(items) do
                local btn = addon.ItemButtons[buttonIndex]
                if not btn then
                    btn = CreateFrame("Button", nil, addon.ScrollChild)
                    btn:SetSize(TILE_SIZE, TILE_SIZE)
                    btn:SetFrameLevel(addon.ScrollChild:GetFrameLevel() + 5)
                    
                    btn.icon = btn:CreateTexture(nil, "ARTWORK")
                    btn.icon:SetAllPoints()
                    
                    btn.count = btn:CreateFontString(nil, "OVERLAY", "NumberFontNormal")
                    btn.count:SetPoint("BOTTOMRIGHT", -2, 2)
                    
                    btn.border = btn:CreateTexture(nil, "OVERLAY")
                    btn.border:SetAllPoints()
                    btn.border:SetTexture("Interface\\Buttons\\UI-ActionButton-Border")
                    btn.border:SetBlendMode("ADD")
                    btn.border:Hide()
                    
                    btn:SetScript("OnEnter", function(self)
                        GameTooltip:SetOwner(self, "ANCHOR_RIGHT")
                        GameTooltip:SetBagItem(self.bag, self.slot)
                        GameTooltip:Show()
                    end)
                    btn:SetScript("OnLeave", function() GameTooltip:Hide() end)
                    btn:SetScript("OnClick", function(self)
                        C_Container.PickupContainerItem(self.bag, self.slot)
                    end)
                    
                    addon.ItemButtons[buttonIndex] = btn
                end
                
                btn.bag = item.bag
                btn.slot = item.slot
                
                if item.icon then
                    btn.icon:SetTexture(item.icon)
                else
                    btn.icon:SetColorTexture(0.5, 0.5, 0.5, 1)
                end
                
                if item.count > 1 then
                    btn.count:SetText(item.count)
                    btn.count:Show()
                else
                    btn.count:Hide()
                end
                
                if item.quality and item.quality > 1 then
                    local r, g, b = C_Item.GetItemQualityColor(item.quality)
                    if r then
                        btn.border:SetVertexColor(r, g, b)
                        btn.border:Show()
                    end
                else
                    btn.border:Hide()
                end
                
                local x = 5 + (col * (TILE_SIZE + PADDING))
                local y = yOffset - (row * (TILE_SIZE + PADDING))
                btn:ClearAllPoints()
                btn:SetPoint("TOPLEFT", addon.ScrollChild, "TOPLEFT", x, y)
                btn:Show()
                
                col = col + 1
                if col >= cols then
                    col = 0
                    row = row + 1
                end
                
                buttonIndex = buttonIndex + 1
            end
            
            -- Move yOffset down for next category
            local rowsUsed = math.ceil(#items / cols)
            yOffset = yOffset - (rowsUsed * (TILE_SIZE + PADDING)) - 10
        end
    end
    
    -- Adjust ScrollChild height
    addon.ScrollChild:SetHeight(math.abs(yOffset) + 50)
    
    if addon.StatusText then 
        addon.StatusText:SetText(#addon.BagItems .. " items") 
    end
end

print("|cff00ff00DeepPockets:|r Loaded.")

-- Create Options Panel
function addon:CreateOptionsPanel()
    local OptionsLib = _G["HolocronOptions-1.0"]
    if not OptionsLib then return end
    
    local panel = OptionsLib:CreateOptionsPanel("DeepPockets", {
        title = "DeepPockets",
        subtitle = "Smart bag management and organization",
        onDefault = function()
            DeepPocketsDB.settings = {
                uiScale = 1.0,
                columns = 10,
                showCategories = true,
                replaceBags = true,
                showItemCount = true,
                autoSort = false
            }
            print("|cff00ff00DeepPockets:|r Settings reset to defaults")
            ReloadUI()
        end
    })
    
    -- General Settings
    panel:AddHeader("General")
    
    panel:AddCheckbox({
        name = "Replace Default Bags",
        tooltip = "Use DeepPockets instead of default bags when pressing 'B'",
        get = function() return DeepPocketsDB.settings.replaceBags ~= false end,
        set = function(val) DeepPocketsDB.settings.replaceBags = val end
    })
    
    panel:AddCheckbox({
        name = "Show Category Headers",
        tooltip = "Display category names in the bag view",
        get = function() return DeepPocketsDB.settings.showCategories ~= false end,
        set = function(val) 
            DeepPocketsDB.settings.showCategories = val
            if addon.Frame and addon.Frame:IsShown() then
                addon:RenderGrid()
            end
        end
    })
    
    panel:AddCheckbox({
        name = "Show Item Counts",
        tooltip = "Display stack counts on items",
        get = function() return DeepPocketsDB.settings.showItemCount ~= false end,
        set = function(val) 
            DeepPocketsDB.settings.showItemCount = val
            if addon.Frame and addon.Frame:IsShown() then
                addon:RenderGrid()
            end
        end
    })
    
    -- Display Settings
    panel:AddHeader("Display")
    
    panel:AddSlider({
        name = "UI Scale",
        min = 0.5,
        max = 2.0,
        step = 0.1,
        minText = "50%",
        maxText = "200%",
        format = "UI Scale: %.1f",
        get = function() return DeepPocketsDB.settings.uiScale or 1.0 end,
        set = function(val) 
            DeepPocketsDB.settings.uiScale = val
            if addon.Frame then
                addon.Frame:SetScale(val)
            end
        end
    })
    
    panel:AddSlider({
        name = "Columns",
        min = 5,
        max = 15,
        step = 1,
        minText = "5",
        maxText = "15",
        format = "Columns: %d",
        get = function() return DeepPocketsDB.settings.columns or 10 end,
        set = function(val) 
            DeepPocketsDB.settings.columns = val
            if addon.Frame and addon.Frame:IsShown() then
                addon:RenderGrid()
            end
        end
    })
    
    -- Minimap Button
    panel:AddHeader("Minimap Button")
    
    panel:AddCheckbox({
        name = "Show Minimap Button",
        tooltip = "Toggle minimap button visibility",
        get = function() return not DeepPocketsDB.settings.minimapHidden end,
        set = function(val) 
            DeepPocketsDB.settings.minimapHidden = not val
            if addon.minimapButton then
                if val then
                    addon.minimapButton:Show()
                else
                    addon.minimapButton:Hide()
                end
            end
        end
    })
    
    addon.optionsPanel = panel
end
