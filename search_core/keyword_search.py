import psycopg2

DB_AYARLARI = {
    "host": "localhost",
    "database": "arama_motoru_db",
    "user": "postgres",
    "password": "gizlisifrem",
    "port": "5432"
}


def keyword_search(query, limit=30):

    conn = psycopg2.connect(**DB_AYARLARI)
    cur = conn.cursor()

    sql = """
    SELECT url,baslik,aciklama,icerik_ozeti,erisim_tarihi
    FROM taranan_linkler
    WHERE to_tsvector('simple',
    baslik||' '||
    aciklama||' '||
    icerik_ozeti)
    @@ plainto_tsquery(%s)
    LIMIT %s
    """

    cur.execute(sql,(query,limit))

    rows=cur.fetchall()

    cur.close()
    conn.close()

    return rows