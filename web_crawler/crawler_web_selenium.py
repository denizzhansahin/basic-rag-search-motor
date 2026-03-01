import sys
from pathlib import Path

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))

#from embedding.embeddin_url_selenium import embedding_url
from postgresql_islem.postgres_islem import veritabanina_kaydet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, urljoin
from datetime import datetime
import time


from rq import Queue

# Ağır kütüphaneler sadece burada import ediliyor!
import redis

# Redis bağlantısı
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)





def otomatik_site_tarayici(baslangic_url, max_sayfa=5):
    """
    Selenium ile siteyi gezer, JavaScript ile oluşturulmuş linkleri bile bulur
    ve her bulduğu linki RAG veritabanına kaydetmek üzere gönderir.
    """
    











    chrome_options = Options()
    
    # --- 1. Çekirdek Hız Ayarları (Arguments) ---
    arguments = [
        "--headless=new",              # Yeni nesil headless mod (daha kararlı)
        "--disable-gpu",               # Grafik işlemciyi devre dışı bırak (Sunucu/Bot için gereksiz)
        "--no-sandbox",                # Güvenlik katmanını bot için hafiflet
        "--disable-dev-shm-usage",     # Bellek paylaşım hatalarını önle
        "--disable-extensions",        # Eklentileri yükleme
        "--mute-audio",                # Sesi kapat
        "--disable-blink-features=AutomationControlled", # Bot olduğumuzu gizle
        "--blink-settings=imagesEnabled=false",         # Resimleri yükleme
        "--disable-web-security",      # Bazı sitelerde hız kazandırır
        "--disable-software-rasterizer",
        "--disk-cache-size=1",         # Önbelleği minimumda tut
        "--media-cache-size=1",        # Medya önbelleğini kapat
        "--disable-notifications",     # Bildirim pencerelerini engelle
        "--disable-infobars"           # "Chrome otomatik yazılım tarafından kontrol ediliyor" barını gizle
    ]
    
    for arg in arguments:
        chrome_options.add_argument(arg)

    # --- 2. Gelişmiş Tercihler (Preferences) ---
    # Bu ayarlar tarayıcının içindeki özellikleri (CSS, Resim vb.) kökten kapatır
    prefs = {
        "profile.managed_default_content_settings.images": 2,      # Resimleri yükleme
        "profile.managed_default_content_settings.stylesheets": 2, # CSS/Stil dosyalarını yükleme (Çok hızlandırır!)
        "profile.managed_default_content_settings.cookies": 2,     # İsteğe bağlı: Çerezleri kapat (Hızlandırır ama login gerektiren sitelerde sorun çıkarabilir)
        "profile.managed_default_content_settings.plugins": 2,     # Eklentileri/Flash'ı kapat
        "profile.managed_default_content_settings.popups": 2,      # Popup pencereleri engelle
        "profile.managed_default_content_settings.geolocation": 2, # Konum servislerini kapat
        "profile.default_content_setting_values.notifications": 2, # Bildirimleri engelle
        "profile.default_content_setting_values.media_stream": 2   # Mikrofon/Kamera erişimini kapat
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Güvenlik duvarlarını aşmak için kendimizi normal bir Windows/Chrome kullanıcısı gibi gösteriyoruz
    sahte_kimlik = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={sahte_kimlik}")
    
    # Tarayıcıyı başlat
    driver = webdriver.Chrome(options=chrome_options)
    
    # --- 2. CRAWLING (KEŞİF) MANTIĞI ---
    ziyaret_edilecekler = [baslangic_url]
    ziyaret_edilenler = set()
    ana_domain = urlparse(baslangic_url).netloc
    bulunan_gecerli_linkler = set()
    
    print(f"🕷️ Selenium Web Crawler '{ana_domain}' üzerinde göreve başladı...\n")

    while ziyaret_edilecekler and len(ziyaret_edilenler) < max_sayfa:
        suanki_url = ziyaret_edilecekler.pop(0)
        
        if suanki_url in ziyaret_edilenler:
            continue
            
        try:
            print(f"[{len(ziyaret_edilenler) + 1}/{max_sayfa}] Taranıyor: {suanki_url}")
            driver.get(suanki_url)
            
            # JavaScript'in DOM'u oluşturması ve sayfanın oturması için kısa bir bekleme
            time.sleep(3) 
            
            ziyaret_edilenler.add(suanki_url)
            
            # --- 3. SCRAPING & VERİTABANI (DİĞER FONKSİYONA GÖNDERME) ---
            # Sayfa açılmışken, içeriği direkt RAG sistemimiz için indirelim
            # --- 1. VERİLERİ DİREKT SELENIUM'DAN ÇEKME ---
            suanki_zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sayfa_basligi = driver.title # Sekme başlığını al
            
            # Açıklamayı (Meta Description) bulmaya çalış
            try:
                meta_desc = driver.find_element(By.XPATH, '//meta[@name="description"]')
                sayfa_aciklamasi = meta_desc.get_attribute("content")
            except:
                sayfa_aciklamasi = ""
                
            # Sayfadaki tüm görünür metni al
            try:
                sayfa_icerigi = driver.find_element(By.TAG_NAME, "body").text
            except:
                sayfa_icerigi = ""

            # --- 2. POSTGRESQL'E KAYDETME ---
            metadata = {
                "source_url": suanki_url,
                "title": sayfa_basligi,
                "description": sayfa_aciklamasi,
                "scraped_at": suanki_zaman
            }
            veritabanina_kaydet(metadata, sayfa_icerigi)
            
            # --- 4. YENİ LİNKLERİ KEŞFETME ---
            # Selenium üzerinden sayfadaki tüm <a> etiketlerini çekiyoruz (JS ile sonradan gelenler dahil)
            link_elementleri = driver.find_elements(By.TAG_NAME, "a")
            
            for element in link_elementleri:
                ham_link = element.get_attribute("href")
                
                if ham_link: # href özniteliği boş değilse
                    tam_link = urljoin(suanki_url, ham_link)
                    temiz_link = tam_link.split("#")[0].split("?")[0]
                    
                    # Sadece kendi sitemizin alt sayfalarıysa ve yeni bir linkse kuyruğa ekle
                    if ana_domain in urlparse(temiz_link).netloc:
                        if not temiz_link.endswith(('.jpg', '.png', '.pdf', '.zip')) and "mailto:" not in temiz_link:
                            if temiz_link not in ziyaret_edilenler and temiz_link not in ziyaret_edilecekler:
                                ziyaret_edilecekler.append(temiz_link)
                                bulunan_gecerli_linkler.add(temiz_link)
                                
                                # --- YENİ EKLENEN KISIM: BULUNAN LİNKİ ANINDA KAYDET ---
                                # 1. Önce veritabanına 'no_data' olarak ön kayıt yapmayı dene
                                kesif_zamani = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                bos_metadata = {
                                    "source_url": temiz_link,
                                    "title": "no_data",
                                    "description": "",
                                    "scraped_at": kesif_zamani
                                }

                                # Kayıt işlemini bir değişkene atıyoruz
                                kayit_basarili = veritabanina_kaydet(bos_metadata, "")

                                # 2. EĞER veritabanına kayıt başarılıysa KUYRUĞA EKLE
                                if kayit_basarili:
                                    print(f"   📥 Veritabanı OK -> Kuyruğa eklendi: {temiz_link}")
                                    ziyaret_edilecekler.append(temiz_link)
                                    bulunan_gecerli_linkler.add(temiz_link)
                                    
                                    r.lpush("link_kuyrugu", temiz_link)
                                else:
                                    print(f"   ⚠️ Kayıt başarısız veya link zaten işleniyor, kuyruğa eklenmedi: {temiz_link}")
                                # -------------------------------------------------------

        except Exception as e:
            print(f"Bağlantı/Tarama hatası ({suanki_url}): {e}")

    driver.quit()
    print(f"\n✅ Görev Tamamlandı! {len(ziyaret_edilenler)} sayfa başarıyla tarandı ve veritabanına aktarıldı.")
    print(f"\n✅ Tarama Tamamlandı! Toplam {len(bulunan_gecerli_linkler)} adet alt sayfa bulundu.")
    return list(bulunan_gecerli_linkler)


# DOSYANIN EN ALTINDAKİ TEST KISMINI ŞÖYLE DEĞİŞTİR:
if __name__ == "__main__":
    # Bu blok SADECE bu dosyayı doğrudan (python crawler_web_selenium.py) 
    # çalıştırdığında devreye girer. 
    # Başka dosyadan import edildiğinde ÇALIŞMAZ.
    #print("🧪 Test modu başlatıldı...")
    #linkler = otomatik_site_tarayici("https://shiftdelete.net", max_sayfa=2)
    #for link in linkler:
    #   print(link)
    pass