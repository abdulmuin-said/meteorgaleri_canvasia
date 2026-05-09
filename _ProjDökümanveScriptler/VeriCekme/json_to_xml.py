import json
import os
import re

json_dosya_adi = "urunler.json"  # JSON dosyanın adı
xml_dosya_adi = "Admin_Yuklenecek_Urunler.xml"

# İndirme scriptinde kullandığımız uzantı (Sen webp demiştin, jpg ise burayı değiştir)
DOSYA_UZANTISI = ".webp" 

def tr_slugify(text):
    """
    Türkçe karakterleri temizler ve metni dosya ismine uygun hale getirir.
    Örnek: "35 Besmele & Allah Yazılı" -> "35-besmele-allah-yazili"
    """
    if not text: return ""
    
    text = text.lower()
    # Türkçe Karakter Değişimi
    replacements = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'c', 'Ğ': 'g', 'İ': 'i', 'Ö': 'o', 'Ş': 's', 'Ü': 'u'
    }
    for tr, eng in replacements.items():
        text = text.replace(tr, eng)
    
    # Geçersiz karakterleri (nokta, virgül, parantez vs) kaldır
    # Sadece harf, rakam ve boşluk kalsın
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    
    # Boşlukları tireye çevir
    text = text.strip().replace(" ", "-")
    
    # Birden fazla tireyi tek tireye indir (olur ya - - olursa)
    text = re.sub(r'-+', '-', text)
    
    return text

def json_to_xml():
    if not os.path.exists(json_dosya_adi):
        print(f"HATA: '{json_dosya_adi}' dosyası bulunamadı!")
        return

    with open(json_dosya_adi, 'r', encoding='utf-8') as f:
        data = json.load(f)

    xml_content = ["<Urunler>"]

    for urun in data:
        baslik = urun.get('Baslik', '')
        if not baslik: continue # Başlıksız ürün olmaz

        # Dosya isminin kökü (Slug)
        dosya_kok = tr_slugify(baslik)
        
        xml_content.append("  <Urun>")
        
        # 1. Temel Bilgiler
        xml_content.append(f"    <Ad>{baslik}</Ad>")
        xml_content.append(f"    <Aciklama>{urun.get('Aciklama', '')}</Aciklama>")
        xml_content.append(f"    <Kategori>{urun.get('HamKategori', 'Genel')}</Kategori>")
        
        # 2. Ana Resim Mantığı: [slug]-ana.webp
        # Örn: 35-besmele-tablo-ana.webp
        ana_resim_adi = f"{dosya_kok}-ana{DOSYA_UZANTISI}"
        xml_content.append(f"    <Resim>{ana_resim_adi}</Resim>")

        # 3. Galeri Mantığı: [slug]-1.webp, [slug]-2.webp ...
        galeri_listesi = urun.get('DigerResimler', [])
        temiz_galeri = []
        
        if isinstance(galeri_listesi, list) and len(galeri_listesi) > 0:
            sayac = 1
            for _ in galeri_listesi: # Linkin ne olduğu önemli değil, sırası önemli
                galeri_resim_adi = f"{dosya_kok}-{sayac}{DOSYA_UZANTISI}"
                temiz_galeri.append(galeri_resim_adi)
                sayac += 1
        
        xml_content.append(f"    <Galeri>{','.join(temiz_galeri)}</Galeri>")

        # 4. Varyantlar (Burası aynı)
        varyantlar_listesi = urun.get('Varyantlar', [])
        varyant_str_list = []
        
        if isinstance(varyantlar_listesi, list):
            for v in varyantlar_listesi:
                olcu = v.get('Olcu', '').strip()
                fiyat = v.get('Fiyat', 0)
                if olcu:
                    varyant_str_list.append(f"{olcu}={fiyat}")
        
        xml_content.append(f"    <Varyantlar>{'|'.join(varyant_str_list)}</Varyantlar>")
        
        xml_content.append("  </Urun>")

    xml_content.append("</Urunler>")

    with open(xml_dosya_adi, "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))

    print(f"✅ XML OLUŞTURULDU: {len(data)} ürün işlendi.")
    print(f"🖼️ Resim formatı: {DOSYA_UZANTISI} (Eğer dosyaların jpg ise kodun başından değiştir)")

# Çalıştır
json_to_xml()