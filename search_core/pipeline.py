import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


from search_core.hybrid_ranker import hybrid_search
from search_core.ai_reranker import rerank_with_ai
from search_core.click_learning import register_click, boost_scores_by_clicks
from search_core.history_learning import save_search, boost_scores_by_history
from search_core.auto_ranking import freshness_boost



from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from search_core.config import OLLAMA_MODEL, OLLAMA_BASE_URL

# AI modeli: sadece sorgu anlama ve iyileştirme
#qu_llm = ChatOllama(model=OLLAMA_MODEL, temperature=0.0, base_url=OLLAMA_BASE_URL)



def query_understanding(query):
    sys_prompt = """
Sen bir Query Understanding (Sorgu Anlama) modelisin.
Kullanıcının sorgusunu al ve arama motoruna en uygun hale getir.
- Gereksiz kelimeleri çıkar.
- Anahtar kelimeleri güçlendir.
- Kullanıcının ne sormak istediğini koru.
SADECE optimize edilmiş sorguyu geri ver.
"""

    user_prompt = f"Sorgu: {query}"

    try:
        r = qu_llm.invoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=user_prompt)
        ])
        optimized_query = r.content.strip()
        return optimized_query
    except Exception as e:
        print(f"QUL hatası: {e}")
        return query  # Hata olursa orijinal sorguyu döndür


def search_pipeline(query, user_history=[]):
    # 0️⃣ Query Understanding Layer
    #optimized_query = query_understanding(query)
    optimized_query = query

    # 1️⃣ Hybrid Search
    results = hybrid_search(optimized_query)

    # 2️⃣ AI Reranker
    results = rerank_with_ai(optimized_query, results)

    # 3️⃣ Click Feedback
    results = boost_scores_by_clicks(results, optimized_query)

    # 4️⃣ Search History
    results = boost_scores_by_history(results, user_history)

    # 5️⃣ Freshness Boost
    results = freshness_boost(results)

    # 6️⃣ Kaydet
    save_search(optimized_query)

    return results

