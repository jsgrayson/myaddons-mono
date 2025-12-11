import json
import os

def get_collection_health():
    """Analyze pet collection for strategic gaps and coverage"""
    try:
        # Pet family mapping
        families = {
            1: "Humanoid", 2: "Dragonkin", 3: "Flying", 4: "Undead",
            5: "Critter", 6: "Magic", 7: "Elemental", 8: "Beast",
            9: "Aquatic", 10: "Mechanical"
        }
        
        # Initialize coverage tracking
        family_coverage = {name: {"owned": 0, "needed": 0, "missing_roles": []} for name in families.values()}
        strategic_value = {}  # pet_id -> number of strategies it unlocks
        
        # Load data
        owned_pets = {}
        if os.path.exists('my_pets.json'):
            print("Loading my_pets.json...")
            with open('my_pets.json', 'r') as f:
                pets_data = json.load(f)
                for pet in pets_data.get('pets', []):
                    # Debug print for structure
                    # print(json.dumps(pet, indent=2)) 
                    
                    # Safe access
                    species = pet.get('species', {})
                    if not species: continue
                    
                    pet_name = species.get('name', 'Unknown')
                    # Handle if name is a dict (localized) or string
                    if isinstance(pet_name, dict):
                        pet_name = pet_name.get('en_US', 'Unknown')
                        
                    stats = pet.get('stats', {})
                    family_id = stats.get('pet_type_id')
                    
                    owned_pets[pet_name] = {
                        'family_id': family_id,
                        'level': pet.get('level', 1),
                        'quality': pet.get('quality', {}).get('name', 'Unknown')
                    }
                    
                    # Count owned by family
                    if family_id in families:
                        family_coverage[families[family_id]]["owned"] += 1
        else:
            print("my_pets.json not found")
        
        print(f"Loaded {len(owned_pets)} owned pets")

        # Analyze strategies to find needed pets
        if os.path.exists('strategies_enhanced.json'):
            print("Loading strategies_enhanced.json...")
            with open('strategies_enhanced.json', 'r') as f:
                strategies = json.load(f)
                
                for encounter in strategies:
                    for team in encounter.get('teams', []):
                        for slot in team.get('loadout', []):
                            for pet_option in slot:
                                pet_name = pet_option.get('name', 'Unknown')
                                pet_id = pet_option.get('id')
                                
                                # Track strategic value
                                if pet_id not in strategic_value:
                                    strategic_value[pet_id] = {"name": pet_name, "unlocks": 0}
                                
                                if pet_name not in owned_pets:
                                    strategic_value[pet_id]["unlocks"] += 1
        else:
            print("strategies_enhanced.json not found")
        
        # Find high-value missing pets
        missing_high_value = sorted(
            [{"id": pid, "name": data["name"], "unlocks": data["unlocks"]} 
             for pid, data in strategic_value.items() if data["unlocks"] > 0],
            key=lambda x: x["unlocks"],
            reverse=True
        )[:10]
        
        # Calculate overall health score (0-100)
        total_families = len(families)
        families_with_pets = sum(1 for f in family_coverage.values() if f["owned"] > 0)
        diversity_score = (families_with_pets / total_families) * 100
        
        # Calculate completeness (based on strategic needs)
        total_strategic_pets = len(strategic_value)
        owned_strategic_pets = sum(1 for pet_id, data in strategic_value.items() if data["unlocks"] == 0)
        completeness_score = (owned_strategic_pets / total_strategic_pets * 100) if total_strategic_pets > 0 else 100
        
        overall_score = (diversity_score * 0.3 + completeness_score * 0.7)
        
        result = {
            "overall_score": round(overall_score, 1),
            "diversity_score": round(diversity_score, 1),
            "completeness_score": round(completeness_score, 1),
            "family_coverage": family_coverage,
            "missing_high_value": missing_high_value,
            "total_owned": len(owned_pets),
            "total_unique_species": len(strategic_value)
        }
        print(json.dumps(result, indent=2))
        return result
        
    except Exception as e:
        print(f"Error in collection health: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    get_collection_health()
