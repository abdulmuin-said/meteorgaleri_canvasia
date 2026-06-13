import requests
import json

url = "https://www.meteorgaleri.com/siyah-beyaz-aslan-gorselli-cam-tablo"
response = requests.get(url)
with open("E:/Projeler/MeteorGaleri/scratch/product_html.txt", "w", encoding="utf-8") as f:
    f.write(response.text)
