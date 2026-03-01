import psycopg2
from psycopg2 import sql

# Docker'da belirlediğimiz bilgiler
DB_AYARLARI = {
    "host": "localhost",
    "database": "arama_motoru_db",
    "user": "postgres",
    "password": "gizlisifrem",
    "port": "5432"
}


def hedef_siteler_tablosu_olustur():
    try:
        baglanti = psycopg2.connect(**DB_AYARLARI)
        cursor = baglanti.cursor()
        sorgu = """
        CREATE TABLE IF NOT EXISTS hedef_siteler (
            id SERIAL PRIMARY KEY,
            ana_url VARCHAR(2048) UNIQUE NOT NULL,
            max_sayfa INTEGER DEFAULT 50,
            durum VARCHAR(50) DEFAULT 'bekliyor', -- bekliyor, taraniyor, tamamlandi
            son_tarama_tarihi TIMESTAMP
        );
        """
        cursor.execute(sorgu)
        baglanti.commit()
        cursor.close()
        baglanti.close()
    except Exception as e:
        print(f"❌ Hedef siteler tablosu hatası: {e}")

def postgres_tablo_olustur():
    """Eğer tablo yoksa ilk çalışmada oluşturur."""
    try:
        baglanti = psycopg2.connect(**DB_AYARLARI)
        cursor = baglanti.cursor()
        
        # Sadece 1000 karakterlik icerik_ozeti tutacağız
        sorgu = """
        CREATE TABLE IF NOT EXISTS taranan_linkler (
            id SERIAL PRIMARY KEY,
            url VARCHAR(2048) UNIQUE NOT NULL,
            baslik VARCHAR(500),
            aciklama TEXT,
            icerik_ozeti VARCHAR(1000), 
            erisim_tarihi TIMESTAMP
        );
        """

        # Hedef Siteler Tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hedef_siteler (
                id SERIAL PRIMARY KEY,
                ana_url VARCHAR(2048) UNIQUE NOT NULL,
                max_sayfa INTEGER DEFAULT 50,
                durum VARCHAR(50) DEFAULT 'bekliyor',
                son_tarama_tarihi TIMESTAMP
            );
        """)


        cursor.execute(sorgu)
        baglanti.commit()
        cursor.close()
        baglanti.close()
    except Exception as e:
        print(f"❌ Postgres Tablo oluşturma hatası: {e}")

def veritabanina_kaydet(metadata, icerik):
    try:
        baglanti = psycopg2.connect(**DB_AYARLARI)
        cursor = baglanti.cursor()
        
        # Değerleri güvenli bir şekilde metadata içinden alıyoruz
        url = metadata.get("source_url") or metadata.get("source")
        baslik = metadata.get("title", "Başlıksız")
        aciklama = metadata.get("description", "")
        erisim_tarihi = metadata.get("scraped_at")
        
        # İÇERİĞİ 1000 KARAKTER İLE SINIRLAMA
        icerik_ozeti = icerik[:1000] if icerik else ""

        # ON CONFLICT kısmı: Eğer bu URL daha önce eklendiyse, bilgileri güncelle (Duplicate hatası alma)
        sorgu = """
        INSERT INTO taranan_linkler (url, baslik, aciklama, icerik_ozeti, erisim_tarihi)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (url) DO UPDATE SET 
            baslik = EXCLUDED.baslik,
            aciklama = EXCLUDED.aciklama,
            icerik_ozeti = EXCLUDED.icerik_ozeti,
            erisim_tarihi = EXCLUDED.erisim_tarihi;
        """
        
        cursor.execute(sorgu, (url, baslik, aciklama, icerik_ozeti, erisim_tarihi))
        baglanti.commit()
        
        print(f"🐘 Postgres'e Kaydedildi: {baslik[:30]}...")
        
        cursor.close()
        baglanti.close()
        return True  # Kayıt başarılı
    except Exception as e:
        print(f"❌ Postgres kayıt hatası ({metadata.get('source_url')}): {e}")
        return False  # Kayıt başarısız
    
if __name__ == "__main__":
    print("🐘 Postgres bağlantısı ve tablo kontrolü yapılıyor...")
    postgres_tablo_olustur()
    hedef_siteler_tablosu_olustur()
    print("✅ Postgres hazır! Site yöneticisi başlatılabilir.")