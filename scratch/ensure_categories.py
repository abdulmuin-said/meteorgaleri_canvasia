import psycopg2, sys

sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect("host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?")
cur = conn.cursor()

# Check and create "Cam Kesme Tahtası" and "Ayna" if they don't exist
categories_to_check = [
    ("Cam Kesme Tahtası", "cam-kesme-tahtasi", ""),
    ("Ayna", "ayna", "")
]

for ad, slug, aciklama in categories_to_check:
    cur.execute('SELECT "Id" FROM "Kategoriler" WHERE "Slug" = %s', (slug,))
    row = cur.fetchone()
    if not row:
        print(f"Creating category: {ad}")
        cur.execute('''
            INSERT INTO "Kategoriler" 
            ("Ad", "KisaAciklama", "Aciklama", "GorselUrl", "BannerUrl", "Sira", "AktifMi", "AnaSayfadaGoster", "SeoTitle", "SeoDescription", "SeoKeywords", "Slug", "OlusturulmaTarihi", "SilindiMi")
            VALUES (%s, %s, '', '', '', 0, true, true, %s, '', '', %s, NOW(), false)
            RETURNING "Id"
        ''', (ad, aciklama, ad, slug))
        cat_id = cur.fetchone()[0]
        print(f"Created {ad} with ID {cat_id}")
    else:
        print(f"Category {ad} already exists with ID {row[0]}")

conn.commit()
cur.close()
conn.close()
