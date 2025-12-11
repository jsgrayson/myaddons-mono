import requests
from bs4 import BeautifulSoup

url = "https://www.wow-petguide.com/Strategy/21512/Rock_Collector"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the tooltip content
tooltip_content = soup.find(id='td_tooltip')
if tooltip_content:
    print("\n=== TOOLTIP CONTENT (SCRIPT) ===")
    print(tooltip_content.get_text().strip())
else:
    print("\n❌ Tooltip content not found")

# Find team structure by searching for a known pet
print("\n\n=== TEAM STRUCTURE SEARCH ===")
pet_name = "Unborn Val'kyr"
pet_element = soup.find(string=lambda text: pet_name in text if text else False)

if pet_element:
    print(f"Found pet: {pet_name}")
    # Print the parent hierarchy to see the container
    parent = pet_element.parent
    for i in range(5):
        print(f"\n--- Parent Level {i} ---")
        print(parent.name)
        print(parent.attrs)
        parent = parent.parent
        if not parent:
            break
else:
    print(f"Pet '{pet_name}' not found in HTML")
