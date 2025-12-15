-- event_guard.lua - register only real events; never register unknown events.
local f = CreateFrame("Frame")
_G.DeepPockets_EventFrame = f

function _G.DeepPockets_RegisterSafeEvent(event, handler)
  if type(event) ~= "string" or event == "" then return end
  local ok = pcall(f.RegisterEvent, f, event)
  if ok and type(handler) == "function" then
    f:HookScript("OnEvent", function(_, e, ...) if e == event then handler(...) end end)
  end
end
