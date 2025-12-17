local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")

-- Normalize content strings
local function NormalizeContent(c)
  c = tostring(c or ""):lower()
  if c == "mythic+" then return "mythic" end
  return c
end

-- Detect content context.
-- Return one of: "raid","mythic","delve","pvp","openworld"
function SkillWeaver:DetectContentContext()
  -- PVP (instanced)
  if IsActiveBattlefieldArena and IsActiveBattlefieldArena() then return "pvp" end
  if C_PvP and C_PvP.IsPVPMap and C_PvP.IsPVPMap() then return "pvp" end

  -- RAID
  if IsInRaid and IsInRaid() then
    -- If you're in a raid group, assume raid content
    return "raid"
  end

  -- PARTY / DUNGEON (treat as mythic bucket; we can refine later with Keystone data)
  local inInstance, instanceType = IsInInstance()
  if inInstance then
    if instanceType == "party" then
      -- Mythic+ detection hook: treat all party instances as mythic bucket for now
      return "mythic"
    elseif instanceType == "raid" then
      return "raid"
    elseif instanceType == "pvp" or instanceType == "arena" then
      return "pvp"
    end
  end

  -- DELVES: MVP fallback
  -- There isn't a single universal simple API across all builds; keep it conservative.
  -- If you later add a reliable Delve API check for your client, put it here.
  -- For now: never auto-detect "delve" unless a profile explicitly forces it by manual Set Active.
  -- return "delve"

  return "openworld"
end

-- Choose best profile given context.
function SkillWeaver:SelectBestProfileForContext(ctx)
  ctx = NormalizeContent(ctx)
  local bestId, bestScore = nil, -math.huge

  for id, prof in pairs(self.db.profile.profiles or {}) do
    local pctx = NormalizeContent(prof.content)
    local prio = tonumber(prof.priority) or 0

    -- Must match context to be eligible (MVP).
    -- If you want "fallback profile", set prof.content="openworld" and give it low priority.
    if pctx == ctx then
      local score = prio
      if score > bestScore then
        bestScore = score
        bestId = id
      end
    end
  end

  return bestId
end

-- Choose best sequence for a profile given context.
function SkillWeaver:SelectBestSequenceForProfile(profileId, ctx)
  if not profileId then return nil end
  ctx = NormalizeContent(ctx)

  local bestId, bestScore = nil, -math.huge
  for id, seq in pairs(self.db.profile.sequences or {}) do
    if seq.profileId == profileId then
      local sctx = NormalizeContent(seq.content) -- nil means "any"
      local prio = tonumber(seq.priority) or 0

      local eligible = (sctx == "" or sctx == nil or sctx == ctx)
      if eligible then
        local score = prio
        -- Prefer exact match over "any" if equal priority
        if sctx == ctx then score = score + 0.001 end
        if score > bestScore then
          bestScore = score
          bestId = id
        end
      end
    end
  end

  return bestId
end

-- Apply active flags safely.
function SkillWeaver:SetActiveProfile(profileId)
  if not (self.db and self.db.profile and self.db.profile.profiles) then return end
  for _, p in pairs(self.db.profile.profiles) do p.active = false end
  local prof = self.db.profile.profiles[profileId]
  if prof then
    prof.active = true
    self.db.profile.meta.last_profileId = profileId
  end
end

function SkillWeaver:AutoSelectProfile(reason)
  self.db.profile.settings = self.db.profile.settings or { debug=false, autoSwitch=true }
  if self.db.profile.settings.autoSwitch == false then return end

  local ctx = self:DetectContentContext()
  local pid = self:SelectBestProfileForContext(ctx)

  if pid then
    local currentActive = nil
    for id, p in pairs(self.db.profile.profiles or {}) do
      if p.active then currentActive = id break end
    end

    if currentActive ~= pid then
      self:SetActiveProfile(pid)
      if self.db.profile.settings.debug then
        self:Print(("AutoSwitch(%s): context=%s -> profile=%s"):format(tostring(reason), tostring(ctx), tostring(pid)))
      end
    end

    local sid = self:SelectBestSequenceForProfile(pid, ctx)
    if sid and self.db.profile.meta.last_seqId ~= sid then
      self.db.profile.meta.last_seqId = sid
      if self.db.profile.settings.debug then
        self:Print(("AutoSwitch(%s): context=%s -> sequence=%s"):format(tostring(reason), tostring(ctx), tostring(sid)))
      end
    end
  else
    if self.db.profile.settings.debug then
      self:Print(("AutoSwitch(%s): context=%s -> no matching profile"):format(tostring(reason), tostring(ctx)))
    end
  end
end

-- Event entrypoint (AceEvent)
function SkillWeaver:SW_OnContentEvent(event)
  self:AutoSelectProfile(event)
end
