-- UI/OpportunityFrame.lua - Display and execute profitable opportunities

GoblinAI.OpportunityFrame = {}
local OppFrame = GoblinAI.OpportunityFrame

function OppFrame:Initialize()
    self:CreateUI()
    self:RegisterEvents()
end

function OppFrame:CreateUI()
    -- Main Frame
    self.frame = CreateFrame("Frame", "GoblinAIOpportunityFrame", UIParent, "BasicFrameTemplateWithInset")
    self.frame:SetSize(600, 400)
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
    self.frame.title:SetText("Goblin AI - Opportunities")

    -- Scroll Frame for List
    self.scrollFrame = CreateFrame("ScrollFrame", nil, self.frame, "UIPanelScrollFrameTemplate")
    self.scrollFrame:SetPoint("TOPLEFT", 10, -30)
    self.scrollFrame:SetPoint("BOTTOMRIGHT", -30, 40)

    self.content = CreateFrame("Frame", nil, self.scrollFrame)
    self.content:SetSize(550, 800) -- Dynamic height
    self.scrollFrame:SetScrollChild(self.content)

    -- Execute Button (The "Minimal Effort" Button)
    self.executeBtn = CreateFrame("Button", nil, self.frame, "GameMenuButtonTemplate")
    self.executeBtn:SetPoint("BOTTOM", 0, 10)
    self.executeBtn:SetSize(140, 25)
    self.executeBtn:SetText("Execute Top Deal")
    self.executeBtn:SetScript("OnClick", function()
        GoblinAI.AssistedTrader:ExecuteNext()
    end)
    
    -- Refresh Button
    self.refreshBtn = CreateFrame("Button", nil, self.frame, "GameMenuButtonTemplate")
    self.refreshBtn:SetPoint("BOTTOMLEFT", 10, 10)
    self.refreshBtn:SetSize(100, 25)
    self.refreshBtn:SetText("Refresh")
    self.refreshBtn:SetScript("OnClick", function()
        self:UpdateList()
    end)
end

function OppFrame:RegisterEvents()
    -- Listen for new data
end

function OppFrame:Toggle()
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
        self:UpdateList()
    end
end

function OppFrame:UpdateList()
    -- Clear current list
    local children = {self.content:GetChildren()}
    for _, child in ipairs(children) do
        child:Hide()
    end

    -- Get opportunities from DB
    local opportunities = GoblinAIDB.opportunities or {}
    
    -- Sort by Profit
    table.sort(opportunities, function(a, b)
        return (a.profit or 0) > (b.profit or 0)
    end)

    local yOffset = 0
    for i, opp in ipairs(opportunities) do
        if i > 50 then break end -- Show top 50

        local row = self:CreateRow(i, opp)
        row:SetPoint("TOPLEFT", 0, yOffset)
        yOffset = yOffset - 35
    end
    
    self.content:SetHeight(math.abs(yOffset))
end

function OppFrame:CreateRow(index, opp)
    local row = CreateFrame("Button", nil, self.content)
    row:SetSize(550, 30)
    
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
    icon:SetSize(24, 24)
    icon:SetPoint("LEFT", 5, 0)
    local _, _, _, _, iconTexture = GetItemInfoInstant(opp.itemID)
    icon:SetTexture(iconTexture)

    -- Name
    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    name:SetPoint("LEFT", icon, "RIGHT", 5, 0)
    name:SetText(opp.itemName or "Unknown Item")

    -- Profit
    local profit = row:CreateFontString(nil, "OVERLAY", "GameFontHighlightRight")
    profit:SetPoint("RIGHT", -10, 0)
    profit:SetText(GoblinAI:FormatGold(opp.profit))
    profit:SetTextColor(0, 1, 0) -- Green

    -- Buy Price
    local buyPrice = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    buyPrice:SetPoint("RIGHT", profit, "LEFT", -10, 0)
    buyPrice:SetText("Buy: " .. GoblinAI:FormatGold(opp.buyPrice))

    -- Click to Buy
    row:SetScript("OnClick", function()
        GoblinAI.AssistedTrader:QueueItem(opp)
    end)

    return row
end
