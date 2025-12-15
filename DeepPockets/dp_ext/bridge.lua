-- dp_ext/bridge.lua
DeepPockets = DeepPockets or {}
DeepPockets.API = DeepPockets.API or {}

-- Stable global bridge for other addons (SkillWeaver/PetWeaver)
_G.DEEPPocketsBridge = _G.DEEPPocketsBridge or { API = DeepPockets.API }
