import json
import os
import requests
from PIL import Image
from io import BytesIO
import re

# ==========================================
# AYARLAR
# ==========================================
# JSON dosyan nerede? (Python dosyası ile yan yana olduğunu varsayıyorum)
GIRIS_JSON_DOSYASI = "urunler.json" 
CIKTI_JSON_DOSYASI = "urunler_resimli_hazir.json" 

# Resimleri nereye kaydedelim? (Senin verdiğin yol)
KAYIT_KLASORU = r"C:\KanvasProje\VeriCekme\çekilen_veriler"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
}

# Klasör yoksa oluştur (Garanti olsun)
if not os.path.exists(KAYIT_KLASORU):
    os.makedirs(KAYIT_KLASORU)

def slugify(text):
    """Ürün başlığını dosya ismine çevirir (Türkçe karakterleri düzeltir)"""
    text = text.lower()
    text = text.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
    text = re.sub(r'[^a-z0-9]', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def resmi_indir_ve_kaydet(url, dosya_adi):
    """Resmi indirir, WebP yapar ve klasöre kaydeder"""
    if not url:
        return None
        
    try:
        # Eğer URL başında https yoksa ekle
        if url.startswith("//"):
            url = "https:" + url
            
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            
            # Saydamlık varsa (PNG) beyaza boyama veya RGB'ye çevirme
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Tam dosya yolu (C:\KanvasProje\...)
            tam_yol = os.path.join(KAYIT_KLASORU, f"{dosya_adi}.webp")
            
            # Resmi sıkıştırarak kaydet
            img.save(tam_yol, "WEBP", quality=85)
            
            print(f"✅ İndi: {dosya_adi}.webp")
            return f"{dosya_adi}.webp" # Veritabanına sadece dosya adını kaydedeceğiz
        else:
            print(f"❌ İndirilemedi ({response.status_code}): {url}")
            return None
    except Exception as e:
        print(f"🔥 Hata: {e} - Link: {url}")
        return None

# ==========================================
# ANA DÖNGÜ
# ==========================================
print("📂 JSON dosyası okunuyor...")

try:
    with open(GIRIS_JSON_DOSYASI, "r", encoding="utf-8") as f:
        urunler = json.load(f)
except FileNotFoundError:
    print("❌ 'urunler.json' dosyası bulunamadı! Lütfen önce scraper.py'yi çalıştır.")
    exit()

print(f"🚀 Toplam {len(urunler)} ürün için resim indirme işlemi başlıyor...")

for urun in urunler:
    baslik_slug = slugify(urun["Baslik"])
    print(f"\n🎨 Ürün: {urun['Baslik']}")

    # 1. ANA RESİM İŞLEMİ
    # Dosya Adı Örneği: urun-adi-ana.webp
    if urun.get("Resim"):
        dosya_adi = f"{baslik_slug}-ana"
        kayitli_isim = resmi_indir_ve_kaydet(urun["Resim"], dosya_adi)
        if kayitli_isim:
            urun["YerelAnaResim"] = kayitli_isim # JSON'a yeni alan ekliyoruz

    # 2. DİĞER RESİMLER (Çoklu Fotoğraf Mantığı)
    # Dosya Adı Örneği: urun-adi-1.webp, urun-adi-2.webp
    yerel_galeri = []
    if urun.get("DigerResimler"):
        sayac = 1
        for img_url in urun["DigerResimler"]:
            # Ana resimle birebir aynıysa indirme (Ticimax bazen duplicate yapar)
            if img_url == urun.get("Resim"):
                continue
                
            dosya_adi = f"{baslik_slug}-{sayac}"
            kayitli_isim = resmi_indir_ve_kaydet(img_url, dosya_adi)
            
            if kayitli_isim:
                yerel_galeri.append(kayitli_isim)
                sayac += 1 # Sayacı arttır ki isimler çakışmasın (1, 2, 3...)
    
    # JSON'a galeri listesini ekliyoruz
    urun["YerelGaleriResimleri"] = yerel_galeri

# Sonuçları Kaydet
with open(CIKTI_JSON_DOSYASI, "w", encoding="utf-8") as f:
    json.dump(urunler, f, indent=4, ensure_ascii=False)

print("\n" + "="*50)
print(f"🎉 İŞLEM TAMAMLANDI!")
print(f"📂 Resimler şuraya kaydedildi: {KAYIT_KLASORU}")
print(f"📄 Yeni JSON dosyası oluşturuldu: {CIKTI_JSON_DOSYASI}")
print("="*50)