from simulator import BattleSimulator, BattleState, Team, Pet, Ability, TurnAction, PetStats, PetFamily, PetQuality

# --- Enemy Team (Squirt) ---
deebs = Pet(
    species_id=1934, name="Deebs", family=PetFamily.MAGIC, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1546, current_hp=1546, power=273, speed=273),
    abilities=[
        Ability(122, "Water Jet", 20, 100, 0, 0, PetFamily.ELEMENTAL),
        Ability(110, "Pump", 13, 100, 0, 3, PetFamily.AQUATIC),
        Ability(120, "Whirlpool", 30, 100, 0, 4, PetFamily.AQUATIC)
    ]
)
tyri = Pet(
    species_id=1935, name="Tyri", family=PetFamily.HUMANOID, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1546, current_hp=1546, power=273, speed=273),
    abilities=[
        Ability(115, "Tail Sweep", 18, 100, 0, 0, PetFamily.DRAGONKIN),
        Ability(593, "Moonfire", 30, 100, 0, 0, PetFamily.MAGIC),
        Ability(489, "Lift-Off", 40, 100, 0, 4, PetFamily.FLYING)
    ]
)
puzzle = Pet(
    species_id=1936, name="Puzzle", family=PetFamily.HUMANOID, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1546, current_hp=1546, power=273, speed=273),
    abilities=[
        Ability(136, "Build Turret", 30, 100, 0, 0, PetFamily.MECHANICAL),
        Ability(406, "Batter", 28, 100, 0, 0, PetFamily.MECHANICAL),
        Ability(125, "Dodge", 0, 100, 0, 4, PetFamily.HUMANOID)
    ]
)
enemy_team = Team(pets=[deebs, tyri, puzzle])

# --- Player Team (Strategy) ---
# Ravenous Prideling (Humanoid)
prideling = Pet(
    species_id=150381, name="Ravenous Prideling", family=PetFamily.HUMANOID, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1400, current_hp=1400, power=300, speed=280),
    abilities=[
        Ability(2356, "Void Nova", 25, 100, 0, 0, PetFamily.MAGIC), 
        Ability(447, "Corrosion", 10, 100, 0, 0, PetFamily.MAGIC, 
                stat_buffs={'damage_taken': (1.5, 2)}), # Simulating debuff
        Ability(1954, "Poison Protocol", 30, 100, 0, 0, PetFamily.ELEMENTAL)
    ]
)
# Widget the Departed (Undead)
widget = Pet(
    species_id=86067, name="Widget", family=PetFamily.UNDEAD, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1400, current_hp=1400, power=300, speed=280),
    abilities=[
        Ability(1055, "Breath of Sorrow", 20, 100, 0, 0, PetFamily.UNDEAD),
        Ability(593, "Surge of Power", 60, 100, 0, 3, PetFamily.MAGIC),
        Ability(1056, "Seethe", 0, 100, 0, 3, PetFamily.UNDEAD)
    ]
)
# Wrathling (Magic)
wrathling = Pet(
    species_id=171118, name="Wrathling", family=PetFamily.MAGIC, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1400, current_hp=1400, power=300, speed=280),
    abilities=[
        Ability(1, "Filler", 20, 100, 0, 0, PetFamily.MAGIC),
        Ability(2, "Filler", 20, 100, 0, 0, PetFamily.MAGIC),
        Ability(3, "Filler", 20, 100, 0, 0, PetFamily.MAGIC)
    ]
)
player_team = Team(pets=[prideling, widget, wrathling])

# --- Agents ---
def player_agent(state: BattleState) -> TurnAction:
    # Hardcoded sequence based on strategy
    turn = state.turn_number
    active = state.player_team.get_active_pet()
    
    if not active:
        print(f"Turn {turn}: Player has no active pet!")
        return TurnAction('player', 'pass')
        
    # print(f"DEBUG: Player Active: {active.name}, HP: {active.stats.current_hp}, Alive: {active.stats.is_alive()}")

    # Check if active pet is dead -> Must Swap
    if not active.stats.is_alive():
        # Find next living pet
        for i, p in enumerate(state.player_team.pets):
            if p.stats.is_alive():
                print(f"Turn {turn}: Active pet dead, swapping to {p.name} ({i})")
                return TurnAction('player', 'swap', target_pet_index=i)
        return TurnAction('player', 'pass') # No one left
    
    if active.name == "Ravenous Prideling":
        if turn == 1: return TurnAction('player', 'ability', ability=active.abilities[0]) # Void Nova
        if turn == 2: return TurnAction('player', 'ability', ability=active.abilities[1]) # Corrosion
        if turn == 3: return TurnAction('player', 'ability', ability=active.abilities[2]) # Poison Protocol
        if turn == 4: return TurnAction('player', 'ability', ability=active.abilities[1]) # Corrosion
        
        return TurnAction('player', 'ability', ability=active.abilities[0])

    if active.name == "Widget":
        if active.can_use_ability(active.abilities[0]):
             return TurnAction('player', 'ability', ability=active.abilities[0])
        if active.can_use_ability(active.abilities[1]):
             return TurnAction('player', 'ability', ability=active.abilities[1])
             
        return TurnAction('player', 'ability', ability=active.abilities[0])

    return TurnAction('player', 'ability', ability=active.abilities[0])

def enemy_agent(state: BattleState) -> TurnAction:
    active = state.enemy_team.get_active_pet()
    
    # Swap if dead
    if active and not active.stats.is_alive():
        for i, p in enumerate(state.enemy_team.pets):
            if p.stats.is_alive():
                print(f"Turn {state.turn_number}: Enemy pet dead, swapping to {p.name} ({i})")
                return TurnAction('enemy', 'swap', target_pet_index=i)
    
    if active:
        for ab in active.abilities:
            if active.can_use_ability(ab):
                # print(f"Enemy using {ab.name}")
                return TurnAction('enemy', 'ability', ability=ab)
    print("Enemy passing!")
    return TurnAction('enemy', 'pass')

# --- Run Simulation ---
sim = BattleSimulator()
state = BattleState(player_team, enemy_team, turn_number=1)
print("Starting Squirt Simulation...")
result = sim.simulate_battle(state, player_agent, enemy_agent, max_turns=50)

print(f"Winner: {result['winner']}")
print(f"Turns: {result['turns']}")
print(f"Player Survivors: {len([p for p in result['final_state'].player_team.pets if p.stats.current_hp > 0])}")
print(f"Enemy Survivors: {len([p for p in result['final_state'].enemy_team.pets if p.stats.current_hp > 0])}")

print("\n--- Battle Events ---")
for event in result['events']:
    print(event)
