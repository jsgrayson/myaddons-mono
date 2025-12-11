import json
import sys
import time
from simulator.simulator import BattleSimulator
from simulator.battle_state import BattleState, Team, Pet, PetStats, PetFamily, PetQuality, Ability
from simulator.npc_ai import create_npc_agent

def create_dummy_player_team():
    """Creates a standard player team for testing"""
    # A generic strong team: Mechanical, Undead, Dragonkin
    pets = [
        Pet(
            species_id=1, name="Iron Starlette", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
            stats=PetStats(max_hp=1400, current_hp=1400, power=325, speed=244),
            abilities=[
                Ability(id=459, name="Wind-Up", power=50, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL),
                Ability(id=208, name="Supercharge", power=0, accuracy=100, speed=0, cooldown=3, family=PetFamily.MECHANICAL),
                Ability(id=777, name="Powerball", power=20, accuracy=100, speed=20, cooldown=0, family=PetFamily.MECHANICAL)
            ]
        ),
        Pet(
            species_id=2, name="Unborn Val'kyr", family=PetFamily.UNDEAD, quality=PetQuality.RARE,
            stats=PetStats(max_hp=1237, current_hp=1237, power=292, speed=292),
            abilities=[
                Ability(id=652, name="Haunt", power=0, accuracy=100, speed=0, cooldown=4, family=PetFamily.UNDEAD),
                Ability(id=218, name="Curse of Doom", power=0, accuracy=100, speed=0, cooldown=5, family=PetFamily.UNDEAD),
                Ability(id=321, name="Unholy Ascension", power=0, accuracy=100, speed=0, cooldown=0, family=PetFamily.UNDEAD)
            ]
        ),
        Pet(
            species_id=3, name="Nexus Whelpling", family=PetFamily.DRAGONKIN, quality=PetQuality.RARE,
            stats=PetStats(max_hp=1400, current_hp=1400, power=325, speed=244),
            abilities=[
                Ability(id=122, name="Tail Sweep", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.DRAGONKIN),
                Ability(id=593, name="Mana Surge", power=60, accuracy=100, speed=0, cooldown=3, family=PetFamily.MAGIC),
                Ability(id=206, name="Arcane Storm", power=25, accuracy=100, speed=0, cooldown=5, family=PetFamily.MAGIC)
            ]
        )
    ]
    return Team(pets=pets)

def load_data():
    try:
        with open('encounters.json', 'r') as f:
            encounters = json.load(f)
        
        with open('abilities.json', 'r') as f:
            abilities = json.load(f)
            
        # Load manual overrides
        import os
        if os.path.exists('ability_stats_manual.json'):
            with open('ability_stats_manual.json', 'r') as f:
                manual_stats = json.load(f)
                for aid, data in manual_stats.items():
                    abilities[aid] = data
                    
        return encounters, abilities
    except FileNotFoundError as e:
        print(f"❌ Data file not found: {e}")
        return {}, {}

def run_suite():
    encounters, ability_db = load_data()
    if not encounters:
        return

    simulator = BattleSimulator(rng_seed=42)
    
    print(f"🚀 Starting Full Encounter Suite ({len(encounters)} encounters)...")
    print("="*60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    start_time = time.time()
    
    # Sort encounters for consistent order
    sorted_keys = sorted(encounters.keys())
    
    for encounter_key in sorted_keys:
        encounter_data = encounters[encounter_key]
        encounter_name = encounter_data.get('name', encounter_key)
        
        # Skip if no pets (some placeholders might exist)
        npc_pets_data = encounter_data.get('pets') or encounter_data.get('npc_pets')
        if not npc_pets_data:
            print(f"⚠️  Skipping {encounter_name}: No pet data")
            skipped += 1
            continue
            
        try:
            # Build Enemy Team
            enemy_pets = []
            for p_data in npc_pets_data:
                # Handle ability IDs (integers) vs objects
                abilities = []
                for ab in p_data.get('abilities', []):
                    if isinstance(ab, int):
                        ab_info = ability_db.get(str(ab)) or ability_db.get(ab)
                        if ab_info:
                            fam_val = ab_info.get('family_id', 7)
                            try: fam = PetFamily(fam_val)
                            except: fam = PetFamily.BEAST
                            abilities.append(Ability(
                                id=ab, name=ab_info.get('name', 'Unknown'), 
                                power=ab_info.get('power', 20), accuracy=ab_info.get('accuracy', 100), 
                                speed=ab_info.get('speed', 0), cooldown=ab_info.get('cooldown', 0), 
                                family=fam,
                                effect_type=ab_info.get('effect_type'),
                                is_heal=ab_info.get('is_heal', False)
                            ))
                        else:
                            abilities.append(Ability(id=ab, name=f"Ability {ab}", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST))
                    else:
                        # Assuming it's a dict if not int
                        pass
                
                stats_data = p_data.get('stats', {'health': 1000, 'power': 200, 'speed': 200})
                stats = PetStats(
                    max_hp=stats_data.get('health', 1000),
                    current_hp=stats_data.get('health', 1000),
                    power=stats_data.get('power', 200),
                    speed=stats_data.get('speed', 200)
                )
                
                family_str = p_data.get('family', 'Beast').upper()
                try:
                    family = PetFamily[family_str]
                except KeyError:
                    family = PetFamily.BEAST
                    
                enemy_pets.append(Pet(
                    species_id=p_data.get('species_id', 0),
                    name=p_data.get('name', 'Unknown'),
                    family=family,
                    quality=PetQuality.RARE,
                    stats=stats,
                    abilities=abilities
                ))
            
            enemy_team = Team(pets=enemy_pets)
            player_team = create_dummy_player_team()
            
            state = BattleState(player_team, enemy_team, 1, rng_seed=42)
            
            # Create AI
            ai = create_npc_agent(encounter_name)
            
            # Run a short simulation (max 10 turns) to verify no crashes
            # We don't need to finish the battle, just ensure the AI and mechanics don't error
            result = simulator.simulate_battle(
                state, 
                lambda s: simulator.get_valid_actions(s, 'player')[0], # Simple player AI
                ai,
                max_turns=10,
                enable_logging=False
            )
            
            passed += 1
            # print(f"✅ {encounter_name}") # Too verbose for all
            
        except Exception as e:
            print(f"❌ FAILED: {encounter_name}")
            print(f"   Error: {str(e)}")
            failed += 1
            
    duration = time.time() - start_time
    
    print("="*60)
    print(f"Suite Completed in {duration:.2f}s")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print("="*60)
    
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    run_suite()
