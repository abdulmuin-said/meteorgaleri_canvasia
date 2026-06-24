import psycopg2

def main():
    conn_str = "host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        cur.execute('SELECT "Id", "Title", "SectionType" FROM public."HomePageSections" ORDER BY "SortOrder";')
        sections = cur.fetchall()
        for sec_id, title, sec_type in sections:
            cur.execute('SELECT COUNT(*) FROM public."HomePageSectionProducts" WHERE "SectionId" = %s;', (sec_id,))
            cnt = cur.fetchone()[0]
            print(f"Section ID: {sec_id} | Title: {title} | Type: {sec_type} | Manual Products Count: {cnt}")
            
            # If it's a manual product block or if it has products, let's list them
            if cnt > 0:
                cur.execute('''
                    SELECT u."Id", u."Baslik", u."AnaGorselUrl"
                    FROM public."HomePageSectionProducts" hsp
                    JOIN public."Urunler" u ON hsp."UrunId" = u."Id"
                    WHERE hsp."SectionId" = %s
                    ORDER BY hsp."SortOrder";
                ''', (sec_id,))
                for p_id, p_title, img_url in cur.fetchall():
                    print(f"  -> Prod ID: {p_id} | Title: {p_title} | Image: {img_url}")
                    
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
