-- SkillWeaver Minimap Button
-- Handles consumables toggle and other settings

local AddonName, SkillWeaver = ...

-- Create minimap button using LibDBIcon (LibDataBroker)
SkillWeaver.MinimapButton = {}
local MinimapButton = SkillWeaver.MinimapButton

-- Default settings are now handled by SettingsManager.lua
-- SkillWeaver.Settings is a reference to SettingsManager.Char

-- Create LibDataBroker object
local LDB = LibStub("LibDataBroker-1.1"):NewDataObject("SkillWeaver", {
    type = "data source",
    text = "SkillWeaver",
    icon = "Interface\\Icons\\spell_nature_elementalshields", -- Placeholder icon
    OnClick = function(self, button)
        if button == "LeftButton" then
            MinimapButton:ToggleConsumables()
        elseif button == "RightButton" then
            MinimapButton:ShowDropdownMenu()
        end
    end,
    OnTooltipShow = function(tooltip)
        if not tooltip or not tooltip.AddLine then return end
        tooltip:SetText("SkillWeaver")
        tooltip:AddLine(" ")
        tooltip:AddLine("|cffFFFFFFLeft-Click:|r Toggle Consumables", 1, 1, 1)
        tooltip:AddLine("|cffFFFFFFRight-Click:|r Open Settings", 1, 1, 1)
        tooltip:AddLine(" ")
        
        -- Always On Features
        tooltip:AddLine("Always Active (FREE):", 0.5, 1, 0.5)
        tooltip:AddLine("  ✓ Healthstones", 0, 1, 0)
        tooltip:AddLine("  ✓ Interrupts", 0, 1, 0)
        tooltip:AddLine("  ✓ Defensives", 0, 1, 0)
        tooltip:AddLine(" ")
        
        -- Show current consumables status
        local status = SkillWeaver.Settings.consumables.enabled and "|cff00FF00ON|r" or "|cffFF0000OFF|r"
        tooltip:AddLine("Paid Consumables: " .. status, 1, 1, 1)
        
        if SkillWeaver.Settings.consumables.enabled then
            tooltip:AddLine("  - Healing Potions", 1, 1, 1)
            tooltip:AddLine("  - Flasks", 1, 1, 1)
            tooltip:AddLine("  - Food Buffs", 1, 1, 1)
            tooltip:AddLine("  - Augment Runes", 1, 1, 1)
        end
    end,
})

-- Initialize minimap button
function MinimapButton:Initialize()
    -- Create icon using LibDBIcon
    local icon = LibStub("LibDBIcon-1.0")
    icon:Register("SkillWeaver", LDB, SkillWeaver.Settings.minimap)
    
    print("|cff00FF00SkillWeaver|r: Minimap button initialized. Left-click to toggle consumables.")
end

-- Toggle consumables on/off
function MinimapButton:ToggleConsumables()
    SkillWeaver.Settings.consumables.enabled = not SkillWeaver.Settings.consumables.enabled
    
    local status = SkillWeaver.Settings.consumables.enabled and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Consumables " .. status)
    
    -- Play sound feedback
    if SkillWeaver.Settings.consumables.enabled then
        PlaySound(SOUNDKIT.ACHIEVEMENT_MENU_OPEN)
    else
        PlaySound(SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
    end
    
    -- Update tooltip
    if GameTooltip:IsShown() and GameTooltip:GetOwner() == MinimapButton then
        LDB.OnTooltipShow(GameTooltip)
    end
end

-- Open settings panel (placeholder for now)
function MinimapButton:OpenSettings()
    if SkillWeaver.SettingsPanel then
        SkillWeaver.SettingsPanel:Show()
    else
        print("|cff00FF00SkillWeaver|r: Settings panel coming soon! Use /skillweaver for commands.")
    end
end

-- Show dropdown menu (controller-friendly)
function MinimapButton:ShowDropdownMenu()
    local menu = {
        -- Title
        { text = "SkillWeaver Controls", isTitle = true, notCheckable = true },
        
        -- Quick Toggles Section
        { text = "Quick Toggles", isTitle = true, notCheckable = true },
        { 
            text = "Paid Consumables", 
            checked = function() return SkillWeaver.Settings.consumables.enabled end,
            func = function() self:ToggleConsumables() end,
            tooltipTitle = "Paid Consumables",
            tooltipText = "Flasks, Potions, Food, Augment Runes (costs gold!)",
            keepShownOnClick = true,
        },
        { 
            text = "Auto-Interrupt", 
            checked = function() return SkillWeaver.Settings.utilities.autoInterrupt end,
            func = function() self:ToggleInterrupts() end,
            tooltipTitle = "Auto-Interrupt",
            tooltipText = "Automatically interrupt enemy casts",
            keepShownOnClick = true,
        },
        { 
            text = "Emergency Ally Healing", 
            checked = function() return SkillWeaver.Settings.utilities.emergencyAllyHealing end,
            func = function() self:ToggleAllyHealing() end,
            tooltipTitle = "Ally Healing",
            tooltipText = "Emergency healing when allies < 15% health",
            keepShownOnClick = true,
        },
        { 
            text = "Pet Auto-Management", 
            checked = function() return SkillWeaver.Settings.utilities.petAutoManagement end,
            func = function() self:TogglePetManagement() end,
            tooltipTitle = "Pet Management",
            tooltipText = "Auto Growl toggle, Misdirection logic, pet summon",
            keepShownOnClick = true,
        },
        { 
            text = "Auto Battle Res", 
            checked = function() return SkillWeaver.Settings.utilities.autoBattleRes end,
            func = function() self:ToggleBattleRes() end,
            tooltipTitle = "Auto Battle Res",
            tooltipText = "Automatically resurrect dead tanks/healers in combat",
            keepShownOnClick = true,
        },
        
        -- Advanced Modules Submenu
        { 
            text = "Advanced Modules", 
            hasArrow = true,
            notCheckable = true,
            menuList = {
                { text = "Automation Modules", isTitle = true, notCheckable = true },
                { 
                    text = "Auto Trinkets", 
                    checked = function() return SkillWeaver.Settings.utilities.autoTrinkets end,
                    func = function() self:ToggleTrinkets() end,
                    tooltipText = "Automatically use DPS trinkets with cooldowns",
                    keepShownOnClick = true,
                },
                { 
                    text = "Auto Racials", 
                    checked = function() return SkillWeaver.Settings.utilities.autoRacials end,
                    func = function() self:ToggleRacials() end,
                    tooltipText = "Automatically use Racial abilities",
                    keepShownOnClick = true,
                },
                { 
                    text = "Auto Loss Control", 
                    checked = function() return SkillWeaver.Settings.utilities.autoLossControl end,
                    func = function() self:ToggleLossControl() end,
                    tooltipText = "Automatically use CC breakers (Trinket/Racial/Class)",
                    keepShownOnClick = true,
                },
                { 
                    text = "Auto Buffs", 
                    checked = function() return SkillWeaver.Settings.utilities.autoBuffs end,
                    func = function() self:ToggleBuffs() end,
                    tooltipText = "Automatically cast group buffs out of combat",
                    keepShownOnClick = true,
                },
                { text = "", isTitle = true, notCheckable = true },
                { text = "Stock Management", isTitle = true, notCheckable = true },
                { 
                    text = "Low Stock Warnings", 
                    checked = function() return SkillWeaver.Settings.consumables.lowStockWarning end,
                    func = function() self:ToggleStockWarnings() end,
                    tooltipText = "Warn when consumables are low",
                    keepShownOnClick = true,
                },
            },
        },

        -- Separator
        { text = "", isTitle = true, notCheckable = true },
        
        -- Options Submenu
        { 
            text = "Options", 
            hasArrow = true,
            notCheckable = true,
            menuList = {
                { text = "Consumable Options", isTitle = true, notCheckable = true },
                { 
                    text = "Potion Threshold: " .. SkillWeaver.Settings.consumables.potionHealthThreshold .. "%",
                    notCheckable = true,
                    func = function() self:ShowThresholdSlider("potion") end,
                    tooltipText = "Health % to use healing potions",
                },
                { 
                    text = "Healthstone Threshold: " .. SkillWeaver.Settings.consumables.healthstoneThreshold .. "%",
                    notCheckable = true,
                    func = function() self:ShowThresholdSlider("healthstone") end,
                    tooltipText = "Health % to use healthstones",
                },
                { 
                    text = "Low Stock Threshold: " .. SkillWeaver.Settings.consumables.lowStockThreshold,
                    notCheckable = true,
                    func = function() self:ShowThresholdSlider("stock") end,
                    tooltipText = "Count to trigger low stock warning",
                },
                { text = "", isTitle = true, notCheckable = true },
                { text = "Utility Options", isTitle = true, notCheckable = true },
                { 
                    text = "Ally Healing Threshold: 15%",
                    notCheckable = true,
                    func = function() print("|cff00FF00SkillWeaver|r: Coming soon!") end,
                    tooltipText = "Health % to trigger ally healing",
                },
                { text = "", isTitle = true, notCheckable = true },
                { 
                    text = "Reset to Defaults",
                    notCheckable = true,
                    func = function() self:ResetToDefaults() end,
                },
            },
        },
        
        -- Info
        { 
            text = "Show Current Status", 
            notCheckable = true,
            func = function() self:ShowStatus() end,
        },
        
        -- Separator
        { text = "", isTitle = true, notCheckable = true },
        
        -- Close
        { 
            text = "Close Menu", 
            notCheckable = true,
            func = function() CloseDropDownMenus() end,
        },
    }
    
    -- Add registered submenus
    if self.subMenus then
        for _, subMenu in ipairs(self.subMenus) do
            -- Separator before submenus
            table.insert(menu, { text = "", isTitle = true, notCheckable = true })
            
            -- Create submenu entry
            local subMenuEntry = {
                text = subMenu.title,
                hasArrow = true,
                notCheckable = true,
                menuList = {}
            }
            
            -- Populate submenu
            subMenu.populateFunc(subMenuEntry.menuList)
            
            table.insert(menu, subMenuEntry)
        end
    end

    -- Create dropdown frame if it doesn't exist
    if not SkillWeaver.DropdownFrame then
        SkillWeaver.DropdownFrame = CreateFrame("Frame", "SkillWeaverDropdownFrame", UIParent, "UIDropDownMenuTemplate")
    end
    
    EasyMenu(menu, SkillWeaver.DropdownFrame, "cursor", 0, 0, "MENU")
end

-- Register a submenu
function MinimapButton:AddSubMenu(title, populateFunc)
    self.subMenus = self.subMenus or {}
    table.insert(self.subMenus, { title = title, populateFunc = populateFunc })
end

-- Toggle interrupts
function MinimapButton:ToggleInterrupts()
    SkillWeaver.Settings.utilities.autoInterrupt = not SkillWeaver.Settings.utilities.autoInterrupt
    local status = SkillWeaver.Settings.utilities.autoInterrupt and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Auto-Interrupt " .. status)
    PlaySound(SkillWeaver.Settings.utilities.autoInterrupt and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle ally healing
function MinimapButton:ToggleAllyHealing()
    SkillWeaver.Settings.utilities.emergencyAllyHealing = not SkillWeaver.Settings.utilities.emergencyAllyHealing
    local status = SkillWeaver.Settings.utilities.emergencyAllyHealing and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Emergency Ally Healing " .. status)
    PlaySound(SkillWeaver.Settings.utilities.emergencyAllyHealing and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle pet management
function MinimapButton:TogglePetManagement()
    SkillWeaver.Settings.utilities.petAutoManagement = not SkillWeaver.Settings.utilities.petAutoManagement
    local status = SkillWeaver.Settings.utilities.petAutoManagement and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Pet Auto-Management " .. status)
    PlaySound(SkillWeaver.Settings.utilities.petAutoManagement and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle battle res
function MinimapButton:ToggleBattleRes()
    SkillWeaver.Settings.utilities.autoBattleRes = not SkillWeaver.Settings.utilities.autoBattleRes
    
    local status = SkillWeaver.Settings.utilities.autoBattleRes and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Auto Battle Res " .. status)
    PlaySound(SkillWeaver.Settings.utilities.autoBattleRes and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle Trinkets
function MinimapButton:ToggleTrinkets()
    SkillWeaver.Settings.utilities.autoTrinkets = not SkillWeaver.Settings.utilities.autoTrinkets
    local status = SkillWeaver.Settings.utilities.autoTrinkets and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Auto Trinkets " .. status)
    PlaySound(SkillWeaver.Settings.utilities.autoTrinkets and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle Racials
function MinimapButton:ToggleRacials()
    SkillWeaver.Settings.utilities.autoRacials = not SkillWeaver.Settings.utilities.autoRacials
    local status = SkillWeaver.Settings.utilities.autoRacials and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Auto Racials " .. status)
    PlaySound(SkillWeaver.Settings.utilities.autoRacials and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle Loss Control
function MinimapButton:ToggleLossControl()
    SkillWeaver.Settings.utilities.autoLossControl = not SkillWeaver.Settings.utilities.autoLossControl
    local status = SkillWeaver.Settings.utilities.autoLossControl and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Auto Loss Control " .. status)
    PlaySound(SkillWeaver.Settings.utilities.autoLossControl and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle Buffs
function MinimapButton:ToggleBuffs()
    SkillWeaver.Settings.utilities.autoBuffs = not SkillWeaver.Settings.utilities.autoBuffs
    local status = SkillWeaver.Settings.utilities.autoBuffs and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Auto Buffs " .. status)
    PlaySound(SkillWeaver.Settings.utilities.autoBuffs and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Toggle Stock Warnings
function MinimapButton:ToggleStockWarnings()
    SkillWeaver.Settings.consumables.lowStockWarning = not SkillWeaver.Settings.consumables.lowStockWarning
    local status = SkillWeaver.Settings.consumables.lowStockWarning and "|cff00FF00ENABLED|r" or "|cffFF0000DISABLED|r"
    print("|cff00FF00SkillWeaver|r: Low Stock Warnings " .. status)
    PlaySound(SkillWeaver.Settings.consumables.lowStockWarning and SOUNDKIT.ACHIEVEMENT_MENU_OPEN or SOUNDKIT.INTERFACE_SOUND_LOST_TARGET_SOUND)
end

-- Show status of all toggles
function MinimapButton:ShowStatus()
    print("|cff00FF00SkillWeaver Status:|r")
    print("  Always Active: Healthstones, Interrupts (base), Defensives")
    print("  Paid Consumables: " .. (SkillWeaver.Settings.consumables.enabled and "|cff00FF00ON|r" or "|cffFF0000OFF|r"))
    print("  Auto-Interrupt: " .. (SkillWeaver.Settings.utilities.autoInterrupt and "|cff00FF00ON|r" or "|cffFF0000OFF|r"))
    print("  Ally Healing: " .. (SkillWeaver.Settings.utilities.emergencyAllyHealing and "|cff00FF00ON|r" or "|cffFF0000OFF|r"))
    print("  Ally Healing: " .. (SkillWeaver.Settings.utilities.emergencyAllyHealing and "|cff00FF00ON|r" or "|cffFF0000OFF|r"))
    print("  Pet Management: " .. (SkillWeaver.Settings.utilities.petAutoManagement and "|cff00FF00ON|r" or "|cffFF0000OFF|r"))
    print("  Auto Battle Res: " .. (SkillWeaver.Settings.utilities.autoBattleRes and "|cff00FF00ON|r" or "|cffFF0000OFF|r"))
end

-- Show threshold slider (placeholder)
function MinimapButton:ShowThresholdSlider(type)
    local val = 0
    if type == "potion" then val = SkillWeaver.Settings.consumables.potionHealthThreshold
    elseif type == "healthstone" then val = SkillWeaver.Settings.consumables.healthstoneThreshold
    elseif type == "stock" then val = SkillWeaver.Settings.consumables.lowStockThreshold
    end
    
    print("|cff00FF00SkillWeaver|r: Threshold sliders coming soon! Current (" .. type .. "): " .. val)
end

-- Reset to defaults
function MinimapButton:ResetToDefaults()
    SkillWeaver.Settings.consumables.enabled = false
    SkillWeaver.Settings.consumables.potionHealthThreshold = 35
    SkillWeaver.Settings.consumables.healthstoneThreshold = 30
    SkillWeaver.Settings.utilities.autoInterrupt = true
    SkillWeaver.Settings.utilities.emergencyAllyHealing = true
    SkillWeaver.Settings.utilities.emergencyAllyHealing = true
    SkillWeaver.Settings.utilities.petAutoManagement = true
    SkillWeaver.Settings.utilities.autoBattleRes = true
    if SkillWeaver.BattleResManager then SkillWeaver.BattleResManager:Toggle(true) end
    print("|cff00FF00SkillWeaver|r: Settings reset to defaults!")
    PlaySound(SOUNDKIT.ACHIEVEMENT_MENU_OPEN)
end

-- Slash commands
SLASH_SKILLWEAVER1 = "/skillweaver"
SLASH_SKILLWEAVER2 = "/sw"
SlashCmdList["SKILLWEAVER"] = function(msg)
    local command = string.lower(msg)
    
    if command == "consumables" or command == "cons" then
        MinimapButton:ToggleConsumables()
    elseif command == "interrupt" or command == "int" then
        MinimapButton:ToggleInterrupts()
    elseif command == "healing" or command == "heal" then
        MinimapButton:ToggleAllyHealing()
    elseif command == "pet" then
        MinimapButton:TogglePetManagement()
    elseif command == "bres" or command == "res" then
        MinimapButton:ToggleBattleRes()
    elseif command == "status" then
        MinimapButton:ShowStatus()
    elseif command == "settings" or command == "config" then
        MinimapButton:OpenSettings()
    elseif command == "minimap" then
        local icon = LibStub("LibDBIcon-1.0")
        SkillWeaver.Settings.minimap.hide = not SkillWeaver.Settings.minimap.hide
        if SkillWeaver.Settings.minimap.hide then
            icon:Hide("SkillWeaver")
            print("|cff00FF00SkillWeaver|r: Minimap button hidden.")
        else
            icon:Show("SkillWeaver")
            print("|cff00FF00SkillWeaver|r: Minimap button shown.")
        end
    elseif command == "help" or command == "" then
        print("|cff00FF00SkillWeaver Commands:|r")
        print("  /sw consumables (cons) - Toggle paid consumables")
        print("  /sw interrupt (int) - Toggle auto-interrupt")
        print("  /sw healing (heal) - Toggle ally healing")
        print("  /sw healing (heal) - Toggle ally healing")
        print("  /sw pet - Toggle pet auto-management")
        print("  /sw bres (res) - Toggle auto battle res")
        print("  /sw status - Show all toggle status")
        print("  /sw settings - Open settings panel")
        print("  /sw minimap - Hide/show minimap button")
        print("  /sw help - Show this help")
    else
        print("|cff00FF00SkillWeaver|r: Unknown command. Type '/sw help' for commands.")
    end
end

-- Initialize on addon load
local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_LOGIN")
frame:SetScript("OnEvent", function(self, event)
    if event == "PLAYER_LOGIN" then
        MinimapButton:Initialize()
    end
end)
