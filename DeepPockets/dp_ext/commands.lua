SLASH_DEEPPOCKETS1 = "/dp"
SLASH_DEEPPOCKETS2 = "/dpb"
SlashCmdList["DEEPPOCKETS"] = function(msg)
  msg = tostring(msg or "")
  local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
  cmd = cmd or ""

  if cmd == "" or cmd == "help" then
    print("|cffDAA520DeepPockets|r backend " .. (DeepPockets and DeepPockets.VERSION or "?"))
    print("Commands: /dp scan | /dp dump | /dp autoscan on|off | /dp debug on|off | /dp sanity")
    return
  end

  if cmd == "scan" then
    DeepPocketsAPI.Scan(false)
    return
  end

  if cmd == "dump" then
    local db = DeepPocketsDB
    local inv = db and db.inventory and #db.inventory or 0
    local cats = 0
    if db and db.index and db.index.by_category then
      for _ in pairs(db.index.by_category) do cats = cats + 1 end
    end
    print("DP DUMP: inv=" .. inv .. " cats=" .. cats .. " last_scan=" .. tostring(db and db.meta and db.meta.last_scan))
    return
  end

  if cmd == "autoscan" then
    if not DeepPocketsDB then return end
    if arg == "on" then DeepPocketsDB.settings.autoscan = true
    elseif arg == "off" then DeepPocketsDB.settings.autoscan = false
    else DeepPocketsDB.settings.autoscan = not DeepPocketsDB.settings.autoscan end
    print("|cffDAA520DeepPockets|r: autoscan=" .. tostring(DeepPocketsDB.settings.autoscan))
    return
  end

  if cmd == "debug" then
    if not DeepPocketsDB then return end
    if arg == "on" then DeepPocketsDB.settings.debug = true
    elseif arg == "off" then DeepPocketsDB.settings.debug = false
    else DeepPocketsDB.settings.debug = not DeepPocketsDB.settings.debug end
    print("|cffDAA520DeepPockets|r: debug=" .. tostring(DeepPocketsDB.settings.debug))
    return
  end

  if cmd == "sanity" then
    if not DeepPocketsDB or not DeepPocketsDB.index then return end
    local invCount = DeepPocketsDB.inventory and #DeepPocketsDB.inventory or 0
    local idxCount = 0
    if DeepPocketsDB.index.by_category then
      for _, list in pairs(DeepPocketsDB.index.by_category) do
        idxCount = idxCount + #list
      end
    end
    if invCount == idxCount then
      print("|cff00FF00DP SANITY PASS|r")
    else
      print("|cffff0000DP SANITY FAIL|r inv="..invCount.." index="..idxCount)
    end
    return
  end

  print("|cffDAA520DeepPockets|r: unknown command. /dp help")
end
