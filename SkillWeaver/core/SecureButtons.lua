-- core/SecureButtons.lua
-- Creates the invisible buttons that the Hardware/Keybinds actually "Click"

local SW = SkillWeaver
SW.SecureButtons = { buttons = {} }

-- Helper: Create a SecureActionButton that runs a macro
local function createSecureButton(id)
    local name = "SkillWeaver_" .. id
    local b = CreateFrame("Button", name, UIParent, "SecureActionButtonTemplate")
    
    -- Default behavior (Safety)
    b:SetAttribute("type", "macro")
    b:SetAttribute("macrotext", "/startattack")
    
    -- Allow clicks from Bindings.xml
    b:RegisterForClicks("AnyUp", "AnyDown")
    b:Hide() 
    
    return b
end

function SW.SecureButtons:Init()
    -- 1. Create the buttons mapped in Bindings.xml
    self.buttons.ST   = createSecureButton("ST")
    self.buttons.AOE  = createSecureButton("AOE")
    self.buttons.HEAL = createSecureButton("HEAL")
    self.buttons.SELF = createSecureButton("SELF")
    self.buttons.INT  = createSecureButton("INT")
    self.buttons.UTIL = createSecureButton("UTIL")
end

-- Called by Engine.lua to update spells
function SW.SecureButtons:SetMacro(id, macroText)
    if InCombatLockdown() then return false end -- Cannot change in combat
    
    local b = self.buttons[id]
    if not b then return false end
    
    b:SetAttribute("macrotext", macroText or "")
    return true
end

-- Called by Engine.lua to show/hide buttons (optional visual feedback)
function SW.SecureButtons:SetVisible(id, visible)
    local b = self.buttons[id]
    if not b then return end
    -- Note: Secure buttons usually stay hidden, but if you have a UI logic:
    if visible then b:Show() else b:Hide() end
end
