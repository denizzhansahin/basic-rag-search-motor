import sys
import json
import math
import asyncio
from pathlib import Path
from datetime import datetime, date
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

base_path = Path(__file__).resolve().parent
sys.path.append(str(base_path))

from python_api.config import ACCEPT_URL, SECRET_KEY
from search_core.pipeline import search_pipeline
from search_core.ai_reranker import rerank_with_ai
from search_core.ai_engine import ai_answer

app = FastAPI(title="Space Teknopoli Internal AI Engine")


search_cache = {}



def serialize_results(results):
    for r in results:
        if 'date' in r and isinstance(r['date'], (datetime, date)):
            r['date'] = r['date'].isoformat()
    return results





@app.websocket("/ws/search")
async def websocket_search_endpoint(websocket: WebSocket):

    client_ip = websocket.client.host
    token = websocket.query_params.get("token")

    if client_ip not in ACCEPT_URL:
        await websocket.close()
        print("❌ Yetkisiz bağlantı:", client_ip)
        return

    if token != SECRET_KEY:
        await websocket.close()
        print("❌ Yetkisiz token")
        return


    
    await websocket.accept()
    connection_alive = True

    """

    async def watch_disconnect():
        nonlocal connection_alive
        try:
            while True:
                await websocket.receive_text()
        except:
            connection_alive = False
            print("🔴 Kullanıcı ayrıldı, işlem iptal ediliyor.")

    disconnect_task = asyncio.create_task(watch_disconnect())
    """

    try:

        while connection_alive:

            data = await websocket.receive_text()
            request = json.loads(data)
            query = request.get("query", "").strip().lower()

            if not query:
                continue

            print(f"🔍 Geniş arama başlatılıyor: {query}")

            # Pipeline
            all_results = await asyncio.to_thread(search_pipeline, query, [])

            if not connection_alive:
                print("⛔ Pipeline sonrası kullanıcı yok → durduruldu")
                return


            safe_results = serialize_results(all_results[:200])

            await websocket.send_json({
                "type": "FULL_RESULTS",
                "data": safe_results
            })


            # AI rerank
            top_20 = all_results[:20]

            ai_ranked_results = await asyncio.to_thread(
                rerank_with_ai,
                query,
                top_20
            )

            if not connection_alive:
                print("⛔ Rerank sonrası kullanıcı yok → durduruldu")
                return


            ai_response = await asyncio.to_thread(
                ai_answer,
                query,
                ai_ranked_results
            )

            if not connection_alive:
                print("⛔ AI sonrası kullanıcı yok → durduruldu")
                return


            await websocket.send_json({
                "type": "AI_RESULTS",
                "summary": ai_response.get("summary", ""),
                "suggestions": ai_response.get("suggestions", []),
                "top_results": serialize_results(ai_ranked_results[:8])
            })


            await websocket.send_json({"type": "DONE"})

    except WebSocketDisconnect:
        connection_alive = False
        print("🔴 Bağlantı koptu.")

    except Exception as e:

        connection_alive = False
        print("Hata:", e)


    finally:
        #disconnect_task.cancel()
        connection_alive = False
        print("🛑 İşlem tamamen durduruldu")


"""
@app.websocket("/ws/search")
async def websocket_search_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            query = request.get("query", "").strip().lower()

            if not query: continue

            # 1. Pipeline'dan geniş bir sonuç kümesi çek (Örn: 100 sonuç)
            # 1. Pipeline'dan geniş bir sonuç kümesi çek (Örn: 100 sonuç)
            print(f"🔍 Geniş arama başlatılıyor: {query}")
            all_results = await asyncio.to_thread(search_pipeline, query, [])
            
            # 2. Klasik sonuçların (ilk 100 tanesini) tek seferde gönderiyoruz
            # Backend tarafında pagination artık yok, tüm havuz gidiyor.
            safe_results = serialize_results(all_results[:200])
            await websocket.send_json({
                "type": "FULL_RESULTS", 
                "data": safe_results
            })

            # 3. AI Analizi (Sadece bir kez, en iyi 20 veriyle)
            top_20 = all_results[:20]
            ai_ranked_results = await asyncio.to_thread(rerank_with_ai, query, top_20)
            ai_response = await asyncio.to_thread(ai_answer, query, ai_ranked_results)
            
            await websocket.send_json({
                "type": "AI_RESULTS",
                "summary": ai_response.get("summary", ""),
                "suggestions": ai_response.get("suggestions", []),
                "top_results": serialize_results(ai_ranked_results[:8])
            })

            await websocket.send_json({"type": "DONE"})

    except WebSocketDisconnect:
        print("🔴 Bağlantı koptu (İstemci ayrıldı).")
    except Exception as e:
        print(f"❌ Beklenmeyen Hata: {e}")
        try:
            await websocket.send_json({"type": "ERROR", "message": str(e)})
        except:
            pass

"""






# api_server.py EN ÜSTÜNE EKLE:
from ollama_run.ollama_rag_read import soru_sor # Bu fonksiyonu senin dosyandan alıyoruz

# GEÇMİŞİ FORMATLAYAN FONKSİYON (Tanımlanmamış hatası için)
def format_history(history_list):
    formatted = ""
    for msg in history_list:
        role = "Kullanıcı" if msg['role'] == 'user' else "Asistan"
        formatted += f"{role}: {msg['content']}\n"
    return formatted
