-- UI/CraftingQueue.lua - Display and manage crafting queue

GoblinAI.CraftingQueue = {}
local QueueFrame = GoblinAI.CraftingQueue

function QueueFrame:Initialize()
    self:CreateUI()
end

function QueueFrame:CreateUI()
    -- Main Frame
    self.frame = CreateFrame("Frame", "GoblinAICraftingQueue", UIParent, "BasicFrameTemplateWithInset")
    self.frame:SetSize(500, 600)
    self.frame:SetPoint("CENTER")
    self.frame:SetMovable(true)
    self.frame:EnableMouse(true)
    self.frame:RegisterForDrag("LeftButton")
    self.frame:SetScript("OnDragStart", self.frame.StartMoving)
    self.frame:SetScript("OnDragStop", self.frame.StopMovingOrSizing)
    self.frame:Hide()

    -- Title
    self.frame.title = self.frame:CreateFontString(nil, "OVERLAY")
    self.frame.title:SetFontObject("GameFontHighlight")
    self.frame.title:SetPoint("LEFT", self.frame.TitleBg, "LEFT", 5, 0)
    self.frame.title:SetText("Goblin AI - Crafting Queue")

    -- Scroll Frame
    self.scrollFrame = CreateFrame("ScrollFrame", nil, self.frame, "UIPanelScrollFrameTemplate")
    self.scrollFrame:SetPoint("TOPLEFT", 10, -30)
    self.scrollFrame:SetPoint("BOTTOMRIGHT", -30, 40)

    self.content = CreateFrame("Frame", nil, self.scrollFrame)
    self.content:SetSize(450, 800)
    self.scrollFrame:SetScrollChild(self.content)

    -- Craft Next Button
    self.craftBtn = CreateFrame("Button", nil, self.frame, "GameMenuButtonTemplate")
    self.craftBtn:SetPoint("BOTTOM", 0, 10)
    self.craftBtn:SetSize(140, 25)
    self.craftBtn:SetText("Craft Next")
    self.craftBtn:SetScript("OnClick", function()
        GoblinAI.CraftingManager:CraftNext()
    end)
end

function QueueFrame:UpdateList()
    -- Clear list
    local children = {self.content:GetChildren()}
    for _, child in ipairs(children) do
        child:Hide()
    end

    local queue = GoblinAI.CraftingManager:GetQueue()
    local yOffset = 0

    for i, craft in ipairs(queue) do
        local row = self:CreateRow(i, craft)
        row:SetPoint("TOPLEFT", 0, yOffset)
        yOffset = yOffset - 40
    end
    
    self.content:SetHeight(math.abs(yOffset))
end

function QueueFrame:CreateRow(index, craft)
    local row = CreateFrame("Button", nil, self.content)
    row:SetSize(450, 35)

    -- Background
    local bg = row:CreateTexture(nil, "BACKGROUND")
    bg:SetAllPoints()
    if index % 2 == 0 then
        bg:SetColorTexture(0.1, 0.1, 0.1, 0.5)
    else
        bg:SetColorTexture(0.2, 0.2, 0.2, 0.5)
    end

    -- Icon
    local icon = row:CreateTexture(nil, "ARTWORK")
    icon:SetSize(28, 28)
    icon:SetPoint("LEFT", 5, 0)
    local _, _, _, _, iconTexture = GetItemInfoInstant(craft.itemID)
    icon:SetTexture(iconTexture)

    -- Name & Quantity
    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    name:SetPoint("LEFT", icon, "RIGHT", 5, 5)
    name:SetText(craft.itemName .. " x" .. craft.quantity)

    -- Profit
    local profit = row:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    profit:SetPoint("LEFT", icon, "RIGHT", 5, -8)
    profit:SetText("Est. Profit: " .. GoblinAI:FormatGold(craft.profit))
    profit:SetTextColor(0, 1, 0)

    -- Remove Button
    local removeBtn = CreateFrame("Button", nil, row, "UIPanelCloseButton")
    removeBtn:SetSize(20, 20)
    removeBtn:SetPoint("RIGHT", -5, 0)
    removeBtn:SetScript("OnClick", function()
        GoblinAI.CraftingManager:RemoveFromQueue(index)
        self:UpdateList()
    end)

    return row
end

function QueueFrame:Toggle()
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
        self:UpdateList()
    end
end
