import requests
from bs4 import BeautifulSoup
import re, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9',
}

# Download cat HTML and find the ProductListContent, then look inside it
url = "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar"
r = requests.get(url, headers=HEADERS, timeout=20)
html = r.text

# Find .ProductListContent
soup = BeautifulSoup(html, 'html.parser')
plc = soup.select_one('.ProductListContent')
if plc:
    print(f"ProductListContent found, length: {len(str(plc))}")
    # Look for product items inside
    # Save it to file for inspection
    with open("E:/Projeler/MeteorGaleri/scratch/plc_content.html", "w", encoding="utf-8") as f:
        f.write(str(plc))
    print("Saved to plc_content.html")
    
    # Look for any 'a' tags with href that look like product URLs
    links = plc.find_all('a', href=True)
    print(f"Found {len(links)} links inside ProductListContent")
    for a in links[:5]:
        print(f"  href={a['href']} text={a.text.strip()[:40]}")
else:
    print("ProductListContent NOT found")
    # Let's look at all divs with classes
    divs = soup.find_all('div', class_=True)
    classes_with_product = [(d.get('class'), len(str(d))) for d in divs if any('product' in c.lower() or 'urun' in c.lower() for c in d.get('class', []))]
    print(f"Divs with product/urun in class: {len(classes_with_product)}")
    for cls, sz in classes_with_product[:10]:
        print(f"  class={cls}, size={sz}")
