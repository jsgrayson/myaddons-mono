# All NPC Strategies (Xufu Scrape)

## The War Within

### World Quests

#### Rock Collector
**URL:** [https://www.wow-petguide.com/Encounter/1589/Rock_Collector](https://www.wow-petguide.com/Encounter/1589/Rock_Collector)

##### Strategy: Default Strategy
```text
use(Curse of Doom:218)
use(Unholy Ascension:321)
use(Poison Protocol:1954) [round=3]
use(Void Nova:2356) [round=4]
change(#3) [round=5]
use(Carpnado:1287)
use(Water Jet:118)
use(Void Nova:2356) [self(#3).dead]
use(Ooze Touch:445) [self(#3).dead]
change(#2)
```

#### Robot Rumble
**URL:** [https://www.wow-petguide.com/Encounter/1590/Robot_Rumble](https://www.wow-petguide.com/Encounter/1590/Robot_Rumble)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
use(Chop:943) [!enemy.aura(Bleeding:491).exists]
use(BONESTORM!!:1762)
use(Chop:943)
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
use(Flock:581)
standby
change(next)
```

#### The Power of Friendship
**URL:** [https://www.wow-petguide.com/Encounter/1592/The_Power_of_Friendship](https://www.wow-petguide.com/Encounter/1592/The_Power_of_Friendship)

##### Strategy: Default Strategy
```text
use(Poison Fang:152) [round=1]
use(Pheromones:1063)
use(Puncture Wound:1050)
use(Minefield:634)
use(Explode:282)
use(Devour:538)
use(Rampage:124)
change(next)
```

#### Major Malfunction
**URL:** [https://www.wow-petguide.com/Encounter/1593/Major_Malfunction](https://www.wow-petguide.com/Encounter/1593/Major_Malfunction)

##### Strategy: Default Strategy
```text
use(Thunderbolt:779) [round=1]
use(Explode:282)
use(Call Blizzard:206)
use(#1)
change(next)
```

#### Miniature Army
**URL:** [https://www.wow-petguide.com/Encounter/1595/Miniature_Army](https://www.wow-petguide.com/Encounter/1595/Miniature_Army)

##### Strategy: Default Strategy
```text
use(Swarm of Flies:232) [round=1]
change(#2) [round=2]
use(Time Bomb:602) [round=3]
use(Armageddon:1025)
use(Booby-Trapped Presents:1080) [round=5]
use(Call Blizzard:206) [round=6]
use(Ice Lance:413)
use(#1)
change(#3)
```

#### The Thing from the Swamp
**URL:** [https://www.wow-petguide.com/Encounter/1596/The_Thing_from_the_Swamp](https://www.wow-petguide.com/Encounter/1596/The_Thing_from_the_Swamp)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Unholy Ascension:321)
ability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
ability(Flock:581)
ability(Thunderbolt:779)
ability(Breath:115)
change(next)
```

#### Ziriak
**URL:** [https://www.wow-petguide.com/Encounter/1598/Ziriak](https://www.wow-petguide.com/Encounter/1598/Ziriak)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Undead:242).exists]
use(Wind Buffet:1963) [enemy(#1).active]
change(#2) [round=2]
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Quicksand:912)
use(Sandstorm:453)
change(#1) [enemy(#2).active]
change(#3) [enemy(#1).active]
```

#### One Hungry Worm
**URL:** [https://www.wow-petguide.com/Encounter/1599/One_Hungry_Worm](https://www.wow-petguide.com/Encounter/1599/One_Hungry_Worm)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Underground:340).exists & self.speed.fast]
use(Glowing Toxin:270) [!enemy.aura(Glowing Toxin:271).exists]
use(Explode:282)
use(Call Lightning:204)
change(next)
```

### The Undermine

## Dragonflight

### World Quests

#### To a Land Down Under
**URL:** [https://www.wow-petguide.com/Encounter/1526/To_a_Land_Down_Under](https://www.wow-petguide.com/Encounter/1526/To_a_Land_Down_Under)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Corrosion:446).exists & round=3]
standby [self(#1).active & round>2]

use(Poison Protocol:1954)
use(Corrosion:447)
use(Flame Breath:501) [round=3 & !enemy.aura(Corrosion:446).exists]
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204) [enemy(#3).active]
use(Counterspell:308) [enemy(#2).active]
standby [self(#3).active & enemy(#2).active & enemy.aura(601).exists]
use(Reckless Strike:186)
change(next)
```

#### Are They Not Beautiful?
**URL:** [https://www.wow-petguide.com/Encounter/1527/Are_They_Not_Beautiful](https://www.wow-petguide.com/Encounter/1527/Are_They_Not_Beautiful)

##### Strategy: Default Strategy
```text
change(#3) [enemy(#3).active & !self.aura(242).exists]
use(Prowl:536) [!enemy(#2).dead]
use(Call Darkness:256)
use(Spectral Strike:442)
use(Arcane Dash:1536)
if [enemy(#3).active]
use(Howl:362)
use(Shadowmeld:2253)
use(Surge of Power:593) [!weather(Darkness:257) & self(Salverun:3545).active]
use(Surge of Power:593) [self(Chrominius:1152).active]
endif
use(#1) [round>3]
change(next)
```

#### Delver Mardei
**URL:** [https://www.wow-petguide.com/Encounter/1528/Delver_Mardei](https://www.wow-petguide.com/Encounter/1528/Delver_Mardei)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025) [ enemy.aura(Flame Breath:500).exists ]
use(Flame Breath:501)
use(Ice Tomb:624) [ !enemy.is(Dustie:3568) ]
use(Arcane Storm:589)
use(Breath:115)
if [ enemy.is(Dustie:3568) ]
    use(Howl:362) [ enemy.hp>1665 & self.aura(Dragonkin:245).exists ]
    use(Howl:362) [ enemy.hp>1110 & !self.aura(Dragonkin:245).exists ]
    use(Surge of Power:593)
endif
use(Bite:110)
change(next)
```

#### Do You Even Train?
**URL:** [https://www.wow-petguide.com/Encounter/1529/Do_You_Even_Train](https://www.wow-petguide.com/Encounter/1529/Do_You_Even_Train)

##### Strategy: Default Strategy
```text
quit [round=9 & enemy(#1).active]
standby [round=9]
change(#2) [round=2]
change(#1) [round=10]
use(Tail Smash:2214) [enemy(#1).active]
use(Slither:929)
use(Time Bomb:602)
use(Armageddon:1025) [round=5]
use(Puncture Wound:1050) [round>11]
use(Great Sting:1966)
use(Enrage:1392) [round=7]
use(Puncture Wound:1050)
use(#1)
change(next)
```

#### Swog the Elder
**URL:** [https://www.wow-petguide.com/Encounter/1366/Swog_the_Elder](https://www.wow-petguide.com/Encounter/1366/Swog_the_Elder)

##### Strategy: Default Strategy
```text
use(2223)
use(377)
```

#### The Terrible Three
**URL:** [https://www.wow-petguide.com/Encounter/1367/The_Terrible_Three](https://www.wow-petguide.com/Encounter/1367/The_Terrible_Three)

##### Strategy: Default Strategy
```text
standby [round=5]
use(Corrosion:447) [round=1]
use(Void Nova:2356)
use(Poison Protocol:1954)
use(Corrosion:447)
use(Armageddon:1025)
use(Surge of Power:593) [self.aura(Dragonkin:245).exists]
use(Bite:110)
change(next)
--
```

#### Sharp as Flint
**URL:** [https://www.wow-petguide.com/Encounter/1497/Sharp_as_Flint](https://www.wow-petguide.com/Encounter/1497/Sharp_as_Flint)

##### Strategy: Default Strategy
```text
change(#2) [round=2]
use(Razor Talons:2237) [round~4,6]
use(Armageddon:1025) [round>6]
use(Geyser:418)
if [enemy(#3).active]
use(Call Darkness:256) [enemy(#3).hp<=1811 & !enemy.ability(Digest Brains:1065).usable]
use(Call Darkness:256) [enemy(#3).hp<=1492]
endif
use(Nocturnal Strike:517) [weather(Darkness:257).duration!=0]
use(#1)
change(next)
```

#### Adinakon
**URL:** [https://www.wow-petguide.com/Encounter/1498/Adinakon](https://www.wow-petguide.com/Encounter/1498/Adinakon)

##### Strategy: Default Strategy
```text
ability(Explode:282)
ability(Call Darkness:256)
change(next)
```

#### Two and Two Together
**URL:** [https://www.wow-petguide.com/Encounter/1369/Two_and_Two_Together](https://www.wow-petguide.com/Encounter/1369/Two_and_Two_Together)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Explode:282) [enemy.hp.can_explode]
use(Powerball:566) [round=3]
use(Wind-Up:459)
change(next)
```

#### Eye of the Stormling
**URL:** [https://www.wow-petguide.com/Encounter/1370/Eye_of_the_Stormling](https://www.wow-petguide.com/Encounter/1370/Eye_of_the_Stormling)

##### Strategy: Default Strategy
```text
ability(Explode:282)
ability(Pump:297)
change(next)
```

#### Paws of Thunder
**URL:** [https://www.wow-petguide.com/Encounter/1499/Paws_of_Thunder](https://www.wow-petguide.com/Encounter/1499/Paws_of_Thunder)

##### Strategy: Default Strategy
```text
use(Toxic Fumes:2349)
use(Poison Protocol:1954)
use(Time Bomb:602)
use(Armageddon:1025)

standby [enemy(#2).active & enemy.hp<733 & enemy.aura(601).duration=1]
if [enemy(#2).aura(927).exists]
use(Puncture Wound:1050)
standby [enemy(#2).active]
endif

use(Impale:800)
use(Slicing Wind:420)
change(next)
```

#### Lyver
**URL:** [https://www.wow-petguide.com/Encounter/1500/Lyver](https://www.wow-petguide.com/Encounter/1500/Lyver)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Black Claw:919) [ !enemy.aura(Black Claw:918).exists ]
use(Hunting Party:921)
change(next)
```

#### The Grand Master
**URL:** [https://www.wow-petguide.com/Encounter/1372/The_Grand_Master](https://www.wow-petguide.com/Encounter/1372/The_Grand_Master)

##### Strategy: Default Strategy
```text
change(#2) [round=6]
use(Ice Tomb:624) [enemy(#1).active]
use(Call Blizzard:206) [round=2]
use(Ice Lance:413)
use(Poison Protocol:1954)
use(Void Nova:2356)
use(Corrosion:447)
change(#3)
```

#### Mini Manafiend Melee
**URL:** [https://www.wow-petguide.com/Encounter/1373/Mini_Manafiend_Melee](https://www.wow-petguide.com/Encounter/1373/Mini_Manafiend_Melee)

##### Strategy: Default Strategy
```text
use(Blinding Powder:1015)
use(Explode:282)
use(Armageddon:1025) [enemy.hp<531]
use(Razor Talons:2237) [!enemy.aura(2238).exists]
use(Flame Breath:501)
change(next)
```

#### A New Vocation
**URL:** [https://www.wow-petguide.com/Encounter/1501/A_New_Vocation](https://www.wow-petguide.com/Encounter/1501/A_New_Vocation)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Dodge:311).exists]
ability(Bubble:934) [enemy.aura(Flying:341).exists]
ability(Dive:564) [enemy.aura(Flying:341).exists]
ability(Arcane Storm:589)
ability(Mana Surge:489)
ability(#1)
change(next)
```

#### Enok the Stinky
**URL:** [https://www.wow-petguide.com/Encounter/1502/Enok_the_Stinky](https://www.wow-petguide.com/Encounter/1502/Enok_the_Stinky)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652) [round=3]
ability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
ability(Flock:581)
ability(Hunting Party:921)
ability(Leap:364)
ability(#1)
change(next)
```

#### You Have to Start Somewhere
**URL:** [https://www.wow-petguide.com/Encounter/1375/You_Have_to_Start_Somewhere](https://www.wow-petguide.com/Encounter/1375/You_Have_to_Start_Somewhere)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [enemy(#3).active]
use(Surge of Power:593) 
use(Explode:282)
endif
use(#2) [enemy.round=2]
use(#1)
change(next)
```

#### The Oldest Dragonfly
**URL:** [https://www.wow-petguide.com/Encounter/1376/The_Oldest_Dragonfly](https://www.wow-petguide.com/Encounter/1376/The_Oldest_Dragonfly)

##### Strategy: Default Strategy
```text
change(#1) [self(#3).active]
use(Illuminate:460)
use(Soul Ward:751) [round=6 & self.hp<1063]
use(Light:461) [round>2]
use(Beam:114) [round>2]
use(Blinding Powder:1015)
use(Explode:282)
change(next)
```

#### They're Full of Stars!
**URL:** [https://www.wow-petguide.com/Encounter/1503/They're_Full_of_Stars!](https://www.wow-petguide.com/Encounter/1503/They're_Full_of_Stars!)

##### Strategy: Default Strategy
```text
use(Explode:282) [enemy.hp.can_explode]
use(Prowl:536) [!self.aura(Undead:242).exists]
use(Call Darkness:256)
use(#1)
change(next)
```

#### Right Twice a Day
**URL:** [https://www.wow-petguide.com/Encounter/1504/Right_Twice_a_Day](https://www.wow-petguide.com/Encounter/1504/Right_Twice_a_Day)

##### Strategy: Default Strategy
```text
ability(Fire Shield:1754)
ability(Lightning Shield:906)
ability(Flamethrower:503)
change(next)
```

### The Forbidden Reach

#### Storm-Touched Swoglet
**URL:** [https://www.wow-petguide.com/Encounter/1521/Storm-Touched_Swoglet](https://www.wow-petguide.com/Encounter/1521/Storm-Touched_Swoglet)

##### Strategy: Default Strategy
```text
ability(Explode:282) [round~1,3]
ability(Flyby:515)
ability(Call Darkness:256)
ability(Nocturnal Strike:517)
change(next)
```

#### Vortex - Legendary
**URL:** [https://www.wow-petguide.com/Encounter/1506/Vortex_-_Legendary](https://www.wow-petguide.com/Encounter/1506/Vortex_-_Legendary)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786) 
use(Chop:943) [round=2] 
use(BONESTORM!!:1762) 
change(Ikky:1532) [self(Boneshard:1963).dead] 
use(Flock:581) [enemy.aura(Black Claw:918).exists] 
use(Black Claw:919)
```

#### Vortex - Epic
**URL:** [https://www.wow-petguide.com/Encounter/1507/Vortex_-_Epic](https://www.wow-petguide.com/Encounter/1507/Vortex_-_Epic)

##### Strategy: Default Strategy
```text
ability(Time Bomb:602)
ability(Armageddon:1025)
ability(Stampede:163) [self.round=2]
ability(Corpse Explosion:663) [enemy.aura(Shattered Defenses:542).exists]
ability(Rabid Strike:666)
ability(Squeeze:1572)
ability(Grasp:249)
change(next)
```

#### Vortex - Rare
**URL:** [https://www.wow-petguide.com/Encounter/1508/Vortex_-_Rare](https://www.wow-petguide.com/Encounter/1508/Vortex_-_Rare)

##### Strategy: Default Strategy
```text
use(haunt:652)
use(claw:919) [ !enemy.aura(claw:918).exists ]
use(finisher:921)
change(next)
```

#### Storm-Touched Skitterer
**URL:** [https://www.wow-petguide.com/Encounter/1522/Storm-Touched_Skitterer](https://www.wow-petguide.com/Encounter/1522/Storm-Touched_Skitterer)

##### Strategy: Default Strategy
```text
use(claw:919) [ !enemy.aura(claw:918).exists ]
use(flock:581) [ !enemy.aura(flock:542).exists ]
use(filler:184)
```

#### Wildfire - Legendary
**URL:** [https://www.wow-petguide.com/Encounter/1510/Wildfire_-_Legendary](https://www.wow-petguide.com/Encounter/1510/Wildfire_-_Legendary)

##### Strategy: Default Strategy
```text
use(Illuminate:460)
use(Murder the Innocent:2223)
change(next)
```

#### Wildfire - Epic
**URL:** [https://www.wow-petguide.com/Encounter/1511/Wildfire_-_Epic](https://www.wow-petguide.com/Encounter/1511/Wildfire_-_Epic)

##### Strategy: Default Strategy
```text
ability(Blistering Cold:786)
ability(Chop:943) [!enemy.aura(Bleeding:491).exists]
ability(BONESTORM!!:1762) [!self.aura(Undead:242).exists]
ability(Chop:943)

ability(Primal Cry:920)
ability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
ability(Hunting Party:921)

ability(Stampede:163)
ability(Scratch:119)

change(next)
```

#### Wildfire - Rare
**URL:** [https://www.wow-petguide.com/Encounter/1512/Wildfire_-_Rare](https://www.wow-petguide.com/Encounter/1512/Wildfire_-_Rare)

##### Strategy: Default Strategy
```text
ability(Black Claw:919) [round=1]
ability(Flock:581)
ability(#1)
change(next)
```

#### Storm-Touched Slyvern
**URL:** [https://www.wow-petguide.com/Encounter/1523/Storm-Touched_Slyvern](https://www.wow-petguide.com/Encounter/1523/Storm-Touched_Slyvern)

##### Strategy: Default Strategy
```text
ability(Immolate:178) [!enemy.aura(Immolate:177).exists]
ability(Flyby:515) [!enemy.aura(Weakened Defenses:516).exists]
ability(Explode:282)
ability(Gift of Winter's Veil:586)
change(next)
```

#### Tremblor - Legendary
**URL:** [https://www.wow-petguide.com/Encounter/1514/Tremblor_-_Legendary](https://www.wow-petguide.com/Encounter/1514/Tremblor_-_Legendary)

##### Strategy: Default Strategy
```text
use(Wild Magic:592) [round=1]
use(Illuminate:460)
use(Murder the Innocent:2223)
change(next)
```

#### Tremblor - Epic
**URL:** [https://www.wow-petguide.com/Encounter/1515/Tremblor_-_Epic](https://www.wow-petguide.com/Encounter/1515/Tremblor_-_Epic)

##### Strategy: Default Strategy
```text
ability(Tail Sweep:122) [self.speed.fast & !self(#2).dead]
ability(Call Lightning:204)

ability(Blistering Cold:786)
ability(Chop:943) [!enemy.aura(Bleeding:491).exists]
ability(BONESTORM!!:1762)

ability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
ability(Hunting Party:921)

change(#1)
change(#2)
change(#3)
```

#### Tremblor - Rare
**URL:** [https://www.wow-petguide.com/Encounter/1516/Tremblor_-_Rare](https://www.wow-petguide.com/Encounter/1516/Tremblor_-_Rare)

##### Strategy: Default Strategy
```text
ability(Black Claw:919) [round=1]
ability(Flock:581) [round=2]
ability(Explode:282)
ability(#1)
change(next)
```

#### Storm-Touched Ohuna
**URL:** [https://www.wow-petguide.com/Encounter/1524/Storm-Touched_Ohuna](https://www.wow-petguide.com/Encounter/1524/Storm-Touched_Ohuna)

##### Strategy: Default Strategy
```text
standby [ round = 1 ]
use(curse:218)
use(haunt:652)
use(claw:919) [ !enemy.aura(claw:918).exists ]
use(flock:581)
change(next)
```

#### Flow - Legendary
**URL:** [https://www.wow-petguide.com/Encounter/1518/Flow_-_Legendary](https://www.wow-petguide.com/Encounter/1518/Flow_-_Legendary)

##### Strategy: Default Strategy
```text
ability(Time Bomb:602)
ability(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]
ability(Armageddon:1025)

ability(Rabid Strike:666) [!enemy.aura(Rabies:807).exists]
ability(Corpse Explosion:663)

ability(Rip:803) [!enemy.aura(Bleeding:491).exists]
ability(Blood in the Water:423)
ability(Surge:509)

change(next)
```

#### Flow - Epic
**URL:** [https://www.wow-petguide.com/Encounter/1519/Flow_-_Epic](https://www.wow-petguide.com/Encounter/1519/Flow_-_Epic)

##### Strategy: Default Strategy
```text
ability(Time Bomb:602)
ability(Armageddon:1025)

ability(Rabid Strike:666) [!enemy.aura(Rabies:807).exists]
ability(Corpse Explosion:663)

ability(Rip:803) [!enemy.aura(Bleeding:491).exists]
ability(Blood in the Water:423)
ability(Surge:509)

change(next)
```

#### Flow - Rare
**URL:** [https://www.wow-petguide.com/Encounter/1520/Flow_-_Rare](https://www.wow-petguide.com/Encounter/1520/Flow_-_Rare)

##### Strategy: Default Strategy
```text
ability(Black Claw:919) [round=1]
ability(Flock:581)
ability(Explode:282)
ability(#1)
change(next)
```

#### https://www.wow-petguide.com/Strategy/18465/Right_Twice_a_Day
**URL:** [https://www.wow-petguide.com/Strategy/18465/Right_Twice_a_Day](https://www.wow-petguide.com/Strategy/18465/Right_Twice_a_Day)

##### Strategy: Default Strategy
```text
ability(Forboding Curse:1068) [!enemy.aura(Forboding Curse:1067).exists]
ability(Corpse Explosion:663)
ability(Fire Shield:1754)
ability(Lightning Shield:906)
ability(Flamethrower:503)
change(next)
```

### Zaralek Cavern

#### Humanoid Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1530](https://www.wow-petguide.com/Encounter/1530)

##### Strategy: Default Strategy
```text
change(#2) [round=4]
change(#2) [enemy(#1).active & enemy.aura(Stunned:927).exists]

ability(Creeping Insanity:1760) [round=1]
ability(Soulrush:752) [round=2]

ability(Stampede:163) [enemy(#3).active]
ability(Bubble:934) [self.aura(Whirlpool:512).duration=1]

ability(Call Lightning:204) [enemy.hp<1246 & enemy.aura(Tough n' Cuddly:1111).exists & enemy.aura(Shattered Defenses:542).exists]
ability(Call Lightning:204) [!enemy.aura(Tough n' Cuddly:1111).exists]

ability(#1)
change(next)
```

#### Dragonkin Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1534](https://www.wow-petguide.com/Encounter/1534)

##### Strategy: Default Strategy
```text
ability(Emerald Presence:597) [round=1]

ability(Lift-Off:170) [self.aura(Whirlpool:512).duration=1]
ability(Dragon's Call:2283)

ability(Call Lightning:204) [enemy(#3).active & !enemy.aura(Tough n' Cuddly:1111).exists]
ability(Call Lightning:204) [enemy(#3).active & enemy.hp<823 & enemy.aura(Tough n' Cuddly:1111).exists & self.aura(Dragonkin:245).exists]
ability(Call Lightning:204) [enemy(#3).active & enemy.hp<529 & enemy.aura(Tough n' Cuddly:1111).exists]

ability(Thunderbolt:779)

ability(#1)
change(next)
```

#### Flying Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1538](https://www.wow-petguide.com/Encounter/1538)

##### Strategy: Default Strategy
```text
change(#3) [ round=12 & !self(#3).played ]
use(Shadow Talon:1238) [ enemy.is(Murrey:3558) ]
use(Void Tremors:2360)
use(Shadowmeld:2253)
use(Preen:1545) [ enemy.is(Clawz:3559) & self.aura(Pumped Up:296).exists ]
use(Rush:567) [ enemy.is(Murrey:3558) & enemy.round!~1,3 ]
use(Rush:567) [ enemy.hp<400 & !self.aura(Pumped Up:296).exists ]
use(Pump:297)
use(Call Lightning:204) [ enemy.ability(Tough n' Cuddly:1112).duration<2 ]
use(Thunderbolt:779)
use(Alpha Strike:504)
change(next)
```

#### Undead Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1542](https://www.wow-petguide.com/Encounter/1542)

##### Strategy: Default Strategy
```text

```

#### Critter Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1546](https://www.wow-petguide.com/Encounter/1546)

##### Strategy: Default Strategy
```text
ability(Refuge:1344)
ability(Apocalypse:519)

standby [enemy(#3).active & self(#2).active]
ability(Spirit Spikes:914) [self.round=1]
ability(Ooze Touch:445) [enemy(#1).active]

ability(Blinding Powder:1015) [enemy(#2).active]
ability(Jab:219) [!enemy(#3).active]

standby [enemy(#3).active & enemy.round=1]
ability(Blinding Powder:1015) [enemy.aura(Tough n' Cuddly:1111).exists]
standby [enemy.aura(Blinded:1014).exists]
ability(Smoke Bomb:1679)
standby [enemy(#3).active & self(#3).active]

standby [enemy(#3).active & self(#1).active]
change(#2) [enemy(#3).active & self(#3).dead]
change(next)
```

#### Magic Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1550](https://www.wow-petguide.com/Encounter/1550)

##### Strategy: Default Strategy
```text
change(#1) [ self(#2).dead & !enemy(Murrey:3558).played ]
change(#3) [ enemy.aura(Tough n' Cuddly:1111).duration=1 & self.speed.fast ]
change(#3) [ enemy.aura(Tough n' Cuddly:1111).duration=2 & self.speed.slow ]
if [ enemy.is(Murrey:3558) ]
    use(Curse of Doom:218) [ enemy.ability(Tough n' Cuddly:1112).usable ]
    if [ enemy.ability(Tough n' Cuddly:1112).duration=4 ]
        use(Eyeblast:475)
        use(Creeping Insanity:1760)
    endif
    use(Tentacle Slap:1570)
endif
if [ enemy.is(Bassalt:3560) ]
    use(Creeping Insanity:1760)
    use(Illusionary Barrier:465)
endif
use(Tentacle Slap:1570) [ enemy.is(Clawz:3559) & self(#2).dead ]
use(Eyeblast:475) [ !enemy.is(Clawz:3559) ]
use(Nether Blast:608)
use(Wind-Up:459)
change(next)
```

#### Elemental Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1554](https://www.wow-petguide.com/Encounter/1554)

##### Strategy: Default Strategy
```text
use(Drain Power:486)
use(Illuminate:460)
use(Blinkstrike:616)

use(Bash:348)
use(Call Lightning:204) [ enemy(Murrey:3558).active ]
use(Wild Winds:514)

change(next)
```

#### Beast Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1558](https://www.wow-petguide.com/Encounter/1558)

##### Strategy: Default Strategy
```text
if [ enemy(Murrey:3558).hp<1242 ]
    change(#3)
    use(Prowl:536)
endif
use(Trample:377) [ self(#2).active ]
use(Prowl:536) [ round=1 ]
use(Arcane Dash:1536)
use(Scrabble:2430)
use(Howl:362) [ self.aura(Prowl:543).exists ]
use(Scratch:119)
change(next)
```

#### Aquatic Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1562](https://www.wow-petguide.com/Encounter/1562)

##### Strategy: Default Strategy
```text
change(#3) [round=6]
use(Feign Death:568) [round=2]
use(Water Jet:118) [enemy.aura(Swarm of Flies:231).duration=5]
use(Swarm of Flies:232) 
use(Bubble:934) [self(#2).active]
use(First Croak:2451)
use(Acid Touch:756)
use(Fish Slap:1737) [enemy(#1).active]
use(Whirlpool:513)
use(Bubble:934)
use(Fish Slap:1737)
change(#1)
```

#### Mechanical Battler of Zaralek Cavern
**URL:** [https://www.wow-petguide.com/Encounter/1566](https://www.wow-petguide.com/Encounter/1566)

##### Strategy: Default Strategy
```text
change(#2) [enemy(#2).active]

ability(Minefield:634)
ability(Explode:282) [enemy.aura(Minefield:635).duration=7]
ability(Zap:116)

ability(Jolt:908) [enemy(#2).active]
ability(Supercharge:208)
ability(Call Lightning:204)
ability(#1)

standby
change(#1)
```

#### Explorer BezzertQuest: To a Land Down Under
**URL:** [https://www.wow-petguide.com/Encounter/1530/To_a_Land_Down_Under](https://www.wow-petguide.com/Encounter/1530/To_a_Land_Down_Under)

##### Strategy: Default Strategy
```text
change(#2) [round=4]
change(#2) [enemy(#1).active & enemy.aura(Stunned:927).exists]

ability(Creeping Insanity:1760) [round=1]
ability(Soulrush:752) [round=2]

ability(Stampede:163) [enemy(#3).active]
ability(Bubble:934) [self.aura(Whirlpool:512).duration=1]

ability(Call Lightning:204) [enemy.hp<1246 & enemy.aura(Tough n' Cuddly:1111).exists & enemy.aura(Shattered Defenses:542).exists]
ability(Call Lightning:204) [!enemy.aura(Tough n' Cuddly:1111).exists]

ability(#1)
change(next)
```

#### ShinmuraQuest: Are They Not Beautiful?
**URL:** [https://www.wow-petguide.com/Encounter/1531/Are_They_Not_Beautiful](https://www.wow-petguide.com/Encounter/1531/Are_They_Not_Beautiful)

##### Strategy: Default Strategy
```text
ability(Eggnog:835) [enemy(#3).active & enemy.ability(Conflagrate:179).duration=4]
ability(Gift of Winter's Veil:586)
ability(Frost Shock:416) [!enemy.aura(Frost Shock:415).exists & enemy(#1).active]
ability(Call Blizzard:206) [!weather(Blizzard:205)]
ability(#1)
change(next)
```

#### Delver MardeiQuest: Delver Mardei
**URL:** [https://www.wow-petguide.com/Encounter/1532/Delver_Mardei](https://www.wow-petguide.com/Encounter/1532/Delver_Mardei)

##### Strategy: Default Strategy
```text
use(Sandstorm:453)
use(Rupture:814)
use(Crush:406)
change(next)
```

#### Trainer OrloggQuest: Do You Even Train?
**URL:** [https://www.wow-petguide.com/Encounter/1533/Do_You_Even_Train](https://www.wow-petguide.com/Encounter/1533/Do_You_Even_Train)

##### Strategy: Default Strategy
```text
if [ally(Gilded Darknight:3130).active]
use(Deflection:490) [enemy(Lifft:3572).aura(Underwater:830).exists]
use(Cleave:1273)
endif
if [enemy(Brul'dan:3571).dead & enemy(Swole:3573).dead & ally(Gilded Darknight:3130).active]
change(Globe Yeti:2114)
endif
if [ally(Globe Yeti:2114).active]
use(Rampage:124) [self.aura(Attack Boost:485).exists]
use(Roar:347)
endif
if [ally(Gilded Darknight:3130).dead]
change(Zanj'ir Poker:2680)
endif
if [ally(Zanj'ir Poker:2680).active]
use(Dodge:312) [enemy(Lifft:3572).aura(Underwater:830).exists]
use(Whirlwind:741)
use(Jab:219)
endif
```

## Shadowlands

### World Quests

#### Illidari Masters: Sissix
**URL:** [https://www.wow-petguide.com/Encounter/346/Illidari_Masters:_Sissix](https://www.wow-petguide.com/Encounter/346/Illidari_Masters:_Sissix)

##### Strategy: Default Strategy
```text
use(Cleansing Rain:230) [round=2]
use(Water Jet:118) [self.aura(Pumped Up:296).exists & enemy.hpp=100]
use(Pump:297)
use(#1) [enemy(#2).active]

if [enemy(#3).active]
use(Prowl:536)
use(Call Darkness:256)
standby [self(#3).hp<712 & self(#3).type=1]
standby [self(#3).hp<316 & self(#3).type=9]
standby [self(#3).hp<475 & self(#3).type!=6]
standby [self(#1).active]
endif

change(next)
```

#### Illidari Masters: Madam Viciosa
**URL:** [https://www.wow-petguide.com/Encounter/347/Illidari_Masters:_Madam_Viciosa](https://www.wow-petguide.com/Encounter/347/Illidari_Masters:_Madam_Viciosa)

##### Strategy: Default Strategy
```text
standby [round=1]
change(#3) [enemy(#3).active & enemy.round=2]
change(#1) [!enemy(#1).active]
use(Acidic Goo:369) [self.round=1]
use(Dive:564) [enemy.round>5]
use(Absorb:449)
use(Decoy:334)
use(Thunderbolt:779) [enemy(#3).active]
use(Breath:115)
change(#2)
```

#### Illidari Masters: Nameless Mystic
**URL:** [https://www.wow-petguide.com/Encounter/348/Illidari_Masters:_Nameless_Mystic](https://www.wow-petguide.com/Encounter/348/Illidari_Masters:_Nameless_Mystic)

##### Strategy: Default Strategy
```text
ability(Decoy:334) [self(#1).active]
ability(Thunderbolt:779) [!enemy(#1).active]
ability(Breath:115)
ability(Explode:282) [enemy.hp<618]
ability(Missile:777)
change(#2)
```

#### Fight Night: AmaliaFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/145/Fight_Night:_Amalia](https://www.wow-petguide.com/Encounter/145/Fight_Night:_Amalia)

##### Strategy: Default Strategy
```text
change(#1) [self(#3).played]
standby [enemy.aura(Puppies of the Flame:1355).exists]
change(#2) [round=5]
use(Thunderbolt:779) [!enemy(#1).active]
use(Call Lightning:204)
use(Zap:116)
use(Explode:282) [enemy(#3).active]
use(Alert!:1585)
change(#3)
```

#### Fight Night: Bodhi SunwayverFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/146/Fight_Night:_Bodhi_Sunwayver](https://www.wow-petguide.com/Encounter/146/Fight_Night:_Bodhi_Sunwayver)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
change(#2) [round=2] 

use(Armageddon:1025) [enemy.hp<=439 & self(#1).power=346 & enemy.hp>365]
if [self(#1).power=276]
use(Armageddon:1025) [enemy.hp<=532 & self.aura(245).exists & enemy.hp>355]
use(Armageddon:1025) [enemy.hp<=355 & enemy.hp>236] 
endif

use(Time Bomb:602) [!self(#3).dead]
use(Prowl:536)
use(Moonfire:595)
use(#1)
change(#1)
```

#### Fight Night: Heliosus
**URL:** [https://www.wow-petguide.com/Encounter/147/Fight_Night:_Heliosus](https://www.wow-petguide.com/Encounter/147/Fight_Night:_Heliosus)

##### Strategy: Default Strategy
```text
ability(218)
ability(652)
change(#2) 
ability(919) [self.round=1]
ability(581)
```

#### Fight Night: Sir GalvestonFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/148/Fight_Night:_Sir_Galveston](https://www.wow-petguide.com/Encounter/148/Fight_Night:_Sir_Galveston)

##### Strategy: Default Strategy
```text
change(next) [self(#1).dead & !self(#3).played]
use(#3) [round~1]
use(#2) [round~3]
if [enemy.hp>246]
use(Surge of Light:769)
use(Holy Charge:767)
endif
use(#1)
change(next)
```

#### Fight Night: Rats!
**URL:** [https://www.wow-petguide.com/Encounter/149/Fight_Night:_Rats!](https://www.wow-petguide.com/Encounter/149/Fight_Night:_Rats!)

##### Strategy: Default Strategy
```text
ability(218)
ability(652)
change(#2) [self(#1).dead]
ability(919) [!enemy.aura(918).exists]
ability(581)
```

#### Fight Night: Stitches Jr. Jr.
**URL:** [https://www.wow-petguide.com/Encounter/150/Fight_Night:_Stitches_Jr._Jr.](https://www.wow-petguide.com/Encounter/150/Fight_Night:_Stitches_Jr._Jr.)

##### Strategy: Default Strategy
```text
ability(301)
change(#2)
ability(362)
ability(593)
```

#### Fight Night: Tiffany NelsonFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/151/Fight_Night:_Tiffany_Nelson](https://www.wow-petguide.com/Encounter/151/Fight_Night:_Tiffany_Nelson)

##### Strategy: Default Strategy
```text
change(#1) [self(#3).played]
change(#2) [round=2]
use(Prowl:536) [round=3]
use(Moonfire:595) [round=4]
use(Greench's Gift:1076) [enemy(#3).active]
use(Ice Tomb:624) [enemy(#1).active]
use(Spirit Claws:974)
change(#3)
```

#### Size Doesn't Matter
**URL:** [https://www.wow-petguide.com/Encounter/153/Size_Doesn't_Matter](https://www.wow-petguide.com/Encounter/153/Size_Doesn't_Matter)

##### Strategy: Default Strategy
```text
use(277) [ round = 4 ]
use(1731) [ round > 1 ]
use(608)
change(#2)
use(282) [round = 8]
use(779)
```

#### Dazed and Confused and Adorable
**URL:** [https://www.wow-petguide.com/Encounter/155/Dazed_and_Confused_and_Adorable](https://www.wow-petguide.com/Encounter/155/Dazed_and_Confused_and_Adorable)

##### Strategy: Default Strategy
```text
ability(Unholy Ascension:321)
change(next) [ !self(#3).played ]
ability(#3) [ enemy.aura(Leaping:839).exists ]
ability(#1)
```

#### Training with the NightwatchersFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/156/Training_with_the_Nightwatchers](https://www.wow-petguide.com/Encounter/156/Training_with_the_Nightwatchers)

##### Strategy: Default Strategy
```text
change(#1) [round=5]
change(#3) [round=4]
change(#2) [round=2]
use(Armageddon:1025) [round=8]
use(Zeitbombe:602)
use(Flammenatem:501)
use(Arkaner Sturm:589) [round=11]
use(Kristallgefängnis:569)
use(Arkanes Schlitzen:1353)
change(#2)
```

#### The Wine's Gone Bad
**URL:** [https://www.wow-petguide.com/Encounter/157/The_Wine's_Gone_Bad](https://www.wow-petguide.com/Encounter/157/The_Wine's_Gone_Bad)

##### Strategy: Default Strategy
```text
use(Lucky Dance:757) [!self.aura(Uncanny Luck:251).exists]
change(#2) [self(#1).active & self.aura(Uncanny Luck:251).exists]
use(Curse of Doom:218) [!enemy.aura(Curse of Doom:217).exists]
use(Haunt:652)
change(#3)
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
use(Flock:581)
change(#1)
use(#1)
standby
```

#### Help a Whelp
**URL:** [https://www.wow-petguide.com/Encounter/158/Help_a_Whelp](https://www.wow-petguide.com/Encounter/158/Help_a_Whelp)

##### Strategy: Default Strategy
```text
quit [enemy(#1).active & enemy.round=4]
use(Clean-Up:456) [round=1]
use(Soulrush:752) [round=2]
use(Magic Sword:1085)
ability(Explode:282) [enemy.hp.can_explode]
ability(Decoy:334)
ability(Missile:777)
change(next)
```

#### Training with DurianFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/160/Training_with_Durian](https://www.wow-petguide.com/Encounter/160/Training_with_Durian)

##### Strategy: Default Strategy
```text
ability(Ashes of Outland:2396) [round=1]
standby [self(#1).aura(Autumn Breeze:963).exists & self(#1).active]
ability(Void Slap:2361) [self.aura(Dragonkin:245).exists & enemy(#2).active]
ability(Needle Claw:2375)
ability(Explode:282) [enemy(#3).active & enemy.hp.can_explode]
ability(Frost Shot:1865)
change(next)
```

#### Only Pets Can Prevent Forest Fires
**URL:** [https://www.wow-petguide.com/Encounter/161/Only_Pets_Can_Prevent_Forest_Fires](https://www.wow-petguide.com/Encounter/161/Only_Pets_Can_Prevent_Forest_Fires)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).hpp<100]
change(#2) [self(#3).active]

use(Water Jet:118) [round=2]
use(Whirlpool:513)
use(Prowl:536)

use(Pump:297) [enemy(#2).active & enemy.round=1]
use(Pump:297) [enemy.ability(Extra Plating:392).duration=2]
use(Cleansing Rain:230) [!weather(Cleansing Rain:229)]
use(Pump:297) [self.aura(Pumped Up:296).exists]

use(#1)
change(next)
```

#### Meet The Maw
**URL:** [https://www.wow-petguide.com/Encounter/162/Meet_The_Maw](https://www.wow-petguide.com/Encounter/162/Meet_The_Maw)

##### Strategy: Default Strategy
```text
ability(Razor Talons:2237) [!enemy.aura(Razor Talons:2238).exists]
ability(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]
ability(Armageddon:1025)

ability(Explode:282)

change(next)
```

#### Stand Up to Bullies
**URL:** [https://www.wow-petguide.com/Encounter/163/Stand_Up_to_Bullies](https://www.wow-petguide.com/Encounter/163/Stand_Up_to_Bullies)

##### Strategy: Default Strategy
```text
change(#1) [self(#2).dead]
use(#1) [round=1]
use(#3) [round=2]
change(#2) [round=3]
use(Black Claw:919) [!enemy.aura(Black Claw).exists]
use(Flock:581)
use(Build Turret:710) [enemy.aura(Black Claw).exists]
use(Metal Fist:384)
```

#### Dealing with SatyrsFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/165/Dealing_with_Satyrs](https://www.wow-petguide.com/Encounter/165/Dealing_with_Satyrs)

##### Strategy: Default Strategy
```text
ability(Explode:282) [enemy.hp<561 & enemy(#3).active]
ability(Thunderbolt:779) [!enemy(#2).active]
ability(BONESTORM:649)
ability(Ancient Blessing:611) [!self.aura(Undead:242).exists & self.hpp<100]
ability(#1)
change(#1)
```

#### Training with BreddaFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/167/Training_with_Bredda](https://www.wow-petguide.com/Encounter/167/Training_with_Bredda)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).played]
use(Supercharge:208) [enemy(#3).active]
use(Ion Cannon:209) [enemy(#3).active]
use(Alert!:1585) [enemy(#2).active]
use(Dodge:312)
use(Stampede:163) [enemy(#2).active]
use(Flurry:360) [enemy.aura(Shattered Defenses:542).exists]
use(Stampede:163)
change(next)
```

#### Tiny Poacher, Tiny AnimalsFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/168/Tiny_Poacher,_Tiny_Animals](https://www.wow-petguide.com/Encounter/168/Tiny_Poacher,_Tiny_Animals)

##### Strategy: Default Strategy
```text
-- rng in the beginning (<0.5%)
quit [enemy(#1).dead & round=4]
--
-- rare case: too many critical strikes Ice lance Turn4+ 5
use(Explode:282) [enemy(#1).dead & enemy(#2).dead]
--
use(Explode:282) [enemy(#1).dead & enemy(#3).dead & enemy(#2).hp<561]
use(Ice Tomb:624)
use(Call Blizzard:206)
use(Ice Lance:413)
use(Thunderbolt:779) [enemy(#3).active & enemy.aura(Stunned:927).exists]
use(Breath:115)
change(next)
```

#### Wildlife Protection Force
**URL:** [https://www.wow-petguide.com/Encounter/169/Wildlife_Protection_Force](https://www.wow-petguide.com/Encounter/169/Wildlife_Protection_Force)

##### Strategy: Default Strategy
```text
standby [round=1]
change(#2) [round=2]

ability(Razor Talons:2237) [!enemy.aura(Razor Talons:2238).exists]
ability(Armageddon:1025)

ability(Poison Protocol:1954) [enemy.aura(Corrosion:446).exists]
ability(Void Nova:2356) [!self.ability(Poison Protocol:1954).usable]
ability(Corrosion:447)

change(next)
```

#### It's Illid... Wait.
**URL:** [https://www.wow-petguide.com/Encounter/170/It's_Illid..._Wait.](https://www.wow-petguide.com/Encounter/170/It's_Illid..._Wait.)

##### Strategy: Default Strategy
```text
use(Disruption:1123)
use(Life Exchange:277)
use(Unholy Ascension:321)
use(Prowl:536)
use(Call Darkness:256)
change(next)
```

#### Snail Fight!Family Familiar
**URL:** [https://www.wow-petguide.com/Encounter/171/Snail_Fight!](https://www.wow-petguide.com/Encounter/171/Snail_Fight!)

##### Strategy: Default Strategy
```text
quit [self(#2).dead]
standby [round=1]
change(#2) [!self(#2).active]
change(#3) [enemy(#1).dead & !self(#3).played]

if [enemy(#3).active]
use(Feed:1016) [self.aura(Prowl:543).exists]
standby [enemy.aura(Underwater:830).exists]
use(Prowl:536) [self.hp>723 & self.ability(Feed:1016).duration<2]
use(Feed:1016)
use(Bite:110)
endif

use(Prowl:536)
use(Feed:1016) [self.aura(Prowl:543).duration=1]
use(Bite:110) [!self.aura(Prowl:543).exists & enemy.hpp<100 & !enemy(#2).active]
use(Bite:110) [enemy.ability(Headbutt:376).usable]
standby
```

#### Rocko Needs a Shave
**URL:** [https://www.wow-petguide.com/Encounter/172/Rocko_Needs_a_Shave](https://www.wow-petguide.com/Encounter/172/Rocko_Needs_a_Shave)

##### Strategy: Default Strategy
```text
use(1123)
```

#### All Howl, No Bite
**URL:** [https://www.wow-petguide.com/Encounter/174/All_Howl,_No_Bite](https://www.wow-petguide.com/Encounter/174/All_Howl,_No_Bite)

##### Strategy: Default Strategy
```text
use(Disruption:1123)
use(Prowl:536)
use(Call Darkness:256)
change(#2)
```

#### Jarrun's LadderFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/175/Jarrun's_Ladder](https://www.wow-petguide.com/Encounter/175/Jarrun's_Ladder)

##### Strategy: Default Strategy
```text
if [self(#1).active]
change(#2) [round=3]
change(#2) [self(#1).dead]
use(Poison Protocol:1954)
use(Void Nova:2356) [enemy(#2).hp>95]
standby [enemy.aura(Undead:242).exists]
use(Ooze Touch:445)
endif

if [self(#2).active]
standby [enemy.aura(Undead:242).exists]
change(#3) [round=8]
use(Great Sting:1966) [round>4]
use(Cleave:1273)
endif

if [self(#3).active]
change(#1)
endif
```

#### Oh, Ominitron
**URL:** [https://www.wow-petguide.com/Encounter/176/Oh,_Ominitron](https://www.wow-petguide.com/Encounter/176/Oh,_Ominitron)

##### Strategy: Default Strategy
```text
use(Dark Rebirth:794) [self.hp < 300]
use(Corrupted Touch:2258) [!enemy.aura(Corrupted Touch:2257).exists]
use(Corrupted Ground:2255) [!enemy.aura(Corrupted Ground:2256).exists]
use(Corrupted Touch:2258)

change(#3) [!ally(#3).played]
change(#2)

use(Thunderbolt:779)
use(Decoy:334)
use(Breath:115)

use(#1)
use(#2)
use(#3)

quit
```

#### My Beast's BiddingFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/177/My_Beast's_Bidding](https://www.wow-petguide.com/Encounter/177/My_Beast's_Bidding)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
use(Arcane Storm:589)
use(Mana Surge:489)
use(Toxic Smoke:640) [enemy.hp<=390]
use(Wind-Up:459)
change(next)
```

#### All Pets Go to Heaven
**URL:** [https://www.wow-petguide.com/Encounter/178/All_Pets_Go_to_Heaven](https://www.wow-petguide.com/Encounter/178/All_Pets_Go_to_Heaven)

##### Strategy: Default Strategy
```text
use(bubble:934) [ enemy.ability(bigdot:218).usable ]
use(frogdot:232) [ !enemy.aura(frogdot:231).exists ]
use(frogdot:232) [ enemy.aura(undead:242).exists ]
use(snaildot:369) [ !enemy.aura(snaildot:368).exists ]
use(filler:228)
use(filler:449)
change(#2) [ !self(#2).played & !self(#2).level.max ]
change(#3)
```

#### Beasts of Burden:
**URL:** [https://www.wow-petguide.com/Encounter/337/Beasts_of_Burden](https://www.wow-petguide.com/Encounter/337/Beasts_of_Burden)

##### Strategy: Default Strategy
```text
use(Explode:282) [enemy.hp<=620]
use(Toxic Smoke:640) [enemy.aura(Toxic Smoke:639).duration!=2]
use(Wind-Up:459)
```

#### Andurs
**URL:** [https://www.wow-petguide.com/Encounter/337/Andurs](https://www.wow-petguide.com/Encounter/337/Andurs)

##### Strategy: Default Strategy
```text
use(Explode:282) [enemy.hp<=620]
use(Toxic Smoke:640) [enemy.aura(Toxic Smoke:639).duration!=2]
use(Wind-Up:459)
```

#### Rydyr
**URL:** [https://www.wow-petguide.com/Encounter/338/Rydyr](https://www.wow-petguide.com/Encounter/338/Rydyr)

##### Strategy: Default Strategy
```text
ability(Explode:282) [enemy.hp<1178]
ability(#1)
change(#2) [self(#1).dead]
```

#### The Master of PetsFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/181/The_Master_of_Pets](https://www.wow-petguide.com/Encounter/181/The_Master_of_Pets)

##### Strategy: Default Strategy
```text
standby [round~1]
change(#2) [round=2]
change(#3) [enemy(#2).active]
use(Scrabble:2430) [enemy(#2).active]
use(Prowl:536)
use(Arcane Dash:1536)
use(Thunderbolt:779) [self.aura(Speed Reduction:154).duration=4]
use(Explode:282)
change(#2)
```

#### Clear the Catacombs
**URL:** [https://www.wow-petguide.com/Encounter/182/Clear_the_Catacombs](https://www.wow-petguide.com/Encounter/182/Clear_the_Catacombs)

##### Strategy: Default Strategy
```text
quit [self.aura(Mechanical:244).exists & round<6]
quit [self(#1).dead]
change(#1) [self(#3).active]
change(#2) [round=2]
use(Call Lightning:204)
use(Time Bomb:602)
use(Armageddon:1025) [enemy.aura(601).duration=2]
use(Spark:617) [enemy.aura(601).duration=3 & enemy.hp>706]
standby
change(next)
```

#### ChoppedFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/183/Chopped](https://www.wow-petguide.com/Encounter/183/Chopped)

##### Strategy: Default Strategy
```text
quit [ self(#3).dead ]
change(#3) [ enemy(#3).active & !self(#3).played ]
change(#2) [ self(#1).dead ]
ability(Crouch:165) [ round = 1 ]
ability(Burn:113) [ round > 2 & enemy(#1).active ]
ability(Flamethrower:503)
ability(Ironskin:1758)
ability(Predatory Strike:518) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Falcosaur Swarm!:1773)
standby
```

#### FlummoxedFamily Familiar
**URL:** [https://www.wow-petguide.com/Encounter/184/Flummoxed](https://www.wow-petguide.com/Encounter/184/Flummoxed)

##### Strategy: Default Strategy
```text
use(Blinding Powder:1015)
use(Glowing Toxin:270) [!enemy.aura(Glowing Toxin:271).exists]
use(Creeping Fungus:743) [!enemy.aura(Creeping Fungus:742).exists]
use(Explode:282) [self(#2).active]
use(Explode:282) [self(#2).dead]
change(#2)
change(#1)
```

#### Threads of Fate
**URL:** [https://www.wow-petguide.com/Encounter/185/Threads_of_Fate](https://www.wow-petguide.com/Encounter/185/Threads_of_Fate)

##### Strategy: Default Strategy
```text
ability(#1) [ enemy.round~1,2 ] 
ability(#2) [ enemy(#3).hp<556 ] 
ability(#3) [ enemy(#3).active & enemy.hp>555 ] 
ability(#1) 
change(#2)
```

#### Mana Tap
**URL:** [https://www.wow-petguide.com/Encounter/186/Mana_Tap](https://www.wow-petguide.com/Encounter/186/Mana_Tap)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Dodge:311).exists]
ability(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]
ability(Razor Talons:2237) [!enemy.aura(Razor Talons:2238).exists]
ability(Flame Breath:501) [enemy.aura(Prismatic Barrier:443).exists]
ability(Armageddon:1025) [enemy(#2).active]
ability(Explode:282) [enemy(#3).active & enemy.hp<470]
ability(Thunderbolt:779)
ability(#1)
change(next)
```

### Covenant Adventures

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

### Torghast

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

### Family Exorcist

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

## BfA

### World Quests

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

### Island Expeditions

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

### Warfronts

### Family Battler

### Nazjatar & Mechagon

#### Crystalsnap
**URL:** [https://www.wow-petguide.com/Encounter/1199/Crystalsnap](https://www.wow-petguide.com/Encounter/1199/Crystalsnap)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
ability(Flock:581) [enemy.aura(Black Claw:918).exists]
ability(Black Claw:919)
change(Ikky:1532)
```

#### Digallo
**URL:** [https://www.wow-petguide.com/Encounter/1200/Digallo](https://www.wow-petguide.com/Encounter/1200/Digallo)

##### Strategy: Default Strategy
```text
use(Toxic Skin:1087) [round=1]
use(Emerald Dream:598) [round=3]
use(#1)
```

#### Kostos
**URL:** [https://www.wow-petguide.com/Encounter/1201/Kostos](https://www.wow-petguide.com/Encounter/1201/Kostos)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
use(BONESTORM!!:1762)
use(Chop:943)
use(Black Claw:919) [ self.round=1 ]
use(Flock:581)
change(next)
```

#### Gelatinous
**URL:** [https://www.wow-petguide.com/Encounter/1202/Gelatinous](https://www.wow-petguide.com/Encounter/1202/Gelatinous)

##### Strategy: Default Strategy
```text
use(Illuminate:460) [ round>2 ]
use(Soul Ward:751) [ round>1 & enemy.hp>148 ]
use(Beam:114) [ round!=4 ]
use(Explode:282)
change(next)
```

#### Glurp
**URL:** [https://www.wow-petguide.com/Encounter/1203/Glurp](https://www.wow-petguide.com/Encounter/1203/Glurp)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
use(Chop:943)
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
use(Toxic Spray:2232) [!enemy.aura(Toxic Wound:2112).exists]
standby
change(next)
```

#### Sewer Creeper
**URL:** [https://www.wow-petguide.com/Encounter/1204/Sewer_Creeper](https://www.wow-petguide.com/Encounter/1204/Sewer_Creeper)

##### Strategy: Default Strategy
```text
ability(Black Claw:919) [!enemy(#1).aura(Black Claw:918).exists]
ability(BONESTORM!!:1762) [round=3]
ability(Blistering Cold:786)
ability(Chop:943)
standby [self(#2).active]
standby [self(#3).active]
change(next)
```

#### The Countess
**URL:** [https://www.wow-petguide.com/Encounter/1205/The_Countess](https://www.wow-petguide.com/Encounter/1205/The_Countess)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786) [enemy(The Countess:3074).hp.full]
use(Chop:943) [enemy(The Countess:3074).aura(Blistering Cold:785).duration>2]
change(Ikky:1532)
use(Black Claw:919) [!enemy(The Countess:3074).aura(Black Claw:918).exists]
use(Flock:581)
```

#### Briarpaw
**URL:** [https://www.wow-petguide.com/Encounter/1206/Briarpaw](https://www.wow-petguide.com/Encounter/1206/Briarpaw)

##### Strategy: Default Strategy
```text
if [ !enemy.aura(Dodge:311).exists ]
    use(Missile:777) [ self.power=260 & enemy.hp<177 ]
    use(Missile:777) [ self.power=273 & enemy.hp<185 ]
    use(Missile:777) [ self.power=289 & enemy.hp<195 ]
    use(Missile:777) [ self.power=325 & enemy.hp<217 ]
endif
if [ enemy.aura(Dodge:311).exists ]
    change(next) [ self.aura(Decoy:333).exists & self.ability(Decoy:334).duration<6 ]
    use(Decoy:334) [ !self.aura(Decoy:333).exists ]
endif
-- Delete or comment out Explode line if you want all pets alive
use(Explode:282) [ round=8 ]
-- Stop deleting here
if [ enemy.ability(Quick Dodge:2422).usable & !self.aura(Decoy:333).exists & round>4 ]
    change(#2)
    change(#1)
endif
use(Missile:777) [ !enemy.aura(Dodge:311).exists ]
standby
change(next)
```

#### Chittermaw
**URL:** [https://www.wow-petguide.com/Encounter/1207/Chittermaw](https://www.wow-petguide.com/Encounter/1207/Chittermaw)

##### Strategy: Default Strategy
```text
change(Darkmoon Zeppelin:339) [round=2]
change(Fel-Afflicted Skyfin:2119) [round=6]
change(Iron Starlette:1387) [round=7]
use(Glowing Toxin:270)
use(Decoy:334) [round=3]
standby [round=4]
use(Explode:282)
```

#### Mistwing
**URL:** [https://www.wow-petguide.com/Encounter/1208/Mistwing](https://www.wow-petguide.com/Encounter/1208/Mistwing)

##### Strategy: Default Strategy
```text
change(#2) [round=3]
use(Blistering Cold:786)
use(Chop:943)
use(Smoke Cloud:2239)
use(Toxic Spray:2232) [!enemy.aura(Toxic Wound:2112).exists]
use(Flurry:360)
change(next)
```

## Legion

### World Quests

### Family Familiar

#### Tiny Madness
**URL:** [https://www.wow-petguide.com/Encounter/1146/Tiny_Madness](https://www.wow-petguide.com/Encounter/1146/Tiny_Madness)

##### Strategy: Default Strategy
```text
standby [round=2]
ability(Curse of Doom:218) [round=3]
ability(Haunt:652) [round=4]
ability(Dead Man's Party:1093) [!enemy.aura(Shattered Defenses:542).exists]
ability(#1)
change(next)
```

#### Brain Tickling
**URL:** [https://www.wow-petguide.com/Encounter/1147/Brain_Tickling](https://www.wow-petguide.com/Encounter/1147/Brain_Tickling)

##### Strategy: Default Strategy
```text
use(#1) [ self(#2).dead ]
use(Flock:581) [ enemy.aura(Black Claw:918).exists ]
use(Black Claw:919)
use(Conflagrate:179) [ enemy.aura(Shattered Defenses:542).duration<2 ]
use(Scorched Earth:172)
use(Flame Breath:501)
change(#1)
```

#### Living Statues Are Tough
**URL:** [https://www.wow-petguide.com/Encounter/1148/Living_Statues_Are_Tough](https://www.wow-petguide.com/Encounter/1148/Living_Statues_Are_Tough)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218) 
ability(Haunt:652) 
ability(Dead Man's Party:1093) [!enemy.aura(Shattered Defenses:542).exists]
ability(#1)
change(next)
```

#### Flight of the Vil'thik
**URL:** [https://www.wow-petguide.com/Encounter/1149/Flight_of_the_Vil'thik](https://www.wow-petguide.com/Encounter/1149/Flight_of_the_Vil'thik)

##### Strategy: Default Strategy
```text
use(Toxic Skin:1087) [ !self.aura(Toxic Skin:1086).exists ]
use(Emerald Dream:598)
use(#1)
change(#2)
```

#### Retinus the Seeker
**URL:** [https://www.wow-petguide.com/Encounter/1151/Retinus_the_Seeker](https://www.wow-petguide.com/Encounter/1151/Retinus_the_Seeker)

##### Strategy: Default Strategy
```text
use(Explode:282) [enemy.hp<610]
use(Flock:581) [enemy.aura(Black Claw:918).exists]
use(Black Claw:919)
use(Thunderbolt:779)
use(Missile:777)
change(next)
```

#### I Am The One Who Whispers
**URL:** [https://www.wow-petguide.com/Encounter/1152/I_Am_The_One_Who_Whispers](https://www.wow-petguide.com/Encounter/1152/I_Am_The_One_Who_Whispers)

##### Strategy: Default Strategy
```text
use(Flock:581) [ enemy.aura(Black Claw:918).exists ]
use(Black Claw:919)
use(Scorched Earth:172)
use(Breath:115)
change(next)
```

#### Dune Buggy
**URL:** [https://www.wow-petguide.com/Encounter/1153/Dune_Buggy](https://www.wow-petguide.com/Encounter/1153/Dune_Buggy)

##### Strategy: Default Strategy
```text
ability(Blistering Cold:786) [round=1]
ability(BONESTORM:1762) [round>2]
ability(Chop:943)
ability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
ability(Hunting Party:921)
change(next)
```

#### Watch Where You Step
**URL:** [https://www.wow-petguide.com/Encounter/1154/Watch_Where_You_Step](https://www.wow-petguide.com/Encounter/1154/Watch_Where_You_Step)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Inflation:1002) [enemy.aura(Shattered Defenses:542).duration<2]
ability(#1) [self(#3).active]
ability(#3)
change(next)
```

#### That's a Big Carcass
**URL:** [https://www.wow-petguide.com/Encounter/699/That's_a_Big_Carcass](https://www.wow-petguide.com/Encounter/699/That's_a_Big_Carcass)

##### Strategy: Default Strategy
```text
standby [ enemy(#2).active & enemy.round=1 ]
ability(#2) [ !enemy(#3).active ]
ability(#3) [ enemy.aura(Shattered Defenses:542).exists ]
ability(#1)
change(#2)
```

#### Strange Looking Dogs
**URL:** [https://www.wow-petguide.com/Encounter/700/Strange_Looking_Dogs](https://www.wow-petguide.com/Encounter/700/Strange_Looking_Dogs)

##### Strategy: Default Strategy
```text
change(#2) [ self(Iron Starlette:1387).dead & !self(#2).played ]
change(#3) [ self(Iron Starlette:1387).dead & self(#2).played ]
use(Wind-Up:459) [ !self.aura(Wind-Up:458).exists ]
use(Supercharge:208) [ !self.aura(Supercharged:207).exists ]
use(Powerball:566) [ !self.aura(Speed Boost:831).exists & enemy(Pokey:2332).active ]
use(Wind-Up:459)
use(Swarm of Flies:232) [ !enemy.aura(Swarm of Flies:231).exists ]
use(Bubble:934)
use(Tongue Lash:228)
```

#### Not So Bad Down Here
**URL:** [https://www.wow-petguide.com/Encounter/701/Not_So_Bad_Down_Here](https://www.wow-petguide.com/Encounter/701/Not_So_Bad_Down_Here)

##### Strategy: Default Strategy
```text
use(Supercharge:208) [ enemy(#3).hp>988 ]
use(Explode:282) [ enemy(#2).hp.can_explode ]
use(Wind-Up:459) [ !enemy(#1).active & enemy(#2).hp>1004 ]
use(Drill Charge:1921)
use(Arcane Storm:589) [ round=2 ]
use(Call Lightning:204)
use(Tail Sweep:122)
change(#2)
```

#### Unbreakable
**URL:** [https://www.wow-petguide.com/Encounter/702/Unbreakable](https://www.wow-petguide.com/Encounter/702/Unbreakable)

##### Strategy: Default Strategy
```text
standby [self.aura(Stunned:927).exists]
ability(#3)
change(next)
```

#### Captured Evil
**URL:** [https://www.wow-petguide.com/Encounter/704/Captured_Evil](https://www.wow-petguide.com/Encounter/704/Captured_Evil)

##### Strategy: Default Strategy
```text
use(Poison Protocol:1954) [round=2]
use(Void Nova:2356) [round=3]
use(Corrosion:447)
use(Quills:184) [!enemy(#3).active]
use(Conflagrate:179) [enemy.aura(Flame Breath:500).exists]
use(Flame Breath:501)
change(next)
```

#### Sea Creatures Are Weird
**URL:** [https://www.wow-petguide.com/Encounter/705/Sea_Creatures_Are_Weird_](https://www.wow-petguide.com/Encounter/705/Sea_Creatures_Are_Weird_)

##### Strategy: Default Strategy
```text
quit [ enemy(#1).active & !enemy.ability(Sweep:457).usable ]
change(#1) [ self(#3).active ]
change(#3) [ self(#1).dead ]
if [ self(#1).active ]
    ability(Supercharge:208) [ round~2,6 ]
    ability(Wind-Up:459) [ enemy(#1).active ]
    ability(Wind-Up:459) [ round>6 & self.aura(Mechanical:244).exists & self.aura(Wind-Up:458).exists ]
    ability(Powerball:566)
endif
ability(Explode:282) [ enemy(#3).active & enemy(#3).hp<561 ]
ability(Thunderbolt:779) [ !enemy(#2).dead & enemy(#2).hp<245 ]
ability(Thunderbolt:779) [ enemy(#3).active ]
ability(Breath:115)
```

#### Automated Chaos
**URL:** [https://www.wow-petguide.com/Encounter/706/Automated_Chaos](https://www.wow-petguide.com/Encounter/706/Automated_Chaos)

##### Strategy: Default Strategy
```text
change(#3) [ enemy(#3).active ]
standby [ self(#3).active ]
change(#1) [ round = 6 ]
use(1955) [ round = 1 ]
use(118) [ round = 7 & enemy(#1).hp > 1250 ]
standby [ round = 7 ]
use(418)
change(#2)
use(206) [ round = 5 ]
use(481) [ enemy.aura(417).exists ]
use(477)
```

#### This Little Piggy Has Sharp Tusks
**URL:** [https://www.wow-petguide.com/Encounter/707/This_Little_Piggy_Has_Sharp_Tusks](https://www.wow-petguide.com/Encounter/707/This_Little_Piggy_Has_Sharp_Tusks)

##### Strategy: Default Strategy
```text
change(next) [ self(#1).dead & !self(#3).played ] 
ability(#2) [ !enemy.aura(217).exists ] 
ability(#3) 
ability(#1)
```

#### What's the Buzz?
**URL:** [https://www.wow-petguide.com/Encounter/709/What's_the_Buzz](https://www.wow-petguide.com/Encounter/709/What's_the_Buzz)

##### Strategy: Default Strategy
```text
standby [ round=1 ]
change(#2) [ round=2 ]
change(#3) [ round= 3 ]
use(#3)
use(#2)
```

#### Rogue Azerite
**URL:** [https://www.wow-petguide.com/Encounter/710/Rogue_Azerite](https://www.wow-petguide.com/Encounter/710/Rogue_Azerite)

##### Strategy: Default Strategy
```text
ability(Whirlpool:513) [self(Pandaren Water Spirit:868).active]
ability(Dive:564) [self(Pandaren Water Spirit:868).active]
ability(Water Jet:118) [self(Pandaren Water Spirit:868).active]
change(#2) [self(Pandaren Water Spirit:868).dead & !self(#3).active]
change(#3)
ability(Shell Shield:310) [self(#3).aura(Shell Shield:309).duration <2]
ability(Dive:564)
ability(Absorb:449)
```

#### Night Horrors
**URL:** [https://www.wow-petguide.com/Encounter/711/Night_Horrors](https://www.wow-petguide.com/Encounter/711/Night_Horrors)

##### Strategy: Default Strategy
```text
change(next) [ self(#1).dead & !self(#3).played ]
ability(Black Claw:919) [ !enemy.aura(Black Claw:918).exists ]
ability(Black Claw:919) [ enemy(#3).active & self.hp>366 ]
ability(Flock:581)
ability(Make it Rain:985)
ability(#1)
```

#### Crab People
**URL:** [https://www.wow-petguide.com/Encounter/712/Crab_People](https://www.wow-petguide.com/Encounter/712/Crab_People)

##### Strategy: Default Strategy
```text
ability(Predatory Strike:518) [enemy.aura(Shattered Defenses:542).exists]
ability(Savage Talon:1370) [enemy.aura(Shattered Defenses:542).exists]
ability(Falcosaur Swarm!:1773)
change(next)
```

#### Add More to the Collection
**URL:** [https://www.wow-petguide.com/Encounter/714/Add_More_to_the_Collection](https://www.wow-petguide.com/Encounter/714/Add_More_to_the_Collection)

##### Strategy: Default Strategy
```text
change(#3) [enemy(#3).active]
ability(어슬렁:536) [enemy(#2).active]
ability(비전 폭풍:589)
ability(부정한 희생:321)
ability(#2)
ability(#1) 
change(next)
```

#### Small Beginnings
**URL:** [https://www.wow-petguide.com/Encounter/715/Small_Beginnings](https://www.wow-petguide.com/Encounter/715/Small_Beginnings)

##### Strategy: Default Strategy
```text
standby [ round~1,4 ]
use(Prowl:536)
use(Call Darkness:256)
use(Spectral Strike:442)
use(Nocturnal Strike:517)
change(next)
```

#### You've Never Seen Jammer Upset
**URL:** [https://www.wow-petguide.com/Encounter/716/You've_Never_Seen_Jammer_Upset](https://www.wow-petguide.com/Encounter/716/You've_Never_Seen_Jammer_Upset)

##### Strategy: Default Strategy
```text
if [ self(Iron Starlette:1387).active ] 
ability(Wind-Up:459) [ round=1 ] 
ability(Supercharge:208) [ round=2 ] 
ability(Wind-Up:459) [ round=3 ] 
ability(Wind-Up:459) [ round=4 ] 
change(#2) [ round=5 ] 
ability(Wind-Up:459) [ round >= 6 ] 
endif 
change(Iron Starlette:1387) [ self(#2).active ]
```

#### Critters are Friends, Not Food
**URL:** [https://www.wow-petguide.com/Encounter/717/Critters_are_Friends,_Not_Food](https://www.wow-petguide.com/Encounter/717/Critters_are_Friends,_Not_Food)

##### Strategy: Default Strategy
```text
ability(Void Nova:2356)
ability(Poison Protocol:1954)
ability(Soulrush:752) [enemy(#2).active]
ability(Moonfire:595) [enemy(#3).active]
ability(#1)
change(next)
```

#### Crawg in the Bog
**URL:** [https://www.wow-petguide.com/Encounter/719/Crawg_in_the_Bog](https://www.wow-petguide.com/Encounter/719/Crawg_in_the_Bog)

##### Strategy: Default Strategy
```text
ability(Alert!:1585) [round=1]
ability(Supercharge:208)
ability(Ion Cancon:209)
```

#### Marshdwellers
**URL:** [https://www.wow-petguide.com/Encounter/720/Marshdwellers](https://www.wow-petguide.com/Encounter/720/Marshdwellers)

##### Strategy: Default Strategy
```text
use(Predatory Strike) [enemy.aura(Shattered Defenses:542).exists]
use(Falcosaur Swarm!)
change(#2)
use(Arcane Storm)
use(Mana Surge)
use(Tail Sweep)
change(#3)
```

#### Accidental Dread
**URL:** [https://www.wow-petguide.com/Encounter/721/Accidental_Dread](https://www.wow-petguide.com/Encounter/721/Accidental_Dread)

##### Strategy: Default Strategy
```text
if [ !self(#2).active ]
    ability(Life Exchange:277) [ enemy(#2).active ]
    ability(Moonfire:595) [ enemy.round<3 ]
    ability(Arcane Blast:421)
endif
change(#3) [ self(#2).played ]
change(#2) [ !self(#2).played ]
ability(Arcane Storm:589)
ability(Mana Surge:489)
ability(Tail Sweep:122)
```

#### Pack Leader
**URL:** [https://www.wow-petguide.com/Encounter/722/Pack_Leader](https://www.wow-petguide.com/Encounter/722/Pack_Leader)

##### Strategy: Default Strategy
```text
use(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]
use(Time Bomb:602)
use(Armageddon:1025)

use(Toxic Smoke:640) [round=4]
use(Storm Coil:1922)
use(Explode:282)

change(next)
```

#### Keeyo's Champions of Vol'dun
**URL:** [https://www.wow-petguide.com/Encounter/724/Keeyo's_Champions_of_Vol'dun](https://www.wow-petguide.com/Encounter/724/Keeyo's_Champions_of_Vol'dun)

##### Strategy: Default Strategy
```text
change(#2) [ enemy(#1).hp<715 ]
use(Booby-Trapped Presents:1080)
use(Greench's Gift:1076)
use(Club:1079)
use(Moonfire:595) [ !weather(Moonlight:596) ]
use(Prowl:536) [ enemy(#3).active ]
use(Spirit Claws:974)
```

#### Desert Survivors
**URL:** [https://www.wow-petguide.com/Encounter/725/Desert_Survivors](https://www.wow-petguide.com/Encounter/725/Desert_Survivors)

##### Strategy: Default Strategy
```text
use(Whirlpool:513)
use(Inner Vision:216) [enemy.aura(Whirlpool:512).exists & enemy(#3).active]
use(Inner Vision:216) [enemy.aura(Underground:340).exists]
use(Inner Vision:216) [enemy.aura(Whirlpool:512).duration=1]
use(Punch:111)
use(Pounce:535) [enemy(#2).active]
use(Supercharge:208)
use(Pounce:535)
change(next)
```

#### What Do You Mean, Mind Controlling Plants?
**URL:** [https://www.wow-petguide.com/Encounter/726/What_Do_You_Mean,_Mind_Controlling_Plants](https://www.wow-petguide.com/Encounter/726/What_Do_You_Mean,_Mind_Controlling_Plants)

##### Strategy: Default Strategy
```text
use(Curse of Doom:218)
use(Haunt:652)
change(#2) [self(#1).dead & !self(#2).active]
use(Black Claw:919) [round=3]
use(Black Claw:919) [round=9]
standby [self.aura(Stunned).duration>=1]
use(Savage Talon:518) [enemy.aura(Shattered Defenses:542).exists]
use(Flock:581)
use(Arcane Storm:589)
change(#3) [self(#2).dead & !self(#3).active]
use(Falcosaur Swarm!:1773)
```

#### Snakes on a Terrace
**URL:** [https://www.wow-petguide.com/Encounter/727/Snakes_on_a_Terrace](https://www.wow-petguide.com/Encounter/727/Snakes_on_a_Terrace)

##### Strategy: Default Strategy
```text
use(Puppy Parade:1681) [ self.round=1 ]
use(Howl:362)
use(Moonfire:595) [ round=4 ]
use(Prowl:536)
use(#1) [ !enemy(#1).active & enemy.round!=1 ]
change(next)
```

#### Ezra Grimm
**URL:** [https://www.wow-petguide.com/Encounter/1116/Ezra_Grimm](https://www.wow-petguide.com/Encounter/1116/Ezra_Grimm)

##### Strategy: Default Strategy
```text
change(#2) [self.aura(Howl:1725).exists & self(#1).active]
change(#1) [self(#2).active & enemy(#3).active & enemy.hpp=100 & enemy.aura(Blinding Poison:1048).exists]
change(#2) [self(#3).active & enemy(#3).active]
change(#3) [self(#2).active & enemy(#2).active]
change(#2) [round=3]
use(Blistering Cold:786)
use(Chop:943)
use(Blinding Poison:1049)
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
use(Barbed Stinger:1369)
--
use(Dodge:312) [self.aura(Elementium Bolt:605).exists]
use(Tornado Punch:1052) [enemy.hp<335]
use(Jab:219)
change(#3)
```

#### Postmaster Malown
**URL:** [https://www.wow-petguide.com/Encounter/1117/Postmaster_Malown](https://www.wow-petguide.com/Encounter/1117/Postmaster_Malown)

##### Strategy: Default Strategy
```text

```

### Broken Isles

#### Clone Dance
**URL:** [https://www.wow-petguide.com/Encounter/1060/Clone_Dance](https://www.wow-petguide.com/Encounter/1060/Clone_Dance)

##### Strategy: Default Strategy
```text

```

#### Darkness
**URL:** [https://www.wow-petguide.com/Encounter/1061/Darkness](https://www.wow-petguide.com/Encounter/1061/Darkness)

##### Strategy: Default Strategy
```text

```

#### AoE/Cleave
**URL:** [https://www.wow-petguide.com/Encounter/1062/AoE/Cleave](https://www.wow-petguide.com/Encounter/1062/AoE/Cleave)

##### Strategy: Default Strategy
```text

```

#### Dazzling Dance
**URL:** [https://www.wow-petguide.com/Encounter/1063/Dazzling_Dance](https://www.wow-petguide.com/Encounter/1063/Dazzling_Dance)

##### Strategy: Default Strategy
```text

```

#### Leeching
**URL:** [https://www.wow-petguide.com/Encounter/1064/Leeching](https://www.wow-petguide.com/Encounter/1064/Leeching)

##### Strategy: Default Strategy
```text

```

#### Sandstorm (Shielding)
**URL:** [https://www.wow-petguide.com/Encounter/1065/Sandstorm_(Shielding)](https://www.wow-petguide.com/Encounter/1065/Sandstorm_(Shielding))

##### Strategy: Default Strategy
```text

```

#### Bleeding
**URL:** [https://www.wow-petguide.com/Encounter/1119/Bleeding](https://www.wow-petguide.com/Encounter/1119/Bleeding)

##### Strategy: Default Strategy
```text

```

#### Black Claw
**URL:** [https://www.wow-petguide.com/Encounter/1120/Black_Claw](https://www.wow-petguide.com/Encounter/1120/Black_Claw)

##### Strategy: Default Strategy
```text

```

#### Toxic Fumes
**URL:** [https://www.wow-petguide.com/Encounter/1155/Toxic_Fumes](https://www.wow-petguide.com/Encounter/1155/Toxic_Fumes)

##### Strategy: Default Strategy
```text

```

#### Miscellaneous
**URL:** [https://www.wow-petguide.com/Encounter/1067/Miscellaneous](https://www.wow-petguide.com/Encounter/1067/Miscellaneous)

##### Strategy: Default Strategy
```text

```

#### Using PvE Pets
**URL:** [https://www.wow-petguide.com/Encounter/1070/Using_PvE_Pets](https://www.wow-petguide.com/Encounter/1070/Using_PvE_Pets)

##### Strategy: Default Strategy
```text

```

## Draenor

### Garrison

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Encounter/438/Foe_Reaper_50](https://www.wow-petguide.com/Encounter/438/Foe_Reaper_50)

##### Strategy: Default Strategy
```text
use(753) [ round=5 ]
use(404)
use(282)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Encounter/442/Unfortunate_Defias](https://www.wow-petguide.com/Encounter/442/Unfortunate_Defias)

##### Strategy: Default Strategy
```text
use(541) [ enemy(#1).active ]
use(253) [ enemy.aura(542).exists ]
use(163)
use(490) [ self.aura(512).duration=1 ]
use(490) [ enemy.aura(341).exists ]
use(436) [ self.aura(435).duration<=1 & enemy(#3).hp>227 ]
use(#1)
change(#2)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Encounter/444/Angry_Geode](https://www.wow-petguide.com/Encounter/444/Angry_Geode)

##### Strategy: Default Strategy
```text
ability(Dive:564) [enemy.aura(Stoneskin:435).exists & enemy.ability(Crystal Prison:569).usable]
ability(Nature's Ward:574) [self.hpp<100 & !self.aura(Nature's Ward:820).exists]
ability(#1)
change(next)
```

#### Mining Monkey
**URL:** [https://www.wow-petguide.com/Encounter/448/Mining_Monkey](https://www.wow-petguide.com/Encounter/448/Mining_Monkey)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=2]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### "Captain" Klutz
**URL:** [https://www.wow-petguide.com/Encounter/452/"Captain"_Klutz](https://www.wow-petguide.com/Encounter/452/"Captain"_Klutz)

##### Strategy: Default Strategy
```text
standby [ enemy.round < 3 ]
ability(218)
ability(652)
change(#2)
ability(919) [ !enemy.aura(918).exists ]
ability(581)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Encounter/456/Klutz's_Battle_Rat](https://www.wow-petguide.com/Encounter/456/Klutz's_Battle_Rat)

##### Strategy: Default Strategy
```text
ability(124)
ability(202)
change(#2)

ability(#3) [enemy.hp<618 & enemy.type !~ 3]
ability(#3) [enemy.hp<406 & enemy.type ~ 3]
ability(#2) [!self(#2).aura(820).exists]
ability(#1)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Encounter/458/Klutz's_Battle_Monkey](https://www.wow-petguide.com/Encounter/458/Klutz's_Battle_Monkey)

##### Strategy: Default Strategy
```text
use(208) [ round=1 ]
use(204)
use(490) [ self.aura(512).duration=1 ]
use(490) [ enemy.aura(341).exists ]
use(436) [ self.aura(435).duration<=1 & enemy(#3).hp>227 ]
use(#1)
change(#2)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Encounter/460/Klutz's_Battle_Bird](https://www.wow-petguide.com/Encounter/460/Klutz's_Battle_Bird)

##### Strategy: Default Strategy
```text
use(weather:595) [ !weather(weather:596) ]
use(dodge:440) [ enemy(#1).active & round = 4 ]
use(dodge:440) [ !enemy(#1).active ]
use(filler:421)
```

#### Cookie's Leftovers
**URL:** [https://www.wow-petguide.com/Encounter/464/Cookie's_Leftovers](https://www.wow-petguide.com/Encounter/464/Cookie's_Leftovers)

##### Strategy: Default Strategy
```text
standby [ round=1]
standby [ self.aura(Asleep:926).exists]
use(Blistering Cold:786) [self.ability(Blistering Cold:786).usable]
use(Chop:943) [!enemy.aura(Bleeding:491).exists]
use(BONESTORM!!:1762)
change(#2) [self(#1).dead]
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
use(Flock:581)
```

### The Menagerie

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

### Tamers

## Pandaria

### Spirit Tamers

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

### Beasts of Fable

#### Dos-Ryga
**URL:** [https://www.wow-petguide.com/Encounter/69/Dos-Ryga](https://www.wow-petguide.com/Encounter/69/Dos-Ryga)

##### Strategy: Default Strategy
```text
change(#1) [self(#2).active & self.dead]
change(#2) [round=2]
use(Supercharge:208) [self.aura(Wind-Up:458).exists]
use(Wind-Up:459)
use(Howl:362) [self.aura(Undead:242).exists]
use(Diseased Bite:499)
```

#### Kafi
**URL:** [https://www.wow-petguide.com/Encounter/70/Kafi](https://www.wow-petguide.com/Encounter/70/Kafi)

##### Strategy: Default Strategy
```text
use(Explode:282) [enemy.hp.can_explode]
use(282) [enemy.aura(639).exists & enemy.hp<700]
use(282) [self(#1).active & round>2]
use(Toxic Smoke:640) [!enemy.aura(639).exists]
use(Reflective Shield:1105)
use(#1)
standby
change(next)
```

#### Ti'un the Wanderer
**URL:** [https://www.wow-petguide.com/Encounter/71/Ti'un_the_Wanderer](https://www.wow-petguide.com/Encounter/71/Ti'un_the_Wanderer)

##### Strategy: Default Strategy
```text
if [ self(#1).active]
standby [enemy(#1).hp.can_be_exploded]
ability(Black Claw:919) [ round=1 ]
ability(#3) [ enemy.aura(Black Claw:918).exists ]
ability(#1) [ !enemy.hp.can_be_exploded]
endif
change(#3) [ self(#1).dead ]
ability(#1) [ !enemy.hp.can_be_exploded]
ability(Explode:282) [ enemy.hp.can_be_exploded]
```

#### No-No
**URL:** [https://www.wow-petguide.com/Encounter/72/No-No](https://www.wow-petguide.com/Encounter/72/No-No)

##### Strategy: Default Strategy
```text
use(Predatory Strike:518) [round=1]
use(Crouch:165) [enemy.aura(Underwater:830).exists]
use(Ironskin:1758) [enemy.aura(Underwater:830).exists]
standby [self(#2).active & enemy.aura(Underwater:830).exists]
use(Falcosaur Swarm!:1773) [enemy.aura(Beaver Dam:326).exists]
use(Predatory Strike:518) [enemy.aura(Shattered Defenses:542).exists]
use(Savage Talon:1370) [enemy.aura(Shattered Defenses:542).exists]
use(Falcosaur Swarm!:1773)
change(next)
```

#### Gorespine
**URL:** [https://www.wow-petguide.com/Encounter/73/Gorespine](https://www.wow-petguide.com/Encounter/73/Gorespine)

##### Strategy: Default Strategy
```text
use(Explode:282) [enemy.hp<=1250]
use(Reflective Shield:1105) [self.round=1]
use(#1)
change(next)
```

#### Skitterer Xi'a
**URL:** [https://www.wow-petguide.com/Encounter/74/Skitterer_Xi'a](https://www.wow-petguide.com/Encounter/74/Skitterer_Xi'a)

##### Strategy: Default Strategy
```text
use(Flyby:515) [round=1]
use(Thunderbolt:779)
use(Explode:282)
change(next)
```

#### Greyhoof
**URL:** [https://www.wow-petguide.com/Encounter/75/Greyhoof](https://www.wow-petguide.com/Encounter/75/Greyhoof)

##### Strategy: Default Strategy
```text
ability(Wind-Up:459) [round=1]
ability(Supercharge:208) [round=2]
ability(Wind-Up:459) [round=3]
ability(Powerball:566)
change(#2) [self(#1).dead]
ability(Explode:282) [enemy.hp<614]
ability(Decoy:334)
ability(Missile:777)
```

#### Lucky Yi
**URL:** [https://www.wow-petguide.com/Encounter/76/Lucky_Yi](https://www.wow-petguide.com/Encounter/76/Lucky_Yi)

##### Strategy: Default Strategy
```text
use(Hunting Party:921) [enemy.aura(918).exists]
use(Black Claw:919) [self.round=1]
use(Leap:364)
change(next)
```

#### Ka'wi the Gorger
**URL:** [https://www.wow-petguide.com/Encounter/77/Ka'wi_the_Gorger](https://www.wow-petguide.com/Encounter/77/Ka'wi_the_Gorger)

##### Strategy: Default Strategy
```text
change(#2) [self(#1).dead]
use(Garra negra:919) [!enemy.aura(Garra negra:918).exists]
use(Bandada:581)
use(Grupo de caza:921)
use(Saltar:364)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Encounter/78/Nitun](https://www.wow-petguide.com/Encounter/78/Nitun)

##### Strategy: Default Strategy
```text
use(Curse of Doom:218)
use(Haunt:652)
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
use(Flock:581)
change(next)
```

#### https://www.wow-petguide.com/Strategy/11487/The_Mind_Games_of_Addius
**URL:** [https://www.wow-petguide.com/Strategy/11487/The_Mind_Games_of_Addius](https://www.wow-petguide.com/Strategy/11487/The_Mind_Games_of_Addius)

##### Strategy: Default Strategy
```text
use(1015) [round~1,4]
use(282) [round~3,6]
use(270)
use(359)
use(2223)

change(next)
```

### Tamers

#### Ashlei
**URL:** [https://www.wow-petguide.com/Encounter/16/Ashlei](https://www.wow-petguide.com/Encounter/16/Ashlei)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [enemy.aura(Flammenatem:500).exists & enemy.aura(Messerkrallen:2238).exists & enemy(#3).active]
use(Messerkrallen:2237) [enemy.aura(Flammenatem:500).exists & !enemy.aura(Messerkrallen:2238).exists]
use(Flammenatem:501)
```

#### Cymre Brightblade
**URL:** [https://www.wow-petguide.com/Encounter/17/Cymre_Brightblade](https://www.wow-petguide.com/Encounter/17/Cymre_Brightblade)

##### Strategy: Default Strategy
```text
change(#1) [self(#3).played]
change(#2) [round=3]
use(Nether Gate:466) [round=2]
use(Burn:113) [enemy(#3).active]
use(Flamethrower:503)
use(Flame Breath:501) [enemy(#2).active]
use(Time Bomb:602)
use(Armageddon:1025)
change(#3)
```

#### Gargra
**URL:** [https://www.wow-petguide.com/Encounter/18/Gargra](https://www.wow-petguide.com/Encounter/18/Gargra)

##### Strategy: Default Strategy
```text
change(#2) [enemy(#2).active & !self(#2).played]
change(#1) [self(#2).active]
use(Fel Immolate:901) [enemy(#3).active]
use(Supercharge:208)
use(Haywire:916)
use(Ion Cannon:209)
change(#3)
```

#### Taralune
**URL:** [https://www.wow-petguide.com/Encounter/19/Taralune](https://www.wow-petguide.com/Encounter/19/Taralune)

##### Strategy: Default Strategy
```text
if [enemy(#1).active]
standby [round=1]
ability(Supercharge:208) [round=3]
ability(Wind-Up:459)
endif

change(#3) [self(#1).dead & !self(#3).played]
change(#2) [self(#3).active]
ability(Arcane Storm:589)
ability(Mana Surge:489)
ability(#2)
ability(#1)
```

#### Tarr the Terrible
**URL:** [https://www.wow-petguide.com/Encounter/20/Tarr_the_Terrible](https://www.wow-petguide.com/Encounter/20/Tarr_the_Terrible)

##### Strategy: Default Strategy
```text
change(#1) [self(#2).played]
change(#2) [round=4]
use(Corrosion:447) [round=1]
use(Poison Protocol:1954)
use(Void Nova:2356)
use(Corrosion:447)
use(Raise Ally:2298)
use(Dead Man's Party:1093)
change(#3)
```

#### Vesharr
**URL:** [https://www.wow-petguide.com/Encounter/21/Vesharr](https://www.wow-petguide.com/Encounter/21/Vesharr)

##### Strategy: Default Strategy
```text
ability(Arcane Explosion:299)
ability(Explode:282) [enemy.aura(Mechanical:244).exists]
ability(Thunderbolt:779) [!enemy.aura(Flying Mark:1420).exists]
ability(Breath:115)
change(#2)
```

### Celestial Tournament

#### Taran Zhu
**URL:** [https://www.wow-petguide.com/Encounter/37/Taran_Zhu](https://www.wow-petguide.com/Encounter/37/Taran_Zhu)

##### Strategy: Default Strategy
```text
ability(Call Lightning:204)
standby [ round=2 ]

change(Infernal Pyreclaw:2089)
ability(Great Sting:1966) [ self.round=1 ]
standby [ self.round=5 ]
standby [ self.round=6 ]
ability(Great Sting:1966) [ self.round=7 ]
ability(Cleave:1273)

change(Anomalus:2842)
ability(Poison Protocol:1954)
ability(Void Nova:2356)
ability(Corrosion:447)
```

#### Wrathion
**URL:** [https://www.wow-petguide.com/Encounter/38/Wrathion](https://www.wow-petguide.com/Encounter/38/Wrathion)

##### Strategy: Default Strategy
```text
change(next) [self.dead]
use(Dodge:312) [self.aura(Ice Tomb:623).duration = 1]
use(Stampede:163) [enemy(Cindy:1299).active & enemy.round = 4]
use(Stampede:163) [enemy(Alex:1301).active & !self.aura(Ice Tomb:623).exists]
standby [enemy.aura(Undead:242).exists]
use(Scratch:119)
use(Crush:406) [enemy(Alex:1301).aura(Shattered Defenses:542).exists]
use(Stoneskin:436) [!self.aura(Stoneskin:435).exists]
use(Deflection:490) [self.aura(Elementium Bolt:605).duration = 1]
use(Crush:406)
use(Dead Man's Party:1093)
use(Macabre Maraca:1094)
```

#### Chen Stormstout
**URL:** [https://www.wow-petguide.com/Encounter/39/Chen_Stormstout](https://www.wow-petguide.com/Encounter/39/Chen_Stormstout)

##### Strategy: Default Strategy
```text
change(next) [ enemy(#2).active & !self(#3).played ]
ability(Decoy:334)
ability(Haywire:916)
ability(Dodge:312) [ enemy(#2).active ]
ability(Dodge:312) [ enemy.aura(Barrel Ready:353).exists ]
ability(Ravage:802) [ enemy(#2).active & enemy.hp<927 ]
ability(Ravage:802) [ enemy(#3).hp<619 ]
ability(#1)
change(#1)
```

#### Shademaster Kiryn
**URL:** [https://www.wow-petguide.com/Encounter/43/Shademaster_Kiryn](https://www.wow-petguide.com/Encounter/43/Shademaster_Kiryn)

##### Strategy: Default Strategy
```text
change(#3) [enemy(Eté:1286).active & !self(#3).played]
change(#2) [self(#3).active]

use(Frappé par l’amour:772) [enemy(Stormoen:1287).active]

use(Malédiction funeste:218) [!enemy(Eté:1286).active]
use(Horion de l’ombre:422) [enemy(Nairn:1288).active]

standby [enemy.aura(Esquive:311).exists]
use(Prison de cristal:569) [enemy.aura(Rôder:543).exists]
use(Peau de pierre:436) [enemy(Eté:1286).active & !self.aura(Peau de pierre:435).exists ]
use(Peau de pierre:436) [enemy(Eté:1286).active & enemy.round =1]
use(Brûlure:113)

use(Frappé par l’amour:772) [enemy.aura(Rôder:543).exists]
use(Horion de l’ombre:422)

change(#1)
```

#### Wise Mari
**URL:** [https://www.wow-petguide.com/Encounter/41/Wise_Mari](https://www.wow-petguide.com/Encounter/41/Wise_Mari)

##### Strategy: Default Strategy
```text
ability(Blingtron Gift Package:989) [ enemy.aura(Make it Rain:986).duration=1 ]
ability(Make it Rain:985)
ability(Inflation:1002)
ability(Consume Magic:1231) [ self.aura(Whirlpool:512).exists ]
ability(Creeping Ooze:448)
change(#2)
```

#### Blingtron 4000
**URL:** [https://www.wow-petguide.com/Encounter/42/Blingtron_4000](https://www.wow-petguide.com/Encounter/42/Blingtron_4000)

##### Strategy: Default Strategy
```text
ability(Pump:297) [round~1,3]
ability(Water Jet:118)

ability(Nature's Ward:574) [!self.aura(Nature's Ward:820).exists]
ability(Hawk Eye:521) [!self.aura(Hawk Eye:520).exists]
ability(Claw:429)

ability(Conflagrate:179) [enemy.aura(Immolate:177).exists]
ability(Immolate:178) [!enemy.aura(Immolate:177).exists]
ability(Burn:113)

change(next)
```

#### Sully "The Pickle" McLeary
**URL:** [https://www.wow-petguide.com/Encounter/45/Sully_"The_Pickle"_McLeary](https://www.wow-petguide.com/Encounter/45/Sully_"The_Pickle"_McLeary)

##### Strategy: Default Strategy
```text
ability(Swarm of Flies:232) [ !enemy.aura(Swarm of Flies:231).exists ]
ability(Healing Wave:123) [ self.hpp<75 ]
ability(Swarm of Flies:232) [ enemy.aura(Undead:242).exists ]
ability(Swarm of Flies:232) [ enemy.aura(Underground:340).exists ]
ability(Tongue Lash:228)
change(#2) [ self(#1).dead & enemy(#2).active ]
ability(Lift-Off:170) [ enemy(#3).active ]
ability(Thrash:202)
change(#3)
ability(Call Darkness:256)
ability(Nocturnal Strike:517) [ weather(Darkness:257) ]
ability(#1)
```

#### Dr. Ion Goldbloom
**URL:** [https://www.wow-petguide.com/Encounter/46/Dr._Ion_Goldbloom](https://www.wow-petguide.com/Encounter/46/Dr._Ion_Goldbloom)

##### Strategy: Default Strategy
```text
use(Howl:362) [enemy.aura(Flying:341).exists]
use(Surge of Power:593) [enemy.aura(Howl:1725).exists]
use(Arcane Explosion:299)
use(Conflagrate:179) [enemy(#3).active]
use(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]
use(Scorched Earth:172)
use(Ion Cannon:209) [enemy(#3).hp<1142]
use(#1)
change(next)
```

#### Lorewalker Cho
**URL:** [https://www.wow-petguide.com/Encounter/47/Lorewalker_Cho](https://www.wow-petguide.com/Encounter/47/Lorewalker_Cho)

##### Strategy: Default Strategy
```text
ability(Life Exchange:277) [ enemy(#2).active ]
ability(Moonfire:595)
if [ enemy(#3).active ]
    ability(Plagued Blood:657) [ !enemy.aura(Plagued Blood:658).exists ]
    ability(Death and Decay:214) [ !enemy.aura(Death and Decay:213).exists ]
    ability(Kick:307)
endif
ability(#1)
change(#2)
```

#### Chi-Chi, Hatchling of Chi-Ji
**URL:** [https://www.wow-petguide.com/Encounter/51/Chi-Chi,_Hatchling_of_Chi-Ji](https://www.wow-petguide.com/Encounter/51/Chi-Chi,_Hatchling_of_Chi-Ji)

##### Strategy: Default Strategy
```text
standby [ round=7 & self(#3).active ]
use(409) [ round=1 ]
use(592) [ round=2 ]
use(163) [ round=4 ]
use(518)
change(next)
```

#### Zao, Calfling of Niuzao
**URL:** [https://www.wow-petguide.com/Encounter/52/Zao,_Calfling_of_Niuzao](https://www.wow-petguide.com/Encounter/52/Zao,_Calfling_of_Niuzao)

##### Strategy: Default Strategy
```text
use(Nut Barrage:167) [round=1]
use(Woodchipper:411) [self(#1).active]
use(Black Claw:919) [self.round=1 & self(#2).active]
use(Hunting Party:921) [self(#2).active]
use(Leap:364) [self(#2).active]
use(#1)
change(next)
```

#### Xu-Fu, Cub of Xuen
**URL:** [https://www.wow-petguide.com/Encounter/49/Xu-Fu,_Cub_of_Xuen](https://www.wow-petguide.com/Encounter/49/Xu-Fu,_Cub_of_Xuen)

##### Strategy: Default Strategy
```text
use(116) [ round=1 ]
use(282)
use(518)
change(#2)
```

#### Yu'la, Broodling of Yu'lon
**URL:** [https://www.wow-petguide.com/Encounter/50/Yu'la,_Broodling_of_Yu'lon](https://www.wow-petguide.com/Encounter/50/Yu'la,_Broodling_of_Yu'lon)

##### Strategy: Default Strategy
```text
ability(Illuminate:460)
ability(Explode:282)
ability(#1) [self(#3).dead]
change(next)
```

#### another strategy
**URL:** [https://www.wow-petguide.com/Strategy/4924/Yula,_Broodling_of_Yulon](https://www.wow-petguide.com/Strategy/4924/Yula,_Broodling_of_Yulon)

##### Strategy: Default Strategy
```text
use(Clobber:350)
use(Dive:564) [enemy(Yu'la, Broodling of Yu'lon:1317).aura(Flying:341).exists]
use(Punch:111)
use(#1)
change(next)
```

## Dungeons

### Wailing Caverns

#### Human Resources
**URL:** [https://www.wow-petguide.com/Encounter/729](https://www.wow-petguide.com/Encounter/729)

##### Strategy: Default Strategy
```text
ability(Deflection:490) [enemy(Fungus:2233).active]
ability(Deflection:490) [enemy(Murray:2232).active]
ability(Deflection:490) [self.aura(Whirlpool:512).duration=1]
ability(Sandstorm:453) [enemy.hp>227]
ability(Reckless Strike:186) 
ability(Frost Shock:416) [self.round=1]
ability(Deep Freeze:481)
ability(#1)
standby
change(next)
```

#### Dragons Make Everything Better
**URL:** [https://www.wow-petguide.com/Encounter/759](https://www.wow-petguide.com/Encounter/759)

##### Strategy: Default Strategy
```text
use(Arcane Storm:589) [!weather(Arcane Winds:590)]
use(Mana Surge:489)
use(Moonfire:595) [!weather(Moonlight:596)]
use(Life Exchange:277) [self.hp<500]
use(#1)
change(next)
```

#### Fun With Flying
**URL:** [https://www.wow-petguide.com/Encounter/789](https://www.wow-petguide.com/Encounter/789)

##### Strategy: Default Strategy
```text
standby [ enemy(#2).active & enemy.round=1 ]
ability(#2) [ !enemy(#3).active ]
ability(#3) [ enemy.aura(Shattered Defenses:542).exists ]
ability(#1)
change(#2)
```

#### Not Quite Dead Yet
**URL:** [https://www.wow-petguide.com/Encounter/819](https://www.wow-petguide.com/Encounter/819)

##### Strategy: Default Strategy
```text
change(next) [ self.dead ] 
ability(170) [ !self.aura(242).exists ] 
ability(420) 
ability(1392) [ enemy(2231).active & enemy.round = 1 ] 
ability(752) [ enemy(2232).hp < 463 ] 
ability(752) [ enemy(2231).active ] 
ability(1066)
```

#### Critters With Huge Teeth
**URL:** [https://www.wow-petguide.com/Encounter/849](https://www.wow-petguide.com/Encounter/849)

##### Strategy: Default Strategy
```text
use(Hawk Eye:521) [!self.aura(Hawk Eye:520).exists]
use(Flock:581)
use(Lovestruck:772) [enemy(#2).active & !enemy(#3).dead]
use(Predatory Strike:518) [enemy.hp<630 & enemy(#2).active]
use(#1)
change(next)
```

#### Magicians Secret
**URL:** [https://www.wow-petguide.com/Encounter/879](https://www.wow-petguide.com/Encounter/879)

##### Strategy: Default Strategy
```text
use(Evanescence:440) [round=1]
use(Forboding Curse:1068) [round=2]
use(Forboding Curse:1068) [enemy.round=1]
use(Lift-Off:170) [self.aura(Whirlpool:512).duration=1]
use(Lift-Off:170) [enemy(Murray:2232).hp>462]
use(Adrenaline Rush:162) [self.speed.slow]
use(Spectral Spine:913)
use(#1)
change(next)
```

#### Element of Success
**URL:** [https://www.wow-petguide.com/Encounter/909](https://www.wow-petguide.com/Encounter/909)

##### Strategy: Default Strategy
```text
ability(Wind Buffet:1963) [round=2] 
ability(Autumn Breeze:964) [round=4] 
ability(#1) 
change(next)
```

#### Beast Mode
**URL:** [https://www.wow-petguide.com/Encounter/939](https://www.wow-petguide.com/Encounter/939)

##### Strategy: Default Strategy
```text
ability(Tough n' Cuddly:1112) [self.round=1]
ability(Headbutt:376) [self.aura(Beast:237).exists]

ability(Prowl:536) [self.round=1]
ability(Moonfire:595)

ability(#1)
change(next)
```

#### Hobbyist Aquarist
**URL:** [https://www.wow-petguide.com/Encounter/969](https://www.wow-petguide.com/Encounter/969)

##### Strategy: Default Strategy
```text
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists & enemy(#1).active]
use(Black Claw:919) [!enemy.aura(Black Claw:918).exists & enemy(#2).active]
use(Swarm:706) [!enemy.aura(Shattered Defenses:542).exists]
use(Sandstorm:453)
use(Bubble:934) [self.aura(Whirlpool:512).duration=1]
use(#1)
change(next)
```

#### Machine Learning
**URL:** [https://www.wow-petguide.com/Encounter/999](https://www.wow-petguide.com/Encounter/999)

##### Strategy: Default Strategy
```text
ability(Supercharge:208) [ self.aura(Wind-Up:458).exists ]
ability(Wind-Up:459)
change(next) [ !self.ability(Haywire:916).usable ]
ability(Haywire:916)
change(next)
```

#### Delia HanakoQuest: That's a Big Carcass
**URL:** [https://www.wow-petguide.com/Encounter/729/That's_a_Big_Carcass](https://www.wow-petguide.com/Encounter/729/That's_a_Big_Carcass)

##### Strategy: Default Strategy
```text
ability(Deflection:490) [enemy(Fungus:2233).active]
ability(Deflection:490) [enemy(Murray:2232).active]
ability(Deflection:490) [self.aura(Whirlpool:512).duration=1]
ability(Sandstorm:453) [enemy.hp>227]
ability(Reckless Strike:186) 
ability(Frost Shock:416) [self.round=1]
ability(Deep Freeze:481)
ability(#1)
standby
change(next)
```

#### BurlyQuest: Strange Looking Dogs
**URL:** [https://www.wow-petguide.com/Encounter/730/Strange_Looking_Dogs](https://www.wow-petguide.com/Encounter/730/Strange_Looking_Dogs)

##### Strategy: Default Strategy
```text
use(Ice Tomb:624) [enemy.hpp = 100 & !enemy.aura(Ice Tomb:623).exists]
use(Call Blizzard:206) [!enemy.aura(Undead:242).exists & !weather(Blizzard:205)]
use(#1)

standby
change(next)
```

#### KwintQuest: Not So Bad Down Here
**URL:** [https://www.wow-petguide.com/Encounter/731/Not_So_Bad_Down_Here](https://www.wow-petguide.com/Encounter/731/Not_So_Bad_Down_Here)

##### Strategy: Default Strategy
```text
change(next) [self.dead] 
standby [self.aura(Stunned:927).exists] 
ability(Focus:426) [round=1] 
ability(Call Lightning:204) 
ability(Zap:116) 
ability(Flyby:515) [enemy(#3).active & !enemy.aura(Weakened Defenses:516).exists] 
ability(Lift-Off:170) 
ability(Slicing Wind:420) 
ability(Greench's Gift:1076) 
ability(#1)
```

#### Leana DarkwindQuest: Captured Evil
**URL:** [https://www.wow-petguide.com/Encounter/734/Captured_Evil](https://www.wow-petguide.com/Encounter/734/Captured_Evil)

##### Strategy: Default Strategy
```text
ability(Backflip:669)
ability(Poison Lash:398) [!enemy.aura(Poisoned:379).exists]
ability(Dazzling Dance:366) [!self.aura(Dazzling Dance:365).exists]
ability(Frost Shock:416) [!enemy.aura(Frost Shock:415).exists]
ability(Deep Freeze:481)
ability(#1)
change(next)
```

#### Ellie VernQuest: Sea Creatures Are Weird
**URL:** [https://www.wow-petguide.com/Encounter/735/Sea_Creatures_Are_Weird_](https://www.wow-petguide.com/Encounter/735/Sea_Creatures_Are_Weird_)

##### Strategy: Default Strategy
```text
use(Ice Tomb:624) [enemy.aura(Undead:242).exists]
standby [enemy.aura(Undead:242).exists]
use(Ice Tomb:624) [enemy.hpp>95 & !enemy.aura(Ice Tomb:623).exists]
use(Call Blizzard:206)
use(Ice Lance:413)
change(#1)
change(next)
```

#### Eddie FixitQuest: Automated Chaos
**URL:** [https://www.wow-petguide.com/Encounter/736/Automated_Chaos](https://www.wow-petguide.com/Encounter/736/Automated_Chaos)

##### Strategy: Default Strategy
```text
standby [ enemy("Fixed" Remote Control Rocket Chicken:2204).active ]
use(Sandstorm:453)
use(Rupture:814)
use(Crush:406)
use(#1)
change(next)
```

#### Michael SkarnQuest: What's the Buzz?
**URL:** [https://www.wow-petguide.com/Encounter/739/What's_the_Buzz](https://www.wow-petguide.com/Encounter/739/What's_the_Buzz)

##### Strategy: Default Strategy
```text
use(Deflection:490) [round=11]
use(Stoneskin:436) [self.aura(Stoneskin:435).duration<2]
standby
change(next)
```

#### Fizzie SparkwhistleQuest: Rogue Azerite
**URL:** [https://www.wow-petguide.com/Encounter/740/Rogue_Azerite](https://www.wow-petguide.com/Encounter/740/Rogue_Azerite)

##### Strategy: Default Strategy
```text
ability(Clobber:350) [enemy(Azerite Slime:2210).active]
ability(Backflip:669) [enemy(Azerite Slime:2210).active]
ability(Bubble:934) [enemy(Azerite Elemental:2212).active]
ability(#1)
change(next)
```

#### Dilbert McClintQuest: Night Horrors
**URL:** [https://www.wow-petguide.com/Encounter/741/Night_Horrors](https://www.wow-petguide.com/Encounter/741/Night_Horrors)

##### Strategy: Default Strategy
```text
standby [self.aura(Blinding Poison:1048).exists]
use(Booby-Trapped Presents:1080) [!enemy.aura(Booby-Trapped Presents:1081).exists]
use(Greench's Gift:1076) [enemy(Atherton:2209).aura(Underground:340).exists]
use(Greench's Gift:1076) [enemy.ability(Burrow:159).duration>=1 & enemy.ability(Blinding Poison:1049).duration>=1]
use(Greench's Gift:1076) [enemy(Jennings:2208).active]
use(Gift of Winter Veil:586)
use(Call Blizzard:206)
use(Ice Lance:413)
use(Dive Bomb:2463)
use(Arm Cannon Blast:2462)
change(next)
```

#### Captain HermesQuest: Crab People
**URL:** [https://www.wow-petguide.com/Encounter/742/Crab_People](https://www.wow-petguide.com/Encounter/742/Crab_People)

##### Strategy: Default Strategy
```text
use(Ice Tomb:624) [!enemy.aura(Ice Tomb:623).exists]
use(Call Blizzard:206)
use(Ice Lance:413)
change(next)
```

#### Talia SparkbrowQuest: Add More to the Collection
**URL:** [https://www.wow-petguide.com/Encounter/744/Add_More_to_the_Collection](https://www.wow-petguide.com/Encounter/744/Add_More_to_the_Collection)

##### Strategy: Default Strategy
```text
standby [enemy(#2).active & enemy.round=1 & self.speed.fast]
ability(Deflection:490) [enemy(#2).active & enemy.round=2]
ability(Deflection:490) [round=1]
ability(Rampage:124)
ability(Call Blizzard:206) [weather(Sandstorm:454)]
ability(Call Blizzard:206) [enemy.ability(Sandstorm:453).usable & self.speed.slow]
ability(Ice Lance:413) [enemy.ability(Cocoon Strike:506).usable & self.speed.slow]
ability(Ice Lance:413) [enemy(Whiplash:2366).aura(Silk Cocoon:505).exists]
ability(Gift of Winter's Veil:586) 
ability(#1)
change(next)
```

#### ZujaiQuest: Small Beginnings
**URL:** [https://www.wow-petguide.com/Encounter/745/Small_Beginnings](https://www.wow-petguide.com/Encounter/745/Small_Beginnings)

##### Strategy: Default Strategy
```text
use(Deflection:490) [self(#1).active]
use(Rampage:124)
use(Gift of Winter Veil:586)
use(Call Blizzard:206)
use(Deflection:490) [enemy(#3).active & enemy.ability(Frog Kiss:233).usable & !enemy.ability(Croak:932).usable]
use(Sandstorm:453) [enemy(#3).active]
use(#1)
standby
change(next)
```

#### KaragaQuest: Critters are Friends, Not Food
**URL:** [https://www.wow-petguide.com/Encounter/747/Critters_are_Friends,_Not_Food](https://www.wow-petguide.com/Encounter/747/Critters_are_Friends,_Not_Food)

##### Strategy: Default Strategy
```text
change(next) [ self.dead ]
ability(1080)
ability(1076)
ability(814) [ enemy.hp > 400 ]
ability(436) [ self.aura(435).duration <= 1 ]
ability(#1)
```

#### LozuQuest: Marshdwellers
**URL:** [https://www.wow-petguide.com/Encounter/750/Marshdwellers](https://www.wow-petguide.com/Encounter/750/Marshdwellers)

##### Strategy: Default Strategy
```text
ability(Ice Tomb:624) [round=1]
ability(Gift of Winter's Veil:586) [enemy(#2).active]
ability(Gift of Winter's Veil:586) [!enemy.ability(Cocoon Strike:506).usable]
ability(Call Blizzard:206) [!weather(Blizzard:205)]
ability(Ice Lance:413)
change(next)
```

#### Korval DarkbeardQuest: Accidental Dread
**URL:** [https://www.wow-petguide.com/Encounter/751/Accidental_Dread](https://www.wow-petguide.com/Encounter/751/Accidental_Dread)

##### Strategy: Default Strategy
```text
ability(Bubble:934) [round=1]
ability(Stampede:163) [!enemy.aura(Shattered Defenses:542).exists]
ability(#3)
ability(Call Blizzard:206)
ability(#1)
change(next)
```

#### Grady PrettQuest: Pack Leader
**URL:** [https://www.wow-petguide.com/Encounter/752/Pack_Leader](https://www.wow-petguide.com/Encounter/752/Pack_Leader)

##### Strategy: Default Strategy
```text
quit [self(#2).dead & !enemy(#2).aura(Egg Barrage:641).exists]
change(#2) [enemy(#2).active]
use(Call Lightning:204)
use(Swarm of Flies:232) [!enemy.aura(Swarm of Flies:231).exists]
use(Egg Barrage:642)
use(Booby-Trapped Presents:1080) [enemy.aura(Undead:242).exists]
use(Greench's Gift:1076) [enemy(#3).active]
use(#1)
change(next)
```

#### KeeyoQuest: Keeyo's Champions of Vol'dun
**URL:** [https://www.wow-petguide.com/Encounter/754/Keeyo's_Champions_of_Vol'dun](https://www.wow-petguide.com/Encounter/754/Keeyo's_Champions_of_Vol'dun)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Dodge:2060).exists]
ability(Gift of Winter's Veil:586)
ability(Call Blizzard:206) [round=2]
ability(Booby-Trapped Presents:1080) [self.round=1]
ability(Greench's Gift:1076) [enemy(Tikka:2346).hp<1060]
ability(Rampage:124)
ability(#1)
change(next)
```

#### KusaQuest: Desert Survivors
**URL:** [https://www.wow-petguide.com/Encounter/755/Desert_Survivors](https://www.wow-petguide.com/Encounter/755/Desert_Survivors)

##### Strategy: Default Strategy
```text
use(Deflection:490) [enemy.aura(Underground:340).exists]
use(Stoneskin:436) [!self.aura(Stoneskin:435).exists]
use(Stoneskin:436) [self.aura(Stoneskin:435).duration<2]
use(Crush:406)
use(#1)
change(next)
```

#### SizzikQuest: Snakes on a Terrace
**URL:** [https://www.wow-petguide.com/Encounter/757/Snakes_on_a_Terrace](https://www.wow-petguide.com/Encounter/757/Snakes_on_a_Terrace)

##### Strategy: Default Strategy
```text
standby [round=1]
ability(#1) [!enemy(#3).dead]
ability(#3)
```

### Deadmines

### Stratholme

#### Haunted Humanoids
**URL:** [https://www.wow-petguide.com/Encounter/1210](https://www.wow-petguide.com/Encounter/1210)

##### Strategy: Default Strategy
```text
change(#2) [round=2]
ability(Ice Tomb:624) [round=1]
ability(Ice Tomb:624) [enemy(#3).active & enemy.round=1]
ability(Booby-Trapped Presents:1080) [self.round=1]
ability(Greench's Gift:1076)
ability(Call Blizzard:206)
ability(#1)
change(#1)
```

#### Deathly Dragonkin
**URL:** [https://www.wow-petguide.com/Encounter/1225](https://www.wow-petguide.com/Encounter/1225)

##### Strategy: Default Strategy
```text
use(Arcane Storm:589) [ round>1 & !enemy(#2).active ]
if [ enemy(#1).active ]
    use(Surge of Power:593) [ enemy.hp<1099 & self.aura(Dragonkin:245).exists ]
    use(Surge of Power:593) [ enemy.hp<733 ]
endif
use(Surge of Power:593) [ enemy(#3).active ]
use(Arcane Blast:421)
use(Mana Surge:489)
change(next)
```

#### Flickering Fliers
**URL:** [https://www.wow-petguide.com/Encounter/1240](https://www.wow-petguide.com/Encounter/1240)

##### Strategy: Default Strategy
```text
use(Decoy:334)
use(Haywire:916) [ !enemy(#1).active ]
use(Alpha Strike:504)
use(Lift-Off:170) [ enemy.ability(Amplify Magic:488).usable & enemy.ability(Moonfire:595).duration<2 & !self.speed.fast ]
use(Shadowmeld:2253) [ enemy(#3).active ]
use(Dark Talon:1233)
standby
change(next)
```

#### Unholy Undead
**URL:** [https://www.wow-petguide.com/Encounter/1255](https://www.wow-petguide.com/Encounter/1255)

##### Strategy: Default Strategy
```text
use(Bash:348) [ round=1 ]
use(Toxic Smoke:640)
use(Slicing Wind:420) [ enemy.hp<163 & !self.aura(Undead).exists ]
use(Ghostly Bite:654) [ self.aura(Undead).exists ]
use(Lift-Off:170) [ !enemy.ability(Toxic Fumes:2349).usable & enemy.ability(Sludge Claw:2352).usable ]
use(Lift-Off:170) [ enemy.ability(Amplify Magic:488).usable & enemy.ability(Moonfire:595).duration<2 & self.speed.slow ]
use(Slicing Wind:420)
use(Roar of the Dead:2071) [ enemy.hp>497 ]
use(Spiritfire Bolt:1066)
change(next)
```

#### Creepy Critters
**URL:** [https://www.wow-petguide.com/Encounter/1270](https://www.wow-petguide.com/Encounter/1270)

##### Strategy: Default Strategy
```text
quit [self(#2).dead & !enemy(#2).dead]
use(Predatory Strike:518) [round=3]
use(Quicksand:912) [enemy.aura(Acidic Goo:368).exists]
use(Dive:564) [enemy.ability(Amplify Magic:488).usable & enemy.hp>420]
use(Acidic Goo:369) [enemy.hpp>50 & !enemy.aura(Acidic Goo:368).exists]
use(#1)
use(#2)
change(next)
```

#### Mummified Magics
**URL:** [https://www.wow-petguide.com/Encounter/1285](https://www.wow-petguide.com/Encounter/1285)

##### Strategy: Default Strategy
```text
standby [round=3]
use(Evanescence:440) [round=4]
use(Life Exchange:277) [enemy(#3).active]
use(Eyeblast:475) [enemy(#1).dead]
use(#1)
change(next)
```

#### Eerie Elementals
**URL:** [https://www.wow-petguide.com/Encounter/1300](https://www.wow-petguide.com/Encounter/1300)

##### Strategy: Default Strategy
```text
change(#3) [enemy(#3).active]
ability(Stun Seed:402)
ability(Toxic Smoke:640) [round=3]
ability(Call Lightning:204) 
ability(Surge of Power:593) [enemy(#3).active & enemy.hp<1362]
ability(#1)
change(next)
```

#### Beast Busters
**URL:** [https://www.wow-petguide.com/Encounter/1315](https://www.wow-petguide.com/Encounter/1315)

##### Strategy: Default Strategy
```text
use(Pheromones:1063)
use(Puncture Wound:1050)
use(Body Slam:532) [self(#1).active]

use(Gift of Winter's Veil:586) [enemy(#3).active]
change(#3) [enemy(#3).active]
use(Swipe:2346) [enemy(#2).active]
use(Arcane Dash:1536)
use(Soulrush:752)
use(Booby-Trapped Presents:1080)
use(Pounce:535)

standby [self.aura(Stunned:927).exists]
change(next)
```

#### Aquatic Apparitions
**URL:** [https://www.wow-petguide.com/Encounter/1330](https://www.wow-petguide.com/Encounter/1330)

##### Strategy: Default Strategy
```text
use(Ice Tomb:624)
use(Call Blizzard:206)
use(Surge:509) [ enemy.ability(Horn Attack:571).usable ]
use(Surge:509) [ enemy(#2).active & enemy.hp<211 ]
use(Ice Lance:413) [ weather(Blizzard:205) & !enemy.aura(Amplify Magic:487).exists ]
use(Surge:509)
use(Phase Shift:764) [ enemy.ability(Amplify Magic:488).usable & self.speed.slow ]
use(Expunge:450) [ enemy.aura(Amplify Magic:487).exists ]
use(Ooze Touch:445)
change(next)
```

#### Macabre Mechanicals
**URL:** [https://www.wow-petguide.com/Encounter/1345](https://www.wow-petguide.com/Encounter/1345)

##### Strategy: Default Strategy
```text
if [self(Darkmoon Zeppelin:339).active]
use(Explode:282) [enemy(Shelby:2972).active & enemy.hp <=618]
use(Decoy:334)
use(Missile:777)
endif
if [self(Iron Starlette:1387).active &enemy(Tinyhoof:2973).active]
use(Wind-Up:459)
endif
if [self(Iron Starlette:1387).active & enemy(Glitterwing:2974).active]
use(Toxic Smoke:640) [!enemy.aura(Toxic Smoke:639).exists]
use(Toxic Smoke:640) [self(Iron Starlette:1387).hp<500]
use(Wind-Up:459) [self.aura(Wind-Up:458).exists]
use(Wind-Up:459)
endif
if [self(Lil' Bling:1320).active]
use(Blingtron Gift Package:989)
use(Make it Rain:985) [!enemy.aura(Make it Rain:986).exists]
use(Inflation:1002)
endif
change(next)
```

#### StratiosQuest: Cliffs of Bastion
**URL:** [https://www.wow-petguide.com/Encounter/1210/Cliffs_of_Bastion](https://www.wow-petguide.com/Encounter/1210/Cliffs_of_Bastion)

##### Strategy: Default Strategy
```text
change(#2) [round=2]
ability(Ice Tomb:624) [round=1]
ability(Ice Tomb:624) [enemy(#3).active & enemy.round=1]
ability(Booby-Trapped Presents:1080) [self.round=1]
ability(Greench's Gift:1076)
ability(Call Blizzard:206)
ability(#1)
change(#1)
```

#### ZollaQuest: Micro Defense Force
**URL:** [https://www.wow-petguide.com/Encounter/1211/Micro_Defense_Force](https://www.wow-petguide.com/Encounter/1211/Micro_Defense_Force)

##### Strategy: Default Strategy
```text
ability(Ice Tomb:624) [round=1]
ability(Ice Tomb:624) [enemy(#3).active & enemy.round=1]
ability(Call Blizzard:206) [weather(Blizzard:205).duration<2]
ability(Ice Lance:413)
change(next)
```

#### TheniaQuest: Thenia's Loyal Companions
**URL:** [https://www.wow-petguide.com/Encounter/1212/Thenia's_Loyal_Companions](https://www.wow-petguide.com/Encounter/1212/Thenia's_Loyal_Companions)

##### Strategy: Default Strategy
```text
ability(Gift of Winter's Veil:586)
ability(Booby-Trapped Presents:1080) [enemy(#2).active]
ability(Call Blizzard:206) [weather(Blizzard:205).duration<2]
ability(Ice Lance:413)
standby
change(next)
```

#### Caregiver MaximillianQuest: Mighty Minions of Maldraxxus
**URL:** [https://www.wow-petguide.com/Encounter/1214/Mighty_Minions_of_Maldraxxus](https://www.wow-petguide.com/Encounter/1214/Mighty_Minions_of_Maldraxxus)

##### Strategy: Default Strategy
```text
change(#2) [round=3]
change(#1) [enemy(#2).dead & enemy(#1).active]

ability(Booby-Trapped Presents:1080) [enemy(#1).hp>0]
standby [enemy(#3).active & enemy.ability(Lift-Off:170).usable]
ability(Greench's Gift:1076)

ability(Ice Tomb:624) [enemy.aura(Resilient:924).duration=1]
ability(Call Blizzard:206)
ability(Ice Tomb:624) [enemy.ability(Burrow:159).usable & enemy(#2).hp>0 & enemy(#1).active]

ability(Gift of Winter's Veil:586)

ability(#1)
change(#1)
```

#### RotgutQuest: Extra Pieces
**URL:** [https://www.wow-petguide.com/Encounter/1215/Extra_Pieces](https://www.wow-petguide.com/Encounter/1215/Extra_Pieces)

##### Strategy: Default Strategy
```text

```

#### Dundley StickyfingersQuest: Uncomfortably Undercover
**URL:** [https://www.wow-petguide.com/Encounter/1216/Uncomfortably_Undercover](https://www.wow-petguide.com/Encounter/1216/Uncomfortably_Undercover)

##### Strategy: Default Strategy
```text
ability(Nether Gate:466) [enemy(#1).active & enemy(#2).dead]
ability(Nether Gate:466) [round=3]
ability(Jar of Smelly Liquid:1556) [!enemy(#3).active]
ability(Kick:307) [self.speed.fast & !enemy.aura(Dodge:2060).exists]
standby [enemy(#3).aura(Undead:242).exists]
ability(Frolick:1047) [enemy.aura(Dodge:2060).exists]
ability(#1)

change(next)
```

#### SyllaQuest: Resilient Survivors
**URL:** [https://www.wow-petguide.com/Encounter/1218/Resilient_Survivors](https://www.wow-petguide.com/Encounter/1218/Resilient_Survivors)

##### Strategy: Default Strategy
```text
use(Bubble:934)
use(Fish Slap:1737)

use(Call Blizzard:206)
use(Gift of Winter's Veil:586) [round>=9]
use(Ice Lance:413)

use(Pounce:535)

change(next)
```

#### EyegorQuest: Eyegor's Special Friends
**URL:** [https://www.wow-petguide.com/Encounter/1219/Eyegor's_Special_Friends](https://www.wow-petguide.com/Encounter/1219/Eyegor's_Special_Friends)

##### Strategy: Default Strategy
```text
ability(Nether Gate:466) [round=2]
ability(Flamethrower:503) [round=1]
ability(Flamethrower:503) [!enemy.aura(Flamethrower:502).exists & self.aura(Toxic Wound:2112).exists]
ability(Booby-Trapped Presents:1080)
ability(Greench's Gift:1076)
ability(Curse of Doom:218) [self.round=1]
ability(Lovestruck:772) [self.round>2]
ability(#1)
change(next)
```

#### Addius the TormentorQuest: The Mind Games of Addius
**URL:** [https://www.wow-petguide.com/Encounter/1220/The_Mind_Games_of_Addius](https://www.wow-petguide.com/Encounter/1220/The_Mind_Games_of_Addius)

##### Strategy: Default Strategy
```text
use(Mind Games: Health:2388)
use(Call Blizzard:206)
use(Ice Tomb:624) [ round<5 ]
use(Greench's Gift:1076)
use(Ice Lance:413)
change(next)
```

#### GlitterdustQuest: Natural Defenders
**URL:** [https://www.wow-petguide.com/Encounter/1222/Natural_Defenders](https://www.wow-petguide.com/Encounter/1222/Natural_Defenders)

##### Strategy: Default Strategy
```text
change(#2) [round=4]
change(#1) [self.dead]
change(#3) [self.dead]
use(Booby-Trapped Presents:1080) [enemy(#2).active & enemy.aura(Stunned:927).exists]
use(Booby-Trapped Presents:1080) [enemy(#3).active & !enemy(#2).dead]
use(Ice Tomb:624)
use(Greench's Gift:1076)
use(Booby-Trapped Presents:1080)
use(Deflection:490) [enemy(#3).active & enemy.ability(Moth Balls:507).usable]
use(Deflection:490) [enemy(#2).active]
use(Soulrush:752)
use(#1)
standby
```

#### FarylQuest: Airborne Defense Force
**URL:** [https://www.wow-petguide.com/Encounter/1223/Airborne_Defense_Force](https://www.wow-petguide.com/Encounter/1223/Airborne_Defense_Force)

##### Strategy: Default Strategy
```text
use(Deflection:490)
use(Sandstorm:453)
use(Creeping Insanity:1760) [enemy(Brite:3005).active]
use(Gift of Winter's Veil:586)
use(#1)
change(next)
```

#### https://www.wow-petguide.com/Strategy/11028/Mega_Bite
**URL:** [https://www.wow-petguide.com/Strategy/11028/Mega_Bite](https://www.wow-petguide.com/Strategy/11028/Mega_Bite)

##### Strategy: Default Strategy
```text
use(Aufladen:208) [ !enemy.ability(Stachelpanzerschale:2324).usable ]
use(Aufziehen:459)
```

### Blackrock Depths

#### Trainer Grrglin
**URL:** [https://www.wow-petguide.com/Encounter/1359/Trainer_Grrglin](https://www.wow-petguide.com/Encounter/1359/Trainer_Grrglin)

##### Strategy: Default Strategy
```text
use(Cocoon Strike:506)
use(Moth Dust:508)
use(Alpha Strike:504)
change(next)
```

#### https://www.wow-petguide.com/Strategy/10529/Trainer_Grrglin
**URL:** [https://www.wow-petguide.com/Strategy/10529/Trainer_Grrglin](https://www.wow-petguide.com/Strategy/10529/Trainer_Grrglin)

##### Strategy: Default Strategy
```text
ability(Savage Talon:1370) [enemy.round>4]
ability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
ability(Puppy Parade:1681) [!enemy.aura(Shattered Defenses:542).exists]
ability(Flock:581)
ability(Superbark:1357) [enemy.hp>661]
ability(#1)
change(next)
```

#### Klick
**URL:** [https://www.wow-petguide.com/Strategy/10529/Lehrer_Grrglin](https://www.wow-petguide.com/Strategy/10529/Lehrer_Grrglin)

##### Strategy: Default Strategy
```text
ability(Savage Talon:1370) [enemy.round>4]
ability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]
ability(Puppy Parade:1681) [!enemy.aura(Shattered Defenses:542).exists]
ability(Flock:581)
ability(Superbark:1357) [enemy.hp>661]
ability(#1)
change(next)
```

### Gnomeregan

#### Prototype Annoy-O-Tron
**URL:** [https://www.wow-petguide.com/Encounter/1032/Prototype_Annoy-O-Tron](https://www.wow-petguide.com/Encounter/1032/Prototype_Annoy-O-Tron)

##### Strategy: Default Strategy
```text
standby [ round<3 ]
use(Blistering Cold:786)
use(Wild Magic:592) [ round=5 ]
use(Ice Tomb:624)
use(Black Claw:919) [ round=8 ]
use(Flock:581)
change(next)
```

#### Living Sludge
**URL:** [https://www.wow-petguide.com/Encounter/1034/Living_Sludge](https://www.wow-petguide.com/Encounter/1034/Living_Sludge)

##### Strategy: Default Strategy
```text
standby [ enemy.aura(Dodge:2060).exists ]
standby [ enemy.aura(Undead:242).exists ]

change(#3) [enemy(Cockroach:2486).active]

ability(Shell Armor:1380) [enemy(#2).active & enemy.round=1 & !enemy(Cockroach:2486).active]
ability(Shell Armor:1380) [enemy(#2).active & enemy.round=3 & enemy(Cockroach:2486).active]

ability(Shell Armor:1380) [enemy(#3).active & enemy.round=1 & !enemy(Cockroach:2486).active]
ability(Shell Armor:1380) [enemy(#3).active & enemy.round=3 & enemy(Cockroach:2486).active]

ability(Dive:564) [round=3]
ability(Dive:564) [self.ability(Shell Armor:1380).duration~1,2,3]

ability(Leech Seed:745)
ability(Fist of the Forest:1343)
ability(Lash:394)

ability(Cauterize:173) [self.hpp<65]
ability(Brittle Webbing:382) [enemy(Cockroach:2486).active]
ability(Burn:113)

ability(#1)
change(#2) [!enemy(Cockroach:2486).active]
change(#3)
```

#### Living Napalm
**URL:** [https://www.wow-petguide.com/Encounter/1035/Living_Napalm](https://www.wow-petguide.com/Encounter/1035/Living_Napalm)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Dodge:2060).exists]
standby [enemy.aura(Undead:242).exists]

change(#3) [enemy(Cockroach:2486).active]

ability(Acidic Goo:369) [!enemy.aura(Acidic Goo:368).exists]
ability(Corrosion:447) [!enemy.aura(Corrosion:446).exists & self(#1).active]
ability(Gnash:2322)

ability(Immolate:178) [!enemy.aura(Immolate:177).exists]
ability(Conflagrate:179) [enemy.aura(Immolate:177).exists]
ability(Burn:113)

ability(Creeping Ooze:448) [!enemy.aura(Creeping Ooze:781).exists]
ability(Corrosion:447) [!enemy.aura(Corrosion:446).exists]
ability(Poison Spit:380)

change(next)
```

#### Living Permafrost
**URL:** [https://www.wow-petguide.com/Encounter/1036/Living_Permafrost](https://www.wow-petguide.com/Encounter/1036/Living_Permafrost)

##### Strategy: Default Strategy
```text
use(Toxic Skin:1087) [round~1]
use(Toxic Skin:1087) [self.aura(Toxic Skin:1086).duration~1]
use(Whirlpool:513)
use(Water Jet:118)
change(#2) [enemy.type=10]
change(#3) [enemy.type=5]
use(Stoneskin:436) [!self.aura(Stoneskin:435).exists]
use(Stoneskin:436) [self.aura(Stoneskin:435).duration=1]
use(Leech Life:383) [enemy.aura(Webbed:338).exists]
use(Sticky Web:339)
use(Brittle Webbing:382) [!enemy.aura(Brittle Webbing:381).exists]
use(Leech Life:383) [enemy.aura(Brittle Webbing:381).exists]
use(Poison Spit:380)
change(#2)
change(#3)
```

#### Door Control Console
**URL:** [https://www.wow-petguide.com/Encounter/1038/Door_Control_Console](https://www.wow-petguide.com/Encounter/1038/Door_Control_Console)

##### Strategy: Default Strategy
```text
ability(Acidic Goo:369) [ enemy.hp.full ]
use(Dive:564) [round=2] 
use(Dive:564) [self.aura(Ice Tomb:623).duration=1] 
use(Dive:564) [self.aura(Sewage Eruption:2063).duration=1] 
use(Ooze Touch:445) 
change(next)
```

#### Cockroach
**URL:** [https://www.wow-petguide.com/Encounter/1040/Cockroach](https://www.wow-petguide.com/Encounter/1040/Cockroach)

##### Strategy: Default Strategy
```text
standby [enemy.aura(Dodge:2060).exists]
standby [enemy.aura(Undead:242).exists] 
ability(Rampage:124)
ability(Leap:364) [enemy(Cockroach:2486).active]
ability(Claw:429) [self.ability(Claw:429).strong]
ability(Ice Tomb:624) 
ability(Frost Nova:414) [self.ability(Frost Nova:414).strong]
ability(Unstable Shield:1598)
ability(Burrow:159) [self.round>3]
ability(#1)
change(next)
```

#### Leper Rat
**URL:** [https://www.wow-petguide.com/Encounter/1041/Leper_Rat](https://www.wow-petguide.com/Encounter/1041/Leper_Rat)

##### Strategy: Default Strategy
```text
ability(#3) [!enemy.aura(502).exists]
standby [enemy.aura(2060).exists] 
standby [enemy.aura(242).exists]
ability(2067) [enemy.aura(542).exists]
ability(2067) [enemy(2486).active]
ability(163)
ability(179) [enemy.aura(502).exists]
ability(503) [self.ability(503).strong]
ability(#1) 
change(next)
```

#### Bloated Leper Rat
**URL:** [https://www.wow-petguide.com/Encounter/1043/Bloated_Leper_Rat](https://www.wow-petguide.com/Encounter/1043/Bloated_Leper_Rat)

##### Strategy: Default Strategy
```text
ability(Toxic Skin:1087) [!self.aura(Toxic Skin:1086).exists & self.hp>313]
ability(Whirlpool:513) [!enemy.aura(Whirlpool:512).exists]
ability(#1)

change(next)
```

#### Gnomeregan Guard Mechanostrider
**URL:** [https://www.wow-petguide.com/Encounter/1045/Gnomeregan_Guard_Mechanostrider](https://www.wow-petguide.com/Encounter/1045/Gnomeregan_Guard_Mechanostrider)

##### Strategy: Default Strategy
```text
change(next) [ self.dead ]
ability(Photosynthese:268) [ !self.aura(Photosynthese:267).exists ]
ability(Sonnenlicht:404) [ !weather(Sonnenschein:403) ]
ability(Panzerschild:310) [ !self.aura(Panzerschild:309).exists ]
standby [ enemy.aura(Untot:242).exists ]
ability(#1)
```

#### Gnomeregan Guard Tiger
**URL:** [https://www.wow-petguide.com/Encounter/1046/Gnomeregan_Guard_Tiger](https://www.wow-petguide.com/Encounter/1046/Gnomeregan_Guard_Tiger)

##### Strategy: Default Strategy
```text
if [self(Tiny Snowman:117).active]
use(Call Blizzard:206)
use(Howling Blast:120)
use(Snowball:477)
change(next)
endif

if [self(#2).active]
use(#1)
change(next)
endif

if [self(#3).active]
use(#1)
endif
```

#### Gnomeregan Guard Wolf
**URL:** [https://www.wow-petguide.com/Encounter/1047/Gnomeregan_Guard_Wolf](https://www.wow-petguide.com/Encounter/1047/Gnomeregan_Guard_Wolf)

##### Strategy: Default Strategy
```text
ability(508)
ability(506)
ability(504)
change(next)
```

#### Pulverizer Bot Mk 6001
**URL:** [https://www.wow-petguide.com/Encounter/1049/Pulverizer_Bot_Mk_6001](https://www.wow-petguide.com/Encounter/1049/Pulverizer_Bot_Mk_6001)

##### Strategy: Default Strategy
```text
use(Howl:362)
use(Lightning Shield:906)
standby
```

## Misc

### Darkmoon Faire

#### Next Squirt Day:
**URL:** [https://www.wow-petguide.com/Encounter/1](https://www.wow-petguide.com/Encounter/1)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### Chopped
**URL:** [https://www.wow-petguide.com/Strategy/17886](https://www.wow-petguide.com/Strategy/17886)

##### Strategy: Default Strategy
```text
change(#3) [self(#2).active]
if [self(#1).active]
change(#2) [enemy(#3).active]
standby [enemy(#2).active & enemy.hp<421 & round=5]
endif
use(Terrifying Toxicity:2456) [enemy(#1).active]
use(Crouch:165) [round=2]
use(Flock:581) [!enemy.aura(Shattered Defenses:542).exists & enemy(#3).active]
use(#1)
```

#### Fight Night: Sir Galveston
**URL:** [https://www.wow-petguide.com/Strategy/5204](https://www.wow-petguide.com/Strategy/5204)

##### Strategy: Default Strategy
```text
standby [ enemy.ability(Lift-Off:170).usable ]
ability(#3) [ enemy(#2).dead ]
ability(Stone Rush:621)
ability(#1)
change(#2)
```

#### https://classic.wow-petguide.com/Encounter/2000031/]Nicki
**URL:** [https://classic.wow-petguide.com/Encounter/2000031/]Nicki](https://classic.wow-petguide.com/Encounter/2000031/]Nicki)

##### Strategy: Default Strategy
```text
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).played ]
change(#2) [ self(#1).dead ]
change(#1)
use(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]
use(Ancient Blessing:611) [ self.hpp < 50 ]
use(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]
use(#1)
standby
```

#### Nicki Tinytech
**URL:** [https://www.wow-petguide.com/Strategy/25093](https://www.wow-petguide.com/Strategy/25093)

##### Strategy: Default Strategy
```text
change(#3) [round=5]
change(next) [self.level<25]
change(next) [self.dead]
use(Geysir:418)
use(Frostschock:416) [!enemy.aura(Frostschock:415).exists]
use(#1)
```

#### Burning Pandaren Spirit
**URL:** [https://www.wow-petguide.com/Strategy/25085](https://www.wow-petguide.com/Strategy/25085)

##### Strategy: Default Strategy
```text
quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]
change(#2) [ !self(#2).played & self(#1).dead ]
change(#3) [ self(#2).played & self(#1).dead ]
ability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]
ability(Dead Man's Party:1093)
ability(Surge:509) [ enemy(#2).active ]
ability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]
ability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]
ability(Surge:509)
```

#### Nitun
**URL:** [https://www.wow-petguide.com/Strategy/25084](https://www.wow-petguide.com/Strategy/25084)

##### Strategy: Default Strategy
```text
ability(Curse of Doom:218)
ability(Haunt:652)
change(#2)
ability(Death and Decay:214) [self.round = 1]
ability(Dead Man's Party:1093)
ability(#1)
```

#### The Terrible Three (Humanoid)
**URL:** [https://www.wow-petguide.com/Strategy/25080](https://www.wow-petguide.com/Strategy/25080)

##### Strategy: Default Strategy
```text
use(Lovestruck:772) [round=4]
use(Rapid Fire:774)
use(Backflip:669) [self.speed.fast]
use(Crush:406)
change(next)
```

#### Gloamwing
**URL:** [https://www.wow-petguide.com/Strategy/25077](https://www.wow-petguide.com/Strategy/25077)

##### Strategy: Default Strategy
```text
use(Blistering Cold:786)
change(Boneshard:1963)
use(Blistering Cold:786)
use(Chop:943)
use(Razor Talons:2237)
use(Omni Pummel:2241)
use(Shock and Awe:646)
change(PHA7-YNX:2889)
use(#1)
standby
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25076](https://www.wow-petguide.com/Strategy/25076)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Call Lightning:204)
use(Thunderbolt:779)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25067](https://www.wow-petguide.com/Strategy/25067)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Bird
**URL:** [https://www.wow-petguide.com/Strategy/25066](https://www.wow-petguide.com/Strategy/25066)

##### Strategy: Default Strategy
```text
use(Armageddon:1025) [self.round=2]
use(Blinding Powder:1015)
use(Explode:282)
if [!enemy(#1).active]
use(Call Darkness:256)
use(Nocturnal Strike:517)
endif
use(#1)
change(next)
```

#### Klutz's Battle Monkey
**URL:** [https://www.wow-petguide.com/Strategy/25065](https://www.wow-petguide.com/Strategy/25065)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25064](https://www.wow-petguide.com/Strategy/25064)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=2]
use(Rip:803) [round=3]
use(Armageddon:1025)
use(Call Darkness:256)
use(Nocturnal Strike:517)
change(next)
```

#### Klutz's Battle Rat
**URL:** [https://www.wow-petguide.com/Strategy/25063](https://www.wow-petguide.com/Strategy/25063)

##### Strategy: Default Strategy
```text
use(Razor Talons:2237) [round=1]
use(Flame Breath:501) [round=3]
use(Armageddon:1025)
use(Dive Bomb:2463)
change(next)
```

#### Foe Reaper 50
**URL:** [https://www.wow-petguide.com/Strategy/25061](https://www.wow-petguide.com/Strategy/25061)

##### Strategy: Default Strategy
```text
use(Explode:282)
use(Ice Age:2512)
use(Frost Nova:414)
change(next)
```

#### Angry Geode
**URL:** [https://www.wow-petguide.com/Strategy/25060](https://www.wow-petguide.com/Strategy/25060)

##### Strategy: Default Strategy
```text
use(Conflagrate:179)
use(Razor Talons:2237) [self.round=1]
if [self.round=2 & self(#2).active]
use(Rip:803)
use(Flame Breath:501)
endif
use(Armageddon:1025)
use(Twilight Fire:1890)
use(Twilight Meteorite:1960)
change(next)
```

#### Unfortunate Defias
**URL:** [https://www.wow-petguide.com/Strategy/25059](https://www.wow-petguide.com/Strategy/25059)

##### Strategy: Default Strategy
```text
use(Rip:803) [round=2]
use(Razor Talons:2237) [round=1]
use(Armageddon:1025)
use(Twilight Meteorite:1960) [self.aura(Dragonkin:245).exists]
use(Twilight Meteorite:1960) [enemy(#2).dead & enemy(#3).hp<330]
use(Twilight Meteorite:1960) [enemy(#3).dead & enemy(#2).hp<330]
use(Twilight Meteorite:1960) [enemy(#2).hp<254 & enemy(#3).hp<254]
use(Twilight Fire:1890)
change(next)
```

#### Fight Night: Tiffany Nelson (Dragonkin)
**URL:** [https://www.wow-petguide.com/Strategy/25032](https://www.wow-petguide.com/Strategy/25032)

##### Strategy: Default Strategy
```text
use(Time Bomb:602)
use(Armageddon:1025)
use(Call Lightning:204)
use(Arcane Storm:589)
use(#1)
change(next)
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/9236/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
if [ enemy(#1).active ]
ability(#1) [enemy.hp<=254]
ability(#2) 
ability(#1)
endif

if [ enemy(#2).active ]
ability(593)
ability(#2)
change(next)
endif

if [ enemy(#3).active ]
change(#3) [ !self(#3).played ]
change(#2) [ !self(#2).active ]
ability(#3)
ability(#2)
ability(#1)
endif
```

#### here
**URL:** [https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle](https://www.wow-petguide.com/Strategy/14013/Deebs,_Tyri_and_Puzzle)

##### Strategy: Default Strategy
```text
change(#3) [!self(#3).played & enemy(#3).active]
change(#2) [self(#3).played]
use(Void Nova:2356)
use(Corrosion:447) [round=2]
use(Poison Protocol:1954)
use(Corrosion:447)
use(Breath of Sorrow:1055) [enemy(#2).active]
use(Surge of Power:593) [self.aura(Greedy:1122).exists & enemy.hp>650]
use(Seethe:1056)
change(#2)
```

#### https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast
**URL:** [https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast](https://www.wow-petguide.com/Strategy/16923/Swog_the_Elder-Beast)

##### Strategy: Default Strategy
```text
change(#3) [round=7]
change(#2) [round~3]
change(#1) [round~5,9]
use(Dazzling Dance:366) [round~1,10]
use(Vengeance:997)
use(Howl:362)
change(next)
```

