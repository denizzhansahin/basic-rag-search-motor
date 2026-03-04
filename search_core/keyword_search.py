import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

import psycopg2

from search_core.config import DB_AYARLARI




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