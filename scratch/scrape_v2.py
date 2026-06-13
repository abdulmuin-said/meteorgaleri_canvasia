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

# Sadece Cam Tablo alt kategorileri - doğru URL'lerle
TARGET_CATEGORIES = {
    'osmanli-ve-tugra-temali-cam-tablo': ('Osmanlı ve Tuğra Temalı Cam Tablo', 'https://www.meteorgaleri.com/osmanli-ve-tugra-temali-cam-tablo'),
    'spor-ve-taraftar-temali-cam-tablo': ('Spor ve Taraftar Temalı Cam Tablo', 'https://www.meteorgaleri.com/spor-ve-taraftar-temali-cam-tablo'),
    'farkli-tablolar1': ('Farklı Tablolar', 'https://www.meteorgaleri.com/farkli-tablolar1'),
    'dini-hat-temali-cam-tablolar': ('Dini, Hat Temalı Cam Tablolar', 'https://www.meteorgaleri.com/dini-hat-temali-cam-tablolar'),
    'cicekli-dekoratif-cam-tablolar': ('Çiçekli Dekoratif Cam Tablolar', 'https://www.meteorgaleri.com/cicekli-dekoratif-cam-tablolar'),
    'mutfak-cam-tablolar': ('Mutfak Cam Tablolar', 'https://www.meteorgaleri.com/mutfak-cam-tablolar'),
    'soyut-cam-tablolar': ('Soyut Cam Tablolar', 'https://www.meteorgaleri.com/soyut-cam-tablolar'),
    'ataturk-cam-tablolar': ('Atatürk Cam Tablolar', 'https://www.meteorgaleri.com/ataturk-cam-tablolar'),
    'manzara-cam-tablolar': ('Manzara Cam Tablolar', 'https://www.meteorgaleri.com/manzara-cam-tablolar'),
    'hayvan-temali-cam-tablolar': ('Hayvan Temalı Cam Tablolar', 'https://www.meteorgaleri.com/hayvan-temali-cam-tablolar'),
}

IMG_SAVE_DIR = "E:/Projeler/MeteorGaleri/KanvasProje.Web/wwwroot/img/products"
os.makedirs(IMG_SAVE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def make_request(url, max_retries=3, timeout=20):
    for attempt in range(max_retries):
        try:
            r = SESSION.get(url, timeout=timeout)
            if r.status_code == 200:
                return r
            elif r.status_code == 429:
                wait = (attempt + 1) * 10
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                return None
        except Exception as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 5
                print(f"  Error (attempt {attempt+1}), retrying in {wait}s: {str(e)[:60]}")
                time.sleep(wait)
            else:
                print(f"  Failed after {max_retries} attempts: {str(e)[:80]}")
                return None
    return None

def get_cat_id_map():
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    cur.execute('SELECT "Id", "Slug" FROM "Kategoriler" WHERE "Slug" = ANY(%s)',
                ([slug for slug in TARGET_CATEGORIES.keys()],))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {row[1]: row[0] for row in rows}

def get_products_from_sitemap(cat_slug):
    """Try to find product URLs from the site's category-based sitemap or category page."""
    products = []
    
    # Try category sitemap
    cat_sitemap_url = f"https://www.meteorgaleri.com/sitemap/categories/{cat_slug}.xml"
    r = make_request(cat_sitemap_url)
    if r and r.status_code == 200 and '<loc>' in r.text:
        soup = BeautifulSoup(r.text, 'xml')
        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if url not in [f"https://www.meteorgaleri.com/{cat_slug}"]:
                products.append(url)
        if products:
            return products
    
    # Use the existing product data: scan all sitemaps and find products matching this category
    return None

def get_products_from_ticimax_api(cat_slug, category_id_on_source):
    """Ticimax has a product list API we can use."""
    products = []
    page = 1
    while True:
        url = f"https://www.meteorgaleri.com/Urun/UrunListesiGetir?kategoriUrlKodu={cat_slug}&sayfa={page}&sayfaBasiUrunSayisi=100"
        r = make_request(url)
        if not r:
            break
        try:
            data = r.json()
            if 'Products' in data and data['Products']:
                for p in data['Products']:
                    purl = p.get('Url') or p.get('ProductUrl') or p.get('url')
                    if purl:
                        if not purl.startswith('http'):
                            purl = "https://www.meteorgaleri.com/" + purl.lstrip('/')
                        products.append(purl)
                if len(data['Products']) < 100:
                    break
                page += 1
            else:
                break
        except:
            break
    return products

def get_product_urls_from_all_sitemaps(target_cat_slugs):
    """Scan all product sitemaps and filter by breadcrumb category."""
    print("Scanning all product sitemaps for cam tablo products...")
    all_cam_products = {}  # url -> cat_slug
    
    for page_num in range(5):
        sitemap_url = f"https://www.meteorgaleri.com/sitemap/products/{page_num}.xml"
        r = make_request(sitemap_url)
        if not r: continue
        
        soup = BeautifulSoup(r.text, 'xml')
        locs = [loc.text.strip() for loc in soup.find_all('loc')]
        print(f"  Sitemap page {page_num}: {len(locs)} products")
        
        # Quick filter: only URLs likely to be cam tablolar
        cam_urls = [l for l in locs if 'cam-tablo' in l]
        print(f"    -> {len(cam_urls)} contain 'cam-tablo'")
        all_cam_products.update({url: None for url in cam_urls})
    
    return list(all_cam_products.keys())

def get_product_info(url):
    """Scrape a single product page and return structured data."""
    r = make_request(url)
    if not r: return None
    
    html = r.text
    match = re.search(r'var productDetailModel\s*=\s*(\{.*?\});', html, re.DOTALL)
    if not match: return None
    
    try:
        data = json.loads(match.group(1))
    except:
        return None
    
    # Get category from breadcrumb
    breadcrumb = data.get('breadCrumb', [])
    cat_slug = None
    for bc in breadcrumb:
        url_kod = bc.get('urlKod', '').strip('/')
        if url_kod in TARGET_CATEGORIES:
            cat_slug = url_kod
            break
    
    if not cat_slug:
        return None  # Not in our target categories
    
    # Get description from HTML
    soup = BeautifulSoup(html, 'html.parser')
    description = ""
    
    # Try multiple selectors for description
    for sel_id in ['uTab1', 'divDetay', 'divOzetBilgi', 'tabDetay']:
        desc_div = soup.find('div', id=sel_id)
        if desc_div and len(str(desc_div)) > 100:
            description = str(desc_div)
            break
    
    if not description:
        # Try class-based
        desc_div = soup.find('div', class_='urunDetayTabContent')
        if desc_div:
            description = str(desc_div)
    
    # Variants and pricing
    products_list = {p['id']: p for p in data.get('products', [])}
    variants_data = [v for v in data.get('productVariantData', []) if v.get('aktif', True)]
    
    if not products_list:
        return None
    
    # Find main product price (first active variant)
    main_id = data.get('mainVariantId')
    main_price_obj = products_list.get(main_id) or list(products_list.values())[0]
    
    satis = main_price_obj.get('satisFiyati', 0)
    satiskdv = main_price_obj.get('satisKDV', 0)
    indirim = main_price_obj.get('indirimliFiyati', 0)
    indirimkdv = main_price_obj.get('indirimliKDV', 0)
    
    fiyat = round(satis + satiskdv, 2)
    indirimli = round(indirim + indirimkdv, 2) if indirim > 0 else None
    
    # Images
    images = []
    for img in data.get('productImages', []):
        bpath = img.get('bigImagePath', '')
        if bpath:
            if bpath.startswith('//'):
                bpath = "https:" + bpath
            images.append(bpath)
    
    if not images and main_price_obj.get('spotResimBuyukYolu'):
        images.append(main_price_obj['spotResimBuyukYolu'])
    
    # Variant pricing
    variant_info = []
    for i, vd in enumerate(variants_data):
        vid = vd.get('urunID')
        tanim = vd.get('tanim', '')
        if vid in products_list:
            vp = products_list[vid]
            v_satis = vp.get('satisFiyati', 0) + vp.get('satisKDV', 0)
            v_ind = vp.get('indirimliFiyati', 0) + vp.get('indirimliKDV', 0)
            actual_price = round(v_ind if v_ind > 0 and v_ind < v_satis else v_satis, 2)
            variant_info.append({
                'olcu': tanim,
                'fiyat': actual_price,
                'is_default': (i == 0)
            })
    
    product_slug = url.strip('/').split('/')[-1]
    
    return {
        'title': data.get('productName', '').strip(),
        'slug': product_slug,
        'sku': data.get('stockCode', ''),
        'description': description,
        'fiyat': fiyat,
        'indirimli': indirimli,
        'images': images,
        'variants': variant_info,
        'cat_slug': cat_slug,
    }

def download_and_convert_image(url, slug, idx):
    from PIL import Image
    try:
        # Get HD image
        if 'cdn-cgi/image' in url:
            url = re.sub(r'width=\d+,quality=\d+', 'width=-,quality=85', url)
        elif 'width=' in url:
            url = re.sub(r'width=\d+', 'width=-', url)
        
        r = SESSION.get(url, timeout=20)
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            
            filename = f"{slug}-{idx}.webp"
            filepath = os.path.join(IMG_SAVE_DIR, filename)
            img.save(filepath, "WEBP", quality=85)
            return f"/img/products/{filename}"
    except Exception as e:
        print(f"    Image error: {str(e)[:80]}")
    return ""

def insert_product(product, cat_id):
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    
    try:
        # Check if already exists
        cur.execute('SELECT "Id" FROM "Urunler" WHERE "Slug" = %s OR "Baslik" = %s',
                    (product['slug'], product['title']))
        existing = cur.fetchone()
        if existing:
            print(f"  Skipping existing: {product['title']}")
            return False
        
        # Insert product
        cur.execute('''
            INSERT INTO "Urunler" 
            ("Baslik", "KisaAd", "Slug", "UrlYolu", "SKU", "Barkod", "Marka", "UrunTipi", "Etiketler", 
             "KisaAciklama", "Aciklama", "TeknikOzellikler", "MalzemeBilgisi", "BakimTalimati", "PaketlemeBilgisi", 
             "AnaGorselUrl", "StokDurumu", "Fiyat", "IndirimliFiyat", "Maliyet", "KdvOrani", 
             "UretimSuresiGun", "KargoyaVerilisSuresiGun", "TahminiTeslimSuresiGun",
             "AktifMi", "OneCikanMi", "YeniUrunMu", "KampanyaliMi", "AnaSayfadaGoster", 
             "Sira", "GoruntulenmeSayisi", "SatisSayisi", "FavoriSayisi", 
             "MinSiparisAdedi", "MaxSiparisAdedi", "SeoTitle", "SeoDescription", "SeoKeywords", 
             "KategoriId", "OlusturulmaTarihi", "SilindiMi")
            VALUES (%s, '', %s, %s, %s, '', 'MeteorGaleri', 'Cam Tablo', 'cam tablo',
                    '', %s, '', 'Cam', '', '',
                    '', 'Stokta', %s, %s, 0, 20,
                    3, 3, 5,
                    true, false, true, false, false,
                    0, 0, 0, 0,
                    1, 10, %s, %s, 'cam tablo',
                    %s, NOW(), false)
            RETURNING "Id"
        ''', (
            product['title'], product['slug'], product['slug'], product['sku'],
            product['description'],
            product['fiyat'], product['indirimli'],
            product['title'], product['title'],
            cat_id
        ))
        
        urun_id = cur.fetchone()[0]
        
        # Download images
        first_img = ""
        for idx, img_url in enumerate(product['images'][:5]):
            print(f"    Downloading image {idx+1}/{len(product['images'][:5])}: {img_url[:60]}...")
            local_path = download_and_convert_image(img_url, product['slug'], idx+1)
            if local_path:
                if idx == 0:
                    first_img = local_path
                cur.execute('''
                    INSERT INTO "UrunResimleri"
                    ("ResimYolu", "Baslik", "AltMetin", "MedyaTipi", "MedyaAlani", "VideoUrl", 
                     "ThumbnailYolu", "MobilResimYolu", "Etiketler", "Sira", "VarsayilanMi", 
                     "UrunSecenekId", "UrunId", "OlusturulmaTarihi", "SilindiMi")
                    VALUES (%s, %s, %s, 'Gorsel', 'Galeri', '', '', '', '', %s, %s, NULL, %s, NOW(), false)
                ''', (local_path, product['title'], product['title'], idx+1, (idx == 0), urun_id))
        
        if first_img:
            cur.execute('UPDATE "Urunler" SET "AnaGorselUrl" = %s WHERE "Id" = %s', (first_img, urun_id))
        
        # Insert variants
        for i, v in enumerate(product['variants']):
            cur.execute('''
                INSERT INTO "UrunSecenekleri"
                ("UrunId", "Olcu", "CerceveTipi", "CerceveRengi", "CerceveKalinligi", "MalzemeTuru", 
                 "Yon", "ParcaSayisi", "VaryantSku", "KisilestirmeMetni", "OzelTasarimNotu", 
                 "FiyatFarki", "SatisFiyati", "MaliyetFiyati", "StokAdedi", "UretimSuresiGun", 
                 "Desi", "GorselUrl", "AktifMi", "VarsayilanMi", "TukeninceGizle", 
                 "OnSipariseAcikMi", "Sira", "OlusturulmaTarihi", "SilindiMi")
                VALUES (%s, %s, '', '', '', '',
                        '', 1, '', '', '',
                        0, %s, 0, 100, 3,
                        1, '', true, %s, false,
                        false, %s, NOW(), false)
            ''', (urun_id, v['olcu'], v['fiyat'], v['is_default'], i+1))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"  DB Error: {str(e)[:120]}")
        return False
    finally:
        cur.close()
        conn.close()

def main():
    print("=== Cam Tablo Ürün Aktarımı ===\n")
    
    # Get local category IDs
    cat_id_map = get_cat_id_map()
    print(f"Found {len(cat_id_map)} categories in DB:")
    for slug, cid in cat_id_map.items():
        print(f"  {slug} -> ID: {cid}")
    
    # Get all cam-tablo product URLs from sitemap
    cam_urls = get_product_urls_from_all_sitemaps(list(TARGET_CATEGORIES.keys()))
    print(f"\nFound {len(cam_urls)} cam-tablo URLs in sitemaps.")
    
    # Process one-by-one (sequential, with delays to avoid rate limiting)
    success = 0
    skipped = 0
    failed = 0
    
    for i, url in enumerate(cam_urls):
        print(f"\n[{i+1}/{len(cam_urls)}] Processing: {url.split('/')[-1]}")
        
        product = get_product_info(url)
        if not product:
            # Not in our categories or failed
            skipped += 1
            continue
        
        cat_id = cat_id_map.get(product['cat_slug'])
        if not cat_id:
            print(f"  No local cat ID for slug: {product['cat_slug']}")
            skipped += 1
            continue
        
        print(f"  Title: {product['title']}")
        print(f"  Category: {product['cat_slug']} (ID: {cat_id})")
        print(f"  Price: {product['fiyat']} TL | Variants: {len(product['variants'])} | Images: {len(product['images'])}")
        
        if insert_product(product, cat_id):
            print(f"  ✓ Inserted successfully!")
            success += 1
        else:
            failed += 1
        
        # Be polite to the server - wait 1-2 seconds between requests
        time.sleep(1.5)
    
    print(f"\n=== TAMAMLANDI ===")
    print(f"  ✓ Başarıyla eklendi: {success}")
    print(f"  ⟳ Atlandı (kategori dışı/mevcut): {skipped}")
    print(f"  ✗ Hata: {failed}")

if __name__ == "__main__":
    main()
