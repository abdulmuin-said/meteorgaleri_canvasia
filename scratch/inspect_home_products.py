import psycopg2

def main():
    conn_str = "host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Find the "Yeni Eklenenler" section or ID = 1
        cur.execute('SELECT "Id", "Title" FROM public."HomePageSections" WHERE "Title" = \'Yeni Eklenenler\' OR "Id" = 1;')
        section = cur.fetchone()
        if not section:
            print("Section not found in DB.")
            return
            
        section_id, title = section
        print(f"Found Section: {title} (ID: {section_id})")
        
        # Get products in this section
        cur.execute('''
            SELECT u."Id", u."Baslik", u."AnaGorselUrl"
            FROM public."HomePageSectionProducts" hsp
            JOIN public."Urunler" u ON hsp."UrunId" = u."Id"
            WHERE hsp."SectionId" = %s
            ORDER BY hsp."SortOrder";
        ''', (section_id,))
        
        products = cur.fetchall()
        print(f"Total products in section: {len(products)}")
        for idx, (p_id, title, img_url) in enumerate(products, 1):
            print(f"{idx}. ID: {p_id} | Title: {title} | Image: {img_url}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
