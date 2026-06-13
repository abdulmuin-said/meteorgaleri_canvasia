from bs4 import BeautifulSoup
import re

with open("E:/Projeler/MeteorGaleri/scratch/product_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Prices are usually in a select dropdown or hidden inputs or JSON data
# Let's try to find variant information
print("Looking for dropdown options...")
selects = soup.find_all('select')
for s in selects:
    print("Select name:", s.get('name'), "id:", s.get('id'))
    for opt in s.find_all('option'):
        print("  - Option:", opt.text.strip(), "value:", opt.get('value'))

print("\nLooking for json/variant data in script tags...")
scripts = soup.find_all('script')
for script in scripts:
    if script.string and ('30x45' in script.string or 'variant' in script.string.lower() or 'fiyat' in script.string.lower()):
        # Print a snippet
        content = script.string.strip()
        if len(content) < 500:
            print("Script:", content)
        else:
            # try to extract json block
            match = re.search(r'var\s+variants\s*=\s*(\[.*?\]);', content, re.DOTALL | re.IGNORECASE)
            if match:
                print("Found variants json:", match.group(1)[:200] + "...")
            else:
                # search for another common pattern in Ticimax (ticimax cloud used according to URL)
                match2 = re.search(r'UrunFiyatlari\s*=\s*(\{.*?\});', content, re.DOTALL | re.IGNORECASE)
                if match2:
                    print("Found UrunFiyatlari json:", match2.group(1)[:200] + "...")

# Also look for hidden inputs with prices
print("\nLooking for hidden inputs related to prices:")
for input_tag in soup.find_all('input', {'type': 'hidden'}):
    if 'price' in str(input_tag.get('name')).lower() or 'fiyat' in str(input_tag.get('name')).lower():
        print("Hidden:", input_tag)

