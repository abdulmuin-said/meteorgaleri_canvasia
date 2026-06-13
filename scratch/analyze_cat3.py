from bs4 import BeautifulSoup

with open("E:/Projeler/MeteorGaleri/scratch/category_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

urls = set()
for a in soup.find_all('a', href=True):
    href = a['href']
    if len(href) > 20 and '?' not in href and '#' not in href and '.js' not in href and '.css' not in href:
        if not href.startswith('http'):
            href = "https://www.meteorgaleri.com" + href
        if 'meteorgaleri.com' in href and 'kategori' not in href and 'uye' not in href and 'sepet' not in href:
            urls.add(href)

print("Potential product URLs:")
for u in list(urls)[:50]:
    print(u)
