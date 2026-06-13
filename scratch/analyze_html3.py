from bs4 import BeautifulSoup
import re
import sys

# Windows console encoding fix for python
sys.stdout.reconfigure(encoding='utf-8')

with open("E:/Projeler/MeteorGaleri/scratch/product_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Looking for tags containing '30x45'...")
elements = soup.find_all(string=re.compile("30x45", re.IGNORECASE))
for el in elements:
    parent = el.parent
    text = el.strip()
    if len(text) > 200: text = text[:200] + "..."
    print("Found text:", text)
    print("Parent tag:", parent.name, "class:", parent.get('class'), "id:", parent.get('id'), "data-id:", parent.get('data-id'), "data-price:", parent.get('data-price'))
    print("Grandparent tag:", parent.parent.name, "class:", parent.parent.get('class'))

print("\nLet's search for the price element:")
price_divs = soup.find_all('div', class_=re.compile("Fiyat", re.IGNORECASE))
for div in price_divs:
    print("Price div class:", div.get('class'), "text:", div.text.strip())
    
price_spans = soup.find_all('span', class_=re.compile("Fiyat", re.IGNORECASE))
for span in price_spans:
    print("Price span class:", span.get('class'), "text:", span.text.strip())
