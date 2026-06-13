import psycopg2, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect("host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?")
cur = conn.cursor()
cur.execute('''
    SELECT u."Baslik", u."Fiyat", k."Ad" as "Kategori", u."OlusturulmaTarihi"
    FROM "Urunler" u
    JOIN "Kategoriler" k ON u."KategoriId" = k."Id"
    WHERE u."OlusturulmaTarihi" > NOW() - INTERVAL '2 hours'
    ORDER BY u."OlusturulmaTarihi" DESC
    LIMIT 30
''')
rows = cur.fetchall()
print(f"Son 2 saatte eklenen ürünler: {len(rows)}")
for r in rows:
    print(f"  {r[3].strftime('%H:%M:%S')} | {r[2]} | {r[0][:60]} | {r[1]} TL")
cur.close()
conn.close()
