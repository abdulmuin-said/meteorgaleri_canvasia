import re
import json

with open("E:/Projeler/MeteorGaleri/scratch/category_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

# search for product urls
links = re.findall(r'href=["\'](/[^"\']*?-cam-tablo[^"\']*?)["\']', html)
print("Found links matching pattern:", set(links))

# check if there's any javascript data containing the products
match = re.search(r'var productListModel\s*=\s*(\{.*?\});', html, re.DOTALL)
if match:
    print("Found productListModel!")
    
match = re.search(r'var categoryProducts\s*=\s*(\[.*?\]);', html, re.DOTALL)
if match:
    print("Found categoryProducts!")

match = re.search(r'window\.products\s*=\s*(\[.*?\]);', html, re.DOTALL)
if match:
    print("Found window.products!")

# Look for ticimax data objects
match = re.search(r'productDetailModel', html)
if match:
    print("Found productDetailModel in category?!")

# What if the products are loaded via AJAX from a web service?
match = re.search(r'url:\s*["\']([^"\']*?ProductList[^"\']*?)["\']', html, re.IGNORECASE)
if match:
    print("Found AJAX URL for products:", match.group(1))

# Let's just find ANY json-like array containing "url"
matches = re.finditer(r'\{[^{}]*?"url"[^{}]*?\}', html, re.IGNORECASE)
for m in matches:
    if 'cam-tablo' in m.group(0):
        print("Found JSON object with cam-tablo url:", m.group(0)[:200])

