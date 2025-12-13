-- dp_ext/util.lua
local ADDON_NAME, ns = ...
local DP = _G.DeepPockets
DP.Util = {}

function DP.Util.ItemKey(bag, slot)
    return bag .. ":" .. slot
end

function DP.Util.SafeCall(func, ...)
    local ok, res = pcall(func, ...)
    if not ok then
        if DP.API and DP.API.DPrint then
             DP.API.DPrint("Error: " .. tostring(res))
        end
        return nil
    end
    return res
end

-- Debounce: returns a function that, when called, waits 'delay' seconds 
-- before executing 'func'. If called again, timer resets.
function DP.Util.Debounce(func, delay)
    local timer
    return function(...)
        local args = {...}
        if timer then timer:Cancel() end
        timer = C_Timer.NewTimer(delay, function()
            func(unpack(args))
        end)
    end
end
