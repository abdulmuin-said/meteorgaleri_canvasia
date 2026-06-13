import requests
from bs4 import BeautifulSoup
import re, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9',
}

# The site loads only 5 products in HTML but loads more via AJAX
# Ticimax uses a POST or GET AJAX call to load products
# Let's look at the network calls by inspecting the HTML for AJAX URLs

url = "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar"
r = requests.get(url, headers=HEADERS, timeout=20)
html = r.text

# Search for categoryId in the html
cat_id_match = re.search(r'"categoryId"\s*:\s*(\d+)', html)
cat_id_match2 = re.search(r'categoryId\s*=\s*(\d+)', html)
cat_id_match3 = re.search(r'data-category-id=["\'](\d+)["\']', html)

print("categoryId matches:", cat_id_match, cat_id_match2, cat_id_match3)
if cat_id_match:
    print(f"categoryId = {cat_id_match.group(1)}")
if cat_id_match2:
    print(f"categoryId = {cat_id_match2.group(1)}")
if cat_id_match3:
    print(f"categoryId = {cat_id_match3.group(1)}")

# Look for AJAX endpoint hints
ajax_patterns = re.findall(r'url\s*:\s*["\']([^"\']*(?:ProductList|GetProduct|UrunList)[^"\']*)["\']', html, re.IGNORECASE)
print("\nAJAX URL patterns found:", ajax_patterns[:5])

# Look for the search/filter form
forms = re.findall(r'action=["\']([^"\']+)["\']', html)
print("\nForm actions:", forms[:5])

# Check for data-url attributes
data_urls = re.findall(r'data-url=["\']([^"\']*)["\']', html)
print("\ndata-url attributes:", data_urls[:5])

# Look for searchProductList or similar JS config
match = re.search(r'categoryModel\s*=\s*(\{[^;]+\});', html, re.DOTALL)
if match:
    try:
        data = json.loads(match.group(1))
        print("\ncategoryModel:", list(data.keys())[:10])
        if 'Id' in data: print(f"  Category ID: {data['Id']}")
        if 'TotalProductCount' in data: print(f"  TotalProductCount: {data['TotalProductCount']}")
    except:
        pass

# Try page 2 explicitly
print("\n--- Checking page 2 ---")
r2 = requests.get(url + "?sayfa=2", headers=HEADERS, timeout=20)
soup2 = BeautifulSoup(r2.text, 'html.parser')
plc2 = soup2.select_one('.ProductListContent')
if plc2:
    links2 = set(a['href'] for a in plc2.find_all('a', href=True) if a['href'].startswith('/'))
    print(f"Page 2 has {len(links2)} unique product links")
    for l in list(links2)[:3]:
        print(f"  {l}")
else:
    print("No ProductListContent on page 2")
