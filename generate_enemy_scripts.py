"""
Enemy AI Script Generator

Analyzes player battle scripts to reverse-engineer enemy ability rotation order
and generates combat-ready enemy AI scripts in the same format as player scripts.

Output: enemy_npc_scripts.json with scripts for each encounter's enemy pets
"""

import json
import re
from collections import defaultdict, Counter

def parse_turn_patterns(variations):
    """Analyze turn-based patterns to infer enemy ability rotation."""
    
    turn_patterns = defaultdict(lambda: {
        'abilities_seen': Counter(),
        'conditions': [],
        'auras_active': Counter()
    })
    
    for var in variations:
        script = var.get('script', '')
        if not script:
            continue
        
        lines = script.split('\\n')
        for line in lines:
            if not line.strip():
                continue
            
            # Look for round-specific conditions
            round_matches = re.findall(r'round\s*[=!<>]+\s*(\d+)', line)
            
            # Look for enemy.round patterns
            enemy_round = re.findall(r'enemy\.round\s*[=!<>]+\s*(\d+)', line)
            
            for round_num in round_matches + enemy_round:
                turn = int(round_num)
                
                # Extract what happens on this turn
                abilities = re.findall(r'enemy\.aura\(([^:]+):(\d+)\)', line)
                for ability_name, ability_id in abilities:
                    turn_patterns[turn]['abilities_seen'][(ability_name, int(ability_id))] += 1
                
                turn_patterns[turn]['conditions'].append(line.strip())
    
    return turn_patterns

def deduce_ability_rotation(turn_patterns, enemy_abilities):
    """Build enemy ability rotation based on turn patterns."""
    
    rotation = []
    
    # Sort turns
    sorted_turns = sorted(turn_patterns.keys())
    
    for turn in sorted_turns:
        data = turn_patterns[turn]
        
        if data['abilities_seen']:
            # Most common ability on this turn
            top_ability = data['abilities_seen'].most_common(1)[0]
            ability_name, ability_id = top_ability[0]
            frequency = top_ability[1]
            
            rotation.append({
                'turn': turn,
                'ability_id': ability_id,
                'ability_name': ability_name,
                'confidence': min(frequency / 10, 1.0),
                'frequency': frequency
            })
    
    return rotation

def generate_enemy_script(rotation, enemy_abilities):
    """Generate enemy AI script in the same format as player scripts."""
    
    script_lines = []
    script_lines.append("# Enemy AI Script (Auto-generated)")
    script_lines.append("")
    
    # Turn-based abilities first
    for entry in sorted(rotation, key=lambda x: x['turn']):
        turn = entry['turn']
        ability_name = entry['ability_name']
        ability_id = entry['ability_id']
        
        script_lines.append(f"use({ability_name}:{ability_id}) [round={turn}]")
    
    # General rotation based on frequency
    general_abilities = [
        (ability_id, info) 
        for ability_id, info in enemy_abilities.items()
        if ability_id not in {r['ability_id'] for r in rotation}
    ]
    
    # Sort by frequency (most common first)
    general_abilities.sort(key=lambda x: -x[1]['frequency'])
    
    # Add top abilities to rotation
    for ability_id, info in general_abilities:
        name = info['most_common_name']
        
        # Skip if name is Unknown
        if name == 'Unknown':
            continue
        
        # Check example conditions for clues
        conditions = info.get('example_conditions', [])
        condition_hints = []
        
        for cond in conditions[:1]:  # Just first condition
            # If player checks "!enemy.aura(...).exists", enemy applies it
            if '!enemy.aura(' in cond and '.exists' in cond:
                condition_hints.append('# Applies debuff/buff')
            elif 'enemy.aura(' in cond and '.exists' in cond:
                condition_hints.append('# Primary rotation ability')
        
        if condition_hints:
            script_lines.append(f"{condition_hints[0]}")
        
        script_lines.append(f"use({name}:{ability_id})")
    
    # If still empty, add placeholder
    if len(script_lines) <= 2:
        script_lines.append("# No specific rotation detected")
        script_lines.append("# Enemy abilities identified but usage pattern unclear")
    
    return "\\n".join(script_lines)

def main():
    print("Loading battle data and enemy abilities...")
    
    with open('variations_with_scripts_final.json', 'r') as f:
        battle_data = json.load(f)
    
    with open('enemy_abilities_database.json', 'r') as f:
        ability_db = json.load(f)
    
    enemy_scripts = {}
    
    print(f"Generating enemy AI scripts for {len(ability_db['encounters'])} encounters...\n")
    
    for encounter_name, encounter_info in ability_db['encounters'].items():
        print(f"Processing: {encounter_name}")
        
        # Get variations for this encounter
        encounter_url = encounter_info['encounter_url']
        if encounter_url not in battle_data:
            print(f"  ⚠️  No battle data found")
            continue
        
        variations = battle_data[encounter_url].get('variations', [])
        enemy_abilities = encounter_info.get('enemy_abilities', {})
        
        if not variations or not enemy_abilities:
            print(f"  ⚠️  Insufficient data")
            continue
        
        # Analyze turn patterns
        turn_patterns = parse_turn_patterns(variations)
        
        # Build rotation
        rotation = deduce_ability_rotation(turn_patterns, enemy_abilities)
        
        # Generate script
        script = generate_enemy_script(rotation, enemy_abilities)
        
        enemy_scripts[encounter_name] = {
            'encounter_url': encounter_url,
            'abilities': enemy_abilities,
            'rotation': rotation,
            'ai_script': script,
            'total_abilities': len(enemy_abilities)
        }
        
        print(f"  ✅ Generated script with {len(rotation)} turn-based abilities")
        if rotation:
            turns = ', '.join(f"T{r['turn']}:{r['ability_name']}" for r in rotation[:3])
            print(f"     Turn breakdown: {turns}")
        print()
    
    # Save
    output = {
        'generated': '2025-11-26',
        'total_encounters': len(enemy_scripts),
        'npc_scripts': enemy_scripts
    }
    
    with open('enemy_npc_scripts.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Generated {len(enemy_scripts)} enemy AI scripts")
    print(f"💾 Saved to: enemy_npc_scripts.json")
    
    # Show sample
    if enemy_scripts:
        sample = list(enemy_scripts.items())[0]
        print(f"\n📜 Sample Script ({sample[0]}):")
        print(sample[1]['ai_script'])

if __name__ == "__main__":
    main()
