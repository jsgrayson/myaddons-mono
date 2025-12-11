# Next Steps: NPC Ability Data Collection

## Summary of Investigation

### Data Sources Checked
1. ❌ **CSV files** - Template/placeholder data (all identical)
2. ❌ **encounters.json** - Empty abilities arrays
3. ❌ **Enhanced AI** - Missing abilities (only shows what players counter)
4. ❌ **Public APIs** - None exist for NPC battle data
5. ❌ **Wowhead/Xu-Fu** - Data exists but requires complex scraping

### What We Found
- Wowhead has complete NPC ability data but no public API
- Blizzard API doesn't cover enemy NPC abilities
- Community sites have data spread across individual tamer pages
- Enhanced AI scripts incomplete (only abilities mentioned in player counters)

## Recommended Solution: In-Game Data Collection

**Use the PetWeaverEnemyRecorder.lua addon** (already implemented!)

### Why This is Best
1. ✅ Real data from actual battles
2. ✅ Complete movesets (not just countered abilities)
3. ✅ Validated against live game
4. ✅ No scraping/API issues
5. ✅ Self-updating as you battle

### How to Use
1. Load PetWeaver addon in-game
2. Type `/pwrecord` to enable recording
3. Battle NPC tamers normally
4. Type `/reload` to save data
5. Run `export_ingame_recordings.py` to process

### Integration Plan
1. Collect 20-50 encounter recordings
2. Parse SavedVariables data
3. Generate complete npc_move_orders.json
4. Validate against known strategies
5. Use for genetic algorithm training

## Interim Solution
Use **Smart Agent** (basic AI without scripts) for genetic algorithm until we have enough recorded data.

**File:** `simulator/smart_agent.py`
- Already implemented
- Doesn't require NPC scripts
- Good enough for initial GA testing

## Timeline
- **Short term:** Use Smart Agent for GA (ready now)
- **Medium term:** Collect in-game recordings (1-2 weeks)
- **Long term:** Complete NPC database from recordings

## Files Status
- ✅ `PetWeaverEnemyRecorder.lua` - Ready
- ✅ `export_ingame_recordings.py` - Template exists
- ✅ `simulator/smart_agent.py` - Working
- ⏳ `npc_move_orders.json` - Awaiting recordings
