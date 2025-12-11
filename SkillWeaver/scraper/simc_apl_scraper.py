"""
SimC APL Scraper - Fetches Action Priority Lists from SimulationCraft GitHub
"""

import requests
import re

# SimC GitHub profile files - THE WAR WITHIN (11.0+)
SIMC_PROFILE_BASE = "https://raw.githubusercontent.com/simulationcraft/simc/thewarwithin/profiles/TWW1"

# Class/Spec mapping to profile filenames (TWW Season 1)
SIMC_PROFILES = {
    "Warrior": {"Arms": "TWW1_Warrior_Arms.simc", "Fury": "TWW1_Warrior_Fury.simc", "Protection": "TWW1_Warrior_Protection.simc"},
    "DeathKnight": {"Blood": "TWW1_Death_Knight_Blood.simc", "Frost": "TWW1_Death_Knight_Frost.simc", "Unholy": "TWW1_Death_Knight_Unholy.simc"},
    "DemonHunter": {"Havoc": "TWW1_Demon_Hunter_Havoc.simc", "Vengeance": "TWW1_Demon_Hunter_Vengeance.simc"},
    "Druid": {"Balance": "TWW1_Druid_Balance.simc", "Feral": "TWW1_Druid_Feral.simc", "Guardian": "TWW1_Druid_Guardian.simc"},
    "Evoker": {"Devastation": "TWW1_Evoker_Devastation.simc"},
    "Mage": {"Arcane": "TWW1_Mage_Arcane.simc", "Fire": "TWW1_Mage_Fire.simc", "Frost": "TWW1_Mage_Frost.simc"},
    "Monk": {"Brewmaster": "TWW1_Monk_Brewmaster.simc", "Windwalker": "TWW1_Monk_Windwalker.simc"},
    "Paladin": {"Protection": "TWW1_Paladin_Protection.simc", "Retribution": "TWW1_Paladin_Retribution.simc"},
    "Priest": {"Shadow": "TWW1_Priest_Shadow.simc"},
    "Rogue": {"Assassination": "TWW1_Rogue_Assassination.simc", "Outlaw": "TWW1_Rogue_Outlaw.simc", "Subtlety": "TWW1_Rogue_Subtlety.simc"},
    "Shaman": {"Elemental": "TWW1_Shaman_Elemental.simc", "Enhancement": "TWW1_Shaman_Enhancement.simc"},
    "Warlock": {"Affliction": "TWW1_Warlock_Affliction.simc", "Demonology": "TWW1_Warlock_Demonology.simc", "Destruction": "TWW1_Warlock_Destruction.simc"},
}

def fetch_simc_file(class_name, spec_name):
    """Fetch a SimC profile file from GitHub"""
    if class_name not in SIMC_PROFILES or spec_name not in SIMC_PROFILES[class_name]:
        print(f"Error: No profile found for {class_name} {spec_name}")
        return None
    
    filename = SIMC_PROFILES[class_name][spec_name]
    url = f"{SIMC_PROFILE_BASE}/{filename}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_apl_from_simc(simc_content):
    """
    Parse action priority lists from SimC profile content
    
    SimC format:
    actions=spell1
    actions+=/spell2,if=condition
    actions.list_name=spell3
    actions.list_name+=/spell4,if=condition
    
    Returns dict of {list_name: [actions]}
    """
    apls = {}
    current_list = "default"
    
    lines = simc_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Match action list definitions
        # Format: actions=... or actions.name=... or actions+=/... or actions.name+=/...
        if line.startswith('actions'):
            # Extract list name (default if none specified)
            if line.startswith('actions.'):
                # Extract list name: actions.slayer_st+=/execute -> slayer_st
                match = re.match(r'actions\.(\w+)(\+)?=/(.+)', line)
                if match:
                    list_name = match.group(1)
                    action = match.group(3)
                    
                    if list_name not in apls:
                        apls[list_name] = []
                    apls[list_name].append(action)
            else:
                # Default action list: actions=/... or actions+=/...
                match = re.match(r'actions(\+)?=/(.+)', line)
                if match:
                    action = match.group(2)
                    if "default" not in apls:
                        apls["default"] = []
                    apls["default"].append(action)
    
    return apls
def convert_simc_condition_to_lua(condition):
    """
    Convert SimC condition syntax to SkillWeaver Lua syntax
    
    SimC examples:
    - rage>40 → rage > 40
    - buff.avatar.up → buff:Avatar > 0
    - cooldown.warbreaker.remains<10 → cooldown:Warbreaker < 10
    - target.time_to_die>20 → time_to_die > 20
    """
    
    if not condition:
        return "true"
    
    # Remove SimC-specific prefixes
    condition = condition.replace("player.", "")
    condition = condition.replace("target.", "")
    
    # Convert buff syntax: buff.avatar.up → buff:Avatar > 0
    condition = re.sub(r'buff\.(\w+)\.up', r'buff:\1 > 0', condition)
    condition = re.sub(r'buff\.(\w+)\.down', r'buff:\1 == 0', condition)
    condition = re.sub(r'buff\.(\w+)\.remains', r'buff:\1', condition)
    
    # Convert debuff syntax
    condition = re.sub(r'debuff\.(\w+)\.up', r'debuff:\1 > 0', condition)
    condition = re.sub(r'debuff\.(\w+)\.down', r'debuff:\1 == 0', condition)
    
    # Convert cooldown syntax: cooldown.avatar.remains → cooldown:Avatar
    condition = re.sub(r'cooldown\.(\w+)\.remains', r'cooldown:\1', condition)
    condition = re.sub(r'cooldown\.(\w+)\.up', r'cooldown:\1 == 0', condition)
    
    # Convert talent checks: talent.warbreaker.enabled → talent(Warbreaker)
    condition = re.sub(r'talent\.(\w+)\.enabled', r'talent(\1)', condition)
    
    # Convert resource checks
    condition = condition.replace("rage>", "rage > ")
    condition = condition.replace("rage<", "rage < ")
    condition = condition.replace("energy>", "energy > ")
    
    # Convert time_to_die
    condition = condition.replace("time_to_die", "ttd")
    
    # Convert target.health.pct
    condition = re.sub(r'health\.pct<(\d+)', r'target_health < \1', condition)
    
    # Capitalize spell names for consistency
    def capitalize_spell(match):
        spell = match.group(1)
        return spell.title().replace("_", " ")
    
    condition = re.sub(r'buff:(\w+)', lambda m: f'buff:{capitalize_spell(m)}', condition)
    condition = re.sub(r'cooldown:(\w+)', lambda m: f'cooldown:{capitalize_spell(m)}', condition)
    condition = re.sub(r'talent\((\w+)\)', lambda m: f'talent({capitalize_spell(m)})', condition)
    
    return condition

def parse_simc_action(action_str):
    """
    Parse a SimC action line into spell name and conditions
    
    Example: "avatar,if=buff.bloodlust.up|target.time_to_die<20"
    Returns: ("Avatar", "heroism or ttd < 20")
    """
    
    parts = action_str.split(',if=')
    spell = parts[0].strip()
    condition = parts[1] if len(parts) > 1 else ""
    
    # Capitalize spell name
    spell = spell.title().replace("_", " ")
    
    # Convert conditions
    lua_condition = convert_simc_condition_to_lua(condition)
    
    # Convert SimC OR (|) to Lua (or)
    lua_condition = lua_condition.replace("|", " or ")
    lua_condition = lua_condition.replace("&", " and ")
    lua_condition = lua_condition.replace("!", "not ")
    
    return spell, lua_condition

def generate_lua_from_apl(action_list, spec_name, class_name):
    """Generate Lua sequence from SimC APL"""
    
    lua_lines = []
    lua_lines.append(f'-- Auto-generated from SimulationCraft APL')
    lua_lines.append(f'-- Spec: {spec_name}')
    lua_lines.append(f'-- Class: {class_name}')
    lua_lines.append('')
    lua_lines.append('st = {')
    
    for action in action_list:
        spell, condition = parse_simc_action(action)
        lua_lines.append(f'    {{command = "/cast {spell}", conditions = "{condition}"}},')
    
    lua_lines.append('},')
    
    return '\n'.join(lua_lines)

if __name__ == "__main__":
    specs_to_check = [
        ("Warrior", "Arms"), ("Warrior", "Fury"),
        ("Warlock", "Destruction"),
        ("Priest", "Shadow"),
        ("Paladin", "Retribution"),
        ("Druid", "Balance"),
        ("Shaman", "Enhancement"),
        ("Monk", "Windwalker"),
        ("DeathKnight", "Unholy"),
        ("Rogue", "Subtlety")
    ]

    print("Checking SimC profiles for Hero Talent Action Lists...\n")

    for class_name, spec_name in specs_to_check:
        print(f"--- {class_name} {spec_name} ---")
        content = fetch_simc_file(class_name, spec_name)
        
        if content:
            apls = parse_apl_from_simc(content)
            if apls:
                # Filter for potential Hero Talent lists
                hero_lists = [name for name in apls.keys() if name not in ["default", "precombat", "variables"]]
                print(f"Found {len(apls)} lists. Potential Hero/Special lists: {', '.join(hero_lists)}")
                
                # Check for specific Hero Talent keywords
                keywords = ["slayer", "colossus", "thane", "diabolist", "hellcaller", "archon", "voidweaver", "templar", "herald", "elune", "keeper", "storm", "totemic", "shado", "conduit", "sanlayn", "rider", "trickster", "deathstalker"]
                found_keywords = [k for k in keywords if any(k in name.lower() for name in apls.keys())]
                if found_keywords:
                    print(f"-> DETECTED HERO TALENT LOGIC: {', '.join(found_keywords)}")
            else:
                print("No APLs found.")
        else:
            print("Failed to fetch.")
        print("")
