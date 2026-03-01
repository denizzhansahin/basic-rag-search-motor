import qdrant_client

from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def soru_sor(soru, sohbet_gecmisi="", collection_name="ollama_my_rag_collection"):

    print(f"'{soru}' sorusu için veritabanında arama yapılıyor...\n")

    try:
        client = qdrant_client.QdrantClient(url="http://localhost:6333")
        embeddings = OllamaEmbeddings(model="embeddinggemma")

        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        llm = OllamaLLM(model="gemma3:4b")

        # Prompt'a "Önceki Sohbet Geçmişi" bölümü eklendi
        prompt = ChatPromptTemplate.from_template("""
Sen dikkatli, tutarlı ve daha önceki konuşmaları asla unutmayan bir yapay zeka asistanısın. 

Aşağıdaki kurallara KESİNLİKLE uymalısın:
1. BAĞLAMA SADAKAT: Kullanıcının sorusuna cevap verirken YALNIZCA aşağıdaki 'Context (Bağlam)' bölümünde verilen bilgileri kullan. Bağlamda cevap yoksa, uydurma yapma ve doğrudan "Bilgi belgelerde bulunamadı" de.
2. GEÇMİŞİ HATIRLAMA: 'Önceki Sohbet Geçmişi' bölümünü dikkatlice oku. Kullanıcının geçmiş mesajlarda sana verdiği özel talimatları, koyduğu kuralları veya sohbetin gidişatını DİKKATE AL ve unutma.
3. TUTARLILIK: Önceki cevaplarınla çelişme. Kullanıcı bir format veya üslup istediyse, yeni cevaplarında da bunu sürdür.
4. DETAY: Cevaplarını detaylı, uzun, anlaşılır ve adım adım şekilde yapılandır.
                                            
                                                  
Önceki Sohbet Geçmişi:
{sohbet_gecmisi}

Context:
{context}

Soru:
{question}
""")

        docs = retriever.invoke(soru)

        context = "\n\n".join([d.page_content for d in docs])

        chain = prompt | llm | StrOutputParser()

        # Invoke ederken sohbet_gecmisi'ni de dahil ediyoruz
        cevap = chain.invoke({
            "context": context,
            "question": soru,
            "sohbet_gecmisi": sohbet_gecmisi
        })

        return cevap

    except Exception as e:
        return f"Hata: {e}"