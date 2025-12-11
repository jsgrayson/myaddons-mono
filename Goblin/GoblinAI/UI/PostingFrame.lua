-- UI/PostingFrame.lua - TSM-Style Group & Operation Management
-- Part of GoblinAI v2.0

GoblinAI.PostingFrame = {}
local Posting = GoblinAI.PostingFrame

Posting.selectedGroup = nil
Posting.selectedOperation = nil
Posting.postingQueue = {}

-- ============================================================================
-- Initialize Posting Tab
-- ============================================================================

function Posting:Initialize(parentFrame)
    self.frame = parentFrame
    self:CreateUI()
end

function Posting:CreateUI()
    -- Mode selector
    local modeFrame = CreateFrame("Frame", nil, self.frame)
    modeFrame:SetSize(660, 40)
    modeFrame:SetPoint("TOP", 0, -10)
    
    -- Groups button
    self.groupsBtn = CreateFrame("Button", nil, modeFrame, "UIPanelButtonTemplate")
    self.groupsBtn:SetSize(150, 30)
    self.groupsBtn:SetPoint("LEFT", 10, 0)
    self.groupsBtn:SetText("Manage Groups")
    self.groupsBtn:SetScript("OnClick", function()
        Posting:SetMode("groups")
    end)
    
    -- Operations button
    self.operationsBtn = CreateFrame("Button", nil, modeFrame, "UIPanelButtonTemplate")
    self.operationsBtn:SetSize(150, 30)
    self.operationsBtn:SetPoint("LEFT", self.groupsBtn, "RIGHT", 10, 0)
    self.operationsBtn:SetText("Operations")
    self.operationsBtn:SetScript("OnClick", function()
        Posting:SetMode("operations")
    end)
    
    -- Post button
    self.postBtn = CreateFrame("Button", nil, modeFrame, "UIPanelButtonTemplate")
    self.postBtn:SetSize(150, 30)
    self.postBtn:SetPoint("LEFT", self.operationsBtn, "RIGHT", 10, 0)
    self.postBtn:SetText("Bulk Post")
    self.postBtn:SetScript("OnClick", function()
        Posting:SetMode("post")
    end)
    
    -- Mailbox button
    self.mailBtn = CreateFrame("Button", nil, modeFrame, "UIPanelButtonTemplate")
    self.mailBtn:SetSize(100, 30)
    self.mailBtn:SetPoint("LEFT", self.postBtn, "RIGHT", 10, 0)
    self.mailBtn:SetText("Mailbox")
    self.mailBtn:SetScript("OnClick", function()
        Posting:SetMode("mail")
    end)
    
    -- Create content frames
    self:CreateGroupsUI()
    self:CreateOperationsUI()
    self:CreatePostingUI()
    self:CreateMailboxUI()
    
    self:SetMode("groups")
end

function Posting:SetMode(mode)
    -- Hide all
    if self.groupsContent then self.groupsContent:Hide() end
    if self.operationsContent then self.operationsContent:Hide() end
    if self.postingContent then self.postingContent:Hide() end
    if self.mailContent then self.mailContent:Hide() end
    
    -- Show selected
    if mode == "groups" and self.groupsContent then
        self.groupsContent:Show()
        self:RefreshGroups()
    elseif mode == "operations" and self.operationsContent then
        self.operationsContent:Show()
        self:RefreshOperations()
    elseif mode == "post" and self.postingContent then
        self.postingContent:Show()
        self:RefreshPostingQueue()
    elseif mode == "mail" and self.mailContent then
        self.mailContent:Show()
    end
end

-- ============================================================================
-- Groups UI
-- ============================================================================

function Posting:CreateGroupsUI()
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -60)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    content:Hide()
    
    -- Header
    local header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -5)
    header:SetText("Item Groups")
    header:SetTextColor(1, 0.84, 0, 1)
    
    -- Create group button
    local createBtn = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
    createBtn:SetSize(100, 25)
    createBtn:SetPoint("TOPRIGHT", -10, -5)
    createBtn:SetText("New Group")
    createBtn:SetScript("OnClick", function()
        Posting:CreateNewGroup()
    end)
    
    -- Group list (left side)
    local groupList = GoblinAI:CreateScrollFrame(content, 200, 400)
    groupList:SetPoint("TOPLEFT", 5, -40)
    self.groupList = groupList
    
    -- Group details (right side)
    local detailsFrame = CreateFrame("Frame", nil, content, "BackdropTemplate")
    detailsFrame:SetSize(430, 400)
    detailsFrame:SetPoint("TOPLEFT", groupList, "TOPRIGHT", 10, 0)
    detailsFrame:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    detailsFrame:SetBackdropColor(0.1, 0.1, 0.1, 0.5)
    detailsFrame:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
    
    local detailsTitle = detailsFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    detailsTitle:SetPoint("TOP", 0, -10)
    detailsTitle:SetText("Select a group")
    self.groupDetailsTitle = detailsTitle
    
    -- Add item to group
    local addItemBtn = CreateFrame("Button", nil, detailsFrame, "UIPanelButtonTemplate")
    addItemBtn:SetSize(100, 25)
    addItemBtn:SetPoint("TOP", 0, -35)
    addItemBtn:SetText("Add Item")
    addItemBtn:SetScript("OnClick", function()
        Posting:AddItemToGroup()
    end)
    self.addItemBtn = addItemBtn
    
    -- Item list in group
    local itemList = GoblinAI:CreateScrollFrame(detailsFrame, 410, 320)
    itemList:SetPoint("TOP", 0, -65)
    self.groupItemList = itemList
    
    self.groupsContent = content
end

function Posting:CreateNewGroup()
    StaticPopupDialogs["GOBLINAI_NEW_GROUP"] = {
        text = "Enter group name:",
        button1 = "Create",
        button2 = "Cancel",
        hasEditBox = true,
        maxLetters = 50,
        OnAccept = function(self)
            local name = self.editBox:GetText()
            if name and name ~= "" then
                if not GoblinAIDB.groups then
                    GoblinAIDB.groups = {}
                end
                
                table.insert(GoblinAIDB.groups, {
                    name = name,
                    items = {},
                    operation = nil,
                    created = time(),
                })
                
                print("|cFFFFD700Goblin AI:|r Group '" .. name .. "' created!")
                Posting:RefreshGroups()
            end
        end,
        timeout = 0,
        whileDead = true,
        hideOnEscape = true,
        preferredIndex = 3,
    }
    StaticPopup_Show("GOBLINAI_NEW_GROUP")
end

function Posting:RefreshGroups()
    if not self.groupList then return end
    
    -- Clear
    for _, child in ipairs({self.groupList.content:GetChildren()}) do
        child:Hide()
    end
    
    local groups = GoblinAIDB.groups or {}
    local yOffset = 0
    
    for i, group in ipairs(groups) do
        local groupRow = self:CreateGroupRow(group, i, yOffset)
        groupRow:SetParent(self.groupList.content)
        yOffset = yOffset - 40
    end
    
    self.groupList.content:SetHeight(math.max(1, #groups * 40))
end

function Posting:CreateGroupRow(group, index, yOffset)
    local row = CreateFrame("Button", nil, self.groupList.content, "BackdropTemplate")
    row:SetSize(190, 35)
    row:SetPoint("TOPLEFT", 5, yOffset)
    row:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    row:SetBackdropColor(0.1, 0.1, 0.1, 0.7)
    row:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
    
    -- Name
    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    name:SetPoint("LEFT", 5, 5)
    name:SetText(group.name)
    name:SetTextColor(1, 0.84, 0, 1)
    
    -- Item count
    local count = row:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    count:SetPoint("LEFT", 5, -8)
    count:SetText(#group.items .. " items")
    
    -- Click to select
    row:SetScript("OnClick", function()
        Posting:SelectGroup(index)
    end)
    
    return row
end

function Posting:SelectGroup(index)
    local groups = GoblinAIDB.groups or {}
    local group = groups[index]
    if not group then return end
    
    self.selectedGroup = index
    self.groupDetailsTitle:SetText(group.name)
    
    -- Refresh item list
    self:RefreshGroupItems()
end

function Posting:RefreshGroupItems()
    if not self.selectedGroup or not self.groupItemList then return end
    
    local groups = GoblinAIDB.groups or {}
    local group = groups[self.selectedGroup]
    if not group then return end
    
    -- Clear
    for _, child in ipairs({self.groupItemList.content:GetChildren()}) do
        child:Hide()
    end
    
    local yOffset = 0
    for i, itemID in ipairs(group.items) do
        local itemRow = self:CreateGroupItemRow(itemID, i, yOffset)
        itemRow:SetParent(self.groupItemList.content)
        yOffset = yOffset - 40
    end
    
    self.groupItemList.content:SetHeight(math.max(1, #group.items * 40))
end

function Posting:CreateGroupItemRow(itemID, index, yOffset)
    local row = CreateFrame("Frame", nil, self.groupItemList.content, "BackdropTemplate")
    row:SetSize(390, 35)
    row:SetPoint("TOPLEFT", 5, yOffset)
    row:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Buttons\\WHITE8X8",
        edgeSize = 1,
    })
    row:SetBackdropColor(0.05, 0.05, 0.05, 0.7)
    row:SetBackdropBorderColor(0.2, 0.2, 0.2, 1)
    
    -- Icon
    local itemName, _, _, _, _, _, _, _, _, itemTexture = GetItemInfo(itemID)
    local icon = row:CreateTexture(nil, "ARTWORK")
    icon:SetSize(28, 28)
    icon:SetPoint("LEFT", 5, 0)
    icon:SetTexture(itemTexture or "Interface\\Icons\\INV_Misc_QuestionMark")
    
    -- Name
    local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    name:SetPoint("LEFT", 38, 0)
    name:SetText(itemName or ("Item " .. itemID))
    
    -- Remove button
    local removeBtn = CreateFrame("Button", nil, row, "UIPanelButtonTemplate")
    removeBtn:SetSize(60, 20)
    removeBtn:SetPoint("RIGHT", -5, 0)
    removeBtn:SetText("Remove")
    removeBtn:SetScript("OnClick", function()
        Posting:RemoveItemFromGroup(index)
    end)
    
    return row
end

function Posting:AddItemToGroup()
    if not self.selectedGroup then
        print("|cFFFF0000Goblin AI:|r Select a group first!")
        return
    end
    
    StaticPopupDialogs["GOBLINAI_ADD_ITEM"] = {
        text = "Enter item ID or link:",
        button1 = "Add",
        button2 = "Cancel",
        hasEditBox = true,
        OnAccept = function(self)
            local input = self.editBox:GetText()
            if input and input ~= "" then
                local itemID = tonumber(input) or GetItemInfoInstant(input)
                if itemID then
                    local groups = GoblinAIDB.groups or {}
                    local group = groups[Posting.selectedGroup]
                    if group then
                        table.insert(group.items, itemID)
                        Posting:RefreshGroupItems()
                        print("|cFFFFD700Goblin AI:|r Item added to group")
                    end
                end
            end
        end,
        timeout = 0,
        whileDead = true,
        hideOnEscape = true,
        preferredIndex = 3,
    }
    StaticPopup_Show("GOBLINAI_ADD_ITEM")
end

function Posting:RemoveItemFromGroup(itemIndex)
    if not self.selectedGroup then return end
    
    local groups = GoblinAIDB.groups or {}
    local group = groups[self.selectedGroup]
    if not group then return end
    
    table.remove(group.items, itemIndex)
    self:RefreshGroupItems()
end

-- ============================================================================
-- Operations UI
-- ============================================================================

function Posting:CreateOperationsUI()
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -60)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    content:Hide()
    
    local header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -5)
    header:SetText("Posting Operations")
    header:SetTextColor(1, 0.84, 0, 1)
    
    local info = content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    info:SetPoint("TOP", 0, -35)
    info:SetText("Operations define pricing rules for groups")
    
    -- Create operation button
    local createBtn = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
    createBtn:SetSize(120, 25)
    createBtn:SetPoint("TOP", 0, -65)
    createBtn:SetText("New Operation")
    createBtn:SetScript("OnClick", function()
        Posting:CreateNewOperation()
    end)
    
    self.operationsContent = content
end

function Posting:CreateNewOperation()
    StaticPopupDialogs["GOBLINAI_NEW_OPERATION"] = {
        text = "Enter operation name:",
        button1 = "Create",
        button2 = "Cancel",
        hasEditBox = true,
        OnAccept = function(self)
            local name = self.editBox:GetText()
            if name and name ~= "" then
                if not GoblinAIDB.operations then
                    GoblinAIDB.operations = {}
                end
                
                table.insert(GoblinAIDB.operations, {
                    name = name,
                    minPrice = 0.90, -- 90% of market
                    normalPrice = 1.10, -- 110% of market
                    maxPrice = 1.50, -- 150% of market
                    undercut = 1, -- Undercut by 1 copper
                    duration = 48, -- 48 hours
                    stackSize = 1,
                })
                
                print("|cFFFFD700Goblin AI:|r Operation '" .. name .. "' created!")
                Posting:RefreshOperations()
            end
        end,
        timeout = 0,
        whileDead = true,
        hideOnEscape = true,
        preferredIndex = 3,
    }
    StaticPopup_Show("GOBLINAI_NEW_OPERATION")
end

function Posting:RefreshOperations()
    -- Placeholder for operations list display
end

-- ============================================================================
-- Bulk Posting UI
-- ============================================================================

function Posting:CreatePostingUI()
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -60)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    content:Hide()
    
    local header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -5)
    header:SetText("Bulk Posting")
    header:SetTextColor(1, 0.84, 0, 1)
    
    -- Post all button
    local postAllBtn = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
    postAllBtn:SetSize(150, 30)
    postAllBtn:SetPoint("TOP", 0, -40)
    postAllBtn:SetText("Post All Groups")
    postAllBtn:SetScript("OnClick", function()
        Posting:StartBulkPost()
    end)
    
    -- Progress
    self.postProgress = content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    self.postProgress:SetPoint("TOP", 0, -80)
    self.postProgress:SetText("Ready to post")
    
    -- Queue list
    local queueScroll = GoblinAI:CreateScrollFrame(content, 650, 320)
    queueScroll:SetPoint("TOP", 0, -110)
    self.postQueue = queueScroll
    
    self.postingContent = content
end

function Posting:StartBulkPost()
    if not AuctionHouseFrame or not AuctionHouseFrame:IsShown() then
        print("|cFFFF0000Goblin AI:|r You must be at the auction house!")
        return
    end
    
    -- Build posting queue from groups
    self.postingQueue = {}
    local groups = GoblinAIDB.groups or {}
    
    for _, group in ipairs(groups) do
        for _, itemID in ipairs(group.items) do
            table.insert(self.postingQueue, {
                itemID = itemID,
                groupName = group.name,
                status = "pending",
            })
        end
    end
    
    if #self.postingQueue == 0 then
        print("|cFFFF0000Goblin AI:|r No items in groups to post!")
        return
    end
    
    print("|cFFFFD700Goblin AI:|r Starting bulk post - " .. #self.postingQueue .. " items queued")
    self:ProcessPostingQueue()
end

function Posting:ProcessPostingQueue()
    -- Process posting queue (throttled to avoid spam)
    -- In reality, this would interact with AH frames
    -- Due to Blizzard restrictions, actual posting requires user clicks
    
    self.postProgress:SetText("Posting " .. #self.postingQueue .. " items...")
    print("|cFFFFD700Goblin AI:|r Bulk posting requires manual clicks due to game restrictions")
end

function Posting:RefreshPostingQueue()
    -- Display current queue status
end

-- ============================================================================
-- Mailbox UI
-- ============================================================================

function Posting:CreateMailboxUI()
    local content = CreateFrame("Frame", nil, self.frame)
    content:SetPoint("TOPLEFT", 10, -60)
    content:SetPoint("BOTTOMRIGHT", -10, 10)
    content:Hide()
    
    local header = content:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOP", 0, -5)
    header:SetText("Mailbox Automation")
    header:SetTextColor(1, 0.84, 0, 1)
    
    -- Collect all button
    local collectBtn = CreateFrame("Button", nil, content, "UIPanelButtonTemplate")
    collectBtn:SetSize(150, 30)
    collectBtn:SetPoint("TOP", 0, -40)
    collectBtn:SetText("Collect All Mail")
    collectBtn:SetScript("OnClick", function()
        Posting:CollectAllMail()
    end)
    
    local info = content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    info:SetPoint("TOP", 0, -80)
    info:SetText("Quickly collect gold and items from mailbox")
    
    self.mailContent = content
end

function Posting:CollectAllMail()
    if not MailFrame or not MailFrame:IsShown() then
        print("|cFFFF0000Goblin AI:|r You must be at a mailbox!")
        return
    end
    
    local numItems = GetInboxNumItems()
    if numItems == 0 then
        print("|cFFFFD700Goblin AI:|r No mail to collect")
        return
    end
    
    print("|cFFFFD700Goblin AI:|r Collecting " .. numItems .. " mail items...")
    
    -- Auto-collect (throttled to avoid disconnects)
    for i = 1, numItems do
        C_Timer.After((i - 1) * 0.5, function()
            if GetInboxNumItems() >= i then
                TakeInboxMoney(i)
                TakeInboxItem(i)
            end
        end)
    end
end

-- ============================================================================
-- Initialization
-- ============================================================================

print("|cFFFFD700Goblin AI:|r Posting Frame loaded - Group & operation management ready")
