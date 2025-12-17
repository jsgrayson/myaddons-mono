-- policies/PolicyMerger.lua
local addonName, addonTable = ...
local Merger = {}
addonTable.PolicyMerger = Merger

local function isTable(x) return type(x) == "table" end

local function deepCopy(t)
  if not isTable(t) then return t end
  local out = {}
  for k,v in pairs(t) do out[k] = deepCopy(v) end
  return out
end

-- Check if path/key is locked
-- locks structure matching manual config: 
-- { __locks = { section = true, section2 = { key = true } } }
local function isLocked(locks, path, key)
  if not isTable(locks) then return false end
  local node = locks[path]
  
  -- Section lock: section=true
  if node == true then return true end
  
  -- Key lock: section={ key=true }
  if isTable(node) and key ~= nil and node[key] == true then return true end
  
  return false
end

local function mergeInto(dst, src)
  if not isTable(src) then return dst end
  if not isTable(dst) then dst = {} end

  for k, v in pairs(src) do
    if isTable(v) and v.__delete == true then
      dst[k] = nil
    else
      if isTable(v) and isTable(dst[k]) then
        dst[k] = mergeInto(dst[k], v)
      else
        dst[k] = deepCopy(v)
      end
    end
  end

  return dst
end

-- merge gen + manual, respecting manual.__locks
function Merger:Merge(defaults, gen, manual)
  defaults = defaults or {}
  gen = gen or {}
  manual = manual or {}

  local locks = manual.__locks or {}

  -- Start with defaults
  local out = deepCopy(defaults)

  -- Apply generated (Base layer)
  out = mergeInto(out, gen)

  -- Apply manual with locks logic
  for section, mval in pairs(manual) do
    if section ~= "__locks" then
      if isLocked(locks, section, nil) then
        -- Section is locked: Manual fully overrides, ignoring gen/defaults for this section
        out[section] = deepCopy(mval)
      else
        -- Section unlocked: Merge manual on top
        if isTable(mval) then
            -- Ensure dst section exists
            if not isTable(out[section]) then out[section] = {} end
            
            -- Prepare destination by reverting specific locked keys if needed? 
            -- Actually locks mean "Manual value MUST be used".
            -- Standard merge overrides anyway, locks just signal INTENT or prevent external tools from overwriting (which happens at file level).
            -- Runtime merge: manual beats gen naturally. 
            -- But getting "locking" behavior usually implies "Don't let Gen overwrite Manual". 
            -- Here, since we overlay Manual ON TOP of Gen, Manual always wins collisions.
            -- The 'locks' table is mostly for the external tool to know not to touch manual file (handled by separate files).
            -- However, user specifically asked for "Merge rules: Manual wins for any locked area... If scalar conflicts: manual overrides".
            -- This function does exactly that: Manual is applied LAST.
            
            out[section] = mergeInto(out[section], mval)
        else
            out[section] = deepCopy(mval)
        end
      end
    end
  end

  return out
end

return Merger
