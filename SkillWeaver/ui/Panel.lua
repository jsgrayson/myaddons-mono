local SW = SkillWeaver
SW.UI = SW.UI or {}

-- 1. Helper to create a standard Checkbox (Robust Version)
local function CreateCheck(parent, label, dbKey, onClick)
    -- Note: Passing nil as name prevents _G lookup crashes
    local cb = CreateFrame("CheckButton", nil, parent, "ChatConfigCheckButtonTemplate")
    
    -- Explicitly create/attach the label if the template fails us (which it often does on unnamed frames)
    if not cb.Text then
        cb.Text = cb:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        cb.Text:SetPoint("LEFT", cb, "RIGHT", 0, 1)
    end
    
    cb.Text:SetText(label)
    
    cb:SetScript("OnClick", function(self)
        local val = self:GetChecked()
        if SkillWeaverDB and SkillWeaverDB.toggles then
            SkillWeaverDB.toggles[dbKey] = val
        end
        if onClick then onClick(val) end
        
        if SW.Engine and SW.Engine.RefreshAll then
            SW.Engine:RefreshAll("ui_toggle_" .. dbKey)
        end
    end)
    return cb
end

-- 2. Helper to create a Label
local function CreateLabel(parent, text, relativeTo, yOff)
    local fs = parent:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    fs:SetPoint("TOPLEFT", relativeTo, "BOTTOMLEFT", 0, yOff)
    fs:SetText(text)
    return fs
end

function SW.UI:InitPanel()
    if self.panel then return end

    -- Main Frame
    local f = CreateFrame("Frame", "SkillWeaver_Panel", UIParent, "BackdropTemplate")
    f:SetSize(300, 400) -- Increased height slightly for breathing room
    f:SetPoint("CENTER")
    f:SetMovable(true)
    f:EnableMouse(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)
    
    f:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        tile = true, tileSize = 16, edgeSize = 16,
        insets = { left=4, right=4, top=4, bottom=4 }
    })
    f:Hide()

    -- Title
    local title = f:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    title:SetPoint("TOP", 0, -12)
    title:SetText("SkillWeaver Command")

    -- Close Button
    local close = CreateFrame("Button", nil, f, "UIPanelCloseButton")
    close:SetPoint("TOPRIGHT", -4, -4)

    -- --- MODE DROPDOWN ---
    local modeLabel = CreateLabel(f, "Combat Mode:", f, -40)
    modeLabel:SetPoint("TOPLEFT", 20, -40)
    
    local modeDrop = CreateFrame("Frame", "SW_ModeDrop", f, "UIDropDownMenuTemplate")
    modeDrop:SetPoint("TOPLEFT", modeLabel, "BOTTOMLEFT", -15, -5)
    UIDropDownMenu_SetWidth(modeDrop, 180) -- Fix squash
    UIDropDownMenu_JustifyText(modeDrop, "LEFT")
    SW.UI.modeDrop = modeDrop

    -- --- INPUT DROPDOWN ---
    local inputLabel = CreateLabel(f, "Input Profile:", modeDrop, -10)
    inputLabel:SetPoint("TOPLEFT", 20, -100)
    
    local inputDrop = CreateFrame("Frame", "SW_InputDrop", f, "UIDropDownMenuTemplate")
    inputDrop:SetPoint("TOPLEFT", inputLabel, "BOTTOMLEFT", -15, -5)
    UIDropDownMenu_SetWidth(inputDrop, 180) -- Fix squash
    UIDropDownMenu_JustifyText(inputDrop, "LEFT")
    SW.UI.inputDrop = inputDrop

    -- --- TOGGLES ---
    local toggleLabel = CreateLabel(f, "Live Controls:", inputDrop, -15)
    toggleLabel:SetPoint("TOPLEFT", 20, -160)

    self.checks = {}
    local checks = {
        { k="burst", l="Burst Mode" },
        { k="defensives", l="Auto Defensives" },
        { k="interrupts", l="Auto Interrupts" },
        { k="showHealButton", l="Show Healer Helper" },
        { k="hideEmptyButtons", l="Hide Empty Buttons" },
    }

    local prev = toggleLabel
    for i, data in ipairs(checks) do
        local cb = CreateCheck(f, data.l, data.k)
        -- Slightly better spacing
        cb:SetPoint("TOPLEFT", prev, "BOTTOMLEFT", 0, (i==1 and -10 or -2))
        self.checks[data.k] = cb
        prev = cb
    end

    -- --- RELOAD BUTTON ---
    local rld = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    rld:SetSize(120, 25)
    rld:SetPoint("BOTTOM", 0, 20)
    rld:SetText("Reload UI")
    rld:SetScript("OnClick", ReloadUI)

    self.panel = f
    self:SetupDropdowns()
end

function SW.UI:SetupDropdowns()
    -- 1. Mode Menu Init
    UIDropDownMenu_Initialize(self.modeDrop, function(self, level, menuList)
        local modes = { "Delves", "MythicPlus", "Raid", "PvP", "OpenWorld" }
        for _, m in ipairs(modes) do
            local info = UIDropDownMenu_CreateInfo()
            info.text = m
            info.checked = (SW.State:GetMode() == m)
            info.func = function() 
                SW.State:SetMode(m) 
                local key = SW.State:GetClassSpecKey()
                if SW.Profiles and SW.Profiles.LoadProfile then
                    SW.Profiles:LoadProfile(key, m, "Balanced")
                end
                SW.UI:UpdatePanel()
                CloseDropDownMenus()
            end
            UIDropDownMenu_AddButton(info)
        end
    end)

    -- 2. Input Menu Init
    UIDropDownMenu_Initialize(self.inputDrop, function(self, level, menuList)
        local profiles = { "Keyboard", "Controller", "MMO_Mouse" }
        if SkillWeaverDB and SkillWeaverDB.bindingProfiles then
             for k,_ in pairs(SkillWeaverDB.bindingProfiles) do
                 local exists = false
                 for _,p in ipairs(profiles) do if p == k then exists = true end end
                 if not exists then table.insert(profiles, k) end
             end
        end

        local current = SW.Defaults:GetCurrentBindingProfile()
        for _, p in ipairs(profiles) do
            local info = UIDropDownMenu_CreateInfo()
            info.text = p
            info.checked = (current == p)
            info.func = function() 
                SW.Bindings:LoadProfile(p) 
                SW.UI:UpdatePanel()
                CloseDropDownMenus()
            end
            UIDropDownMenu_AddButton(info)
        end
    end)
end

function SW.UI:TogglePanel()
    if not self.panel then self:InitPanel() end
    if self.panel:IsShown() then 
        self.panel:Hide() 
    else 
        self.panel:Show() 
        self:UpdatePanel() -- Update when showing to ensure fresh data
    end
end

function SW.UI:UpdatePanel()
    if not self.panel then return end
    
    -- Refresh Dropdown Text
    UIDropDownMenu_SetText(self.modeDrop, SW.State:GetMode())
    UIDropDownMenu_SetText(self.inputDrop, SW.Defaults:GetCurrentBindingProfile())
    
    -- Refresh Toggles
    if SkillWeaverDB and SkillWeaverDB.toggles then
        for k, cb in pairs(self.checks) do
            cb:SetChecked(SkillWeaverDB.toggles[k] or false)
        end
    end
end
