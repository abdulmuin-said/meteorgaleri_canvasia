import requests
import re, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

# Ticimax has a specific API for product lists
# It's typically accessed as POST to the same category URL with specific params
# Or via a dedicated search/list API

# Let's try Ticimax's known API format
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'tr-TR,tr;q=0.9',
    'Referer': 'https://www.meteorgaleri.com/hayvan-temali-cam-tablolar',
    'X-Requested-With': 'XMLHttpRequest',
}

# Ticimax typical product list API calls
endpoints_to_try = [
    # Format 1: standard Ticimax API
    ("GET", "https://www.meteorgaleri.com/api/Product/GetCategoryProducts?categoryUrl=hayvan-temali-cam-tablolar&page=1&pageSize=100", {}),
    ("GET", "https://www.meteorgaleri.com/api/Category/GetProducts?url=hayvan-temali-cam-tablolar&page=1&pageSize=100", {}),
    # Format 2: with store ID
    ("GET", "https://www.meteorgaleri.com/UrunListesi?kategoriId=130&sayfa=1&sayfaBasiUrunSayisi=100", {}),
    # Format 3: REST style
    ("GET", "https://www.meteorgaleri.com/rest/product?categoryUrl=hayvan-temali-cam-tablolar&page=1&pageSize=100", {}),
    # Format 4: Ticimax cloud API
    ("POST", "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar", {
        'sayfa': '1', 'sayfaBasiUrunSayisi': '100', 'tip': 'ajax'
    }),
]

for method, url, data in endpoints_to_try:
    try:
        if method == "GET":
            r = requests.get(url, headers=HEADERS, timeout=10)
        else:
            r = requests.post(url, headers=HEADERS, data=data, timeout=10)
        
        ct = r.headers.get('Content-Type', '')
        print(f"{method} {url[:80]}")
        print(f"  Status: {r.status_code}, Size: {len(r.text)}, CT: {ct[:40]}")
        
        if r.status_code == 200 and 'json' in ct:
            try:
                d = r.json()
                if isinstance(d, dict):
                    for k in ['total', 'Total', 'count', 'Count', 'totalCount', 'TotalCount', 'productCount']:
                        if k in d:
                            print(f"  >> {k} = {d[k]}")
                print(f"  JSON keys: {list(d.keys())[:8] if isinstance(d, dict) else 'array'}")
            except:
                pass
        elif r.status_code == 200 and 'html' in ct:
            # Count product links
            matches = re.findall(r'href=["\']/([\w-]+)["\']', r.text)
            # filter for likely product urls
            product_like = [m for m in matches if len(m) > 20 and '-' in m and 'cam-tablo' in m]
            print(f"  HTML product-like URLs: {len(set(product_like))}")
        print()
        time.sleep(0.5)
    except Exception as e:
        print(f"  Error: {str(e)[:60]}\n")

# Try the Ticimax getMoreProducts endpoint format  
print("=== Trying getMoreProducts format ===")
gmp_url = "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar"
gmp_headers = {**HEADERS, 'Content-Type': 'application/x-www-form-urlencoded'}
# Ticimax pagination uses these params
for nextpage in [2, 3]:
    r = requests.get(f"{gmp_url}?sayfa={nextpage}", headers=HEADERS, timeout=15)
    matches = re.findall(r'href=["\']/([\w-]+)["\']', r.text)
    product_like = [m for m in matches if len(m) > 20 and '-' in m and 'tablo' in m]
    print(f"  Page {nextpage}: {len(set(product_like))} product-like URLs, html size: {len(r.text)}")
    time.sleep(1)
