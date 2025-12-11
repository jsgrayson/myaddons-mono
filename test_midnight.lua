-- Test Script for Midnight Compliance
-- Simulates restricted environment and verifies SafeGet behavior

dofile("midnight_compliance.lua")

print("--- Midnight Compliance Test ---")

-- 1. Mock UnitHealth (Restricted)
function UnitHealth(unit)
    error("Script too complex") -- Simulate restricted environment error
end

-- 2. Mock UnitPower (Safe)
function UnitPower(unit, type)
    return 1000
end

-- Test 1: SafeGet on Restricted Function
print("\nTest 1: SafeGet on Restricted UnitHealth")
local health = MidnightCompliance.UnitHealth("player")
print("Result: " .. tostring(health))
if health == 100 then
    print("PASS: Fallback value returned")
else
    print("FAIL: Expected 100, got " .. tostring(health))
end

-- Test 2: SafeGet on Safe Function
print("\nTest 2: SafeGet on Safe UnitPower")
local power = MidnightCompliance.UnitPower("player", 0)
print("Result: " .. tostring(power))
if power == 1000 then
    print("PASS: Actual value returned")
else
    print("FAIL: Expected 1000, got " .. tostring(power))
end

-- Test 3: IsSecret Check
print("\nTest 3: IsSecret Check")
if MidnightCompliance.IsSecret("UnitHealth") then
    print("PASS: UnitHealth identified as secret")
else
    print("FAIL: UnitHealth not identified as secret")
end
