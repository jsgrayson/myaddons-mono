import requests
from bs4 import BeautifulSoup

url = "https://www.wow-petguide.com/Strategy/21512" 
print(f"Fetching {url}...")
headers = {
    'User-Agent': 'Mozilla/5.0'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

print("\n--- Pet Container Structure ---")

# Find all elements with class 'bt_petdetails'
elements = soup.select(".bt_petdetails")

# Group them by parent to see if we can identify the 3 slots
parents = {}
for el in elements:
    parent = el.parent
    if parent not in parents:
        parents[parent] = []
    parents[parent].append(el)

print(f"Found {len(parents)} parent containers.")

for i, (parent, children) in enumerate(parents.items()):
    print(f"\nParent {i+1} (Tag: {parent.name}, Class: {parent.get('class')}):")
    # print(parent.prettify()[:500])
    
    # Check for images in this parent
    imgs = parent.find_all('img')
    for img in imgs:
        src = img.get('src')
        print(f"  Image: {src}")
        
    # Check for text
    text = parent.get_text(strip=True)[:100]
    print(f"  Text: {text}")
