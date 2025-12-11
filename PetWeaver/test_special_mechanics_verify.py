from simulator.battle_state import BattleState, Team, Pet, PetStats, PetFamily, Ability, TurnAction
from simulator.simulator import BattleSimulator
from simulator.special_encounters import SpecialEncounterHandler

def test_rocko_mechanic():
    print("\nTesting Rocko Immunity Mechanic...")
    
    player_pet = Pet(
        species_id=1, name="Player Pet", family=PetFamily.BEAST, quality=3,
        stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=300),
        abilities=[Ability(id=1, name="Bite", power=100, accuracy=100, speed=10, cooldown=0, family=PetFamily.BEAST)]
    )
    
    rocko = Pet(
        species_id=1811, name="Rocko", family=PetFamily.ELEMENTAL, quality=3,
        stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
        abilities=[Ability(id=1, name="Smash", power=20, accuracy=100, speed=10, cooldown=0, family=PetFamily.ELEMENTAL)]
    )
    
    state = BattleState(Team([player_pet]), Team([rocko]))
    sim = BattleSimulator()
    
    # Turn 1: Player attacks Rocko. Should be Immune.
    print("--- Turn 1 ---")
    sim.execute_turn(
        state, 
        TurnAction('player', 'ability', ability=player_pet.abilities[0]),
        TurnAction('enemy', 'pass'),
        turn_number=1,
        special_encounter_id='rocko_immunity'
    )
    
    if rocko.stats.current_hp == 1000:
        print("✅ Rocko took NO damage (Immune)")
    else:
        print(f"❌ Rocko took damage! HP: {rocko.stats.current_hp}")

    # Turn 11: Rocko should die automatically
    print("--- Turn 11 (Simulated) ---")
    # Manually advance turn to 11
    state.turn_number = 11
    # We need to call apply_rocko_immunity directly or via execute_turn
    # But execute_turn calls it inside the ability logic.
    # Wait, Rocko's death is handled in apply_rocko_immunity which returns False if turn > 10.
    # But who calls it?
    # In simulator.py:
    # if special_encounter_id == 'rocko_immunity' and SpecialEncounterHandler.apply_rocko_immunity(defender, state.turn_number): is_immune = True
    
    # So we need to attack Rocko on turn 11 to trigger the check?
    # Or does it happen automatically?
    # The code says:
    # if turn <= 10: return True
    # else: pet.stats.current_hp = 0; return False
    
    # So yes, we need to attack Rocko.
    sim.execute_turn(
        state, 
        TurnAction('player', 'ability', ability=player_pet.abilities[0]),
        TurnAction('enemy', 'pass'),
        turn_number=11,
        special_encounter_id='rocko_immunity'
    )
    
    if rocko.stats.current_hp == 0:
        print("✅ Rocko died on Turn 11")
    else:
        print(f"❌ Rocko is still alive! HP: {rocko.stats.current_hp}")


def test_life_exchange_mechanic():
    print("\nTesting Life Exchange Mechanic...")
    
    # Attacker (Low HP)
    attacker = Pet(
        species_id=1, name="Attacker", family=PetFamily.HUMANOID, quality=3,
        stats=PetStats(max_hp=1000, current_hp=100, power=300, speed=300), # 10% HP
        abilities=[Ability(id=277, name="Life Exchange", power=0, accuracy=100, speed=10, cooldown=0, family=PetFamily.HUMANOID)]
    )
    
    # Defender (High HP)
    defender = Pet(
        species_id=2, name="Defender", family=PetFamily.DRAGONKIN, quality=3,
        stats=PetStats(max_hp=2000, current_hp=2000, power=300, speed=250), # 100% HP
        abilities=[Ability(id=1, name="Bite", power=20, accuracy=100, speed=10, cooldown=0, family=PetFamily.DRAGONKIN)]
    )
    
    state = BattleState(Team([attacker]), Team([defender]))
    sim = BattleSimulator()
    
    print(f"Before: Attacker HP {attacker.stats.current_hp} (10%), Defender HP {defender.stats.current_hp} (100%)")
    
    sim.execute_turn(
        state, 
        TurnAction('player', 'ability', ability=attacker.abilities[0]),
        TurnAction('enemy', 'pass'),
        turn_number=1
    )
    
    # Expected:
    # Attacker gets 100% of its max HP = 1000
    # Defender gets 10% of its max HP = 200
    
    print(f"After:  Attacker HP {attacker.stats.current_hp}, Defender HP {defender.stats.current_hp}")
    
    if attacker.stats.current_hp == 1000 and defender.stats.current_hp == 200:
        print("✅ Life Exchange Swapped Percentages Correctly")
    else:
        print("❌ Life Exchange Failed")

if __name__ == "__main__":
    test_rocko_mechanic()
    test_life_exchange_mechanic()
