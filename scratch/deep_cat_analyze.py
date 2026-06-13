import requests
from bs4 import BeautifulSoup
import re, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9',
}

# Save one category page HTML and look for product count / page structure
CATS = {
    'cam-tablolar': 'CAM TABLOLAR (Ana)',
    'hayvan-temali-cam-tablolar': 'Hayvan Temalı',
    'spor-ve-taraftar-temali-cam-tablo': 'Spor ve Taraftar',
}

for slug, name in CATS.items():
    url = f"https://www.meteorgaleri.com/{slug}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        html = r.text

        # Dump HTML size
        print(f"\n=== {name} ({slug}) ===")
        print(f"HTTP {r.status_code}, HTML boyutu: {len(html)} bytes")

        # Find productListModel
        match = re.search(r'var productListModel\s*=\s*(\{.*?\});', html, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                print(f"productListModel keys: {list(data.keys())[:10]}")
                for k in ['TotalProductCount', 'totalProductCount', 'ProductCount', 'TotalCount']:
                    if k in data:
                        print(f"  {k} = {data[k]}")
            except:
                print("  productListModel JSON parse failed")
        else:
            print("  productListModel bulunamadi")

        # Find any totalCount / product sayisi
        patterns = [
            r'"TotalProductCount"\s*:\s*(\d+)',
            r'"totalCount"\s*:\s*(\d+)',
            r'"UrunSayisi"\s*:\s*(\d+)',
            r'toplam\s*<[^>]*>\s*(\d+)',
            r'(\d+)\s*[Üü]r[üu]n\s*[Bb]ulundu',
        ]
        for pat in patterns:
            m = re.search(pat, html, re.IGNORECASE)
            if m:
                print(f"  Desen '{pat[:40]}' => {m.group(1)}")

        # Look for pagination info
        pm = re.search(r'"PageCount"\s*:\s*(\d+)', html, re.IGNORECASE)
        ps = re.search(r'"PageSize"\s*:\s*(\d+)', html, re.IGNORECASE)
        if pm and ps:
            pages = int(pm.group(1))
            per_page = int(ps.group(1))
            print(f"  Sayfalama: {pages} sayfa x {per_page} ürün/sayfa = ~{pages*per_page} ürün")

        # Count product items in soup
        soup = BeautifulSoup(html, 'html.parser')
        # Common Ticimax selectors
        for sel in ['.ProductListContent', '.productListContent', '.urun-liste', '.productItem', '#productListDiv', '.product-list-item']:
            items = soup.select(sel)
            if items:
                print(f"  Selector '{sel}' => {len(items)} eleman bulundu")
                break

        time.sleep(2)
    except Exception as e:
        print(f"Hata: {e}")
