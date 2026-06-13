import psycopg2

def check_db():
    conn_str = "host=localhost port=5432 dbname=kanvasdb user=postgres password=h3ker6655?"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        cur.execute('SELECT "Id", "Ad" FROM "Kategoriler" WHERE "Ad" ILIKE \'%Cam Tablo%\'')
        rows = cur.fetchall()
        print("Categories matching 'Cam Tablo':", rows)
        
        cur.execute('SELECT "Id", "Ad" FROM "Kategoriler" WHERE "Ad" ILIKE \'%Cam%\'')
        rows = cur.fetchall()
        print("Categories matching 'Cam':", rows)
        
        cur.close()
        conn.close()
    except Exception as e:
        print("DB Error:", str(e))

if __name__ == "__main__":
    check_db()
