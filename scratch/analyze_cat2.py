from bs4 import BeautifulSoup

with open("E:/Projeler/MeteorGaleri/scratch/category_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

product_urls = set()
# Ticimax usually wraps products in 'div.productItem' or 'div.ProductListContent'
items = soup.find_all('div', class_=lambda c: c and 'Item' in c)
for item in items:
    a = item.find('a', href=True)
    if a:
        href = a['href']
        if href.startswith('/'):
            href = "https://www.meteorgaleri.com" + href
        if 'sepet' not in href.lower() and 'kategori' not in href.lower():
            product_urls.add(href)

print("Found via item class:", list(product_urls)[:5])

# Also look for data-url or specific a tags
details = soup.find_all('a', class_=lambda c: c and 'detailLink' in c)
for a in details:
    href = a.get('href')
    if href:
        if href.startswith('/'):
            href = "https://www.meteorgaleri.com" + href
        product_urls.add(href)
        
print("Found via detailLink:", list(product_urls)[:5])
