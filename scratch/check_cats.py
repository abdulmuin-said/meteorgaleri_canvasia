import psycopg2, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect("host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?")
cur = conn.cursor()
cur.execute('''
    SELECT k."Ad", k."GorselUrl", k."Slug", COUNT(u."Id") as urun_sayisi
    FROM "Kategoriler" k
    LEFT JOIN "Urunler" u ON u."KategoriId" = k."Id" AND u."SilindiMi" = false
    WHERE k."ParentKategoriId" IS NOT NULL
    GROUP BY k."Id", k."Ad", k."GorselUrl", k."Slug"
    ORDER BY urun_sayisi DESC
''')
for row in cur.fetchall():
    gorsel = row[1] or "(yok)"
    print(f"{str(row[0])[:40]:40} | {str(row[3]):4} urun | {gorsel[:50]}")
cur.close()
conn.close()
