from simulator import BattleSimulator, BattleState, Team, Pet, Ability, TurnAction, PetStats, PetFamily, PetQuality

# Create a simple battle scenario
# Player: Faster, has a strong attack
player_pet = Pet(
    species_id=1, name="Fast Attacker", family=PetFamily.BEAST, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=300),
    abilities=[
        Ability(id=1, name="Smack", power=40, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST)
    ]
)

# Enemy: Slower, has a strong attack
enemy_pet = Pet(
    species_id=2, name="Slow Defender", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
    stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=200),
    abilities=[
        Ability(id=2, name="Zap", power=40, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL)
    ]
)

player_team = Team(pets=[player_pet])
enemy_team = Team(pets=[enemy_pet])

state = BattleState(player_team, enemy_team, turn_number=1)
sim = BattleSimulator()

# Simple scripts: always use ability 1
def script(s):
    active = s.player_team.get_active_pet() if s.player_team.active_pet_index is not None else None
    if active:
        return TurnAction('player', 'ability', ability=active.abilities[0])
    return TurnAction('player', 'pass')

def enemy_script(s):
    active = s.enemy_team.get_active_pet() if s.enemy_team.active_pet_index is not None else None
    if active:
        return TurnAction('enemy', 'ability', ability=active.abilities[0])
    return TurnAction('enemy', 'pass')

print("Starting simulation...")
result = sim.simulate_battle(state, script, enemy_script)

print(f"Winner: {result['winner']}")
print(f"Turns: {result['turns']}")
print("\nBattle Log:")
print(result['log'].get_full_log())

# Verification
# Player is faster (300 vs 200), so Player should hit first.
# Both deal ~300-400 dmg (Power 300 * Ability 40 / 20ish constant).
# Should be over in ~3 turns.
