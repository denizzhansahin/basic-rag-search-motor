from embedding_save_qdrant import qdranta_kaydet
from embedding_pdf import embedding_pdf
from embedding.embeddin_url_selenium import embedding_url

if __name__ == "__main__":
    # PDF'ten metin parçalarını al
    #pdf_metni = embedding_pdf("2.pdf")
    
    # Web sayfasından metin parçalarını al
    url_metni = embedding_url("https://www.webtekno.com/google-circle-to-search-her-seyi-tek-seferde-taniyabiliyor-h212973.html")
    
    # PDF ve URL'den gelen metin parçalarını birleştir
    tum_metniler = url_metni
    
    # Birleştirilen metin parçalarını Qdrant'a kaydet
    qdranta_kaydet(tum_metniler, collection_name="ollama_my_rag_collection")