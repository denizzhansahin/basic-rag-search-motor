import sys
import json
import asyncio
import os
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal
import uuid
from python_api.ai_chat_engine import process_ai_chat
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






# 1. ÇALIŞAN GÖREVLERİ TUTACAĞIMIZ SÖZLÜK
running_tasks = {} # format: { "jobId": asyncio.Task_objesi }



# 2. İPTAL SİNYALLERİNİ DİNLEYEN ARKA PLAN GÖREVİ
async def cancel_listener():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('cancel_jobs')
    print("🛑 İptal dinleyicisi aktif...")
    
    async for message in pubsub.listen():
        try:
            if message['type'] == 'message':
                raw_data = message['data']
                
                # Redis'ten gelen veri bytes ise decode et, zaten string ise doğrudan al
                if isinstance(raw_data, bytes):
                    job_id_to_cancel = raw_data.decode('utf-8')
                else:
                    job_id_to_cancel = str(raw_data)
                
                task = running_tasks.get(job_id_to_cancel)
                if task:
                    print(f"🔪 Görev zorla iptal ediliyor: {job_id_to_cancel}")
                    task.cancel() # Asenkron görevi anında öldürür!
        except Exception as e:
            print(f"⚠️ İptal dinleyicisinde (cancel_listener) küçük bir hata oluştu ama dinlemeye devam ediyor: {e}")


async def main_loop():
    print("🚀 Space Teknopoli AI Worker Başladı! (Asenkron Mod)")

# İptal dinleyicisini ana döngü başlamadan önce çalıştır
    asyncio.create_task(cancel_listener())

    while True:
            res = await redis_client.brpop('task_queue', timeout=0)
            if res:
                _, message = res
                job = json.loads(message)
                job_id = job['jobId']
                
                # 3. GÖREVİ BAŞLAT VE SÖZLÜĞE EKLE
                if job['type'] == 'search':
                    task = asyncio.create_task(process_search(job_id, job['query']))
                    running_tasks[job_id] = task
                    # Görev bitince sözlükten kendi kendini silsin
                    task.add_done_callback(lambda t, jid=job_id: running_tasks.pop(jid, None))
                    
                elif job['type'] == 'ai_chat':
                    task = asyncio.create_task(process_ai_chat(
                        job_id, redis_client, job['query'], job.get('history', []), job.get('fileBase64'), job.get('fileType')
                    ))
                    running_tasks[job_id] = task
                    task.add_done_callback(lambda t, jid=job_id: running_tasks.pop(jid, None))
                    




if __name__ == "__main__":
    # Tabloları oluştur (Opsiyonel: Zaten varsa bir şey yapmaz)
    from postgresql_islem.postgres_islem import hedef_siteler_tablosu_olustur, postgres_tablo_olustur
    postgres_tablo_olustur()
    hedef_siteler_tablosu_olustur()
    
    asyncio.run(main_loop())