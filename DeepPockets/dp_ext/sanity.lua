DeepPockets = DeepPockets or {}

function DeepPockets:Sanity()
    DeepPocketsDB = DeepPocketsDB or {}
    local ok = true
    local failures = 0

    -- Required DB shape (backend contract)
    DeepPocketsDB.version   = DeepPocketsDB.version   or "0.1.0-backend"
    DeepPocketsDB.settings  = DeepPocketsDB.settings  or {}
    DeepPocketsDB.inventory = DeepPocketsDB.inventory or {}
    DeepPocketsDB.index     = DeepPocketsDB.index     or { by_item = {}, by_category = {} }
    DeepPocketsDB.delta     = DeepPocketsDB.delta     or { last_seen = {}, is_new = {}, expire_at = {} }
    DeepPocketsDB.meta      = DeepPocketsDB.meta      or {}

    -- Checks (keep simple + deterministic)
    if type(DeepPocketsDB.inventory) ~= "table" then ok=false; failures=failures+1; print("DP SANITY FAIL: inventory not table") end
    if type(DeepPocketsDB.index) ~= "table" or type(DeepPocketsDB.index.by_item) ~= "table" or type(DeepPocketsDB.index.by_category) ~= "table" then
        ok=false; failures=failures+1; print("DP SANITY FAIL: index shape invalid")
    end
    if type(DeepPocketsDB.delta) ~= "table" or type(DeepPocketsDB.delta.is_new) ~= "table" then
        ok=false; failures=failures+1; print("DP SANITY FAIL: delta shape invalid")
    end

    if ok then
        print("|cff00FF00DP SANITY PASS|r")
        print(string.format('SANITY_RESULT {"addon":"DeepPockets","status":"OK","checks":3,"failures":0}'))
    else
        print("|cffff0000DP SANITY FAIL|r")
        print(string.format('SANITY_RESULT {"addon":"DeepPockets","status":"FAIL","checks":3,"failures":%d}', failures))
    end

    return ok
end
