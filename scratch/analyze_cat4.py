import re

with open("E:/Projeler/MeteorGaleri/scratch/category_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

images = re.findall(r'src=["\']([^"\']*?\.jpg)["\']', html)
print("Found jpg images:")
for img in set(images):
    print(img)

# Let's search for "href" containing any word followed by "-cam-tablo"
links = re.findall(r'href=["\']([^"\']*?-cam-tablo[^"\']*?)["\']', html)
print("\nFound links:")
for l in set(links):
    print(l)
    
# Let's search for "urunAdi" or "Siyah Beyaz" or any known product name
if "aslan" in html.lower():
    print("\n'aslan' is in html!")
else:
    print("\n'aslan' is NOT in html!")
    
# What about "Cam Tablo"?
matches = re.finditer(r'.{0,50}Cam Tablo.{0,50}', html, re.IGNORECASE)
print("\nContexts with 'Cam Tablo':")
for i, m in enumerate(matches):
    if i > 5: break
    print(m.group(0).strip())
