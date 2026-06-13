import requests
from bs4 import BeautifulSoup
import re, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9',
}

# The site only shows 5 products in static HTML but uses infinite scroll
# We need to find what's inside the HTML for category/product count
# Let's search for "toplam" or urun sayi in the raw HTML

url = "https://www.meteorgaleri.com/hayvan-temali-cam-tablolar"
r = requests.get(url, headers=HEADERS, timeout=20)
html = r.text

# Save raw and search
lines = html.split('\n')
interesting = []
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['toplam', 'urun', 'sayfa', 'pagecount', 'pagesize', 'totalcount', 'productcount']):
        stripped = line.strip()
        if stripped and len(stripped) < 300:
            interesting.append((i, stripped[:200]))

print(f"Interesting lines ({len(interesting)} found):")
for ln, content in interesting[:30]:
    print(f"  Line {ln}: {content}")
