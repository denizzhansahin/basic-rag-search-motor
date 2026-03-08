import sys
from pathlib import Path

from web_crawler.config import DB_AYARLARI

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))

from crawler_web_selenium import otomatik_site_tarayici






import psycopg2
from datetime import datetime, timedelta
import time


def siradaki_siteyi_tara():
    baglanti = None
    print("Site bağlantı")
    print(DB_AYARLARI)
    try:
        baglanti = psycopg2.connect(**DB_AYARLARI)
        cursor = baglanti.cursor()

        # SQL MANTIĞI: 
        # 1. Durumu 'bekliyor' olanları al.
        # 2. VE (Daha önce hiç taranmamış olanları (NULL) VEYA üzerinden 5 saat geçmiş olanları getir)
        sorgu = """
            SELECT id, ana_url, max_sayfa 
            FROM hedef_siteler 
            WHERE durum = 'bekliyor' 
              AND (son_tarama_tarihi IS NULL OR son_tarama_tarihi < NOW() - INTERVAL '5 hours')
            ORDER BY son_tarama_tarihi ASC NULLS FIRST
            LIMIT 1;
        """
        
        cursor.execute(sorgu)
        site = cursor.fetchone()

        if not site:
            # Tarancak site yoksa bekleme moduna geçebiliriz
            return False

        site_id, url, max_sayfa = site
        
        # 2. Durumu 'taraniyor' olarak güncelle (Aynı anda başka script çalışmasın diye)
        cursor.execute("UPDATE hedef_siteler SET durum = 'taraniyor' WHERE id = %s", (site_id,))
        baglanti.commit()

        print(f"\n⏰ Zamanı Geldi: {url} taranıyor... (Son tarama: {site[0]})")
        
        # 3. Mevcut Crawler'ı çalıştır
        otomatik_site_tarayici(url, max_sayfa=max_sayfa)

        # 4. İşlem bitince durumu 'bekliyor' yap ve zamanı GÜNCELLE
        cursor.execute("""
            UPDATE hedef_siteler 
            SET durum = 'bekliyor', son_tarama_tarihi = %s 
            WHERE id = %s
        """, (datetime.now(), site_id))
        baglanti.commit()
        print(f"✅ {url} tarama seansı bitti. Bir sonraki tarama 5 saat sonra.")
        return True

    except Exception as e:
       print(f"❌ Hata oluştu: {e}")
        # Sadece site_id tanımlanmışsa (yani bir site seçilebilmişse) geri al
       if baglanti and 'site_id' in locals():
            cursor.execute("UPDATE hedef_siteler SET durum = 'bekliyor' WHERE id = %s", (site_id,))
            baglanti.commit()
       return False
    
    finally:
        if baglanti:
            cursor.close()
            baglanti.close()

if __name__ == "__main__":
    print("🤖 Site Yönetici Otopilotu Başlatıldı...")
    
    # Sürekli çalışan bir döngü
    while True:
        is_processed = siradaki_siteyi_tara()
        
        if is_processed:
            print("🔄 Liste kontrol ediliyor...")
            time.sleep(10) # Bir siteden diğerine geçmeden önce kısa bir nefes al
        else:
            # Eğer taranacak (5 saati dolmuş) site yoksa 5 dakika uyu ve tekrar kontrol et
            print("😴 Şimdilik taranacak site yok. 5 dakika bekleniyor...")
            time.sleep(10)