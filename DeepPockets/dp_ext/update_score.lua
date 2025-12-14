-- DeepPockets Upgrade Score Backend
-- Safe, backend-only module
-- No UI, no hooks, no events, no slash commands

local ADDON, DP = ...
DP = DP or {}
DP.UpgradeScore = {}

local UpgradeScore = DP.UpgradeScore

-- Internal cache
local scoreCache = {}
local lastScan = 0

-- Optional dependency
local SkillWeaver = _G.SkillWeaver

-- Public: check availability
function UpgradeScore:IsAvailable()
    return SkillWeaver and SkillWeaver.GetItemScore
end

-- Public: get cached score
function UpgradeScore:GetScore(itemID)
    return scoreCache[itemID]
end

-- Internal: calculate score safely
local function CalculateScore(itemID)
    if not UpgradeScore:IsAvailable() then
        return nil
    end

    local ok, score = pcall(SkillWeaver.GetItemScore, SkillWeaver, itemID)
    if not ok then
        return nil
    end

    return score
end

-- Public: scan bags and refresh cache
function UpgradeScore:ScanBags()
    wipe(scoreCache)

    for bag = 0, NUM_BAG_SLOTS do
        local slots = C_Container.GetContainerNumSlots(bag)
        for slot = 1, slots do
            local itemID = C_Container.GetContainerItemID(bag, slot)
            if itemID and not scoreCache[itemID] then
                scoreCache[itemID] = CalculateScore(itemID)
            end
        end
    end

    lastScan = time()
end

-- Public: dump for debugging / external use
function UpgradeScore:Dump()
    return scoreCache
end

-- Optional auto-scan on PLAYER_LOGIN (safe, silent)
local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:SetScript("OnEvent", function()
    UpgradeScore:ScanBags()
end)
