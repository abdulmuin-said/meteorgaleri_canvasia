import psycopg2

def main():
    conn_str = "host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'HomePageSectionProducts';
        """)
        for row in cur.fetchall():
            print(row)
            
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
