"""
Comprehensive Enemy AI Deduction

Cross-references BOTH team compositions AND scripts to infer enemy movesets.
Analyzes what pets/abilities are chosen to counter specific enemies.
"""

import json
import re
from collections import defaultdict, Counter

def load_pet_abilities():
    """Load pet abilities from your pet database if available."""
    # Placeholder - you may have a pet abilities database
    # For now, we'll infer from usage patterns
    return {}

def analyze_team_patterns(encounter_name, variations):
    """Analyze which pets are commonly used against this encounter."""
    
    team_usage = Counter()
    pet_usage = Counter()
    
    for var in variations:
        team = var.get('team', [])
        for pet_id in team:
            if pet_id != 0:
                pet_usage[pet_id] += 1
        
        # Track full team compositions
        team_tuple = tuple(sorted([p for p in team if p != 0]))
        if team_tuple:
            team_usage[team_tuple] += 1
    
    return {
        'most_used_pets': pet_usage.most_common(10),
        'most_common_teams': team_usage.most_common(5),
        'total_variations': len(variations)
    }

def analyze_defensive_patterns(variations):
    """Identify defensive abilities used, which suggest enemy offense."""
    
    defensive_abilities = {
        284: 'Dodge',
        360: 'Deflection', 
        485: 'Decoy',
        311: 'Dodge',
        125: 'Survival',
        543: 'Prowl',
        242: 'Undead (passive)',
        619: 'Elemental (passive)'
    }
    
    defensive_usage = Counter()
    
    for var in variations:
        script = var.get('script', '')
        for ability_id, ability_name in defensive_abilities.items():
            if f':{ability_id})' in script:
                defensive_usage[ability_name] += 1
    
    return defensive_usage.most_common()

def analyze_speed_patterns(variations):
    """Analyze speed checks to infer enemy speed tier."""
    
    speed_checks = {
        'fast': 0,
        'slow': 0,
        'speed_neutral': 0
    }
    
    for var in variations:
        script = var.get('script', '')
        
        if 'self.speed.fast' in script:
            speed_checks['fast'] += 1
        elif 'self.speed.slow' in script:
            speed_checks['slow'] += 1
    
    return speed_checks

def analyze_hp_breakpoints(variations):
    """Find HP thresholds that matter."""
    
    hp_thresholds = []
    
    for var in variations:
        script = var.get('script', '')
        
        # Find patterns like enemy.hp>700, enemy.hp<=500
        hp_checks = re.findall(r'enemy\.hp\s*([><=]+)\s*(\d+)', script)
        for operator, value in hp_checks:
            hp_thresholds.append((operator, int(value)))
    
    threshold_counter = Counter(hp_thresholds)
    return threshold_counter.most_common(5)

def infer_enemy_from_teams_and_scripts(encounter_url, encounter_data, variations):
    """Combine team and script analysis for comprehensive enemy deduction."""
    
    encounter_name = encounter_data['encounter_name']
    
    # Team analysis
    team_patterns = analyze_team_patterns(encounter_name, variations)
    
    # Script analysis
    defensive_patterns = analyze_defensive_patterns(variations)
    speed_patterns = analyze_speed_patterns(variations)
    hp_breakpoints = analyze_hp_breakpoints(variations)
    
    # Extract enemy abilities from conditions
    enemy_abilities = Counter()
    for var in variations:
        script = var.get('script', '')
        abilities = re.findall(r'enemy\.aura\(([^:]+):(\d+)\)', script)
        for name, ability_id in abilities:
            enemy_abilities[(name, int(ability_id))] += 1
    
    # Build comprehensive analysis
    analysis = {
        'encounter_name': encounter_name,
        'encounter_url': encounter_url,
        'total_variations': len(variations),
        'top_pets_used': team_patterns['most_used_pets'][:5],
        'top_teams': team_patterns['most_common_teams'][:3],
        'enemy_abilities': [
            {'name': name, 'id': ability_id, 'frequency': count}
            for (name, ability_id), count in enemy_abilities.most_common(10)
        ],
        'defensive_counters': [
            {'ability': ability, 'usage': count}
            for ability, count in defensive_patterns[:5]
        ],
        'speed_analysis': speed_patterns,
        'hp_breakpoints': [
            {'operator': op, 'value': val, 'frequency': count}
            for (op, val), count in hp_breakpoints
        ]
    }
    
    # Infer enemy characteristics
    inferences = []
    
    # Speed inference
    if speed_patterns['fast'] > speed_patterns['slow']:
        inferences.append({
            'type': 'speed',
            'inference': 'Enemy is SLOW (players check self.speed.fast)',
            'confidence': min(speed_patterns['fast'] / 20, 1.0)
        })
    elif speed_patterns['slow'] > speed_patterns['fast']:
        inferences.append({
            'type': 'speed',
            'inference': 'Enemy is FAST (players check self.speed.slow)',
            'confidence': min(speed_patterns['slow'] / 20, 1.0)
        })
    
    # Defensive patterns suggest offense
    if defensive_patterns:
        top_defense = defensive_patterns[0]
        inferences.append({
            'type': 'offense',
            'inference': f"Enemy has big hits (players use {top_defense[0]} {top_defense[1]} times)",
            'confidence': min(top_defense[1] / 30, 1.0)
        })
    
    # HP breakpoints suggest burst windows
    if hp_breakpoints:
        for (op, val), count in hp_breakpoints[:2]:
            inferences.append({
                'type': 'mechanics',
                'inference': f"Important HP threshold at {val} HP ({op})",
                'confidence': min(count / 20, 1.0)
            })
    
    analysis['inferences'] = inferences
    
    return analysis

def main():
    print("Loading comprehensive battle data...")
    
    with open('variations_with_scripts_final.json', 'r') as f:
        battle_data = json.load(f)
    
    print(f"Analyzing {len(battle_data)} encounters with team + script cross-reference...\n")
    
    comprehensive_analysis = {}
    
    count = 0
    for encounter_url, encounter_data in battle_data.items():
        variations = encounter_data.get('variations', [])
        
        if not variations:
            continue
        
        # Only analyze encounters with scripts
        has_scripts = any(var.get('script', '').strip() for var in variations)
        if not has_scripts:
            continue
        
        analysis = infer_enemy_from_teams_and_scripts(encounter_url, encounter_data, variations)
        comprehensive_analysis[encounter_data['encounter_name']] = analysis
        
        count += 1
        if count <= 5:  # Show progress
            print(f"Analyzed: {encounter_data['encounter_name']}")
            print(f"  Variations: {len(variations)}")
            print(f"  Enemy abilities: {len(analysis['enemy_abilities'])}")
            print(f"  Inferences: {len(analysis['inferences'])}")
            print()
    
    # Save comprehensive analysis
    output = {
        'generated': '2025-11-26',
        'analysis_type': 'teams_and_scripts_combined',
        'total_encounters': len(comprehensive_analysis),
        'encounters': comprehensive_analysis
    }
    
    with open('comprehensive_enemy_analysis.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Comprehensive analysis complete!")
    print(f"📊 Analyzed {len(comprehensive_analysis)} encounters")
    print(f"💾 Saved to: comprehensive_enemy_analysis.json")

if __name__ == "__main__":
    main()
