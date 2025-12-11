-- Holocron_Status.lua
-- Exports game state for Project Lumos (Lighting Control)

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_DEAD")
f:RegisterEvent("PLAYER_UNGHOST") -- Alive
f:RegisterEvent("CHAT_MSG_LOOT")
f:RegisterEvent("PLAYER_LEVEL_UP")
f:RegisterEvent("PLAYER_REGEN_DISABLED") -- Combat Start
f:RegisterEvent("PLAYER_REGEN_ENABLED")  -- Combat End
f:RegisterEvent("ZONE_CHANGED_NEW_AREA")
f:RegisterEvent("UNIT_HEALTH")
f:RegisterEvent("PLAYER_ENTERING_WORLD")

Holocron_Status = {
    ["combat"] = false,
    ["health"] = 1.0,
    ["zone"] = "Unknown",
    ["is_dead"] = false,
    ["last_loot_rarity"] = 0, -- 0=None, 3=Rare, 4=Epic, 5=Legendary
    ["last_loot_time"] = 0,
    ["timestamp"] = 0
}

f:SetScript("OnEvent", function(self, event, arg1)
    if event == "UNIT_HEALTH" and arg1 ~= "player" then return end
    
    Holocron_Status["combat"] = combat
    Holocron_Status["guid"] = UnitGUID("player") -- Needed for Log Parsing

    -- Health
    local hp = UnitHealth("player")
    local maxHp = UnitHealthMax("player")
    
    -- Check for Secret Values (Patch 12.0+)
    if (issecretvalue and issecretvalue(hp)) or (combat and not issecretvalue) then
        -- In 12.0, HP is secret in combat.
        -- Fallback: If we can't read it, signal -1
        Holocron_Status["health"] = -1.0
    else
        if maxHp > 0 then
            Holocron_Status["health"] = hp / maxHp
        else
            Holocron_Status["health"] = 0.0
        end
    end

    Holocron_Status["zone"] = GetRealZoneText()
    Holocron_Status["is_dead"] = UnitIsDeadOrGhost("player")
    
    if event == "CHAT_MSG_LOOT" then
        -- Simple check for Epic/Legendary color codes in chat string
        -- |cff0070dd = Rare (Blue), |cffa335ee = Epic (Purple), |cffff8000 = Legendary (Orange)
        if string.find(arg1, "cffa335ee") then
            Holocron_Status["last_loot_rarity"] = 4
            Holocron_Status["last_loot_time"] = GetTime()
        elseif string.find(arg1, "cffff8000") then
            Holocron_Status["last_loot_rarity"] = 5
            Holocron_Status["last_loot_time"] = GetTime()
        end
    end

    Holocron_Status["timestamp"] = GetTime()
end)

