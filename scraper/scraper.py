import requests
from bs4 import BeautifulSoup
import os
import re

# Import class configurations
from generate_config import generate_targets

# Configuration - ALL 39 SPECS WITH ALL 4 MODES (156 total)
TARGETS = generate_targets()

OUTPUT_FILE = "sequences/Generated_Scraped.lua"

print(f"Loaded {len(TARGETS)} class/spec combinations")
print(f"Total modes to scrape: {len(TARGETS) * 4}")

def fetch_page(url):
    print(f"Fetching {url}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            print(f"404 Not Found: {url}")
            return None
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_condition(text):
    text = text.lower()
    conditions = []

    # Resources: Rage
    if "rage" in text:
        m = re.search(r'(?:more than|above|>) (\d+) rage', text)
        if m: conditions.append(f"rage > {m.group(1)}")
        
        m = re.search(r'(?:less than|under|<) (\d+) rage', text)
        if m: conditions.append(f"rage < {m.group(1)}")

    # Resources: Holy Power
    if "holy power" in text:
        # "at 3 holy power" -> >= 3
        m = re.search(r'(?:at|with|have) (\d+) holy power', text)
        if m: conditions.append(f"holypower >= {m.group(1)}")
        
        m = re.search(r'(?:more than|above|>) (\d+) holy power', text)
        if m: conditions.append(f"holypower > {m.group(1)}")

    # Health
    if "health" in text:
        m = re.search(r'(?:less than|under|<) (\d+)%? health', text)
        if m: conditions.append(f"health < {m.group(1)}")

    # Buffs (Simple heuristic: "if Enrage is up")
    # This is risky, so we only do it for very clear patterns
    # "maintain X" -> buff:X
    
    if not conditions:
        return "true"
    return " and ".join(conditions)

def parse_rotation(html):
    if not html: return []
    soup = BeautifulSoup(html, 'html.parser')
    rotation = []
    
    content = soup.find('div', class_='page_content') or soup
    lists = content.find_all(['ol', 'ul']) # Check both ordered and unordered
    
    for ol in lists:
        items = ol.find_all('li')
        if len(items) > 3: 
            for li in items:
                text = li.get_text().strip()
                print(f"DEBUG: {text[:50]}...") # Debug print
                
                # Extract Spell
                match = re.search(r'(?:Cast|Use|Keep up|Maintain)\s+([A-Za-z\s\':]+)', text)
                if match:
                    spell = match.group(1).strip()
                    spell = re.sub(r'\s+\b(if|when|on|until|to)\b.*', '', spell, flags=re.IGNORECASE)
                    
                    if len(spell) > 2 and "Potion" not in spell and "Trinket" not in spell:
                        # Extract Condition from the FULL text
                        cond = parse_condition(text)
                        
                        # Extra Heuristic: "generate Holy Power" -> don't overcap
                        if cond == "true" and "generate holy power" in text.lower():
                            cond = "holypower < 5"
                            
                        rotation.append({"spell": spell, "condition": cond})
            
            if rotation:
                break 
                
    return rotation

def parse_talents(html, source="icy-veins"):
    if not html: return None
    soup = BeautifulSoup(html, 'html.parser')
    
    text = soup.get_text()
    
    if source == "wowhead":
        # Wowhead often has talent strings in data attributes or specific divs
        # Look for talent calculator links or copy buttons
        links = soup.find_all('a', href=re.compile(r'talent-calc'))
        for link in links:
            href = link.get('href', '')
            # Extract from URL parameter
            match = re.search(r'loadout=([A-Za-z0-9+/=]+)', href)
            if match:
                return match.group(1)
        
        # Fallback to text search
        matches = re.findall(r'\b([A-Za-z0-9+/]{40,})\b', text)
    else:
        # Icy Veins
        matches = re.findall(r'\b([A-Za-z0-9+/]{30,})\b', text)
    
    for m in matches:
        if "http" in m or "function" in m or "Guide" in m or "Balance" in m: continue
        return m 
        
    return "TalentStringNotFound"

def generate_lua(targets):
    lua_content = """local ADDON_NAME, SkillWeaver = ...
-- GENERATED FILE - DO NOT EDIT MANUALLY
-- Scraped from Icy Veins & Wowhead

SkillWeaver.Sequences = SkillWeaver.Sequences or {}
SkillWeaver.Talents = SkillWeaver.Talents or {}

"""
    
    for target in targets:
        class_key = f"{target['class']}_{target['spec_id']}"
        
        # Ensure tables exist
        lua_content += f"""
SkillWeaver.Sequences["{class_key}"] = SkillWeaver.Sequences["{class_key}"] or {{}}
SkillWeaver.Talents["{class_key}"] = SkillWeaver.Talents["{class_key}"] or {{}}
"""
        
        for mode_name, urls in target['modes'].items():
            print(f"Processing {target['spec']} - {mode_name}...")
            
            # 1. Rotation
            rot_html = fetch_page(urls.get('rotation'))
            rotation = parse_rotation(rot_html)
            
            if rotation:
                lua_content += f"""
SkillWeaver.Sequences["{class_key}"]["{mode_name}"] = SkillWeaver.Sequences["{class_key}"]["{mode_name}"] or {{}}
SkillWeaver.Sequences["{class_key}"]["{mode_name}"]["Scraped"] = {{
    type = "Priority",
    st = {{
"""
                for item in rotation:
                    lua_content += f'        {{ command = "/cast {item["spell"]}", conditions = "{item["condition"]}" }},\n'
                
                lua_content += """    },
    aoe = {}, 
    steps = {}
}
"""
            else:
                print(f"  No rotation found for {mode_name}")

            # 2. Talents (try Icy Veins first, then Wowhead)
            talent_string = None
            
            tal_html = fetch_page(urls.get('talents'))
            talent_string = parse_talents(tal_html, "icy-veins")
            
            if not talent_string or talent_string == "TalentStringNotFound":
                print(f"  Trying Wowhead for {mode_name}...")
                wh_html = fetch_page(urls.get('wowhead'))
                talent_string = parse_talents(wh_html, "wowhead")
            
            if talent_string and talent_string != "TalentStringNotFound":
                lua_content += f"""
SkillWeaver.Talents["{class_key}"]["{mode_name}"] = SkillWeaver.Talents["{class_key}"]["{mode_name}"] or {{}}
SkillWeaver.Talents["{class_key}"]["{mode_name}"]["Scraped"] = "{talent_string}"
"""
            else:
                 print(f"  No talent string found for {mode_name}")

    with open(OUTPUT_FILE, "w") as f:
        f.write(lua_content)
    print(f"Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_lua(TARGETS)
