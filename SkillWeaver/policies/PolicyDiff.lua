-- policies/PolicyDiff.lua
local addonName, addonTable = ...
local Diff = {}
addonTable.PolicyDiff = Diff

local function isTable(x) return type(x) == "table" end

local function keyset(t)
  local s = {}
  for k,_ in pairs(t or {}) do
    if k ~= "__locks" then s[k] = true end
  end
  return s
end

local function toString(v)
  if v == nil then return "nil" end
  if type(v) == "boolean" then return v and "true" or "false" end
  if type(v) == "number" then return tostring(v) end
  if type(v) == "string" then
    if #v > 70 then return '"' .. v:sub(1,70) .. '..."' end
    return '"' .. v .. '"'
  end
  if isTable(v) then return "{...}" end
  return tostring(v)
end

-- Returns { added={}, removed={}, changed={} }
-- changed entries: { path="a.b", from=..., to=... }
function Diff:Compute(oldT, newT, basePath, out)
  basePath = basePath or ""
  out = out or { added={}, removed={}, changed={} }

  if oldT == nil and newT == nil then return out end
  if not isTable(oldT) or not isTable(newT) then
    if oldT ~= newT then
      table.insert(out.changed, { path=basePath, from=oldT, to=newT })
    end
    return out
  end

  local keys = keyset(oldT)
  for k,_ in pairs(keyset(newT)) do keys[k] = true end

  for k,_ in pairs(keys) do
    local p = (basePath == "" and tostring(k) or (basePath .. "." .. tostring(k)))
    local ov = oldT[k]
    local nv = newT[k]

    if ov == nil and nv ~= nil then
      table.insert(out.added, { path=p, to=nv })
    elseif ov ~= nil and nv == nil then
      table.insert(out.removed, { path=p, from=ov })
    else
      if isTable(ov) and isTable(nv) then
        self:Compute(ov, nv, p, out)
      elseif ov ~= nv then
        table.insert(out.changed, { path=p, from=ov, to=nv })
      end
    end
  end

  return out
end

function Diff:Format(result, limit)
  limit = limit or 40
  local lines = {}

  local function addSection(title, items, fmt)
    if #items == 0 then return end
    lines[#lines+1] = title .. " (" .. #items .. "):"
    local n = math.min(#items, limit)
    for i=1,n do
      lines[#lines+1] = "  " .. fmt(items[i])
    end
    if #items > limit then
      lines[#lines+1] = ("  ...and %d more"):format(#items - limit)
    end
  end

  addSection("ADDED", result.added, function(x)
    return x.path .. " = " .. toString(x.to)
  end)

  addSection("REMOVED", result.removed, function(x)
    return x.path .. " (was " .. toString(x.from) .. ")"
  end)

  addSection("CHANGED", result.changed, function(x)
    return x.path .. ": " .. toString(x.from) .. " -> " .. toString(x.to)
  end)

  if #lines == 0 then
    lines[#lines+1] = "No changes."
  end

  return lines
end

return Diff
