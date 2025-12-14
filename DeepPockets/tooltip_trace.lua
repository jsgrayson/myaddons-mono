DeepPockets = DeepPockets or {}
local DP = DeepPockets

DP.TooltipTrace = DP.TooltipTrace or {
  enabled = false,
  hooked = false,
}

local function safeName(obj)
  if type(obj) == "table" or type(obj) == "userdata" then
    if obj.GetName then
      local ok, n = pcall(obj.GetName, obj)
      if ok and n then return n end
    end
  end
  return tostring(obj)
end

local function printTT(...)
  DEFAULT_CHAT_FRAME:AddMessage("|cff55aaffDP|r " .. string.format(...))
end

function DP.TooltipTrace:HookOnce()
  if self.hooked then return end
  self.hooked = true

  -- Track last owner + last SetOwner caller.
  hooksecurefunc(GameTooltip, "SetOwner", function(tt, owner, ...)
    if not DP.TooltipTrace.enabled then return end
    DP.TooltipTrace.lastOwner = owner
    DP.TooltipTrace.lastOwnerName = safeName(owner)
    DP.TooltipTrace.lastSetOwnerAt = debugstack(2, 1, 0)
    printTT("GameTooltip:SetOwner owner=%s", DP.TooltipTrace.lastOwnerName or "nil")
  end)

  hooksecurefunc(GameTooltip, "Hide", function(tt)
    if not DP.TooltipTrace.enabled then return end
    local owner = tt:GetOwner()
    local ownerName = safeName(owner)
    printTT("GameTooltip:Hide ownerNow=%s lastOwner=%s", ownerName or "nil", DP.TooltipTrace.lastOwnerName or "nil")
  end)

  -- Some addons call SetHyperlink/SetItem and then tooltip vanishes; log those too.
  hooksecurefunc(GameTooltip, "SetHyperlink", function(tt, link)
    if not DP.TooltipTrace.enabled then return end
    printTT("GameTooltip:SetHyperlink %s", tostring(link))
  end)

  hooksecurefunc(GameTooltip, "SetBagItem", function(tt, bag, slot)
    if not DP.TooltipTrace.enabled then return end
    printTT("GameTooltip:SetBagItem bag=%s slot=%s", tostring(bag), tostring(slot))
  end)
end

function DP.TooltipTrace:Toggle()
  self.enabled = not self.enabled
  self:HookOnce()
  printTT("TooltipTrace %s", self.enabled and "ON" or "OFF")
  if self.enabled then
    printTT("Tip: reproduce tooltip disappearance now; you'll get logs on SetOwner/Hide.")
  end
end
