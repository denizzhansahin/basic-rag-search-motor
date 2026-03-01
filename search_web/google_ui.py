import sys
from pathlib import Path


# Base path
base_path = Path(__file__).resolve().parent
sys.path.append(str(base_path.parent))


import streamlit as st
from search_core.pipeline import search_pipeline


# ----------------- Streamlit Konfig -----------------
st.set_page_config(
    page_title="Space Teknopoli Search",
    layout="wide",
    page_icon="🛸"
)

# CSS
st.markdown("""
<style>
.card {padding:1rem;margin-bottom:1rem;border-radius:0.75rem;
       background:linear-gradient(145deg,#f5f7fa,#e4e7eb);
       box-shadow:5px 5px 15px #d1d5db, -5px -5px 15px #ffffff;}
.card:hover {box-shadow: inset 2px 2px 5px #d1d5db, inset -2px -2px 5px #ffffff;}
.ai-panel {background:linear-gradient(145deg,#dce7ff,#c4d7ff);padding:1rem;border-radius:0.75rem;height:100%;overflow-y:auto;}
</style>
""", unsafe_allow_html=True)

# Layout
st.title("🛸 Space Teknopoli Search Engine")
st.caption("AI destekli hibrit arama motoru")

query = st.text_input("🔍 Aramak istediğiniz konuyu girin...", "")
if query:
    with st.spinner("Aranıyor..."):
        results = search_pipeline(query, user_history=[])

    col_main, col_ai = st.columns([3,1])

    # Ana panel
    with col_main:
        st.subheader(f"🌐 {len(results)} sonuç bulundu")
        if results:
            best = results[0]
            st.info(f"### En iyi sonuç\n[{best['title']}]({best['url']})\n{best['content'][:400]}...")
            for item in results:
                st.markdown(f"""
                <div class="card">
                    <h4><a href="{item['url']}" target="_blank">{item['title']}</a></h4>
                    <small>{item['url']}</small>
                    <p>{item['content'][:300]}...</p>
                    <div style="display:flex; justify-content:space-between;">
                        <span>Skor: {item['score']:.2f}</span>
                        <span>Kaynak: {item['source']}</span>
                        <span>{item['date']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.subheader("📊 Skor ve Detaylar")
            import pandas as pd
            df = pd.DataFrame(results)
            st.dataframe(df[["title","score","source","date","url"]])

    # AI panel
    with col_ai:
        st.subheader("🤖 AI Paneli")
        if results:
            from search_core.ai_engine import generate_ai_response
            context = "\n\n".join([f"{r['title']}:\n{r['content'][:800]}" for r in results[:5]])
            sys_prompt = "Sen gelişmiş bir arama motoru yapay zekasısın. Kısa özet, detaylı açıklama, önemli maddeler."
            user_prompt = f"Soru: {query}\nVeriler:\n{context}"
            ai_response = generate_ai_response(sys_prompt, user_prompt)
            st.markdown(f"### AI Özet\n{ai_response['summary']}")
            st.markdown(f"### AI Önerileri")
            for link, title in ai_response['suggestions']:
                st.markdown(f"- [{title}]({link})")