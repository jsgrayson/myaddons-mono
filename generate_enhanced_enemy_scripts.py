"""
Enhanced Enemy AI Script Generator

Uses comprehensive team + script analysis to generate detailed enemy AI scripts
with inferred abilities, speed, mechanics, and HP-based behaviors.
"""

import json
import re
from collections import Counter

def generate_enhanced_enemy_script(encounter_data):
    """Generate detailed enemy AI script using comprehensive analysis."""
    
    name = encounter_data['encounter_name']
    abilities = encounter_data.get('enemy_abilities', [])
    inferences = encounter_data.get('inferences', [])
    hp_breakpoints = encounter_data.get('hp_breakpoints', [])
    speed_analysis = encounter_data.get('speed_analysis', {})
    
    script_lines = []
    script_lines.append(f"# Enemy AI: {name}")
    script_lines.append("# Auto-generated from comprehensive analysis")
    script_lines.append("")
    
    # Add metadata comments
    if inferences:
        script_lines.append("# Characteristics:")
        for inf in inferences:
            conf = int(inf['confidence'] * 100)
            script_lines.append(f"#   [{conf}%] {inf['inference']}")
        script_lines.append("")
    
    # Priority abilities (high frequency = opener/spam)
    if abilities:
        priority = [a for a in abilities if a['frequency'] > 50]
        if priority:
            script_lines.append("# Priority abilities (high usage)")
            for ability in priority[:2]:
                script_lines.append(f"use({ability['name']}:{ability['id']}) [round=1]")
            script_lines.append("")
        
        # HP-based conditionals
        if hp_breakpoints:
            script_lines.append("# HP-based abilities")
            for bp in hp_breakpoints[:2]:
                op = bp['operator']
                val = bp['value']
                
                # Find an ability to use at this HP
                if abilities:
                    ability = abilities[0]  # Use most common
                    script_lines.append(f"use({ability['name']}:{ability['id']}) [enemy.hp{op}{val}]")
            script_lines.append("")
        
        # General rotation
        script_lines.append("# General rotation")
        for ability in abilities[:5]:  # Top 5 abilities
            freq_comment = f"  # Used {ability['frequency']} times"
            script_lines.append(f"use({ability['name']}:{ability['id']}){freq_comment}")
    
    # If no abilities detected, mark as incomplete
    if not abilities:
        script_lines.append("# No abilities detected from analysis")
        script_lines.append("# This enemy may need manual scripting")
    
    return "\\n".join(script_lines)

def main():
    print("Loading comprehensive analysis...")
    
    with open('comprehensive_enemy_analysis.json', 'r') as f:
        analysis_data = json.load(f)
    
    print(f"Generating enhanced AI scripts for {analysis_data['total_encounters']} encounters...\n")
    
    enhanced_scripts = {}
    script_count = 0
    
    for encounter_name, encounter_data in analysis_data['encounters'].items():
        # Generate script
        script = generate_enhanced_enemy_script(encounter_data)
        
        enhanced_scripts[encounter_name] = {
            'encounter_url': encounter_data['encounter_url'],
            'total_variations': encounter_data['total_variations'],
            'abilities_count': len(encounter_data.get('enemy_abilities', [])),
            'inferences_count': len(encounter_data.get('inferences', [])),
            'ai_script': script
        }
        
        if encounter_data.get('enemy_abilities'):
            script_count += 1
    
    # Save
    output = {
        'generated': '2025-11-26',
        'analysis_source': 'comprehensive_team_and_script_analysis',
        'total_encounters': len(enhanced_scripts),
        'encounters_with_scripts': script_count,
        'npc_scripts': enhanced_scripts
    }
    
    with open('enhanced_enemy_npc_scripts.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Generated enhanced AI scripts!")
    print(f"   Total encounters: {len(enhanced_scripts)}")
    print(f"   With AI scripts: {script_count}")
    print(f"   Coverage: {script_count/len(enhanced_scripts)*100:.1f}%")
    print(f"\n💾 Saved to: enhanced_enemy_npc_scripts.json")
    
    # Show sample
    print(f"\n📜 Sample Enhanced Scripts:\n")
    samples = ['Miniature Army', 'here', 'Briarpaw']
    for name in samples:
        if name in enhanced_scripts:
            print(f"{'='*60}")
            print(enhanced_scripts[name]['ai_script'].replace('\\n', '\n'))
            print()

if __name__ == "__main__":
    main()
