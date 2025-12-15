-- dp_ext/api_backend.lua
-- Backend API surface. No UI. Safe to load early.

local DP = _G.DeepPockets or {}
_G.DeepPockets = DP

DP.API = DP.API or {}
local API = DP.API

-- internal provider slot
API._categoryProvider = API._categoryProvider or nil

-- Called by providers (e.g. dp_ext/category_provider_basic.lua)
function API._SetCategoryProvider(fn)
  if type(fn) == "function" then
    API._categoryProvider = fn
  end
end

-- Public: returns a category string
function API.GetItemCategory(itemID, itemLink)
  if API._categoryProvider then
    local ok, cat = pcall(API._categoryProvider, itemID, itemLink)
    if ok and type(cat) == "string" and cat ~= "" then
      return cat
    end
  end
  return "Misc"
end

-- Optional: feature discovery
function API.Has(feature)
  return feature == "category"
end
