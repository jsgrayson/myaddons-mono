-- tests/run.lua
package.path = package.path .. ";./?.lua;./engine/?.lua;./utils/?.lua;./tests/?.lua"

local Sim = require("tests.SimContext")

-- Mock Global Env for WoW
addonTable = {}
SkillWeaver = {}
SkillWeaver.db = { profile = { settings = { debug = false } } }
SkillWeaver.Print = function(self, msg) print("SW: "..msg) end

LibStub = {
    GetAddon = function(self, name) return SkillWeaver end
}
-- Enum mock
Enum = { PowerType = { RunicPower = 6, Mana = 0 } }
C_PvP = { IsPVPMap = function() return false end }

-- Mock ChargeBudget specific to the test spec expectation
local origGetSpellCharges = GetSpellCharges
GetSpellCharges = function(spell)
    if spell == "Blood Boil" then
        return 2, 2, 0, 0 -- Fully capped
    end
    return origGetSpellCharges(spell)
end

-- Custom loader to handle "local addonName, addonTable = ..." which require cannot do
local function loadAddonFile(path)
    local f, err = loadfile(path)
    if not f then error("Failed to load "..path..": "..(err or "unknown")) end
    f("SkillWeaver", addonTable)
end

-- Load Engine Files roughly in TOC order
loadAddonFile("utils/DecisionTrace.lua")
loadAddonFile("engine/SequenceRunner.lua")
loadAddonFile("engine/SectionSplit.lua")
-- For full context, we need Policies too
loadAddonFile("engine/CooldownPolicy.lua")
loadAddonFile("engine/BurstWindow.lua")
loadAddonFile("engine/CooldownSync.lua")
loadAddonFile("engine/ChargeBudget.lua")
loadAddonFile("engine/ResourcePolicy.lua")
loadAddonFile("engine/ProcPolicy.lua")
loadAddonFile("engine/InterruptAuthority.lua")
loadAddonFile("engine/InterruptScanner.lua")
loadAddonFile("engine/CCAuthority.lua")
loadAddonFile("engine/SectionScheduler.lua")

local Runner = SkillWeaver.SequenceRunner
local Split = SkillWeaver.SectionSplit
local Scheduler = SkillWeaver.SectionScheduler

-- Minimal SkillWeaver ExecuteCommand hook
SkillWeaver.lastCommand = nil
function SkillWeaver:ExecuteCommand(cmd) self.lastCommand = cmd end
function SkillWeaver:EvaluateCondition(cond, context) 
    if cond == "true" then return true end
    if cond == "false" then return false end
    return true -- Default true for test simplicity
end

local cases = require("tests.RunnerSpec")

local function extractSpell(cmd)
  if not cmd then return nil end
  local x = cmd:gsub("^/cast%s+", ""):gsub("^%b[]%s*", ""):gsub("%s*$","")
  return x ~= "" and x or nil
end

local pass, fail = 0, 0
print("Running "..#cases.." test cases...")

for _, c in ipairs(cases) do
  SkillWeaver.lastCommand = nil
  Sim.now = 100
  local context = c.context or {}
  
  -- Setup Sim Context
  Sim.buffs = context.procs or {}
  
  -- Build canonical sections so Scheduler works
  -- If test provides 'blocks', we convert to sections.core manually if needed
  -- or we just verify SectionScheduler against a raw list? 
  -- Creating a full sequence object similar to GetNextAction input
  
  local seq = c.seq
  if not seq.sections and seq.blocks then
     seq.sections = Split:FromBlocks(seq.blocks)
  end
  
  -- We want to run SectionScheduler:RunSection logic or full Master tick?
  -- Let's test SectionScheduler:RunSection directly for "core" section to simulate the decision
  
  local execType = seq.meta.exec or "Priority"
  -- sectionSteps
  local sectionSteps = seq.sections.core or {}
  if context.__sectionName then
       sectionSteps = seq.sections[context.__sectionName] or {}
  end
  
  -- Force context section name if missing
  context.__sectionName = context.__sectionName or "core"
  
  local ok = Scheduler:RunSection(Runner, sectionSteps, execType, "st", context)
  
  local got = extractSpell(SkillWeaver.lastCommand)
  if got == c.expect then
    pass = pass + 1
  else
    fail = fail + 1
    print(("FAIL: %s\n  expected: %s\n  got: %s\n"):format(c.name, tostring(c.expect), tostring(got)))
  end
end

print(("Done. pass=%d fail=%d"):format(pass, fail))
os.exit(fail == 0 and 0 or 1)
