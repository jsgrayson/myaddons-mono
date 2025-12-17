-- core/InternalDispatcher.lua
-- This frame receives "signals" from the secure buttons
local Dispatcher = CreateFrame(
  "Button",
  "SkillWeaver_Internal",
  UIParent,
  "SecureActionButtonTemplate"
)

Dispatcher:RegisterForClicks("AnyUp")

Dispatcher:SetScript("OnClick", function(_, intent)
  -- 'intent' is passed as the argument to /click
  -- E.g. "/click SkillWeaver_Internal PRIMARY" -> intent="PRIMARY"
  if addonTable and addonTable.SkillWeaver then
      addonTable.SkillWeaver:OnIntent(intent)
  end
end)

return Dispatcher
