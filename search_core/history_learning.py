import psycopg2

DB_AYARLARI = {
    "host":"localhost","database":"arama_motoru_db",
    "user":"postgres","password":"gizlisifrem","port":"5432"
}

def save_search(query):
    conn=psycopg2.connect(**DB_AYARLARI)
    cur=conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id SERIAL PRIMARY KEY,
            query TEXT,
            search_time TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("INSERT INTO search_history (query) VALUES (%s)", (query,))
    conn.commit()
    cur.close()
    conn.close()

def boost_scores_by_history(results, user_history):
    """
    user_history: ['ai', 'machine learning', ...]
    """
    for r in results:
        for h in user_history:
            if h.lower() in r['title'].lower() or h.lower() in r['content'].lower():
                r['score'] += 0.05
    return sorted(results, key=lambda x: x['score'], reverse=True)