-- utils/ReplayExport.lua
local addonName, addonTable = ...
local Export = {}
addonTable.ReplayExport = Export

local Base64 = addonTable.Base64
local Store  = addonTable.SnapshotStore

-- Simple serializer (safe subset). Keeps it deterministic and tiny.
local function esc(s)
  s = tostring(s or "")
  s = s:gsub("\\","\\\\"):gsub("\n","\\n"):gsub("\r","\\r"):gsub("\"","\\\"")
  return s
end

local function serializeSnapshot(s)
  -- Only export what replay needs; keep small
  return string.format(
    '{"spec":"%s","p":"%s","v":"%s","e":%d,"b":%s,"ttd":%s,"rp":%d,"KM":%s,"R":%s,"SD":%s,"c":"%s"}',
    esc(s.specKey),
    esc(s.profile),
    esc(s.variant),
    tonumber(s.enemies or 0),
    s.isBoss and "true" or "false",
    (s.ttd ~= nil) and tostring(s.ttd) or "null",
    tonumber(s.rp or 0),
    (s.procs and s.procs.KM) and "true" or "false",
    (s.procs and s.procs.Rime) and "true" or "false",
    (s.procs and s.procs.SD) and "true" or "false",
    esc(s.chosen)
  )
end

local function serializePacket(items)
  local parts = { "SWREPLAY|v1|count="..#items }
  parts[#parts+1] = "["
  for i=1,#items do
    parts[#parts+1] = serializeSnapshot(items[i])
    if i < #items then parts[#parts+1] = "," end
  end
  parts[#parts+1] = "]"
  return table.concat(parts)
end

function Export:MakeChunks(maxItems, chunkLen)
  if not Store then Store = addonTable.SnapshotStore end
  if not Base64 then Base64 = addonTable.Base64 end
  
  maxItems = tonumber(maxItems) or 120
  chunkLen = tonumber(chunkLen) or 220

  local items = {}
  local n = Store:Count()
  local start = math.max(1, n - maxItems + 1)

  for i=start,n do
    items[#items+1] = Store:Get(i)
  end

  local payload = serializePacket(items)
  local b64 = Base64:Encode(payload)

  local chunks = {}
  local total = math.ceil(#b64 / chunkLen)
  for i=1,total do
    local a = (i-1)*chunkLen + 1
    local z = math.min(i*chunkLen, #b64)
    local piece = b64:sub(a, z)
    chunks[#chunks+1] = string.format("SWREPLAY_CHUNK|%d/%d|%s", i, total, piece)
  end

  return chunks, #items
end

-- Import buffer lives in SavedVariables so reloads won't lose it
function Export:ImportLine(line)
  if type(line) ~= "string" then return false end
  if not line:find("^SWREPLAY_CHUNK|") then return false end

  SkillWeaver_ReplayImport = SkillWeaver_ReplayImport or { total=nil, got={}, parts={} }

  local _, _, idx, total, payload = line:find("^SWREPLAY_CHUNK|(%d+)/(%d+)|(.+)$")
  idx, total = tonumber(idx), tonumber(total)
  if not idx or not total or not payload then return false end

  -- Reset if total changes (new import started implicitly?) 
  -- Or just trust user to use /swimport consistently.
  if SkillWeaver_ReplayImport.total and SkillWeaver_ReplayImport.total ~= total then
       -- New import session detected?
       SkillWeaver_ReplayImport = { total=total, got={}, parts={} }
  end
  SkillWeaver_ReplayImport.total = total

  if not SkillWeaver_ReplayImport.got[idx] then
    SkillWeaver_ReplayImport.got[idx] = true
    SkillWeaver_ReplayImport.parts[idx] = payload
  end

  return true
end

function Export:FinalizeImport()
  if not Base64 then Base64 = addonTable.Base64 end
  local buf = SkillWeaver_ReplayImport
  if not buf or not buf.total then return nil, "no_import" end

  for i=1,buf.total do
    if not buf.parts[i] then
      return nil, ("missing_chunk_%d"):format(i)
    end
  end

  local b64 = table.concat(buf.parts)
  local raw = Base64:Decode(b64)

  -- raw begins with SWREPLAY|v1|count=...
  if not raw:find("^SWREPLAY|v1|") then
    return nil, "bad_header"
  end

  -- Store raw packet for replay module to parse (simple approach)
  SkillWeaver_ReplayPacket = raw

  -- clear import buffer
  SkillWeaver_ReplayImport = nil

  return raw
end

return Export
