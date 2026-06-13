import requests
from bs4 import BeautifulSoup
import re, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9',
}

# totalItems = 5 means only 5 initially. But the page uses infinite scroll (getMoreProducts)
# Let's find the exact Ticimax AJAX endpoint by searching for 'getMoreProducts' function definition
url = "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar"
r = requests.get(url, headers=HEADERS, timeout=20)
html = r.text

# Find all mentions of 'getMoreProducts'
idx = html.find('getMoreProducts')
if idx >= 0:
    context = html[max(0,idx-100):idx+500]
    print("getMoreProducts context:", context[:400])

# Find the AJAX URL pattern - search in JS files
# First, find the JS files loaded
soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script', src=True)
ticimax_scripts = [s['src'] for s in scripts if 'ticimax' in s.get('src','').lower() or 'urun' in s.get('src','').lower()]
print("\nTicimax/Urun related scripts:", ticimax_scripts[:5])

# Look for the AJAX URL in html
ajax_search = re.findall(r'["\']([^"\']*getProduct[^"\']*)["\']', html, re.IGNORECASE)
print("\ngetProduct URLs:", ajax_search[:5])

ajax_search2 = re.findall(r'["\']([^"\']*product.*?list[^"\']*)["\']', html, re.IGNORECASE)
print("product list URLs:", ajax_search2[:5])

# Another approach: look for the JSON config that tells how many items to load
jdata_match = re.search(r'var\s+jsondata\s*=\s*(\{[^;]+\})', html, re.DOTALL)
if jdata_match:
    print("jsondata:", jdata_match.group(1)[:200])

# Find siteSettings which usually has product list config
# Search any var=data pattern
for varname in ['listSettings', 'productSettings', 'filterSettings', 'categorySettings', 'settings']:
    m = re.search(rf'var\s+{varname}\s*=\s*(\{{[^;]+\}})', html, re.DOTALL)
    if m:
        print(f"\n{varname}:", m.group(1)[:300])
