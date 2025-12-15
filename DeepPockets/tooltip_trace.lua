-- tooltip_trace.lua - lightweight tooltip trace toggle
local enabled = false

local function HookTooltip(tt)
  if tt.__dp_hooked then return end
  tt.__dp_hooked = true
  tt:HookScript("OnShow", function(self)
    if enabled then
      local owner = self:GetOwner()
      local on = owner and owner:GetName() or "nil-owner"
      print("DP TT: show", self:GetName() or "GameTooltip", "owner=", on)
    end
  end)
end

_G.DeepPockets_ToggleTooltipTrace = function()
  enabled = not enabled
  HookTooltip(GameTooltip)
  HookTooltip(ItemRefTooltip)
  print("DeepPockets tooltip trace:", enabled and "ON" or "OFF")
end
