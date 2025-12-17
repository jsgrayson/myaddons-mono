-- engine/ReplayContext.lua
local addonName, addonTable = ...
local Replay = {}
addonTable.ReplayContext = Replay -- Expose internally
-- Will need Store, which is in addonTable or global
local Store = addonTable.SnapshotStore

function Replay:IsEnabled()
  return SkillWeaver_Replay and SkillWeaver_Replay.enabled == true
end

function Replay:Start(source)
  SkillWeaver_Replay = SkillWeaver_Replay or {}
  SkillWeaver_Replay.enabled = true
  SkillWeaver_Replay.idx = 1
  SkillWeaver_Replay.source = source or "snapshots"
end

function Replay:Stop()
  SkillWeaver_Replay = SkillWeaver_Replay or {}
  SkillWeaver_Replay.enabled = false
end

-- Returns (contextOverride, expectedCommand) or nil if no more frames
function Replay:Next()
  -- If Store not loaded yet (e.g. strict load order), try fetch
  if not Store then Store = addonTable.SnapshotStore end
  if not self:IsEnabled() then return nil end
  
  local idx = SkillWeaver_Replay.idx or 1
  local snap = nil
  
  if SkillWeaver_Replay.source == "packet" then
      -- Packet Source
      if not self.packetItems then
         local Packet = addonTable.ReplayPacket
         if Packet then 
             self.packetItems = Packet:GetItems() 
         end
      end
      if self.packetItems then
          snap = self.packetItems[idx]
      end
  else
      -- Snapshot Store Source
      if Store then
          snap = Store:Get(idx)
      end
  end

  if not snap then
    -- Reset packet cache just in case
    self.packetItems = nil
    self:Stop()
    return nil
  end

  SkillWeaver_Replay.idx = idx + 1

  -- Build a context that matches what the engine expects
  local ctx = {
    -- specKey = snap.specKey,
    -- profileName = snap.profile,
    -- variantName = snap.variant,

    activeEnemies = snap.enemies,
    aoeThreshold = 3, -- Default, or capture?
    isBoss = snap.isBoss,
    targetTTD = snap.ttd,

    runicPower = snap.rp,

    procs = {
      ["Killing Machine"] = snap.procs and snap.procs.KM or (snap.KM), -- Handle packet flattened format
      ["Rime"] = snap.procs and snap.procs.Rime or (snap.Rime),
      ["Sudden Doom"] = snap.procs and snap.procs.SD or (snap.SD),
    },

    -- Replay flags to prevent loops
    __replay = true,
  }

  return ctx, snap.chosen
end

return Replay
