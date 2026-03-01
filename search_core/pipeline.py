import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))


from search_core.hybrid_ranker import hybrid_search
from search_core.ai_reranker import rerank_with_ai
from search_core.click_learning import register_click, boost_scores_by_clicks
from search_core.history_learning import save_search, boost_scores_by_history
from search_core.auto_ranking import freshness_boost

def search_pipeline(query, user_history=[]):
    # 1️⃣ Hybrid Search
    results = hybrid_search(query)

    # 2️⃣ AI Reranker
    results = rerank_with_ai(query, results)

    # 3️⃣ Click Feedback
    results = boost_scores_by_clicks(results, query)

    # 4️⃣ Search History
    results = boost_scores_by_history(results, user_history)

    # 5️⃣ Freshness Boost
    results = freshness_boost(results)

    # 6️⃣ Kaydet
    save_search(query)

    return results