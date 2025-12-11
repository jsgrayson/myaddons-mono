-- Test Script for SkillWeaver Logic
-- Run with: lua tests/test_logic.lua

local ADDON_NAME = "SkillWeaver"
local SkillWeaver = {
    Engine = {},
    SafeMode = false,
    Restricted = false,
    FullEngine = true,
    Sequences = {}
}

-- Mock WoW API
local mock_time = 1000
_G.GetTime = function() return mock_time end
_G.UnitPower = function(unit, type) 
    if type == 1 then return 50 end -- Rage
    return 100 
end
_G.UnitPowerMax = function() return 100 end
_G.UnitHealth = function() return 50 end
_G.UnitHealthMax = function() return 100 end
_G.UnitExists = function() return true end
_G.UnitAffectingCombat = function() return true end
_G.GetUnitSpeed = function() return 0 end
_G.GetSpellCooldown = function(spell)
    if spell == "Execute" then return 0, 0 end -- Ready
    if spell == "Mortal Strike" then return 990, 10 end -- On CD (start=990, dur=10, now=1000 -> ready)
    if spell == "Bladestorm" then return 1000, 10 end -- On CD (start=1000, dur=10, now=1000 -> 10s left)
    return 0, 0
end
_G.RunMacroText = function(cmd)
    print("  [EXEC] " .. cmd)
end
_G.AuraUtil = {
    FindAuraByName = function(name)
        if name == "Sudden Death" then return true end
        return false
    end
}

-- Helper to load files relative to script location
-- Assumes running from project root
local function load_module(path)
    local chunk, err = loadfile(path)
    if not chunk then error(err) end
    return chunk(ADDON_NAME, SkillWeaver)
end

print("Loading Modules...")
local Parser = load_module("engine/ConditionParser.lua")
local Engine = load_module("engine/SequenceEngine.lua")
print("Modules Loaded.")

local function assert_true(val, msg)
    if not val then error("FAIL: " .. msg) end
    print("PASS: " .. msg)
end

local function assert_false(val, msg)
    if val then error("FAIL: " .. msg) end
    print("PASS: " .. msg)
end

print("\n--- Testing Condition Parser ---")
assert_true(Parser.Evaluate("true"), "true is true")
assert_false(Parser.Evaluate("false"), "false is false")
assert_true(Parser.Evaluate("rage == 50"), "rage == 50")
assert_true(Parser.Evaluate("rage > 40"), "rage > 40")
assert_false(Parser.Evaluate("rage > 60"), "rage > 60")

-- Boolean Logic
assert_true(Parser.Evaluate("true and true"), "true and true")
assert_false(Parser.Evaluate("true and false"), "true and false")
assert_true(Parser.Evaluate("false or true"), "false or true")
assert_true(Parser.Evaluate("rage > 40 and rage < 60"), "rage range check")
assert_true(Parser.Evaluate("(true or false) and true"), "Parens 1")
assert_false(Parser.Evaluate("false or (true and false)"), "Parens 2")

-- Complex
assert_true(Parser.Evaluate("buff:Sudden Death or cooldown:Bladestorm == 0"), "Buff check")

print("\n--- Testing Sequence Engine (Priority) ---")
SkillWeaver.Sequences["WARRIOR_ARMS"] = {
    ["Raid"] = {
        ["Balanced"] = {
            type = "Priority",
            steps = {
                { command = "/cast Execute", conditions = "rage > 90" }, -- Should fail (rage=50)
                { command = "/cast Mortal Strike", conditions = "rage > 40" }, -- Should pass
                { command = "/cast Slam", conditions = "true" },
            }
        }
    }
}

print("Running Priority Sequence (Expect Mortal Strike)...")
Engine:Run("WARRIOR_ARMS", "Raid", "Balanced")

print("\n--- Testing Sequence Engine (Safe Mode Failover) ---")
SkillWeaver.SafeMode = true
print("SafeMode ON. Running Priority Sequence (Expect Execute - Step 1)...")
-- In Safe Mode, Priority becomes Sequential.
-- First run: Step 1
Engine:Run("WARRIOR_ARMS", "Raid", "Balanced")

print("Running again (Expect Mortal Strike - Step 2)...")
Engine:Run("WARRIOR_ARMS", "Raid", "Balanced")

print("\nAll Tests Passed!")
