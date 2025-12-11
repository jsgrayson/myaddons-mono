import json

def generate_missing_report():
    with open('encounters_full.json', 'r') as f:
        encounters = json.load(f)
        
    missing_count = 0
    report_lines = []
    
    report_lines.append("MISSING ABILITIES REPORT")
    report_lines.append("========================")
    
    for tamer in encounters:
        tamer_missing = []
        for pet in tamer['pets']:
            if pet.get('missing_abilities', False):
                tamer_missing.append(f"  - Species {pet['species_id']} (Model {pet['model_id']})")
                missing_count += 1
        
        if tamer_missing:
            report_lines.append(f"\n{tamer['name']}:")
            report_lines.extend(tamer_missing)
            
    report_lines.append(f"\nTotal Missing: {missing_count}")
    
    with open('missing_pets_report.txt', 'w') as f:
        f.write('\n'.join(report_lines))
        
    print(f"Report saved to missing_pets_report.txt. Total missing: {missing_count}")

if __name__ == "__main__":
    generate_missing_report()
