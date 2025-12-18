local SW = SkillWeaver
SW.UI = SW.UI or {}

local menuFrame

function SW.UI:ToggleMenu(anchor)
    if not menuFrame then
        menuFrame = CreateFrame("Frame", "SkillWeaver_Dropdown", UIParent, "UIDropDownMenuTemplate")
    end

    -- The Menu Generator Function
    local function Initialize(self, level)
        local info = UIDropDownMenu_CreateInfo()

        -- TITLE
        info.text = "SkillWeaver"
        info.isTitle = true
        info.notCheckable = true
        UIDropDownMenu_AddButton(info, level)

        -- SECTION 1: MODE
        info = UIDropDownMenu_CreateInfo()
        info.text = "Combat Mode"
        info.isTitle = true
        info.notCheckable = true
        UIDropDownMenu_AddButton(info, level)

        local currentMode = SW.State:GetMode()
        local modes = { "Delves", "MythicPlus", "Raid", "PvP", "OpenWorld" }

        for _, m in ipairs(modes) do
            info = UIDropDownMenu_CreateInfo()
            info.text = m
            info.checked = (currentMode == m)
            info.func = function() 
                SW.State:SetMode(m) 
                -- If the panel is open, update it to reflect the change
                if SW.UI.UpdatePanel then SW.UI:UpdatePanel() end
                CloseDropDownMenus()
            end
            UIDropDownMenu_AddButton(info, level)
        end

        -- SECTION 2: INPUT PROFILE
        info = UIDropDownMenu_CreateInfo()
        info.isTitle = true
        info.notCheckable = true
        info.text = "" 
        UIDropDownMenu_AddButton(info, level) -- Spacer

        info = UIDropDownMenu_CreateInfo()
        info.text = "Input Profile"
        info.isTitle = true
        info.notCheckable = true
        UIDropDownMenu_AddButton(info, level)

        local profiles = { "Keyboard", "Controller", "MMO_Mouse" }
        if SkillWeaverDB and SkillWeaverDB.bindingProfiles then
            for k, _ in pairs(SkillWeaverDB.bindingProfiles) do
                local found = false
                for _, p in ipairs(profiles) do if p == k then found = true end end
                if not found then table.insert(profiles, k) end
            end
        end

        local currentInput = SW.Defaults and SW.Defaults.GetCurrentBindingProfile and SW.Defaults:GetCurrentBindingProfile() or "None"

        for _, p in ipairs(profiles) do
            info = UIDropDownMenu_CreateInfo()
            info.text = p
            info.checked = (currentInput == p)
            info.func = function() 
                if SW.Bindings and SW.Bindings.LoadProfile then
                    SW.Bindings:LoadProfile(p) 
                end
                if SW.UI.UpdatePanel then SW.UI:UpdatePanel() end
                CloseDropDownMenus()
            end
            UIDropDownMenu_AddButton(info, level)
        end

        -- Save Current Option
        info = UIDropDownMenu_CreateInfo()
        info.text = "|cFF00FF00+ Save Current as...|r"
        info.notCheckable = true
        info.func = function() 
            StaticPopup_Show("SW_SAVE_PROFILE") 
        end
        UIDropDownMenu_AddButton(info, level)

        -- SECTION 3: TOGGLES
        info = UIDropDownMenu_CreateInfo()
        info.isTitle = true
        info.notCheckable = true
        info.text = "" 
        UIDropDownMenu_AddButton(info, level) -- Spacer

        info = UIDropDownMenu_CreateInfo()
        info.text = "Live Toggles"
        info.isTitle = true
        info.notCheckable = true
        UIDropDownMenu_AddButton(info, level)

        local toggles = {
            { k="burst", text="Burst Mode" },
            { k="defensives", text="Auto Defensives" },
            { k="interrupts", text="Auto Interrupts" },
            { k="showHealButton", text="Healer Helper" },
        }

        for _, t in ipairs(toggles) do
            info = UIDropDownMenu_CreateInfo()
            info.text = t.text
            info.checked = SkillWeaverDB and SkillWeaverDB.toggles and SkillWeaverDB.toggles[t.k]
            info.isNotRadio = true
            info.keepShownOnClick = true
            info.func = function()
                if SkillWeaverDB and SkillWeaverDB.toggles then
                    SkillWeaverDB.toggles[t.k] = not SkillWeaverDB.toggles[t.k]
                end
                if SW.Engine and SW.Engine.RefreshAll then
                    SW.Engine:RefreshAll("toggle_" .. t.k)
                end
                if SW.UI.UpdatePanel then SW.UI:UpdatePanel() end
            end
            UIDropDownMenu_AddButton(info, level)
        end

        -- RELOAD UI
        info = UIDropDownMenu_CreateInfo()
        info.isTitle = true
        info.notCheckable = true
        info.text = "" 
        UIDropDownMenu_AddButton(info, level) -- Spacer

        info = UIDropDownMenu_CreateInfo()
        info.text = "|cFFFF0000Reload UI|r"
        info.notCheckable = true
        info.func = ReloadUI
        UIDropDownMenu_AddButton(info, level)
    end

    -- Initialize and Toggle
    UIDropDownMenu_Initialize(menuFrame, Initialize, "MENU")
    ToggleDropDownMenu(1, nil, menuFrame, anchor, 0, 0)
end

-- Keep the StaticPopup as is
StaticPopupDialogs["SW_SAVE_PROFILE"] = {
    text = "Name your Input Profile:",
    button1 = "Save",
    button2 = "Cancel",
    hasEditBox = true,
    OnAccept = function(self)
        local text = self.editBox:GetText()
        if SW.Bindings and SW.Bindings.SaveProfile then
            SW.Bindings:SaveProfile(text)
        end
    end,
    timeout = 0,
    whileDead = true,
    hideOnEscape = true,
    preferredIndex = 3,
}
