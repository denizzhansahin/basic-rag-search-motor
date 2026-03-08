import os

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from search_core.config import OLLAMA_MODEL, OLLAMA_BASE_URL,CROSS_ENCODER_MODEL


llm = ChatOllama(model=CROSS_ENCODER_MODEL, temperature=0.0, base_url = OLLAMA_BASE_URL)


def rerank_with_ai(query, results):
    if not results:
        return results

    top_results = results[:200]

    context = "\n".join([
        f"ID:{i} | Başlık: {r['title']} | İçerik: {r.get('content','')[:200]}"
        for i, r in enumerate(top_results)
    ])

    sys_prompt = """
Sen bir reranking modelisin.

Sorgu ile belgelerin alakasını 0.0 ile 1.0 arasında puanla.

SADECE şu formatta cevap ver:

ID|score

Örnek:
0|0.95
1|0.80

Başka hiçbir şey yazma.
"""

    user_prompt = f"Sorgu: {query}\n\nBelgeler:\n{context}"

    try:
        r = llm.invoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=user_prompt)
        ])

        reranked = {}

        for line in r.content.strip().split("\n"):
            if "|" in line:
                doc_id, score = line.split("|", 1)

                try:
                    reranked[int(doc_id.strip())] = float(score.strip())
                except:
                    continue

        for i, r_dict in enumerate(top_results):
            if i in reranked:
                r_dict['score'] += reranked[i] * 0.2

    except Exception as e:
        print(f"Reranker hatası: {e}")

    return sorted(results, key=lambda x: x['score'], reverse=True)



def rerank_with_ai_eski(query, results):
    if not results:
        return results

    top_results = results[:10]
    
    context = "\n".join([
        f"ID:{i} | Başlık: {r['title']} | URL: {r['url']}"
        for i, r in enumerate(top_results)
    ])

    sys_prompt = """
Sen bir sıralama (reranking) modelisin. 
Sorgu ile belgelerin alakasını 0.0 ile 1.0 arasında puanla. 
SADECE aşağıdaki formatta yanıt ver. Hiçbir ekstra kelime kullanma!
Format:
URL1|0.95
URL2|0.80
"""

    user_prompt = f"Sorgu: {query}\n\nBelgeler:\n{context}"

    try:
        r = llm.invoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=user_prompt)
        ])

        reranked = {}
        for line in r.content.strip().split("\n"):
            if "|" in line:
                url, score = line.split("|", 1)
                try:
                    reranked[url.strip()] = float(score.strip())
                except ValueError:
                    continue

        for r_dict in results:
            url = r_dict.get('url')
            if url in reranked:
                # Mevcut skora AI alaka skorunu ağırlıklı ekliyoruz
                r_dict['score'] += (reranked[url] * 0.2)
                
    except Exception as e:
        print(f"Reranker hatası: {e}")
        # Hata olursa orijinal sonuçları bozmadan geri dön

    return sorted(results, key=lambda x: x['score'], reverse=True)