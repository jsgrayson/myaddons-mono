# Future-Proofing for Midnight (11.1+)

## Expected Changes in Midnight

### 1. Hero Talents
- New talent trees added to existing specs
- Could affect `C_Traits.GetConfigInfo` structure
- **Mitigation:** Already scanning all `treeIDs` - will pick up Hero talents automatically

### 2. Potential New Class
- Tinker or other new class rumored
- **Mitigation:** Scraper is class-agnostic, just add to `generate_config.py`

### 3. API Changes
- Blizzard may update talent API
- **Mitigation:** Added `pcall()` wrappers in TalentDetector for safe failures

### 4. Resource System Changes
- New resource types (similar to Essence for Evoker)
- **Mitigation:** ConditionParser is extensible - add new tokens easily

### 5. Spell Name Changes
- Abilities renamed or replaced by talents
- **Mitigation:** Use spell IDs where possible, scraper auto-updates

---

## Architecture Decisions for Longevity

### Modular Design
```
core/           # Foundational logic (unlikely to change)
engine/         # Condition/Sequence parsing (extensible)
scraper/        # External data (easy to update)
sequences/      # User-facing (regenerated from scraper)
```

### API Safety
All API calls wrapped in `pcall()` to prevent errors:
```lua
local success, result = pcall(C_Traits.GetConfigInfo, configID)
if not success then
    -- Fallback or graceful degradation
end
```

### Scraper-Driven Content
- Rotations come from Icy Veins/Wowhead (not hardcoded)
- Talent strings auto-update
- **When Midnight launches:** Just run scraper again

### Extensible Tokens
Adding new condition tokens is simple:
```lua
-- In ConditionParser.lua
if token == "new_resource" then
    return UnitPower("player", NEW_POWER_TYPE)
end
```

---

## Midnight Update Plan

### Day 1 (Expansion Launch):
1. **Test addon** - Check for API errors
2. **Update scraper URLs** - Icy Veins will have new guides
3. **Run scrapers** - Generate fresh rotations

### Week 1:
1. **Monitor class discords** - New theorycrafting
2. **Add Hero talent support** - Should work automatically, verify
3. **Update manual sequences** - Adjust for new abilities

### Month 1:
1. **Implement new mechanics** - If Midnight adds new systems
2. **SimC APL integration** - Phase 3 will make this automatic

---

## What Might Break

### High Risk:
- ❌ `C_Traits` API structure changes
  - **Fix:** Update TalentDetector.lua
- ❌ Spell IDs change massively
  - **Fix:** Re-run scraper

### Medium Risk:
- ⚠️ New resource types not detected
  - **Fix:** Add new tokens to ConditionParser
- ⚠️ Hero talents use different API
  - **Fix:** Update `RefreshCache()` logic

### Low Risk:
- ✅ Rotation changes (handled by scraper)
- ✅ New class (add to config generator)
- ✅ Spell renames (scraper uses current names)

---

## Maintenance Strategy

### Before Each Patch:
1. Backup `sequences/` folder
2. Test on PTR if possible
3. Check WoW API changelog

### After Patch:
1. Run all scrapers
2. Test one spec per role
3. Update documentation

### Community:
- GitHub issues for bug reports
- Discord for quick fixes
- Wiki for user guides

---

## API Monitoring

**Watch these Blizzard APIs:**
- `C_ClassTalents.*` - Talent system
- `C_Traits.*` - Talent trees
- `UnitPower()` - Resource tracking
- `GetSpellInfo()` - Spell data

**When they change:**
- TalentDetector.lua (talent detection)
- ConditionParser.lua (resource tokens)

---

## Scraper Updates

### If Icy Veins changes HTML:
1. Update CSS selectors in `scraper.py`
2. Test with 2-3 classes
3. Re-run full scraper

### If SimC APL format changes:
1. Update APL parser (Phase 3)
2. Regenerate sequences

---

## Long-Term Vision

**11.1 (Midnight):**
- Hero talents supported
- New class added
- Fresh rotations scraped

**11.2-11.3:**
- SimC APL integration complete
- Auto-updates from theorycrafting
- ML performance tracking

**12.0 (Next Expansion):**
- Repeat Midnight process
- Architecture is expansion-agnostic
- Community maintains scrapers

---

## Resilience Checklist

✅ Modular architecture  
✅ API safety with pcall()  
✅ Scraper-driven content  
✅ Extensible token system  
✅ Fallback mechanisms  
✅ Community update path  
✅ Documentation for maintainers  

**The addon will survive Midnight and beyond!**
