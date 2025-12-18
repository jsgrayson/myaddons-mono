# SkillWeaver Macro Command Guide

**All slash commands work in macros!** Perfect for controller players using action bars.

---

## Quick Macro Examples

### **Macro 1: Toggle Consumables**
```
#showtooltip
/skw cons
```
**Bind to:** Action bar slot (controller: D-Pad Up)  
**Use:** Before boss pulls in M+/raids

---

### **Macro 2: Toggle Interrupts**
```
#showtooltip
/skw int
```
**Bind to:** Action bar slot (controller: D-Pad Left)  
**Use:** Disable for specific mechanics

---

### **Macro 3: Toggle Ally Healing**
```
#showtooltip
/skw heal
```
**Bind to:** Action bar slot (controller: D-Pad Right)  
**Use:** Disable for pure DPS parsing

---

### **Macro 4: Toggle Pet Management**
```
#showtooltip
/skw pet
```
**Bind to:** Action bar slot (controller: L3)  
**Use:** Hunter/Warlock/DK only

---

### **Macro 5: Show Status**
```
#showtooltip
/skw status
```
**Bind to:** Action bar slot (controller: D-Pad Down)  
**Use:** Check all current toggle states

---

## Advanced Macros

### **Enable Consumables + Announce**
```
/skw cons
/say Consumables ON - going hard!
```

### **Disable Consumables + Save Gold Message**
```
/skw cons
/say Consumables OFF - farming mode 💰
```

### **Pre-Pull Consumables Check**
```
/skw status
/say Ready check - verify consumables!
```

### **Emergency Toggle Everything Off**
```
/skw cons
/skw int
/skw heal
/say All features disabled - manual mode
```

### **Conditional Toggle (with modifier)**
```
#showtooltip
/skw [mod:shift] int; [mod:ctrl] heal; cons
```
**This macro:**
- **Normal press:** Toggle consumables
- **Shift + press:** Toggle interrupts
- **Ctrl + press:** Toggle ally healing

---

## All Available Slash Commands

### **Primary Commands**
```
/skw consumables    (or /skw cons)   - Toggle paid consumables
/skw interrupt      (or /skw int)    - Toggle auto-interrupt
/skw healing        (or /skw heal)   - Toggle ally healing
/skw pet                            - Toggle pet management
/skw status                         - Show all toggle states
```

### **Utility Commands**
```
/skw settings       (or /skw config) - Open settings panel
/skw minimap                        - Hide/show minimap button
/skw help                           - Show all commands
```

### **Alternative Prefix**
Both work the same:
```
/skillweaver cons  = /skw cons
/skillweaver int   = /skw int
```

---

## Controller Player Setup

### **Option 1: Action Bar Macros (Recommended)**

**Step 1:** Create macros (examples above)  
**Step 2:** Drag macros to action bars  
**Step 3:** Bind controller buttons to those bar slots  

**Example ConsolePort Setup:**
- Action Bar 1, Slot 1 = `/skw cons` → Bind to D-Pad Up
- Action Bar 1, Slot 2 = `/skw int` → Bind to D-Pad Left
- Action Bar 1, Slot 3 = `/skw heal` → Bind to D-Pad Right
- Action Bar 1, Slot 4 = `/skw status` → Bind to D-Pad Down

### **Option 2: Direct Keybinds (Advanced)**

Use WoW's built-in keybinds (no macro needed):
- Keybindings → SkillWeaver → Bind controller buttons directly

---

## Macro Tips

### **Use #showtooltip for Visual Feedback**
```
#showtooltip
/skw cons
```
Shows current action on cursor hover.

### **Combine with Other Actions**
```
#showtooltip
/use [combat] Healthstone
/skw [nocombat] cons
```
**Result:**
- In combat: Use healthstone
- Out of combat: Toggle consumables

### **Party/Raid Announcements**
```
/skw cons
/p Consumables %t - pulling boss!
```
Announces consumables state to party.

### **Emergency Macro (All Defensives)**
```
#showtooltip
/use Healthstone
/cast Exhilaration
/skw status
```
Use healthstone, pop defensive, check status.

---

## Text Macro Expansion

### **Status Output Example**
When you run `/skw status`, you get:
```
SkillWeaver Status:
  Always Active: Healthstones, Interrupts, Defensives
  Paid Consumables: ON
  Auto-Interrupt: ON
  Ally Healing: ON
  Pet Management: ON
```

### **Toggle Output Example**
When you run `/skw cons`, you get:
```
SkillWeaver: Consumables ENABLED
```
(with green color and sound effect)

---

## Macro Naming Ideas

**Short & Clear:**
- "SW: Cons"
- "SW: Int"
- "SW: Heal"
- "SW: Pet"
- "SW: Status"

**Descriptive:**
- "Toggle $$$" (consumables)
- "Toggle Interrupt"
- "Toggle Healing"
- "Check Status"

**Icon Suggestions:**
- Consumables: Flask icon
- Interrupts: Kick/Pummel icon
- Healing: Flash Heal icon
- Status: Question mark icon

---

## Common Use Cases

### **M+ Tyran Week (Lots of Interrupts)**
```
Macro 1: /skw int    (keep interrupts ON)
Macro 2: /skw cons   (toggle consumables for hard pulls)
```

### **Raid Progression**
```
Macro 1: /skw cons   (enable before boss, disable after)
Macro 2: /skw status (verify all ON before pull)
```

### **Gold Farming**
```
Macro 1: /skw cons   (verify OFF to save gold)
Macro 2: /skw int    (disable if not needed)
```

### **PvP Arena**
```
Macro 1: /skw heal   (disable for pure DPS)
Macro 2: /skw pet    (manual pet control)
```

---

## Troubleshooting

### **"Macro doesn't work"**
- Ensure you typed `/sw` not `/sw,` (no comma!)
- Check for typos (`cons` not `con`)
- Test the command directly in chat first

### **"No output in chat"**
- Slash commands DO print to chat
- Check if chat is filtered (Combat Log settings)
- Run `/skw help` to verify addon is loaded

### **"Controller button not toggling"**
- Verify macro is on action bar
- Check controller button is bound to that bar slot
- Test with keyboard first (press action bar keybind)

---

## Pro Tips

1. **Place on Visible Action Bar**
   - See icon when it's ready to toggle
   - Visual reminder of current state

2. **Use Conditional Modifiers**
   - One button, multiple toggles
   - Save controller buttons

3. **Create Sound Macros**
   - Add `/script PlaySound(SOUNDKIT.RAID_WARNING)` for extra audio cue

4. **Announce to Raid**
   - Let team know when you're using expensive consumables
   - Coordinate lust timing with consumable use

5. **Keyboard + Controller Combo**
   - Keyboard: Use minimap button or slash commands
   - Controller: Use macros on action bars
   - Best of both worlds!

---

## Summary

**For Controller Players:**
- ✅ Create macros with `/sw` commands
- ✅ Drag to action bars
- ✅ Bind controller buttons to bar slots
- ✅ Press button = instant toggle!

**For Keyboard Players:**
- ✅ Same macros work
- ✅ OR use minimap button
- ✅ OR type commands directly

**Everyone has full access via macros!** 🎮⌨️
