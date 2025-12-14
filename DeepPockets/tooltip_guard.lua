-- Purpose:
-- Prevent tooltip disappearance (ConsolePort-style nil owners / bad clears)
-- Safe, no hooks into BetterBags internals.

local function SafeSetOwner(tooltip, owner, anchor)
    if not tooltip or not tooltip.SetOwner then return end
    if not owner then return end
    tooltip:SetOwner(owner, anchor or "ANCHOR_RIGHT")
end

local function GuardTooltip(tooltip)
    if not tooltip then return end

    hooksecurefunc(tooltip, "Hide", function(self)
        if self:IsForbidden() then return end
        if self._dp_guarding then return end
        self._dp_guarding = true
        C_Timer.After(0, function()
            self._dp_guarding = nil
        end)
    end)
end

-- Apply guard to common tooltips
C_Timer.After(0, function()
    GuardTooltip(GameTooltip)
    GuardTooltip(ItemRefTooltip)
end)
