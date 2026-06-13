import json

with open("E:/Projeler/MeteorGaleri/scratch/productDetailModel.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("productCategoryId:", data.get('productCategoryId'))

if 'breadCrumb' in data:
    print("breadCrumb:", data['breadCrumb'])

if 'breadCrumbHtml' in data:
    print("breadCrumbHtml:", data['breadCrumbHtml'])
