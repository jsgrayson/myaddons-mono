# WoW Midnight (Patch 12.0) Addon Compatibility Guide

## Core Philosophy: The "Black Box" Combat Model
In Patch 12.0, Blizzard has removed the ability for addons to make logical decisions based on combat data.
- **Visuals are OK:** You can skin frames.
- **Logic is Banned:** You cannot use real-time combat data (`UnitHealth`, `UnitName`) to conditionally run code.

## Critical API Changes: The "Secret" System
### 1. What is a "Secret Value"?
A protected value type returned by game functions during combat.
- **Behavior:** You cannot read the actual value (e.g., `50%`). You only know it exists.
- **Taint:** Using a Secret in `if` statements or arithmetic (`+`, `-`, `*`) causes a crash/error.

### 2. Restricted Functions
The following now return **Secret** values in combat:
- `UnitName(unit)`
- `UnitHealth(unit)` / `UnitHealthMax(unit)`
- `UnitPower(unit)` / `UnitPowerMax(unit)`
- `UnitAura(unit)`
- `GetSpellCooldown(spellID)`

### 3. Compatibility Checks
Use these new functions to guard your code:
- `issecretvalue(value)`: Returns `true` if the variable is Secret.
- `canaccesssecrets()`: Returns `true` if the environment is secure (rare).

## Holocron Compliance Strategy
To ensure Holocron functions in Patch 12.0:

### Lua (`Holocron_Status.lua`)
- **Guard Arithmetic:** Before calculating percentages (e.g., `Health / Max`), check `issecretvalue()`.
- **Fallback:** If values are secret, export a sentinel value (e.g., `-1`) or a generic status.
- **No Logic:** Do not use `if health < 0.5` in Lua. Export the raw (or secret) state and let the external Python engine handle the ambiguity.

### Python (`lumos.py`)
- **Handle Secrets:** If the Lua file reports `-1` for health, default to a generic "Combat Mode" lighting scheme (e.g., Solid Red) instead of a precise Health Gradient.
- **Combat Log:** Rely on `WoWCombatLog.txt` for event triggers (Spells, Death) as this file stream is external to the Lua sandbox restrictions.

## Migration Checklist
- [x] Update `.toc` interface to `120000`.
- [x] Wrap `UnitHealth` calls with `issecretvalue`.
- [x] Remove string concatenation with `UnitName`.
