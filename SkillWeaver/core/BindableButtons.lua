-- core/BindableButtons.lua
local Buttons = {}

local function createButton(name)
  local btn = CreateFrame(
    "Button",
    name,
    UIParent,
    "SecureActionButtonTemplate"
  )
  btn:SetAttribute("type", "macro")
  btn:RegisterForClicks("AnyUp")
  btn:Hide()
  return btn
end

-- Create the 4 bindable buttons
Buttons.Primary   = createButton("SkillWeaver_Primary")
Buttons.GroupHeal = createButton("SkillWeaver_GroupHeal")
Buttons.TankSave  = createButton("SkillWeaver_TankSave")
Buttons.SelfSave  = createButton("SkillWeaver_SelfSave")

-- Set Attributes (Composite: Action + Dispatch Event)
-- This ensures the cast happens securely (macro) AND the engine gets the signal (click)

-- Primary: Driven by engine updates (dynamic), but defaults to simple dispatcher for now
Buttons.Primary:SetAttribute("macrotext", "/click SkillWeaver_Internal PRIMARY")

-- Group: Static AoE macro placeholder (dynamically updated by policies usually)
Buttons.GroupHeal:SetAttribute("macrotext", "/click SkillWeaver_Internal GROUP")

-- Tank Save: Static ToT logic
Buttons.TankSave:SetAttribute("macrotext", "/cast [@targettarget,help,nodead] Blessing of Sacrifice\n/click SkillWeaver_Internal TANK")

-- Self Save: Static Self logic
Buttons.SelfSave:SetAttribute("macrotext", "/cast [@player] Divine Shield\n/click SkillWeaver_Internal SELF")

return Buttons
