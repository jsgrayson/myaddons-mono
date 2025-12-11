import simc_apl_scraper as scraper

def generate_reference_lua():
    specs = [
        ("Warrior", "Arms", ["slayer", "colossus"]),
        ("Warrior", "Fury", ["slayer", "thane"]),
        ("Warlock", "Destruction", ["diabolist", "hellcaller"]),
        ("Priest", "Shadow", ["archon", "voidweaver"]),
        ("Paladin", "Retribution", []), # Embedded
        ("Druid", "Balance", ["kotg", "elune"]), # Keeper, Elune
        ("Shaman", "Enhancement", ["totemic", "storm"]),
        ("Monk", "Windwalker", ["shado", "conduit"]),
        ("DeathKnight", "Unholy", ["san", "rider"]),
        ("Rogue", "Subtlety", ["trickster", "deathstalker"])
    ]

    output_lua = ["-- Reference SimC Rotations (Auto-Generated)", "local SkillWeaver = ...", "SkillWeaver.Reference = {}"]

    for class_name, spec_name, hero_keywords in specs:
        print(f"Processing {class_name} {spec_name}...")
        content = scraper.fetch_simc_file(class_name, spec_name)
        if not content:
            print(f"  Failed to fetch content for {class_name} {spec_name}")
            continue

        apls = scraper.parse_apl_from_simc(content)
        if not apls:
            print(f"  Failed to parse APLs for {class_name} {spec_name}")
            continue

        spec_key = f"{class_name}_{spec_name}"
        output_lua.append(f'\nSkillWeaver.Reference["{spec_key}"] = {{')

        # 1. Try to find specific Hero Talent lists
        found_hero_lists = False
        for keyword in hero_keywords:
            # Find lists matching the keyword (e.g., "slayer_st", "slayer_aoe")
            matching_lists = [name for name in apls.keys() if keyword in name.lower()]
            
            if matching_lists:
                found_hero_lists = True
                output_lua.append(f'    ["{keyword.capitalize()}"] = {{')
                for list_name in matching_lists:
                    actions = apls[list_name]
                    print(f"  Found list '{list_name}' with {len(actions)} actions")
                    output_lua.append(f'        -- SimC List: {list_name} ({len(actions)} actions)')
                    
                    # Generate Lua lines directly here to avoid filtering issues
                    for action in actions:
                        spell, condition = scraper.parse_simc_action(action)
                        output_lua.append(f'        {{ command = "/cast {spell}", conditions = "{condition}" }},')
                        
                output_lua.append('    },')

        # 2. If no specific lists found, or to provide a baseline, dump 'default' or 'main' lists
        output_lua.append('    ["Default_Main"] = {')
        # Prioritize 'default', 'main', 'st', 'aoe' lists
        priority_lists = ["default", "main", "st", "aoe", "cooldowns", "generators", "finishers"]
        for list_name in priority_lists:
            if list_name in apls:
                actions = apls[list_name]
                print(f"  Found list '{list_name}' with {len(actions)} actions")
                output_lua.append(f'        -- SimC List: {list_name} ({len(actions)} actions)')
                for action in actions:
                    spell, condition = scraper.parse_simc_action(action)
                    output_lua.append(f'        {{ command = "/cast {spell}", conditions = "{condition}" }},')
        output_lua.append('    },')

        output_lua.append('}')

    with open("../sequences/Reference_SimC.lua", "w") as f:
        f.write("\n".join(output_lua))
    print("Done! Generated ../sequences/Reference_SimC.lua")

if __name__ == "__main__":
    generate_reference_lua()
