-- SkillWeaver Keybinds
-- Registers keybinds that controller players can map to controller buttons

local AddonName, SkillWeaver = ...

-- Register keybind category
BINDING_HEADER_SKILLWEAVER = "SkillWeaver"

-- Register individual keybinds (these show up in WoW Keybindings menu)
BINDING_NAME_SKILLWEAVER_TOGGLE_CONSUMABLES = "Toggle Paid Consumables"
BINDING_NAME_SKILLWEAVER_TOGGLE_INTERRUPTS = "Toggle Auto-Interrupt"
BINDING_NAME_SKILLWEAVER_TOGGLE_HEALING = "Toggle Ally Healing"
BINDING_NAME_SKILLWEAVER_TOGGLE_PET = "Toggle Pet Management"
BINDING_NAME_SKILLWEAVER_SHOW_STATUS = "Show Toggle Status"
BINDING_NAME_SKILLWEAVER_OPEN_MENU = "Open Settings Menu"

-- Keybind functions (called when controller button pressed)
function SkillWeaver_ToggleConsumables()
    if SkillWeaver and SkillWeaver.MinimapButton then
        SkillWeaver.MinimapButton:ToggleConsumables()
    end
end

function SkillWeaver_ToggleInterrupts()
    if SkillWeaver and SkillWeaver.MinimapButton then
        SkillWeaver.MinimapButton:ToggleInterrupts()
    end
end

function SkillWeaver_ToggleHealing()
    if SkillWeaver and SkillWeaver.MinimapButton then
        SkillWeaver.MinimapButton:ToggleAllyHealing()
    end
end

function SkillWeaver_TogglePet()
    if SkillWeaver and SkillWeaver.MinimapButton then
        SkillWeaver.MinimapButton:TogglePetManagement()
    end
end

function SkillWeaver_ShowStatus()
    if SkillWeaver and SkillWeaver.MinimapButton then
        SkillWeaver.MinimapButton:ShowStatus()
    end
end

function SkillWeaver_OpenMenu()
    if SkillWeaver and SkillWeaver.MinimapButton then
        SkillWeaver.MinimapButton:ShowDropdownMenu()
    end
end
