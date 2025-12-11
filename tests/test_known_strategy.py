import json
import sys
from simulator import BattleSimulator, BattleState, Team, Pet, Ability, PetFamily, PetQuality, PetStats, TurnAction

# --- 1. Define Teams ---
def create_boss_team():
    grizzle = Pet(979, "Grizzle (Boss)", PetFamily.BEAST, PetQuality.EPIC, PetStats(1700, 1700, 320, 270), [
        Ability(1, "Bash", 25, 100, 0, 0, PetFamily.BEAST),
        Ability(2, "Hibernate", 0, 100, 0, 4, PetFamily.BEAST),
        Ability(3, "Rampage", 35, 95, 0, 0, PetFamily.BEAST)])
    beakmaster = Pet(978, "Beakmaster (Boss)", PetFamily.MECHANICAL, PetQuality.EPIC, PetStats(1500, 1500, 290, 300), [
        Ability(4, "Batter", 10, 100, 0, 0, PetFamily.MECHANICAL),
        Ability(5, "Shock and Awe", 25, 100, 0, 3, PetFamily.MECHANICAL),
        Ability(6, "Wind-Up", 50, 90, 0, 2, PetFamily.MECHANICAL)])
    bloom = Pet(977, "Bloom (Boss)", PetFamily.ELEMENTAL, PetQuality.EPIC, PetStats(1400, 1400, 340, 250), [
        Ability(7, "Lash", 20, 100, 0, 0, PetFamily.ELEMENTAL),
        Ability(8, "Soothing Mists", 0, 100, 0, 3, PetFamily.ELEMENTAL),
        Ability(9, "Entangling Roots", 15, 100, 0, 4, PetFamily.ELEMENTAL)])
    return Team([grizzle, beakmaster, bloom])

def create_counter_team():
    # 1. Iron Starlette (Mech > Beast)
    # Wind-Up (459), Supercharge, Powerball
    starlette = Pet(1155, "Iron Starlette", PetFamily.MECHANICAL, PetQuality.RARE, PetStats(1400, 1400, 341, 244), [
        Ability(459, "Wind-Up", 30, 100, 0, 0, PetFamily.MECHANICAL), 
        Ability(208, "Supercharge", 0, 100, 0, 3, PetFamily.MECHANICAL, stat_buffs={'power': (2.25, 1)}), # +125% damage for 1 turn
        Ability(566, "Powerball", 15, 100, 0, 0, PetFamily.MECHANICAL)
    ])
    
    # 2. Fel Flame (Elemental > Mech)
    # Burn, Scorched Earth, Conflagrate
    felflame = Pet(845, "Fel Flame", PetFamily.ELEMENTAL, PetQuality.RARE, PetStats(1481, 1481, 276, 276), [
        Ability(113, "Burn", 20, 100, 0, 0, PetFamily.ELEMENTAL),
        Ability(172, "Scorched Earth", 15, 100, 0, 5, PetFamily.ELEMENTAL),
        Ability(179, "Conflagrate", 40, 100, 0, 4, PetFamily.ELEMENTAL)
    ])
    
    # 3. Emperor Crab (Aquatic > Elemental)
    # Snap, Renewing Mists, Whirlpool
    crab = Pet(1194, "Emperor Crab", PetFamily.AQUATIC, PetQuality.RARE, PetStats(1806, 1806, 357, 211), [
        Ability(116, "Snap", 20, 100, 0, 0, PetFamily.AQUATIC),
        Ability(231, "Renewing Mists", 15, 100, 0, 3, PetFamily.AQUATIC, is_heal=False, effect_type='hot', dot_duration=3), # HoT
        Ability(513, "Whirlpool", 30, 100, 0, 3, PetFamily.AQUATIC)
    ])
    
    return Team([starlette, felflame, crab])

# --- 2. Define Strategy Script ---
def player_script(state: BattleState) -> TurnAction:
    active = state.player_team.get_active_pet()
    if not active or not active.stats.is_alive():
        # Swap logic
        for i, p in enumerate(state.player_team.pets):
            if p.stats.is_alive(): return TurnAction('player', 'swap', target_pet_index=i)
        return TurnAction('player', 'pass')

    # Iron Starlette Logic
    if active.name == "Iron Starlette":
        # Combo: Wind-Up -> Supercharge -> Wind-Up (Boom)
        windup = active.abilities[0]
        supercharge = active.abilities[1]
        
        # If Wind-Up is primed (has buff), unleash it!
        # Note: Simulator might not track "primed" state explicitly in ability object, 
        # but usually Wind-Up applies a buff to self.
        is_primed = any(b.name == "Wind-Up" for b in active.active_buffs)
        
        if is_primed:
             if active.can_use_ability(windup): return TurnAction('player', 'ability', ability=windup)
        
        if active.can_use_ability(supercharge): return TurnAction('player', 'ability', ability=supercharge)
        if active.can_use_ability(windup): return TurnAction('player', 'ability', ability=windup)
        
        return TurnAction('player', 'ability', ability=active.abilities[2]) # Powerball filler

    # Fel Flame Logic
    if active.name == "Fel Flame":
        conflag = active.abilities[2]
        scorch = active.abilities[1]
        burn = active.abilities[0]
        
        # Conflag if target burning (Scorched Earth applies weather, or Burn)
        # Simplified: Just Scorch -> Conflag -> Burn spam
        if active.can_use_ability(scorch): return TurnAction('player', 'ability', ability=scorch)
        if active.can_use_ability(conflag): return TurnAction('player', 'ability', ability=conflag)
        return TurnAction('player', 'ability', ability=burn)

    # Emperor Crab Logic
    if active.name == "Emperor Crab":
        whirlpool = active.abilities[2]
        heal = active.abilities[1]
        snap = active.abilities[0]
        
        if active.can_use_ability(whirlpool): return TurnAction('player', 'ability', ability=whirlpool)
        if active.can_use_ability(heal) and active.stats.current_hp < active.stats.max_hp * 0.7: 
            return TurnAction('player', 'ability', ability=heal)
        return TurnAction('player', 'ability', ability=snap)

    return TurnAction('player', 'pass')

# --- 3. Run Simulation ---
def run_test():
    print("Initializing Known Strategy Test...")
    boss = create_boss_team()
    player = create_counter_team()
    
    print(f"Player Team: {[p.name for p in player.pets]}")
    print(f"Boss Team: {[p.name for p in boss.pets]}")
    
    sim = BattleSimulator()
    
    # Create simple enemy AI (Random/Smart)
    from simulator.smart_agent import SmartAgent
    enemy_ai = SmartAgent(1.0).decide
    
    state = BattleState(player, boss, 1)
    
    print("\nStarting Simulation...")
    result = sim.simulate_battle(state, player_script, enemy_ai, max_turns=50, enable_logging=True)
    
    print(f"\nWinner: {result['winner'].upper()}")
    print(f"Turns: {result['turns']}")
    print(f"Remaining Player HP: {sum(p.stats.current_hp for p in result['final_state'].player_team.pets)}")
    
    # Print Log Summary
    print("\n--- Battle Log ---")
    print(result['log'].get_full_log())
    
    print("\n--- Event Log ---")
    for event in result['events']:
        print(event)

if __name__ == "__main__":
    run_test()
