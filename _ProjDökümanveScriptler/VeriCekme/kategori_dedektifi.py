import requests
import json
import re
import time
import unicodedata

# ==========================================
# AYARLAR
# ==========================================
GIRIS_DOSYASI = "urunler_resimli_hazir.json" 
CIKTI_DOSYASI = "urunler_kategorili_son.json"
SITE_ADRESI = "https://www.meteorgaleri.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}

def seo_link_yap(baslik):
    """
    Ürün başlığını Ticimax formatında linke çevirir.
    Örn: "Dini & Hat Tablo" -> "dini-hat-tablo"
    """
    # 1. Türkçe karakterleri değiştir
    text = baslik.lower()
    text = text.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
    
    # 2. Yumuşatma ve temizleme
    # "normalize" işlemi ile garip karakterleri (â gibi) düzelt
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    
    # 3. İstenmeyen karakterleri (parantez, tırnak vs) sil, boşlukları tire yap
    text = re.sub(r'[^a-z0-9\s-]', '', text) # Harf, rakam ve boşluk hariç her şeyi sil
    text = text.replace(' ', '-')
    
    # 4. Çift tireleri tek tireye düşür
    text = re.sub(r'-+', '-', text)
    
    # 5. Baştaki ve sondaki tireleri at
    return text.strip('-')

def kategori_bul_dedektif(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # Eğer tahmin ettiğimiz link yanlışsa 404 döner
        if response.status_code != 200:
            return None 
        
        html_content = response.text
        
        # HEDEF: content_category: 'Dini, Hat Temalı Tablolar',
        pattern = r"content_category\s*:\s*'([^']+)'"
        match = re.search(pattern, html_content)
        
        if match:
            kategori = match.group(1).strip()
            # HTML temizliği
            kategori = kategori.replace("&amp;", "&").replace("&gt;", ">")
            return kategori
            
        return "Genel" # Sayfa açıldı ama kategori bulunamadı

    except Exception as e:
        print(f"   🔥 Hata: {e}")
        return None

# ==========================================
# ANA İŞLEM
# ==========================================
print("📂 JSON okunuyor...")

try:
    with open(GIRIS_DOSYASI, "r", encoding="utf-8") as f:
        urunler = json.load(f)
except FileNotFoundError:
    print("❌ Dosya bulunamadı!")
    exit()

print(f"🚀 {len(urunler)} ürün için URL tahmini ve kategori avı başlıyor...")

bulunan_sayisi = 0

for index, urun in enumerate(urunler):
    baslik = urun.get("Baslik", "")
    
    # Zaten kategori bulduysak geç
    if urun.get("HamKategori") and urun.get("HamKategori") != "Genel":
        continue

    # 1. Başlıktan Link Üret
    seo_url = seo_link_yap(baslik)
    tahmini_link = f"{SITE_ADRESI}/{seo_url}"
    
    print(f"[{index+1}] Hedef: {baslik[:30]}...")
    
    # 2. Siteye Sor
    kategori = kategori_bul_dedektif(tahmini_link)
    
    if kategori:
        urun["HamKategori"] = kategori
        # Gelecekte lazım olur diye tahmin ettiğimiz URL'i de kaydedelim
        urun["Url"] = tahmini_link 
        
        if kategori != "Genel":
            print(f"   ✅ BULUNDU: {kategori}")
            bulunan_sayisi += 1
        else:
            print(f"   ⚠️ Kategori kodu sayfada yok.")
    else:
        # 404 Döndüyse (Link tahmini yanlışsa)
        urun["HamKategori"] = "Genel"
        print(f"   ❌ Link Tahmini Tutmadı (404)")

    # Her 20 üründe bir kaydet
    if index % 20 == 0:
        with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(urunler, f, indent=4, ensure_ascii=False)
            
    time.sleep(0.2) # Siteyi yormamak için

# Final Kayıt
with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
    json.dump(urunler, f, indent=4, ensure_ascii=False)

print("\n" + "="*40)
print(f"🎉 İŞLEM BİTTİ!")
print(f"Toplam {bulunan_sayisi} ürünün kategorisi başarıyla çekildi.")
print(f"📄 Yeni dosya: {CIKTI_DOSYASI}")
print("="*40)