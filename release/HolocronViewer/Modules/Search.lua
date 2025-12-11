local addonName, addon = ...
addon.Search = {}
local Search = addon.Search

function Search:Create(parent)
    local frame = CreateFrame("Frame", nil, parent)
    frame:SetAllPoints()
    frame:Hide()
    
    -- Title
    local title = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOPLEFT", 10, -10)
    title:SetText("Item Search")
    
    -- Search Box
    local searchBox = CreateFrame("EditBox", nil, frame, "InputBoxTemplate")
    searchBox:SetSize(300, 30)
    searchBox:SetPoint("TOPLEFT", 10, -40)
    searchBox:SetAutoFocus(false)
    searchBox:SetTextInsets(5, 5, 0, 0)
    searchBox:SetFontObject("ChatFontNormal")
    
    searchBox:SetScript("OnEnterPressed", function(self)
        local query = self:GetText()
        Search:PerformSearch(query)
        self:ClearFocus()
    end)
    
    -- Search Button
    local searchBtn = CreateFrame("Button", nil, frame, "UIPanelButtonTemplate")
    searchBtn:SetSize(80, 30)
    searchBtn:SetPoint("LEFT", searchBox, "RIGHT", 10, 0)
    searchBtn:SetText("Search")
    searchBtn:SetScript("OnClick", function()
        local query = searchBox:GetText()
        Search:PerformSearch(query)
        searchBox:ClearFocus()
    end)
    
    -- Results ScrollFrame
    local scroll = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
    scroll:SetPoint("TOPLEFT", 10, -80)
    scroll:SetPoint("BOTTOMRIGHT", -30, 10)
    
    local content = CreateFrame("Frame", nil, scroll)
    content:SetSize(500, 1) 
    scroll:SetScrollChild(content)
    self.content = content
    
    self.frame = frame
    return frame
end

function Search:PerformSearch(query)
    if not query or query == "" then return end
    
    print("Holocron: Searching for '" .. query .. "'...")
    
    -- Clear previous results
    for _, child in ipairs({self.content:GetChildren()}) do
        child:Hide()
    end
    
    -- Send API Request
    addon.Holocron:SendRequest("/api/deeppockets/search", { q = query }, function(success, data)
        if success then
            Search:DisplayResults(data)
        else
            print("Holocron: Search failed.")
        end
    end)
end

function Search:DisplayResults(data)
    local results = data.results or {}
    local yOffset = 0
    
    if #results == 0 then
        local noResults = self.content:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        noResults:SetPoint("TOPLEFT", 5, -5)
        noResults:SetText("No items found.")
        return
    end
    
    for i, item in ipairs(results) do
        local row = CreateFrame("Frame", nil, self.content, "BackdropTemplate")
        row:SetSize(500, 40)
        row:SetPoint("TOPLEFT", 0, yOffset)
        
        row:SetBackdrop({
            bgFile = "Interface\\Buttons\\WHITE8X8",
            edgeFile = "Interface\\Buttons\\WHITE8X8",
            edgeSize = 1,
        })
        row:SetBackdropColor(0.1, 0.1, 0.1, 0.5)
        row:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
        
        -- Icon
        local icon = row:CreateTexture(nil, "ARTWORK")
        icon:SetSize(32, 32)
        icon:SetPoint("LEFT", 5, 0)
        icon:SetTexture(item.icon or "Interface\\Icons\\INV_Misc_QuestionMark")
        
        -- Name
        local name = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        name:SetPoint("LEFT", 45, 5)
        name:SetText(item.name)
        
        -- Location info
        local loc = row:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
        loc:SetPoint("LEFT", 45, -8)
        loc:SetText(string.format("%s - %s (x%d)", item.character, item.container, item.count))
        loc:SetTextColor(0.7, 0.7, 0.7)
        
        yOffset = yOffset - 45
    end
    
    self.content:SetHeight(math.max(1, #results * 45))
end
