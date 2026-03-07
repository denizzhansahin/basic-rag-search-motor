# python_api/search_core/ai_chat_engine.py
import asyncio
import json
import os
from langchain_ollama import OllamaLLM
from python_api.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from search_core.pipeline import search_pipeline


# Karar verici (Router) için model (Sıcaklık 0, çok net ve kurallı cevap versin diye)
router_llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)

# Sohbet edecek model (Sıcaklık 0.3, biraz daha yaratıcı olabilir)
chat_llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.3)

async def should_search(query, history):
    if not history:
        return True 
        
    prompt = f"""Sen bir arama motoru yönlendiricisisin. Kesin ve net karar vermelisin.
    
Son Konuşulanlar: {history[-2:] if len(history) >= 2 else history}
Kullanıcının YENİ Sorusu: "{query}"

KURALLAR:
1. YENİ BİR KONU: Eğer yeni soru, son konuşulanlardan tamamen farklı bir konuyorsa (örneğin son konu "telefon" iken yeni soru "Denizhan kimdir", "uçak bileti", "hava durumu" ise) -> KESİNLİKLE "EVET" yaz.
2. GÜNCEL BİLGİ/ÖZEL İSİM: Soru bir kişinin kim olduğunu, fiyatları, güncel bir veriyi veya bir markayı soruyorsa -> KESİNLİKLE "EVET" yaz.
3. BAĞLAMSAL DEVAM: SADECE eğer kullanıcı "neden böyle?", "bunu biraz daha açıkla", "ne demek istedin", "özetle" gibi GÖZÜ KAPALI cevaplanabilecek geçmişe dönük bir soru sorduysa -> "HAYIR" yaz.

SADECE "EVET" veya "HAYIR" YAZ. Başka tek bir harf veya nokta bile kullanma."""

    cevap = await asyncio.to_thread(router_llm.invoke, prompt)
    karar = "EVET" in cevap.upper()
    print(f"🧠 [ROUTER KARARI] Soru: '{query}' -> AI Cevabı: '{cevap.strip()}' -> Arama Yapılacak Mı? {karar}")
    return karar

async def process_ai_chat(job_id, redis_client, query, history, file_b64, file_type):
    print(f"🤖 [AI CHAT BAŞLADI] Soru: {query}")
    try:
        sources = []
        context_text = ""

        # 1. YÖNLENDİRİCİ KARARI
        needs_search = await should_search(query, history)

        # 2. EĞER ARAMA GEREKİYORSA QDRANT/POSTGRES'İ ÇALIŞTIR
        if needs_search:
            print("🔍 Arama motoru tetiklendi...")
            search_results = await asyncio.to_thread(search_pipeline, query, [])
            # React tarafındaki kutucuklar için en iyi 4 sonucu alalım
            top_results = search_results[:4] 
            sources = top_results 
            
            context_text = "Bulunan Yeni Kaynaklar:\\n"
            for r in top_results:
                 if isinstance(r, dict):
                     context_text += f"- {r.get('title')}: {r.get('content')[:300]}\\n"

        # 3. DOSYA/GÖRSEL İŞLEME
        if file_b64:
             # Eğer Ollama Vision kullanıyorsan base64'ü modele verebiliriz.
             # Şimdilik modele dosya yüklendiğini bildiriyoruz:
             context_text += f"\\n[DİKKAT: Kullanıcı {file_type} formatında bir dosya yükledi.]"

        # 4. CEVABI ÜRET
        chat_prompt = f"""Önceki Sohbet: {history}\\n\\nEk Kaynaklar: {context_text}\\n\\nKullanıcı: {query}\\nAsistan:"""
        ai_response = await asyncio.to_thread(chat_llm.invoke, chat_prompt)

        # 5. REACT'A GÖNDER
        response_payload = {
            "type": "AI_CHAT_REPLY",
            "message": ai_response,
            "sources": sources, 
            "didSearch": needs_search 
        }
        
        # DÜZELTME BURADA: json.dumps içine 'default=str' ekledik!
        await redis_client.publish(f"job:{job_id}", json.dumps(response_payload, default=str))
        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "DONE"}))

    except Exception as e:
        print(f"❌ [AI CHAT ERROR] {e}")
        # Buraya da önlem olarak ekleyelim
        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "ERROR", "message": str(e)}, default=str))