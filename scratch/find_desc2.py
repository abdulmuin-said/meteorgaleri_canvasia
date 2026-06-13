from bs4 import BeautifulSoup
import re

with open("E:/Projeler/MeteorGaleri/scratch/product_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Search for common description phrases
elems = soup.find_all(string=re.compile("kalınlığında|Kırılmaya karşı|montaj", re.IGNORECASE))
for el in elems:
    parent = el.parent
    print("Found text in:", parent.name, "id:", parent.get('id'), "class:", parent.get('class'))
    print("Grandparent:", parent.parent.name, "id:", parent.parent.get('id'), "class:", parent.parent.get('class'))
    
# Let's also look at all tabs
tabs = soup.find_all('div', class_=re.compile("tab", re.IGNORECASE))
for tab in tabs:
    if len(str(tab)) > 100:
        print("Tab id:", tab.get('id'), "class:", tab.get('class'), "len:", len(str(tab)))
