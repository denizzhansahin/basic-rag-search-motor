from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings

import os
import json
from datetime import datetime

def embedding_pdf(pdf_yolu):
    klasor_adi = "pdf_veri"
    if not os.path.exists(klasor_adi):
        os.makedirs(klasor_adi)
        print(f"'{klasor_adi}' klasörü oluşturuldu.")

    # 1. LangChain Loader ile PDF'i yükle (Arka planda pypdf kullanır ve sayfaları ayırır)
    loader = PyPDFLoader(pdf_yolu)
    docs = loader.load() # docs listesi, her bir sayfanın metnini ve meta verilerini (sayfa no vb.) tutar


    # 2. Dokümanları vektörlere çevir
    # embed_documents metodu, liste halindeki metinleri alır ve hepsini vektörleştirir

    # 3. Veriyi Dosya Olarak Kaydetme
    # Dosya adını benzersiz yapmak için o anki zamanı ve URL'nin bir kısmını kullanıyoruz
    zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")

    suanki_zaman = datetime.now().isoformat()
    # URL'deki geçersiz karakterleri temizleyerek güvenli bir dosya adı oluşturuyoruz
    temiz_yol = pdf_yolu.replace("https://", "").replace("http://", "").replace("/", "_")[:30]
    dosya_adi = f"{klasor_adi}/pdf_{temiz_yol}_{zaman_damgasi}.json"

    # 1. Tam şu anki zamanı alıyoruz
    suanki_zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. ÖNEMLİ: Her bir dokümanın kendi metadata sözlüğüne bu bilgiyi kalıcı olarak ekliyoruz
    for doc in docs:
        doc.metadata["scraped_at"] = suanki_zaman
        doc.metadata["source_url"] = pdf_yolu # Takip için URL'yi de içine gömüyoruz

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
    
    return docs

    print(f"LangChain ile toplam {len(metin_listesi)} adet metin parçası Qdrant'a kaydedildi.")