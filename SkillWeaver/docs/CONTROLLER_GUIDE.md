# SkillWeaver Controller Support Guide

## For Controller Players (ConsolePort / Native WoW Controller)

### **How to Set Up Toggle Controls**

Controller players **need to bind SkillWeaver actions to controller buttons** via WoW's Keybindings menu.

---

## Step-by-Step Setup

### 1. **Open WoW Keybindings Menu**
- Press **ESC** → **Options** → **Keybindings**
- OR use your controller's menu button to access settings

### 2. **Scroll to "SkillWeaver" Category**
You'll find these keybinds:

```
SkillWeaver
├─ Toggle Paid Consumables     [Unbound]
├─ Toggle Auto-Interrupt        [Unbound]
├─ Toggle Ally Healing          [Unbound]
├─ Toggle Pet Management        [Unbound]
├─ Show Toggle Status           [Unbound]
└─ Open Settings Menu           [Unbound]
```

### 3. **Bind to Controller Buttons**

**Recommended Controller Mapping:**
- **D-Pad Up:** Toggle Paid Consumables (most common toggle)
- **D-Pad Down:** Show Toggle Status (check current state)
- **D-Pad Left:** Toggle Auto-Interrupt
- **D-Pad Right:** Toggle Ally Healing
- **L3 (Left Stick Click):** Toggle Pet Management
- **R3 (Right Stick Click):** Open Settings Menu

**OR use ConsolePort bindings:**
- In ConsolePort addon, assign SkillWeaver keybinds to your preferred buttons

### 4. **Test Your Bindings**
- Press the bound button
- You'll see: `SkillWeaver: [Feature] ENABLED/DISABLED` in chat
- Hear a sound effect confirming the toggle

---

## What Each Keybind Does

### **Toggle Paid Consumables**
- **What:** Flasks, Potions, Food, Augment Runes
- **Default:** OFF (saves gold)
- **When to enable:** Mythic+, Raids, Rated PvP
- **Cost:** ~3000-5000g per hour

### **Toggle Auto-Interrupt**
- **What:** Automatically interrupt enemy casts
- **Default:** ON
- **When to disable:** Specific mechanics that require NOT interrupting
- **Example:** Certain Sanguine Depths bosses

### **Toggle Ally Healing**
- **What:** Emergency healing when allies < 15% health
- **Default:** ON
- **When to disable:** Pure DPS parsing (meters)
- **Example:** Disable for personal best logs

### **Toggle Pet Management**
- **What:** Auto Growl toggle, Misdirection logic, pet summon
- **Default:** ON (Hunter/Warlock/DK only)
- **When to disable:** Manual pet control preferred
- **Example:** PvP arenas with specific strategies

### **Show Toggle Status**
- **What:** Prints all current toggle states to chat
- **Output:**
  ```
  SkillWeaver Status:
    Always Active: Healthstones, Interrupts, Defensives
    Paid Consumables: OFF
    Auto-Interrupt: ON
    Ally Healing: ON
    Pet Management: ON
  ```

### **Open Settings Menu**
- **What:** Opens dropdown menu (navigable with controller cursor)
- **Contains:** All toggles + options submenu
- **Navigation:** Use controller cursor to select options

---

## ConsolePort Integration

### **If You Use ConsolePort Addon:**

1. **Open ConsolePort Bindings:**
   - `/cp` → **Bindings**

2. **Find "SkillWeaver" Section:**
   - Scroll to addon keybinds
   - SkillWeaver actions will be listed

3. **Assign to Controller Buttons:**
   - Use ConsolePort's visual button mapper
   - Assign each action to your preferred button

4. **Save & Test:**
   - Press the button to toggle
   - Visual and audio feedback confirms action

---

## Alternative: Macro Buttons

### **If You Prefer Macros on Action Bars:**

Create macros and bind controller buttons to action bar slots:

**Macro 1: Toggle Consumables**
```
/skw consumables
```

**Macro 2: Toggle Interrupts**
```
/skw interrupt
```

**Macro 3: Toggle Healing**
```
/skw healing
```

**Macro 4: Toggle Pet**
```
/skw pet
```

**Macro 5: Show Status**
```
/skw status
```

Place these macros on your action bars, then bind controller buttons to those bar slots in ConsolePort.

---

## Recommended Controller Setup

### **Quick Access (D-Pad)**
```
        ↑ Consumables
        
   ←Interrupt   Healing→
        
        ↓ Status
```

### **Advanced (Stick Clicks)**
```
L3: Pet Management
R3: Settings Menu
```

### **Why This Layout?**
- **Up (Consumables):** Most frequently toggled (enable for progression, disable for farm)
- **Down (Status):** Quick check of all states
- **Left/Right:** Less frequently changed utilities
- **Stick Clicks:** Advanced features (pet, settings)

---

## Troubleshooting

### **"Keybinds not showing in menu"**
- Ensure SkillWeaver is loaded: `/skw help`
- Reload UI: `/reload`
- Check for addon conflicts

### **"Controller button not working"**
- Check if button is already bound to another action
- Verify keybind was saved
- Test with keyboard first (`/skw cons`) to confirm feature works

### **"ConsolePort not detecting SkillWeaver"**
- Update ConsolePort to latest version
- SkillWeaver keybinds use standard WoW API (should work)
- Try binding via WoW's native keybinds menu instead

---

## Visual Feedback

### **When You Toggle:**
- **Chat Message:** `SkillWeaver: [Feature] ENABLED/DISABLED`
- **Sound Effect:** 
  - ✅ ENABLED: Achievement chime
  - ❌ DISABLED: Lost target sound
- **Color Coding:**
  - Green = Enabled
  - Red = Disabled

### **Status Check (D-Pad Down):**
```
SkillWeaver Status:
  Always Active: Healthstones, Interrupts, Defensives
  Paid Consumables: [GREEN ON] or [RED OFF]
  Auto-Interrupt: [GREEN ON] or [RED OFF]
  Ally Healing: [GREEN ON] or [RED OFF]
  Pet Management: [GREEN ON] or [RED OFF]
```

---

## Default States Summary

| Feature | Default | Cost | When to Toggle |
|---------|---------|------|----------------|
| **Healthstones** | ALWAYS ON | FREE | Never (always use!) |
| **Paid Consumables** | OFF | HIGH | Enable for progression |
| **Auto-Interrupt** | ON | FREE | Disable for specific mechanics |
| **Ally Healing** | ON | FREE | Disable for pure DPS parses |
| **Pet Management** | ON | FREE | Disable for manual control |

---

## Pro Tips for Controller Players

1. **Bind D-Pad Up (Consumables) for Quick Access**
   - Enable before M+ boss pulls
   - Disable immediately after for gold savings

2. **Use Status Check Often**
   - Verify consumables are OFF when farming
   - Confirm everything is ON before progression

3. **Create ConsolePort Profile per Content**
   - **Mythic+ Profile:** Consumables ON
   - **Farm Profile:** Consumables OFF
   - **PvP Profile:** Custom toggles

4. **Don't Forget Healthstones!**
   - Always active (can't disable)
   - Ask Warlock for healthstones before dungeon/raid
   - 100% free emergency heal

---

## Need Help?

**Test Keybinds:**
```
/skw status    - Show all current states
/skw help      - Show all commands
```

**Report Issues:**
- Discord: [SkillWeaver Community](#)
- GitHub: [SkillWeaver Issues](#)

---

**Remember:** Controller players have **full access** to all features via keybinds! 🎮
