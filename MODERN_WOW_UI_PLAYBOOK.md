# Modern WoW UI Playbook (Retail 11.x - The War Within)

**Target Environment:** World of Warcraft Retail 11.x
**Deprecation Warning:** Do not use APIs marked for Dragonflight (10.x) deprecation. Do not assume Vanilla/Classic widget behavior.

---

## 1. Core Philosophy: The "No-Touch" Secure Rule
The modern WoW UI is a mix of Lua and C++ secured code.
**Rule #1:** Never attempt to "shim" or "mock" a protected frame (Bags, ActionBars, UnitFrames) to force it to work your way. You will taint the execution path and cause "Action Blocked" errors.

- **Bad:** Forking `ContainerFrame.lua` code to make your own bag buttons.
- **Good:** Creating a completely independent frame (`C_Container` based) OR securely hooking headers using `SecureHandlerStateTemplate` (advanced only).
- **Best:** Writing a **Data Provider** for an existing, stable UI addon (e.g., BetterBags, Masque).

---

## 2. Inventory & Containers (C_Container)
The global `GetContainer*` functions are deprecated or wrappers. Use `C_Container` namespace.

**Read Operations (Backend Safe):**
- `C_Container.GetContainerNumSlots(bagID)`
- `C_Container.GetContainerItemInfo(bagID, slotID)` -> returns table (not multi-return!) containing `info.itemID`, `info.hyperlink`, `info.iconFileID` etc.
- `C_Container.GetContainerItemID(bagID, slotID)`

**Write/Action Operations (UI Restricted):**
- `C_Container.UseContainerItem(bagID, slotID)` -> **PROTECTED**. Requires hardware event. Cannot be called by background logic.
- `C_Container.PickupContainerItem(bagID, slotID)` -> **PROTECTED**.

**Playbook Rule:**
Backend addons (DeepPockets) must **ONLY** use Read Operations. Never call `Use/Pickup` functions. Leave that to the UI frame (BetterBags) which handles the secure hardware clicks.

---

## 3. Tooltips & The "Owner Nil" Crash
Tooltip handling changed in 10.x/11.x to use `TooltipDataProcessor` and unified data structures.

**The Danger Zone:**
- `GameTooltip:SetOwner(nil)` crashes the client or breaks the tooltip state.
- Hooking `OnTooltipSetItem` recklessly can cause infinite loops or taint.

**Patterns for 11.x:**
1. **Ownership Check:** Always check `if not tooltip:GetOwner() then return end` before modifying.
2. **Data Processor:** Use `TooltipDataProcessor.AddLinePostCall(Enum.TooltipDataType.Item, function(tooltip, data) ... end)` instead of hooking `OnTooltipSetItem` directly on `GameTooltip`.
3. **Scan Lines:** If you need to read text, scan the `TooltipData`, do not traverse regions manually unless absolutely necessary.

---

## 4. Bindings.xml & Secure Headers
**Bindings.xml** is parsed at startup.
- **Strict Schema:** If your XML is malformed or uses old schema, the client may silently fail or create "phantom" bindings that crash legacy code.
- **Backend Rule:** Backend addons MUST NOT ship `Bindings.xml`.
- **UI Rule:** If a UI needs bindings, register them via `LibStub("AceConsole-3.0"):RegisterChatCommand` or let the user map them via Blizzard's Keybinding UI if you create a proper standard frame.

---

## 5. Templates & Mixins
Retail WoW uses Mixins heavily.
- **BackdropTemplate:** Frames no longer have backdrops by default. You MUST inherit `BackdropTemplate` and call `Mixin(self, BackdropTemplateMixin)` or include it in XML to use `SetBackdrop`.
- **Panel Templates:** Use `UIPanelDialogTemplate` or `PortraitFrameTemplate` for standard look-and-feel. Do not build windows from scratch using textures unless creating a custom skin.

---

## 6. Combat Lockdown (InCombatLockdown)
**Rule:** You cannot Show/Hide/Move secure frames or change attributes on them during combat.
- **Backend Impact:** Low. Data processing can happen in combat.
- **UI Impact:** High. If BetterBags is open and you try to inject a frame into it during combat, you will crash it.
- **Mitigation:** Listen for `PLAYER_REGEN_DISABLED` (combat start) and `PLAYER_REGEN_ENABLED` (combat end). Queue UI updates until `ENABLED`.

---

## 7. Integration Strategy (The "Provider" Pattern)
Instead of hooking functionality:
1. **Expose Data:** `MyAddon.GetCategory(itemID)`
2. **Register Callbacks:** `MyAddon:RegisterCallback("OnInventoryUpdate", function() ... end)`
3. **Let UI Pull:** The UI layer (BetterBags) should *pull* data from the Backend (DeepPockets) when it is ready to render, rather than the Backend *pushing* updates to the UI frames.
