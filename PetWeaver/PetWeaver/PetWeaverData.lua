PetWeaverDB = {
    ["Robot Rumble"] = {
        pet1 = 115146,
        pet2 = 86447,
        pet3 = 143564,
        script = "use(Blistering Cold:786)\nuse(Chop:943) [!enemy.aura(Bleeding:491).exists]\nuse(BONESTORM!!:1762)\nuse(Chop:943)\nuse(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nuse(Flock:581)\nstandby\nchange(next)"
    },
    ["Major Malfunction"] = {
        pet1 = 55367,
        pet2 = 64899,
        pet3 = 86716,
        script = "use(Thunderbolt:779) [round=1]\nuse(Explode:282)\nuse(Call Blizzard:206)\nuse(#1)\nchange(next)"
    },
    ["The Thing from the Swamp"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 64899,
        script = "ability(Curse of Doom:218)\nability(Unholy Ascension:321)\nability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nability(Flock:581)\nability(Thunderbolt:779)\nability(Breath:115)\nchange(next)"
    },
    ["One Hungry Worm"] = {
        pet1 = 86718,
        pet2 = 86716,
        pet3 = 87705,
        script = "standby [enemy.aura(Underground:340).exists & self.speed.fast]\nuse(Glowing Toxin:270) [!enemy.aura(Glowing Toxin:271).exists]\nuse(Explode:282)\nuse(Call Lightning:204)\nchange(next)"
    },
    ["Are They Not Beautiful?"] = {
        pet1 = 86061,
        pet2 = 86067,
        pet3 = 68662,
        script = "change(#3) [enemy(#3).active & !self.aura(242).exists]\nuse(Prowl:536) [!enemy(#2).dead]\nuse(Call Darkness:256)\nuse(Spectral Strike:442)\nuse(Arcane Dash:1536)\nif [enemy(#3).active]\nuse(Howl:362)\nuse(Shadowmeld:2253)\nuse(Surge of Power:593) [!weather(Darkness:257) & self(Salverun:3545).active]\nuse(Surge of Power:593) [self(Chrominius:1152).active]\nendif\nuse(#1) [round>3]\nchange(next)"
    },
    ["Delver Mardei"] = {
        pet1 = 179125,
        pet2 = 97207,
        pet3 = 68662,
        script = "use(Time Bomb:602)\nuse(Armageddon:1025) [ enemy.aura(Flame Breath:500).exists ]\nuse(Flame Breath:501)\nuse(Ice Tomb:624) [ !enemy.is(Dustie:3568) ]\nuse(Arcane Storm:589)\nuse(Breath:115)\nif [ enemy.is(Dustie:3568) ]\n    use(Howl:362) [ enemy.hp>1665 & self.aura(Dragonkin:245).exists ]\n    use(Howl:362) [ enemy.hp>1110 & !self.aura(Dragonkin:245).exists ]\n    use(Surge of Power:593)\nendif\nuse(Bite:110)\nchange(next)"
    },
    ["Swog the Elder"] = {
        pet1 = 205637,
        pet2 = 0,
        pet3 = 0,
        script = "use(2223)\nuse(377)"
    },
    ["Sharp as Flint"] = {
        pet1 = 143811,
        pet2 = 66950,
        pet3 = 62820,
        script = "change(#2) [round=2]\nuse(Razor Talons:2237) [round~4,6]\nuse(Armageddon:1025) [round>6]\nuse(Geyser:418)\nif [enemy(#3).active]\nuse(Call Darkness:256) [enemy(#3).hp<=1811 & !enemy.ability(Digest Brains:1065).usable]\nuse(Call Darkness:256) [enemy(#3).hp<=1492]\nendif\nuse(Nocturnal Strike:517) [weather(Darkness:257).duration!=0]\nuse(#1)\nchange(next)"
    },
    ["Adinakon"] = {
        pet1 = 55367,
        pet2 = 77221,
        pet3 = 9656,
        script = "ability(Explode:282)\nability(Call Darkness:256)\nchange(next)"
    },
    ["Two and Two Together"] = {
        pet1 = 179125,
        pet2 = 77221,
        pet3 = 0,
        script = "use(Time Bomb:602)\nuse(Armageddon:1025)\nuse(Explode:282) [enemy.hp.can_explode]\nuse(Powerball:566) [round=3]\nuse(Wind-Up:459)\nchange(next)"
    },
    ["Paws of Thunder"] = {
        pet1 = 161964,
        pet2 = 179125,
        pet3 = 171230,
        script = "use(Toxic Fumes:2349)\nuse(Poison Protocol:1954)\nuse(Time Bomb:602)\nuse(Armageddon:1025)\n\nstandby [enemy(#2).active & enemy.hp<733 & enemy.aura(601).duration=1]\nif [enemy(#2).aura(927).exists]\nuse(Puncture Wound:1050)\nstandby [enemy(#2).active]\nendif\n\nuse(Impale:800)\nuse(Slicing Wind:420)\nchange(next)"
    },
    ["Lyver"] = {
        pet1 = 86716,
        pet2 = 70451,
        pet3 = 69796,
        script = "use(Explode:282)\nuse(Black Claw:919) [ !enemy.aura(Black Claw:918).exists ]\nuse(Hunting Party:921)\nchange(next)"
    },
    ["The Grand Master"] = {
        pet1 = 15698,
        pet2 = 15705,
        pet3 = 161964,
        script = "change(#2) [round=6]\nuse(Ice Tomb:624) [enemy(#1).active]\nuse(Call Blizzard:206) [round=2]\nuse(Ice Lance:413)\nuse(Poison Protocol:1954)\nuse(Void Nova:2356)\nuse(Corrosion:447)\nchange(#3)"
    },
    ["Enok the Stinky"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 143564,
        script = "ability(Curse of Doom:218)\nability(Haunt:652) [round=3]\nability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nability(Flock:581)\nability(Hunting Party:921)\nability(Leap:364)\nability(#1)\nchange(next)"
    },
    ["They're Full of Stars!"] = {
        pet1 = 86061,
        pet2 = 127953,
        pet3 = 0,
        script = "use(Explode:282) [enemy.hp.can_explode]\nuse(Prowl:536) [!self.aura(Undead:242).exists]\nuse(Call Darkness:256)\nuse(#1)\nchange(next)"
    },
    ["Storm-Touched Swoglet"] = {
        pet1 = 86719,
        pet2 = 86716,
        pet3 = 64899,
        script = "ability(Explode:282) [round~1,3]\nability(Flyby:515)\nability(Call Darkness:256)\nability(Nocturnal Strike:517)\nchange(next)"
    },
    ["Vortex - Legendary"] = {
        pet1 = 115146,
        pet2 = 86447,
        pet3 = 70451,
        script = "use(Blistering Cold:786) \nuse(Chop:943) [round=2] \nuse(BONESTORM!!:1762) \nchange(Ikky:1532) [self(Boneshard:1963).dead] \nuse(Flock:581) [enemy.aura(Black Claw:918).exists] \nuse(Black Claw:919)"
    },
    ["Vortex - Rare"] = {
        pet1 = 71163,
        pet2 = 69796,
        pet3 = 70451,
        script = "use(haunt:652)\nuse(claw:919) [ !enemy.aura(claw:918).exists ]\nuse(finisher:921)\nchange(next)"
    },
    ["Storm-Touched Skitterer"] = {
        pet1 = 86447,
        pet2 = 0,
        pet3 = 0,
        script = "use(claw:919) [ !enemy.aura(claw:918).exists ]\nuse(flock:581) [ !enemy.aura(flock:542).exists ]\nuse(filler:184)"
    },
    ["Wildfire - Epic"] = {
        pet1 = 115146,
        pet2 = 70451,
        pet3 = 62178,
        script = "ability(Blistering Cold:786)\nability(Chop:943) [!enemy.aura(Bleeding:491).exists]\nability(BONESTORM!!:1762) [!self.aura(Undead:242).exists]\nability(Chop:943)\n\nability(Primal Cry:920)\nability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nability(Hunting Party:921)\n\nability(Stampede:163)\nability(Scratch:119)\n\nchange(next)"
    },
    ["Wildfire - Rare"] = {
        pet1 = 86447,
        pet2 = 143564,
        pet3 = 0,
        script = "ability(Black Claw:919) [round=1]\nability(Flock:581)\nability(#1)\nchange(next)"
    },
    ["Storm-Touched Ohuna"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 143564,
        script = "standby [ round = 1 ]\nuse(curse:218)\nuse(haunt:652)\nuse(claw:919) [ !enemy.aura(claw:918).exists ]\nuse(flock:581)\nchange(next)"
    },
    ["Flow - Legendary"] = {
        pet1 = 179125,
        pet2 = 61828,
        pet3 = 26056,
        script = "ability(Time Bomb:602)\nability(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]\nability(Armageddon:1025)\n\nability(Rabid Strike:666) [!enemy.aura(Rabies:807).exists]\nability(Corpse Explosion:663)\n\nability(Rip:803) [!enemy.aura(Bleeding:491).exists]\nability(Blood in the Water:423)\nability(Surge:509)\n\nchange(next)"
    },
    ["Flow - Epic"] = {
        pet1 = 179125,
        pet2 = 61828,
        pet3 = 26056,
        script = "ability(Time Bomb:602)\nability(Armageddon:1025)\n\nability(Rabid Strike:666) [!enemy.aura(Rabies:807).exists]\nability(Corpse Explosion:663)\n\nability(Rip:803) [!enemy.aura(Bleeding:491).exists]\nability(Blood in the Water:423)\nability(Surge:509)\n\nchange(next)"
    },
    ["Flow - Rare"] = {
        pet1 = 86447,
        pet2 = 143564,
        pet3 = 86716,
        script = "ability(Black Claw:919) [round=1]\nability(Flock:581)\nability(Explode:282)\nability(#1)\nchange(next)"
    },
    ["Mechanical Battler of Zaralek Cavern"] = {
        pet1 = 115140,
        pet2 = 9656,
        pet3 = 15699,
        script = "change(#2) [enemy(#2).active]\n\nability(Minefield:634)\nability(Explode:282) [enemy.aura(Minefield:635).duration=7]\nability(Zap:116)\n\nability(Jolt:908) [enemy(#2).active]\nability(Supercharge:208)\nability(Call Lightning:204)\nability(#1)\n\nstandby\nchange(#1)"
    },
    ["ShinmuraQuest: Are They Not Beautiful?"] = {
        pet1 = 97229,
        pet2 = 15705,
        pet3 = 15698,
        script = "ability(Eggnog:835) [enemy(#3).active & enemy.ability(Conflagrate:179).duration=4]\nability(Gift of Winter's Veil:586)\nability(Frost Shock:416) [!enemy.aura(Frost Shock:415).exists & enemy(#1).active]\nability(Call Blizzard:206) [!weather(Blizzard:205)]\nability(#1)\nchange(next)"
    },
    ["Illidari Masters: Sissix"] = {
        pet1 = 162518,
        pet2 = 53884,
        pet3 = 0,
        script = "use(Cleansing Rain:230) [round=2]\nuse(Water Jet:118) [self.aura(Pumped Up:296).exists & enemy.hpp=100]\nuse(Pump:297)\nuse(#1) [enemy(#2).active]\n\nif [enemy(#3).active]\nuse(Prowl:536)\nuse(Call Darkness:256)\nstandby [self(#3).hp<712 & self(#3).type=1]\nstandby [self(#3).hp<316 & self(#3).type=9]\nstandby [self(#3).hp<475 & self(#3).type!=6]\nstandby [self(#1).active]\nendif\n\nchange(next)"
    },
    ["Illidari Masters: Madam Viciosa"] = {
        pet1 = 64899,
        pet2 = 64352,
        pet3 = 63001,
        script = "standby [round=1]\nchange(#3) [enemy(#3).active & enemy.round=2]\nchange(#1) [!enemy(#1).active]\nuse(Acidic Goo:369) [self.round=1]\nuse(Dive:564) [enemy.round>5]\nuse(Absorb:449)\nuse(Decoy:334)\nuse(Thunderbolt:779) [enemy(#3).active]\nuse(Breath:115)\nchange(#2)"
    },
    ["Illidari Masters: Nameless Mystic"] = {
        pet1 = 64899,
        pet2 = 55367,
        pet3 = 0,
        script = "ability(Decoy:334) [self(#1).active]\nability(Thunderbolt:779) [!enemy(#1).active]\nability(Breath:115)\nability(Explode:282) [enemy.hp<618]\nability(Missile:777)\nchange(#2)"
    },
    ["Fight Night: AmaliaFamily Familiar"] = {
        pet1 = 148995,
        pet2 = 154798,
        pet3 = 0,
        script = "change(#1) [self(#3).played]\nstandby [enemy.aura(Puppies of the Flame:1355).exists]\nchange(#2) [round=5]\nuse(Thunderbolt:779) [!enemy(#1).active]\nuse(Call Lightning:204)\nuse(Zap:116)\nuse(Explode:282) [enemy(#3).active]\nuse(Alert!:1585)\nchange(#3)"
    },
    ["Fight Night: Heliosus"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 143564,
        script = "ability(218)\nability(652)\nchange(#2) \nability(919) [self.round=1]\nability(581)"
    },
    ["Fight Night: Rats!"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 143564,
        script = "ability(218)\nability(652)\nchange(#2) [self(#1).dead]\nability(919) [!enemy.aura(918).exists]\nability(581)"
    },
    ["Fight Night: Stitches Jr. Jr."] = {
        pet1 = 55356,
        pet2 = 68662,
        pet3 = 0,
        script = "ability(301)\nchange(#2)\nability(362)\nability(593)"
    },
    ["Fight Night: Tiffany NelsonFamily Familiar"] = {
        pet1 = 73741,
        pet2 = 71942,
        pet3 = 0,
        script = "change(#1) [self(#3).played]\nchange(#2) [round=2]\nuse(Prowl:536) [round=3]\nuse(Moonfire:595) [round=4]\nuse(Greench's Gift:1076) [enemy(#3).active]\nuse(Ice Tomb:624) [enemy(#1).active]\nuse(Spirit Claws:974)\nchange(#3)"
    },
    ["Meet The Maw"] = {
        pet1 = 179125,
        pet2 = 86716,
        pet3 = 0,
        script = "ability(Razor Talons:2237) [!enemy.aura(Razor Talons:2238).exists]\nability(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]\nability(Armageddon:1025)\n\nability(Explode:282)\n\nchange(next)"
    },
    ["Stand Up to Bullies"] = {
        pet1 = 48609,
        pet2 = 86447,
        pet3 = 0,
        script = "change(#1) [self(#2).dead]\nuse(#1) [round=1]\nuse(#3) [round=2]\nchange(#2) [round=3]\nuse(Black Claw:919) [!enemy.aura(Black Claw).exists]\nuse(Flock:581)\nuse(Build Turret:710) [enemy.aura(Black Claw).exists]\nuse(Metal Fist:384)"
    },
    ["Dealing with SatyrsFamily Familiar"] = {
        pet1 = 64899,
        pet2 = 45340,
        pet3 = 0,
        script = "ability(Explode:282) [enemy.hp<561 & enemy(#3).active]\nability(Thunderbolt:779) [!enemy(#2).active]\nability(BONESTORM:649)\nability(Ancient Blessing:611) [!self.aura(Undead:242).exists & self.hpp<100]\nability(#1)\nchange(#1)"
    },
    ["Training with BreddaFamily Familiar"] = {
        pet1 = 62178,
        pet2 = 7560,
        pet3 = 63557,
        script = "change(#3) [self(#2).played]\nuse(Supercharge:208) [enemy(#3).active]\nuse(Ion Cannon:209) [enemy(#3).active]\nuse(Alert!:1585) [enemy(#2).active]\nuse(Dodge:312)\nuse(Stampede:163) [enemy(#2).active]\nuse(Flurry:360) [enemy.aura(Shattered Defenses:542).exists]\nuse(Stampede:163)\nchange(next)"
    },
    ["Tiny Poacher, Tiny AnimalsFamily Familiar"] = {
        pet1 = 15698,
        pet2 = 15705,
        pet3 = 64899,
        script = "-- rng in the beginning (<0.5%)\nquit [enemy(#1).dead & round=4]\n--\n-- rare case: too many critical strikes Ice lance Turn4+ 5\nuse(Explode:282) [enemy(#1).dead & enemy(#2).dead]\n--\nuse(Explode:282) [enemy(#1).dead & enemy(#3).dead & enemy(#2).hp<561]\nuse(Ice Tomb:624)\nuse(Call Blizzard:206)\nuse(Ice Lance:413)\nuse(Thunderbolt:779) [enemy(#3).active & enemy.aura(Stunned:927).exists]\nuse(Breath:115)\nchange(next)"
    },
    ["Snail Fight!Family Familiar"] = {
        pet1 = 71942,
        pet2 = 0,
        pet3 = 0,
        script = "quit [self(#2).dead]\nstandby [round=1]\nchange(#2) [!self(#2).active]\nchange(#3) [enemy(#1).dead & !self(#3).played]\n\nif [enemy(#3).active]\nuse(Feed:1016) [self.aura(Prowl:543).exists]\nstandby [enemy.aura(Underwater:830).exists]\nuse(Prowl:536) [self.hp>723 & self.ability(Feed:1016).duration<2]\nuse(Feed:1016)\nuse(Bite:110)\nendif\n\nuse(Prowl:536)\nuse(Feed:1016) [self.aura(Prowl:543).duration=1]\nuse(Bite:110) [!self.aura(Prowl:543).exists & enemy.hpp<100 & !enemy(#2).active]\nuse(Bite:110) [enemy.ability(Headbutt:376).usable]\nstandby"
    },
    ["Jarrun's LadderFamily Familiar"] = {
        pet1 = 161964,
        pet2 = 127951,
        pet3 = 0,
        script = "if [self(#1).active]\nchange(#2) [round=3]\nchange(#2) [self(#1).dead]\nuse(Poison Protocol:1954)\nuse(Void Nova:2356) [enemy(#2).hp>95]\nstandby [enemy.aura(Undead:242).exists]\nuse(Ooze Touch:445)\nendif\n\nif [self(#2).active]\nstandby [enemy.aura(Undead:242).exists]\nchange(#3) [round=8]\nuse(Great Sting:1966) [round>4]\nuse(Cleave:1273)\nendif\n\nif [self(#3).active]\nchange(#1)\nendif"
    },
    ["My Beast's BiddingFamily Familiar"] = {
        pet1 = 97205,
        pet2 = 68845,
        pet3 = 77221,
        script = "change(#3) [self(#2).active]\nuse(Arcane Storm:589)\nuse(Mana Surge:489)\nuse(Toxic Smoke:640) [enemy.hp<=390]\nuse(Wind-Up:459)\nchange(next)"
    },
    ["All Pets Go to Heaven"] = {
        pet1 = 83642,
        pet2 = 69819,
        pet3 = 113136,
        script = "use(bubble:934) [ enemy.ability(bigdot:218).usable ]\nuse(frogdot:232) [ !enemy.aura(frogdot:231).exists ]\nuse(frogdot:232) [ enemy.aura(undead:242).exists ]\nuse(snaildot:369) [ !enemy.aura(snaildot:368).exists ]\nuse(filler:228)\nuse(filler:449)\nchange(#2) [ !self(#2).played & !self(#2).level.max ]\nchange(#3)"
    },
    ["Beasts of Burden:"] = {
        pet1 = 77221,
        pet2 = 0,
        pet3 = 0,
        script = "use(Explode:282) [enemy.hp<=620]\nuse(Toxic Smoke:640) [enemy.aura(Toxic Smoke:639).duration!=2]\nuse(Wind-Up:459)"
    },
    ["Andurs"] = {
        pet1 = 77221,
        pet2 = 0,
        pet3 = 0,
        script = "use(Explode:282) [enemy.hp<=620]\nuse(Toxic Smoke:640) [enemy.aura(Toxic Smoke:639).duration!=2]\nuse(Wind-Up:459)"
    },
    ["FlummoxedFamily Familiar"] = {
        pet1 = 86718,
        pet2 = 222590,
        pet3 = 86716,
        script = "use(Blinding Powder:1015)\nuse(Glowing Toxin:270) [!enemy.aura(Glowing Toxin:271).exists]\nuse(Creeping Fungus:743) [!enemy.aura(Creeping Fungus:742).exists]\nuse(Explode:282) [self(#2).active]\nuse(Explode:282) [self(#2).dead]\nchange(#2)\nchange(#1)"
    },
    ["Threads of Fate"] = {
        pet1 = 64899,
        pet2 = 55367,
        pet3 = 0,
        script = "ability(#1) [ enemy.round~1,2 ] \nability(#2) [ enemy(#3).hp<556 ] \nability(#3) [ enemy(#3).active & enemy.hp>555 ] \nability(#1) \nchange(#2)"
    },
    ["Mana Tap"] = {
        pet1 = 179125,
        pet2 = 64899,
        pet3 = 0,
        script = "standby [enemy.aura(Dodge:311).exists]\nability(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]\nability(Razor Talons:2237) [!enemy.aura(Razor Talons:2238).exists]\nability(Flame Breath:501) [enemy.aura(Prismatic Barrier:443).exists]\nability(Armageddon:1025) [enemy(#2).active]\nability(Explode:282) [enemy(#3).active & enemy.hp<470]\nability(Thunderbolt:779)\nability(#1)\nchange(next)"
    },
    ["Fight Night: Sir Galveston"] = {
        pet1 = 112728,
        pet2 = 127950,
        pet3 = 0,
        script = "standby [ enemy.ability(Lift-Off:170).usable ]\nability(#3) [ enemy(#2).dead ]\nability(Stone Rush:621)\nability(#1)\nchange(#2)"
    },
    ["https://classic.wow-petguide.com/Encounter/2000031/]Nicki"] = {
        pet1 = 40624,
        pet2 = 0,
        pet3 = 0,
        script = "change(#3) [ !self(#3).played ]\nchange(#2) [ !self(#2).played ]\nchange(#2) [ self(#1).dead ]\nchange(#1)\nuse(Ancient Blessing:611) [ self.hpp < 70 & !self.aura(Dragonkin:245).exists ]\nuse(Ancient Blessing:611) [ self.hpp < 50 ]\nuse(Moonfire:595) [ weather(Moonlight:596).duration <= 1 ]\nuse(#1)\nstandby"
    },
    ["Nicki Tinytech"] = {
        pet1 = 62820,
        pet2 = 15698,
        pet3 = 73741,
        script = "change(#3) [round=5]\nchange(next) [self.level<25]\nchange(next) [self.dead]\nuse(Geysir:418)\nuse(Frostschock:416) [!enemy.aura(Frostschock:415).exists]\nuse(#1)"
    },
    ["Burning Pandaren Spirit"] = {
        pet1 = 34770,
        pet2 = 65203,
        pet3 = 61312,
        script = "quit [ self(#1).aura(Undead:242).exists & !enemy(#1).dead ]\nchange(#2) [ !self(#2).played & self(#1).dead ]\nchange(#3) [ self(#2).played & self(#1).dead ]\nability(Macabre Maraca:1094) [ enemy.aura(Shattered Defenses:542).exists ]\nability(Dead Man's Party:1093)\nability(Surge:509) [ enemy(#2).active ]\nability(Shell Shield:310) [ self.aura(Shell Shield:309).duration<=1 ]\nability(Renewing Mists:511) [ self.aura(Renewing Mists:510).duration<=1 ]\nability(Surge:509)"
    },
    ["Nitun"] = {
        pet1 = 71163,
        pet2 = 34770,
        pet3 = 0,
        script = "ability(Curse of Doom:218)\nability(Haunt:652)\nchange(#2)\nability(Death and Decay:214) [self.round = 1]\nability(Dead Man's Party:1093)\nability(#1)"
    },
    ["The Terrible Three (Humanoid)"] = {
        pet1 = 16085,
        pet2 = 63621,
        pet3 = 64632,
        script = "use(Lovestruck:772) [round=4]\nuse(Rapid Fire:774)\nuse(Backflip:669) [self.speed.fast]\nuse(Crush:406)\nchange(next)"
    },
    ["Foe Reaper 50"] = {
        pet1 = 86716,
        pet2 = 77221,
        pet3 = 55367,
        script = "use(Explode:282)\nuse(Ice Age:2512)\nuse(Frost Nova:414)\nchange(next)"
    },
    ["Crystalsnap"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 143564,
        script = "ability(Curse of Doom:218)\nability(Haunt:652)\nability(Flock:581) [enemy.aura(Black Claw:918).exists]\nability(Black Claw:919)\nchange(Ikky:1532)"
    },
    ["Kostos"] = {
        pet1 = 115146,
        pet2 = 86447,
        pet3 = 0,
        script = "use(Blistering Cold:786)\nuse(BONESTORM!!:1762)\nuse(Chop:943)\nuse(Black Claw:919) [ self.round=1 ]\nuse(Flock:581)\nchange(next)"
    },
    ["Sewer Creeper"] = {
        pet1 = 115146,
        pet2 = 69796,
        pet3 = 70451,
        script = "ability(Black Claw:919) [!enemy(#1).aura(Black Claw:918).exists]\nability(BONESTORM!!:1762) [round=3]\nability(Blistering Cold:786)\nability(Chop:943)\nstandby [self(#2).active]\nstandby [self(#3).active]\nchange(next)"
    },
    ["The Countess"] = {
        pet1 = 115146,
        pet2 = 86447,
        pet3 = 0,
        script = "use(Blistering Cold:786) [enemy(The Countess:3074).hp.full]\nuse(Chop:943) [enemy(The Countess:3074).aura(Blistering Cold:785).duration>2]\nchange(Ikky:1532)\nuse(Black Claw:919) [!enemy(The Countess:3074).aura(Black Claw:918).exists]\nuse(Flock:581)"
    },
    ["Tiny Madness"] = {
        pet1 = 71163,
        pet2 = 34770,
        pet3 = 0,
        script = "standby [round=2]\nability(Curse of Doom:218) [round=3]\nability(Haunt:652) [round=4]\nability(Dead Man's Party:1093) [!enemy.aura(Shattered Defenses:542).exists]\nability(#1)\nchange(next)"
    },
    ["Brain Tickling"] = {
        pet1 = 86447,
        pet2 = 143564,
        pet3 = 62621,
        script = "use(#1) [ self(#2).dead ]\nuse(Flock:581) [ enemy.aura(Black Claw:918).exists ]\nuse(Black Claw:919)\nuse(Conflagrate:179) [ enemy.aura(Shattered Defenses:542).duration<2 ]\nuse(Scorched Earth:172)\nuse(Flame Breath:501)\nchange(#1)"
    },
    ["Living Statues Are Tough"] = {
        pet1 = 71163,
        pet2 = 34770,
        pet3 = 0,
        script = "ability(Curse of Doom:218) \nability(Haunt:652) \nability(Dead Man's Party:1093) [!enemy.aura(Shattered Defenses:542).exists]\nability(#1)\nchange(next)"
    },
    ["Retinus the Seeker"] = {
        pet1 = 86447,
        pet2 = 143564,
        pet3 = 55367,
        script = "use(Explode:282) [enemy.hp<610]\nuse(Flock:581) [enemy.aura(Black Claw:918).exists]\nuse(Black Claw:919)\nuse(Thunderbolt:779)\nuse(Missile:777)\nchange(next)"
    },
    ["I Am The One Who Whispers"] = {
        pet1 = 86447,
        pet2 = 143564,
        pet3 = 62201,
        script = "use(Flock:581) [ enemy.aura(Black Claw:918).exists ]\nuse(Black Claw:919)\nuse(Scorched Earth:172)\nuse(Breath:115)\nchange(next)"
    },
    ["Dune Buggy"] = {
        pet1 = 115146,
        pet2 = 70451,
        pet3 = 69796,
        script = "ability(Blistering Cold:786) [round=1]\nability(BONESTORM:1762) [round>2]\nability(Chop:943)\nability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nability(Hunting Party:921)\nchange(next)"
    },
    ["Watch Where You Step"] = {
        pet1 = 71163,
        pet2 = 73011,
        pet3 = 99505,
        script = "ability(Curse of Doom:218)\nability(Inflation:1002) [enemy.aura(Shattered Defenses:542).duration<2]\nability(#1) [self(#3).active]\nability(#3)\nchange(next)"
    },
    ["Strange Looking Dogs"] = {
        pet1 = 77221,
        pet2 = 113136,
        pet3 = 83642,
        script = "change(#2) [ self(Iron Starlette:1387).dead & !self(#2).played ]\nchange(#3) [ self(Iron Starlette:1387).dead & self(#2).played ]\nuse(Wind-Up:459) [ !self.aura(Wind-Up:458).exists ]\nuse(Supercharge:208) [ !self.aura(Supercharged:207).exists ]\nuse(Powerball:566) [ !self.aura(Speed Boost:831).exists & enemy(Pokey:2332).active ]\nuse(Wind-Up:459)\nuse(Swarm of Flies:232) [ !enemy.aura(Swarm of Flies:231).exists ]\nuse(Bubble:934)\nuse(Tongue Lash:228)"
    },
    ["Sea Creatures Are Weird"] = {
        pet1 = 77221,
        pet2 = 64899,
        pet3 = 0,
        script = "quit [ enemy(#1).active & !enemy.ability(Sweep:457).usable ]\nchange(#1) [ self(#3).active ]\nchange(#3) [ self(#1).dead ]\nif [ self(#1).active ]\n    ability(Supercharge:208) [ round~2,6 ]\n    ability(Wind-Up:459) [ enemy(#1).active ]\n    ability(Wind-Up:459) [ round>6 & self.aura(Mechanical:244).exists & self.aura(Wind-Up:458).exists ]\n    ability(Powerball:566)\nendif\nability(Explode:282) [ enemy(#3).active & enemy(#3).hp<561 ]\nability(Thunderbolt:779) [ !enemy(#2).dead & enemy(#2).hp<245 ]\nability(Thunderbolt:779) [ enemy(#3).active ]\nability(Breath:115)"
    },
    ["Automated Chaos"] = {
        pet1 = 143811,
        pet2 = 15710,
        pet3 = 0,
        script = "change(#3) [ enemy(#3).active ]\nstandby [ self(#3).active ]\nchange(#1) [ round = 6 ]\nuse(1955) [ round = 1 ]\nuse(118) [ round = 7 & enemy(#1).hp > 1250 ]\nstandby [ round = 7 ]\nuse(418)\nchange(#2)\nuse(206) [ round = 5 ]\nuse(481) [ enemy.aura(417).exists ]\nuse(477)"
    },
    ["This Little Piggy Has Sharp Tusks"] = {
        pet1 = 71163,
        pet2 = 73011,
        pet3 = 99505,
        script = "change(next) [ self(#1).dead & !self(#3).played ] \nability(#2) [ !enemy.aura(217).exists ] \nability(#3) \nability(#1)"
    },
    ["Rogue Azerite"] = {
        pet1 = 66950,
        pet2 = 64352,
        pet3 = 63001,
        script = "ability(Whirlpool:513) [self(Pandaren Water Spirit:868).active]\nability(Dive:564) [self(Pandaren Water Spirit:868).active]\nability(Water Jet:118) [self(Pandaren Water Spirit:868).active]\nchange(#2) [self(Pandaren Water Spirit:868).dead & !self(#3).active]\nchange(#3)\nability(Shell Shield:310) [self(#3).aura(Shell Shield:309).duration <2]\nability(Dive:564)\nability(Absorb:449)"
    },
    ["Night Horrors"] = {
        pet1 = 86447,
        pet2 = 73011,
        pet3 = 0,
        script = "change(next) [ self(#1).dead & !self(#3).played ]\nability(Black Claw:919) [ !enemy.aura(Black Claw:918).exists ]\nability(Black Claw:919) [ enemy(#3).active & self.hp>366 ]\nability(Flock:581)\nability(Make it Rain:985)\nability(#1)"
    },
    ["You've Never Seen Jammer Upset"] = {
        pet1 = 77221,
        pet2 = 0,
        pet3 = 0,
        script = "if [ self(Iron Starlette:1387).active ] \nability(Wind-Up:459) [ round=1 ] \nability(Supercharge:208) [ round=2 ] \nability(Wind-Up:459) [ round=3 ] \nability(Wind-Up:459) [ round=4 ] \nchange(#2) [ round=5 ] \nability(Wind-Up:459) [ round >= 6 ] \nendif \nchange(Iron Starlette:1387) [ self(#2).active ]"
    },
    ["Critters are Friends, Not Food"] = {
        pet1 = 161964,
        pet2 = 88225,
        pet3 = 0,
        script = "ability(Void Nova:2356)\nability(Poison Protocol:1954)\nability(Soulrush:752) [enemy(#2).active]\nability(Moonfire:595) [enemy(#3).active]\nability(#1)\nchange(next)"
    },
    ["Keeyo's Champions of Vol'dun"] = {
        pet1 = 73741,
        pet2 = 71942,
        pet3 = 0,
        script = "change(#2) [ enemy(#1).hp<715 ]\nuse(Booby-Trapped Presents:1080)\nuse(Greench's Gift:1076)\nuse(Club:1079)\nuse(Moonfire:595) [ !weather(Moonlight:596) ]\nuse(Prowl:536) [ enemy(#3).active ]\nuse(Spirit Claws:974)"
    },
    ["Desert Survivors"] = {
        pet1 = 143821,
        pet2 = 68838,
        pet3 = 0,
        script = "use(Whirlpool:513)\nuse(Inner Vision:216) [enemy.aura(Whirlpool:512).exists & enemy(#3).active]\nuse(Inner Vision:216) [enemy.aura(Underground:340).exists]\nuse(Inner Vision:216) [enemy.aura(Whirlpool:512).duration=1]\nuse(Punch:111)\nuse(Pounce:535) [enemy(#2).active]\nuse(Supercharge:208)\nuse(Pounce:535)\nchange(next)"
    },
    ["Ezra Grimm"] = {
        pet1 = 115146,
        pet2 = 88134,
        pet3 = 143796,
        script = "change(#2) [self.aura(Howl:1725).exists & self(#1).active]\nchange(#1) [self(#2).active & enemy(#3).active & enemy.hpp=100 & enemy.aura(Blinding Poison:1048).exists]\nchange(#2) [self(#3).active & enemy(#3).active]\nchange(#3) [self(#2).active & enemy(#2).active]\nchange(#2) [round=3]\nuse(Blistering Cold:786)\nuse(Chop:943)\nuse(Blinding Poison:1049)\nuse(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nuse(Barbed Stinger:1369)\n--\nuse(Dodge:312) [self.aura(Elementium Bolt:605).exists]\nuse(Tornado Punch:1052) [enemy.hp<335]\nuse(Jab:219)\nchange(#3)"
    },
    ["Darkness"] = {
        pet1 = 88577,
        pet2 = 97324,
        pet3 = 86067,
        script = ""
    },
    ["AoE/Cleave"] = {
        pet1 = 154814,
        pet2 = 115148,
        pet3 = 64899,
        script = ""
    },
    ["Sandstorm (Shielding)"] = {
        pet1 = 113440,
        pet2 = 69748,
        pet3 = 77221,
        script = ""
    },
    ["Using PvE Pets"] = {
        pet1 = 71163,
        pet2 = 68659,
        pet3 = 77221,
        script = ""
    },
    ["Angry Geode"] = {
        pet1 = 88300,
        pet2 = 0,
        pet3 = 0,
        script = "ability(Dive:564) [enemy.aura(Stoneskin:435).exists & enemy.ability(Crystal Prison:569).usable]\nability(Nature's Ward:574) [self.hpp<100 & !self.aura(Nature's Ward:820).exists]\nability(#1)\nchange(next)"
    },
    ["\"Captain\" Klutz"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 0,
        script = "standby [ enemy.round < 3 ]\nability(218)\nability(652)\nchange(#2)\nability(919) [ !enemy.aura(918).exists ]\nability(581)"
    },
    ["Klutz's Battle Rat"] = {
        pet1 = 68846,
        pet2 = 68805,
        pet3 = 81431,
        script = "ability(124)\nability(202)\nchange(#2)\n\nability(#3) [enemy.hp<618 & enemy.type !~ 3]\nability(#3) [enemy.hp<406 & enemy.type ~ 3]\nability(#2) [!self(#2).aura(820).exists]\nability(#1)"
    },
    ["Klutz's Battle Monkey"] = {
        pet1 = 15699,
        pet2 = 68659,
        pet3 = 0,
        script = "use(208) [ round=1 ]\nuse(204)\nuse(490) [ self.aura(512).duration=1 ]\nuse(490) [ enemy.aura(341).exists ]\nuse(436) [ self.aura(435).duration<=1 & enemy(#3).hp>227 ]\nuse(#1)\nchange(#2)"
    },
    ["Cookie's Leftovers"] = {
        pet1 = 115146,
        pet2 = 86447,
        pet3 = 143564,
        script = "standby [ round=1]\nstandby [ self.aura(Asleep:926).exists]\nuse(Blistering Cold:786) [self.ability(Blistering Cold:786).usable]\nuse(Chop:943) [!enemy.aura(Bleeding:491).exists]\nuse(BONESTORM!!:1762)\nchange(#2) [self(#1).dead]\nuse(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nuse(Flock:581)"
    },
    ["Dos-Ryga"] = {
        pet1 = 77221,
        pet2 = 115140,
        pet3 = 68654,
        script = "change(#1) [self(#2).active & self.dead]\nchange(#2) [round=2]\nuse(Supercharge:208) [self.aura(Wind-Up:458).exists]\nuse(Wind-Up:459)\nuse(Howl:362) [self.aura(Undead:242).exists]\nuse(Diseased Bite:499)"
    },
    ["Kafi"] = {
        pet1 = 84885,
        pet2 = 9656,
        pet3 = 0,
        script = "use(Explode:282) [enemy.hp.can_explode]\nuse(282) [enemy.aura(639).exists & enemy.hp<700]\nuse(282) [self(#1).active & round>2]\nuse(Toxic Smoke:640) [!enemy.aura(639).exists]\nuse(Reflective Shield:1105)\nuse(#1)\nstandby\nchange(next)"
    },
    ["Ti'un the Wanderer"] = {
        pet1 = 86447,
        pet2 = 64899,
        pet3 = 0,
        script = "if [ self(#1).active]\nstandby [enemy(#1).hp.can_be_exploded]\nability(Black Claw:919) [ round=1 ]\nability(#3) [ enemy.aura(Black Claw:918).exists ]\nability(#1) [ !enemy.hp.can_be_exploded]\nendif\nchange(#3) [ self(#1).dead ]\nability(#1) [ !enemy.hp.can_be_exploded]\nability(Explode:282) [ enemy.hp.can_be_exploded]"
    },
    ["Gorespine"] = {
        pet1 = 84885,
        pet2 = 86716,
        pet3 = 77221,
        script = "use(Explode:282) [enemy.hp<=1250]\nuse(Reflective Shield:1105) [self.round=1]\nuse(#1)\nchange(next)"
    },
    ["Skitterer Xi'a"] = {
        pet1 = 55367,
        pet2 = 86716,
        pet3 = 0,
        script = "use(Flyby:515) [round=1]\nuse(Thunderbolt:779)\nuse(Explode:282)\nchange(next)"
    },
    ["Greyhoof"] = {
        pet1 = 77221,
        pet2 = 115140,
        pet3 = 55367,
        script = "ability(Wind-Up:459) [round=1]\nability(Supercharge:208) [round=2]\nability(Wind-Up:459) [round=3]\nability(Powerball:566)\nchange(#2) [self(#1).dead]\nability(Explode:282) [enemy.hp<614]\nability(Decoy:334)\nability(Missile:777)"
    },
    ["Lucky Yi"] = {
        pet1 = 69796,
        pet2 = 70451,
        pet3 = 0,
        script = "use(Hunting Party:921) [enemy.aura(918).exists]\nuse(Black Claw:919) [self.round=1]\nuse(Leap:364)\nchange(next)"
    },
    ["Ka'wi the Gorger"] = {
        pet1 = 70451,
        pet2 = 69796,
        pet3 = 86447,
        script = "change(#2) [self(#1).dead]\nuse(Garra negra:919) [!enemy.aura(Garra negra:918).exists]\nuse(Bandada:581)\nuse(Grupo de caza:921)\nuse(Saltar:364)"
    },
    ["Nitun"] = {
        pet1 = 71163,
        pet2 = 86447,
        pet3 = 143564,
        script = "use(Curse of Doom:218)\nuse(Haunt:652)\nuse(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nuse(Flock:581)\nchange(next)"
    },
    ["Ashlei"] = {
        pet1 = 179125,
        pet2 = 0,
        pet3 = 0,
        script = "use(Armageddon:1025) [enemy.aura(Flammenatem:500).exists & enemy.aura(Messerkrallen:2238).exists & enemy(#3).active]\nuse(Messerkrallen:2237) [enemy.aura(Flammenatem:500).exists & !enemy.aura(Messerkrallen:2238).exists]\nuse(Flammenatem:501)"
    },
    ["Gargra"] = {
        pet1 = 69778,
        pet2 = 55356,
        pet3 = 0,
        script = "change(#2) [enemy(#2).active & !self(#2).played]\nchange(#1) [self(#2).active]\nuse(Fel Immolate:901) [enemy(#3).active]\nuse(Supercharge:208)\nuse(Haywire:916)\nuse(Ion Cannon:209)\nchange(#3)"
    },
    ["Taralune"] = {
        pet1 = 77221,
        pet2 = 97205,
        pet3 = 68845,
        script = "if [enemy(#1).active]\nstandby [round=1]\nability(Supercharge:208) [round=3]\nability(Wind-Up:459)\nendif\n\nchange(#3) [self(#1).dead & !self(#3).played]\nchange(#2) [self(#3).active]\nability(Arcane Storm:589)\nability(Mana Surge:489)\nability(#2)\nability(#1)"
    },
    ["Tarr the Terrible"] = {
        pet1 = 161964,
        pet2 = 172148,
        pet3 = 0,
        script = "change(#1) [self(#2).played]\nchange(#2) [round=4]\nuse(Corrosion:447) [round=1]\nuse(Poison Protocol:1954)\nuse(Void Nova:2356)\nuse(Corrosion:447)\nuse(Raise Ally:2298)\nuse(Dead Man's Party:1093)\nchange(#3)"
    },
    ["Vesharr"] = {
        pet1 = 68662,
        pet2 = 54027,
        pet3 = 64899,
        script = "ability(Arcane Explosion:299)\nability(Explode:282) [enemy.aura(Mechanical:244).exists]\nability(Thunderbolt:779) [!enemy.aura(Flying Mark:1420).exists]\nability(Breath:115)\nchange(#2)"
    },
    ["Wrathion"] = {
        pet1 = 61080,
        pet2 = 7560,
        pet3 = 63557,
        script = "change(next) [self.dead]\nuse(Dodge:312) [self.aura(Ice Tomb:623).duration = 1]\nuse(Stampede:163) [enemy(Cindy:1299).active & enemy.round = 4]\nuse(Stampede:163) [enemy(Alex:1301).active & !self.aura(Ice Tomb:623).exists]\nstandby [enemy.aura(Undead:242).exists]\nuse(Scratch:119)\nuse(Crush:406) [enemy(Alex:1301).aura(Shattered Defenses:542).exists]\nuse(Stoneskin:436) [!self.aura(Stoneskin:435).exists]\nuse(Deflection:490) [self.aura(Elementium Bolt:605).duration = 1]\nuse(Crush:406)\nuse(Dead Man's Party:1093)\nuse(Macabre Maraca:1094)"
    },
    ["Chen Stormstout"] = {
        pet1 = 79410,
        pet2 = 81431,
        pet3 = 0,
        script = "change(next) [ enemy(#2).active & !self(#3).played ]\nability(Decoy:334)\nability(Haywire:916)\nability(Dodge:312) [ enemy(#2).active ]\nability(Dodge:312) [ enemy.aura(Barrel Ready:353).exists ]\nability(Ravage:802) [ enemy(#2).active & enemy.hp<927 ]\nability(Ravage:802) [ enemy(#3).hp<619 ]\nability(#1)\nchange(#1)"
    },
    ["Shademaster Kiryn"] = {
        pet1 = 90206,
        pet2 = 68666,
        pet3 = 0,
        script = "change(#3) [enemy(Eté:1286).active & !self(#3).played]\nchange(#2) [self(#3).active]\n\nuse(Frappé par l’amour:772) [enemy(Stormoen:1287).active]\n\nuse(Malédiction funeste:218) [!enemy(Eté:1286).active]\nuse(Horion de l’ombre:422) [enemy(Nairn:1288).active]\n\nstandby [enemy.aura(Esquive:311).exists]\nuse(Prison de cristal:569) [enemy.aura(Rôder:543).exists]\nuse(Peau de pierre:436) [enemy(Eté:1286).active & !self.aura(Peau de pierre:435).exists ]\nuse(Peau de pierre:436) [enemy(Eté:1286).active & enemy.round =1]\nuse(Brûlure:113)\n\nuse(Frappé par l’amour:772) [enemy.aura(Rôder:543).exists]\nuse(Horion de l’ombre:422)\n\nchange(#1)"
    },
    ["Wise Mari"] = {
        pet1 = 73011,
        pet2 = 86081,
        pet3 = 0,
        script = "ability(Blingtron Gift Package:989) [ enemy.aura(Make it Rain:986).duration=1 ]\nability(Make it Rain:985)\nability(Inflation:1002)\nability(Consume Magic:1231) [ self.aura(Whirlpool:512).exists ]\nability(Creeping Ooze:448)\nchange(#2)"
    },
    ["Dr. Ion Goldbloom"] = {
        pet1 = 68662,
        pet2 = 62621,
        pet3 = 25706,
        script = "use(Howl:362) [enemy.aura(Flying:341).exists]\nuse(Surge of Power:593) [enemy.aura(Howl:1725).exists]\nuse(Arcane Explosion:299)\nuse(Conflagrate:179) [enemy(#3).active]\nuse(Flame Breath:501) [!enemy.aura(Flame Breath:500).exists]\nuse(Scorched Earth:172)\nuse(Ion Cannon:209) [enemy(#3).hp<1142]\nuse(#1)\nchange(next)"
    },
    ["Chi-Chi, Hatchling of Chi-Ji"] = {
        pet1 = 68664,
        pet2 = 32791,
        pet3 = 61366,
        script = "standby [ round=7 & self(#3).active ]\nuse(409) [ round=1 ]\nuse(592) [ round=2 ]\nuse(163) [ round=4 ]\nuse(518)\nchange(next)"
    },
    ["Zao, Calfling of Niuzao"] = {
        pet1 = 54227,
        pet2 = 62818,
        pet3 = 61081,
        script = "use(Nut Barrage:167) [round=1]\nuse(Woodchipper:411) [self(#1).active]\nuse(Black Claw:919) [self.round=1 & self(#2).active]\nuse(Hunting Party:921) [self(#2).active]\nuse(Leap:364) [self(#2).active]\nuse(#1)\nchange(next)"
    },
    ["another strategy"] = {
        pet1 = 88300,
        pet2 = 0,
        pet3 = 0,
        script = "use(Clobber:350)\nuse(Dive:564) [enemy(Yu'la, Broodling of Yu'lon:1317).aura(Flying:341).exists]\nuse(Punch:111)\nuse(#1)\nchange(next)"
    },
    ["Not Quite Dead Yet"] = {
        pet1 = 61826,
        pet2 = 90203,
        pet3 = 90204,
        script = "change(next) [ self.dead ] \nability(170) [ !self.aura(242).exists ] \nability(420) \nability(1392) [ enemy(2231).active & enemy.round = 1 ] \nability(752) [ enemy(2232).hp < 463 ] \nability(752) [ enemy(2231).active ] \nability(1066)"
    },
    ["Element of Success"] = {
        pet1 = 127863,
        pet2 = 127862,
        pet3 = 68467,
        script = "ability(Wind Buffet:1963) [round=2] \nability(Autumn Breeze:964) [round=4] \nability(#1) \nchange(next)"
    },
    ["Machine Learning"] = {
        pet1 = 77221,
        pet2 = 69778,
        pet3 = 90212,
        script = "ability(Supercharge:208) [ self.aura(Wind-Up:458).exists ]\nability(Wind-Up:459)\nchange(next) [ !self.ability(Haywire:916).usable ]\nability(Haywire:916)\nchange(next)"
    },
    ["BurlyQuest: Strange Looking Dogs"] = {
        pet1 = 15698,
        pet2 = 73741,
        pet3 = 15705,
        script = "use(Ice Tomb:624) [enemy.hpp = 100 & !enemy.aura(Ice Tomb:623).exists]\nuse(Call Blizzard:206) [!enemy.aura(Undead:242).exists & !weather(Blizzard:205)]\nuse(#1)\n\nstandby\nchange(next)"
    },
    ["Ellie VernQuest: Sea Creatures Are Weird"] = {
        pet1 = 73741,
        pet2 = 15698,
        pet3 = 15705,
        script = "use(Ice Tomb:624) [enemy.aura(Undead:242).exists]\nstandby [enemy.aura(Undead:242).exists]\nuse(Ice Tomb:624) [enemy.hpp>95 & !enemy.aura(Ice Tomb:623).exists]\nuse(Call Blizzard:206)\nuse(Ice Lance:413)\nchange(#1)\nchange(next)"
    },
    ["Eddie FixitQuest: Automated Chaos"] = {
        pet1 = 68659,
        pet2 = 0,
        pet3 = 0,
        script = "standby [ enemy(\"Fixed\" Remote Control Rocket Chicken:2204).active ]\nuse(Sandstorm:453)\nuse(Rupture:814)\nuse(Crush:406)\nuse(#1)\nchange(next)"
    },
    ["Dilbert McClintQuest: Night Horrors"] = {
        pet1 = 73741,
        pet2 = 15698,
        pet3 = 15705,
        script = "standby [self.aura(Blinding Poison:1048).exists]\nuse(Booby-Trapped Presents:1080) [!enemy.aura(Booby-Trapped Presents:1081).exists]\nuse(Greench's Gift:1076) [enemy(Atherton:2209).aura(Underground:340).exists]\nuse(Greench's Gift:1076) [enemy.ability(Burrow:159).duration>=1 & enemy.ability(Blinding Poison:1049).duration>=1]\nuse(Greench's Gift:1076) [enemy(Jennings:2208).active]\nuse(Gift of Winter Veil:586)\nuse(Call Blizzard:206)\nuse(Ice Lance:413)\nuse(Dive Bomb:2463)\nuse(Arm Cannon Blast:2462)\nchange(next)"
    },
    ["Captain HermesQuest: Crab People"] = {
        pet1 = 73741,
        pet2 = 15698,
        pet3 = 15705,
        script = "use(Ice Tomb:624) [!enemy.aura(Ice Tomb:623).exists]\nuse(Call Blizzard:206)\nuse(Ice Lance:413)\nchange(next)"
    },
    ["KaragaQuest: Critters are Friends, Not Food"] = {
        pet1 = 73741,
        pet2 = 68659,
        pet3 = 0,
        script = "change(next) [ self.dead ]\nability(1080)\nability(1076)\nability(814) [ enemy.hp > 400 ]\nability(436) [ self.aura(435).duration <= 1 ]\nability(#1)"
    },
    ["LozuQuest: Marshdwellers"] = {
        pet1 = 73741,
        pet2 = 15698,
        pet3 = 15705,
        script = "ability(Ice Tomb:624) [round=1]\nability(Gift of Winter's Veil:586) [enemy(#2).active]\nability(Gift of Winter's Veil:586) [!enemy.ability(Cocoon Strike:506).usable]\nability(Call Blizzard:206) [!weather(Blizzard:205)]\nability(Ice Lance:413)\nchange(next)"
    },
    ["KeeyoQuest: Keeyo's Champions of Vol'dun"] = {
        pet1 = 15698,
        pet2 = 15705,
        pet3 = 73741,
        script = "standby [enemy.aura(Dodge:2060).exists]\nability(Gift of Winter's Veil:586)\nability(Call Blizzard:206) [round=2]\nability(Booby-Trapped Presents:1080) [self.round=1]\nability(Greench's Gift:1076) [enemy(Tikka:2346).hp<1060]\nability(Rampage:124)\nability(#1)\nchange(next)"
    },
    ["KusaQuest: Desert Survivors"] = {
        pet1 = 68659,
        pet2 = 0,
        pet3 = 0,
        script = "use(Deflection:490) [enemy.aura(Underground:340).exists]\nuse(Stoneskin:436) [!self.aura(Stoneskin:435).exists]\nuse(Stoneskin:436) [self.aura(Stoneskin:435).duration<2]\nuse(Crush:406)\nuse(#1)\nchange(next)"
    },
    ["Haunted Humanoids"] = {
        pet1 = 15698,
        pet2 = 73741,
        pet3 = 15705,
        script = "change(#2) [round=2]\nability(Ice Tomb:624) [round=1]\nability(Ice Tomb:624) [enemy(#3).active & enemy.round=1]\nability(Booby-Trapped Presents:1080) [self.round=1]\nability(Greench's Gift:1076)\nability(Call Blizzard:206)\nability(#1)\nchange(#1)"
    },
    ["Deathly Dragonkin"] = {
        pet1 = 54027,
        pet2 = 68845,
        pet3 = 97205,
        script = "use(Arcane Storm:589) [ round>1 & !enemy(#2).active ]\nif [ enemy(#1).active ]\n    use(Surge of Power:593) [ enemy.hp<1099 & self.aura(Dragonkin:245).exists ]\n    use(Surge of Power:593) [ enemy.hp<733 ]\nendif\nuse(Surge of Power:593) [ enemy(#3).active ]\nuse(Arcane Blast:421)\nuse(Mana Surge:489)\nchange(next)"
    },
    ["Flickering Fliers"] = {
        pet1 = 79410,
        pet2 = 149205,
        pet3 = 0,
        script = "use(Decoy:334)\nuse(Haywire:916) [ !enemy(#1).active ]\nuse(Alpha Strike:504)\nuse(Lift-Off:170) [ enemy.ability(Amplify Magic:488).usable & enemy.ability(Moonfire:595).duration<2 & !self.speed.fast ]\nuse(Shadowmeld:2253) [ enemy(#3).active ]\nuse(Dark Talon:1233)\nstandby\nchange(next)"
    },
    ["Aquatic Apparitions"] = {
        pet1 = 143041,
        pet2 = 29726,
        pet3 = 32595,
        script = "use(Ice Tomb:624)\nuse(Call Blizzard:206)\nuse(Surge:509) [ enemy.ability(Horn Attack:571).usable ]\nuse(Surge:509) [ enemy(#2).active & enemy.hp<211 ]\nuse(Ice Lance:413) [ weather(Blizzard:205) & !enemy.aura(Amplify Magic:487).exists ]\nuse(Surge:509)\nuse(Phase Shift:764) [ enemy.ability(Amplify Magic:488).usable & self.speed.slow ]\nuse(Expunge:450) [ enemy.aura(Amplify Magic:487).exists ]\nuse(Ooze Touch:445)\nchange(next)"
    },
    ["Macabre Mechanicals"] = {
        pet1 = 55367,
        pet2 = 77221,
        pet3 = 73011,
        script = "if [self(Darkmoon Zeppelin:339).active]\nuse(Explode:282) [enemy(Shelby:2972).active & enemy.hp <=618]\nuse(Decoy:334)\nuse(Missile:777)\nendif\nif [self(Iron Starlette:1387).active &enemy(Tinyhoof:2973).active]\nuse(Wind-Up:459)\nendif\nif [self(Iron Starlette:1387).active & enemy(Glitterwing:2974).active]\nuse(Toxic Smoke:640) [!enemy.aura(Toxic Smoke:639).exists]\nuse(Toxic Smoke:640) [self(Iron Starlette:1387).hp<500]\nuse(Wind-Up:459) [self.aura(Wind-Up:458).exists]\nuse(Wind-Up:459)\nendif\nif [self(Lil' Bling:1320).active]\nuse(Blingtron Gift Package:989)\nuse(Make it Rain:985) [!enemy.aura(Make it Rain:986).exists]\nuse(Inflation:1002)\nendif\nchange(next)"
    },
    ["StratiosQuest: Cliffs of Bastion"] = {
        pet1 = 15698,
        pet2 = 73741,
        pet3 = 15705,
        script = "change(#2) [round=2]\nability(Ice Tomb:624) [round=1]\nability(Ice Tomb:624) [enemy(#3).active & enemy.round=1]\nability(Booby-Trapped Presents:1080) [self.round=1]\nability(Greench's Gift:1076)\nability(Call Blizzard:206)\nability(#1)\nchange(#1)"
    },
    ["ZollaQuest: Micro Defense Force"] = {
        pet1 = 15698,
        pet2 = 73741,
        pet3 = 15705,
        script = "ability(Ice Tomb:624) [round=1]\nability(Ice Tomb:624) [enemy(#3).active & enemy.round=1]\nability(Call Blizzard:206) [weather(Blizzard:205).duration<2]\nability(Ice Lance:413)\nchange(next)"
    },
    ["TheniaQuest: Thenia's Loyal Companions"] = {
        pet1 = 15698,
        pet2 = 15705,
        pet3 = 73741,
        script = "ability(Gift of Winter's Veil:586)\nability(Booby-Trapped Presents:1080) [enemy(#2).active]\nability(Call Blizzard:206) [weather(Blizzard:205).duration<2]\nability(Ice Lance:413)\nstandby\nchange(next)"
    },
    ["Caregiver MaximillianQuest: Mighty Minions of Maldraxxus"] = {
        pet1 = 15698,
        pet2 = 73741,
        pet3 = 15705,
        script = "change(#2) [round=3]\nchange(#1) [enemy(#2).dead & enemy(#1).active]\n\nability(Booby-Trapped Presents:1080) [enemy(#1).hp>0]\nstandby [enemy(#3).active & enemy.ability(Lift-Off:170).usable]\nability(Greench's Gift:1076)\n\nability(Ice Tomb:624) [enemy.aura(Resilient:924).duration=1]\nability(Call Blizzard:206)\nability(Ice Tomb:624) [enemy.ability(Burrow:159).usable & enemy(#2).hp>0 & enemy(#1).active]\n\nability(Gift of Winter's Veil:586)\n\nability(#1)\nchange(#1)"
    },
    ["Addius the TormentorQuest: The Mind Games of Addius"] = {
        pet1 = 15698,
        pet2 = 73741,
        pet3 = 15705,
        script = "use(Mind Games: Health:2388)\nuse(Call Blizzard:206)\nuse(Ice Tomb:624) [ round<5 ]\nuse(Greench's Gift:1076)\nuse(Ice Lance:413)\nchange(next)"
    },
    ["https://www.wow-petguide.com/Strategy/11028/Mega_Bite"] = {
        pet1 = 77221,
        pet2 = 115140,
        pet3 = 0,
        script = "use(Aufladen:208) [ !enemy.ability(Stachelpanzerschale:2324).usable ]\nuse(Aufziehen:459)"
    },
    ["Trainer Grrglin"] = {
        pet1 = 21010,
        pet2 = 62050,
        pet3 = 65187,
        script = "use(Cocoon Strike:506)\nuse(Moth Dust:508)\nuse(Alpha Strike:504)\nchange(next)"
    },
    ["https://www.wow-petguide.com/Strategy/10529/Trainer_Grrglin"] = {
        pet1 = 86447,
        pet2 = 106283,
        pet3 = 0,
        script = "ability(Savage Talon:1370) [enemy.round>4]\nability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nability(Puppy Parade:1681) [!enemy.aura(Shattered Defenses:542).exists]\nability(Flock:581)\nability(Superbark:1357) [enemy.hp>661]\nability(#1)\nchange(next)"
    },
    ["Klick"] = {
        pet1 = 86447,
        pet2 = 106283,
        pet3 = 0,
        script = "ability(Savage Talon:1370) [enemy.round>4]\nability(Black Claw:919) [!enemy.aura(Black Claw:918).exists]\nability(Puppy Parade:1681) [!enemy.aura(Shattered Defenses:542).exists]\nability(Flock:581)\nability(Superbark:1357) [enemy.hp>661]\nability(#1)\nchange(next)"
    },
    ["Living Permafrost"] = {
        pet1 = 90201,
        pet2 = 62922,
        pet3 = 62182,
        script = "use(Toxic Skin:1087) [round~1]\nuse(Toxic Skin:1087) [self.aura(Toxic Skin:1086).duration~1]\nuse(Whirlpool:513)\nuse(Water Jet:118)\nchange(#2) [enemy.type=10]\nchange(#3) [enemy.type=5]\nuse(Stoneskin:436) [!self.aura(Stoneskin:435).exists]\nuse(Stoneskin:436) [self.aura(Stoneskin:435).duration=1]\nuse(Leech Life:383) [enemy.aura(Webbed:338).exists]\nuse(Sticky Web:339)\nuse(Brittle Webbing:382) [!enemy.aura(Brittle Webbing:381).exists]\nuse(Leech Life:383) [enemy.aura(Brittle Webbing:381).exists]\nuse(Poison Spit:380)\nchange(#2)\nchange(#3)"
    },
    ["Door Control Console"] = {
        pet1 = 64352,
        pet2 = 63001,
        pet3 = 62246,
        script = "ability(Acidic Goo:369) [ enemy.hp.full ]\nuse(Dive:564) [round=2] \nuse(Dive:564) [self.aura(Ice Tomb:623).duration=1] \nuse(Dive:564) [self.aura(Sewage Eruption:2063).duration=1] \nuse(Ooze Touch:445) \nchange(next)"
    },
    ["Gnomeregan Guard Mechanostrider"] = {
        pet1 = 98463,
        pet2 = 71488,
        pet3 = 0,
        script = "change(next) [ self.dead ]\nability(Photosynthese:268) [ !self.aura(Photosynthese:267).exists ]\nability(Sonnenlicht:404) [ !weather(Sonnenschein:403) ]\nability(Panzerschild:310) [ !self.aura(Panzerschild:309).exists ]\nstandby [ enemy.aura(Untot:242).exists ]\nability(#1)"
    },
    ["Gnomeregan Guard Tiger"] = {
        pet1 = 15710,
        pet2 = 0,
        pet3 = 0,
        script = "if [self(Tiny Snowman:117).active]\nuse(Call Blizzard:206)\nuse(Howling Blast:120)\nuse(Snowball:477)\nchange(next)\nendif\n\nif [self(#2).active]\nuse(#1)\nchange(next)\nendif\n\nif [self(#3).active]\nuse(#1)\nendif"
    },
}