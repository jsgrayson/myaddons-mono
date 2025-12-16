-- dp_ext/provenance_api.lua
-- Backend-only: stable provenance API (safe defaults).
-- Returns: "loot"|"craft"|"quest"|"vendor"|"drop"|"unknown"
-- Does NOT attempt protected actions; does NOT hook bags/UI.

DeepPockets = DeepPockets or {}
DeepPockets.API = DeepPockets.API or {}

local DP = DeepPockets
local API = DP.API

local VALID = {
  loot = true, craft = true, quest = true, vendor = true, drop = true, unknown = true,
}

local function norm(tag)
  if type(tag) ~= "string" then return nil end
  tag = tag:lower()
  return VALID[tag] and tag or nil
end

local function getOverrides()
  DeepPocketsDB = DeepPocketsDB or {}
  DeepPocketsDB.provenanceOverrides = DeepPocketsDB.provenanceOverrides or {}
  return DeepPocketsDB.provenanceOverrides
end

-- Very conservative heuristic: only mark quest items; everything else unknown.
local function heuristic(itemID)
  if not itemID then return "unknown" end
  local _, _, _, _, _, classID = C_Item.GetItemInfoInstant(itemID)
  if classID == 12 then return "quest" end
  return "unknown"
end

function API.GetItemProvenance(itemID, itemLink)
  itemID = tonumber(itemID)
  if not itemID then return "unknown" end

  local ov = norm(getOverrides()[itemID])
  if ov then return ov end

  return heuristic(itemID)
end

function API.SetItemProvenanceOverride(itemID, tag)
  itemID = tonumber(itemID)
  tag = norm(tag)
  if not itemID or not tag then return false end
  getOverrides()[itemID] = tag
  return true
end

function API.ClearItemProvenanceOverride(itemID)
  itemID = tonumber(itemID)
  if not itemID then return false end
  getOverrides()[itemID] = nil
  return true
end
