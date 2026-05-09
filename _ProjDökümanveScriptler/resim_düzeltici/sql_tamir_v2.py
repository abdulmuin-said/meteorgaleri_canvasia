import json
import os

# --- AYARLAR ---
json_dosyasi = 'urunler_kategorili_final_tam.json'
sql_dosyasi = 'update_resimler_KESIN_COZUM.sql'

# Sütun İsimleri (Senin Veritabanına Göre)
URUNLER_RESIM_SUTUNU = "AnaGorselUrl"
GALERI_RESIM_SUTUNU = "ResimYolu"
VARSAYILAN_MI = "VarsayilanMi"

print("JSON dosyası okunuyor...")
if not os.path.exists(json_dosyasi):
    print("HATA: JSON dosyası bulunamadı!")
    exit()

with open(json_dosyasi, 'r', encoding='utf-8') as f:
    urunler = json.load(f)

print(f"Toplam {len(urunler)} ürün için GÜVENLİ SQL hazırlanıyor...")

sql_komutlari = []
sql_komutlari.append("BEGIN;")

for urun in urunler:
    baslik = urun.get('Baslik')
    if not baslik: continue

    # SQL Escape
    safe_baslik = baslik.replace("'", "''")

    # 1. TEMİZLİK (Varsa Sil)
    sql_delete = f"""DELETE FROM "UrunResimleri" WHERE "UrunId" IN (SELECT "Id" FROM "Urunler" WHERE "Baslik" = '{safe_baslik}');"""
    sql_komutlari.append(sql_delete)

    # 2. ANA RESİM GÜNCELLEME (Urunler Tablosu)
    ana_resim_url = urun.get('Resim')
    if ana_resim_url:
        dosya_adi = ana_resim_url.split('/')[-1].split('?')[0]
        web_yolu = f"/img/products_yeni/{dosya_adi}"
        
        # Güncelleme
        sql_update = f"""UPDATE "Urunler" SET "{URUNLER_RESIM_SUTUNU}" = '{web_yolu}' WHERE "Baslik" = '{safe_baslik}';"""
        sql_komutlari.append(sql_update)

        # UrunResimleri Tablosuna Ekleme (GÜVENLİ YÖNTEM)
        # Eğer ürün bulunamazsa bu satır çalışmaz ve HATA VERMEZ.
        sql_insert_ana = f"""
        INSERT INTO "UrunResimleri" ("{GALERI_RESIM_SUTUNU}", "{VARSAYILAN_MI}", "UrunId", "OlusturulmaTarihi", "SilindiMi")
        SELECT '{web_yolu}', true, "Id", NOW(), false
        FROM "Urunler" WHERE "Baslik" = '{safe_baslik}';
        """
        sql_komutlari.append(sql_insert_ana)

    # 3. GALERİ RESİMLERİ
    diger_resimler = urun.get('DigerResimler', [])
    for galeri_url in diger_resimler:
        if not galeri_url: continue
        
        dosya_adi = galeri_url.split('/')[-1].split('?')[0]
        web_yolu = f"/img/products_yeni/{dosya_adi}"

        sql_insert_galeri = f"""
        INSERT INTO "UrunResimleri" ("{GALERI_RESIM_SUTUNU}", "{VARSAYILAN_MI}", "UrunId", "OlusturulmaTarihi", "SilindiMi")
        SELECT '{web_yolu}', false, "Id", NOW(), false
        FROM "Urunler" WHERE "Baslik" = '{safe_baslik}';
        """
        sql_komutlari.append(sql_insert_galeri)

sql_komutlari.append("COMMIT;")

with open(sql_dosyasi, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_komutlari))

print(f"\n✅ GÜVENLİ SQL OLUŞTURULDU: {sql_dosyasi}")
print("Bu dosya 'INSERT INTO ... SELECT' yapısını kullandığı için ürün bulunamazsa hata vermez, sadece atlar.")
print("PgAdmin'de Gönül Rahatlığıyla Çalıştırabilirsin! 🚀")