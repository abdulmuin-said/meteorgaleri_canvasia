import requests
from bs4 import BeautifulSoup
import re
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
}

TARGET_CATEGORIES = {
    'osmanli-ve-tugra-temali-cam-tablo': 'Osmanlı ve Tuğra Temalı',
    'spor-ve-taraftar-temali-cam-tablo': 'Spor ve Taraftar',
    'farkli-tablolar1': 'Farklı Tablolar',
    'dini-hat-temali-cam-tablolar': 'Dini/Hat Temalı',
    'cicekli-dekoratif-cam-tablolar': 'Çiçekli Dekoratif',
    'mutfak-cam-tablolar': 'Mutfak',
    'soyut-cam-tablolar': 'Soyut',
    'ataturk-cam-tablolar': 'Atatürk',
    'manzara-cam-tablolar': 'Manzara',
    'hayvan-temali-cam-tablolar': 'Hayvan Temalı',
}

# Also try the main Cam Tablolar category
all_cats = {
    'cam-tablolar': 'Cam Tablolar (Ana)',
    **TARGET_CATEGORIES
}

def count_products_in_category(slug, name):
    """Try to count products via Ticimax's product list endpoint."""
    # Try the JSON API first
    product_urls = []
    page = 1
    
    while True:
        url = f"https://www.meteorgaleri.com/{slug}?sayfa={page}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                break
            
            # Look for product count in the HTML
            html = r.text
            
            # Ticimax stores product list data in a JS variable
            match = re.search(r'"totalProductCount"\s*:\s*(\d+)', html)
            if match:
                total = int(match.group(1))
                print(f"  [{name}]: {total} ürün (JSON'dan)")
                return total
            
            # Another pattern
            match = re.search(r'"UrunSayisi"\s*:\s*(\d+)', html)
            if match:
                total = int(match.group(1))
                print(f"  [{name}]: {total} ürün")
                return total

            # Try to find product links
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check meta or OG for product count
            total_match = re.search(r'toplam.*?(\d+).*?ürün', html, re.IGNORECASE)
            if total_match:
                total = int(total_match.group(1))
                print(f"  [{name}]: {total} ürün (metin'den)")
                return total
            
            # Look for pagination
            pg_match = re.search(r'"pageCount"\s*:\s*(\d+)', html)
            pp_match = re.search(r'"pageSize"\s*:\s*(\d+)', html)
            if pg_match and pp_match:
                pages = int(pg_match.group(1))
                per_page = int(pp_match.group(1))
                total = pages * per_page
                print(f"  [{name}]: ~{total} ürün ({pages} sayfa x {per_page}/sayfa)")
                return total

            # Try another way: count product items
            # Ticimax product card containers
            items = soup.select('.productItem, .product-item, [class*="ProductItem"]')
            if items:
                # Check if there's a next page
                has_next = soup.find(string=re.compile('sonraki|next', re.IGNORECASE)) is not None
                if not has_next:
                    print(f"  [{name}]: ~{len(items)} ürün (tek sayfa)")
                    return len(items)
                else:
                    product_urls.extend(items)
                    page += 1
                    continue
            
            break
        except Exception as e:
            print(f"  [{name}]: Hata - {e}")
            break
    
    # If we couldn't determine from HTML, check product category API
    try:
        api_url = f"https://www.meteorgaleri.com/api/product/GetProductsByCategory?categoryUrlCode={slug}&pageSize=100&pageIndex=1"
        r = requests.get(api_url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if 'totalCount' in data:
                print(f"  [{name}]: {data['totalCount']} ürün (API)")
                return data['totalCount']
    except:
        pass
    
    print(f"  [{name}]: Sayı belirlenemedi")
    return -1

print("Kategori bazlı ürün sayıları:\n")
grand_total = 0
for slug, name in all_cats.items():
    count = count_products_in_category(slug, name)
    if count > 0:
        grand_total += count
    import time
    time.sleep(1)

print(f"\nTahmini Toplam: {grand_total} ürün")
