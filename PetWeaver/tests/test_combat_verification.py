import unittest
from simulator import BattleSimulator, BattleState, Team, Pet, PetStats, PetFamily, PetQuality, Ability, TurnAction

class TestCombatVerification(unittest.TestCase):
    def setUp(self):
        # 1. Define Dos-Ryga (Boss)
        # Stats estimated for Boss: High HP, decent power
        self.dos_ryga = Pet(
            species_id=1193, name="Dos-Ryga", family=PetFamily.AQUATIC, quality=PetQuality.LEGENDARY,
            stats=PetStats(max_hp=3000, current_hp=3000, power=350, speed=280),
            abilities=[
                Ability(id=782, name="Frost Breath", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.DRAGONKIN), # Frost Breath is Dragonkin dmg
                Ability(id=513, name="Whirlpool", power=30, accuracy=100, speed=0, cooldown=3, family=PetFamily.AQUATIC),
                Ability(id=123, name="Healing Wave", power=40, accuracy=100, speed=0, cooldown=3, family=PetFamily.AQUATIC, is_heal=True)
            ]
        )
        self.enemy_team = Team([self.dos_ryga])

        # 2. Define Player Team (from Strategy)
        # Iron Starlette (P/P)
        self.starlette = Pet(
            species_id=77221, name="Iron Starlette", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
            stats=PetStats(max_hp=1400, current_hp=1400, power=341, speed=244),
            abilities=[
                Ability(id=459, name="Wind-Up", power=140, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL, stat_buffs={'power': (1.1, 99)}), # Simulating buff + big hit
                Ability(id=208, name="Supercharge", power=0, accuracy=100, speed=0, cooldown=3, family=PetFamily.MECHANICAL, stat_buffs={'power': (2.25, 1)}), # +125% for 1 turn
                Ability(id=777, name="Toxic Smoke", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL) # Filler
            ]
        )
        # Runeforged Servitor
        self.servitor = Pet(
            species_id=115140, name="Runeforged Servitor", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
            stats=PetStats(max_hp=1500, current_hp=1500, power=300, speed=260),
            abilities=[
                Ability(id=459, name="Wind-Up", power=30, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL),
                Ability(id=208, name="Supercharge", power=0, accuracy=100, speed=0, cooldown=3, family=PetFamily.MECHANICAL),
                Ability(id=111, name="Punch", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.HUMANOID)
            ]
        )
        # Stitched Pup (Undead)
        self.pup = Pet(
            species_id=68654, name="Stitched Pup", family=PetFamily.UNDEAD, quality=PetQuality.RARE,
            stats=PetStats(max_hp=1600, current_hp=1600, power=290, speed=250),
            abilities=[
                Ability(id=499, name="Diseased Bite", power=25, accuracy=100, speed=0, cooldown=0, family=PetFamily.UNDEAD),
                Ability(id=362, name="Howl", power=0, accuracy=100, speed=0, cooldown=3, family=PetFamily.BEAST, stat_buffs={'damage_taken': (2.0, 2)}), # Debuff enemy
                Ability(id=111, name="Consume", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.UNDEAD)
            ]
        )
        self.player_team = Team([self.starlette, self.servitor, self.pup])

    def test_dos_ryga_strategy(self):
        # Script Logic from Strategy:
        # change(#1) [self(#2).active & self.dead]
        # change(#2) [round=2]
        # use(Supercharge:208) [self.aura(Wind-Up:458).exists]
        # use(Wind-Up:459)
        # use(Howl:362) [self.aura(Undead:242).exists]
        # use(Diseased Bite:499)
        
        def player_agent(state):
            active_pet = state.player_team.get_active_pet()
            active_idx = state.player_team.active_pet_index
            turn = state.turn_number
            print(f"DEBUG: Agent called Turn {turn}, Active: {active_pet.name if active_pet else 'None'}")
            
            # 1. change(#2) [round=2] -> Swap to Servitor? Or Pup?
            # Strategy says: Iron Starlette (#1), Servitor (#2), Pup (#3)
            # Wait, usually strategies optimize for specific turns.
            # Let's try to follow the script literally.
            
            # "change(#2) [round=2]"
            # If it's round 2, swap to Pet 2 (Servitor)
            if turn == 2 and active_idx != 1:
                return TurnAction('player', 'swap', target_pet_index=1)

            # "use(Supercharge) [self.aura(Wind-Up).exists]"
            # Wind-Up applies a buff/aura when used first time.
            # In our sim, Wind-Up sets a flag or buff.
            # Let's assume if we have the "Wind-Up" buff, use Supercharge.
            wind_up_aura = any(b.name == "Wind-Up" for b in active_pet.active_buffs)
            supercharge = next((a for a in active_pet.abilities if a.name == "Supercharge"), None)
            if wind_up_aura and supercharge and active_pet.can_use_ability(supercharge):
                return TurnAction('player', 'ability', ability=supercharge)

            # "use(Wind-Up)"
            wind_up = next((a for a in active_pet.abilities if a.name == "Wind-Up"), None)
            if wind_up:
                if active_pet.can_use_ability(wind_up):
                    # print(f"Turn {turn}: Using Wind-Up")
                    return TurnAction('player', 'ability', ability=wind_up)
                else:
                    print(f"Turn {turn}: Wind-Up on cooldown?")
            else:
                print(f"Turn {turn}: Wind-Up not found")
                
            # "use(Howl)"
            howl = next((a for a in active_pet.abilities if a.name == "Howl"), None)
            if howl and active_pet.can_use_ability(howl):
                return TurnAction('player', 'ability', ability=howl)
                
            # "use(Diseased Bite)"
            bite = next((a for a in active_pet.abilities if a.name == "Diseased Bite"), None)
            if bite and active_pet.can_use_ability(bite):
                return TurnAction('player', 'ability', ability=bite)
                
            # Fallback
            print(f"Turn {turn}: Fallback to ability 0")
            return TurnAction('player', 'ability', ability=active_pet.abilities[0])

        def enemy_agent(state):
            # Simple AI for Dos-Ryga
            pet = state.enemy_team.get_active_pet()
            # Use cooldowns if available
            for ab in pet.abilities:
                if ab.cooldown > 0 and pet.can_use_ability(ab):
                    return TurnAction('enemy', 'ability', ability=ab)
            return TurnAction('enemy', 'ability', ability=pet.abilities[0])

        simulator = BattleSimulator()
        state = BattleState(self.player_team, self.enemy_team, 1)
        result = simulator.simulate_battle(state, player_agent, enemy_agent, enable_logging=True)
        
        print(f"Winner: {result['winner']}")
        print(f"Turns: {result['turns']}")
        print(result['log'].get_full_log()) # Uncomment to debug
        
        self.assertEqual(result['winner'], 'player')

if __name__ == '__main__':
    unittest.main()
