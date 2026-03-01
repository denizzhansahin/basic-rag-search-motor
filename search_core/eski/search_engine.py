import psycopg2
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings

# ---------- CONFIG ----------

DB_AYARLARI = {
    "host": "localhost",
    "database": "arama_motoru_db",
    "user": "postgres",
    "password": "gizlisifrem",
    "port": "5432"
}

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "ollama_my_rag_collection"


class SearchEngine:

    def __init__(self):

        self.client = QdrantClient(url=QDRANT_URL)

        self.embeddings = OllamaEmbeddings(
            model="embeddinggemma"
        )

    # ---------- KEYWORD ----------

    def keyword_search(self, query, limit=10):

        conn = psycopg2.connect(**DB_AYARLARI)

        cur = conn.cursor()

        sql = """
        SELECT url, baslik, aciklama, icerik_ozeti, erisim_tarihi
        FROM taranan_linkler
        WHERE baslik ILIKE %s
        OR aciklama ILIKE %s
        OR icerik_ozeti ILIKE %s
        LIMIT %s
        """

        cur.execute(sql,
                    (f'%{query}%',
                     f'%{query}%',
                     f'%{query}%',
                     limit))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows


    # ---------- VECTOR ----------

    def vector_search(self, query, limit=20):

        query_vector = self.embeddings.embed_query(query)

        result = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True
        )

        return result.points


    # ---------- HYBRID ----------

    def hybrid_search(self, query, alpha=0.7):

        v_results = self.vector_search(query)
        k_results = self.keyword_search(query)

        merged = {}

        # VECTOR

        for r in v_results:

            url = r.payload.get(
                "metadata",{}
            ).get("source_url")

            if not url:
                continue

            merged[url] = {

                "title":

                r.payload.get(
                    "metadata",{}
                ).get("title","Başlık yok"),

                "url":url,

                "content":

                r.payload.get(
                    "page_content",""),

                "score":

                float(r.score)*alpha,

                "source":

                "Semantic"
            }


        # KEYWORD

        for row in k_results:

            url,title,desc,content,date=row

            if url in merged:

                merged[url]["score"]+=(1-alpha)

                merged[url]["source"]="Hybrid"

            else:

                merged[url]={

                    "title":title,

                    "url":url,

                    "content":

                    content if content else desc,

                    "score":

                    0.3,

                    "source":"Keyword"
                }


        return sorted(
            merged.values(),
            key=lambda x:x["score"],
            reverse=True
        )