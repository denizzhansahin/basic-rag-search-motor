import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import math

# Path Ayarları
base_path = Path(__file__).resolve().parent
sys.path.append(str(base_path.parent))

from search_core.hybrid_ranker import hybrid_search
from search_core.click_learning import boost_scores_by_clicks, register_click
from search_core.history_learning import boost_scores_by_history
from search_core.auto_ranking import freshness_boost
from search_core.ai_engine import ai_answer
from search_core.ai_reranker import rerank_with_ai

# -------------------- UI CONFIG --------------------
st.set_page_config(page_title="Space Teknopoli Search", layout="wide", page_icon="🛸")

with st.sidebar:
    st.title("⚙️ Ayarlar")
    total_pool_size = st.number_input("Arka Planda Taranacak Toplam Kayıt", value=100, step=50)
    results_per_page = st.slider("Sayfa Başına Sonuç", 5, 20, 10)
    ai_mode = st.toggle("Yapay Zeka (RAG) Aktif", value=True)
    st.divider()
    st.info("Space Teknopoli: M4 Power 🚀 - Önbellekli Mimari Aktif")

# ==========================================
# YAPAY ZEKA ÖNBELLEK FONKSİYONU
# ==========================================
# ttl=600 demek, bu aramanın sonucu 10 dakika (600 saniye) boyunca hafızada tutulacak demektir.
# _all_results başına alt çizgi koyduk ki Streamlit yüzlerce satırlık listeyi hashlemeye çalışıp zaman kaybetmesin.
@st.cache_data(ttl=600, show_spinner=False)
def run_ai_analysis_cached(query, _all_results):
    ranked_for_ai = rerank_with_ai(query, _all_results[:15])
    response_from_ai = ai_answer(query, ranked_for_ai)
    return ranked_for_ai, response_from_ai

st.title("🛸 Space Teknopoli")
query = st.text_input("Arama Yap", placeholder="Teknoloji, yazılım, uzay vb. ...")

if query:
    # Yer Tutucular
    ai_status_placeholder = st.empty()
    ai_summary_placeholder = st.empty()
    ai_top_results_placeholder = st.empty()
    ai_tabs_placeholder = st.empty()
    
    st.markdown("---")
    classic_results_placeholder = st.empty()

    # ==========================================
    # 1. AŞAMA: HAVUZU DOLDUR (Hızlı Arama)
    # ==========================================
    fast_results = hybrid_search(query) 
    fast_results = boost_scores_by_clicks(fast_results, query)
    fast_results = boost_scores_by_history(fast_results, [])
    fast_results = freshness_boost(fast_results)
    
    all_results = fast_results[:total_pool_size]
    total_results_count = len(all_results)

    # ==========================================
    # 2. AŞAMA: SAYFALAMA (PAGINATION) MANTIĞI
    # ==========================================
    if total_results_count > 0:
        total_pages = math.ceil(total_results_count / results_per_page)
        
        current_page = st.selectbox("Sayfa", range(1, total_pages + 1))
        
        start_idx = (current_page - 1) * results_per_page
        end_idx = start_idx + results_per_page
        
        page_results = all_results[start_idx:end_idx]

        with classic_results_placeholder.container():
            st.markdown(f"### 🗄️ Klasik Sonuçlar ({total_results_count} sonuçtan {start_idx+1}-{min(end_idx, total_results_count)} arası)")
            for item in page_results:
                st.markdown(f"**[{item.get('title', 'Başlık Yok')}]({item.get('url', '#')})**")
                st.caption(f"Skor: {item.get('score', 0):.4f} | {item.get('url', '#')}")
                st.write(f"{item.get('content', '')[:200]}...")
                
                # Tıklama Kaydı
                if st.button("🔗 Ziyaret Et", key=f"classic_{item.get('url', '#')}_{start_idx}"):
                    try:
                        register_click(query, item.get('url', '#'))
                        st.success("Tıklandı!")
                    except Exception as e:
                        st.error("Tıklama kaydedilemedi.")
                st.markdown("---")

    # ==========================================
    # 3. AŞAMA: YAPAY ZEKA (Önbellekli Çağrı)
    # ==========================================
    if ai_mode and all_results:
        with ai_status_placeholder.container():
            # Eğer veri önbellekte varsa bu spinner sadece 0.1 saniye görünür ve kaybolur.
            # Yoksa (ilk aramaysa) AI modeli çalışır.
            with st.spinner("✨ Space Teknopoli AI sonuçları analiz ediyor..."):
                ai_ranked_results, ai_response = run_ai_analysis_cached(query, all_results)
                
                summary = ai_response.get('summary', 'Özet oluşturulamadı.')
                suggestions = ai_response.get('suggestions', [])

        ai_status_placeholder.empty()

        with ai_summary_placeholder.container():
            st.markdown("### ✨ AI Özeti")
            st.info(summary)
            
        with ai_top_results_placeholder.container():
            st.markdown("### 🚀 AI Destekli Öne Çıkanlar")
            cols = st.columns(1)
            for item in ai_ranked_results[:5]:
                st.success(f"**{item.get('title')}**\n\n{item.get('content')[:180]}...\n\n[Kaynağa Git]({item.get('url')})")

        with ai_tabs_placeholder.container():
            tab1, tab2 = st.tabs(["💡 AI Önerileri", "📊 Skor Analizi"])
            with tab1:
                if suggestions:
                    for sug in suggestions:
                        st.markdown(f"🔗 **[{sug.get('title')}]({sug.get('url')})**")
                else:
                    st.write("Daha fazla öneri bulunamadı.")
            with tab2:
                # Ekrana basarken karmaşayı önlemek için pandas tablosunu temizliyoruz
                df = pd.DataFrame(all_results[:20])
                if not df.empty and "title" in df.columns:
                    st.dataframe(df[["title", "score", "url"]], use_container_width=True)

    elif not all_results:
        st.warning("Sonuç bulunamadı.")