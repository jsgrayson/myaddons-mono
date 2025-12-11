import requests
from bs4 import BeautifulSoup

url = "https://www.wow-petguide.com/Strategy/22249"
print(f"Fetching {url}...")
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

# Check meta description
meta_desc = soup.find('meta', attrs={'name': 'description'})
if meta_desc:
    print(f"\nMeta Description:")
    print(f"  {meta_desc.get('content', 'N/A')}")

# Check OG description
og_desc = soup.find('meta', attrs={'property': 'og:description'})
if og_desc:
    print(f"\nOG Description:")
    print(f"  {og_desc.get('content', 'N/A')}")

# Check page title
title = soup.find('title')
if title:
    print(f"\nPage Title:")
    print(f"  {title.get_text(strip=True)}")

# Look for strategy description in main content
# Usually in a div or p near the top
strategy_desc = soup.find('div', class_='strategy_description')
if strategy_desc:
    print(f"\nStrategy Description:")
    print(f"  {strategy_desc.get_text(strip=True)}")
