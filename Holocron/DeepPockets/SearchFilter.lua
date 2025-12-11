-- SearchFilter.lua
-- Search and filter functionality for DeepPockets

local _, addon = ...
addon.SearchFilter = {}
local Filter = addon.SearchFilter

-- Filter state
Filter.searchText = ""
Filter.qualityFilter = nil
Filter.typeFilter = nil

-- Create search UI
function Filter:CreateUI(parentFrame)
    if Filter.searchBox then return end  -- Already created
    
    -- Search Box
    local searchBox = CreateFrame("EditBox", "DeepPocketsSearchBox", parentFrame, "InputBoxTemplate")
    searchBox:SetSize(200, 20)
    searchBox:SetPoint("TOPLEFT", parentFrame, "TOPLEFT", 80, -10)
    searchBox:SetAutoFocus(false)
    searchBox:SetText("Search...")
    
    searchBox:SetScript("OnTextChanged", function(self)
        local text = self:GetText()
        if text == "Search..." then text = "" end
        Filter.searchText = text:lower()
        addon:RenderGrid()
    end)
    
    searchBox:SetScript("OnEditFocusGained", function(self)
        if self:GetText() == "Search..." then
            self:SetText("")
        end
    end)
    
    searchBox:SetScript("OnEditFocusLost", function(self)
        if self:GetText() == "" then
            self:SetText("Search...")
        end
    end)
    
    Filter.searchBox = searchBox
    
    -- Quality Filter Dropdown
    local qualityDropdown = CreateFrame("Frame", "DeepPocketsQualityFilter", parentFrame, "UIDropDownMenuTemplate")
    qualityDropdown:SetPoint("TOPLEFT", searchBox, "BOTTOMLEFT", -15, -5)
    
    UIDropDownMenu_SetWidth(qualityDropdown, 100)
    UIDropDownMenu_SetText(qualityDropdown, "All Quality")
    
    local function QualityDropdown_OnClick(self)
        Filter.qualityFilter = self.value
        UIDropDownMenu_SetText(qualityDropdown, self:GetText())
        addon:RenderGrid()
    end
    
    local function QualityDropdown_Initialize(self, level)
        local info = UIDropDownMenu_CreateInfo()
        
        -- All
        info.text = "All Quality"
        info.value = nil
        info.func = QualityDropdown_OnClick
        UIDropDownMenu_AddButton(info)
        
        -- Qualities
        local qualities = {
            {text = "Poor (Gray)", value = 0},
            {text = "Common (White)", value = 1},
            {text = "Uncommon (Green)", value = 2},
            {text = "Rare (Blue)", value = 3},
            {text = "Epic (Purple)", value = 4},
            {text = "Legendary (Orange)", value = 5}
        }
        
        for _, q in ipairs(qualities) do
            info.text = q.text
            info.value = q.value
            info.func = QualityDropdown_OnClick
            UIDropDownMenu_AddButton(info)
        end
    end
    
    UIDropDownMenu_Initialize(qualityDropdown, QualityDropdown_Initialize)
    Filter.qualityDropdown = qualityDropdown
    
    -- Type Filter Dropdown
    local typeDropdown = CreateFrame("Frame", "DeepPocketsTypeFilter", parentFrame, "UIDropDownMenuTemplate")
    typeDropdown:SetPoint("LEFT", qualityDropdown, "RIGHT", -10, 0)
    
    UIDropDownMenu_SetWidth(typeDropdown, 120)
    UIDropDownMenu_SetText(typeDropdown, "All Types")
    
    local function TypeDropdown_OnClick(self)
        Filter.typeFilter = self.value
        UIDropDownMenu_SetText(typeDropdown, self:GetText())
        addon:RenderGrid()
    end
    
    local function TypeDropdown_Initialize(self, level)
        local info = UIDropDownMenu_CreateInfo()
        
        -- All
        info.text = "All Types"
        info.value = nil
        info.func = TypeDropdown_OnClick
        UIDropDownMenu_AddButton(info)
        
        -- Common types
        local types = {"Quest", "Consumable", "Trade Goods", "Equipment", "Junk", "Other"}
        for _, itemType in ipairs(types) do
            info.text = itemType
            info.value = itemType
            info.func = TypeDropdown_OnClick
            UIDropDownMenu_AddButton(info)
        end
    end
    
    UIDropDownMenu_Initialize(typeDropdown, TypeDropdown_Initialize)
    Filter.typeDropdown = typeDropdown
end

-- Apply filters to item list
function Filter:ApplyFilters(items)
    if not items then return {} end
    
    local filtered = {}
    
    for _, item in ipairs(items) do
        local include = true
        
        -- Search filter
        if Filter.searchText and Filter.searchText ~= "" then
            local itemName = item.link and item.link:match("|h%[(.-)%]|h") or ""
            if not itemName:lower():find(Filter.searchText, 1, true) then
                include = false
            end
        end
        
        -- Quality filter
        if Filter.qualityFilter and item.quality ~= Filter.qualityFilter then
            include = false
        end
        
        -- Type filter
        if Filter.typeFilter then
            -- Map category to type
            local category = item.category or addon:GetItemCategory(item)
            if category ~= Filter.typeFilter then
                include = false
            end
        end
        
        if include then
            table.insert(filtered, item)
        end
    end
    
    return filtered
end

-- Get item category (helper for filtering)
function addon:GetItemCategory(item)
    if item.quality == 0 then
        return "Junk"
    elseif item.type == "Quest" or item.type == "Questline" then
        return "Quest"
    elseif item.type == "Consumable" then
        return "Consumable"
    elseif item.type == "Trade Goods" or item.type == "Tradeskill" then
        return "Trade Goods"
    elseif item.type == "Armor" or item.type == "Weapon" then
        return "Equipment"
    else
        return "Other"
    end
end
