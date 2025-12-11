from simulator.battle_state import BattleState, Team, Pet, PetStats, PetFamily, Ability, TurnAction
from simulator.simulator import BattleSimulator
from simulator.special_encounters import SpecialEncounterHandler

def test_gorespine_mechanic():
    print("Testing Gorespine Gore Stacks Mechanic...")
    
    # Create Player Pet (Beast)
    player_pet = Pet(
        species_id=1, 
        name="Player Pet", 
        family=PetFamily.BEAST,
        quality=3,
        stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=300),
        abilities=[Ability(id=1, name="Bite", power=20, accuracy=100, speed=10, cooldown=0, family=PetFamily.BEAST)]
    )
    
    # Create Gorespine (Beast)
    gorespine = Pet(
        species_id=1187, 
        name="Gorespine", 
        family=PetFamily.BEAST,
        quality=3,
        stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250), # Slower
        abilities=[Ability(id=1, name="Bite", power=20, accuracy=100, speed=10, cooldown=0, family=PetFamily.BEAST)]
    )
    
    player_team = Team([player_pet])
    enemy_team = Team([gorespine])
    
    state = BattleState(player_team, enemy_team)
    sim = BattleSimulator()
    
    # Turn 1: Player passes, Gorespine passes
    # Gore Stacks should apply at end of turn
    print("\n--- Turn 1 ---")
    sim.execute_turn(
        state, 
        player_action=TurnAction('player', 'pass'), 
        enemy_action=TurnAction('enemy', 'pass'),
        turn_number=1,
        special_encounter_id='gore_stacks'
    )
    
    # Check buffs
    gore_buff = next((b for b in player_pet.active_buffs if b.source_ability == 99999), None)
    if gore_buff:
        print(f"✅ Gore Buff Applied! Stacks: {gore_buff.stacks}, Magnitude: {gore_buff.magnitude}")
    else:
        print("❌ Gore Buff NOT Applied!")
        return

    # Check damage taken (should be 10 damage from 1 stack)
    # Note: process_end_of_turn applies DoT damage immediately after applying stacks
    # Initial HP was 1000. 
    # Damage = 10 (Base) * 1 (Stack) = 10
    # Beast racial (below 50% HP) doesn't apply yet.
    # Wait, Beast racial is +25% damage dealt below 50% HP.
    # Damage taken modifiers? None.
    print(f"Player HP: {player_pet.stats.current_hp} (Expected ~990)")
    
    # Turn 2: Stacks should increase to 2
    print("\n--- Turn 2 ---")
    sim.execute_turn(
        state, 
        player_action=TurnAction('player', 'pass'), 
        enemy_action=TurnAction('enemy', 'pass'),
        turn_number=2,
        special_encounter_id='gore_stacks'
    )
    
    gore_buff = next((b for b in player_pet.active_buffs if b.source_ability == 99999), None)
    if gore_buff and gore_buff.stacks == 2:
        print(f"✅ Gore Buff Stacked! Stacks: {gore_buff.stacks}, Magnitude: {gore_buff.magnitude}")
    else:
        print(f"❌ Gore Buff Failed to Stack! Stacks: {gore_buff.stacks if gore_buff else 'None'}")

    # Damage should be 20 this turn. Total damage 10 + 20 = 30. HP ~ 970.
    print(f"Player HP: {player_pet.stats.current_hp} (Expected ~970)")

    # Turn 3: Stacks should increase to 3
    print("\n--- Turn 3 ---")
    sim.execute_turn(
        state, 
        player_action=TurnAction('player', 'pass'), 
        enemy_action=TurnAction('enemy', 'pass'),
        turn_number=3,
        special_encounter_id='gore_stacks'
    )
    
    gore_buff = next((b for b in player_pet.active_buffs if b.source_ability == 99999), None)
    if gore_buff and gore_buff.stacks == 3:
        print(f"✅ Gore Buff Stacked! Stacks: {gore_buff.stacks}, Magnitude: {gore_buff.magnitude}")
    else:
        print(f"❌ Gore Buff Failed to Stack! Stacks: {gore_buff.stacks if gore_buff else 'None'}")
        
    print(f"Player HP: {player_pet.stats.current_hp} (Expected ~940)")

    print("\n✅ Gorespine Mechanic Verification Complete!")

if __name__ == "__main__":
    test_gorespine_mechanic()
