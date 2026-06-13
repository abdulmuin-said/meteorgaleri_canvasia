import requests
from bs4 import BeautifulSoup
import re

url = "https://www.meteorgaleri.com/spor-ve-taraftar-temali-cam-tablo"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

product_links = set()
for a in soup.find_all('a', href=True):
    href = a['href']
    # product links usually don't have '/' at the end, and they are long, or they are inside a product item container
    # let's look for elements with class containing 'product', 'urun', 'Item'
    pass

# let's just find product containers
containers = soup.find_all('div', class_=re.compile("product|urun", re.IGNORECASE))
for c in containers:
    a = c.find('a', href=True)
    if a:
        href = a['href']
        if not href.startswith('http'):
            href = "https://www.meteorgaleri.com" + href
        if 'sepet' not in href.lower() and 'kategori' not in href.lower():
            product_links.add(href)

print("Found links:", list(product_links)[:10])
