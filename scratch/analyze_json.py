import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("E:/Projeler/MeteorGaleri/scratch/product_html.txt", "r", encoding="utf-8") as f:
    html = f.read()

match = re.search(r'var productDetailModel\s*=\s*(\{.*?\});', html, re.DOTALL)
if match:
    json_str = match.group(1)
    data = json.loads(json_str)
    print("Product Name:", data.get('productName'))
    print("Variants:")
    if 'productVariants' in data:
        for v in data['productVariants']:
            # The structure depends on the JSON
            # Sometimes variants are in a different place
            pass
    # Let's just print keys to see what's inside
    print(data.keys())
    
    # Are variants in productDetailModel?
    if 'productVariants' in data:
        print("productVariants exist:", len(data['productVariants']))
    
    # Maybe let's just dump the JSON to a file so we can inspect it easily
    with open("E:/Projeler/MeteorGaleri/scratch/productDetailModel.json", "w", encoding="utf-8") as out:
        json.dump(data, out, indent=2, ensure_ascii=False)
    print("Dumped productDetailModel to scratch/productDetailModel.json")
