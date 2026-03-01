import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

import streamlit as st
import psycopg2
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import pandas as pd

# ---------------- CONFIG ----------------

DB_AYARLARI = {
    "host": "localhost",
    "database": "arama_motoru_db",
    "user": "postgres",
    "password": "gizlisifrem",
    "port": "5432"
}

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "ollama_my_rag_collection"

# ---------------- SEARCH ENGINE ----------------

class SearchEngine:

    def __init__(self):

        self.client = QdrantClient(url=QDRANT_URL)

        self.embeddings = OllamaEmbeddings(
            model="embeddinggemma"
        )

        self.llm = ChatOllama(
            model="gemma3:4b",
            temperature=0.3
        )

    # -------- KEYWORD SEARCH --------

    def keyword_search(self, query, limit=10):

        try:

            conn = psycopg2.connect(**DB_AYARLARI)
            cur = conn.cursor()

            sql = """
            SELECT url, baslik, aciklama, icerik_ozeti, erisim_tarihi
            FROM taranan_linkler
            WHERE baslik ILIKE %s
            OR aciklama ILIKE %s
            OR icerik_ozeti ILIKE %s
            ORDER BY erisim_tarihi DESC
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

        except Exception as e:

            print(e)

            return []


    # -------- VECTOR SEARCH --------

    def vector_search(self, query, limit=15):

        query_vector = self.embeddings.embed_query(query)

        result = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True
        )

        return result.points


    # -------- HYBRID RANKING --------

    def hybrid_ranker(self, query, alpha=0.7):

        v_results = self.vector_search(query)

        k_results = self.keyword_search(query)

        merged = {}

        # VECTOR RESULTS

        for res in v_results:

            url = res.payload.get(
                "metadata", {}
            ).get("source_url")

            if not url:
                continue

            merged[url] = {

                "url": url,

                "title":

                res.payload.get(
                    "metadata", {}
                ).get("title","Başlık Yok"),

                "content":

                res.payload.get(
                    "page_content",""),

                "score":

                float(res.score) * alpha,

                "source":

                "Semantic",

                "date":

                res.payload.get(
                    "metadata",{}
                ).get("scraped_at","")
            }


        # KEYWORD RESULTS

        for row in k_results:

            url,baslik,aciklama,icerik,tarih = row

            if url in merged:

                merged[url]["score"] += (1-alpha)

                merged[url]["source"]="Hybrid"

            else:

                merged[url]={

                    "url":url,

                    "title":baslik,

                    "content":

                    icerik if icerik else aciklama,

                    "score":

                    0.4*(1-alpha),

                    "source":

                    "Keyword",

                    "date":str(tarih)

                }


        return sorted(
            merged.values(),
            key=lambda x:x["score"],
            reverse=True
        )


# ---------------- UI ----------------

st.set_page_config(
    page_title="Space Teknopoli Search",
    layout="wide"
)

engine=SearchEngine()

# -------- SIDEBAR --------

with st.sidebar:

    st.title("⚙️ Ayarlar")

    search_depth=st.slider(
        "Sonuç Sayısı",
        5,
        50,
        20
    )

    ai_mode=st.toggle(
        "AI Özeti",
        value=True
    )

    st.divider()

    st.subheader("Arama Motoru")

    st.write("✔ Vector Search")

    st.write("✔ Keyword Search")

    st.write("✔ Hybrid Ranking")

    st.write("✔ RAG AI")


# -------- MAIN --------

st.title("🛸 Space Teknopoli Search Engine")

st.caption("AI destekli hibrit arama motoru")

query=st.text_input(
    "",
    placeholder="Bir şey ara..."
)


if query:

    with st.spinner("Aranıyor..."):

        results=engine.hybrid_ranker(
            query,
            alpha=0.7
        )

    tab1,tab2,tab3=st.tabs(

        [

        "🤖 AI Cevap",

        "🌐 Sonuçlar",

        "📊 Analiz"

        ]

    )


    # ---------- TAB 1 AI ----------

    with tab1:

        if ai_mode and results:


            st.subheader("AI Özet")


            context="\n\n".join([

                f"{r['title']}:\n{r['content'][:800]}"

                for r in results[:5]

            ])


            sys_prompt="""

Sen gelişmiş bir arama motoru yapay zekasısın.

Cevap yapısı:

Kısa özet

Detaylı açıklama

Önemli maddeler

"""


            user_prompt=f"""

Soru:

{query}

Veriler:

{context}

"""


            response=engine.llm.invoke(

                [

                SystemMessage(content=sys_prompt),

                HumanMessage(content=user_prompt)

                ]

            )


            st.write(response.content)


            st.divider()


            st.subheader("AI Önerileri")


            suggest_prompt=f"""

Kullanıcı şunu aradı:

{query}

5 yeni arama önerisi üret.

"""


            sug=engine.llm.invoke(

                [

                HumanMessage(content=suggest_prompt)

                ]

            )


            st.write(sug.content)



        else:

            st.warning("AI kapalı")


    # ---------- TAB 2 RESULTS ----------

    with tab2:


        if results:


            st.subheader(

                f"{len(results)} sonuç bulundu"

            )


            best=results[0]


            st.info(

                f"""

### En iyi sonuç

{best['title']}

{best['content'][:400]}

"""

            )


            st.divider()


            for item in results:


                st.markdown(

                    f"""

### [{item['title']}]({item['url']})

{item['url']}

{item['content'][:300]}...

"""

                )


                c1,c2,c3=st.columns(3)


                c1.caption(

                    f"Skor: {round(item['score'],2)}"

                )


                c2.caption(

                    item["source"]

                )


                c3.caption(

                    item["date"]

                )


                st.divider()


    # ---------- TAB 3 ANALYTICS ----------


    with tab3:


        if results:


            df=pd.DataFrame(results)


            st.subheader("Skor Analizi")


            st.bar_chart(

                df.set_index("title")["score"]

            )


            avg_score=sum(

                r["score"]

                for r in results

            )/len(results)


            st.metric(

                "Ortalama Alaka",

                round(avg_score,2)

            )


            st.dataframe(df)