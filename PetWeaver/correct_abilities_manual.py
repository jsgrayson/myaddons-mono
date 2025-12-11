import json

def main():
    with open('abilities.json', 'r') as f:
        data = json.load(f)
    
    species_abilities = data.get('species_abilities', {})
    
    # Manual Data
    # Ravenous Prideling (150381)
    # Slot 1: Bite (110), Flurry (360)
    # Slot 2: Crouch (168), Sticky Goo (369)
    # Slot 3: Forboding Curse (1085), Swarm (706)
    species_abilities['150381'] = [110, 360, 168, 369, 1085, 706]
    
    # Widget the Departed (86067)
    # Slot 1: Pounce (359), Spirit Claws (974)
    # Slot 2: Spectral Strike (975), Phantom Strike (976)
    # Slot 3: Prowl (536), Spectral Spine (978)
    species_abilities['86067'] = [359, 974, 975, 976, 536, 978]
    
    data['species_abilities'] = species_abilities
    
    with open('abilities.json', 'w') as f:
        json.dump(data, f, indent=2)
        
    print("✅ Manually corrected abilities for 150381 and 86067")

if __name__ == "__main__":
    main()
