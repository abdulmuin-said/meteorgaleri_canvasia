import requests
from bs4 import BeautifulSoup
import re, time, sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9',
}

# The site only renders 5 products per page in static HTML
# Products are loaded via infinite scroll / AJAX
# Let's try the Ticimax AJAX endpoint pattern

# Ticimax's standard product list AJAX endpoint
def try_ajax_endpoints(cat_slug, cat_id=None):
    base = "https://www.meteorgaleri.com"
    
    endpoints = [
        f"{base}/UrunListesiGetir?kategoriUrlKodu={cat_slug}&sayfa=1&sayfaBasiUrunSayisi=100",
        f"{base}/api/product/list?categoryUrl={cat_slug}&page=1&pageSize=100",
        f"{base}/WebService/UrunService.asmx/UrunListesi",
        f"{base}/{cat_slug}?q=&sayfa=1&srule=",
    ]
    
    if cat_id:
        endpoints += [
            f"{base}/UrunListesiGetir?kategoriId={cat_id}&sayfa=1&sayfaBasiUrunSayisi=100",
        ]
    
    for ep in endpoints:
        try:
            r = requests.get(ep, headers=HEADERS, timeout=10)
            print(f"  {ep[:80]}")
            print(f"  Status: {r.status_code}, Size: {len(r.text)}, Content-Type: {r.headers.get('Content-Type','?')[:40]}")
            if r.status_code == 200 and len(r.text) > 200:
                # Try JSON
                try:
                    data = r.json()
                    print(f"  JSON keys: {list(data.keys())[:5] if isinstance(data, dict) else 'array'}")
                    if isinstance(data, dict) and 'Products' in data:
                        print(f"  Products count: {len(data['Products'])}")
                except:
                    # HTML response - count products
                    soup = BeautifulSoup(r.text, 'html.parser')
                    plc = soup.select('.ProductListContent, .productItem')
                    if plc:
                        print(f"  HTML products found: {len(plc)}")
            print()
        except Exception as e:
            print(f"  Error: {str(e)[:50]}\n")

print("Testing AJAX endpoints for 'hayvan-temali-cam-tablolar':\n")
try_ajax_endpoints('hayvan-temali-cam-tablolar')

# Also try POST
print("\nTrying POST request:")
try:
    r = requests.post("https://www.meteorgaleri.com/hayvan-temali-cam-tablolar",
                     headers=HEADERS,
                     data={'sayfa': '1', 'sayfaBasiUrunSayisi': '100', 'siralamaKriteri': '0'},
                     timeout=10)
    print(f"POST Status: {r.status_code}, Size: {len(r.text)}")
    soup = BeautifulSoup(r.text, 'html.parser')
    links = set(a['href'] for a in soup.select('.ProductListContent a') if a.get('href', '').startswith('/'))
    print(f"POST HTML product links: {len(links)}")
except Exception as e:
    print(f"POST Error: {e}")
