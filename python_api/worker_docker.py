import sys
import json
import asyncio
import os
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal
import uuid
import redis.asyncio as redis

# Kütüphane yollarını ekle
base_path = Path(__file__).resolve().parent.parent / "python_api"
sys.path.append(str(base_path))

from python_api.config import REDIS_HOST, REDIS_PORT
from search_core.pipeline import search_pipeline
from search_core.ai_reranker import rerank_with_ai
from search_core.ai_engine import ai_answer
from ollama_run.ollama_rag_read import soru_sor

# JSON Serileştirici (Hata almamak için)
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def serialize_results(results):
    for r in results:
        # Eğer sonuç bir listeyse (Postgres'ten geldiği gibi)
        if isinstance(r, list) and len(r) > 4:
             if isinstance(r[4], (datetime, date)):
                 r[4] = r[4].isoformat()
        # Eğer sonuç bir dict ise
        elif isinstance(r, dict):
            if 'date' in r and isinstance(r['date'], (datetime, date)):
                r['date'] = r['date'].isoformat()
    return results

def format_history(history_list):
    formatted = ""
    for msg in history_list:
        role = "Kullanıcı" if msg.get('role') == 'user' else "Asistan"
        formatted += f"{role}: {msg.get('content')}\n"
    return formatted

# Redis Bağlantısı
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# --- ANA İŞLEMLER ---

async def process_search(job_id, query):
    print(f"⚙️ [WORKER] Arama ve AI Analizi Başladı: {query}")
    try:
        # 1. Geniş Arama (Postgres/Qdrant)
        all_results = await asyncio.to_thread(search_pipeline, query, [])
        safe_results = serialize_results(all_results[:200])
        
        # Hemen ilk sonuçları gönder (Kullanıcı beklemesin)
        await redis_client.publish(f"job:{job_id}", json.dumps({
            "type": "FULL_RESULTS", 
            "data": safe_results
        }, default=json_serial))

        # 2. AI Rerank (En iyi 20 veriyi tekrar sırala)
        print(f"🧠 [AI] Reranking yapılıyor...")
        top_20 = all_results[:20]
        ai_ranked_results = await asyncio.to_thread(rerank_with_ai, query, top_20)

        # 3. AI Özetleme ve Tavsiyeler
        print(f"✍️ [AI] Özet ve tavsiyeler üretiliyor...")
        ai_response = await asyncio.to_thread(ai_answer, query, ai_ranked_results)
        
        # AI Sonuçlarını gönder
        await redis_client.publish(f"job:{job_id}", json.dumps({
            "type": "AI_RESULTS",
            "summary": ai_response.get("summary", ""),
            "suggestions": ai_response.get("suggestions", []),
            "top_results": serialize_results(ai_ranked_results[:8])
        }, default=json_serial))

        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "DONE"}))
        print(f"✅ [WORKER] Arama ve AI işlemi bitti.")

    except Exception as e:
        print(f"❌ Hata: {e}")
        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "ERROR", "message": str(e)}))

async def process_follow_up(job_id, question, history):
    print(f"💬 [FOLLOW-UP] Takip sorusu: {question}")
    try:
        formatted_history = format_history(history)
        # RAG sistemine sor
        cevap = await asyncio.to_thread(soru_sor, question, formatted_history)
        
        await redis_client.publish(f"job:{job_id}", json.dumps({
            "type": "AI_ANSWER", 
            "data": cevap
        }))
        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "DONE"}))
    except Exception as e:
        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "ERROR", "message": str(e)}))

async def main_loop():
    print("🚀 Space Teknopoli AI Worker Başladı! (Asenkron Mod)")
    while True:
        res = await redis_client.brpop('task_queue', timeout=0)
        if res:
            _, message = res
            job = json.loads(message)
            
            if job['type'] == 'search':
                # DEĞİŞEN KISIM BURASI: await yerine create_task kullanıyoruz!
                asyncio.create_task(process_search(job['jobId'], job['query']))
            elif job['type'] == 'follow_up':
                # TAKİP SORUSU İÇİN DE AYNISI
                asyncio.create_task(process_follow_up(job['jobId'], job['question'], job.get('history', [])))

if __name__ == "__main__":
    # Tabloları oluştur (Opsiyonel: Zaten varsa bir şey yapmaz)
    from postgresql_islem.postgres_islem import hedef_siteler_tablosu_olustur, postgres_tablo_olustur
    postgres_tablo_olustur()
    hedef_siteler_tablosu_olustur()
    
    asyncio.run(main_loop())