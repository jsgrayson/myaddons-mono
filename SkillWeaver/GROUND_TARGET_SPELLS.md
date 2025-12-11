# Ground-Target Spell Macro Reference

## Standard Support (Confirmed Working)

### `@player` - Works for ALL ground-target spells ⭐ BEST FOR HANDHELDS
- Consecration
- Death and Decay
- Blizzard
- Flamestrike
- Ring of Frost
- Holy Word: Sanctify
- Meteor
- Rain of Fire
- Heroic Leap
- All Hunter Traps
- All Shaman Totems

### `@cursor` - Works for ALL ground-target spells (Mouse/Keyboard only)
**NOT RECOMMENDED FOR HANDHELDS** - Requires touchscreen!

## `@target` Support (TEST THESE)

### Possibly Working (User Reports Vary):
These may work depending on patches/talents:

**Mage:**
- Flamestrike (some reports it works)
- Meteor (some reports it works)
- Blizzard (mixed reports)

**Warlock:**
- Rain of Fire (some reports)

**Demon Hunter:**
- Sigil abilities (may have built-in target support)

**Death Knight:**
- Death and Decay (mixed reports, may depend on talents)

## Recommended Macro Patterns

### For Handhelds (Steam Deck, ROG Ally, etc.):
```lua
-- ALWAYS use @player - no touchscreen needed!
/cast [@player] Blizzard
/cast [@player] Death and Decay
/cast [@player] Flamestrike
```

**How to use:**
1. Move into position where you want the spell
2. Spam your button
3. Spell drops instantly under you
4. **No cursor, no touchscreen, no problem!**

### For Desktop Controllers (ConsolePort):
```lua
-- Try @target first (test each spell)
/cast [@target] SpellName

-- If @target doesn't work, use @player
/cast [@player] SpellName
```

### For Mouse/Keyboard:
```lua
-- Use @cursor for speed
/cast [@cursor] Blizzard
```

## Handheld Player Tips

**For DPS spells (Blizzard, Flamestrike, etc.):**
- Use `[@player]`
- Position yourself in melee range or edge of pack
- Spell drops under you = hits everything nearby
- Works perfectly with one-button spam!

**For Tank/Healer spells:**
- `[@player]` is already optimal
- You're usually standing where you want the spell anyway

## Testing Your Spells

1. Create a macro: `/cast [@target] YourSpell`
2. Target an enemy
3. Press the macro
4. If it casts at target's feet → ✅ Works!
5. If nothing happens or shows reticle → ❌ Doesn't work, use `[@player]` instead

**Handheld users:** Just use `[@player]` for everything. No testing needed!
