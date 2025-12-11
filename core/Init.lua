---------------------------------------------------------
-- SkillWeaver Addon Entrypoint
---------------------------------------------------------

local SkillWeaver = require("skillweaver.core.SkillWeaver")

---------------------------------------------------------
-- EVENT FRAME
---------------------------------------------------------
local frame = CreateFrame("Frame")

frame:RegisterEvent("PLAYER_LOGIN")
frame:RegisterEvent("PLAYER_SPECIALIZATION_CHANGED")

---------------------------------------------------------
-- EVENT HANDLER
---------------------------------------------------------
frame:SetScript("OnEvent", function(self, event, ...)
    if event == "PLAYER_LOGIN" then
        print("|cff00ff00SkillWeaver Loaded.|r")

        local currentSpecID = select(1, GetSpecializationInfo(GetSpecialization()))
        SkillWeaver:OnSpecChanged(currentSpecID)

    elseif event == "PLAYER_SPECIALIZATION_CHANGED" then
        local unit = ...
        if unit == "player" then
            local newSpecID = select(1, GetSpecializationInfo(GetSpecialization()))
            SkillWeaver:OnSpecChanged(newSpecID)
        end
    end
end)
