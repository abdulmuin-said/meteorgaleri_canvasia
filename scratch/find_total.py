import requests
from bs4 import BeautifulSoup
import re, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9',
}

# Products are loaded via handlebars template + JSON data (AJAX)
# The initial product data is passed to handlebars via a JS variable
# Let's find totalItems or the initial data in the HTML

url = "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar"
r = requests.get(url, headers=HEADERS, timeout=20)
html = r.text

# Look for JSON with totalItems, currentItems
patterns = [
    r'"totalItems"\s*:\s*(\d+)',
    r'"TotalItems"\s*:\s*(\d+)',
    r'"totalPages"\s*:\s*(\d+)',
    r'"TotalPages"\s*:\s*(\d+)',
    r'totalItems\s*=\s*(\d+)',
    r'"total"\s*:\s*(\d+)',
    r'UrunSayisi:\s*(\d+)',
    r'"UrunSayisi":\s*(\d+)',
    r'toplam.*?(\d+).*?ürün',
    r'toplam.*?(\d+).*?urun',
]

found = {}
for pat in patterns:
    m = re.search(pat, html, re.IGNORECASE)
    if m:
        found[pat] = m.group(1)
        print(f"Pattern '{pat}' => {m.group(1)}")

if not found:
    print("No count patterns found. Let's look for the AJAX call URL.")
    # Find getMoreProducts call or similar
    gmp = re.findall(r'getMoreProducts[^)]+', html)
    for g in gmp[:3]:
        print(f"  getMoreProducts call: {g[:100]}")
    
    # Find pageSettings or similar
    psm = re.search(r'pageSettings\s*=\s*(\{[^;]+\})', html, re.DOTALL)
    if psm:
        print(f"pageSettings: {psm.group(1)[:200]}")
    
    # Find initialData or window.data
    wdm = re.search(r'window\.categoryData\s*=\s*(\{.*?\});', html, re.DOTALL)
    if wdm:
        print(f"window.categoryData found!")
    
    # Look for siteSettings
    ssm = re.search(r'siteSettings\s*=\s*(\{[^;]+\})', html, re.DOTALL)
    if ssm:
        try:
            data = json.loads(ssm.group(1))
            print(f"siteSettings keys: {list(data.keys())[:10]}")
        except:
            pass
    
    # Search for any JSON block with products count
    jsblocks = re.findall(r'\{[^{}]{10,500}\}', html)
    for block in jsblocks:
        if '"products"' in block or '"Products"' in block:
            print(f"Block with products: {block[:150]}")
            break

# Try the getMoreProducts AJAX endpoint directly 
print("\nTrying getMoreProducts AJAX call...")
ajax_url = "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar"
ajax_headers = {**HEADERS, 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json, */*'}
r2 = requests.get(ajax_url, headers=ajax_headers, timeout=15)
print(f"XHR response: {r2.status_code}, {len(r2.text)} bytes, {r2.headers.get('Content-Type')}")
try:
    d = r2.json()
    print(f"JSON response keys: {list(d.keys())[:5] if isinstance(d, dict) else 'array length=' + str(len(d))}")
    if isinstance(d, dict):
        for k in ['totalItems', 'TotalItems', 'ProductCount', 'total']:
            if k in d:
                print(f"  {k} = {d[k]}")
except:
    pass
