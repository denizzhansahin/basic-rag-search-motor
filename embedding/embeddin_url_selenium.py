import sys
from pathlib import Path

from embedding.html_language_detect import dili_bul

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

import os
import json
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from langchain_core.documents import Document
import trafilatura

from postgresql_islem.postgres_islem import veritabanina_kaydet


def embedding_url(url_yolu):

    klasor_adi = "web_veri"

    if not os.path.exists(klasor_adi):
        os.makedirs(klasor_adi)

    print("🌐 Selenium sayfayı açıyor...")

    # Selenium ayarları
    options = Options()
    options.binary_location = "/usr/bin/chromium"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--blink-settings=imagesEnabled=false")

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)

    # sayfayı aç
    driver.get(url_yolu)

    time.sleep(3)

    html = driver.page_source

    driver.quit()

    print("📄 HTML alındı. Uzunluk:", len(html))

    # içerik extraction
    text = trafilatura.extract(html)

    if not text:
        print("⚠️ İçerik çıkarılamadı:", url_yolu)
        return []

    print("📰 Çıkarılan metin uzunluğu:", len(text))

    suanki_zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")




    meta = trafilatura.extract_metadata(html)

    suanki_zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    language = dili_bul(html, text)

    metadata = {
        "source": meta.url if meta and meta.url else url_yolu,
        "title": meta.title if meta else None,
        "description": meta.description if meta else None,
        "language": language,
        "scraped_at": suanki_zaman,
        "source_url": url_yolu
    }

    docs = [
    Document(
        page_content=text,
        metadata=metadata
    )
]

    """
    docs = [
        Document(
            page_content=text,
            metadata={
                "source_url": url_yolu,
                "scraped_at": suanki_zaman
            }
        )
    ]
    """

    # postgres kayıt
    for doc in docs:
        veritabanina_kaydet(
            metadata=doc.metadata,
            icerik=doc.page_content
        )

    # JSON kayıt
    zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")

    temiz_url = url_yolu.replace("https://", "").replace("http://", "").replace("/", "_")[:30]

    dosya_adi = f"{klasor_adi}/web_{temiz_url}_{zaman_damgasi}.json"

    kaydedilecek_veri = [
        {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in docs
    ]

    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(kaydedilecek_veri, f, ensure_ascii=False, indent=4)

    print(f"✅ Kaydedildi -> {dosya_adi}")

    return docs