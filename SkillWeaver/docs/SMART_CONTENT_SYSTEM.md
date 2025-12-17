# SkillWeaver Smart Content System Guide

The **Smart Content System** is the brain of SkillWeaver, automatically adapting your interface, recommendations, and automation settings to match the content you are currently playing.

## 1. Content Detection
SkillWeaver automatically detects your current environment and adjusts accordingly.

| Content Type | Detection Criteria | Default Behavior |
| :--- | :--- | :--- |
| **Raid** | Inside a Raid instance | Recommends Single Target / Raid builds. |
| **Mythic+** | Inside a Mythic+ Dungeon | Recommends AoE / Dungeon builds. |
| **Delve** | Inside a Delve instance | Recommends Solo/Survival builds. |
| **PvP** | Battlegrounds or Arenas | Recommends PvP builds & Talents. |
| **Open World** | Outdoors (not in instance) | Defaults to **Delve** (Solo) builds. |

### Manual Override
You can manually force a specific content mode via the **Smart Interface** dropdown menu (e.g., to prepare for a Raid while still in Valdrakken).

## 2. Smart Interface Panel
The Smart Interface is your central hub for optimization. It appears automatically or can be toggled via `/sw smart`.

### Features
- **Current Content**: Displays detected content (or your manual override).
- **Recommended Spec**: Suggests the best specialization for the content.
- **Talent Build**: Shows the name of the optimal talent build.
- **PvP Talents**: (PvP Mode Only) Lists the top 3 PvP talents to select.
- **Equipment Set**: Recommends the best gear set (e.g., "Optimized for Raid").
- **Brann Perk**: Suggests the best Combat Curio for Brann Bronzebeard (Delves).

### "Apply All" Button
One click to rule them all. Clicking **Apply All** will:
1.  Copy the recommended **Talent Import String** to your clipboard.
2.  Equip the recommended **Equipment Set** (if one exists with that name).
3.  Set Brann's **Combat Curio** (if you are near him).

## 3. Automation Modules
SkillWeaver includes several "set and forget" automation modules, configurable via the Minimap Button -> **Advanced Modules**.

### Auto-Trinkets
- **DPS Trinkets**: Uses on-use DPS trinkets during cooldown windows (e.g., with Avenging Wrath).
- **Defensive Trinkets**: Uses defensive trinkets when health drops below 40%.

### Auto-Racials
- **DPS Racials**: Syncs Orc/Troll/etc. racials with major cooldowns.
- **Utility Racials**: Uses War Stomp/Quaking Palm to interrupt casts if kick is on CD.
- **Defensive Racials**: Uses Stoneform/Fireblood to remove debuffs or mitigate damage.

### Loss of Control (LoC)
Automatically uses **Trinkets** (Gladiator's Medallion) or **Racials** (Will to Survive) to break:
- Stuns
- Fears
- Silences
- Roots (if melee)

### Auto-Buffs
Automatically casts group buffs (Intellect, Fortitude, Shout, MotW) when:
- You enter a dungeon/raid.
- A group member is missing the buff.
- You are out of combat.

### Battle Resurrection
Smartly manages Rebirth/Raise Ally/Soulstone.
- **Priority**: Tank > Healer > DPS.
- **Safety**: Checks range and resources before casting.
- **Toggle**: Can be enabled/disabled via `/sw bres`.

## 4. Stock Management
Never run out of consumables again.
- **Low Stock Warning**: Warns you when you have fewer than **5** (configurable) Potions or Healthstones left.
- **Thresholds**: Configure the health % to use Potions and Healthstones via the options menu.
