-- Tooltip recovery guard (ConsolePort-style disappearance fix)

local guard = CreateFrame("Frame")

local function EnsureOwner(tt)
    if not tt then return end
    if tt:IsShown() and not tt:GetOwner() then
        tt:SetOwner(UIParent, "ANCHOR_CURSOR")
    end
end

guard:RegisterEvent("UPDATE_MOUSEOVER_UNIT")
guard:RegisterEvent("MODIFIER_STATE_CHANGED")
guard:RegisterEvent("CURSOR_UPDATE")

guard:SetScript("OnEvent", function()
    EnsureOwner(GameTooltip)
    EnsureOwner(ItemRefTooltip)
end)

-- Recover tooltip if something clears it incorrectly
hooksecurefunc("GameTooltip_Clear", function()
    C_Timer.After(0, function()
        if GameTooltip and not GameTooltip:IsShown() then
            GameTooltip:SetOwner(UIParent, "ANCHOR_CURSOR")
        end
    end)
end)
