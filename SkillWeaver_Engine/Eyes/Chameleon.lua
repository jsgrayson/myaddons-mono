-- Chameleon.lua: PvP Data Extension
local function UpdatePvPData()
    local isCasting, _, _, _, endTime = UnitCastingInfo("target")
    local precogActive = AuraUtil.FindAuraByName("Precognition", "player")

    -- Pixel 6: Precognition & Baiting State
    if precogActive then
        Chameleon:SetPixelColor(6, 0, 255, 0) -- Pure Green for Brain
    elseif isCasting then
        Chameleon:SetPixelColor(6, 255, 165, 0) -- Orange: Target is casting
    else
        Chameleon:SetPixelColor(6, 0, 0, 0)
    end
end
