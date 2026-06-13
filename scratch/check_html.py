import requests, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
r = requests.get('https://www.meteorgaleri.com/temperli-cam-kesme-tahtasi-20x30-cm-hijyenik-dayanikli-kaymaz-silikon-ayakli-sik-mutfak-sunumu')
html = r.text
pdm = re.search(r'var productDetailModel\s*=\s*(\{.*?\});', html, re.DOTALL)
if pdm:
    data = json.loads(pdm.group(1))
    print('ProductDetailModel Keys:', list(data.keys()))
    print('Products:', data.get('products'))
    print('Variant Data:', data.get('productVariantData'))
else:
    print('ProductDetailModel not found')
    
# check alternative places for price
for pat in [r'urunSatisFiyati\s*=\s*\"([^\"]+)\"', r'"satisFiyati"\s*:\s*([^,]+)', r'data-price=\"([^\"]+)\"']:
    m = re.search(pat, html)
    if m:
        print(f'Match for {pat}: {m.group(1)}')
