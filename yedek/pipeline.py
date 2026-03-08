import asyncio
import redis.asyncio as redis
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from search_core.hybrid_ranker import hybrid_search
from search_core.ai_reranker import rerank_with_ai
from search_core.click_learning import boost_scores_by_clicks
from search_core.history_learning import boost_scores_by_history, save_search
from search_core.auto_ranking import freshness_boost
from search_core.config import OLLAMA_MODEL, OLLAMA_BASE_URL

# Redis cache
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# LLM modeli
qu_llm = ChatOllama(model=OLLAMA_MODEL, temperature=0.0, base_url=OLLAMA_BASE_URL)


async def query_understanding_async(query: str) -> str:
    """LLM ile sorguyu optimize eder. Cache varsa direkt döner."""
    cache_key = f"optimized_query:{query}"
    cached = await redis_client.get(cache_key)
    if cached:
        return cached

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
        # Cache'e kaydet (1 gün geçerli)
        await redis_client.set(cache_key, optimized_query, ex=86400)
        return optimized_query
    except Exception as e:
        print(f"QUL hatası: {e}")
        return query


async def search_pipeline_async(query: str, user_history=[]):
    """
    Hızlı arama ve async LLM optimizasyonu:
    - İlk önce raw sorgu ile hızlı hybrid search yapar
    - LLM query understanding arka planda çalışır
    - Sonuçları rerank, click/history boost ve freshness ile iyileştirir
    """
    # 1️⃣ Hızlı Hybrid Search
    results = hybrid_search(query)

    # 2️⃣ Async LLM sorgu iyileştirmesi
    optimized_query_task = asyncio.create_task(query_understanding_async(query))

    # 3️⃣ AI Reranker
    results = rerank_with_ai(query, results)

    # 4️⃣ Click Feedback
    results = boost_scores_by_clicks(results, query)

    # 5️⃣ Search History
    results = boost_scores_by_history(results, user_history)

    # 6️⃣ Freshness Boost
    results = freshness_boost(results)

    # 7️⃣ Kaydet
    save_search(query)

    # 8️⃣ LLM ile optimize edilmiş sorguyu al
    optimized_query = await optimized_query_task
    print(f"🔹 Optimize edilmiş sorgu: {optimized_query}")

    return results, optimized_query