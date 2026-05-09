import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

# ==========================================
# AYARLAR
# ==========================================
URL_DOSYASI = "urls.txt"
CIKTI_DOSYASI = "urunler.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
}

def fiyat_temizle(fiyat_str):
    """
    '₺709,29' gibi stringleri 709.29 float değerine çevirir.
    """
    if not fiyat_str:
        return 0.0
    try:
        # Sembolleri ve boşlukları temizle
        temiz = fiyat_str.replace('₺', '').replace('TL', '').replace('.', '').replace(',', '.').strip()
        return float(temiz)
    except ValueError:
        return 0.0

def veriyi_cek(url):
    print(f"📡 Bağlanılıyor: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        if response.status_code != 200:
            print(f"❌ Sayfa açılamadı: {response.status_code}")
            return None
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # 1. JSON VERİSİNİ BUL (productDetailModel)
        # Sayfa kaynağında 'var productDetailModel = { ... };' kısmını regex ile avlıyoruz.
        pattern = r"var\s+productDetailModel\s*=\s*(\{.*?\});"
        match = re.search(pattern, html_content, re.DOTALL)
        
        if not match:
            print("❌ HATA: Ürün veri modeli (JSON) bulunamadı! Ticimax yapısı farklı olabilir.")
            return None

        json_str = match.group(1)
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Hatası: {e}")
            return None

        # --- ARTIK VERİLER ELİMİZDE, SADECE SEÇİP ALACAĞIZ ---

        # 2. ÜRÜN ADI
        baslik = data.get("productName", "Baslik Yok").strip()

        # 3. GÖRSELLER (productImages dizisinden bigImagePath alıyoruz)
        gorseller = []
        if "productImages" in data and isinstance(data["productImages"], list):
            for img in data["productImages"]:
                if "bigImagePath" in img and img["bigImagePath"]:
                    # URL başında https yoksa ekle
                    img_url = img["bigImagePath"]
                    if img_url.startswith("//"):
                        img_url = "https:" + img_url
                    
                    if img_url not in gorseller:
                        gorseller.append(img_url)
        
        # Eğer JSON'dan görsel gelmezse yedek olarak HTML'den bak (Eski yöntem)
        if not gorseller:
            meta_img = soup.find('meta', {'property': 'og:image'})
            if meta_img:
                gorseller.append(meta_img.get('content'))

        # 4. VARYANTLAR VE FİYATLAR
        # Mantık: productVariantData içinde seçenek tanımları (Örn: 50x70) var.
        # products içinde ise fiyat bilgileri var. Bunlar 'urunID' veya 'id' ile eşleşiyor.
        
        secenekler = []
        
        # Fiyatları hızlı bulmak için products listesini id'ye göre sözlüğe çevirelim
        fiyat_sozlugu = {}
        if "products" in data and isinstance(data["products"], list):
            for p in data["products"]:
                p_id = p.get("id")
                # Fiyatı string olarak alıyoruz örn: "₺709,29"
                fiyat_str = p.get("satisFiyatiStr") or p.get("urunSepetFiyatiStr")
                fiyat_sozlugu[p_id] = fiyat_temizle(fiyat_str)

        # Varyantları dönelim
        if "productVariantData" in data and isinstance(data["productVariantData"], list):
            for v in data["productVariantData"]:
                olcu_adi = v.get("tanim", "").strip()
                urun_id = v.get("urunID") # Bu ID ile fiyatı eşleştireceğiz
                
                # Fiyatı sözlükten bul
                fiyat = fiyat_sozlugu.get(urun_id, 0.0)
                
                # Eğer fiyat 0 ise (bazen ana ürün fiyatı kullanılabilir), ana fiyatı al
                if fiyat == 0.0:
                    ana_fiyat_str = data.get("productPriceStr")
                    fiyat = fiyat_temizle(ana_fiyat_str)

                secenekler.append({
                    "Olcu": olcu_adi,
                    "Fiyat": fiyat
                })
        
        # Eğer hiç varyant yoksa (Standart Ürün)
        if not secenekler:
            ana_fiyat_str = data.get("productPriceStr")
            secenekler.append({
                "Olcu": "Standart",
                "Fiyat": fiyat_temizle(ana_fiyat_str)
            })

        # Çıktı Objesi
        return {
            "Baslik": baslik,
            "Resim": gorseller[0] if gorseller else "", # Ana resim
            "DigerResimler": gorseller[1:], # Galeri (varsa)
            "Varyantlar": secenekler
        }

    except Exception as e:
        print(f"🔥 Beklenmedik Hata: {e}")
        return None

# ==========================================
# ÇALIŞTIRMA
# ==========================================
print("🚀 Ticimax JSON Madencisi Başlatılıyor...")

try:
    with open(URL_DOSYASI, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"❌ '{URL_DOSYASI}' dosyası bulunamadı!")
    exit()

tum_urunler = []

for i, url in enumerate(urls):
    print(f"\n[{i+1}/{len(urls)}] İşleniyor...")
    veri = veriyi_cek(url)
    
    if veri:
        tum_urunler.append(veri)
        print(f"✅ {veri['Baslik']}")
        print(f"🖼️  Toplam Resim: {1 + len(veri['DigerResimler'])}")
        print(f"📏  Toplam Varyant: {len(veri['Varyantlar'])}")
        # Örnek varyant göster
        if veri['Varyantlar']:
            v = veri['Varyantlar'][0]
            print(f"👉  Örnek: {v['Olcu']} -> {v['Fiyat']} TL")
    
    time.sleep(random.uniform(0.5, 1.5)) # Siteyi yormamak için bekleme

# Sonucu Kaydet
with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
    json.dump(tum_urunler, f, indent=4, ensure_ascii=False)

print(f"\n🎉 İŞLEM BİTTİ! Veriler '{CIKTI_DOSYASI}' dosyasına kaydedildi.")