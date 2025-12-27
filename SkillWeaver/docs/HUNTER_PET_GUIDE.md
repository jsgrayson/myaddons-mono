# Complete Hunter Pet Management Guide
**Current for: The War Within (Patch 11.x)**

## Table of Contents
1. [Pet Specializations](#pet-specializations)
2. [Best Pets by Content Type](#best-pets-by-content-type)
3. [Exotic Pets (Beast Mastery Only)](#exotic-pets-beast-mastery-only)
4. [Pet Ability Management](#pet-ability-management)
5. [Taming Guide & Locations](#taming-guide--locations)
6. [Automation Logic](#automation-logic)

---

## Pet Specializations

### Overview
As of Patch 11.1 (The War Within), **all pets can be any specialization**. Change at any Stable Master.


### Ferocity (Offensive)
**Best For:** Raids, Dungeons, DPS Maximization

**Passive:** Predator's Thirst (+10% Leech for hunter and pet)  
**Active:** Primal Rage (30% Haste for 40s - Heroism/Bloodlust equivalent)

**When to Use:**
- Default choice for all group PvE content
- Provides crucial raid buff if no Mage/Shaman present
- Excellent solo sustainability from Leech

### Tenacity (Defensive)
**Best For:** Solo Questing, Tanking, Pet Survivability

**Passive:** Endurance Training (+5% max health for hunter and pet)  
**Active:** Fortitude of the Bear (+20% max health for 10s, heals instantly)

**When to Use:**
- Solo content where pet needs to tank
- Encounters with heavy pet damage
- Leveling

### Cunning (Utility)
**Best For:** PvP, High Mobility Encounters

**Passive:** Pathfinding (+8% movement speed for hunter and pet)  
**Active:** Master's Call (removes roots/snares, 4s immunity)

**When to Use:**
- PvP (essential for root/snare removal)
- Encounters with heavy movement impairment
- M+ with lots of CC

---

## Best Pets by Content Type

### Raiding (High-End PvE)
**Recommended:** **Aqiri (Beetle family)** specced **Tenacity**

**Why Aqiri?**
- Unique passive: +30% movement speed (best pet mobility in game)
- Strong defensive cooldowns when Tenacity
- Fast repositioning = better pet uptime on bosses

**Alternative:** Spirit Beast (Tenacity) - BM Only
- Spirit Mend (heal for hunter or pet)
- Excellent self-sufficiency
- Popular: Loque'nahak, Gondria, Skoll

**Bring Ferocity Pet If:**
- Raid lacks Bloodlust/Heroism (Mage/Shaman missing)
- Swap to Aqiri (Ferocity) for Primal Rage

### Mythic+ Dungeons
**Recommended:** **Ferocity (any pet)** for Bloodlust

**Why Ferocity?**
- Primal Rage essential for timed runs
- Leech helps with incidental damage
- Most M+ groups need lust from hunter

**Best Families:**
- **Mortal Wounds pets** (Carrion Bird, Ravager, Scorpid, Wasp): Reduces enemy healing by 25-50%
- **Aqiri (Ferocity)**: Movement speed + Bloodlust

### Solo/Questing
**Recommended:** **Tenacity** pet with tank abilities

**Best Families:**
- **Clefthooof**: Thick Hide (50% DR when < 40% hp), Blood of the Rhino (+10% armor, +20% healing)
- **Scalehide**: Scale Shield (50% DR for 12s)
- **Spirit Beast** (BM only): Spirit Mend (self-heal)

**Why Tenacity?**
- Pet can tank multiple mobs
- Fortitude of the Bear = instant health boost
- Endurance Training = more survivable

### 3. Raiding (Max DPS & Survival)
**Best Choice:** **Spirit Beast** (BM) or **Tenacity Pet** (Any Spec)
*   **Why:**
    *   **DPS:** Pet damage is normalized (all do same DPS).
    *   **Survival:** **Tenacity** gives +5% Max HP and `Fortitude of the Bear` (Defensive). Dead hunters do 0 DPS.
    *   **Mobility (BM):** **Aqiri** (Tenacity) has +30% movement speed, helping it stick to bosses during heavy movement (indirect DPS gain).
    *   **Utility:** **Spirit Beast** adds a heal (`Spirit Mend`) to help healers.
*   **Note:** Only use **Ferocity** if the raid lacks Lust.

### 4. PvP
**Best Choice:** **Raptor / Hyena / Rodent** (Cunning)** with Mortal Wounds

**Best Choice:** **Undead Raptor** (Nazmir, Shoaljai Tar Pits)
- Cunning specialization (Master's Call)
- Mortal Wounds (reduces enemy healing)
- Pathfinding (+8% movement speed)

**Alternative:** Any Cunning pet with utility (e.g., Scorpid, Wasp)

---

## Pet Family Abilities (The "Core 7")

Every pet family has ONE of these 6 core abilities (plus Exotic abilities for BM).

### 1. Mortal Wounds (Healing Reduction)
**Effect:** Reduces healing received by the target by 50% for 10 sec.
**Families:** Carrion Bird, Devilsaur (Exotic), Direhorn, Hydra, Lizard, Ravager, Riverbeast, Scorpid, Wasp.
**Use:** **Mandatory for PvP**. Useful in M+ for specific mobs (e.g., healers).

### 2. Defense (Damage Reduction)
**Effect:** Reduces damage taken by 50% for 12 sec. (1 min CD)
**Families:** Beetle, Crab, Direhorn, Shale Beast (Exotic), Turtle.
**Use:** **Best for Solo/Tanking**. Use manually or auto-trigger on low health.

### 3. Dodge (Avoidance)
**Effect:** Increases dodge chance by 30% for 20 sec. (1.5 min CD)
**Families:** Cat, Courser, Feathermane (Exotic), Fox, Monkey, Serpent, Wind Serpent.
**Use:** Good for physical damage tanking.

### 4. Magic Defense (Anti-Magic)
**Effect:** Reduces magic damage taken by 70% for 8 sec. (1.5 min CD)
**Families:** Dragonhawk, Ray, Scalehide, Stag, Toad.
**Use:** Specific raid/dungeon mechanics with heavy magic damage.

### 5. Dispel (Purge)
**Effect:** Removes 1 Enrage and 1 Magic effect from an enemy. (10 sec CD)
**Families:** Bat, Nether Ray, Ray, Spirit Beast (Exotic), Sporebat, Stag.
**Use:** **Critical for M+** (removing Raging affix or magic buffs). Note: Hunters also have *Tranquilizing Shot*, so this is a backup/second dispel.

### 6. Slow (Snare)
**Effect:** Reduces movement speed by 50% for 6 sec. (10 sec CD)
**Families:** Basilisk, Bird of Prey, Chimera (Exotic), Crocolisk, Dog, Silithid (Exotic), Spider, Tallstrider, Warp Stalker.
**Use:** PvP (kiting) or M+ (kiting fixated mobs).

### 7. Triggered Defense (Automatic)
**Effect:** When health falls below 40%, reduces damage taken by 60% for 15 sec. (2 min CD)
**Families:** Clefthoof (Exotic), Core Hound (Exotic), Gorilla, Kodo, Ox, Scalehide, Yak.
**Use:** **Lazy Tanking**. Great for solo content as it requires no management.

---

## Exotic Pets (Beast Mastery Only)

### Requirement
- **Must be Beast Mastery spec**
- Level 39+ (some sources say 65 for "Exotic Beasts" passive)

### Top Tier Exotic Pets

#### 1. Spirit Beasts (BEST OVERALL)
**Abilities:**
- **Spirit Mend**: Heal (can cast on self or ally)
- Defensive cooldowns
- Spec: Tenacity (usually)

**Popular Spirit Beasts:**
- **Loque'nahak** (Sholazar Basin, Northrend) - Rare white leopard
- **Gondria** (Zul'Drak, Northrend) - White saber cat
- **Skoll** (Storm Peaks, Northrend) - Blue lightning wolf
- **Ban'thalos** (Mount Hyjal, Cataclysm) - Owl - **HARD TAME** (flies high, requires special positioning)
- **Karoma** (Twilight Highlands, Cataclysm) - Wolf
- **Arcturus** (Grizzly Hills, Northrend) - Bear
- **Gara** (Shadowmoon Valley, Draenor) - Questline required
- **Bloodgullet** (Ohn'ahran Plains, Dragonflight) - Spectral Armoredon
- **Aridan** (Algeth'ar Academy dungeon, Dragonflight) - **Requires defeating first boss, use Void's Guard Storm Hammer**
- **TWW Spirit Beasts**: Check Khaz Algar zones for new Spirit Beast spawns

#### 2. Devilsaurs
**Abilities:**
- Mortal Wounds (reduces enemy healing)
- Spec: Ferocity

**Popular Devilsaurs:**
- **Rezan** (Atal'Dazar dungeon, BfA) - Undead Devilsaur - **Requires Simple Tome of Bone-Binding**

#### 3. Aqiri (Beetles)
**Abilities:**
- +30% Movement Speed (unique passive)
- Spec: Tenacity or Ferocity

**Location:** Various beetle-type creatures across expansions

#### 4. Clefthooves
**Abilities:**
- Thick Hide (50% DR when < 40% hp)
- Blood of the Rhino (+10% armor, +20% healing)
- Spec: Tenacity (extreme tankiness)

#### 5. Core Hounds
**Abilities:**
- Defensive cooldowns
- Spec: Ferocity

---

## Exotic Pet Abilities (BM Only)

### 1. Spirit Mend (Spirit Beast)
**Effect:** Heals a friendly target for a large amount + HoT.
**Use:** Emergency heal for self or tank.

### 2. Surface Trot (Water Strider)
**Effect:** Allows walking on water.
**Use:** Open world convenience.

### 3. Updraft (Feathermane)
**Effect:** Slow fall for 30 sec.
**Use:** Surviving falls in open world/raids.

### 4. Molten Hide (Core Hound)
**Effect:** Deals Fire damage to attackers.
**Use:** Passive DPS increase for tanking.

### 5. Feast (Devilsaur)
**Effect:** Eats a humanoid/beast corpse to heal 20% health and restore 20 focus.
**Use:** Downtime recovery.

### 6. Shell Shield (Turtle/Beetle/Krolusk)
**Effect:** Reduces damage by 50% for 12 sec.
**Use:** Active mitigation.

### 7. Solid Shell (Krolusk)
**Effect:** Reduces damage by 50% for 12 sec.
**Use:** Active mitigation.

---

## Pet Ability Management

### Growl (Taunt) - CRITICAL MANAGEMENT

**Problem:** Growl causes pets to pull aggro from tanks in groups/raids

**Solution:** Automatic toggle based on solo vs group status

```lua
-- Auto-disable Growl when entering group content
{ command = "/cast [pet] Growl", conditions = "pet_exists and not in_group and not pet:buff:Growl" }, -- Enable solo
{ command = "/cast [pet] Growl", conditions = "pet_exists and in_group and pet:buff:Growl" }, -- Disable in group
```

**Manual Macro (Alternative):**
```
/petautocasttoggle Growl
```

**Key Notes:**
- Modern WoW automatically disables Growl in dungeons/raids (usually)
- Growl does NOT work on most raid bosses
- Solo questing: Growl ON
- Groups/Raids: Growl OFF (always)

### Primal Rage (Bloodlust)

**When to Use:**
- Raid: On pull or during execute phase (< 30% boss hp)
- M+: On high-priority packs or bosses
- Solo: Rarely needed

```lua
{ command = "/cast [pet] Primal Rage", conditions = "pet_specialization == Ferocity and in_group and (heroism_needed or boss_health < 30)" },
```

### Master's Call

**When to Use:**
- Self: When rooted or snared
- Ally: When ally is rooted (PvP or specific PvE mechanics)

```lua
{ command = "/cast [target=player] Master's Call", conditions = "rooted or snared" },
{ command = "/cast [target=mouseover,help] Master's Call", conditions = "in_group and ally_rooted" },
```

### Spirit Mend (Spirit Beasts Only)

**When to Use:**
- Emergency self-heal (< 35% health)
- Ally heal in emergencies (< 20% health)

```lua
{ command = "/cast [target=player] Spirit Mend", conditions = "health < 35 and pet_family == Spirit Beast" },
{ command = "/cast [target=mouseover,help] Spirit Mend", conditions = "in_group and ally_health < 20 and pet_family == Spirit Beast" },
```

---

## Taming Guide & Locations

### Basic Taming Process
1. **Find the beast** (see locations below)
2. **Freeze or trap** (if aggressive): `/cast Freezing Trap` or `/cast Concussive Shot`
3. **Cast Tame Beast**: Channel completes after ~6 seconds
4. **Success!** Pet added to your collection

### Special Taming Requirements

#### Mechanical Pets
**Requirement:** **Mecha-Bond Imprint Matrix**
- Crafted by Engineers or purchased on AH
- Gnomes, Goblins, Mechagnomes: No item needed

**Popular Mechanical Pets:**
- **Tekton** (near Stormwind) - Mechanical Sheep - **Must freeze before it explodes!**
- **OOX-Fleetfoot/MG** (Mechagon Island) - Rocket Chicken - **Only available when Olgthorp visits Mechagon**

#### Undead Pets
**Requirement:** **Simple Tome of Bone-Binding**
- Drops from Maldraxxus mobs/dungeons (Shadowlands): Plaguefall, Theater of Pain
- Undead Hunters: No item needed

**Popular Undead Pets:**
- **Rezan** (Atal'Dazar dungeon) - Undead Devilsaur
- **Undead Raptors** (Nazmir, Shoaljai Tar Pits)

#### Lesser Dragonkin (Previous Expansions)
**Requirement:** **Lesser Dragonkin Taming** skill
- Reach Renown 23 with Valdrakken Accord faction (Dragonflight)
- Still available to tame if you have the skill unlocked

**Popular Lesser Dragonkin:**
- **Primal Thunder Lizards** (Ohn'ahran Plains, The Azure Span - Dragonflight zones)

#### Feathermanes/Slyverns
**Requirement:** **Tome of Hybrid Beast Taming**
- Acquired through Hunter Class Hall questline (Legion expansion)

#### Ottuks (Dragonflight)
**Requirement:** **Ottuk Training**
- Reach Renown 11 with Iskaara Tuskarr (Dragonflight faction)
- Still available if requirement met

#### Blood Beasts
**Requirement:** **Blood-Soaked Tome of Dark Whispers**
- Guaranteed drop from Zul in Uldir raid (Battle for Azeroth)

### Notable Rare Tames

#### Ban'thalos (Spirit Beast - Owl)
**Location:** Mount Hyjal (flies high in sky)
**Taming Method:**
1. Bring a Feathermane pet (with Updraft ability)
2. Use **Fruit Basket** toy to stand on
3. Use Updraft to get height
4. Tame Ban'thalos while airborne (do NOT damage it!)

#### Aridan (Spirit Beast)
**Location:** Algeth'ar Academy dungeon
**Taming Method:**
1. Enter dungeon
2. Defeat first boss
3. Use **Void's Guard Storm Hammer** (item you receive) on Aridan
4. Tame while stunned

#### Thornbeasts (Dragonflight)
**Location:** Emerald Dream zone
**Taming Method:**
1. Obtain **Thorn-Laden Heart** from killing specific animals
2. Spawn tamable version
3. Tame quickly

---

## Automation Logic

### Pet Selection Logic

#### Solo Play
```lua
-- Summon Tenacity pet for solo questing
{ command = "/cast Call Pet 1", conditions = "not in_group and not pet_exists and pet_slot_1_spec == Tenacity" },

-- Enable Growl (tank mode)
{ command = "/cast [pet] Growl", conditions = "pet_exists and not in_group and not pet:buff:Growl" },
```

#### Group/Raid Play
```lua
-- Summon Ferocity pet for Bloodlust
{ command = "/cast Call Pet 2", conditions = "in_group and not pet_exists and pet_slot_2_spec == Ferocity" },

-- Disable Growl (avoid pulling aggro)
{ command = "/cast [pet] Growl", conditions = "pet_exists and in_group and pet:buff:Growl" },
```

### Misdirection Logic (CRITICAL)

#### Solo: Redirect to Pet
```lua
-- Misdirect to pet (solo tank)
{ command = "/cast [target=pet] Misdirection", conditions = "not in_group and pet_exists and cooldown:Misdirection == 0" },
{ command = "/cast [target=pet] Misdirection", conditions = "not in_group and pet_exists and pull_timer < 1" }, -- Pull opener
```

#### Group: Redirect to Tank
```lua
-- Misdirect to focus (tank)
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank and cooldown:Misdirection == 0" },
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank and pull_timer < 1" }, -- Pull opener
```

### Pet Health Management
```lua
-- Mend Pet (ongoing heal)
{ command = "/cast Mend Pet", conditions = "pet_exists and pet_health < 60 and not buff:Mend Pet" },

-- Revive Pet (out of combat)
{ command = "/cast Revive Pet", conditions = "pet_dead and not in_combat" },
```

### Complete Priority List
```lua
-- 1. Pet Summon
{ command = "/cast Call Pet 1", conditions = "not pet_exists and not in_combat" },

-- 2. Growl Management
{ command = "/cast [pet] Growl", conditions = "pet_exists and not in_group and not pet:buff:Growl" }, -- Enable solo
{ command = "/cast [pet] Growl", conditions = "pet_exists and in_group and pet:buff:Growl" }, -- Disable group

-- 3. Pet Attack
{ command = "/petattack", conditions = "pet_exists and target_attackable and not pet_attacking" },

-- 4. Misdirection (solo vs group)
{ command = "/cast [target=focus] Misdirection", conditions = "in_group and focus_role == tank and pull_timer < 1" }, -- Group opener
{ command = "/cast [target=pet] Misdirection", conditions = "not in_group and pet_exists and pull_timer < 1" }, -- Solo opener

-- 5. Pet Health
{ command = "/cast Mend Pet", conditions = "pet_exists and pet_health < 60" },

-- 6. Pet Abilities (situational)
{ command = "/cast [pet] Primal Rage", conditions = "pet_specialization == Ferocity and in_group and heroism_needed" },
{ command = "/cast [target=player] Master's Call", conditions = "rooted or snared" },
{ command = "/cast [target=player] Spirit Mend", conditions = "health < 35 and pet_family == Spirit Beast" },
```

---

## Pet Stable Recommendations

### 5 Active Call Pet Slots (Recommended Setup)

**Slot 1: Solo Tenacity Tank**
- **Pet:** Clefthoof or Spirit Beast (BM)
- **Spec:** Tenacity
- **Use:** Solo questing, world content

**Slot 2: Raid Ferocity Bloodlust**
- **Pet:** Aqiri (Beetle) or any Ferocity
- **Spec:** Ferocity
- **Use:** Raids, M+ (Bloodlust)

**Slot 3: Raid Tenacity DPS**
- **Pet:** Aqiri (Beetle) or Spirit Beast (BM)
- **Spec:** Tenacity
- **Use:** Raids when Bloodlust covered by others

**Slot 4: PvP Cunning**
- **Pet:** Undead Raptor (with Mortal Wounds)
- **Spec:** Cunning
- **Use:** PvP arenas/battlegrounds

**Slot 5: Utility/Exotic**
- **Pet:** Devilsaur or Core Hound (BM)
- **Spec:** Ferocity
- **Use:** Situational (Mortal Wounds, specific encounters)

---

## Quick Reference: Best Pets Summary

| Content | Spec | Pet Family | Key Reason |
|---------|------|------------|------------|
| **Raids** | Tenacity | Aqiri (Beetle) | +30% move speed, def CDs |
| **1** | **Animal Companion** | *Your Choice* | **BM Only:** This slot is summoned as your 2nd pet. It is **COSMETIC ONLY** (does not use abilities). Pick your coolest looking pet! |
| **2** | **General / Lust** | **Ferocity** (e.g., Bat, Ray, Clefthoof) | Your default. Provides `Primal Rage` (Lust) + Leech. |
| **3** | **Tank / Solo** | **Tenacity** (e.g., Scalehide, Spirit Beast) | Maximum defense. `Fortitude of the Bear` + `Defense` ability. |
| **4** | **PvP / Mobile** | **Cunning** (e.g., Raptor, Hyena) | `Master's Call` (Freedom) + `Mortal Wounds` (Healing Reduction). |
| **5** | **Utility / Dispel** | **Spirit Beast** (BM) or **Bat** (Any) | Specific dispel utility or extra healing. |

### "Must-Have" Pets to Tame
1.  **Clefthoof (BM Only):** The ultimate tank. Has `Blood of the Rhino` (passive armor/healing) + `Triggered Defense`.
2.  **Spirit Beast (BM Only):** Provides `Spirit Mend` (an extra heal) and a dispel.
3.  **Bat/Nether Ray (Any Spec):** Provides `Primal Rage` (Bloodlust/Heroism effect) and a dispel.
4.  **Raptor/Hyena (Any Spec):** Provides `Mortal Wounds` (healing reduction) and `Master's Call` (freedom effect).
5.  **Aqiri (Any Spec):** Provides `Shell Shield` (defensive CD) and `Dust Cloud` (AoE slow).

---

## Additional Resources

- **Visual Resource:**
For a complete visual database of every tameable look in the game, visit **[WoW-Petopia](https://www.wow-petopia.com)**.

---

## Cool & Unique Looks (The "Flex" Pets)

If you want to stand out, here are some of the most visually distinct pets in the game.

### 1. Spirit Beasts (Spectral/Transparent)
*   **Loque'nahak:** Unique spotted spirit leopard. Rare spawn in Sholazar Basin.
*   **Gondria:** Spectral purple tiger. Rare spawn in Zul'Drak.
*   **Arcturis:** Spectral bear. Rare spawn in Grizzly Hills.
*   **Ban'thalos:** Green spectral owl. Rare spawn high above Mount Hyjal (requires flying).
*   **Elegon:** Astral/Starry Cloud Serpent. Boss in Mogu'shan Vaults (Spirit Beast family, but looks like a dragon).

### 2. Unique Models
*   **Fenryr:** Golden spectral wolf. Tameable in Halls of Valor (Mythic) after soloing the dungeon up to him.
*   **Lalathin:** Bright pink Mana Ray. Found in Suramar (World Quest area).
*   **Faultline:** "Fire-glowing" Clefthoof. Summoned by Beastlord Darmac in Blackrock Foundry.
*   **Oondasta:** Armored Devilsaur with a cannon. World Boss in Isle of Giants (Pandaria).
*   **Thok the Bloodthirsty:** Armored Devilsaur. Boss in Siege of Orgrimmar.

### 3. Mechanicals
*   **Friender:** Mechanical wolf with a distinct blue/red alarm light. Found in Gnomeregan (requires puzzle).
*   **Optimo:** Mechanical dog. Rare in Mechagon.
*   **A-Me 02:** Mechanical gorilla. Un'Goro Crater quest reward.

---

**Final Tips:**
1. Always have multiple pets with different specs stabled
2. Disable Growl in ALL group content (automated)
3. Use Misdirection on CD (to pet solo, to tank in groups)
4. Spirit Beasts = Best all-around exotic pets (BM only)
5. Aqiri = Best non-exotic for raiding (movement speed OP)
