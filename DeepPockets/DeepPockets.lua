-- ========================================================================
-- DEEPPOCKETS CORE (Backend Only)
-- Includes: Sanity Check, Tooltip Trace, Slash Handlers
-- ========================================================================

DeepPockets = DeepPockets or {}
DeepPocketsDB = DeepPocketsDB or {}
DeepPocketsDB.version = "0.1.0-backend"
DeepPocketsDB.settings = DeepPocketsDB.settings or {}
DeepPocketsDB.settings.tt_trace = DeepPocketsDB.settings.tt_trace or false

-- ========================================================================
-- 1. SANITY CHECK
-- ========================================================================
function DeepPockets:Sanity()
    DeepPocketsDB = DeepPocketsDB or {}
    local ok, failures, checks = true, 0, 0

    local function check(cond, msg)
        checks = checks + 1
        if not cond then
            ok = false
            failures = failures + 1
            print("|cffff0000DP SANITY FAIL|r: " .. msg)
        end
    end

    DeepPocketsDB.inventory = DeepPocketsDB.inventory or {}
    DeepPocketsDB.index     = DeepPocketsDB.index     or { by_item = {}, by_category = {} }
    DeepPocketsDB.delta     = DeepPocketsDB.delta     or { last_seen = {}, is_new = {}, expire_at = {} }
    DeepPocketsDB.meta      = DeepPocketsDB.meta      or {}

    check(type(DeepPocketsDB.inventory) == "table", "inventory not table")
    check(type(DeepPocketsDB.index) == "table"
        and type(DeepPocketsDB.index.by_item) == "table"
        and type(DeepPocketsDB.index.by_category) == "table", "index shape invalid")
    check(type(DeepPocketsDB.delta) == "table"
        and type(DeepPocketsDB.delta.is_new) == "table", "delta shape invalid")

    if ok then
        print("|cff00ff00DP SANITY PASS|r")
        print(string.format('SANITY_RESULT {"addon":"DeepPockets","status":"OK","checks":%d,"failures":0}', checks))
    else
        print("|cffff0000DP SANITY FAIL|r")
        print(string.format('SANITY_RESULT {"addon":"DeepPockets","status":"FAIL","checks":%d,"failures":%d}', checks, failures))
    end

    return ok
end

-- ========================================================================
-- 2. TOOLTIP TRACE
-- ========================================================================
function DeepPockets:ToggleTooltipTrace(force)
    if type(force) == "boolean" then
        DeepPocketsDB.settings.tt_trace = force
    else
        DeepPocketsDB.settings.tt_trace = not DeepPocketsDB.settings.tt_trace
    end

    local enabled = DeepPocketsDB.settings.tt_trace
    print("|cffDAA520DeepPockets|r: tooltip trace " .. (enabled and "|cff00ff00ON|r" or "|cffff0000OFF|r"))

    -- Lazy-hook only when enabled.
    if enabled and not self._tt_hooked then
        self._tt_hooked = true

        hooksecurefunc(GameTooltip, "SetOwner", function(_, owner, anchor)
            if not DeepPocketsDB.settings.tt_trace then return end
            local on = owner and owner.GetName and owner:GetName() or tostring(owner)
            print("|cff999999DP TT|r SetOwner owner=" .. tostring(on) .. " anchor=" .. tostring(anchor))
        end)

        hooksecurefunc(GameTooltip, "Hide", function()
            if not DeepPocketsDB.settings.tt_trace then return end
            print("|cff999999DP TT|r Hide()")
        end)

        -- Optional: trace item tooltips
        hooksecurefunc(GameTooltip, "SetBagItem", function(_, bag, slot)
            if not DeepPocketsDB.settings.tt_trace then return end
            print("|cff999999DP TT|r SetBagItem bag=" .. tostring(bag) .. " slot=" .. tostring(slot))
        end)
    end
end

-- ========================================================================
-- 3. SLASH HANDLER
-- ========================================================================
local function DP_PrintHelp()
    print("|cffDAA520DeepPockets|r backend " .. tostring(DeepPocketsDB.version))
    print("|cffDAA520/dp|r commands: scan, dump, debug, autoscan, sanity, tt")
end

SLASH_DEEPPOCKETS1 = "/dp"
SlashCmdList["DEEPPOCKETS"] = function(msg)
    msg = tostring(msg or "")
    local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
    cmd = cmd or "help"

    if cmd == "tt" then
        if arg == "on" then DeepPockets:ToggleTooltipTrace(true)
        elseif arg == "off" then DeepPockets:ToggleTooltipTrace(false)
        else DeepPockets:ToggleTooltipTrace()
        end
        return
    end

    if cmd == "cat" then
        if DeepPockets.CmdCategory then
            DeepPockets:CmdCategory(arg)
        else
            print("|cffff0000DeepPockets|r: category provider missing")
        end
        return
    end

    if cmd == "prov" then
        DeepPockets:CmdProv(arg)
        return
    end

    if cmd == "api" then
        DeepPockets:API_Sanity()
        return
    end

    if cmd == "sanity" and DeepPockets.Sanity then DeepPockets:Sanity(); return end
    
    if cmd == "scan" and DeepPockets.ScanBags then
        local count = DeepPockets:ScanBags()
        print("|cffDAA520DeepPockets|r: Scanned " .. tostring(count) .. " items.")
        return
    end

    if cmd == "dump" and DeepPockets.Dump then DeepPockets:Dump(arg); return end
    if cmd == "debug" and DeepPockets.ToggleDebug then DeepPockets:ToggleDebug(); return end
    if cmd == "autoscan" and DeepPockets.ToggleAutoScan then DeepPockets:ToggleAutoScan(); return end

    DP_PrintHelp()
end
