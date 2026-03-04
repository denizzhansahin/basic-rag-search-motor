from embedding.config import COLLECTION_NAME, QDRANT_URL
import qdrant_client
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from qdrant_client.http.models import Distance, VectorParams




def qdranta_kaydet(belge_parcalari, collection_name=COLLECTION_NAME):
    """
    Dışarıdan gelen metin parçalarını alır, embeddinggemma ile vektöre çevirir
    ve Docker üzerindeki Qdrant veritabanına kaydeder.
    
    Parametreler:
    - belge_parcalari: LangChain Document formatındaki metin parçaları (chunks)
    - collection_name: Verilerin kaydedileceği tablo/koleksiyon adı
    """
    
    if not belge_parcalari:
        print("Uyarı: Kaydedilecek belge bulunamadı!")
        return False

    print(f"{len(belge_parcalari)} adet metin parçası Qdrant'a yükleniyor...")

    try:
        # 1. Docker'daki Qdrant'a bağlan
        client = qdrant_client.QdrantClient(url=QDRANT_URL)
        
        # 2. Embedding modelini tanımla
        embeddings = OllamaEmbeddings(model="embeddinggemma")
        
        # 3. LangChain ile Qdrant nesnesini oluştur

        # Koleksiyon var mı kontrol et
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]

        if collection_name not in collection_names:

            print("Koleksiyon oluşturuluyor...")

            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=768,   # embeddinggemma dimension
                    distance=Distance.COSINE
                ),
            )


        qdrant_store = QdrantVectorStore(
            client=client, 
            collection_name=collection_name, 
            embedding=embeddings
        )
        
        # 4. Belgeleri ekle (Bu adımda metinler otomatik vektörleşip kaydedilir)
        qdrant_store.add_documents(belge_parcalari)
        
        print("✅ Kayıt işlemi başarıyla tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Kayıt sırasında bir hata oluştu: {e}")
        return False