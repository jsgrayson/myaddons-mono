import logging
from simulator import BattleSimulator, BattleState, Team, Pet, Ability, TurnAction, PetStats, PetFamily, PetQuality
from simulator.npc_ai import create_npc_agent
from simulator.smart_agent import SmartAgent

# --- SETUP CONTROL TEAM ---
def get_counter_team():
    # 1. Darkmoon Tonk (Mechanical) -> Wrecks Grizzle (Beast)
    # Stats: Power 325 (Hard Hitter)
    tonk = Pet(
        species_id=1, name="Darkmoon Tonk", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
        stats=PetStats(1400, 1400, 325, 260),
        abilities=[
            Ability(10, "Missile", 20, 100, 0, 0, PetFamily.MECHANICAL),
            Ability(11, "Shock and Awe", 25, 100, 0, 3, PetFamily.MECHANICAL), # Stun
            Ability(12, "Ion Cannon", 70, 100, 0, 5, PetFamily.MECHANICAL) # NUKE
        ]
    )
    
    # 2. Fel Flame (Elemental) -> Wrecks Beakmaster (Mech)
    # Elemental takes 0.67x from Mech, deals 1.0x (Conflagrate hits hard)
    fel = Pet(
        species_id=2, name="Fel Flame", family=PetFamily.ELEMENTAL, quality=PetQuality.RARE,
        stats=PetStats(1400, 1400, 290, 290),
        abilities=[
            Ability(20, "Burn", 20, 100, 0, 0, PetFamily.ELEMENTAL),
            Ability(21, "Scorched Earth", 15, 100, 0, 3, PetFamily.ELEMENTAL), # Weather
            Ability(22, "Conflagrate", 40, 100, 0, 4, PetFamily.ELEMENTAL) # Big Hit
        ]
    )
    
    # 3. Rapana Whelk (Aquatic) -> Wrecks Bloom (Elemental)
    # Aquatic takes 0.67x from Elemental, deals 1.5x to Elemental
    whelk = Pet(
        species_id=3, name="Rapana Whelk", family=PetFamily.AQUATIC, quality=PetQuality.RARE,
        stats=PetStats(1600, 1600, 280, 250),
        abilities=[
            Ability(30, "Ooze Touch", 20, 100, 0, 0, PetFamily.AQUATIC),
            Ability(31, "Acidic Goo", 10, 100, 0, 3, PetFamily.AQUATIC), # DoT + Dmg%
            Ability(32, "Dive", 30, 100, 0, 3, PetFamily.AQUATIC) # Avoidance
        ]
    )
    return Team([tonk, fel, whelk])

def get_major_payne():
    # Stats approx Level 25 Epic
    grizzle = Pet(979, "Grizzle", PetFamily.BEAST, PetQuality.EPIC, PetStats(1650, 1650, 310, 270), [
        Ability(1, "Bash", 25, 100, 0, 0, PetFamily.BEAST),
        Ability(2, "Hibernate", 0, 100, 0, 4, PetFamily.BEAST),
        Ability(3, "Rampage", 35, 95, 0, 0, PetFamily.BEAST)])
    
    beak = Pet(978, "Beakmaster", PetFamily.MECHANICAL, PetQuality.EPIC, PetStats(1550, 1550, 295, 295), [
        Ability(4, "Batter", 10, 100, 0, 0, PetFamily.MECHANICAL),
        Ability(5, "Shock and Awe", 25, 100, 0, 3, PetFamily.MECHANICAL),
        Ability(6, "Wind-Up", 50, 90, 0, 2, PetFamily.MECHANICAL)])
    
    bloom = Pet(977, "Bloom", PetFamily.ELEMENTAL, PetQuality.EPIC, PetStats(1450, 1450, 330, 250), [
        Ability(7, "Lash", 20, 100, 0, 0, PetFamily.ELEMENTAL),
        Ability(8, "Soothing Mists", 0, 100, 0, 3, PetFamily.ELEMENTAL),
        Ability(9, "Entangling Roots", 15, 100, 0, 4, PetFamily.ELEMENTAL)])
    return Team([grizzle, beak, bloom])

# --- GOD SCRIPT (Manual Moves) ---
# We force the exact winning moves.
def god_script(state):
    active = state.player_team.get_active_pet()
    enemy = state.enemy_team.get_active_pet()
    
    if not active.stats.is_alive():
        # Swap Logic
        for i, p in enumerate(state.player_team.pets):
            if p.stats.is_alive(): return TurnAction('player', 'swap', target_pet_index=i)
        return TurnAction('player', 'pass')
        
    # --- STRATEGY FOR TONK vs GRIZZLE ---
    if active.name == "Darkmoon Tonk":
        # 1. Shock and Awe (Stun + Dmg)
        if active.can_use_ability(active.abilities[1]): 
            return TurnAction('player', 'ability', ability=active.abilities[1])
        # 2. Ion Cannon (Nuke)
        if active.can_use_ability(active.abilities[2]) and enemy.stats.current_hp < 900:
             return TurnAction('player', 'ability', ability=active.abilities[2])
        # 3. Missile
        return TurnAction('player', 'ability', ability=active.abilities[0])

    # --- STRATEGY FOR FEL FLAME vs BEAKMASTER ---
    if active.name == "Fel Flame":
        # 1. Scorched Earth (Weather)
        if active.can_use_ability(active.abilities[1]):
             return TurnAction('player', 'ability', ability=active.abilities[1])
        # 2. Conflagrate (Big Hit)
        if active.can_use_ability(active.abilities[2]):
             return TurnAction('player', 'ability', ability=active.abilities[2])
        # 3. Burn
        return TurnAction('player', 'ability', ability=active.abilities[0])

    # --- STRATEGY FOR WHELK vs BLOOM ---
    if active.name == "Rapana Whelk":
        # 1. Acidic Goo (Debuff)
        if active.can_use_ability(active.abilities[1]):
             return TurnAction('player', 'ability', ability=active.abilities[1])
        # 2. Dive (Avoidance)
        if active.can_use_ability(active.abilities[2]):
             return TurnAction('player', 'ability', ability=active.abilities[2])
        # 3. Ooze Touch
        return TurnAction('player', 'ability', ability=active.abilities[0])
        
    return TurnAction('player', 'ability', ability=active.abilities[0])

# --- RUN TEST ---
player_team = get_counter_team()
enemy_team = get_major_payne()

print("--- STARTING CONTROL TEST (God Script vs Major Payne) ---")
print(f"Player Team: {[p.name for p in player_team.pets]}")
print(f"Enemy Team:  {[p.name for p in enemy_team.pets]}")

sim = BattleSimulator()
enemy_ai = create_npc_agent("Major Payne", SmartAgent(1.0).decide)

initial_state = BattleState(player_team, enemy_team, 1)
result = sim.simulate_battle(initial_state, god_script, enemy_ai, max_turns=40, enable_logging=True)

print(f"\nWinner: {result['winner'].upper()}")
print(f"Turns: {result['turns']}")
print("\n--- LOG (Last 15 Lines) ---")
print('\n'.join(result['log'].get_full_log().split('\n')[-15:]))

if result['winner'] == 'player':
    print("\n[SUCCESS] The Simulation Logic is VALID. The Genetic Algorithm is the problem.")
else:
    print("\n[FAILURE] The Simulation Logic is BROKEN. The math/cooldowns are wrong.")
