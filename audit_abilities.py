
import json
import os

def audit_abilities():
    print("=== Auditing Ability Data ===")
    
    # Load Base Data
    if not os.path.exists('abilities.json'):
        print("ERROR: abilities.json not found!")
        return
        
    with open('abilities.json', 'r') as f:
        base_data = json.load(f)
        base_abilities = base_data.get('abilities', {})
        
    print(f"Base Abilities: {len(base_abilities)}")
    
    # Load Manual Data
    if not os.path.exists('ability_stats_manual.json'):
        print("WARNING: ability_stats_manual.json not found!")
        manual_abilities = {}
    else:
        with open('ability_stats_manual.json', 'r') as f:
            manual_data = json.load(f)
            manual_abilities = manual_data.get('abilities', {})
            
    print(f"Manual Overrides: {len(manual_abilities)}")
    
    # Check 1: Manual abilities missing from Base
    missing_in_base = []
    for aid in manual_abilities:
        if aid not in base_abilities:
            missing_in_base.append(aid)
            
    if missing_in_base:
        print(f"\n[WARNING] {len(missing_in_base)} abilities in Manual but missing in Base (IGNORED by app.py):")
        print(f"IDs: {missing_in_base[:10]}...")
    else:
        print("\n[OK] All manual abilities exist in base data.")
        
    # Check 2: Suspicious Stats in Base (not covered by Manual)
    suspicious = []
    for aid, data in base_abilities.items():
        if aid in manual_abilities:
            continue # Covered
            
        # Check for 0 power/accuracy/cooldown where it might be wrong
        # Note: Some abilities legitimately have 0 power (buffs).
        # But 0 accuracy is usually wrong (unless self-buff?).
        # 0 cooldown is common.
        
        name = data.get('name', 'Unknown')
        power = data.get('power', 0)
        accuracy = data.get('accuracy', 0)
        
        # Heuristic: If it has "Strike", "Bite", "Beam" in name but 0 power?
        damage_keywords = ["Strike", "Bite", "Beam", "Breath", "Claw", "Slash", "Shot", "Blast"]
        if power == 0 and any(k in name for k in damage_keywords):
            suspicious.append(f"{aid} ({name}): 0 Power")
            
        # Heuristic: 0 Accuracy?
        if accuracy == 0:
             suspicious.append(f"{aid} ({name}): 0 Accuracy")
             
    if suspicious:
        print(f"\n[WARNING] {len(suspicious)} suspicious abilities (not in manual):")
        for s in suspicious[:20]:
            print(f"  - {s}")
        if len(suspicious) > 20:
            print(f"  ... and {len(suspicious)-20} more")
    else:
        print("\n[OK] No obvious suspicious stats found.")

if __name__ == "__main__":
    audit_abilities()
