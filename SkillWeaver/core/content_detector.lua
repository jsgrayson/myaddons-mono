-- SkillWeaver Content Detection
local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local CD = {}

function CD:GetContentType()
    if C_PvP.IsActiveBattlefield and C_PvP.IsActiveBattlefield() then
        return "PVP"
    end

    local inInstance, instanceType = IsInInstance()
    if not inInstance then
        return "OPEN_WORLD"
    end

    if instanceType == "raid" then
        return "RAID"
    elseif instanceType == "party" then
        if C_ChallengeMode and C_ChallengeMode.IsChallengeModeActive and C_ChallengeMode.IsChallengeModeActive() then
            return "MYTHIC_PLUS"
        end
        return "DUNGEON"
    elseif instanceType == "scenario" then
        return "DELVES" -- MVP Assumption: Delves are scenarios in TWW
    end

    return "UNKNOWN"
end

function CD:Evaluate()
    local content = self:GetContentType()
    if SkillWeaver.HandleContentChange then
        SkillWeaver:HandleContentChange(content)
    end
end

SkillWeaver.ContentDetector = CD
