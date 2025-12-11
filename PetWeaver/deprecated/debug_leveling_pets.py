import requests
from bs4 import BeautifulSoup
import re

# Strategy with leveling pets
url = "https://www.wow-petguide.com/Strategy/22249"
print(f"Fetching {url}...")
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

print("\n--- Extracting Pet Information ---")

# Find the main battle table which contains the 3 team slots
battle_divs = soup.find_all('div', class_=re.compile(r'bt_\d+_'))

for i, div in enumerate(battle_divs[:3]):  # Only first 3 (the team)
    print(f"\nSlot {i+1}:")
    
    # Get the class which indicates pet family (bt_2_Aquatic, bt_2_Mechanical, etc.)
    classes = div.get('class', [])
    family_class = [c for c in classes if c.startswith('bt_') and '_' in c]
    print(f"  Classes: {family_class}")
    
    # Find pet link
    pet_link = div.find('a', href=re.compile(r'/Pet/\d+/'))
    if pet_link:
        pet_name = pet_link.get_text(strip=True)
        pet_id_match = re.search(r'/Pet/(\d+)/', pet_link['href'])
        pet_id = pet_id_match.group(1) if pet_id_match else "Unknown"
        print(f"  Name: {pet_name}")
        print(f"  ID: {pet_id}")
    else:
        # No specific pet link - likely a generic slot
        # Look for any descriptive text
        text = div.get_text(strip=True)
        # Extract just the first part before "Skills:"
        if 'Skills:' in text:
            pet_desc = text.split('Skills:')[0].strip()
        else:
            pet_desc = text[:100]
        print(f"  Generic Pet")
        print(f"  Description: {pet_desc}")
        
        # Check for image which might indicate family
        img = div.find('img', src=re.compile(r'images/pets/'))
        if img:
            print(f"  Image: {img.get('src')}")
