import requests
import json
import psycopg2
from bs4 import BeautifulSoup
import re
import os
import io
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_CONN = "host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?"
IMG_SAVE_DIR = "E:/Projeler/MeteorGaleri/KanvasProje.Web/wwwroot/img/products"
os.makedirs(IMG_SAVE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# URL -> Kategori slug mapping (verilen listeden)
URL_CATEGORY_MAP = {
    # Hayvan Temali (ilk blok "Osmanlı ve Tuğra" yazıyor ama URL'ler hayvan)
    "https://www.meteorgaleri.com/siyah-beyaz-aslan-gorselli-cam-tablo": "hayvan-temali-cam-tablolar",
    "https://www.meteorgaleri.com/mavi-renkli-tavus-kusu-desenli-cam-tablo": "hayvan-temali-cam-tablolar",
    "https://www.meteorgaleri.com/siyah-beyaz-fil-ve-yavrusu-cam-tablo": "hayvan-temali-cam-tablolar",
    "https://www.meteorgaleri.com/zurafa-gorselli-siyah-beyaz-cam-tablo": "hayvan-temali-cam-tablolar",
    "https://www.meteorgaleri.com/kirmizi-beyaz-at-gorselli-cam-tablo": "hayvan-temali-cam-tablolar",
    # Osmanli
    "https://www.meteorgaleri.com/osmanli-armasi-cam-tablo": "osmanli-ve-tugra-temali-cam-tablo",
    # Farkli Tablolar
    "https://www.meteorgaleri.com/van-gogh-terasta-kafe-cizimi-cam-tablo": "farkli-tablolar1",
    "https://www.meteorgaleri.com/mona-lisa-cam-tablo": "farkli-tablolar1",
    "https://www.meteorgaleri.com/salvador-dali-dalgalar-kitap-ve-yelkenli-cam-tablo": "farkli-tablolar1",
    "https://www.meteorgaleri.com/james-webb-astronomi-uzay-manzarali-cam-tablo": "farkli-tablolar1",
    "https://www.meteorgaleri.com/afrikali-kadin-dekoratif-cam-tablo": "farkli-tablolar1",
    "https://www.meteorgaleri.com/gumus-renkli-afrikali-kadin-dekoratif-cam-tablo": "farkli-tablolar1",
    "https://www.meteorgaleri.com/gazete-okuyan-adam-ve-kara-tren-gorselli-cam-tablo": "farkli-tablolar1",
    "https://www.meteorgaleri.com/lacivert-zemin-uzerinde-beyaz-cicekler-yatay-dekoratif-tablo-modern-ve-luks-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/beyaz-gul-desenli-yatay-dekoratif-tablo-zarif-ve-modern-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/pastel-mor-cicekli-yatay-dekoratif-tablo-modern-ve-zarif-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-yaprakli-agac-yatay-dekoratif-tablo-modern-ve-luks-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/mevsim-gecisli-cicekli-agac-yatay-dekoratif-tablo-modern-ve-sanatsal-duvar-dekoru": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-tonlu-soyut-dag-manzarasi-yatay-dekoratif-tablo-modern-ve-luks-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-detayli-beyaz-cicekler-yatay-dekoratif-tablo-zarif-ve-luks-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-detayli-cicekli-agac-yatay-dekoratif-tablo-modern-ve-zarif-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/cok-renkli-yaprakli-yasam-agaci-yatay-dekoratif-tablo-modern-ve-enerjik-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/monokrom-beyaz-cicekler-temperli-cam-tablo-modern-klasik-ve-luks-cam-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/renkli-galaksi-ve-dag-manzarasi-temperli-cam-tablo-modern-ve-carpici-cam-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/renkli-akdeniz-kasabasi-temperli-cam-tablo-sanatsal-ve-canli-cam-duvar-dekoru": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-doku-gorunumlu-mavi-agac-temperli-cam-tablo-modern-ve-luks-cam-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-dokunuslu-beyaz-cicekler-temperli-cam-tablo-zarif-ve-luks-cam-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/kis-manzarali-beyaz-cicekler-temperli-cam-tablo-zarif-ve-huzur-veren-cam-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-gunesli-yasam-agaci-temperli-cam-tablo-modern-ve-anlamli-cam-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/cicekler-arasinda-tavus-kusu-temperli-cam-tablo-zarif-ve-luks-cam-duvar-sanati": "farkli-tablolar1",
    "https://www.meteorgaleri.com/altin-detayli-kugu-yatay-temperli-cam-tablo-luks-floral-duvar-sanati-modern-salon-dekoru": "farkli-tablolar1",
    # Dini Hat
    "https://www.meteorgaleri.com/elif-vav-harfi-dini-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/pembe-ayetel-kursi-dini-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/pembe-felak-suresi-yazili-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/pembe-nas-suresi-yazili-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/felak-suresi-yazili-mavi-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/nas-suresi-yazili-mavi-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/ayetel-kursi-yazili-mavi-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/siyah-esmaul-husna-yazili-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/kabe-": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/ayetel-kursi-yazili-cam-tablo": "dini-hat-temali-cam-tablolar",
    "https://www.meteorgaleri.com/mekke-cam-tablo": "dini-hat-temali-cam-tablolar",
    # Cicekli
    "https://www.meteorgaleri.com/aycicegi-desenli-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    "https://www.meteorgaleri.com/kirmizi-pembe-renkli-cicek-desenli-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    "https://www.meteorgaleri.com/mavi-cicek-ve-kelebekler-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    "https://www.meteorgaleri.com/pembe-renkli-vazoda-cicek-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    "https://www.meteorgaleri.com/vazoda-renkli-cicek-desenli-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    "https://www.meteorgaleri.com/soyut-sonbahar-agac-desenli-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    "https://www.meteorgaleri.com/pembe-ve-beyaz-cicekler-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    "https://www.meteorgaleri.com/renkli-dekoratif-beyaz-laleler-cam-tablo": "cicekli-dekoratif-cam-tablolar",
    # Mutfak
    "https://www.meteorgaleri.com/baharat-desenli-cam-tablo": "mutfak-cam-tablolar",
    # Soyut
    "https://www.meteorgaleri.com/yesil-mavi-beyaz-renkli-soyut-mermer-desenli-cam-tablo": "soyut-cam-tablolar",
    "https://www.meteorgaleri.com/dandelion-gun-batimi-cam-tablo": "soyut-cam-tablolar",
    # Ataturk
    "https://www.meteorgaleri.com/kalpakli-ataturk-gorselli-cam-tablo": "ataturk-cam-tablolar",
    "https://www.meteorgaleri.com/siyah-beyaz-sanli-ataturk-ucu-bir-tabloda-resimleri-cam-tablo": "ataturk-cam-tablolar",
    # Manzara
    "https://www.meteorgaleri.com/urgup-ucan-balon-": "manzara-cam-tablolar",
    "https://www.meteorgaleri.com/-gunbatiminda-yelken-manzarali-cam-tablo": "manzara-cam-tablolar",
    "https://www.meteorgaleri.com/doga-ve-deniz-manzarali-cam-tablo": "manzara-cam-tablolar",
}

def make_request(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            r = SESSION.get(url, timeout=25)
            if r.status_code == 200:
                return r
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep((attempt + 1) * 3)
    return None

def get_cat_id_map():
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    cur.execute('SELECT "Id", "Slug" FROM "Kategoriler" WHERE "Slug" IS NOT NULL AND "Slug" != \'\'')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {row[1]: row[0] for row in rows}

def download_and_convert_image(url, slug, idx):
    from PIL import Image
    try:
        # Get HD version
        if 'cdn-cgi/image' in url:
            url = re.sub(r'width=\d+,quality=\d+', 'width=-,quality=85', url)
        elif 'ticimax' in url and '/thumb/' in url:
            url = url.replace('/thumb/', '/buyuk/')

        r = SESSION.get(url, timeout=25)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            filename = f"{slug}-{idx}.webp"
            filepath = os.path.join(IMG_SAVE_DIR, filename)
            img.save(filepath, "WEBP", quality=85)
            return f"/img/products/{filename}"
    except Exception as e:
        print(f"    Görsel hatası: {str(e)[:80]}")
    return ""

def scrape_product(url):
    r = make_request(url)
    if not r:
        print(f"  HATA: Sayfa açılamadı")
        return None

    html = r.text
    match = re.search(r'var productDetailModel\s*=\s*(\{.*?\});', html, re.DOTALL)
    if not match:
        print(f"  HATA: productDetailModel bulunamadı")
        return None

    try:
        data = json.loads(match.group(1))
    except:
        print(f"  HATA: JSON parse edilemedi")
        return None

    title = data.get('productName', '').strip()
    if not title:
        return None

    product_slug = url.strip('/').split('/')[-1]

    # Description
    soup = BeautifulSoup(html, 'html.parser')
    description = ""
    for tab_id in ['uTab1', 'divDetay', 'tabDetay', 'divOzetBilgi']:
        d = soup.find('div', id=tab_id)
        if d and len(str(d)) > 100:
            description = str(d)
            break

    # Pricing
    products_list = {p['id']: p for p in data.get('products', [])}
    variants_data = [v for v in data.get('productVariantData', []) if v.get('aktif', True)]

    if not products_list:
        return None

    main_id = data.get('mainVariantId')
    main_p = products_list.get(main_id) or list(products_list.values())[0]

    fiyat = round(main_p.get('satisFiyati', 0) + main_p.get('satisKDV', 0), 2)
    indirim_raw = main_p.get('indirimliFiyati', 0) + main_p.get('indirimliKDV', 0)
    indirimli = round(indirim_raw, 2) if indirim_raw > 0 and indirim_raw < fiyat else None

    # Images
    images = []
    for img in data.get('productImages', []):
        bp = img.get('bigImagePath', '')
        if bp:
            if bp.startswith('//'): bp = 'https:' + bp
            images.append(bp)
    if not images and main_p.get('spotResimBuyukYolu'):
        images.append(main_p['spotResimBuyukYolu'])

    # Variants
    variant_info = []
    for i, vd in enumerate(variants_data):
        vid = vd.get('urunID')
        tanim = vd.get('tanim', '')
        if vid in products_list:
            vp = products_list[vid]
            v_s = vp.get('satisFiyati', 0) + vp.get('satisKDV', 0)
            v_i = vp.get('indirimliFiyati', 0) + vp.get('indirimliKDV', 0)
            actual = round(v_i if v_i > 0 and v_i < v_s else v_s, 2)
            variant_info.append({'olcu': tanim, 'fiyat': actual, 'is_default': (i == 0)})

    return {
        'title': title,
        'slug': product_slug,
        'sku': data.get('stockCode', ''),
        'description': description,
        'fiyat': fiyat,
        'indirimli': indirimli,
        'images': images,
        'variants': variant_info,
    }

def insert_product(product, cat_id):
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    try:
        cur.execute('SELECT "Id" FROM "Urunler" WHERE "Slug" = %s OR "Baslik" = %s',
                    (product['slug'], product['title']))
        existing = cur.fetchone()
        if existing:
            print(f"  ⟳ Zaten mevcut, atlanıyor.")
            return False

        cur.execute('''
            INSERT INTO "Urunler"
            ("Baslik","KisaAd","Slug","UrlYolu","SKU","Barkod","Marka","UrunTipi","Etiketler",
             "KisaAciklama","Aciklama","TeknikOzellikler","MalzemeBilgisi","BakimTalimati","PaketlemeBilgisi",
             "AnaGorselUrl","StokDurumu","Fiyat","IndirimliFiyat","Maliyet","KdvOrani",
             "UretimSuresiGun","KargoyaVerilisSuresiGun","TahminiTeslimSuresiGun",
             "AktifMi","OneCikanMi","YeniUrunMu","KampanyaliMi","AnaSayfadaGoster",
             "Sira","GoruntulenmeSayisi","SatisSayisi","FavoriSayisi",
             "MinSiparisAdedi","MaxSiparisAdedi","SeoTitle","SeoDescription","SeoKeywords",
             "KategoriId","OlusturulmaTarihi","SilindiMi")
            VALUES (%s,'', %s,%s,%s,'','MeteorGaleri','Cam Tablo','cam tablo',
                    '',%s,'','Cam','','',
                    '','Stokta',%s,%s,0,20,
                    3,3,5,
                    true,false,true,false,false,
                    0,0,0,0,
                    1,10,%s,%s,'cam tablo',
                    %s,NOW(),false) RETURNING "Id"
        ''', (product['title'], product['slug'], product['slug'], product['sku'],
              product['description'], product['fiyat'], product['indirimli'],
              product['title'], product['title'], cat_id))

        urun_id = cur.fetchone()[0]

        # Images - download and convert
        first_img = ""
        for idx, img_url in enumerate(product['images'][:5]):
            print(f"    Görsel {idx+1}: indiriliyor...")
            local_path = download_and_convert_image(img_url, product['slug'], idx+1)
            if local_path:
                if idx == 0:
                    first_img = local_path
                cur.execute('''
                    INSERT INTO "UrunResimleri"
                    ("ResimYolu","Baslik","AltMetin","MedyaTipi","MedyaAlani","VideoUrl",
                     "ThumbnailYolu","MobilResimYolu","Etiketler","Sira","VarsayilanMi",
                     "UrunSecenekId","UrunId","OlusturulmaTarihi","SilindiMi")
                    VALUES (%s,%s,%s,'Gorsel','Galeri','','','','',%s,%s,NULL,%s,NOW(),false)
                ''', (local_path, product['title'], product['title'], idx+1, (idx == 0), urun_id))

        if first_img:
            cur.execute('UPDATE "Urunler" SET "AnaGorselUrl" = %s WHERE "Id" = %s', (first_img, urun_id))

        # Variants
        for i, v in enumerate(product['variants']):
            cur.execute('''
                INSERT INTO "UrunSecenekleri"
                ("UrunId","Olcu","CerceveTipi","CerceveRengi","CerceveKalinligi","MalzemeTuru",
                 "Yon","ParcaSayisi","VaryantSku","KisilestirmeMetni","OzelTasarimNotu",
                 "FiyatFarki","SatisFiyati","MaliyetFiyati","StokAdedi","UretimSuresiGun",
                 "Desi","GorselUrl","AktifMi","VarsayilanMi","TukeninceGizle",
                 "OnSipariseAcikMi","Sira","OlusturulmaTarihi","SilindiMi")
                VALUES (%s,%s,'','','','',
                        '',1,'','','',
                        0,%s,0,100,3,
                        1,'',true,%s,false,
                        false,%s,NOW(),false)
            ''', (urun_id, v['olcu'], v['fiyat'], v['is_default'], i+1))

        conn.commit()
        return True, first_img
    except Exception as e:
        conn.rollback()
        print(f"  DB Hatası: {str(e)[:120]}")
        return False, ""
    finally:
        cur.close()
        conn.close()

def update_category_image(cat_id, img_path):
    """İlk eklenen ürünün görselini kategori görseli olarak ata."""
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    try:
        cur.execute('SELECT "GorselUrl" FROM "Kategoriler" WHERE "Id" = %s', (cat_id,))
        row = cur.fetchone()
        if row and not row[0]:  # Sadece boşsa güncelle
            cur.execute('UPDATE "Kategoriler" SET "GorselUrl" = %s WHERE "Id" = %s', (img_path, cat_id))
            conn.commit()
    finally:
        cur.close()
        conn.close()

def main():
    print("=== Cam Tablo Ürün Aktarımı (Manuel URL Listesi) ===\n")

    cat_id_map = get_cat_id_map()
    print(f"DB'de bulunan kategori slug'ları: {list(cat_id_map.keys())[:10]}\n")

    total = len(URL_CATEGORY_MAP)
    success = 0
    skipped = 0
    failed = 0

    for i, (url, cat_slug) in enumerate(URL_CATEGORY_MAP.items()):
        print(f"\n[{i+1}/{total}] {url.split('/')[-1]}")
        print(f"  Kategori: {cat_slug}")

        cat_id = cat_id_map.get(cat_slug)
        if not cat_id:
            print(f"  HATA: Kategori bulunamadı: {cat_slug}")
            failed += 1
            continue

        product = scrape_product(url)
        if not product:
            failed += 1
            continue

        print(f"  Başlık: {product['title']}")
        print(f"  Fiyat: {product['fiyat']} TL | Varyant: {len(product['variants'])} | Görsel: {len(product['images'])}")

        result = insert_product(product, cat_id)
        if isinstance(result, tuple):
            ok, first_img = result
        else:
            ok, first_img = result, ""

        if ok:
            print(f"  ✓ Eklendi!")
            success += 1
            # Kategori görseli yoksa bu ürünün görselini ata
            if first_img:
                update_category_image(cat_id, first_img)
        else:
            skipped += 1

        time.sleep(1.2)

    print(f"\n=== TAMAMLANDI ===")
    print(f"  ✓ Eklendi: {success}")
    print(f"  ⟳ Atlandı: {skipped}")
    print(f"  ✗ Hata: {failed}")

if __name__ == "__main__":
    main()
