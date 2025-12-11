-- Materials/CraftingManager.lua - Manage crafting logic and queue

GoblinAI.CraftingManager = {}
local CM = GoblinAI.CraftingManager

CM.queue = {}

function CM:Initialize()
    -- Load queue from SavedVariables if exists
    if GoblinAIDB.craftingQueue then
        self.queue = GoblinAIDB.craftingQueue
    end
end

function CM:AddToQueue(craft)
    table.insert(self.queue, craft)
    self:SaveQueue()
    
    if GoblinAI.CraftingQueue and GoblinAI.CraftingQueue.frame:IsShown() then
        GoblinAI.CraftingQueue:UpdateList()
    end
    
    print("|cFF00FF00Goblin AI|r: Added " .. craft.itemName .. " to crafting queue")
end

function CM:RemoveFromQueue(index)
    table.remove(self.queue, index)
    self:SaveQueue()
end

function CM:GetQueue()
    return self.queue
end

function CM:SaveQueue()
    GoblinAIDB.craftingQueue = self.queue
end

function CM:CraftNext()
    if #self.queue == 0 then
        print("|cFFFF0000Goblin AI|r: Crafting queue is empty")
        return
    end

    local craft = self.queue[1]
    
    -- Check if trade skill window is open
    if not C_TradeSkillUI.IsTradeSkillOpen() then
        print("|cFFFF0000Goblin AI|r: Please open your profession window")
        return
    end
    
    -- Find recipe ID
    local recipeInfo = C_TradeSkillUI.GetRecipeInfo(craft.recipeID)
    if not recipeInfo then
        print("|cFFFF0000Goblin AI|r: Recipe not found")
        return
    end
    
    -- Check materials
    if not C_TradeSkillUI.CanCraftRecipe(craft.recipeID) then
        print("|cFFFF0000Goblin AI|r: Missing materials for " .. craft.itemName)
        -- Could trigger auto-shopping here
        return
    end
    
    -- Craft!
    C_TradeSkillUI.CraftRecipe(craft.recipeID, 1) -- Craft 1 at a time for safety/control
    
    -- Decrement quantity or remove
    craft.quantity = craft.quantity - 1
    if craft.quantity <= 0 then
        table.remove(self.queue, 1)
    end
    
    self:SaveQueue()
    
    if GoblinAI.CraftingQueue then
        GoblinAI.CraftingQueue:UpdateList()
    end
end

function CM:CalculateCraftingCost(recipeID)
    -- Calculate cost based on material prices (from scan data)
    -- This is complex, simplified for now
    return 0 -- Placeholder
end
