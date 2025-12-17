-- engine/ReplayPacket.lua
local addonName, addonTable = ...
local Packet = {}
addonTable.ReplayPacket = Packet

-- Very small parser for our compact JSON-like objects.
-- This is intentionally limited; it just extracts known keys.
local function parseItems(raw)
  local items = {}
  local body = raw:match("%[(.*)%]$")
  if not body then return items end

  for obj in body:gmatch("{(.-)}") do
    local s = {}

    s.specKey  = obj:match('"spec":"(.-)"') or ""
    s.profile  = obj:match('"p":"(.-)"') or ""
    s.variant  = obj:match('"v":"(.-)"') or ""
    s.enemies  = tonumber(obj:match('"e":([%d%-%.]+)')) or 0
    s.isBoss   = obj:match('"b":(true)') ~= nil
    local ttd  = obj:match('"ttd":([%d%-%.]+)')
    s.ttd      = ttd and tonumber(ttd) or nil
    s.rp       = tonumber(obj:match('"rp":([%d%-%.]+)')) or 0
    s.KM       = obj:match('"KM":(true)') ~= nil
    s.Rime     = obj:match('"R":(true)') ~= nil
    s.SD       = obj:match('"SD":(true)') ~= nil
    s.chosen   = obj:match('"c":"(.-)"') or ""

    items[#items+1] = s
  end

  return items
end

function Packet:GetItems()
  if not SkillWeaver_ReplayPacket then return nil end
  return parseItems(SkillWeaver_ReplayPacket)
end

return Packet
