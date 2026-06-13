import requests

url = "https://www.meteorgaleri.com/spor-ve-taraftar-temali-cam-tablo"
response = requests.get(url)
with open("E:/Projeler/MeteorGaleri/scratch/category_html.txt", "w", encoding="utf-8") as f:
    f.write(response.text)
