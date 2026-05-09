import json

# ==========================================
# AYARLAR
# ==========================================
# Dedektif scriptinin oluşturduğu dosyayı buraya gir
GIRIS_DOSYASI = "urunler_kategorili_son.json" 
CIKTI_DOSYASI = "urunler_kategorili_final_tam.json"

# KATEGORİ SÖZLÜĞÜ (İnternetten bulunamayanlar için kelime bazlı tahmin)
KATEGORI_SOZLUGU = {
    "Dini, Hat Temalı Tablolar": ["dini", "islami", "ayet", "sure", "allah", "muhammed", "besmele", "vav", "elif", "cami", "kabe", "mevlana", "semazen", "esmaül", "hüsna", "namaz", "dua", "hat "],
    "Atatürk ve Türkiye Temalı Tablolar": ["atatürk", "ata", "mustafa kemal", "türk", "türkiye", "bayrak", "ay yıldız", "harita", "istiklal", "anıtkabir", "osmanlı"],
    "Manzara Temalı Tablolar": ["manzara", "deniz", "orman", "dağ", "şelale", "göl", "nehir", "gün batımı", "sahil", "doğa", "ağaç", "bahar", "kış", "sonbahar"],
    "Hayvanlar Alemi": ["aslan", "kaplan", "kurt", "at", "fil", "geyik", "kuş", "kartal", "kelebek", "hayvan", "zürafa", "kedi", "köpek", "leopar"],
    "Şehir ve Mimari": ["şehir", "istanbul", "kız kulesi", "galata", "paris", "eyfel", "londra", "new york", "köprü", "bina", "sokak", "mimari"],
    "Araba ve Araçlar": ["araba", "otomobil", "motor", "motosiklet", "ferrari", "bmw", "mercedes", "klasik", "vosvos", "araç", "uçak", "gemi"],
    "Çiçekli ve Dekoratif": ["çiçek", "gül", "lale", "papatya", "orkide", "menekşe", "yaprak", "bitki", "vazo", "renkli", "dekoratif"],
    "Soyut ve Sanatsal": ["soyut", "sanatsal", "modern", "geometrik", "sürreal", "yağlı boya", "fırça"],
    "Parçalı Tablolar": ["5 parça", "3 parça", "4 parça", "parçalı", "set"],
}

def kelimeden_tahmin_et(baslik):
    baslik_kucuk = baslik.lower()
    
    for kategori, kelimeler in KATEGORI_SOZLUGU.items():
        if kategori == "Parçalı Tablolar": continue # Bunu sona sakla
        
        for kelime in kelimeler:
            if kelime in baslik_kucuk:
                return kategori
                
    # Hiçbiri tutmazsa parçalı mı diye bak
    if "parça" in baslik_kucuk:
        return "Parçalı Tablolar"
        
    return "Genel" # Kurtarılamadı

# ==========================================
# ANA İŞLEM
# ==========================================
print("📂 Dosya okunuyor...")

try:
    with open(GIRIS_DOSYASI, "r", encoding="utf-8") as f:
        urunler = json.load(f)
except FileNotFoundError:
    print("❌ Dosya bulunamadı! Önceki işlem bitmemiş olabilir.")
    exit()

kurtarilan_sayisi = 0
genel_kalan_sayisi = 0

print("🧹 Süpürme işlemi başladı...")

for urun in urunler:
    mevcut_kat = urun.get("HamKategori")
    
    # Sadece kategorisi "Genel" olanlara veya hiç olmayanlara müdahale et
    if not mevcut_kat or mevcut_kat == "Genel":
        tahmin = kelimeden_tahmin_et(urun.get("Baslik", ""))
        urun["HamKategori"] = tahmin
        
        if tahmin != "Genel":
            kurtarilan_sayisi += 1
            print(f"✅ Kurtarıldı: {urun['Baslik'][:30]}... -> {tahmin}")
        else:
            genel_kalan_sayisi += 1
            # print(f"❌ Kurtarılamadı: {urun['Baslik']}") # Kirlilik olmasın diye kapalı

# Kaydet
with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
    json.dump(urunler, f, indent=4, ensure_ascii=False)

print("\n" + "="*40)
print(f"🎉 SÜPÜRME BİTTİ!")
print(f"🚑 Kurtarılan Ürün: {kurtarilan_sayisi}")
print(f"🏳️ Hala 'Genel' Kalan: {genel_kalan_sayisi}")
print(f"📄 Son Dosya: {CIKTI_DOSYASI}")
print("="*40)