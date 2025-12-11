import requests
from bs4 import BeautifulSoup
import re

# Season 3 Dungeons (TWW S3)
CURRENT_SEASON = [
    {"name": "Ara-Kara, City of Echoes", "url": "https://www.icy-veins.com/wow/ara-kara-city-of-echoes-dungeon-guide"},
    {"name": "The Dawnbreaker", "url": "https://www.icy-veins.com/wow/the-dawnbreaker-dungeon-guide"},
    {"name": "Eco-Dome Al'dani", "url": "https://www.icy-veins.com/wow/eco-dome-aldani-dungeon-guide"},
    {"name": "Halls of Atonement", "url": "https://www.icy-veins.com/wow/halls-of-atonement-dungeon-guide"},
    {"name": "Operation: Floodgate", "url": "https://www.icy-veins.com/wow/operation-floodgate-dungeon-guide"},
    {"name": "Priory of the Sacred Flame", "url": "https://www.icy-veins.com/wow/priory-of-the-sacred-flame-dungeon-guide"},
    {"name": "Tazavesh: Streets of Wonder", "url": "https://www.icy-veins.com/wow/tazavesh-the-veiled-market-dungeon-guide"}, # Often one guide for both
    {"name": "Tazavesh: So'leah's Gambit", "url": "https://www.icy-veins.com/wow/tazavesh-the-veiled-market-dungeon-guide"},
]

DUNGEONS = CURRENT_SEASON

# Season 3 Raid
RAIDS = [
    {"name": "Manaforge Omega", "url": "https://www.icy-veins.com/wow/manaforge-omega-raid-guide"},
]

# World Bosses (TWW)
WORLD_BOSSES = [
    {"name": "Khaz Algar (World)", "url": "https://www.icy-veins.com/wow/the-war-within-world-bosses-guide"},
]

OUTPUT_FILE = "skillweaver/db/Interrupts.lua"

def fetch_page(url):
    print(f"Fetching {url}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            print(f"  404 Not Found")
            return None
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  Error: {e}")
        return None

def parse_interrupts(html, content_name):
    if not html:
        return {}
    
    soup = BeautifulSoup(html, 'html.parser')
    interrupts = {}
    
    # Strategy: Look for sections with "Interrupt", "Dispel", "Important"
    # Common patterns:
    # - "Important Interrupts"
    # - "Abilities to Interrupt"
    # - Boss/Trash sections with spell lists
    
    # Find all headings and their following lists
    headings = soup.find_all(['h2', 'h3', 'h4'])
    
    for heading in headings:
        heading_text = heading.get_text().lower()
        
        # Check if this is an interrupt-related section
        if any(word in heading_text for word in ['interrupt', 'kick', 'stop', 'priority']):
            # Find the next list (ul or ol)
            next_list = heading.find_next(['ul', 'ol'])
            if next_list:
                # Extract spell names
                items = next_list.find_all('li')
                for item in items:
                    text = item.get_text().strip()
                    # Look for spell-like text (capitalized words)
                    # Common patterns: "Spell Name - description"
                    match = re.search(r'^([A-Z][A-Za-z\s\']+?)(?:\s*-|\s*:|\s*\()', text)
                    if match:
                        spell = match.group(1).strip()
                        # Categorize as priority (default) or optional
                        is_priority = 'must' in heading_text or 'priority' in heading_text or 'important' in heading_text
                        
                        # Use heading as mob/boss name if available
                        mob_name = content_name
                        parent_heading = heading.find_previous(['h2', 'h3'])
                        if parent_heading:
                            mob_name = parent_heading.get_text().strip()
                        
                        if mob_name not in interrupts:
                            interrupts[mob_name] = {'priority': [], 'optional': []}
                        
                        if is_priority:
                            interrupts[mob_name]['priority'].append(spell)
                        else:
                            interrupts[mob_name]['optional'].append(spell)
    
    return interrupts

def generate_lua(dungeons, raids, world_bosses):
    lua_content = """local ADDON_NAME, SkillWeaver = ...
-- GENERATED FILE - DO NOT EDIT MANUALLY
-- Scraped from Icy Veins Dungeon/Raid Guides

SkillWeaver.Interrupts = SkillWeaver.Interrupts or {}

"""
    
    # Process Dungeons
    lua_content += "-- Mythic+ Dungeons (Season 3)\n"
    for dungeon in dungeons:
        html = fetch_page(dungeon['url'])
        data = parse_interrupts(html, dungeon['name'])
        
        if data:
            print(f"  Found {len(data)} interrupt targets")
            lua_content += f'SkillWeaver.Interrupts["{dungeon["name"]}"] = {{\n'
            
            for mob, spells in data.items():
                if spells['priority'] or spells['optional']:
                    lua_content += f'    ["{mob}"] = {{\n'
                    
                    if spells['priority']:
                        lua_content += '        priority = {'
                        lua_content += ', '.join([f'"{s}"' for s in spells['priority']])
                        lua_content += '},\n'
                    
                    if spells['optional']:
                        lua_content += '        optional = {'
                        lua_content += ', '.join([f'"{s}"' for s in spells['optional']])
                        lua_content += '},\n'
                    
                    lua_content += '    },\n'
            
            lua_content += '}\n\n'
        else:
            print(f"  No interrupts found for {dungeon['name']}")
    
    # Process Raids
    lua_content += "-- Raids\n"
    for raid in raids:
        html = fetch_page(raid['url'])
        data = parse_interrupts(html, raid['name'])
        
        if data:
            print(f"  Found {len(data)} interrupt targets")
            lua_content += f'SkillWeaver.Interrupts["{raid["name"]}"] = {{\n'
            
            for boss, spells in data.items():
                if spells['priority'] or spells['optional']:
                    lua_content += f'    ["{boss}"] = {{\n'
                    
                    if spells['priority']:
                        lua_content += '        priority = {'
                        lua_content += ', '.join([f'"{s}"' for s in spells['priority']])
                        lua_content += '},\n'
                    
                    if spells['optional']:
                        lua_content += '        optional = {'
                        lua_content += ', '.join([f'"{s}"' for s in spells['optional']])
                        lua_content += '},\n'
                    
                    lua_content += '    },\n'
            
            lua_content += '}\n\n'
        else:
            print(f"  No interrupts found for {raid['name']}")

    # Process World Bosses
    lua_content += "-- World Bosses\n"
    for boss in world_bosses:
        html = fetch_page(boss['url'])
        data = parse_interrupts(html, boss['name'])
        
        if data:
            print(f"  Found {len(data)} interrupt targets")
            lua_content += f'SkillWeaver.Interrupts["{boss["name"]}"] = {{\n'
            
            for mob, spells in data.items():
                if spells['priority'] or spells['optional']:
                    lua_content += f'    ["{mob}"] = {{\n'
                    
                    if spells['priority']:
                        lua_content += '        priority = {'
                        lua_content += ', '.join([f'"{s}"' for s in spells['priority']])
                        lua_content += '},\n'
                    
                    if spells['optional']:
                        lua_content += '        optional = {'
                        lua_content += ', '.join([f'"{s}"' for s in spells['optional']])
                        lua_content += '},\n'
                    
                    lua_content += '    },\n'
            
            lua_content += '}\n\n'
        else:
            print(f"  No interrupts found for {boss['name']}")
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(lua_content)
    print(f"\nGenerated {OUTPUT_FILE}")

if __name__ == "__main__":
    print("=== Scraping Season 3 Guides ===")
    generate_lua(DUNGEONS, RAIDS, WORLD_BOSSES)
