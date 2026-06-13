import requests
import re

url = "https://www.meteorgaleri.com/spor-ve-taraftar-temali-cam-tablo"
response = requests.get(url)

# find all /...-cam-tablo... inside href
links = re.findall(r'href="([^"]+)"', response.text)
products = set()
for link in links:
    if '-' in link and not any(x in link for x in ['css', 'js', 'jpg', 'png', 'svg', 'kategori', 'uye', 'sepet']):
        if link.startswith('/'):
            products.add("https://www.meteorgaleri.com" + link)
            
print("Potential product links:")
for p in list(products)[:20]:
    print(p)
