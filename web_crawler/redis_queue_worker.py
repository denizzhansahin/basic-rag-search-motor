import sys
from pathlib import Path

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))

from web_crawler.config import REDIS_HOST, REDIS_PORT





import time
import multiprocessing
import redis



from embedding.embedding_save_qdrant import qdranta_kaydet

def isci_baslat(worker_no):
    """
    Her bir Process (işçi) kendi bağımsız Redis bağlantısını ve durumunu yönetir.
    """
    # Redis bağlantısını worker'ın kendi içinde açması multiprocessing için daha sağlıklıdır
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    worker_id = f"worker_{worker_no}_{int(time.time())}"
    
    # Sisteme bu worker'ı kayıt et
    r.sadd("aktif_workerlar", worker_id)
    print(f"🚀 [Worker-{worker_no}] Başlatıldı. ID: {worker_id}")

    # Ağır kütüphaneleri işçinin içinde import etmek, başlangıç hızını artırır
    # ve bellek sızıntılarını (memory leak) önler.
    from embedding.embeddin_url_selenium import embedding_url

    try:
        while True:
            # Kuyrukta iş yoksa burada bekler (CPU tüketmez)
            is_emri = r.brpop("link_kuyrugu", timeout=0)

            if is_emri:
                liste_adi, url = is_emri

                # "aktif_is" yerine "aktif_isler" HASH'i kullanıyoruz. 
                # Böylece Redis'te: hgetall aktif_isler diyerek 5 işçinin ne yaptığını görebilirsin.
                r.hset("aktif_isler", worker_id, url)
                
                print(f"⏳ [Worker-{worker_no}] Yeni iş yakalandı: {url}")

                try:
                    start = time.time()
                    
                    # Embedding ve Qdrant İşlemleri
                    parcalar = embedding_url(url)
                    qdranta_kaydet(parcalar, collection_name="ollama_my_rag_collection")

                    # Başarı sayacını artır
                    r.incr("basarili_is")
                    
                    sure = int(time.time() - start)
                    print(f"✅ [Worker-{worker_no}] Tamamlandı: {url} ({sure}sn)")

                except Exception as e:
                    print(f"❌ [Worker-{worker_no}] Hata ({url}): {e}")
                    # Hata alan linki hata listesine at
                    r.lpush("hatali_linkler", url)
                    r.incr("basarisiz_is")

                finally:
                    # İşlem bitince, hata alsa da almasa da aktif işlerden kendini temizle
                    r.hdel("aktif_isler", worker_id)

    except KeyboardInterrupt:
        print(f"🛑 [Worker-{worker_no}] Kapatılma komutu aldı, durduruluyor...")
    finally:
        # Script tamamen kapanırsa worker'ı aktif listesinden sil
        r.srem("aktif_workerlar", worker_id)
        r.hdel("aktif_isler", worker_id)


if __name__ == "__main__":
    # Kaç adet paralel işçi (worker) çalıştırmak istiyorsun?
    WORKER_SAYISI = 3
    
    print(f"🔥 Sistem başlatılıyor... Toplam {WORKER_SAYISI} paralel işçi kuyruğu dinleyecek.")
    print("Durdurmak için CTRL+C yapabilirsiniz.\n")

    islemler = []
    
    # Worker'ları başlat
    for i in range(WORKER_SAYISI):
        # Her bir işçi için ayrı bir CPU process'i oluşturuluyor
        p = multiprocessing.Process(target=isci_baslat, args=(i+1,))
        p.start()
        islemler.append(p)
        
    # Ana programın kapanmaması için tüm alt process'leri dinle
    try:
        for p in islemler:
            p.join()
    except KeyboardInterrupt:
        print("\n🛑 Ana program durduruldu. Tüm işçiler kapatılıyor...")
        for p in islemler:
            p.terminate()
            p.join()
        print("Tüm işlemler başarıyla sonlandırıldı.")