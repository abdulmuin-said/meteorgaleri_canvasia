from bs4 import BeautifulSoup
import re

with open("E:/Projeler/MeteorGaleri/scratch/product_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# description is usually in a div with id like divOzetBilgi, uTab1, or class like ulinedTabContent, UrunDetaylari
# Ticimax uses uTab1 for description often.
desc_div = soup.find('div', id='divOzetBilgi')
if desc_div:
    print("Found divOzetBilgi length:", len(str(desc_div)))
else:
    desc_div = soup.find('div', id='uTab1')
    if desc_div:
        print("Found uTab1 length:", len(str(desc_div)))
        print(str(desc_div)[:300])

