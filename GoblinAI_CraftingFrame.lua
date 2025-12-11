-- UI/CraftingFrame.lua - Crafting Profitability Calculator
-- Part of GoblinAI v2.0

GoblinAI.CraftingFrame = {}
local Crafting = GoblinAI.CraftingFrame

Crafting.knownRecipes = {}
Crafting.sortBy = "profit" -- profit, gph, roi

-- ============================================================================
-- Initialize Crafting Tab
-- ============================================================================

function Crafting:Initialize(parentFrame)
    self.frame = parentFrame
    self:CreateUI()
    self:ScanKnownRecipes()
end

function Crafting:CreateUI()
    -- Header
    local header = self.frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -10)
    header:SetText("Crafting Profitability")
    header:SetTextColor(1, 0.84, 0, 1)
    
    -- Controls bar
    local controlsFrame = CreateFrame("Frame", nil, self.frame)
    controlsFrame:SetSize(660, 40)
    controlsFrame:SetPoint("TOP", 0, -40)
    
    -- Refresh button
    local refreshBtn = CreateFrame("Button", nil, controlsFrame, "UIPanelButtonTemplate")
    refreshBtn:SetSize(120, 25)
    refreshBtn:SetPoint("LEFT", 10, 0)
    refreshBtn:SetText("Scan Recipes")
    refreshBtn:SetScript("OnClick", function()
        Crafting:ScanKnownRecipes()
        Crafting:RefreshCraftList()
    end)
    
    -- Sort dropdown
    local sortLabel = controlsFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    sortLabel:SetPoint("LEFT", 150, 0)
    sortLabel:SetText("Sort by:")
    
    local sortBtn = CreateFrame("Button", nil, controlsFrame, "UIPanelButtonTemplate")
    sortBtn:SetSize(100, 25)
    sortBtn:SetPoint("LEFT", sortLabel, "RIGHT", 5, 0)
    sortBtn:SetText("Profit")
    sortBtn:SetScript("OnClick", function()
        -- Cycle through sort modes
        if Crafting.sortBy == "profit" then
            Crafting.sortBy = "gph"
            sortBtn:SetText("GPH")
        elseif Crafting.sortBy == "gph" then
            Crafting.sortBy = "roi"
            sortBtn:SetText("ROI")
        else
            Crafting.sortBy = "profit"
            sortBtn:SetText("Profit")
        end
        Crafting:RefreshCraftList()
    end)
    
    -- Filter: Show only profitable
    local profitableCheck = CreateFrame("CheckButton", nil, controlsFrame, "UICheckButtonTemplate")
    profitableCheck:SetPoint("LEFT", 380, 0)
    profitableCheck:SetChecked(true)
    profitableCheck.text = profitableCheck:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    profitableCheck.text:SetPoint("LEFT", profitableCheck, "RIGHT", 0, 0)
    profitableCheck.text:SetText("Profitable only")
    profitableCheck:SetScript("OnClick", function()
        Crafting.filterProfitable = profitableCheck:GetChecked()
        Crafting:RefreshCraftList()
    end)
    self.profitableFilter = profitableCheck
    Crafting.filterProfitable = true
    
    -- Craft list scroll
    local scroll = GoblinAI:CreateScrollFrame(self.frame, 650, 380)
    scroll:SetPoint("TOP", 0, -85)
    self.craftScroll = scroll
end

-- ============================================================================
-- Recipe Scanning
-- ============================================================================

function Crafting:ScanKnownRecipes()
    self.knownRecipes = {}
    
    -- Scan all professions
    local professions = {C_TradeSkillUI.GetAllProfessionTradeSkillLines()}
    
    for _, professionID in ipairs(professions) do
        local profInfo = C_TradeSkillUI.GetProfessionInfoBySkillLineID(professionID)
        
        if profInfo and profInfo.professionID then
            -- Open profession (required to scan)
            C_TradeSkillUI.OpenTradeSkill(profInfo.professionID)
            
            -- Get all recipes
            local recipeIDs = C_TradeSkillUI.GetAllRecipeIDs()
            
            for _, recipeID in ipairs(recipeIDs) do
                local recipeInfo = C_TradeSkillUI.GetRecipeInfo(recipeID)
                
                if recipeInfo and not recipeInfo.disabled then
                    local craftData = self:AnalyzeRecipe(recipeID, recipeInfo)
                    
                    if craftData then
                        table.insert(self.knownRecipes, craftData)
                    end
                end
            end
            
            C_TradeSkillUI.CloseTradeSkill()
        end
    end
    
    print("|cFFFFD700Goblin AI:|r Scanned " .. #self.knownRecipes .. " craftable recipes")
end

function Crafting:AnalyzeRecipe(recipeID, recipeInfo)
    -- Get crafted item
    local itemLink = C_TradeSkillUI.GetRecipeItemLink(recipeID)
    if not itemLink then return nil end
    
    local itemID = GetItemInfoInstant(itemLink)
    if not itemID then return nil end
    
    -- Get sell price (from backend or scan data)
    local sellPrice = self:GetItemPrice(itemID)
    if not sellPrice or sellPrice == 0 then return nil end
    
    -- Calculate material cost
    local reagents = C_TradeSkillUI.GetRecipeReagentInfo(recipeID)
    local totalCost = 0
    local missingMats = {}
    
    if reagents then
        for i = 1, reagents.numReagents do
            local reagentInfo = reagents[i]
            if reagentInfo then
                local reagentID = reagentInfo.itemID
                local reagentCount = reagentInfo.quantity
                
                local reagentPrice = self:GetItemPrice(reagentID)
                
                if reagentPrice then
                    totalCost = totalCost + (reagentPrice * reagentCount)
                else
                    -- Can't calculate without material price
                    table.insert(missingMats, reagentID)
                end
            end
        end
    end
    
    -- Calculate profit
    local profit = sellPrice - totalCost
    local roi = totalCost > 0 and (profit / totalCost) or 0
    
    -- Estimate craft time (seconds)
    local craftTime = recipeInfo.craftTime or 2
    
    -- Gold per hour
    local gph = (profit / craftTime) * 3600
    
    return {
        recipeID = recipeID,
        recipeName = recipeInfo.name,
        itemID = itemID,
        itemLink = itemLink,
        sellPrice = sellPrice,
        materialCost = totalCost,
        profit = profit,
        roi = roi,
        craftTime = craftTime,
        gph = gph,
        difficulty = recipeInfo.difficulty,
        missingMats = missingMats,
    }
end

function Crafting:GetItemPrice(itemID)
    -- Try backend market prices first
    local marketPrice = GoblinAI.BackendAPI:GetMarketPrice(itemID)
    if marketPrice then
        return marketPrice
    end
    
    -- Fallback to last scan
    local lastScan = GoblinAI.Scanner:GetLastScan()
    if lastScan and lastScan.data then
        for _, item in ipairs(lastScan.data) do
            if item.item_id == itemID then
                return item.price
            end
        end
    end
    
    -- Fallback to vendor price
    local vendorPrice = select(11, GetItemInfo(itemID))
    if vendorPrice and vendorPrice > 0 then
        return vendorPrice
    end
    
    return nil
end

-- ============================================================================
-- Craft List Display
-- ============================================================================

function Crafting:RefreshCraftList()
    if not self.craftScroll then return end
    
    -- Clear
    for _, child in ipairs({self.craftScroll.content:GetChildren()}) do
        child:Hide()
    end
    
    -- Filter recipes
    local filteredCrafts = {}
    
    for _, craft in ipairs(self.knownRecipes) do
        if not self.filterProfitable or craft.profit > 0 then
            table.insert(filteredCrafts, craft)
        end
    end
    
    -- Sort
    if self.sortBy == "profit" then
        table.sort(filteredCrafts, function(a, b)
            return a.profit > b.profit
        end)
    elseif self.sortBy == "gph" then
        table.sort(filteredCrafts, function(a, b)
            return a.gph > b.gph
        end)
    elseif self.sortBy == "roi" then
        table.sort(filteredCrafts, function(a, b)
            return a.roi > b.roi
        end)
    end
    
    -- Display
    local yOffset = 0
    for i, craft in ipairs(filteredCrafts) do
        if i > 100 then break end -- Show top 100
        
        local craftRow = self:CreateCraftRow(craft, yOffset)
        craftRow:SetParent(self.craftScroll.content)
        yOffset = yOffset - 70
    end
    
    self.craftScroll.content:SetHeight(math.max(1, #filteredCrafts * 70))
    
    if #filteredCrafts == 0 then
        local noData = self.craftScroll.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        noData:SetPoint("TOP", 0, -20)
        noData:SetText("No profitable crafts found. Try scanning recipes.")
    end
end

function Crafting:CreateCraftRow(craft, yOffset)
    local row = CreateFrame("Frame", nil, self.craftScroll.content, "BackdropTemplate")
    row:SetSize(630, 65)
    row:SetPoint("TOPLEFT", 5, yOffset)
    
    -- Color based on profit
    local bgColor = craft.profit > 0 and {0, 0.15, 0, 0.7} or {0.15, 0, 0, 0.7}
    local borderColor = craft.profit > 0 and {0, 0.8, 0, 1} or {0.8, 0, 0, 1}
    
    row:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    row:SetBackdropColor(unpack(bgColor))
    row:SetBackdropBorderColor(unpack(borderColor))
    
    -- Item icon
    local _, _, _, _, _, _, _, _, _, itemTexture = GetItemInfo(craft.itemID)
    local icon = row:CreateTexture(nil, "ARTWORK")
    icon:SetSize(50, 50)
    icon:SetPoint("LEFT", 5, 0)
    icon:SetTexture(itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark")
    
    -- Recipe name
    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    name:SetPoint("TOPLEFT", 60, -5)
    name:SetText(craft.recipeName)
    name:SetTextColor(1, 0.84, 0, 1)
    
    -- Cost breakdown
    local costs = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    costs:SetPoint("TOPLEFT", 60, -22)
    costs:SetText(string.format("Cost: %s | Sell: %s", 
        GoblinAI:FormatGold(craft.materialCost),
        GoblinAI:FormatGold(craft.sellPrice)))
    
    -- Profit
    local profit = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    profit:SetPoint("TOPLEFT", 60, -40)
    profit:SetText(string.format("Profit: %s (%.0f%% ROI)", 
        GoblinAI:FormatGold(craft.profit),
        craft.roi * 100))
    profit:SetTextColor(craft.profit > 0 and 0 or 1, craft.profit > 0 and 1 or 0, 0, 1)
    
    -- GPH
    local gph = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    gph:SetPoint("TOPRIGHT", -120, -5)
    gph:SetText(string.format("GPH: %s", GoblinAI:FormatGold(craft.gph)))
    gph:SetJustifyH("RIGHT")
    
    -- Craft button
    local craftBtn = CreateFrame("Button", nil, row, "UIPanelButtonTemplate")
    craftBtn:SetSize(90, 22)
    craftBtn:SetPoint("RIGHT", -10, 10)
    craftBtn:SetText("Craft")
    craftBtn:SetScript("OnClick", function()
        Crafting:OpenCraftWindow(craft.recipeID)
    end)
    
    -- Shop mats button
    local shopBtn = CreateFrame("Button", nil, row, "UIPanelButtonTemplate")
    shopBtn:SetSize(90, 22)
    shopBtn:SetPoint("RIGHT", -10, -15)
    shopBtn:SetText("Shop Mats")
    shopBtn:SetScript("OnClick", function()
        Crafting:CreateShoppingList(craft)
    end)
    
    return row
end

-- ============================================================================
-- Crafting Actions
-- ============================================================================

function Crafting:OpenCraftWindow(recipeID)
    -- Open profession window to this recipe
    C_TradeSkillUI.OpenRecipe(recipeID)
    print("|cFFFFD700Goblin AI:|r Opened profession window for this recipe")
end

function Crafting:CreateShoppingList(craft)
    -- Create shopping list for missing materials
    local reagents = C_TradeSkillUI.GetRecipeReagentInfo(craft.recipeID)
    
    if not reagents then
        print("|cFFFF0000Goblin AI:|r Could not get recipe reagents")
        return
    end
    
    -- Create shopping list
    if not GoblinAIDB.shoppingLists then
        GoblinAIDB.shoppingLists = {}
    end
    
    local listName = "Mats for " .. craft.recipeName
    local items = {}
    
    for i = 1, reagents.numReagents do
        local reagent = reagents[i]
        if reagent then
            table.insert(items, {
                itemID = reagent.itemID,
                quantity = reagent.quantity,
            })
        end
    end
    
    table.insert(GoblinAIDB.shoppingLists, {
        name = listName,
        items = items,
        created = time(),
    })
    
    print("|cFFFFD700Goblin AI:|r Shopping list created: " .. listName)
    print("Switch to Shopping tab to view")
end

-- ============================================================================
-- Initialization
-- ============================================================================

print("|cFFFFD700Goblin AI:|r Crafting Frame loaded - Profit calculator ready")
