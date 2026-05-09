import json
import os
import urllib.request
import time

# --- AYARLAR ---
json_dosyasi = 'urunler_kategorili_final_tam.json'
hedef_klasor = 'wwwroot/img/products_yeni' # Projenin wwwroot yapısına göre ayarlandı
sql_dosyasi = 'update_resimler.sql'

# Klasör yoksa oluştur
if not os.path.exists(hedef_klasor):
    os.makedirs(hedef_klasor)
    print(f"Klasör oluşturuldu: {hedef_klasor}")

# Tarayıcı gibi davranmak için Header (Bazı sunucular botları engeller)
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

# JSON Dosyasını Oku
print("JSON dosyası okunuyor...")
with open(json_dosyasi, 'r', encoding='utf-8') as f:
    urunler = json.load(f)

print(f"Toplam {len(urunler)} ürün işlenecek.")

sql_komutlari = []

# İşlem Başlıyor
baslangic = time.time()

for index, urun in enumerate(urunler):
    baslik = urun.get('Baslik')
    if not baslik: continue

    # SQL içinde kesme işareti (') sorun çıkarmasın diye escape yapıyoruz (O'neill -> O''neill)
    safe_baslik = baslik.replace("'", "''")

    # 1. Önce eski galeri resimlerini temizle (Temiz başlangıç için)
    # (Bu ürünün ID'sini bulup ona bağlı resimleri siler)
    sql_delete = f"""DELETE FROM "UrunResimleri" WHERE "UrunId" = (SELECT "Id" FROM "Urunler" WHERE "Baslik" = '{safe_baslik}');"""
    sql_komutlari.append(sql_delete)

    # ---------------------------
    # 2. ANA GÖRSEL İŞLEMLERİ
    # ---------------------------
    ana_resim_url = urun.get('Resim')
    if ana_resim_url:
        dosya_adi = ana_resim_url.split('/')[-1] # URL'nin sonundaki ismi al
        yerel_yol = os.path.join(hedef_klasor, dosya_adi)
        web_yolu = f"/img/products_yeni/{dosya_adi}" # Veritabanına yazılacak yol

        try:
            # Resmi İndir (Eğer daha önce inmemişse)
            if not os.path.exists(yerel_yol):
                urllib.request.urlretrieve(ana_resim_url, yerel_yol)
                # print(f"İndi (Ana): {dosya_adi}")
            
            # Urunler tablosunu güncelle
            sql_update = f"""UPDATE "Urunler" SET "Resim" = '{web_yolu}' WHERE "Baslik" = '{safe_baslik}';"""
            sql_komutlari.append(sql_update)

            # Ana resmi aynı zamanda Vitrin=true olarak UrunResimleri'ne ekle
            sql_insert_ana = f"""INSERT INTO "UrunResimleri" ("Resim", "Vitrin", "UrunId", "OlusturulmaTarihi", "SilindiMi") VALUES ('{web_yolu}', true, (SELECT "Id" FROM "Urunler" WHERE "Baslik" = '{safe_baslik}'), NOW(), false);"""
            sql_komutlari.append(sql_insert_ana)

        except Exception as e:
            print(f"HATA (Ana Resim) - {baslik}: {e}")

    # ---------------------------
    # 3. DİĞER RESİMLER (GALERİ)
    # ---------------------------
    diger_resimler = urun.get('DigerResimler', [])
    for galeri_url in diger_resimler:
        if not galeri_url: continue

        dosya_adi = galeri_url.split('/')[-1]
        yerel_yol = os.path.join(hedef_klasor, dosya_adi)
        web_yolu = f"/img/products_yeni/{dosya_adi}"

        try:
            if not os.path.exists(yerel_yol):
                urllib.request.urlretrieve(galeri_url, yerel_yol)
            
            # Galeriye ekle (Vitrin = false)
            sql_insert_galeri = f"""INSERT INTO "UrunResimleri" ("Resim", "Vitrin", "UrunId", "OlusturulmaTarihi", "SilindiMi") VALUES ('{web_yolu}', false, (SELECT "Id" FROM "Urunler" WHERE "Baslik" = '{safe_baslik}'), NOW(), false);"""
            sql_komutlari.append(sql_insert_galeri)

        except Exception as e:
            print(f"HATA (Galeri) - {baslik}: {e}")

    # İlerleme çubuğu gibi her 50 üründe bir bilgi ver
    if (index + 1) % 50 == 0:
        print(f"{index + 1} ürün tamamlandı...")

# SQL Dosyasını Kaydet
print("SQL dosyası oluşturuluyor...")
with open(sql_dosyasi, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_komutlari))

bitis = time.time()
print(f"\nİŞLEM TAMAMLANDI! Süre: {int(bitis - baslangic)} saniye.")
print(f"1. Resimler '{hedef_klasor}' klasörüne indirildi.")
print(f"2. '{sql_dosyasi}' dosyası oluşturuldu. Bu dosyayı PgAdmin'de çalıştır.")