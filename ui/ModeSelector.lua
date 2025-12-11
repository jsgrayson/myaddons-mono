--========================================================--
-- SkillWeaver - Mode Selector UI
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local UI = {}
SkillWeaver.UI = SkillWeaver.UI or {}
SkillWeaver.UI.ModeSelector = UI

local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end

------------------------------------------------------------
-- Create Main Panel
------------------------------------------------------------

function UI:Create()
    if self.frame then return end

    local f = CreateFrame("Frame", "SkillWeaverModeSelector", UIParent, "BackdropTemplate")
    self.frame = f
    f:SetSize(320, 250)
    f:SetPoint("CENTER")
    f:SetMovable(true)
    f:EnableMouse(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)

    -- Stylish background
    f:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background-Dark",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        edgeSize = 16, insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    f:SetBackdropColor(0, 0, 0, 0.75)

    -- Header
    local title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOP", 0, -10)
    title:SetText("|cff4af2f8SkillWeaver Mode Selector|r")

    --------------------------------------------------------
    -- Mode Dropdown
    --------------------------------------------------------

    local modeLabel = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    modeLabel:SetPoint("TOPLEFT", 20, -50)
    modeLabel:SetText("Content Mode")

    local modeDrop = CreateFrame("Frame", "SW_ModeDropdown", f, "UIDropDownMenuTemplate")
    modeDrop:SetPoint("TOPLEFT", modeLabel, "BOTTOMLEFT", -16, -4)

    local modes = {
        { text = "Mythic+", value = "MythicPlus" },
        { text = "Raid",    value = "Raid" },
        { text = "Delves",  value = "Delves" },
        { text = "PvP",     value = "PvP" },
    }

    UIDropDownMenu_SetWidth(modeDrop, 160)
    UIDropDownMenu_SetText(modeDrop, "Select Mode")

    UIDropDownMenu_Initialize(modeDrop, function(self, level)
        for _, entry in ipairs(modes) do
            local info = UIDropDownMenu_CreateInfo()
            info.text = entry.text
            info.value = entry.value
            info.func = function()
                UIDropDownMenu_SetSelectedValue(modeDrop, entry.value)
                UIDropDownMenu_SetText(modeDrop, entry.text)
                UI.lastMode = entry.value
            end
            UIDropDownMenu_AddButton(info)
        end
    end)

    --------------------------------------------------------
    -- Variant Dropdown
    --------------------------------------------------------

    local varLabel = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    varLabel:SetPoint("TOPLEFT", modeDrop, "BOTTOMLEFT", 20, -20)
    varLabel:SetText("Rotation Style")

    local varDrop = CreateFrame("Frame", "SW_VariantDropdown", f, "UIDropDownMenuTemplate")
    varDrop:SetPoint("TOPLEFT", varLabel, "BOTTOMLEFT", -16, -4)

    local variants = {
        { text = "Balanced",       value = "Balanced" },
        { text = "High Performance", value = "HighPerformance" },
        { text = "Safe Mode",      value = "Safe" },
    }

    UIDropDownMenu_SetWidth(varDrop, 160)
    UIDropDownMenu_SetText(varDrop, "Select Style")

    UIDropDownMenu_Initialize(varDrop, function(self, level)
        for _, entry in ipairs(variants) do
            -- Hide HP if in Safe Mode
            if SAFE() and entry.value == "HighPerformance" then
                -- Skip HP in Safe Mode
            else
                local info = UIDropDownMenu_CreateInfo()
                info.text = entry.text
                info.value = entry.value
                info.func = function()
                    UIDropDownMenu_SetSelectedValue(varDrop, entry.value)
                    UIDropDownMenu_SetText(varDrop, entry.text)
                    UI.lastVariant = entry.value
                end
                UIDropDownMenu_AddButton(info)
            end
        end
    end)

    --------------------------------------------------------
    -- Create Macro Buttons
    --------------------------------------------------------

    local btnST = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    btnST:SetSize(120, 28)
    btnST:SetPoint("BOTTOMLEFT", 20, 20)
    btnST:SetText("Create ST Macro")

    btnST:SetScript("OnClick", function()
        if not UI.lastMode or not UI.lastVariant then
            print("|cffFF6666Select both mode and variant first!|r")
            return
        end
        
        -- Get the sequence data
        local specID = SkillWeaver.currentSpec
        local class = select(2, UnitClass("player"))
        -- In a real scenario, we'd fetch the actual sequence table here
        -- For now, we trigger the update on the core
        -- We need to find the sequence object first.
        
        -- Hack: Trigger a reload of the button with the selected mode
        -- In a real app, we would pass the specific sequence object.
        -- SkillWeaver:LoadSequence(specID, UI.lastMode, UI.lastVariant)
        
        print("|cff4af2f8SkillWeaver|r: Creating ST Macro...")
        -- Create the macro in WoW (requires interaction)
        -- We use a safe wrapper or just print instructions if blocked
        if not InCombatLockdown() then
            -- Delete existing if present to update
            local idx = GetMacroIndexByName("SW_ST")
            if idx > 0 then DeleteMacro(idx) end
            
            CreateMacro("SW_ST", "INV_Misc_QuestionMark", "/click SkillWeaverButton_ST", 1)
            print("|cff00ff00Macro 'SW_ST' created! Drag to bar.|r")
        else
            print("|cffFF0000Cannot create macros in combat.|r")
        end
    end)

    local btnAoE = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    btnAoE:SetSize(120, 28)
    btnAoE:SetPoint("BOTTOMRIGHT", -20, 20)
    btnAoE:SetText("Create AoE Macro")

    btnAoE:SetScript("OnClick", function()
        if not UI.lastMode or not UI.lastVariant then
            print("|cffFF6666Select both mode and variant first!|r")
            return
        end

        print("|cff4af2f8SkillWeaver|r: Creating AoE Macro...")
        if not InCombatLockdown() then
            local idx = GetMacroIndexByName("SW_AoE")
            if idx > 0 then DeleteMacro(idx) end
            
            CreateMacro("SW_AoE", "Spell_Fire_MeteorStorm", "/click SkillWeaverButton_AoE", 1)
            print("|cff00ff00Macro 'SW_AoE' created! Drag to bar.|r")
        else
            print("|cffFF0000Cannot create macros in combat.|r")
        end
    end)

    -- Apply Button (Loads the sequence into the Secure Buttons)
    local apply = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    apply:SetSize(100, 28)
    apply:SetPoint("BOTTOM", 0, 55)
    apply:SetText("Load Sequence")

    apply:SetScript("OnClick", function()
        if not UI.lastMode or not UI.lastVariant then
            print("|cffFF6666Select both mode and variant first!|r")
            return
        end

        -- Fetch sequence
        local spec = SkillWeaver.currentSpec
        local class = select(2, UnitClass("player"))
        local key = class .. "_" .. spec
        
        local seqData = SkillWeaver.Sequences[key]
        if seqData and seqData[UI.lastMode] then
            local seq = seqData[UI.lastMode][UI.lastVariant]
            if seq then
                SkillWeaver:UpdateSecureButton(seq)
                print("|cff4af2f8SkillWeaver|r: Loaded " .. UI.lastMode .. " (" .. UI.lastVariant .. ")")
            else
                print("Sequence variant not found.")
            end
        else
            print("No sequences found for this spec/mode.")
        end
    end)

    --------------------------------------------------------
    -- Close Button
    --------------------------------------------------------

    local close = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    close:SetSize(60, 22)
    close:SetPoint("TOPRIGHT", -10, -10)
    close:SetText("X")

    close:SetScript("OnClick", function()
        f:Hide()
    end)

    --------------------------------------------------------
    -- Store Frame
    --------------------------------------------------------
    SkillWeaver.UI.ModeSelector.frame = f
end

------------------------------------------------------------
-- Toggle Function
------------------------------------------------------------

function UI:Toggle()
    if not self.frame then self:Create() end

    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
    end
end

------------------------------------------------------------
-- Slash Command Hook
------------------------------------------------------------

SlashCmdList["SKILLWEAVER"] = function(msg)
    msg = msg:lower() or ""
    if msg == "" then
        SkillWeaver.UI.ModeSelector:Toggle()
    elseif msg == "mode" then
        SkillWeaver:AnnounceMode()
    elseif msg == "reload" then
        SkillWeaver:ReloadEngine()
    else
        SkillWeaver.UI.ModeSelector:Toggle()
    end
end
