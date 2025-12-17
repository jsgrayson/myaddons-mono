local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):NewAddon("SkillWeaver", "AceConsole-3.0", "AceEvent-3.0")
addonTable.SkillWeaver = SkillWeaver
local AceGUI = LibStub("AceGUI-3.0")

local Serializer = LibStub("AceSerializer-3.0")
local SpecRegistry = require("db.SpecRegistry")
local RotationStore = require("rotations.RotationStore")
local Policies = require("engine.Policies")
local SequenceResolver = require("engine.SequenceResolver")
local HealPass = require("engine.HealPass")
local ClassHeals = require("policies.healing.ClassHeals")
local SpecProfiles = require("policies.healing.SpecProfiles")
local HybridSupport = require("policies.healing.HybridSupport")
local GroupScanner = require("engine.GroupScanner")

-- ============================================================================
-- DB Defaults (canonical storage)
-- ============================================================================

local defaults = {
  profile = {
    settings = {
      debug = false,
      autoswitch = true, -- NEW
    },
    profiles = {},  -- [id] = { name, specId, class, active=false }
    sequences = {}, -- [id] = { name, profileId, stepsText="", steps={}, notes, contentType, priority }
    toggles = {},   -- [name] = { enabled=true/false }
    meta = { last_profileId = nil, last_seqId = nil, last_content = nil }
  }
}

local function NewId()
  -- Good enough for local IDs; we can replace with monotonic later.
  return tostring(math.random(1000000, 9999999))
end

-- ============================================================================
-- Auto-Switch: Moved to autoswitch.lua
-- ============================================================================

local function GetActiveProfile(self)
  for _, prof in pairs(self.db.profile.profiles) do
    if prof and prof.active then return prof end
  end
  return nil
end

local function GetSequenceForProfile(self, profileId)
  if not profileId then return nil end
  for _, seq in pairs(self.db.profile.sequences) do
    if seq and seq.profileId == profileId then return seq end
  end
  return nil
end

-- ============================================================================
-- Init / Commands
-- ============================================================================

function SkillWeaver:OnInitialize()
  self.db = LibStub("AceDB-3.0"):New("SkillWeaverDB", defaults, true)
  self:EnsureSettings()
  self:EnsureAllSequenceDefaults()

  -- AceConsole commands ONLY (do not also register SLASH_* manually)
  self:RegisterEvent("PLAYER_REGEN_DISABLED")
  self:RegisterEvent("PLAYER_REGEN_ENABLED")
  self:RegisterEvent("PLAYER_TARGET_CHANGED")
  
  -- Initialize Minimap
  local Minimap = require("ui.Minimap")
  Minimap:Init()
  
  -- Initialize AutoSelf
  require("engine.AutoSelf")

  self:Print("SkillWeaver Loaded. /sw for options.")
  
  -- Content mode auto-switch hooks (safe)
  self.currentMode = self:DetectContentMode()
  self:RegisterEvent("PLAYER_ENTERING_WORLD", "OnContentMaybeChanged")
  self:RegisterEvent("ZONE_CHANGED_NEW_AREA", "OnContentMaybeChanged")

  -- Mythic+ signals (safe if not present)
  if self.RegisterEvent then
    self:RegisterEvent("CHALLENGE_MODE_START", "OnContentMaybeChanged")
    self:RegisterEvent("CHALLENGE_MODE_COMPLETED", "OnContentMaybeChanged")
  end
end

----------------------------------------------------------------
-- (2) MIGRATION SAFETY: ensure settings/autoswitch exists after DB load
----------------------------------------------------------------
function SkillWeaver:EnsureSettings()
    self.db.profile.settings = self.db.profile.settings or {}
    if self.db.profile.settings.autoswitch == nil then self.db.profile.settings.autoswitch = true end
    if self.db.profile.settings.debug == nil then self.db.profile.settings.debug = false end
    -- manual override: when set, autoswitch uses this instead of detected content
    -- values: "RAID","MYTHIC_PLUS","DELVES","PVP","DUNGEON","OPEN_WORLD"
    self.db.profile.settings.contentOverride = self.db.profile.settings.contentOverride or nil
end

----------------------------------------------------------------
-- (3) CONTENT DETECTION (MVP)
----------------------------------------------------------------
local SW_CONTENT_KEYS = {RAID=1,MYTHIC_PLUS=1,DELVES=1,PVP=1,DUNGEON=1,OPEN_WORLD=1}
local function SW_NormalizeKey(k)
    k = tostring(k or ""):upper():gsub("%s+", "_")
    if k == "MPLUS" then k = "MYTHIC_PLUS" end
    if SW_CONTENT_KEYS[k] then return k end
    return nil
end

function SkillWeaver:GetContentBucket()
     -- Manual override support (preserved from previous patch for utility)
    if self.db and self.db.profile and self.db.profile.settings and self.db.profile.settings.contentOverride then
        local ov = SW_NormalizeKey(self.db.profile.settings.contentOverride)
        if ov then return ov end
    end

    -- Priority: Mythic+ > Raid/Dungeon/PvP > Delves/Scenario > Open World
    if C_ChallengeMode and C_ChallengeMode.IsChallengeModeActive and C_ChallengeMode.IsChallengeModeActive() then
        return "MYTHIC_PLUS"
    end

    local inInstance, instanceType = IsInInstance()
    if inInstance then
        if instanceType == "raid" then return "RAID" end
        if instanceType == "party" then return "DUNGEON" end
        if instanceType == "pvp" or instanceType == "arena" then return "PVP" end
        -- Many delves/scenarios show as "scenario" (heuristic)
        if instanceType == "scenario" then return "DELVES" end
    end

    -- Warmode / PvP without instance is still basically OPEN_WORLD for rotations
    return "OPEN_WORLD"
end

-- Alias for UI compatibility if needed
function SkillWeaver:DetectContentType() return self:GetContentBucket() end

----------------------------------------------------------------
-- (4) ACTIVE SETTERS (safe no-op if you already added these in a prior patch)
----------------------------------------------------------------
function SkillWeaver:SetActiveProfile(profileId)
    if not profileId or not self.db.profile.profiles[profileId] then return false end
    for _, p in pairs(self.db.profile.profiles) do p.active = false end
    self.db.profile.profiles[profileId].active = true
    self.db.profile.meta.last_profileId = profileId
    return true
end

function SkillWeaver:SetActiveSequence(seqId)
    if not seqId or not self.db.profile.sequences[seqId] then return false end
    self.db.profile.meta.last_seqId = seqId
    -- Also uncheck 'active' on all sequences to keep state clean (hybrid approach)
    for _, s in pairs(self.db.profile.sequences) do s.active = false end
    self.db.profile.sequences[seqId].active = true
    return true
end

----------------------------------------------------------------
-- (5) AUTO-SELECT: pick best sequence for current content for ACTIVE profile
----------------------------------------------------------------
function SkillWeaver:AutoSwitchNow(reason)
    self:EnsureSettings()
    if not (self.db and self.db.profile and self.db.profile.settings and self.db.profile.settings.autoswitch) then
        return
    end

    -- Find active profile
    local activeProfileId
    for id, prof in pairs(self.db.profile.profiles or {}) do
        if prof and prof.active then activeProfileId = id break end
    end
    
    -- If no active profile, try to auto-select one (Agentic Improvement: Restore Profile Switching)
    if not activeProfileId and self.AutoSelectProfileForCurrentSpec then
        activeProfileId = self:AutoSelectProfileForCurrentSpec()
    end
    
    if not activeProfileId then return end

    local bucket = self:GetContentBucket()
    self.db.profile.meta.last_content = bucket

    -- Choose best seq for that profile + bucket by priority
    local bestSeqId, bestPriority = nil, -math.huge
    for id, seq in pairs(self.db.profile.sequences or {}) do
        if seq and tostring(seq.profileId) == tostring(activeProfileId) then
            local seqBucket = (seq.contentType or "OPEN_WORLD"):upper()
            if seqBucket == bucket then
                local p = tonumber(seq.priority) or 0
                if p > bestPriority then
                    bestPriority = p
                    bestSeqId = id
                end
            end
        end
    end

    -- Fallback: if nothing matches current bucket, pick OPEN_WORLD highest priority
    if not bestSeqId then
        for id, seq in pairs(self.db.profile.sequences or {}) do
            if seq and tostring(seq.profileId) == tostring(activeProfileId) then
                local seqBucket = (seq.contentType or "OPEN_WORLD"):upper()
                if seqBucket == "OPEN_WORLD" then
                    local p = tonumber(seq.priority) or 0
                    if p > bestPriority then
                        bestPriority = p
                        bestSeqId = id
                    end
                end
            end
        end
    end

    if bestSeqId then
        local current = self.db.profile.meta.last_seqId
        if current ~= bestSeqId then
            self:SetActiveSequence(bestSeqId)
            if self.db.profile.settings.debug then
                local seq = self.db.profile.sequences[bestSeqId]
                self:Print(("AutoSwitch[%s]: %s -> %s (prio %d)"):format(
                    tostring(reason or "tick"),
                    bucket,
                    tostring(seq and seq.name or bestSeqId),
                    tonumber(bestPriority) or 0
                ))
            end
        end
    end
end

-- Backward compatibility wrapper
function SkillWeaver:RunAutoSwitch(reason) self:AutoSwitchNow(reason) end

----------------------------------------------------------------
-- (6) EVENT WIRING (lightweight + safe)
----------------------------------------------------------------
function SkillWeaver:OnEnable()
    self:EnsureSettings()
    -- Only register once
    if self._autoswitchEventsRegistered then return end
    self._autoswitchEventsRegistered = true

    -- These fire often enough to keep content accurate without spam
    self:RegisterEvent("PLAYER_ENTERING_WORLD", function() self:AutoSwitchNow("entering_world") end)
    self:RegisterEvent("ZONE_CHANGED_NEW_AREA", function() self:AutoSwitchNow("zone_changed") end)
    self:RegisterEvent("GROUP_ROSTER_UPDATE", function() self:AutoSwitchNow("group_update") end)
    self:RegisterEvent("PLAYER_SPECIALIZATION_CHANGED", function() self:AutoSwitchNow("spec_changed") end) -- added back for safety

    if C_ChallengeMode then
        self:RegisterEvent("CHALLENGE_MODE_START", function() self:AutoSwitchNow("mplus_start") end)
        self:RegisterEvent("CHALLENGE_MODE_COMPLETED", function() self:AutoSwitchNow("mplus_done") end)
    end

    -- PvP talent updates often correlates with entering PvP modes
    self:RegisterEvent("PLAYER_PVP_TALENT_UPDATE", function() self:AutoSwitchNow("pvp_talent") end)

    -- Initial
    self:AutoSwitchNow("enable")
end

----------------------------------------------------------------
-- Helpers: Active Profile / Active Sequence
----------------------------------------------------------------
----------------------------------------------------------------
-- Helpers: active profile + active sequence (stored on seq.active)
----------------------------------------------------------------
function SkillWeaver:GetActiveProfileId()
  if not (self.db and self.db.profile and self.db.profile.profiles) then return nil end
  for id, prof in pairs(self.db.profile.profiles) do
    if prof and prof.active then return id end
  end
  return self.db.profile.meta and self.db.profile.meta.last_profileId or nil
end

function SkillWeaver:GetActiveSequenceId()
  if not (self.db and self.db.profile and self.db.profile.sequences) then return nil end
  for id, seq in pairs(self.db.profile.sequences) do
    if seq and seq.active then return id end
  end
  return self.db.profile.meta and self.db.profile.meta.last_seqId or nil
end

function SkillWeaver:SetActiveSequence(seqId)
  if not (self.db and self.db.profile and self.db.profile.sequences) then return end
  for _, s in pairs(self.db.profile.sequences) do
    if s then s.active = false end
  end
  local seq = self.db.profile.sequences[seqId]
  if seq then
    seq.active = true
    self.db.profile.meta = self.db.profile.meta or {}
    self.db.profile.meta.last_seqId = seqId
  end
end

----------------------------------------------------------------
-- 2) Sequence schema upgrade (adds: contentType + priority + stepsText)
----------------------------------------------------------------
function SkillWeaver:EnsureSequenceDefaults(seq)
  if not seq then return end
  if seq.contentType == nil then seq.contentType = "OPEN_WORLD" end -- "RAID","MYTHIC_PLUS","DELVES","PVP","DUNGEON","OPEN_WORLD"
  if seq.priority == nil then seq.priority = 0 end
  if seq.stepsText == nil and type(seq.steps) == "table" then
    -- keep compatibility if older seq stored as raw lines
    seq.stepsText = table.concat(seq.steps, "\n")
  end
end

function SkillWeaver:EnsureAllSequenceDefaults()
  if not (self.db and self.db.profile and self.db.profile.sequences) then return end
  for _, seq in pairs(self.db.profile.sequences) do
    self:EnsureSequenceDefaults(seq)
  end
end

----------------------------------------------------------------
-- 3) Step rebuild: Normalizes text -> Sections or Flat Steps
----------------------------------------------------------------
function SkillWeaver:RebuildSequence(seq)
  if not seq then return end
  
  -- Validation (Soft)
  if SkillWeaver.SequenceValidator then
     local errs, warns = SkillWeaver.SequenceValidator:Validate(seq)
     if #errs > 0 and self.db.profile.settings.debug then
        self:Print("Sequence Validation Errors: " .. table.concat(errs, ", "))
     end
  end

  -- If manually authored via stepsText, normalize to 'core' section
  if seq.stepsText and seq.stepsText ~= "" then
      local parsed = self:ParseSteps(seq.stepsText)
      -- Populate BOTH for compatibility during transition
      seq.steps = parsed
      seq.sections = seq.sections or {}
      seq.sections.core = parsed
      seq._parsed = true
      return
  end
  
  -- If Import provided raw sections but no stepsText, trust existing sections
  if seq.sections then
      seq._parsed = true
      return
  end
  
  -- Fallback
  seq.steps = {}
  seq._parsed = true
end

----------------------------------------------------------------
-- 4) AutoSelectSequence(profileId, contentType)
-- Picks best matching sequence for the profile + content bucket.
----------------------------------------------------------------
local function SW_ContentMatch(a, b)
  if not a then return false end
  a = tostring(a):upper()
  b = tostring(b or ""):upper()
  return a == b
}

function SkillWeaver:AutoSelectSequence(profileId, contentType)
  if not (self.db and self.db.profile and self.db.profile.sequences) then return nil end
  if not profileId then return nil end

  contentType = tostring(contentType or "OPEN_WORLD"):upper()

  self.db.profile.meta = self.db.profile.meta or {}
  self.db.profile.meta.last_seqByContext = self.db.profile.meta.last_seqByContext or {}
  self.db.profile.meta.last_seqByContext[profileId] = self.db.profile.meta.last_seqByContext[profileId] or {}
  local remembered = self.db.profile.meta.last_seqByContext[profileId][contentType]

  local bestId, bestScore = nil, -999999
  for id, seq in pairs(self.db.profile.sequences) do
    if seq and seq.profileId == profileId then
      self:EnsureSequenceDefaults(seq)

      local score = 0

      -- Strong preference: exact content type
      if SW_ContentMatch(seq.contentType, contentType) then
        score = score + 200
      elseif SW_ContentMatch(seq.contentType, "OPEN_WORLD") then
        -- fallback bucket
        score = score + 50
      else
        -- other bucket: still selectable but lower
        score = score - 25
      end

      -- Remembered choice for this context
      if remembered and id == remembered then score = score + 100 end

      -- Priority field
      score = score + (tonumber(seq.priority) or 0)

      -- If it is currently active, slight bias
      if seq.active then score = score + 10 end

      if score > bestScore then
        bestScore = score
        bestId = id
      end
    end
  end

  if bestId then
    -- Ensure parsed steps exist
    local chosen = self.db.profile.sequences[bestId]
    self:EnsureSequenceDefaults(chosen)
    self:RebuildSequence(chosen)

    self:SetActiveSequence(bestId)
    self.db.profile.meta.last_seqByContext[profileId][contentType] = bestId

    if self.db.profile.settings and self.db.profile.settings.debug then
      self:Print(("AutoSwitch -> Sequence: %s (content=%s, prio=%s)"):format(
        tostring(chosen.name), tostring(contentType), tostring(chosen.priority)
      ))
    end
  end

  return bestId
end


function SkillWeaver:HandleCommand(input)
  input = tostring(input or "")
  local cmd, arg = input:lower():match("^(%S+)%s*(.*)")
  cmd = cmd or ""

  if cmd == "dump" then
    local profileCount = 0
    local activeProfileName = "None"
    for _, prof in pairs(self.db.profile.profiles) do
      profileCount = profileCount + 1
      if prof.active then activeProfileName = prof.name end
    end

    local seqCount = 0
    for _ in pairs(self.db.profile.sequences) do seqCount = seqCount + 1 end

    self:Print("SW DUMP: Profiles=" .. profileCount .. ", Sequences=" .. seqCount .. ", Active=" .. activeProfileName)
    return
  end

  if cmd == "sanity" then
    local passed = true

    if type(self.db.profile.profiles) ~= "table" then
      self:Print("FAIL: Missing profiles table")
      passed = false
    end

    if type(self.db.profile.sequences) ~= "table" then
      self:Print("FAIL: Missing sequences table")
      passed = false
    end

    local activeCount = 0
    for _, prof in pairs(self.db.profile.profiles or {}) do
      if prof and prof.active then activeCount = activeCount + 1 end
    end

    if activeCount > 1 then
      self:Print("FAIL: Multiple active profiles")
      passed = false
    end

    if passed then
      self:Print("|cff00FF00SW SANITY PASS|r")
      print(string.format('SANITY_RESULT {"addon":"SkillWeaver","status":"OK","checks":3,"failures":0}'))
    else
      self:Print("|cffFF0000SW SANITY FAIL|r")
      print(string.format('SANITY_RESULT {"addon":"SkillWeaver","status":"FAIL","checks":3,"failures":1}'))
    end
    return
  end

  if cmd == "rebuild" then
    for _, seq in pairs(self.db.profile.sequences) do self:RebuildSequence(seq) end
    self:Print("Sequences rebuilt (cache cleared + steps parsed).")
    return
  end

  if cmd == "resetdb" then
    SkillWeaverDB = nil
    ReloadUI()
    return
  end

  if cmd == "next" then
    local a = self:GetNextAction()
    self:Print("NextAction=" .. tostring(a))
    return
  end

  elseif cmd == "mode" then
    local m = (input:match("^%S+%s+(%S+)") or "auto"):lower()
    local valid = { auto=true, raid=true, mythicplus=true, delve=true, pvp=true, openworld=true }
    if not valid[m] then
      self:Print("Usage: /sw mode <auto|raid|mythicplus|delve|pvp|openworld>")
      return
    end
    self:SetModeOverride(m)
    return

  elseif cmd == "autoswitch" then
    local arg = (arg or ""):lower():match("^%s*(.*)$"):gsub("^%s+",""):gsub("%s+$","")
    self:EnsureSettings()
    local s = self.db.profile.settings
    if arg == "" or arg == "status" then
        self:Print("AutoSwitch:", s.autoswitch and "ON" or "OFF", "content=", tostring(self.db.profile.meta.last_content or "nil"))
        return
    end
    if arg == "on" then s.autoswitch = true
    elseif arg == "off" then s.autoswitch = false
    elseif arg == "toggle" then s.autoswitch = not s.autoswitch
    else
        self:Print("Usage: /sw autoswitch on|off|toggle|status")
        return
    end
    self:Print("AutoSwitch now:", s.autoswitch and "ON" or "OFF")
    if s.autoswitch then self:AutoSwitchNow("manual") end
    return
  end

  if cmd == "content" then
      self:EnsureSettings()
      local t = (arg or ""):match("^(%S+)")
      if not t or t:lower() == "clear" then
          self.db.profile.settings.contentOverride = nil
          self:Print("Content override: CLEARED (auto-detect enabled)")
      else
          local norm = SW_NormalizeContentType(t)
          self.db.profile.settings.contentOverride = norm
          self:Print("Content override: " .. norm)
      end
      self:RunAutoSwitch("content")
      return
  end
  
  elseif cmd == "supportheal" then
      self.db.profile.settings.supportHeal = not self.db.profile.settings.supportHeal
      self:Print("Support Healing: " .. (self.db.profile.settings.supportHeal and "ENABLED" or "DISABLED"))
      return
  
  elseif cmd == "seq" then
      -- /sw seq set <seqId> <bucket>
      -- /sw seq prio <seqId> <number>
      -- /sw seq use <seqId>
      self:EnsureSettings()
      self:EnsureAllSequenceDefaults()
      local sub, a, b = (arg or ""):match("^(%S+)%s*(%S*)%s*(.*)$")
      sub = (sub or ""):lower()

      if sub == "use" and a ~= "" then
        local id = a
        if self.db.profile.sequences[id] then
          self:SetActiveSequence(id)
          self:Print("Active sequence set: " .. tostring(self.db.profile.sequences[id].name))
        else
          self:Print("Unknown seq id: " .. tostring(id))
        end
        return
      end

      if sub == "set" and a ~= "" and b ~= "" then
        local id = a
        local bucket = b:match("^(%S+)")
        bucket = bucket and bucket:upper() or "OPEN_WORLD"
        if self.db.profile.sequences[id] then
          self.db.profile.sequences[id].contentType = bucket
          self:Print(("Seq %s bucket -> %s"):format(id, bucket))
        end
        return
      end

      if sub == "prio" and a ~= "" and b ~= "" then
        local id = a
        local p = tonumber(b) or 0
        if self.db.profile.sequences[id] then
          self.db.profile.sequences[id].priority = p
          self:Print(("Seq %s priority -> %s"):format(id, p))
        end
        return
      end

      self:Print("Usage: /sw seq use <seqId> | /sw seq set <seqId> <RAID|MYTHIC_PLUS|DELVES|PVP|DUNGEON|OPEN_WORLD> | /sw seq prio <seqId> <n>")
      return
  end
  
  self:ToggleUI()
end

-- ============================================================================
-- Step Parser (canonical input = stepsText string)
-- ============================================================================

function SkillWeaver:ParseSteps(stepsText)
  local steps = {}
  if not stepsText or stepsText == "" then return steps end

  for line in stepsText:gmatch("[^\r\n]+") do
    line = line:match("^%s*(.-)%s*$") -- trim

    if line ~= "" and not line:match("^#") then
      local action, cond = line:match("^(.-)%s*|%s*(.+)$")
      if not action then
        action = line
        cond = "always"
      end

      -- normalize action (allow "12345" or "spellId:12345" later)
      action = action:match("^%s*(.-)%s*$")
      cond = (cond or "always"):match("^%s*(.-)%s*$")

      table.insert(steps, {
        action = action,
        cond = cond,
        enabled = true
      })
    end
  end

  return steps
end

local function GetParsedSteps(self, seq)
  if not seq then return nil end
  if not seq._parsedSteps then
    seq._parsedSteps = self:ParseSteps(seq.stepsText or "")
  end
  return seq._parsedSteps
end

-- ============================================================================
-- Condition Evaluator (MVP whitelist)
-- ============================================================================

function SkillWeaver:EvaluateCondition(cond, context)
  if not cond or cond == "" or cond == "always" then return true end

  -- Normalize enemy keys to "active_enemies"
  cond = cond:gsub("enemies_nearby", "active_enemies")
  cond = cond:gsub("enemies", "active_enemies")
  
  -- Handle active_enemies from context if present
  if context and context.activeEnemies then
      -- Simple substitution (requires robust parsing for real usage, but MVP hack for "active_enemies>=3")
      local count = tonumber(context.activeEnemies) or 0
      local op, val = cond:match("active_enemies%s*([<>=]=?)%s*(%d+)")
      if op and val then
          val = tonumber(val)
          if op == ">=" then return count >= val end
          if op == "<=" then return count <= val end
          if op == ">" then return count > val end
          if op == "<" then return count < val end
          if op == "==" then return count == val end
      end
  end

  -- NEW: should_interrupt token
  if cond:find("should_interrupt") then
      if SkillWeaver.InterruptAuthority then
          -- Pass context if available? EvaluateCondition usually needs context now.
          -- If context is nil, Decide(nil) uses target/defaults.
          if SkillWeaver.InterruptAuthority:Decide(context) then
              return true
          else
              -- If exact match "should_interrupt", return false.
              -- If complex "should_interrupt or ...", continue?
              -- Simple substitution logic:
              cond = cond:gsub("should_interrupt", "false")
              -- But if it WAS true, we'd return true? 
              -- Actually if we are evaluating a boolean string, we need to substitute.
              -- But for MVP single token:
              if cond == "should_interrupt" then return false end
          end
      end
  end

  -- target.health<0.2
  do
    local op, val = cond:match("^target%.health%s*([<>=]=?)%s*([%d%.]+)$")
    if op and val then
      val = tonumber(val)
      if UnitExists("target") and UnitHealthMax("target") and UnitHealthMax("target") > 0 then
        local healthPct = UnitHealth("target") / UnitHealthMax("target")
        if op == "<" then return healthPct < val end
        if op == ">" then return healthPct > val end
        if op == "<=" then return healthPct <= val end
        if op == ">=" then return healthPct >= val end
        if op == "==" then return healthPct == val end
      end
      return false
    end
  end

  -- player.mana>0.5
  do
    local op, val = cond:match("^player%.mana%s*([<>=]=?)%s*([%d%.]+)$")
    if op and val then
      val = tonumber(val)
      local maxMana = UnitPowerMax("player", Enum.PowerType.Mana) or 0
      if maxMana > 0 then
        local manaPct = (UnitPower("player", Enum.PowerType.Mana) or 0) / maxMana
        if op == "<" then return manaPct < val end
        if op == ">" then return manaPct > val end
        if op == "<=" then return manaPct <= val end
        if op == ">=" then return manaPct >= val end
        if op == "==" then return manaPct == val end
      end
      return false
    end
  end

  -- cooldown(12345).ready
  do
    local cdSpell = cond:match("^cooldown%((%d+)%)%.ready$")
    if cdSpell then
      local spellId = tonumber(cdSpell)
      local start, duration = GetSpellCooldown(spellId)
      if not start or not duration then return false end
      return (start == 0) or ((start + duration - GetTime()) <= 0)
    end
  end

  if self.db.profile.settings and self.db.profile.settings.debug then
    self:Print("Unknown condition: " .. tostring(cond))
  end
  return false
end

function SkillWeaver:OnContentMaybeChanged()
  if not (self.db and self.db.profile and self.db.profile.settings and self.db.profile.settings.autoSwitch) then return end
  local mode = self:DetectContentMode()
  if mode ~= self.currentMode then
    -- (1) Spec Registry available
    -- (2) Load Policies
    self.policies_loaded = Policies:LoadAll()
    
    -- (3) Helper function to get all spec keys
    local function allSpecKeys()
      local keys = {}
      for _, specs in pairs(SpecRegistry) do
        for _, meta in pairs(specs) do
          keys[#keys+1] = meta.key
        end
      end
      table.sort(keys)
      return keys
    end
    
    -- (4) Initialize Sequences from RotationStore (Offline-First)
    SkillWeaverDB = SkillWeaverDB or {}
    SkillWeaverDB.Sequences = RotationStore:BuildAll(allSpecKeys())

    self:Printf("Engine initialized. Loaded %d policy packs.", self.policies_loaded)
    self.currentMode = mode
    if self.db.profile.settings.debug then
      self:Print("Content mode -> " .. tostring(mode))
    end
  end
end

function SkillWeaver:SetModeOverride(mode)
  self.db.profile.settings.modeOverride = mode
  self.currentMode = self:DetectContentMode()
  self:Print("Mode override: " .. tostring(mode) .. " (effective=" .. tostring(self.currentMode) .. ")")
end

-- ============================================================================
-- Runtime (MVP): returns step.action string
-- ============================================================================

----------------------------------------------------------------
-- Use selected sequence in runtime action picker
-- (Replaces your current "first sequence for profile" logic.)
----------------------------------------------------------------

----------------------------------------------------------------
-- 5) Make GetNextAction use ACTIVE sequence + SECTION SCHEDULER
----------------------------------------------------------------
----------------------------------------------------------------
-- 5) Make GetNextAction use ACTIVE sequence + SECTION SCHEDULER + RUNNER
----------------------------------------------------------------
function SkillWeaver:ExecuteCommand(cmd)
    -- This is the bridge for SequenceRunner.
    -- Instead of protected CastSpellByName, we store it for the HW event bridge.
    self.nextAction = cmd
end

function SkillWeaver:MakeRuntimeContext()
    -- MVP context (Rich)
    local isBoss = false
    if UnitExists("target") then
        local c = UnitClassification("target")
        if c == "worldboss" or c == "rareelite" or c == "elite" or (UnitLevel("target") == -1) then
            isBoss = true
        end
        -- Dungeons/Raids check? 
        -- For now, simple classification check is "good enough" for MVP Policy
    end
    
    local cTime = 0 
    -- Basic combat time tracker (requires engine state if not using API)
    -- Using GetTime() - self.combatStart if self.inCombat
    if self.inCombat and self.combatStart then
        cTime = GetTime() - self.combatStart
    end
    
    -- Basic proc scanner for MVP
    -- In real engine, use event listeners to cache this table. Scanning AuraUtil every tick is pricey but workable for MVP.
    local function checkBuff(name)
        if AuraUtil.FindAuraByName then return AuraUtil.FindAuraByName(name, "player") ~= nil end
        return false 
    end
    
    local ctxt = {
        activeEnemies = 1, -- TODO: wiring
        aoeThreshold = 3,
        range = 5,
        isBoss = isBoss,
        activeEnemies = self.activeEnemies,
        aoeThreshold = self.db.profile.settings.aoeThreshold or 3,
        isBoss = UnitClassification("target") == "worldboss" or UnitClassification("target") == "boss",
        burstSoonSeconds = nil, -- Stub
    }
    
    -- (1) Group Scanner (Throttled)
    local scan = GroupScanner:Scan(0.85) -- Global threshold
    ctxt.groupInjuredCount = scan.groupInjuredCount
    ctxt.tankLow = scan.tankLow
    
    -- Load Policy Pack
    local specKey = self:GetCurrentSpecKey() -- Need to ensure this exists or use Registry approach
    if not specKey and addonTable.SpecRegistry then
        local specID = GetSpecializationInfo(GetSpecialization() or 1)
        local info = addonTable.SpecRegistry:Get(specID)
        if info then 
            specKey = info.key 
        end
    end

    if specKey and specKey ~= "" then
        ctxt.specKey = specKey
        -- Load policies from Manager
        if self.PolicyManager then
             ctxt.policy = self.PolicyManager:GetEffectivePolicy(specKey)
        end
        
        -- Role Policies
        local _, _, _, _, role = GetSpecializationInfo(GetSpecialization() or 1)
        ctxt.role = role
        local _, className = UnitClass("player")
        
        if role == "HEALER" then
             if className and ClassHeals[className] then
                 ctxt.policy = ctxt.policy or {}
                 ctxt.policy.healing = ctxt.policy.healing or ClassHeals[className]
             end
        elseif role == "DAMAGER" or role == "TANK" then
             -- Support Heal Toggle check
             if self.db.profile.settings.supportHeal and className and HybridSupport[className] then
                 ctxt.policy = ctxt.policy or {}
                 ctxt.policy.supportHealing = ctxt.policy.supportHealing or HybridSupport[className]
             end
        end
    end
    
    local policyPack = addonTable.Policies and addonTable.Policies:Get(specKey)
    if not policyPack and addonTable.PolicyManager then
       policyPack = addonTable.PolicyManager:Get(specKey)
    end
    
    ctxt.policyPack = policyPack -- Store ref for generic policies
    
    -- Merge defaults with pack
    ctxt.resourceRules = policyPack and policyPack.resources or SkillWeaver.ResourcePolicy.defaults
    ctxt.cooldownRules = policyPack and policyPack.cooldownRules or (self.db.profile.settings.cooldownRules or SkillWeaver.CooldownPolicy.defaults)
    ctxt.cooldownSync  = policyPack and policyPack.cooldownSync -- Special handling in Sync module usually
    ctxt.procsConfig   = policyPack and policyPack.procs
    
    -- Universal Resource Provider (replaces ad-hoc runicPower)
    if addonTable.ResourceProvider then
        local res = addonTable.ResourceProvider:Get(ctxt)
        ctxt.primaryResource = res.token
        ctxt.resourceState = res -- useful for debug
        ctxt.runicPower = res.cur -- back-compat alias if needed, though provider handles it
    end

    -- Universal Interrupt Kits
    local Kits = addonTable.InterruptKits
    ctxt.className = ctxt.className or select(2, UnitClass("player"))
    local kit = (policyPack and policyPack.interrupts and policyPack.interrupts.kit)
            or (Kits and Kits.byClass[ctxt.className])
    ctxt.interruptKit = kit
    
    ctxt.procs = {
             ["Killing Machine"] = checkBuff("Killing Machine"),
             ["Rime"] = checkBuff("Rime"),
             ["Sudden Doom"] = checkBuff("Sudden Doom"),
             ["Heating Up"] = checkBuff("Heating Up"),
             ["Hot Streak"] = checkBuff("Hot Streak"),
             ["Divine Purpose"] = checkBuff("Divine Purpose"),
        },
        interruptUnit = "AUTO",
        petExists = UnitExists("pet"),
        kickAt = 0.50,
        minKickRemaining = 0.2, -- seconds
        isPvP = (C_PvP and C_PvP.IsPVPMap and C_PvP.IsPVPMap()) or false, 
        dr = nil, -- Stub for DR tracker
    }
    
    if SkillWeaver.BurstWindow then
        ctxt.burstWindow = SkillWeaver.BurstWindow:IsActive(ctxt)
    end
    
    return ctxt
end

function SkillWeaver:GetNextAction()
  -- 1) Context
  local context = self:MakeRuntimeContext()

  -- 2) Sequence Selection (uses last known or auto-switch result)
  local seqId = self:GetActiveSequenceId()
  local seq = seqId and self.db.profile.sequences[seqId]
  
  -- 3) Runner Wrapper (CanCast fn)
  local function CanCast(spellName, ctx, targetUnit)
       -- Simple check for MVP. In real engine this checks range, power, cd.
       -- For now, just CD check.
       if not spellName then return false end
       local started, duration = GetSpellCooldown(spellName)
       if started and duration and (started > 0 and duration > 1.5) then
          return false -- on CD (ignoring GCD)
       end
       -- Range check could go here
       return true
  end

  -- NEW: 3b) HEAL PASS (Priority over rotation)
  -- Now returns a full macro string if successful
  local healMacro = HealPass:Run(context, CanCast)
  if healMacro then
       return healMacro
  end

  -- 4) Sequence Execution
  if not seq then return nil end

    -- normalize runtime shape if not ready
    if not seq._normalized then
        -- This logic bridges the gap between DB shape and Runner Normalized shape
        self:RebuildSequence(seq) -- ensure steps/sections exist
        
        -- Normalization Step 1: Flatten to blocks (if legacy)
        local stBlocks = {}
        if seq.steps then
             for _, s in ipairs(seq.steps) do table.insert(stBlocks, {command=s.action, conditions=s.cond}) end
        elseif seq.sections then
             -- If sections already exist in DB (from Import), flatten them to ST for now?
             -- Actually, Master handles sections. We just need to ensure 'blocks' exists for the Splitter to work on if sections are missing.
             -- If sections exist, Master uses them.
             -- If blocks exist, Master splits them.
        end
        
        -- Create a normalized object
        seq._normalized = {
            meta = { 
                key = "PlayerSpec", -- dynamic?
                profile = seq.name, 
                exec = "Sequential" -- Legacy default
            },
            blocks = {
                st = stBlocks,
                aoe = {} 
            },
            sections = seq.sections -- Pass through if present
        }
    end

    local context = self:MakeRuntimeContext()
    if self.SequenceMaster then
        self.SequenceMaster:Tick(seq._normalized, context)
    end

    -- Legacy fallback if Runner didn't set nextAction (or if Runner missing)
    if not self.nextAction then
         return nil
    end

    return self.nextAction
end

-- ============================================================================
-- Export/Import (safe): AceSerializer
-- ============================================================================

function SkillWeaver:ExportSequence(seq)
  local payload = {
    type = "SkillWeaverSequence",
    ver = 1,
    name = seq.name,
    stepsText = seq.stepsText or "",
    notes = seq.notes or "",
  }
  return Serializer:Serialize(payload)
end

function SkillWeaver:ImportSequence(serialized)
  local ok, payload = Serializer:Deserialize(serialized)
  if not ok or type(payload) ~= "table" or payload.type ~= "SkillWeaverSequence" then
    return false, "Invalid import payload"
  end
  return true, payload
end

-- Helpers for the UI (using AceSerializer as the "JSON" engine for now)
function SkillWeaver:TableToJSON(t)
  return Serializer:Serialize(t)
end

function SkillWeaver:JSONToTable(s)
  local ok, res = Serializer:Deserialize(s)
  if not ok then error(res) end
  return res
end

-- ============================================================================
-- UI
-- ============================================================================

function SkillWeaver:ToggleUI()
  if not self.frame then self:CreateMainFrame() end
  if self.frame:IsShown() then self.frame:Hide() else self.frame:Show() end
end

function SkillWeaver:CreateMainFrame()
  local frame = AceGUI:Create("Frame")
  frame:SetTitle("SkillWeaver")
  frame:SetStatusText("Offline-First Rotation Authoring")
  frame:SetCallback("OnClose", function(widget) widget:Hide() end)
  frame:SetLayout("Fill")
  frame:SetWidth(900)
  frame:SetHeight(650)

  local tabGroup = AceGUI:Create("TabGroup")
  tabGroup:SetLayout("Flow")
  tabGroup:SetTabs({
    {text="Profiles", value="profiles"},
    {text="Sequences", value="sequences"}
  })
  tabGroup:SetCallback("OnGroupSelected", function(container, event, group)
    container:ReleaseChildren()
    if group == "profiles" then
      SkillWeaver:DrawProfilesTab(container)
    elseif group == "sequences" then
      SkillWeaver:DrawSequencesTab(container)
    end
  end)

  frame:AddChild(tabGroup)
  tabGroup:SelectTab("profiles")

  self.frame = frame
end

-- ----------------------------------------------------------------------------
-- Profiles Tab
-- ----------------------------------------------------------------------------

function SkillWeaver:DrawProfilesTab(container)
  local btnNew = AceGUI:Create("Button")
  btnNew:SetText("New Profile")
  btnNew:SetWidth(150)
  btnNew:SetCallback("OnClick", function()
    local id = NewId()
    local _, class = UnitClass("player")

    self.db.profile.profiles[id] = {
      id = id,
      name = "New Profile",
      specId = 0,
      class = class,
      active = false,
    }

    container:ReleaseChildren()
    self:DrawProfilesTab(container)
  end)
  container:AddChild(btnNew)

  local tree = AceGUI:Create("TreeGroup")
  tree:SetLayout("Flow")
  tree:SetFullWidth(true)
  tree:SetFullHeight(true)
  tree:SetTreeWidth(220, false)

  local function RefreshTree()
    local t = {}
    for id, prof in pairs(self.db.profile.profiles) do
      local text = prof.name or ("Profile " .. id)
      if prof.active then text = "|cff00ff00" .. text .. "|r" end
      table.insert(t, {value = id, text = text})
    end
    table.sort(t, function(a,b) return a.text < b.text end)
    tree:SetTree(t)
  end

  local activeProfileId = nil

  local function DrawProfileEditor(group)
    group:ReleaseChildren()

    if not activeProfileId then
      local l = AceGUI:Create("Label")
      l:SetText("Select a profile to edit.")
      group:AddChild(l)
      return
    end

    local prof = self.db.profile.profiles[activeProfileId]
    if not prof then return end

    local nameEdit = AceGUI:Create("EditBox")
    nameEdit:SetLabel("Profile Name")
    nameEdit:SetText(prof.name or "")
    nameEdit:SetWidth(350)
    nameEdit:SetCallback("OnEnterPressed", function(_, _, text)
      prof.name = text
      RefreshTree()
    end)
    group:AddChild(nameEdit)

    local specEdit = AceGUI:Create("EditBox")
    specEdit:SetLabel("Spec ID (e.g., 62 Arcane Mage)")
    specEdit:SetText(tostring(prof.specId or 0))
    specEdit:SetWidth(220)
    specEdit:SetCallback("OnEnterPressed", function(_, _, t)
      prof.specId = tonumber(t) or 0
    end)
    group:AddChild(specEdit)

    -- Ensure new fields exist (back-compat)
    prof.content = prof.content or "openworld"
    prof.priority = tonumber(prof.priority) or 0

    -- Content dropdown (raid/mythic/delve/openworld/pvp)
    local contentDropdown = AceGUI:Create("Dropdown")
    contentDropdown:SetLabel("Content Context (auto-switch target)")
    contentDropdown:SetWidth(250)
    contentDropdown:SetList({
      openworld = "Open World",
      delve     = "Delve",
      mythic    = "Mythic+/Dungeon",
      raid      = "Raid",
      pvp       = "PvP",
    })
    contentDropdown:SetValue(prof.content)
    contentDropdown:SetCallback("OnValueChanged", function(_, _, key)
      prof.content = key
      -- Optional: if this profile is active, re-run autoswitch to confirm expected selection
      if self.AutoSelectProfile then self:AutoSelectProfile("ui_content_change") end
    end)
    group:AddChild(contentDropdown)

    -- Priority (higher wins among matches)
    local prioEdit = AceGUI:Create("EditBox")
    prioEdit:SetLabel("Priority (higher wins)")
    prioEdit:SetText(tostring(prof.priority or 0))
    prioEdit:SetWidth(150)
    prioEdit:SetCallback("OnEnterPressed", function(_, _, text)
      prof.priority = tonumber(text) or 0
    end)
    group:AddChild(prioEdit)

    -- Clone buttons: make 1-click copies for each context
    local cloneRow = AceGUI:Create("SimpleGroup")
    cloneRow:SetFullWidth(true)
    cloneRow:SetLayout("Flow")

    local function CloneToContext(ctxKey)
      local newId = tostring(math.random(1000000))
      local copy = {}
      for k, v in pairs(prof) do
        if k ~= "active" then copy[k] = v end
      end
      copy.name = (prof.name or "Profile") .. " (" .. ctxKey .. ")"
      copy.content = ctxKey
      copy.active = false
      self.db.profile.profiles[newId] = copy
      -- redraw tab so it appears immediately
      container:ReleaseChildren()
      self:DrawProfilesTab(container)
      self:Print("Cloned profile to context: " .. ctxKey)
    end

    local contexts = {
      {"openworld","OW"},
      {"delve","Delve"},
      {"mythic","M+"},
      {"raid","Raid"},
      {"pvp","PvP"},
    }

    for _, pair in ipairs(contexts) do
      local ctxKey, label = pair[1], pair[2]
      local b = AceGUI:Create("Button")
      b:SetText("Clone → " .. label)
      b:SetWidth(110)
      b:SetCallback("OnClick", function() CloneToContext(ctxKey) end)
      cloneRow:AddChild(b)
    end

    group:AddChild(cloneRow)

    -- (Optional but recommended) show current detection in editor
    if SkillWeaver.GetContentContextDebug then
      local l = AceGUI:Create("Label")
      l:SetText("Detected now: " .. SkillWeaver:GetContentContextDebug())
      l:SetFullWidth(true)
      group:AddChild(l)
    end

    local btnActive = AceGUI:Create("Button")
    btnActive:SetText(prof.active and "Active" or "Set Active")
    btnActive:SetWidth(150)
    btnActive:SetDisabled(prof.active)
    btnActive:SetCallback("OnClick", function()
      for _, p in pairs(self.db.profile.profiles) do p.active = false end
      prof.active = true
      self.db.profile.meta.last_profileId = prof.id
      RefreshTree()
      DrawProfileEditor(group)
      self:Print("Set active profile: " .. tostring(prof.name))
    end)
    group:AddChild(btnActive)

    local btnDel = AceGUI:Create("Button")
    btnDel:SetText("Delete Profile")
    btnDel:SetWidth(150)
    btnDel:SetCallback("OnClick", function()
      self.db.profile.profiles[activeProfileId] = nil
      activeProfileId = nil
      RefreshTree()
      tree:SelectByValue(nil)
    end)
    group:AddChild(btnDel)
  end

  tree:SetCallback("OnGroupSelected", function(_, _, uniquevalue)
    activeProfileId = uniquevalue
    DrawProfileEditor(tree)
  end)

  RefreshTree()
  container:AddChild(tree)
end

-- ----------------------------------------------------------------------------
-- Sequences Tab
-- ----------------------------------------------------------------------------

function SkillWeaver:DrawSequencesTab(container)
  local btnNew = AceGUI:Create("Button")
  btnNew:SetText("New Sequence")
  btnNew:SetWidth(150)
  btnNew:SetCallback("OnClick", function()
    local id = NewId()
    local prof = GetActiveProfile(self)
    local profileId = (prof and prof.id) or self.db.profile.meta.last_profileId

    self.db.profile.sequences[id] = {
      id = id,
      name = "New Sequence",
      profileId = profileId,
      stepsText = "",
      notes = "",
      content = "OPEN_WORLD",
      priority = 0,
      active = false,
      enabled = true,
      -- mode = (self.currentMode or "openworld"), -- Removed old field
```lua
    self.db.profile.meta.last_seqId = id
    container:ReleaseChildren()
    self:DrawSequencesTab(container)
  end)
  container:AddChild(btnNew)

  local tree = AceGUI:Create("TreeGroup")
  tree:SetLayout("Flow")
  tree:SetFullWidth(true)
  tree:SetFullHeight(true)
  tree:SetTreeWidth(220, false)

  local function RefreshTree()
    local t = {}
    for id, seq in pairs(self.db.profile.sequences) do
      local text = seq.name or ("Sequence " .. id)
      table.insert(t, {value = id, text = text})
    end
    table.sort(t, function(a,b) return a.text < b.text end)
    tree:SetTree(t)
  end

  local activeSeqId = nil

  local function DrawSeqEditor(group)
    group:ReleaseChildren()

    if not activeSeqId then
        local l = AceGUI:Create("Label")
        l:SetText("Select a sequence to edit.")
        group:AddChild(l)
        return
    end

    local seq = self.db.profile.sequences[activeSeqId]
    if not seq then return end

    -- Ensure schema + parsed steps
    self:EnsureSequenceDefaults(seq)
    if not seq.steps or type(seq.steps) ~= "table" or (#seq.steps == 0 and (seq.stepsText and seq.stepsText ~= "")) then
        self:RebuildSequence(seq)
    end

    -- Name
    local nameEdit = AceGUI:Create("EditBox")
    nameEdit:SetLabel("Sequence Name")
    nameEdit:SetText(seq.name or "")
    nameEdit:SetWidth(320)
    nameEdit:SetCallback("OnEnterPressed", function(_, _, text)
        seq.name = text
        RefreshTree()
    end)
    group:AddChild(nameEdit)

    -- >>> NEW: Profile selector (which profile this sequence belongs to)
    do
        local profDropdown = AceGUI:Create("Dropdown")
        profDropdown:SetLabel("Profile (sequence belongs to)")
        profDropdown:SetWidth(300)

        local list = {}
        for pid, prof in pairs(self.db.profile.profiles or {}) do
            list[pid] = prof.name or ("Profile " .. tostring(pid))
        end
        profDropdown:SetList(list)

        if seq.profileId and list[seq.profileId] then
            profDropdown:SetValue(seq.profileId)
        end

        profDropdown:SetCallback("OnValueChanged", function(_, _, val)
            seq.profileId = val
            self.db.profile.meta.last_profileId = val
            RefreshTree()
        end)
        group:AddChild(profDropdown)
    end

    -- >>> NEW: Content bucket selector
    do
        local contentDropdown = AceGUI:Create("Dropdown")
        contentDropdown:SetLabel("Content Type (for AutoSwitch)")
        contentDropdown:SetWidth(300)
        contentDropdown:SetList({
            OPEN_WORLD = "OPEN_WORLD",
            RAID = "RAID",
            MYTHIC_PLUS = "MYTHIC_PLUS",
            DUNGEON = "DUNGEON",
            DELVES = "DELVES",
            PVP = "PVP",
        })

        seq.contentType = (seq.contentType or "OPEN_WORLD"):upper()
        contentDropdown:SetValue(seq.contentType)

        contentDropdown:SetCallback("OnValueChanged", function(_, _, val)
            seq.contentType = tostring(val or "OPEN_WORLD"):upper()
        end)
        group:AddChild(contentDropdown)
    end

    -- >>> NEW: Priority editor (higher wins)
    do
        local prio = AceGUI:Create("EditBox")
        prio:SetLabel("Priority (higher wins within same content type)")
        prio:SetWidth(200)
        prio:SetText(tostring(seq.priority or 0))
        prio:SetCallback("OnEnterPressed", function(_, _, text)
            seq.priority = tonumber(text) or 0
        end)
        group:AddChild(prio)
    end

    -- Now REPLACE your existing "Steps (Multiline)" control with this version:
    do
        local stepsBox = AceGUI:Create("MultiLineEditBox")
        stepsBox:SetLabel("Steps (one per line)  Format: action | condition    (condition optional)")
        stepsBox:SetNumLines(15)
        stepsBox:SetFullWidth(true)

        -- Persist as text; parse into structured steps used by runtime
        seq.stepsText = seq.stepsText or ""
        stepsBox:SetText(seq.stepsText)

        stepsBox:SetCallback("OnTextChanged", function(_, _, text)
            -- Keep seq.stepsText current without needing EnterPressed (more reliable)
            seq.stepsText = text or ""
        end)

        stepsBox:SetCallback("OnEnterPressed", function(_, _, text)
            seq.stepsText = text or ""
            seq.steps = SkillWeaver:ParseSteps(seq.stepsText)
            SkillWeaver:Print("Sequence steps parsed & saved.")
        end)

        group:AddChild(stepsBox)
    end

    local btnRebuild = AceGUI:Create("Button")
    btnRebuild:SetText("Rebuild Steps Now")
    btnRebuild:SetWidth(160)
    btnRebuild:SetCallback("OnClick", function()
        self:RebuildSequence(seq)
        self:Print(("Rebuilt steps for: %s (%d steps)"):format(tostring(seq.name), #(seq.steps or {})))
    end)
    group:AddChild(btnRebuild)

    -- Set Active (manual override)
    local btnUse = AceGUI:Create("Button")
    btnUse:SetText("Use This Sequence")
    btnUse:SetWidth(160)
    btnUse:SetCallback("OnClick", function()
        self:SetActiveSequence(activeSeqId)
        self:Print("Active sequence set: " .. tostring(seq.name))
    end)
    group:AddChild(btnUse)

    -- Delete
    local btnDel = AceGUI:Create("Button")
    btnDel:SetText("Delete Sequence")
    btnDel:SetWidth(160)
    btnDel:SetCallback("OnClick", function()
        self.db.profile.sequences[activeSeqId] = nil
        activeSeqId = nil
        RefreshTree()
        tree:SelectByValue(nil)
    end)
    group:AddChild(btnDel)

    -- Export
    local btnExport = AceGUI:Create("Button")
    btnExport:SetText("Export")
    btnExport:SetWidth(100)
    btnExport:SetCallback("OnClick", function()
        local exportData = {
            type = "SkillWeaverSequence",
            version = 2,
            name = seq.name,
            contentType = seq.contentType,
            priority = seq.priority,
            stepsText = seq.stepsText or "",
            notes = seq.notes or "",
        }
        local jsonStr = self:TableToJSON(exportData)

        local popup = AceGUI:Create("Frame")
        popup:SetTitle("Export Sequence: " .. tostring(seq.name))
        popup:SetWidth(650)
        popup:SetHeight(320)
        popup:SetLayout("Fill")
        popup:SetCallback("OnClose", function(widget) AceGUI:Release(widget) end)

        local editBox = AceGUI:Create("MultiLineEditBox")
        editBox:SetLabel("Copy this string:")
        editBox:SetText(jsonStr)
        editBox:SetNumLines(10)
        editBox:SetFullWidth(true)
        editBox:DisableButton(true)
        popup:AddChild(editBox)
    end)
    group:AddChild(btnExport)

    -- Import (overwrites current seq)
    local btnImport = AceGUI:Create("Button")
    btnImport:SetText("Import String")
    btnImport:SetWidth(120)
    btnImport:SetCallback("OnClick", function()
        local popup = AceGUI:Create("Frame")
        popup:SetTitle("Import Sequence (overwrites selected)")
        popup:SetWidth(650)
        popup:SetHeight(360)
        popup:SetLayout("Flow")
        popup:SetCallback("OnClose", function(widget) AceGUI:Release(widget) end)

        local editBox = AceGUI:Create("MultiLineEditBox")
        editBox:SetLabel("Paste sequence string:")
        editBox:SetNumLines(12)
        editBox:SetFullWidth(true)
        editBox:DisableButton(true)
        popup:AddChild(editBox)

        local btnConfirm = AceGUI:Create("Button")
        btnConfirm:SetText("Import")
        btnConfirm:SetWidth(120)
        btnConfirm:SetCallback("OnClick", function()
            local importStr = editBox:GetText()
            local ok, data = pcall(self.JSONToTable, self, importStr)
            if ok and data and data.type == "SkillWeaverSequence" then
                seq.name = data.name or seq.name
                seq.contentType = (data.contentType or seq.contentType or "OPEN_WORLD"):upper()
                seq.priority = tonumber(data.priority) or (tonumber(seq.priority) or 0)
                seq.stepsText = data.stepsText or seq.stepsText or ""
                seq.notes = data.notes or seq.notes or ""

                self:EnsureSequenceDefaults(seq)
                self:RebuildSequence(seq)

                RefreshTree()
                group:ReleaseChildren()
                DrawSeqEditor(group)
                self:Print("Sequence imported!")
                popup:Hide()
            else
                self:Print("Import failed: invalid string.")
            end
        end)
        popup:AddChild(btnConfirm)
    end)
    group:AddChild(btnImport)
  end

  tree:SetCallback("OnGroupSelected", function(_, _, uniquevalue)
    activeSeqId = uniquevalue
    DrawSeqEditor(tree)
  end)

  RefreshTree()
  container:AddChild(tree)
end
