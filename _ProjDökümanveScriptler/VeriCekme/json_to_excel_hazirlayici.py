import json
import pandas as pd
import os

# ==========================================
# AYARLAR
# ==========================================
JSON_DOSYASI = "urunler_kategorili_final_tam.json" # Elindeki son ve en temiz JSON
CIKTI_EXCEL = "Admin_Yuklenecek_Urunler.xlsx"

print("📂 JSON dosyası okunuyor...")

try:
    with open(JSON_DOSYASI, "r", encoding="utf-8") as f:
        urunler = json.load(f)
except FileNotFoundError:
    print("❌ JSON dosyası bulunamadı!")
    exit()

print(f"🚀 {len(urunler)} ürün Excel formatına dönüştürülüyor...")

excel_verisi = []

for urun in urunler:
    # 1. Varyantları Hazırla (Format: 50x70=500|70x100=750)
    varyant_str = ""
    if urun.get("Varyantlar"):
        v_list = []
        for v in urun["Varyantlar"]:
            # Fiyatı ve ölçüyü al, birleştir
            v_list.append(f"{v['Olcu']}={v['Fiyat']}")
        varyant_str = "|".join(v_list)

    # 2. Galeri Resimlerini Hazırla (Format: resim1.webp,resim2.webp)
    galeri_str = ""
    if urun.get("YerelGaleriResimleri"):
        galeri_str = ",".join(urun["YerelGaleriResimleri"])

    # 3. Listeye Ekle
    excel_verisi.append({
        "Ürün Adı": urun.get("Baslik"),
        "Açıklama": "Birinci sınıf kanvas tablo.", # İstersen burayı özelleştir
        "Kategori (Tam Adı)": urun.get("HamKategori", "Genel"),
        "Ana Resim (Dosya Adı)": urun.get("YerelAnaResim"),
        "Galeri Resimleri (Virgülle)": galeri_str,
        "Varyantlar (Ölçü=Fiyat|Ölçü=Fiyat)": varyant_str
    })

# DataFrame oluştur ve Excel'e kaydet
df = pd.DataFrame(excel_verisi)
df.to_excel(CIKTI_EXCEL, index=False)

print("\n" + "="*40)
print(f"🎉 EXCEL HAZIRLANDI!")
print(f"📄 Dosya Adı: {CIKTI_EXCEL}")
print("Bu dosyayı alıp Admin panelinden yükleyebilirsin.")
print("="*40)