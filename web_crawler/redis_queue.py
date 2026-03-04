import sys
from pathlib import Path

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))


from web_crawler.config import REDIS_HOST, REDIS_PORT




from embedding.embedding_save_qdrant import qdranta_kaydet
import redis
import time




# Ağır kütüphaneler sadece burada import ediliyor!
from embedding.embeddin_url_selenium import embedding_url

# Redis bağlantısı
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def kuyruk_dinleyici():
    print("🚀 Link İşleyici (Consumer) başlatıldı. Kuyruk bekleniyor...")
    
    while True:
        # BRPOP: Listeden veri gelene kadar "blokla" (bekle). 
        # Veri geldiği an en sağdan (Right Pop) al.
        # 0 parametresi: Veri gelene kadar sonsuza kadar bekle demektir.
        is_emri = r.brpop("link_kuyrugu", timeout=0)
        
        if is_emri:
            liste_adi, url = is_emri
            print(f"\n🔔 Yeni iş yakalandı: {url}")
            
            try:
                start_time = time.time()
                # Senin o meşhur fonksiyonun burada çalışıyor

                parcalar = embedding_url(url)
                qdranta_kaydet(parcalar, collection_name="ollama_my_rag_collection")

                end_time = time.time()
                
                print(f"✅ İşlem tamamlandı. Süre: {int(end_time - start_time)}sn")
            except Exception as e:
                print(f"❌ İşlenirken hata oluştu ({url}): {e}")
                # Hata olursa linki 'hatali_linkler' listesine atalım ki kaybolmasın
                r.lpush("hatali_linkler", url)






def kuyruk_dinleyici1():

    worker_id = f"worker_{time.time()}"
    
    # Worker register
    r.sadd("aktif_workerlar", worker_id)

    print("🚀 Link İşleyici başlatıldı")

    while True:

        is_emri = r.brpop("link_kuyrugu", timeout=0)

        if is_emri:

            liste_adi, url = is_emri

            r.set("aktif_is", url)

            try:
                start = time.time()

                parcalar = embedding_url(url)
                qdranta_kaydet(parcalar,
                               collection_name="ollama_my_rag_collection")

                r.incr("basarili_is")

                print("✅ Tamamlandı")

            except Exception as e:

                print("❌ Hata:", e)

                r.lpush("hatali_linkler", url)
                r.incr("basarisiz_is")

            finally:

                r.delete("aktif_is")
if __name__ == "__main__":
    kuyruk_dinleyici1()