import requests
from bs4 import BeautifulSoup
import re

url = "https://www.wow-petguide.com/Strategy/16/Ashlei" # Ashlei
# Or use a strategy URL from the logs: https://www.wow-petguide.com/Strategy/18465/Right_Twice_a_Day

print(f"Fetching {url}...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1'
}
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.content, 'html.parser')

# Check for enemy team
enemy_section = soup.find('div', class_='enemy-team')
print(f"Enemy section (div.enemy-team): {enemy_section is not None}")

if not enemy_section:
    # Try finding by text
    header = soup.find('h3', string=re.compile(r'Enemy Team', re.I))
    print(f"Enemy header (h3 'Enemy Team'): {header is not None}")
    if header:
        print("Found header, looking for siblings...")
        # Maybe the structure changed?

# Check for pet cards
pet_cards = soup.find_all('div', class_='pet-card')
print(f"Pet cards found: {len(pet_cards)}")

if pet_cards:
    print("First card HTML snippet:")
    print(str(pet_cards[0])[:200])
