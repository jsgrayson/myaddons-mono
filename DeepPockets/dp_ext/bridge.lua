-- dp_ext/bridge.lua
-- Single stable global “bridge” object for other addons (SkillWeaver/PetWeaver)
-- Do NOT rename/remove once released.

DeepPockets = DeepPockets or {}
DeepPockets.API = DeepPockets.API or {}

-- Provide a stable global name other addons can check without loading order pain.
-- Usage in other addons:
--   local bridge = _G.DEEPPocketsBridge
--   if bridge and bridge.API and bridge.API.Has("provenance") then ...
_G.DEEPPocketsBridge = _G.DEEPPocketsBridge or {
  API = DeepPockets.API
}
