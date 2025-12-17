-- rotations/RotationStore.lua
local RotationStore = {}

local function deepCopy(t)
    if type(t) ~= "table" then return t end
    local o = {}
    for k,v in pairs(t) do o[k] = deepCopy(v) end
    return o
end

local function merge(dst, src)
    if type(src) ~= "table" then return dst end
    dst = dst or {}
    for k,v in pairs(src) do
        if type(v) == "table" and type(dst[k]) == "table" then
            merge(dst[k], v)
        else
            dst[k] = deepCopy(v)
        end
    end
    return dst
end

-- Always available (addon-shipped)
-- We use pcall here just in case the file is missing/broken during dev
local hasDefaults, LocalDefaults = pcall(require, "rotations.defaults.AllSpecs")
if not hasDefaults then LocalDefaults = {} end

local function getCached()
    SkillWeaver_RotationCache = SkillWeaver_RotationCache or { version=1, bundles={} }
    return SkillWeaver_RotationCache
end

function RotationStore:PutRemoteBundle(bundleId, data)
    local cache = getCached()
    cache.bundles[bundleId] = {
        t = time and time() or 0,
        data = data,
    }
    cache.lastBundleId = bundleId
end

function RotationStore:GetBest(specKey)
    -- 1) remote-loaded-in-session (optional)
    if self.remote and self.remote[specKey] then
        return deepCopy(self.remote[specKey]), "remote"
    end

    -- 2) cached bundle (SavedVariables)
    local cache = getCached()
    if cache.lastBundleId and cache.bundles[cache.lastBundleId] and cache.bundles[cache.lastBundleId].data then
        local b = cache.bundles[cache.lastBundleId].data
        if b[specKey] then return deepCopy(b[specKey]), "cached" end
    end

    -- 3) local defaults (always)
    if LocalDefaults and LocalDefaults[specKey] then
        return deepCopy(LocalDefaults[specKey]), "local"
    end

    return nil, "missing"
end

function RotationStore:BuildAll(specKeys)
    local out = {}
    for _, specKey in ipairs(specKeys) do
        local seq, source = self:GetBest(specKey)
        if seq then 
            out[specKey] = seq 
            -- print("Loaded sequence for " .. specKey .. " from " .. tostring(source))
        end
    end
    return out
end

return RotationStore
