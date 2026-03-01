import sys
from pathlib import Path

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))




import psycopg2
from redis import Redis
from rq import Queue
from rq.job import Job
from embedding.embeddin_url_selenium import embedding_url
import random
import time

# 1. Veritabanı ve Redis Ayarları
DB_AYARLARI = {
    "host": "localhost",
    "database": "arama_motoru_db",
    "user": "postgres",
    "password": "gizlisifrem",
    "port": "5432"
}

# Redis Bağlantısı
try:
    redis_conn = Redis(host='localhost', port=6379)
    # Redis'in açık olup olmadığını test et
    redis_conn.ping()
    q = Queue(connection=redis_conn)
except Exception as e:
    print(f"❌ Redis sunucusuna bağlanılamadı! Lütfen Redis'in çalıştığından emin olun. Hata: {e}")
    exit(1)

def job_kuyrukta_mi(url):
    """
    Belirli bir URL'nin zaten Redis kuyruğunda olup olmadığını kontrol eder.
    RQ, her görevi benzersiz bir ID ile saklayabilir.
    """
    job_id = f"job:{url}"
    try:
        # Belirtilen ID'ye sahip görevi getir
        existing_job = Job.fetch(job_id, connection=redis_conn)
        # Görev varsa; 'queued', 'started' veya 'deferred' durumunda mı bak
        if existing_job.get_status() in ['queued', 'started', 'deferred']:
            return True
        return False
    except:
        # Job bulunamadıysa (fetch hata verirse) kuyrukta değildir
        return False

def eksik_linkleri_kuyruga_at():
    print("🔍 Postgres'te taranmamış (no_data) linkler aranıyor...")
    
    baglanti = None
    try:
        baglanti = psycopg2.connect(**DB_AYARLARI)
        cursor = baglanti.cursor()
        
        # Başlığı 'no_data' olan linkleri getir
        cursor.execute("SELECT url FROM taranan_linkler WHERE baslik = 'no_data';")
        eksik_linkler = cursor.fetchall() 
        
        if not eksik_linkler:
            print("✅ Harika! Taranmamış link bulunamadı.")
            return

        # RASTGELE SIRALAMA: Linkleri karıştırarak botun her zaman aynı sırayla 
        # gitmesini engelliyoruz (Bazı sitelerdeki darboğazları aşmak için faydalıdır).
        random.shuffle(eksik_linkler)
        
        eklenen_sayac = 0
        atlanan_sayac = 0

        for (url,) in eksik_linkler:
            # REDIS KONTROLÜ: Link zaten kuyrukta mı?
            if not job_kuyrukta_mi(url):
                # Görevi benzersiz bir ID (URL'nin kendisi) ile kuyruğa ekle
                # 'job_id' kullanımı aynı URL'nin tekrar eklenmesini engeller
                q.enqueue(
                    embedding_url, 
                    url, 
                    job_id=f"job:{url}",
                    result_ttl=86400 # Sonuçları 24 saat sakla (isteğe bağlı)
                )
                eklenen_sayac += 1
            else:
                atlanan_sayac += 1

        print(f"\n🚀 İşlem Tamamlandı:")
        print(f"   📥 Yeni eklenen: {eklenen_sayac}")
        print(f"   ⏩ Zaten kuyrukta olduğu için atlanan: {atlanan_sayac}")

    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        if baglanti:
            cursor.close()
            baglanti.close()

if __name__ == "__main__":
    eksik_linkleri_kuyruga_at()