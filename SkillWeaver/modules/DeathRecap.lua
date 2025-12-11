-- DeathRecap.lua
-- The Auditor: Analyzes death events to provide actionable feedback

local ADDON_NAME, SkillWeaver = ...
SkillWeaver.DeathRecap = {}
local Recap = SkillWeaver.DeathRecap

local eventHistory = {}
local HISTORY_WINDOW = 10 -- Seconds to keep
local MAX_EVENTS = 50

function Recap:Initialize()
    local frame = CreateFrame("Frame")
    frame:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
    frame:RegisterEvent("PLAYER_DEAD")
    
    frame:SetScript("OnEvent", function(_, event)
        if event == "COMBAT_LOG_EVENT_UNFILTERED" then
            self:OnCombatLog()
        elseif event == "PLAYER_DEAD" then
            self:OnDeath()
        end
    end)
    
    print("|cFF00FF00SkillWeaver Auditor loaded|r")
end

function Recap:OnCombatLog()
    local timestamp, subEvent, _, sourceGUID, sourceName, _, _, destGUID, destName = CombatLogGetCurrentEventInfo()
    
    if destGUID ~= UnitGUID("player") then return end
    
    -- Filter for relevant events
    local isDamage = subEvent:find("_DAMAGE")
    local isHeal = subEvent:find("_HEAL")
    
    if not isDamage and not isHeal then return end
    
    local amount, overkill, spellName
    
    if subEvent:find("SWING") then
        amount, overkill = select(12, CombatLogGetCurrentEventInfo())
        spellName = "Melee"
    elseif subEvent:find("SPELL") or subEvent:find("RANGE") then
        local spellId, spName = select(12, CombatLogGetCurrentEventInfo())
        spellName = spName
        amount, overkill = select(15, CombatLogGetCurrentEventInfo())
    elseif subEvent:find("ENVIRONMENTAL") then
        spellName = select(12, CombatLogGetCurrentEventInfo()) -- Environmental type
        amount, overkill = select(13, CombatLogGetCurrentEventInfo())
    end
    
    if not amount then return end
    
    table.insert(eventHistory, {
        time = GetTime(),
        event = subEvent,
        source = sourceName or "Unknown",
        spell = spellName or "Unknown",
        amount = amount,
        overkill = overkill or 0
    })
    
    -- Prune old events
    self:PruneHistory()
end

function Recap:PruneHistory()
    local now = GetTime()
    -- Remove events older than window
    while #eventHistory > 0 and (now - eventHistory[1].time > HISTORY_WINDOW) do
        table.remove(eventHistory, 1)
    end
    
    -- Cap max events
    while #eventHistory > MAX_EVENTS do
        table.remove(eventHistory, 1)
    end
end

function Recap:OnDeath()
    print("|cFFFF0000[SkillWeaver] DEATH RECAP (Last " .. HISTORY_WINDOW .. "s)|r")
    
    local totalDamage = 0
    local totalHealing = 0
    local killer = nil
    
    for i = #eventHistory, 1, -1 do
        local e = eventHistory[i]
        local timeAgo = string.format("%.1f", GetTime() - e.time)
        
        if e.event:find("_DAMAGE") then
            totalDamage = totalDamage + e.amount
            if e.overkill > 0 and not killer then
                killer = e
            end
            
            -- Print significant hits (>10% HP? For now just print all or last few)
            if i > #eventHistory - 5 then -- Last 5 events
                print(string.format("  -%ss: |cFFFF0000-%d|r (%s) from %s", timeAgo, e.amount, e.spell, e.source))
            end
        elseif e.event:find("_HEAL") then
            totalHealing = totalHealing + e.amount
        end
    end
    
    print(string.format("Total Damage Taken: |cFFFF0000%d|r", totalDamage))
    print(string.format("Total Healing Received: |cFF00FF00%d|r", totalHealing))
    
    if killer then
        print(string.format("|cFFFF0000KILLING BLOW:|r %s by %s (%d overkill)", killer.spell, killer.source, killer.overkill))
    end
    
    -- Clear history
    eventHistory = {}
end

Recap:Initialize()
