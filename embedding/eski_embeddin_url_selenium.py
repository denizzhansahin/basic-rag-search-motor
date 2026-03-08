import sys
from pathlib import Path

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))




from langchain_community.document_loaders import SeleniumURLLoader
from langchain_ollama import OllamaEmbeddings

import os
import json
from datetime import datetime

from postgresql_islem.postgres_islem import veritabanina_kaydet # Yazdığımız fonksiyonu içeri alıyoruz

def embedding_url(url_yolu):
    # 1. Klasör Oluşturma (Eğer yoksa 'web_veri' klasörünü oluşturur)
    klasor_adi = "web_veri"
    if not os.path.exists(klasor_adi):
        os.makedirs(klasor_adi)
        print(f"'{klasor_adi}' klasörü oluşturuldu.")


    # 1. Adım: Selenium ile Web Sayfasını Yükleme
    urls = [
        url_yolu,
        # Buraya dinamik/JavaScript ile yüklenen başka linkler de ekleyebilirsin
    ]

    print("Selenium tarayıcıyı arka planda açıyor ve sayfaları okuyor...")
    loader = SeleniumURLLoader(urls=urls)
    #docs = loader.load() # Tarayıcı açılır, sayfa yüklenir ve metinler alınır
    # --- ASIL DEĞİŞİKLİK BURADA ---
    loader = SeleniumURLLoader(
        urls=urls,
        arguments=[
            "--headless",                  # Tarayıcı penceresini açma (Hız için şart)
            "--disable-gpu",               # Gereksiz GPU kullanımını kapat
            "--no-sandbox",                # Güvenlik katmanını optimize et
            "--blink-settings=imagesEnabled=false", # RESİMLERİ KAPATAN SİHİRLİ KOMUT
            "--disable-extensions",        # Eklentileri yükleme
            "--mute-audio"                 # Sesi kapat
        ]
    )
    # ------------------------------

    docs = loader.load()


    # 3. Veriyi Dosya Olarak Kaydetme
    # Dosya adını benzersiz yapmak için o anki zamanı ve URL'nin bir kısmını kullanıyoruz
    zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
    # URL'deki geçersiz karakterleri temizleyerek güvenli bir dosya adı oluşturuyoruz
    temiz_url = url_yolu.replace("https://", "").replace("http://", "").replace("/", "_")[:30]
    dosya_adi = f"{klasor_adi}/web_{temiz_url}_{zaman_damgasi}.json"

    # 1. Tam şu anki zamanı alıyoruz
    suanki_zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. ÖNEMLİ: Her bir dokümanın kendi metadata sözlüğüne bu bilgiyi kalıcı olarak ekliyoruz
    for doc in docs:
        doc.metadata["scraped_at"] = suanki_zaman
        doc.metadata["source_url"] = url_yolu # Takip için URL'yi de içine gömüyoruz

        # Postgres kayıt fonksiyonunu tetikle!
        # doc.page_content içindeki metni ve az önce güncellediğimiz metadata'yı gönderiyoruz
        veritabanina_kaydet(metadata=doc.metadata, icerik=doc.page_content)

    # 3. JSON için veriyi hazırlıyoruz (Artık metadata içinde olduğu için garanti orada)
    kaydedilecek_veri = [
        {
            "page_content": doc.page_content, 
            "metadata": doc.metadata # 'scraped_at' artık bunun içinde!
        } 
        for doc in docs
    ]

    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(kaydedilecek_veri, f, ensure_ascii=False, indent=4)

    print(f"✅ İşlem tamam! Veriler '{dosya_adi}' dosyasına kaydedildi.")


    # 2. Adım: Web sayfasından çekilen metni vektörlere çevir
    return docs

    print(f"İşlem tamam! Web sayfasından {len(metin_listesi)} adet metin parçası Qdrant'a kaydedildi.")