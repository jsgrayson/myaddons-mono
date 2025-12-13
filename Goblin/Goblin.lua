-- Goblin.lua - TSM-Class Craft Queue System (Offline-First)
local addonName, addonTable = ...
local Goblin = LibStub("AceAddon-3.0"):NewAddon("Goblin", "AceConsole-3.0", "AceEvent-3.0")
local AceGUI = LibStub("AceGUI-3.0")

-- Data Defaults
local defaults = {
    profile = {
        inventory = {},  -- [itemId] = { bags, bank, reagent, total, updatedAt }
        links = {},      -- [recipeId] = { outputItemId, outputQty, reagents=[{itemId,qty}] }
        queue = {},      -- [idx] = { recipeId, qty, source, parentRecipeId }
        matlist = {},    -- [itemId] = { need, have, short }
        settings = { autoSubcraft = true, bankOpen = false }
    }
}

function Goblin:OnInitialize()
    self.db = LibStub("AceDB-3.0"):New("GoblinDB", defaults, true)
    self:RegisterChatCommand("gob", "HandleCommand")
    self:RegisterChatCommand("goblin", "HandleCommand")
    self:Print("Goblin Loaded. Type /gob to open.")
end

function Goblin:OnEnable()
    self:RegisterEvent("BAG_UPDATE_DELAYED")
    self:RegisterEvent("PLAYERBANKSLOTS_CHANGED")
    self:RegisterEvent("BANKFRAME_OPENED")
    self:RegisterEvent("BANKFRAME_CLOSED")
end

-- ============================================================================
-- STEP 1: Inventory Snapshot
-- ============================================================================

function Goblin:ScanInventory()
    local inv = {}
    
    -- Scan bags
    for bag = 0, 4 do
        for slot = 1, C_Container.GetContainerNumSlots(bag) do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if info and info.itemID then
                inv[info.itemID] = inv[info.itemID] or { bags=0, bank=0, reagent=0, total=0 }
                inv[info.itemID].bags = inv[info.itemID].bags + info.stackCount
            end
        end
    end
    
    -- Scan bank (only if open)
    if self.db.profile.settings.bankOpen then
        for slot = 1, 28 do
            local info = C_Container.GetContainerItemInfo(BANK_CONTAINER, slot)
            if info and info.itemID then
                inv[info.itemID] = inv[info.itemID] or { bags=0, bank=0, reagent=0, total=0 }
                inv[info.itemID].bank = inv[info.itemID].bank + info.stackCount
            end
        end
        
        -- Scan reagent bank
        for slot = 1, 98 do
            local info = C_Container.GetContainerItemInfo(REAGENTBANK_CONTAINER, slot)
            if info and info.itemID then
                inv[info.itemID] = inv[info.itemID] or { bags=0, bank=0, reagent=0, total=0 }
                inv[info.itemID].reagent = inv[info.itemID].reagent + info.stackCount
            end
        end
    end
    
    -- Compute totals
    for itemId, data in pairs(inv) do
        data.total = data.bags + data.bank + data.reagent
        data.updatedAt = time()
    end
    
    self.db.profile.inventory = inv
    self:Print("Inventory scanned: " .. self:CountKeys(inv) .. " unique items")
end

function Goblin:BAG_UPDATE_DELAYED()
    C_Timer.After(0.5, function() self:ScanInventory() end)
end

function Goblin:PLAYERBANKSLOTS_CHANGED()
    if self.db.profile.settings.bankOpen then
        C_Timer.After(0.5, function() self:ScanInventory() end)
    end
end

function Goblin:BANKFRAME_OPENED()
    self.db.profile.settings.bankOpen = true
    self:ScanInventory()
end

function Goblin:BANKFRAME_CLOSED()
    self.db.profile.settings.bankOpen = false
end

-- ============================================================================
-- STEP 2: Recipe Ingestion
-- ============================================================================

function Goblin:IngestRecipes()
    if not C_TradeSkillUI or not C_TradeSkillUI.IsTradeSkillReady() then
        self:Print("Open a profession window first")
        return
    end
    
    local recipeIDs = C_TradeSkillUI.GetAllRecipeIDs()
    local count = 0
    
    for _, recipeId in ipairs(recipeIDs or {}) do
        local recipeInfo = C_TradeSkillUI.GetRecipeInfo(recipeId)
        if recipeInfo and not recipeInfo.isDummyRecipe then
            local outputItemLink = C_TradeSkillUI.GetRecipeItemLink(recipeId)
            local outputItemId = outputItemLink and tonumber(outputItemLink:match("item:(%d+)"))
            
            if outputItemId then
                local reagents = {}
                for i = 1, C_TradeSkillUI.GetRecipeNumReagents(recipeId) do
                    local reagentName, reagentIcon, reagentCount = C_TradeSkillUI.GetRecipeReagentInfo(recipeId, i)
                    local reagentLink = C_TradeSkillUI.GetRecipeReagentItemLink(recipeId, i)
                    local reagentItemId = reagentLink and tonumber(reagentLink:match("item:(%d+)"))
                    
                    if reagentItemId then
                        table.insert(reagents, { itemId = reagentItemId, qty = reagentCount })
                    end
                end
                
                self.db.profile.links[recipeId] = {
                    outputItemId = outputItemId,
                    outputQty = recipeInfo.numItemsProduced or 1,
                    reagents = reagents,
                    name = recipeInfo.name
                }
                count = count + 1
            end
        end
    end
    
    self:Print("Ingested " .. count .. " recipes")
end

-- ============================================================================
-- STEP 3: Queue Core
-- ============================================================================

function Goblin:AddToQueue(recipeId, qty, source, parentRecipeId)
    source = source or "manual"
    qty = qty or 1
    
    -- Deduplicate: merge if same recipeId + source + parent
    for i, entry in ipairs(self.db.profile.queue) do
        if entry.recipeId == recipeId and entry.source == source and entry.parentRecipeId == parentRecipeId then
            entry.qty = entry.qty + qty
            self:Print("Merged queue entry: " .. (self.db.profile.links[recipeId] and self.db.profile.links[recipeId].name or recipeId))
            return
        end
    end
    
    table.insert(self.db.profile.queue, {
        recipeId = recipeId,
        qty = qty,
        source = source,
        parentRecipeId = parentRecipeId
    })
    
    self:Print("Added to queue: " .. (self.db.profile.links[recipeId] and self.db.profile.links[recipeId].name or recipeId))
    
    -- Auto-expand subcrafts if enabled
    if self.db.profile.settings.autoSubcraft then
        self:ExpandSubcrafts()
    end
end

function Goblin:RemoveFromQueue(index)
    table.remove(self.db.profile.queue, index)
    self:Print("Removed from queue")
end

function Goblin:ClearQueue()
    wipe(self.db.profile.queue)
    wipe(self.db.profile.matlist)
    self:Print("Queue cleared")
end

-- ============================================================================
-- STEP 4: Subcraft Expansion (with Cycle Detection)
-- ============================================================================

function Goblin:ExpandSubcrafts()
    local visited = {}
    local function expand(recipeId, parentId, depth)
        if depth > 20 then
            self:Print("WARNING: Max recursion depth reached for " .. recipeId)
            return
        end
        
        -- Cycle detection
        local key = recipeId .. "-" .. (parentId or "")
        if visited[key] then
            self:Print("WARNING: Cycle detected at " .. recipeId)
            return
        end
        visited[key] = true
        
        local link = self.db.profile.links[recipeId]
        if not link then return end
        
        -- Find total needed for this recipe across all queue entries
        local totalNeeded = 0
        for _, entry in ipairs(self.db.profile.queue) do
            if entry.recipeId == recipeId then
                totalNeeded = totalNeeded + entry.qty
            end
        end
        
        -- Calculate reagent needs
        for _, reagent in ipairs(link.reagents) do
            local need = reagent.qty * totalNeeded
            local have = (self.db.profile.inventory[reagent.itemId] or {}).total or 0
            local short = math.max(need - have, 0)
            
            if short > 0 then
                -- Check if reagent can be crafted
                local producerRecipe = self:FindProducerRecipe(reagent.itemId)
                if producerRecipe then
                    local producerLink = self.db.profile.links[producerRecipe]
                    local craftsNeeded = math.ceil(short / producerLink.outputQty)
                    
                    self:AddToQueue(producerRecipe, craftsNeeded, "subcraft", recipeId)
                    expand(producerRecipe, recipeId, depth + 1)
                end
            end
        end
    end
    
    -- Expand from manual entries only
    local manualEntries = {}
    for _, entry in ipairs(self.db.profile.queue) do
        if entry.source == "manual" then
            table.insert(manualEntries, entry)
        end
    end
    
    for _, entry in ipairs(manualEntries) do
        expand(entry.recipeId, nil, 0)
    end
    
    self:ComputeMaterialList()
end

function Goblin:FindProducerRecipe(itemId)
    -- Find first recipe that produces this item (MVP: just first match)
    for recipeId, link in pairs(self.db.profile.links) do
        if link.outputItemId == itemId then
            return recipeId
        end
    end
    return nil
end

-- ============================================================================
-- STEP 5: Material List Computation
-- ============================================================================

function Goblin:ComputeMaterialList()
    local matlist = {}
    
    -- Traverse queue and sum base reagent needs
    for _, entry in ipairs(self.db.profile.queue) do
        local link = self.db.profile.links[entry.recipeId]
        if link then
            for _, reagent in ipairs(link.reagents) do
                local totalNeed = reagent.qty * entry.qty
                
                -- Only count if not crafted as subcraft
                local isCrafted = false
                for _, qEntry in ipairs(self.db.profile.queue) do
                    local qLink = self.db.profile.links[qEntry.recipeId]
                    if qLink and qLink.outputItemId == reagent.itemId then
                        isCrafted = true
                        break
                    end
                end
                
                if not isCrafted then
                    matlist[reagent.itemId] = matlist[reagent.itemId] or { need = 0, have = 0, short = 0 }
                    matlist[reagent.itemId].need = matlist[reagent.itemId].need + totalNeed
                end
            end
        end
    end
    
    -- Compute have/short
    for itemId, data in pairs(matlist) do
        data.have = (self.db.profile.inventory[itemId] or {}).total or 0
        data.short = math.max(data.need - data.have, 0)
    end
    
    self.db.profile.matlist = matlist
end

-- ============================================================================
-- STEP 6: UI (Queue + Materials Tabs)
-- ============================================================================

function Goblin:ToggleUI()
    if not self.frame then
        self:CreateMainFrame()
    end
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
    end
end

function Goblin:CreateMainFrame()
    local frame = AceGUI:Create("Frame")
    frame:SetTitle("Goblin - Craft Queue")
    frame:SetStatusText("Workflow-Driven Crafting")
    frame:SetCallback("OnClose", function(widget) widget:Hide() end)
    frame:SetLayout("Fill")
    frame:SetWidth(900)
    frame:SetHeight(650)
    
    local tabGroup = AceGUI:Create("TabGroup")
    tabGroup:SetLayout("Flow")
    tabGroup:SetTabs({
        {text="Queue", value="queue"},
        {text="Materials", value="materials"}
    })
    tabGroup:SetCallback("OnGroupSelected", function(container, event, group)
        container:ReleaseChildren()
        if group == "queue" then
            Goblin:DrawQueueTab(container)
        elseif group == "materials" then
            Goblin:DrawMaterialsTab(container)
        end
    end)
    
    frame:AddChild(tabGroup)
    tabGroup:SelectTab("queue")
    
    self.frame = frame
end

function Goblin:DrawQueueTab(container)
    -- Auto Subcraft Toggle
    local toggle = AceGUI:Create("CheckBox")
    toggle:SetLabel("Auto Subcraft")
    toggle:SetValue(self.db.profile.settings.autoSubcraft)
    toggle:SetCallback("OnValueChanged", function(widget, event, val)
        self.db.profile.settings.autoSubcraft = val
        if val then
            self:ExpandSubcrafts()
        end
    end)
    container:AddChild(toggle)
    
    -- Clear Queue Button
    local btnClear = AceGUI:Create("Button")
    btnClear:SetText("Clear Queue")
    btnClear:SetWidth(150)
    btnClear:SetCallback("OnClick", function()
        self:ClearQueue()
        container:ReleaseChildren()
        self:DrawQueueTab(container)
    end)
    container:AddChild(btnClear)
    
    -- Queue List
    local scroll = AceGUI:Create("ScrollFrame")
    scroll:SetLayout("Flow")
    scroll:SetFullWidth(true)
    scroll:SetFullHeight(true)
    
    if #self.db.profile.queue == 0 then
        local label = AceGUI:Create("Label")
        label:SetText("Queue is empty. Use /gob add <recipeId> or open profession UI.")
        label:SetFullWidth(true)
        scroll:AddChild(label)
    else
        for i, entry in ipairs(self.db.profile.queue) do
            local link = self.db.profile.links[entry.recipeId]
            local name = link and link.name or "Recipe " .. entry.recipeId
            
            local label = AceGUI:Create("Label")
            label:SetText(string.format("%s%s x%d (%s)", 
                entry.source == "subcraft" and "  ↳ " or "",
                name,
                entry.qty,
                entry.source
            ))
            label:SetFullWidth(true)
            scroll:AddChild(label)
        end
    end
    
    container:AddChild(scroll)
end

function Goblin:DrawMaterialsTab(container)
    local scroll = AceGUI:Create("ScrollFrame")
    scroll:SetLayout("Flow")
    scroll:SetFullWidth(true)
    scroll:SetFullHeight(true)
    
    if not next(self.db.profile.matlist) then
        local label = AceGUI:Create("Label")
        label:SetText("No materials needed. Add recipes to queue.")
        label:SetFullWidth(true)
        scroll:AddChild(label)
    else
        -- Header
        local header = AceGUI:Create("Label")
        header:SetText(string.format("%-30s %10s %10s %10s", "Item", "Need", "Have", "Short"))
        header:SetFont("Fonts\\FRIZQT__.TTF", 12, "OUTLINE")
        header:SetFullWidth(true)
        scroll:AddChild(header)
        
        -- Sort by short desc
        local sorted = {}
        for itemId, data in pairs(self.db.profile.matlist) do
            table.insert(sorted, {itemId = itemId, data = data})
        end
        table.sort(sorted, function(a, b) return a.data.short > b.data.short end)
        
        for _, entry in ipairs(sorted) do
            local itemName = GetItemInfo(entry.itemId) or "Item " .. entry.itemId
            local label = AceGUI:Create("Label")
            label:SetText(string.format("%-30s %10d %10d %10d", 
                itemName,
                entry.data.need,
                entry.data.have,
                entry.data.short
            ))
            label:SetFullWidth(true)
            
            if entry.data.short > 0 then
                label:SetColor(1, 0.5, 0.5)
            else
                label:SetColor(0.5, 1, 0.5)
            end
            
            scroll:AddChild(label)
        end
    end
    
    container:AddChild(scroll)
end

-- ============================================================================
-- STEP 7: Commands
-- ============================================================================

function Goblin:HandleCommand(input)
    local cmd, arg = input:match("^(%S*)%s*(.-)$")
    cmd = cmd:lower()
    
    if cmd == "dump" then
        local invCount = self:CountKeys(self.db.profile.inventory)
        local recipeCount = self:CountKeys(self.db.profile.links)
        local queueCount = #self.db.profile.queue
        local matCount = self:CountKeys(self.db.profile.matlist)
        
        self:Print(string.format("DUMP: Inv=%d, Recipes=%d, Queue=%d, Mats=%d",
            invCount, recipeCount, queueCount, matCount))
        
    elseif cmd == "sanity" then
        local passed = true
        
        -- Check 1: Queue qty >= 0
        for i, entry in ipairs(self.db.profile.queue) do
            if entry.qty < 0 then
                self:Print("FAIL: Negative qty at index " .. i)
                passed = false
            end
        end
        
        -- Check 2: No cycles (simple parent chain check)
        local function hasParentCycle(entry, depth)
            if depth > 20 then return true end
            if not entry.parentRecipeId then return false end
            for _, e in ipairs(self.db.profile.queue) do
                if e.recipeId == entry.parentRecipeId then
                    return hasParentCycle(e, depth + 1)
                end
            end
            return false
        end
        
        for _, entry in ipairs(self.db.profile.queue) do
            if hasParentCycle(entry, 0) then
                self:Print("FAIL: Cycle detected")
                passed = false
                break
            end
        end
        
        if passed then
            self:Print("|cff00FF00SANITY PASS|r")
        else
            self:Print("|cffFF0000SANITY FAIL|r")
        end
        
    elseif cmd == "rebuild" then
        self:ExpandSubcrafts()
        self:Print("Rebuilt subcrafts and materials")
        
    elseif cmd == "resetdb" then
        GoblinDB = nil
        ReloadUI()
        
    elseif cmd == "scan" then
        self:ScanInventory()
        
    elseif cmd == "ingest" then
        self:IngestRecipes()
        
    elseif cmd == "add" and arg ~= "" then
        local recipeId = tonumber(arg)
        if recipeId then
            self:AddToQueue(recipeId, 1, "manual")
        else
            self:Print("Usage: /gob add <recipeId>")
        end
        
    else
        self:ToggleUI()
    end
end

-- ============================================================================
-- Utilities
-- ============================================================================

function Goblin:CountKeys(tbl)
    local count = 0
    for _ in pairs(tbl) do count = count + 1 end
    return count
end
