import requests
from bs4 import BeautifulSoup
import re

url = "https://www.meteorgaleri.com/spor-ve-taraftar-temali-cam-tablo"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

product_links = set()
for a in soup.find_all('a', href=True):
    href = a['href']
    # Check if a contains an image with class product-image or if it's inside a product div
    if 'class' in a.attrs and any('detailLink' in c.lower() or 'product' in c.lower() or 'image' in c.lower() for c in a['class']):
        if not href.startswith('http'):
            href = "https://www.meteorgaleri.com" + href
        if 'sepet' not in href.lower() and 'kategori' not in href.lower() and 'uye' not in href.lower():
            product_links.add(href)

print("Found links by class:", list(product_links)[:10])

# Another approach: find links with href ending in .html or just containing no slashes after domain (products usually don't have subfolders)
product_links_2 = set()
for a in soup.find_all('a', href=True):
    href = a['href']
    if not href.startswith('http') and href.startswith('/') and len(href.split('/')) == 2:
        # e.g. /fenerbahce-cam-tablo
        if href != '/' and '.' not in href and '?' not in href:
            product_links_2.add("https://www.meteorgaleri.com" + href)

print("Found links by URL pattern:", list(product_links_2)[:10])

