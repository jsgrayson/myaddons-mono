-- engine/GroupScanner.lua
local GroupScanner = {}

-- Throttled scanning state
local lastScan = 0
local SCAN_INTERVAL = 0.2 -- 200ms throttle is plenty fast enough for group health

-- Cache
GroupScanner.state = {
    groupInjuredCount = 0,
    lowestUnit = nil,
    lowestHP = 1,
    tankLow = false,
}

local function unitHP(u)
  if not UnitExists(u) then return 1 end
  local cur, mx = UnitHealth(u), UnitHealthMax(u)
  if mx == 0 then return 1 end
  return cur / mx
end

function GroupScanner:Scan(threshold)
    local t = GetTime()
    if (t - lastScan) < SCAN_INTERVAL then
        return self.state
    end
    lastScan = t
    
    threshold = threshold or 0.85
    
    local injured = 0
    local lowest, lowestVal = nil, 1
    local tankLow = false
    
    local function check(u)
        if UnitExists(u) and not UnitIsDeadOrGhost(u) then
             local hp = unitHP(u)
             if hp < threshold then injured = injured + 1 end
             if hp < lowestVal then
                 lowestVal = hp
                 lowest = u
             end
             
             -- Optional: Check tank specifically
             if UnitGroupRolesAssigned and UnitGroupRolesAssigned(u) == "TANK" and hp < 0.6 then
                 tankLow = true
             end
             -- Fallback: if focus exists and is friendly, treat as tankish
             if u == "focus" and UnitIsFriend("player", "focus") and hp < 0.6 then
                 tankLow = true
             end
        end
    end

    check("player")
    
    if IsInRaid() then
        for i=1, 40 do check("raid"..i) end
    else
        for i=1, 4 do check("party"..i) end
    end
    
    -- Also check focus explicitly if not covered
    if UnitExists("focus") and not UnitInParty("focus") and not UnitInRaid("focus") then
        check("focus")
    end

    self.state.groupInjuredCount = injured
    self.state.lowestUnit = lowest
    self.state.lowestHP = lowestVal
    self.state.tankLow = tankLow
    
    return self.state
end

return GroupScanner
