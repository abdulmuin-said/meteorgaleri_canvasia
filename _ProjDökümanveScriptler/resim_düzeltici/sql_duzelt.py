import os

# --- AYARLAR ---
hatali_sql_dosyasi = 'update_resimler.sql'
yeni_sql_dosyasi = 'update_resimler_FINAL.sql'

# Değiştirilecek Sütun İsimleri (Eski -> Yeni)
degisiklikler = {
    # Hata: Urunler tablosunda 'Resim' sütunu yok, 'AnaGorselUrl' var.
    'UPDATE "Urunler" SET "Resim" =': 'UPDATE "Urunler" SET "AnaGorselUrl" =',
    
    # KONTROL: Eğer UrunResimleri tablosunda da sütun adı farklıysa buraya ekle.
    # Örn: 'INSERT INTO "UrunResimleri" ("Resim",' : 'INSERT INTO "UrunResimleri" ("ResimUrl",'
}

print("SQL dosyası okunuyor...")

if not os.path.exists(hatali_sql_dosyasi):
    print(f"HATA: '{hatali_sql_dosyasi}' dosyası bulunamadı! Önce resim indirme scriptini çalıştırıp bu dosyayı oluşturmalısın.")
    exit()

with open(hatali_sql_dosyasi, 'r', encoding='utf-8') as f:
    icerik = f.read()

print("Hatalı sütunlar düzeltiliyor...")

sayac = 0
for eski, yeni in degisiklikler.items():
    adet = icerik.count(eski)
    if adet > 0:
        icerik = icerik.replace(eski, yeni)
        print(f"✅ {adet} adet '{eski}' -> '{yeni}' değişikliği yapıldı.")
        sayac += adet
    else:
        print(f"⚠️ Uyarı: '{eski}' ifadesi dosyada bulunamadı.")

if sayac > 0:
    with open(yeni_sql_dosyasi, 'w', encoding='utf-8') as f:
        f.write(icerik)
    print(f"\n🚀 İŞLEM TAMAM! '{yeni_sql_dosyasi}' oluşturuldu.")
    print("Şimdi bu yeni dosyayı PgAdmin'de çalıştırabilirsin.")
else:
    print("\nHerhangi bir değişiklik yapılmadı. Dosya zaten doğru olabilir mi?")