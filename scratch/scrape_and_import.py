import requests
import json
import psycopg2
from bs4 import BeautifulSoup
import re
import os
import io
import time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import uuid

DB_CONN = "host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?"

# Mapping of the requested slugs to their full names (as they might appear in the website)
TARGET_CATEGORIES = {
    'osmanli-ve-tugra-temali-cam-tablo': 'Osmanlı ve Tuğra Temalı Cam Tablo',
    'spor-ve-taraftar-temali-cam-tablo': 'Spor ve Taraftar Temalı Cam Tablo',
    'farkli-tablolar1': 'Farklı Tablolar',
    'dini-hat-temali-cam-tablolar': 'Dini, Hat Temalı Cam Tablolar',
    'cocuk-odasi-': 'Çocuk Odası Cam Tablolar',
    'cicekli-dekoratif-cam-tablolar': 'Çiçekli Dekoratif Cam Tablolar',
    'mutfak-cam-tablolar': 'Mutfak Cam Tablolar',
    'soyut-cam-tablolar': 'Soyut Cam Tablolar',
    'ataturk-cam-tablolar': 'Atatürk Cam Tablolar',
    'modern-cam-tablolar': 'Modern Cam Tablolar',
    'manzara-cam-tablolar': 'Manzara Cam Tablolar',
    'hayvan-temali-cam-tablolar': 'Hayvan Temalı Cam Tablolar'
}

IMG_SAVE_DIR = "E:/Projeler/MeteorGaleri/KanvasProje.Web/wwwroot/img/products"
os.makedirs(IMG_SAVE_DIR, exist_ok=True)

def setup_categories():
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    # Get Parent "Cam Tablo" ID
    cur.execute('SELECT "Id" FROM "Kategoriler" WHERE "Ad" = \'Cam Tablo\' LIMIT 1')
    res = cur.fetchone()
    if not res:
        print("Error: 'Cam Tablo' parent category not found.")
        return None
    parent_id = res[0]
    
    cat_map = {}
    for slug, name in TARGET_CATEGORIES.items():
        cur.execute('SELECT "Id" FROM "Kategoriler" WHERE "Slug" = %s OR "Ad" = %s', (slug, name))
        row = cur.fetchone()
        if not row:
            # Insert
            print(f"Inserting subcategory: {name}")
            cur.execute('''
                INSERT INTO "Kategoriler" 
                ("Ad", "KisaAciklama", "Aciklama", "Slug", "GorselUrl", "BannerUrl", "SeoTitle", "SeoDescription", 
                 "UstMetin", "AltMetin", "KampanyaEtiketi", "UrunSiralamaTipi", "Sira", "AktifMi", "ParentKategoriId", "OlusturulmaTarihi", "SilindiMi")
                VALUES (%s, '', '', %s, '', '', %s, '', '', '', '', 'manual', 0, true, %s, NOW(), false) RETURNING "Id"
            ''', (name, slug, name, parent_id))
            cat_id = cur.fetchone()[0]
        else:
            cat_id = row[0]
        cat_map[slug] = cat_id
    
    conn.commit()
    cur.close()
    conn.close()
    return cat_map

def get_product_urls():
    urls = []
    print("Fetching sitemap.xml...")
    try:
        resp = requests.get("https://www.meteorgaleri.com/sitemap.xml", timeout=10)
        soup = BeautifulSoup(resp.text, 'xml')
        sitemaps = [loc.text for loc in soup.find_all('loc') if 'products' in loc.text]
        for sm in sitemaps:
            print(f"Fetching product sitemap: {sm}")
            r = requests.get(sm, timeout=10)
            psoup = BeautifulSoup(r.text, 'xml')
            plocs = [loc.text for loc in psoup.find_all('loc')]
            urls.extend(plocs)
            print(f"Found {len(plocs)} products in {sm}")
    except Exception as e:
        print("Failed to get product urls:", e)
    return list(set(urls))

def download_and_convert_image(url, slug, idx):
    try:
        if "width=480" in url:
            url = url.replace("width=480", "width=-")
        elif "width=" in url:
            url = re.sub(r'width=\d+', 'width=-', url)
            
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            filename = f"{slug}-{idx}.webp"
            filepath = os.path.join(IMG_SAVE_DIR, filename)
            img.save(filepath, "WEBP", quality=85)
            return f"/img/products/{filename}"
    except Exception as e:
        print(f"Image error for {url}: {e}")
    return ""

def process_product(url, cat_map):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200: return False
        
        html = r.text
        match = re.search(r'var productDetailModel\s*=\s*(\{.*?\});', html, re.DOTALL)
        if not match: return False
        
        data = json.loads(match.group(1))
        if 'breadCrumb' not in data: return False
        
        # Check if the product belongs to our target categories
        cat_slug = None
        for bc in data['breadCrumb']:
            bc_slug = str(bc.get('urlKod', '')).strip('/')
            if bc_slug in cat_map:
                cat_slug = bc_slug
                break
        
        if not cat_slug:
            return False # skip, not in target categories
            
        cat_id = cat_map[cat_slug]
        
        # Product details
        title = data.get('productName', '').strip()
        if not title: return False
        
        product_slug = url.strip('/').split('/')[-1]
        
        # Description
        soup = BeautifulSoup(html, 'html.parser')
        desc_div = soup.find('div', class_='urunTabAlt')
        description = ""
        if desc_div:
            # basic clean
            description = str(desc_div).replace("urunTabAlt", "product-description")
        else:
            description = data.get('productShortDescription', '') or ""
            
        # Pricing & variants
        prices = {p['id']: p for p in data.get('products', [])}
        variants_data = data.get('productVariantData', [])
        
        if not prices: return False
        
        # Calculate main product pricing based on the first price (or mainVariant)
        main_price_obj = prices.get(data.get('mainVariantId')) or list(prices.values())[0]
        fiyat = main_price_obj.get('satisFiyati', 0) + main_price_obj.get('satisKDV', 0)
        indirimli = main_price_obj.get('indirimliFiyati', 0) + main_price_obj.get('indirimliKDV', 0)
        kdv = main_price_obj.get('kdvOrani', 20)
        
        # Connect DB (each thread needs its own conn)
        conn = psycopg2.connect(DB_CONN)
        cur = conn.cursor()
        
        # Check if exists
        cur.execute('SELECT "Id" FROM "Urunler" WHERE "Slug" = %s OR "Baslik" = %s', (product_slug, title))
        existing = cur.fetchone()
        if existing:
            print(f"Skipping existing: {title}")
            conn.close()
            return True
            
        # Images
        image_urls = []
        if 'productImages' in data:
            for img in data['productImages']:
                bpath = img.get('bigImagePath')
                if bpath:
                    if bpath.startswith('//'): bpath = "https:" + bpath
                    image_urls.append(bpath)
        
        if not image_urls and main_price_obj.get('spotResimBuyukYolu'):
            image_urls.append(main_price_obj['spotResimBuyukYolu'])
            
        # Insert product
        print(f"Inserting product: {title}")
        cur.execute('''
            INSERT INTO "Urunler" 
            ("Baslik", "KisaAd", "Slug", "UrlYolu", "SKU", "Barkod", "Marka", "UrunTipi", "Etiketler", 
             "KisaAciklama", "Aciklama", "TeknikOzellikler", "MalzemeBilgisi", "BakimTalimati", "PaketlemeBilgisi", 
             "AnaGorselUrl", "StokDurumu", "Fiyat", "IndirimliFiyat", "Maliyet", "KdvOrani", 
             "UretimSuresiGun", "KargoyaVerilisSuresiGun", "TahminiTeslimSuresiGun", "AktifMi", "OneCikanMi", "YeniUrunMu", 
             "KampanyaliMi", "AnaSayfadaGoster", "Sira", "GoruntulenmeSayisi", "SatisSayisi", "FavoriSayisi", 
             "MinSiparisAdedi", "MaxSiparisAdedi", "SeoTitle", "SeoDescription", "SeoKeywords", "KategoriId", "OlusturulmaTarihi", "SilindiMi")
            VALUES (%s, '', %s, %s, %s, '', '', 'Cam Tablo', '',
                    '', %s, '', 'Cam', '', '',
                    '', 'Stokta', %s, %s, 0, %s,
                    3, 3, 5, true, false, true, 
                    false, false, 0, 0, 0, 0,
                    1, 10, %s, '', '', %s, NOW(), false) RETURNING "Id"
        ''', (title, product_slug, product_slug, data.get('stockCode', ''), description,
              fiyat, indirimli if indirimli < fiyat else None, kdv, title, cat_id))
        
        urun_id = cur.fetchone()[0]
        
        # Download and insert images
        first_img_path = ""
        for idx, img_url in enumerate(image_urls[:5]): # max 5 images
            local_path = download_and_convert_image(img_url, product_slug, idx+1)
            if local_path:
                if idx == 0: first_img_path = local_path
                cur.execute('''
                    INSERT INTO "UrunResimleri"
                    ("ResimYolu", "Baslik", "AltMetin", "MedyaTipi", "MedyaAlani", "VideoUrl", "ThumbnailYolu", "MobilResimYolu", 
                     "Etiketler", "Sira", "VarsayilanMi", "UrunSecenekId", "UrunId", "OlusturulmaTarihi", "SilindiMi")
                    VALUES (%s, %s, %s, 'Gorsel', 'Galeri', '', '', '', '', %s, %s, NULL, %s, NOW(), false)
                ''', (local_path, title, title, idx+1, (idx == 0), urun_id))
        
        # Update Main Image
        if first_img_path:
            cur.execute('UPDATE "Urunler" SET "AnaGorselUrl" = %s WHERE "Id" = %s', (first_img_path, urun_id))
        
        # Insert variants
        for i, var_data in enumerate(variants_data):
            vid = var_data.get('urunID')
            tanim = var_data.get('tanim', '')
            if vid in prices:
                vp = prices[vid]
                v_fiyat = vp.get('satisFiyati', 0) + vp.get('satisKDV', 0)
                v_ind = vp.get('indirimliFiyati', 0) + vp.get('indirimliKDV', 0)
                if v_ind > 0 and v_ind < v_fiyat:
                    satis = v_ind
                else:
                    satis = v_fiyat
                
                # UrunSecenek insert
                cur.execute('''
                    INSERT INTO "UrunSecenekleri"
                    ("UrunId", "Olcu", "CerceveTipi", "CerceveRengi", "CerceveKalinligi", "MalzemeTuru", "Yon", "ParcaSayisi", 
                     "VaryantSku", "KisilestirmeMetni", "OzelTasarimNotu", "FiyatFarki", "SatisFiyati", "MaliyetFiyati", 
                     "StokAdedi", "UretimSuresiGun", "Desi", "GorselUrl", "AktifMi", "VarsayilanMi", "TukeninceGizle", "OnSipariseAcikMi", "Sira", "OlusturulmaTarihi", "SilindiMi")
                    VALUES (%s, %s, '', '', '', '', '', 1, '', '', '', 0, %s, 0,
                            100, 3, 1, '', true, %s, false, false, %s, NOW(), false)
                ''', (urun_id, tanim, satis, (i == 0), i+1))
                
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return False

def main():
    cat_map = setup_categories()
    if not cat_map: return
    
    urls = get_product_urls()
    print(f"Total product URLs from sitemap: {len(urls)}")
    
    success_count = 0
    # Process concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_product, url, cat_map) for url in urls]
        for f in futures:
            if f.result():
                success_count += 1
                
    print(f"Done! Successfully processed and imported {success_count} products.")

if __name__ == "__main__":
    main()
