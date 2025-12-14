-- dp_ext/sanity.lua
SLASH_DP_SANITY1 = "/dp_sanity"
SlashCmdList["DP_SANITY"] = function()
  local ok = true
  local failures = 0

  if not DeepPocketsDB then ok=false failures=failures+1 end

  local status = ok and "OK" or "FAIL"
  -- Print JSON-like for Holocron parser
  print(("SANITY_RESULT {\"addon\":\"DeepPockets\",\"status\":\"%s\",\"checks\":1,\"failures\":%d}"):format(status, failures))
end
