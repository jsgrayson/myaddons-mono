-- ui/PolicyPanel.lua
local addonName, addonTable = ...
local PolicyPanel = {}
addonTable.PolicyPanel = PolicyPanel

local PolicyManager = addonTable.PolicyManager
local Explain = addonTable.PolicyExplain
local PolicySnapshot = addonTable.PolicySnapshot
local PolicyDiff = addonTable.PolicyDiff
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")

PolicyPanel.frame = nil
PolicyPanel.rows = {}
PolicyPanel.tree = nil
PolicyPanel.view = {}
PolicyPanel.expanded = {} -- path -> bool

local function isTable(x) return type(x) == "table" end

local function currentSpecKey()
  return SkillWeaver:GetCurrentSpecKey()
end

local function color(txt, r, g, b)
  return ("|cff%02x%02x%02x%s|r"):format(r*255, g*255, b*255, txt)
end

local function badgeSource(defv, genv, manv)
  if manv ~= nil then return color("M", 0.20, 0.85, 0.20) end
  if genv ~= nil then return color("G", 0.25, 0.60, 1.00) end
  return color("D", 0.75, 0.75, 0.75)
end

local function fmtValue(v)
  if v == nil then return color("nil", 0.7, 0.7, 0.7) end
  if type(v) == "boolean" then return v and color("true", 0.2, 0.9, 0.2) or color("false", 0.9, 0.2, 0.2) end
  if type(v) == "number" then return tostring(v) end
  if type(v) == "string" then
    if #v > 54 then v = v:sub(1, 54) .. "..." end
    return '"' .. v .. '"'
  end
  if isTable(v) then return "{...}" end
  return tostring(v)
end

local function getAtPath(t, path)
  if not path or path == "" then return t end
  local cur = t
  for key in path:gmatch("[^%.]+") do
    if type(cur) ~= "table" then return nil end
    cur = cur[key]
  end
  return cur
end

local function sortedKeys(t)
  local keys = {}
  for k,_ in pairs(t or {}) do
    if k ~= "__locks" then keys[#keys+1] = k end
  end
  table.sort(keys, function(a,b) return tostring(a) < tostring(b) end)
  return keys
end

local function buildTree(specKey)
  -- Ensure loaded
  if not PolicyManager then PolicyManager = addonTable.PolicyManager end
  if not Explain then Explain = addonTable.PolicyExplain end

  local merged = PolicyManager:Get(specKey)
  local root = { path="", key="policy", depth=0, children={}, isTable=true }

  local function walk(node, parent, path, depth)
    if type(node) ~= "table" then return end
    for _, k in ipairs(sortedKeys(node)) do
      local childPath = (path == "" and tostring(k) or (path .. "." .. tostring(k)))
      local v = node[k]
      local isT = type(v) == "table"
      local why = Explain:Why(specKey, childPath)
      local item = {
        path = childPath,
        key = tostring(k),
        depth = depth,
        isTable = isT,
        why = why,
        locked = why.locked == true,
        children = {},
      }
      parent.children[#parent.children+1] = item
      if isT then
        walk(v, item, childPath, depth + 1)
      end
    end
  end

  walk(merged, root, "", 1)
  return root
end

local function defaultExpanded(path)
  return path:find("%.") == nil
end

-- Jump to Path logic
function PolicyPanel:JumpToPath(path)
  if not path or path == "" then return end

  -- Expand all ancestors
  local acc = {}
  for part in path:gmatch("[^%.]+") do
    acc[#acc+1] = part
    local p = table.concat(acc, ".")
    self.expanded[p] = true
  end

  -- Update view and scroll
  self:BuildView()
  
  -- Find index of target path in view
  local targetIdx = nil
  for i, node in ipairs(self.view) do
    if node.item and node.item.path == path then
      targetIdx = i
      break
    end
  end
  
  if targetIdx then
      local rowH = 20
      local offset = (targetIdx-1) * rowH
      -- Clamp
      local maxScroll = math.max(0, self.frame.content:GetHeight() - self.frame.scroll:GetHeight())
      if offset > maxScroll then offset = maxScroll end
      self.frame.scroll:SetVerticalScroll(offset)
      self:Refresh() -- Refresh to update row positions
  end
end


-- Builds Policy Tree View
function PolicyPanel:BuildView()
  local specKey = currentSpecKey()
  if not specKey then self.view = {}; return end
  
  self.tree = buildTree(specKey)

  local filter = (self.frame.search:GetText() or ""):lower()
  local leavesOnly = self.frame.leavesOnly and self.frame.leavesOnly:GetChecked()

  local merged = PolicyManager:Get(specKey)
  local view = {}

  local function matches(item)
    if filter == "" then return true end
    return item.path:lower():find(filter, 1, true) ~= nil
  end

  local function isExpanded(path)
    if self.expanded[path] == nil then
      self.expanded[path] = defaultExpanded(path)
    end
    return self.expanded[path] == true
  end

  local function addNode(item)
    local v = getAtPath(merged, item.path)
    local show = matches(item)
    if leavesOnly and item.isTable then show = false end
    
    if show then
      view[#view+1] = { item=item, value=v }
    end

    if item.isTable and isExpanded(item.path) then
      for _, ch in ipairs(item.children) do
        addNode(ch)
      end
    end
  end

  for _, ch in ipairs(self.tree.children) do
    addNode(ch)
  end

  self.view = view
end


-- Builds Diff List View
function PolicyPanel:BuildDiffView()
  local specKey = currentSpecKey()
  if not specKey then return {} end
  
  if not PolicySnapshot then PolicySnapshot = addonTable.PolicySnapshot end
  if not PolicyDiff then PolicyDiff = addonTable.PolicyDiff end

  local prev = PolicySnapshot:Get(specKey)
  if not prev then
    return {
      { kind="info", text="No snapshot saved. Click 'Save Snapshot' first." }
    }
  end

  local cur = PolicyManager:Get(specKey)
  local d = PolicyDiff:Compute(prev, cur)

  local items = {}

  local function addLine(kind, path, fromV, toV)
    items[#items+1] = { kind=kind, path=path, from=fromV, to=toV }
  end
  
  local function addHeader(txt)
    items[#items+1] = { kind="header", text=txt }
  end

  local mode = self.frame.diffMode or "changed"

  if mode == "all" or mode == "added" then
    if #d.added > 0 then
      addHeader(("ADDED (%d)"):format(#d.added))
      for _, it in ipairs(d.added) do addLine("added", it.path, nil, it.to) end
    end
  end

  if mode == "all" or mode == "removed" then
    if #d.removed > 0 then
      addHeader(("REMOVED (%d)"):format(#d.removed))
      for _, it in ipairs(d.removed) do addLine("removed", it.path, it.from, nil) end
    end
  end

  if mode == "all" or mode == "changed" then
    if #d.changed > 0 then
      addHeader(("CHANGED (%d)"):format(#d.changed))
      for _, it in ipairs(d.changed) do addLine("changed", it.path, it.from, it.to) end
    end
  end

  if #items == 0 then
    items[#items+1] = { kind="info", text="No changes." }
  end

  return items
end


local function copyToClipboard(text)
  if not PolicyPanel.frame then return end
  local box = PolicyPanel.frame.copyBox
  if not box then return end
  box:SetText(text)
  box:HighlightText()
  box:SetFocus()
end

function PolicyPanel:Refresh()
  if not self.frame or not self.frame:IsShown() then return end
  local specKey = currentSpecKey()
  local tab = self.frame.activeTab or "policy"
  
  self.frame.title:SetText(specKey and ("SkillWeaver Policy Inspector - " .. specKey) or "SkillWeaver Policy Inspector")
  
  -- Toggle UI elements visibility based on tab
  if tab == "diff" then
      self.frame.search:Hide()
      self.frame.leavesOnly:Hide()
      self.frame.saveSnap:Show()
      self.frame.diffAllBtn:Show()
      self.frame.diffChgBtn:Show()
      self.frame.diffAddBtn:Show()
      self.frame.diffRemBtn:Show()
  else
      self.frame.search:Show()
      self.frame.leavesOnly:Show()
      self.frame.saveSnap:Hide()
      self.frame.diffAllBtn:Hide()
      self.frame.diffChgBtn:Hide()
      self.frame.diffAddBtn:Hide()
      self.frame.diffRemBtn:Hide()
  end

  local viewList = {}
  
  if tab == "policy" then
      self:BuildView()
      viewList = self.view -- built above
  elseif tab == "diff" then
      viewList = self:BuildDiffView()
      -- self.view stores current list for scrolling logic
      self.view = viewList 
  end

  -- Resize content
  local rowH = 20
  local totalH = math.max(1, #viewList * rowH)
  self.frame.content:SetHeight(totalH)

  local scroll = self.frame.scroll:GetVerticalScroll() or 0
  local maxScroll = math.max(0, totalH - self.frame.scroll:GetHeight())
  if scroll > maxScroll then scroll = maxScroll end 
  
  local first = math.floor(scroll / rowH) + 1
  local ROWS = #self.rows

  for i=1,ROWS do
    local idx = first + (i-1)
    local row = self.rows[i]
    local node = viewList[idx] -- use the list we just built
    
    if node then
      row:SetPoint("TOPLEFT", 0, -((idx-1) * rowH))
      row:Show()
      
      if tab == "policy" then
          -- POLICY RENDER
          local item, value = node.item, node.value
          row.item = item
          row.__diff = nil -- clear diff ref

          local indent = string.rep("  ", item.depth)
          local tri = ""
          if item.isTable then
            local open = self.expanded[item.path]
            if open == nil then open = defaultExpanded(item.path) end
            tri = open and color("v", 0.9, 0.9, 0.9) or color(">", 0.9, 0.9, 0.9)
            tri = tri .. " "
          else
            tri = "  "
          end

          local src = badgeSource(item.why.default, item.why.gen, item.why.manual)
          local lock = item.locked and (color("L", 1.0, 0.85, 0.2) .. " ") or ""
          row.text:SetText(("%s%s%s%s %s = %s"):format(indent, tri, lock, src .. " ", item.key .. " ", fmtValue(value)))
      
      elseif tab == "diff" then
          -- DIFF RENDER
          row.item = nil
          local it = node -- the diff item
          
          if it.kind == "header" then
            row.text:SetText(color(it.text, 1.0, 0.85, 0.2))
            row.__diff = { kind="header" }
          elseif it.kind == "info" then
            row.text:SetText(color(it.text, 0.8, 0.8, 0.8))
            row.__diff = { kind="info" }
          else
            -- diff line
            row.__diff = it
            local label =
              (it.kind == "added" and color("+", 0.2, 0.9, 0.2)) or
              (it.kind == "removed" and color("-", 0.9, 0.3, 0.3)) or
              color("~", 0.25, 0.60, 1.0)
    
            local fromS = it.from ~= nil and fmtValue(it.from) or ""
            local toS = it.to ~= nil and fmtValue(it.to) or ""
    
            local rhs = ""
            if it.kind == "added" then rhs = "= " .. toS
            elseif it.kind == "removed" then rhs = "(was " .. fromS .. ")"
            else rhs = fromS .. " -> " .. toS end
    
            row.text:SetText(("%s %s  %s"):format(label, it.path, rhs))
          end
      end
    
    else
      row.item = nil
      row:Hide()
    end
  end
end

function PolicyPanel:ToggleExpand(path)
  if not path or path == "" then return end
  if self.expanded[path] == nil then self.expanded[path] = defaultExpanded(path) end
  self.expanded[path] = not self.expanded[path]
  self:Refresh()
end

function PolicyPanel:Create()
  if self.frame then return end

  local f = CreateFrame("Frame", "SkillWeaverPolicyPanel", UIParent, "BackdropTemplate")
  f:SetSize(740, 460)
  f:SetPoint("CENTER")
  f:SetMovable(true); f:EnableMouse(true)
  f:RegisterForDrag("LeftButton")
  f:SetScript("OnDragStart", f.StartMoving)
  f:SetScript("OnDragStop", f.StopMovingOrSizing)
  f:SetBackdrop({
    bgFile="Interface/Tooltips/UI-Tooltip-Background",
    edgeFile="Interface/Tooltips/UI-Tooltip-Border",
    tile=true, tileSize=16, edgeSize=16,
    insets={left=4,right=4,top=4,bottom=4}
  })
  f:SetBackdropColor(0,0,0,0.92)

  f.title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
  f.title:SetPoint("TOPLEFT", 12, -10)
  f.title:SetText("SkillWeaver Policy Inspector")

  local close = CreateFrame("Button", nil, f, "UIPanelCloseButton")
  close:SetPoint("TOPRIGHT", -4, -4)
  
  -- Tabs
  f.tabPolicy = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.tabPolicy:SetSize(90, 20)
  f.tabPolicy:SetPoint("TOPLEFT", 12, -30)
  f.tabPolicy:SetText("Policy")
  f.tabPolicy:SetScript("OnClick", function()
      f.activeTab = "policy"
      PolicyPanel:Refresh()
  end)

  f.tabDiff = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.tabDiff:SetSize(90, 20)
  f.tabDiff:SetPoint("LEFT", f.tabPolicy, "RIGHT", 6, 0)
  f.tabDiff:SetText("Diff")
  f.tabDiff:SetScript("OnClick", function()
      f.activeTab = "diff"
      PolicyPanel:Refresh()
  end)

  f.activeTab = "policy"

  -- Filter (Policy Tab)
  local searchLabel = f:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
  searchLabel:SetPoint("TOPRIGHT", -316, -14)
  searchLabel:SetText("Filter")

  f.search = CreateFrame("EditBox", nil, f, "InputBoxTemplate")
  f.search:SetSize(240, 20)
  f.search:SetPoint("TOPRIGHT", -70, -12)
  f.search:SetAutoFocus(false)
  f.search:SetScript("OnTextChanged", function() PolicyPanel:Refresh() end)

  -- Leaves-only checkbox (Policy Tab)
  f.leavesOnly = CreateFrame("CheckButton", nil, f, "UICheckButtonTemplate")
  f.leavesOnly:SetPoint("TOPLEFT", f.search, "BOTTOMLEFT", 0, -6)
  f.leavesOnly.text = f.leavesOnly:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
  f.leavesOnly.text:SetPoint("LEFT", f.leavesOnly, "RIGHT", 2, 0)
  f.leavesOnly.text:SetText("Leaves only")
  f.leavesOnly:SetScript("OnClick", function() PolicyPanel:Refresh() end)

  -- Copy box (Shared)
  f.copyBox = CreateFrame("EditBox", nil, f, "InputBoxTemplate")
  f.copyBox:SetSize(520, 20)
  f.copyBox:SetPoint("TOPLEFT", 12, -56)
  f.copyBox:SetAutoFocus(false)
  f.copyBox:SetText("Click a row -> Copy path/value here")
  f.copyBox:SetScript("OnEscapePressed", function() f.copyBox:ClearFocus() end)
  
  -- Diff Controls (Diff Tab)
  f.saveSnap = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.saveSnap:SetSize(120, 20)
  f.saveSnap:SetPoint("TOPLEFT", f.copyBox, "TOPRIGHT", 8, 0)
  f.saveSnap:SetText("Save Snapshot")
  f.saveSnap:SetScript("OnClick", function()
      local specKey = currentSpecKey()
      if not specKey then print("SkillWeaver: no specKey") return end
      if not PolicySnapshot then PolicySnapshot = addonTable.PolicySnapshot end
      local cur = PolicyManager:Get(specKey)
      PolicySnapshot:Set(specKey, cur)
      print("SkillWeaver: saved policy snapshot for " .. specKey)
      PolicyPanel:Refresh()
  end)
  f.saveSnap:Hide()
  
  -- Mode Toggles
  f.diffMode = "changed"
  local function setDiffMode(m) f.diffMode = m; PolicyPanel:Refresh() end
  
  f.diffAllBtn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.diffAllBtn:SetSize(60, 20)
  f.diffAllBtn:SetPoint("TOPLEFT", f.saveSnap, "BOTTOMLEFT", 0, -6)
  f.diffAllBtn:SetText("All")
  f.diffAllBtn:SetScript("OnClick", function() setDiffMode("all") end)
  f.diffAllBtn:Hide()

  f.diffChgBtn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.diffChgBtn:SetSize(80, 20)
  f.diffChgBtn:SetPoint("LEFT", f.diffAllBtn, "RIGHT", 6, 0)
  f.diffChgBtn:SetText("Changed")
  f.diffChgBtn:SetScript("OnClick", function() setDiffMode("changed") end)
  f.diffChgBtn:Hide()

  f.diffAddBtn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.diffAddBtn:SetSize(70, 20)
  f.diffAddBtn:SetPoint("LEFT", f.diffChgBtn, "RIGHT", 6, 0)
  f.diffAddBtn:SetText("Added")
  f.diffAddBtn:SetScript("OnClick", function() setDiffMode("added") end)
  f.diffAddBtn:Hide()

  f.diffRemBtn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.diffRemBtn:SetSize(80, 20)
  f.diffRemBtn:SetPoint("LEFT", f.diffAddBtn, "RIGHT", 6, 0)
  f.diffRemBtn:SetText("Removed")
  f.diffRemBtn:SetScript("OnClick", function() setDiffMode("removed") end)
  f.diffRemBtn:Hide()

  -- Scroll
  local sf = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
  sf:SetPoint("TOPLEFT", 12, -82)
  sf:SetPoint("BOTTOMRIGHT", -32, 12)

  local content = CreateFrame("Frame", nil, sf)
  content:SetSize(1, 1)
  sf:SetScrollChild(content)

  f.scroll = sf
  f.content = content

  -- Row pool
  local ROWS = 22
  local rowH = 20

  for i=1,ROWS do
    local r = CreateFrame("Button", nil, content)
    r:SetSize(680, rowH)
    r.text = r:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    r.text:SetPoint("LEFT", 4, 0)
    r.text:SetJustifyH("LEFT")

    r:SetScript("OnClick", function()
      local specKey = currentSpecKey()
      if not specKey then return end
      
      -- Handle Diff Tab Clicks (Jump)
      if PolicyPanel.frame.activeTab == "diff" then
          local d = r.__diff
          if not d or not d.path then return end
          
          -- Copy logic
          local merged = PolicyManager:Get(specKey)
          local eff = merged and getAtPath(merged, d.path) or nil
          copyToClipboard(d.path .. " = " .. tostring(eff))
          
          if Explain then Explain:PrintWhy(Explain:Why(specKey, d.path)) end
          
          -- Jump
          PolicyPanel.frame.activeTab = "policy"
          PolicyPanel:JumpToPath(d.path)
          return
      end

      -- Handle Policy Tab Clicks (Expand/Copy)
      if not r.item then return end
      local item = r.item

      if item.isTable then
        PolicyPanel:ToggleExpand(item.path)
        return
      end

      -- Leaf: copy path and print WHY to chat
      local merged = PolicyManager:Get(specKey)
      local eff = getAtPath(merged, item.path)
      copyToClipboard(item.path .. " = " .. tostring(eff))
      if Explain then Explain:PrintWhy(Explain:Why(specKey, item.path)) end
    end)

    r:SetScript("OnEnter", function()
      if f.activeTab == "diff" then return end -- simplified tooltip for diff (none needed mostly)
      if not r.item then return end
      GameTooltip:SetOwner(r, "ANCHOR_CURSOR")
      GameTooltip:AddLine(r.item.path, 1, 1, 1)
      GameTooltip:AddLine("Click table: expand/collapse", 0.8, 0.8, 0.8)
      GameTooltip:AddLine("Click leaf: copy path + print WHY", 0.8, 0.8, 0.8)
      GameTooltip:Show()
    end)
    r:SetScript("OnLeave", function() GameTooltip:Hide() end)
    
    r:SetHighlightTexture("Interface/QuestFrame/UI-QuestTitleHighlight")
    self.rows[i] = r
  end
  
  sf:SetScript("OnVerticalScroll", function(self, offset)
    sf:SetVerticalScroll(offset)
    PolicyPanel:Refresh()
  end)

  self.frame = f
  f:Hide()
end

function PolicyPanel:SetShown(shown)
  self:Create()
  if shown then self.frame:Show(); self:Refresh() else self.frame:Hide() end
end

return PolicyPanel
