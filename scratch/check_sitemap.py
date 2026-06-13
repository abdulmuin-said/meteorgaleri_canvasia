import requests
from bs4 import BeautifulSoup

url = "https://www.meteorgaleri.com/sitemap.xml"
response = requests.get(url)
print("Sitemap status:", response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'xml')
    locs = soup.find_all('loc')
    
    sitemaps = [loc.text for loc in locs if 'sitemap' in loc.text]
    if sitemaps:
        print("Found sub-sitemaps:")
        for s in sitemaps:
            print(s)
            
        # check products sitemap
        prod_sitemap = next((s for s in sitemaps if 'urun' in s.lower() or 'product' in s.lower()), None)
        if prod_sitemap:
            resp = requests.get(prod_sitemap)
            prod_soup = BeautifulSoup(resp.text, 'xml')
            prod_locs = [l.text for l in prod_soup.find_all('loc')]
            print(f"Found {len(prod_locs)} products in sitemap.")
            print("First 10 products:")
            for p in prod_locs[:10]:
                print(p)
    else:
        print(f"Found {len(locs)} links directly in sitemap")
        print("First 10:")
        for loc in locs[:10]:
            print(loc.text)
