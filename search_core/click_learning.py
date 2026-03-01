import psycopg2

DB_AYARLARI = {
    "host":"localhost","database":"arama_motoru_db",
    "user":"postgres","password":"gizlisifrem","port":"5432"
}

def register_click(query, url):
    conn=psycopg2.connect(**DB_AYARLARI)
    cur=conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id SERIAL PRIMARY KEY,
            query TEXT,
            url TEXT,
            click_time TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("INSERT INTO clicks (query,url) VALUES (%s,%s)", (query,url))
    conn.commit()
    cur.close()
    conn.close()

def boost_scores_by_clicks_eski(results, query):
    conn=psycopg2.connect(**DB_AYARLARI)
    cur=conn.cursor()
    cur.execute("SELECT url, COUNT(*) FROM clicks WHERE query=%s GROUP BY url", (query,))
    click_data = {url:cnt for url,cnt in cur.fetchall()}
    cur.close()
    conn.close()

    for r in results:
        r['score'] += click_data.get(r['url'],0)*0.05  # her tıklama puanı 0.05 artırır
    return sorted(results, key=lambda x: x['score'], reverse=True)


def boost_scores_by_clicks(results, query):
    import psycopg2
    from search_core.config import DB_AYARLARI

    try:
        conn = psycopg2.connect(**DB_AYARLARI)
        cur = conn.cursor()
        cur.execute("SELECT url, COUNT(*) FROM clicks WHERE query=%s GROUP BY url", (query,))
        clicks_data = cur.fetchall()
        cur.close()
        conn.close()
    except psycopg2.errors.UndefinedTable:
        # Eğer tablo yoksa, sadece original skor döndür
        return results

    # clicks_data var ise skoru yükselt
    clicks_dict = {url: count for url, count in clicks_data}
    for r in results:
        if r['url'] in clicks_dict:
            r['score'] += clicks_dict[r['url']] * 0.05  # ufak boost
    return results