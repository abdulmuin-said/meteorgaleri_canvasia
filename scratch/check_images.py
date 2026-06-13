import json
import re

with open("E:/Projeler/MeteorGaleri/scratch/productDetailModel.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if 'productImages' in data:
    for img in data['productImages']:
        print(img)
        
if 'resimler' in data['products'][0] and data['products'][0]['resimler']:
    print("resimler in product:", data['products'][0]['resimler'])
