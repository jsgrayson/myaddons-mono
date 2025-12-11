-- OptionsPanel.lua
-- Shared options panel framework for Holocron addons

local LIBRARY_NAME = "HolocronOptions-1.0"
local LIBRARY_VERSION = 1

if not LibStub then LibStub = {} end
local lib = LibStub:NewLibrary and LibStub:NewLibrary(LIBRARY_NAME, LIBRARY_VERSION)
if not lib then
    lib = {}
    _G[LIBRARY_NAME] = lib
end

-- Create an options panel
function lib:CreateOptionsPanel(addonName, config)
    config = config or {}
    
    local panel = CreateFrame("Frame", addonName .. "OptionsPanel")
    panel.name = config.title or addonName
    panel.parent = config.parent
    
    -- Title
    local title = panel:CreateFontString(nil, "ARTWORK", "GameFontNormalLarge")
    title:SetPoint("TOPLEFT", 16, -16)
    title:SetText(config.title or addonName)
    
    -- Subtitle
    if config.subtitle then
        local subtitle = panel:CreateFontString(nil, "ARTWORK", "GameFontHighlightSmall")
        subtitle:SetPoint("TOPLEFT", title, "BOTTOMLEFT", 0, -8)
        subtitle:SetText(config.subtitle)
        subtitle:SetNonSpaceWrap(true)
        subtitle:SetJustifyH("LEFT")
        subtitle:SetJustifyV("TOP")
        panel.subtitle = subtitle
    end
    
    -- Container for options
    panel.controls = {}
    panel.yOffset = -60
    
    -- Add checkbox option
    function panel:AddCheckbox(option)
        local check = CreateFrame("CheckButton", nil, self, "InterfaceOptionsCheckButtonTemplate")
        check:SetPoint("TOPLEFT", 20, self.yOffset)
        check.Text:SetText(option.name)
        
        -- Load saved value
        if option.get then
            check:SetChecked(option.get())
        end
        
        check:SetScript("OnClick", function(self)
            if option.set then
                option.set(self:GetChecked())
            end
            if option.callback then
                option.callback(self:GetChecked())
            end
        end)
        
        if option.tooltip then
            check.tooltipText = option.tooltip
        end
        
        table.insert(self.controls, check)
        self.yOffset = self.yOffset - 30
        return check
    end
    
    -- Add slider option
    function panel:AddSlider(option)
        local slider = CreateFrame("Slider", nil, self, "OptionsSliderTemplate")
        slider:SetPoint("TOPLEFT", 20, self.yOffset)
        slider:SetMinMaxValues(option.min or 0, option.max or 100)
        slider:SetValueStep(option.step or 1)
        slider:SetObeyStepOnDrag(true)
        
        -- Labels
        slider.Text:SetText(option.name)
        slider.Low:SetText(option.minText or option.min)
        slider.High:SetText(option.maxText or option.max)
        
        -- Load saved value
        if option.get then
            slider:SetValue(option.get())
        end
        
        slider:SetScript("OnValueChanged", function(self, value)
            if option.format then
                self.Text:SetText(string.format(option.format, value))
            else
                self.Text:SetText(option.name .. ": " .. value)
            end
            
            if option.set then
                option.set(value)
            end
            if option.callback then
                option.callback(value)
            end
        end)
        
        -- Trigger initial display
        slider:GetScript("OnValueChanged")(slider, slider:GetValue())
        
        table.insert(self.controls, slider)
        self.yOffset = self.yOffset - 60
        return slider
    end
    
    -- Add dropdown option
    function panel:AddDropdown(option)
        local dropdown = CreateFrame("Frame", nil, self, "UIDropDownMenuTemplate")
        dropdown:SetPoint("TOPLEFT", 10, self.yOffset)
        
        -- Label
        local label = self:CreateFontString(nil, "ARTWORK", "GameFontNormal")
        label:SetPoint("BOTTOMLEFT", dropdown, "TOPLEFT", 20, 0)
        label:SetText(option.name)
        
        UIDropDownMenu_SetWidth(dropdown, option.width or 150)
        
        local function OnClick(self)
            UIDropDownMenu_SetSelectedValue(dropdown, self.value)
            if option.set then
                option.set(self.value)
            end
            if option.callback then
                option.callback(self.value)
            end
        end
        
        local function Initialize(self, level)
            local info = UIDropDownMenu_CreateInfo()
            for _, item in ipairs(option.items) do
                info.text = item.text
                info.value = item.value
                info.func = OnClick
                UIDropDownMenu_AddButton(info)
            end
        end
        
        UIDropDownMenu_Initialize(dropdown, Initialize)
        
        -- Load saved value
        if option.get then
            UIDropDownMenu_SetSelectedValue(dropdown, option.get())
        end
        
        table.insert(self.controls, dropdown)
        self.yOffset = self.yOffset - 50
        return dropdown
    end
    
    -- Add button
    function panel:AddButton(option)
        local button = CreateFrame("Button", nil, self, "UIPanelButtonTemplate")
        button:SetPoint("TOPLEFT", 20, self.yOffset)
        button:SetSize(option.width or 150, 25)
        button:SetText(option.name)
        
        button:SetScript("OnClick", function(self)
            if option.callback then
                option.callback()
            end
        end)
        
        if option.tooltip then
            button.tooltipText = option.tooltip
        end
        
        table.insert(self.controls, button)
        self.yOffset = self.yOffset - 35
        return button
    end
    
    -- Add header
    function panel:AddHeader(text)
        local header = self:CreateFontString(nil, "ARTWORK", "GameFontNormalLarge")
        header:SetPoint("TOPLEFT", 20, self.yOffset)
        header:SetText(text)
        
        table.insert(self.controls, header)
        self.yOffset = self.yOffset - 30
        return header
    end
    
    -- Add description text
    function panel:AddDescription(text)
        local desc = self:CreateFontString(nil, "ARTWORK", "GameFontHighlightSmall")
        desc:SetPoint("TOPLEFT", 20, self.yOffset)
        desc:SetWidth(550)
        desc:SetText(text)
        desc:SetJustifyH("LEFT")
        desc:SetNonSpaceWrap(true)
        
        table.insert(self.controls, desc)
        self.yOffset = self.yOffset - 40
        return desc
    end
    
    -- Okay/Cancel handlers
    panel.okay = function(self)
        if config.onOkay then
            config.onOkay()
        end
    end
    
    panel.cancel = function(self)
        if config.onCancel then
            config.onCancel()
        end
    end
    
    panel.default = function(self)
        if config.onDefault then
            config.onDefault()
        end
    end
    
    -- Register with Interface Options if available
    if InterfaceOptions_AddCategory then
        InterfaceOptions_AddCategory(panel)
    elseif Settings and Settings.RegisterCanvasLayoutCategory then
        -- Dragonflight+ API
        local category = Settings.RegisterCanvasLayoutCategory(panel, panel.name)
        category.ID = panel.name
        Settings.RegisterAddOnCategory(category)
    end
    
    return panel
end

return lib
