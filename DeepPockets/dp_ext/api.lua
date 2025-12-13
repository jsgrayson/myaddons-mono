-- dp_ext/api.lua
local ADDON_NAME, ns = ...
local DP = _G.DeepPockets
DP.API = {}

local listeners = {}

function DP.API.NotifyListeners(event)
    for _, fn in ipairs(listeners) do
        pcall(fn, event)
    end
end

-- Public Contract

function DP.API.GetVersion()
    return DeepPocketsDB and DeepPocketsDB.version or 0
end

function DP.API.ScanNow(opts)
    if not DP.API.IsEnabled() then
        return false, "disabled"
    end
    
    local success, count = pcall(DP.Scanner.ScanBags)
    if not success then return false, count end -- count is err msg here
    
    DP.Index.Rebuild()
    return true, nil
end

function DP.API.GetIndex()
    DP.Migrate.Ensure()
    return DeepPocketsDB.index
end

function DP.API.GetItem(itemKey)
    DP.Migrate.Ensure()
    return DeepPocketsDB.inventory[itemKey]
end

function DP.API.Subscribe(fn)
    if type(fn) ~= "function" then return function() end end
    table.insert(listeners, fn)
    return function()
        for i, f in ipairs(listeners) do
            if f == fn then
                table.remove(listeners, i)
                break
            end
        end
    end
end

function DP.API.IsEnabled()
    DP.Migrate.Ensure()
    return DeepPocketsDB.settings.enabled
end

function DP.API.SetEnabled(bool)
    DP.Migrate.Ensure()
    DeepPocketsDB.settings.enabled = bool
end
