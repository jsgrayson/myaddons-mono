local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local BurstWindow = {}
SkillWeaver.BurstWindow = BurstWindow

-- Example: define a burst window as "major buff active" OR "major cooldown ready and we want to burst"
-- Input: context (runtime state)
function BurstWindow:IsActive(context)
  
  -- 1. Explicit user override (e.g. keybind toggled burst mode)
  if context.forceBurst == true then return true end
  
  -- 2. Major Buffs Active (engine tracks)
  -- e.g. if we are in Pillar of Frost or Combustion, we are IN a window.
  if context.burstBuffActive == true then return true end
  
  -- 3. Engine logic says "Ready to Burn" (e.g. aligned CDs)
  -- (Future feature)
  
  return false
end

return BurstWindow
