import asyncio
import json
import os
import base64
import io
from langchain_ollama import OllamaLLM, ChatOllama
from langchain_core.messages import HumanMessage
from python_api.config import OLLAMA_MODEL, OLLAMA_MODEL_VISION
from search_core.pipeline import search_pipeline

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 yüklü değil! PDF okuma çalışmayabilir. (pip install PyPDF2)")

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

router_llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL, temperature=0)
chat_llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL, temperature=0.3)
vision_llm = ChatOllama(model=OLLAMA_MODEL_VISION, base_url=OLLAMA_URL, temperature=0.3)

# 1. YÖNLENDİRİCİ ARTIK DOSYA İÇERİĞİNİ DE BİLİYOR
async def should_search(query, history, file_context):
    if not history and not file_context:
        return True 
        
    prompt = f"""Sen bir arama motoru yönlendiricisisin. Kararını sadece EVET veya HAYIR olarak ver.
    
Son Konuşulanlar: {history[-2:] if len(history) >= 2 else history}
Kullanıcının Yüklediği Dosya İçeriği: {file_context[:10000] if file_context else 'Yok'}
Kullanıcının Sorusu: "{query}"

KURALLAR:
1. Eğer kullanıcı YALNIZCA yüklediği dosya hakkında soru soruyorsa ("bu dosyayı özetle", "belgede ne yazıyor", "bunu yorumla") -> "HAYIR" yaz.
2. Eğer kullanıcı dosyadaki bir bilgiyi alıp dış dünyayla veya internetle karşılaştırmanı istiyorsa (örn: "Belgedeki bu şirket şu an ne yapıyor?") -> "EVET" yaz.
3. Yepyeni bir konu açıyorsa veya güncel bir bilgi istiyorsa -> "EVET" yaz.

SADECE "EVET" veya "HAYIR" YAZ."""

    #cevap = await asyncio.to_thread(router_llm.invoke, prompt)

    # YENİ HALİ (Doğrudan ainvoke kullanıyoruz):
    cevap = await router_llm.ainvoke(prompt)

    karar = "EVET" in str(cevap).upper()
    print(f"🧠 [ROUTER KARARI] Soru: '{query}' -> Arama Yapılacak Mı? {karar}")
    return karar

async def process_ai_chat(job_id, redis_client, query, history, file_b64, file_type):
    print(f"🤖 [AI CHAT BAŞLADI] Soru: {query}")
    try:
        sources = []
        context_text = ""
        file_context_for_router = ""
        is_image = False

        # 1. ADIM: ÖNCE DOSYAYI OKU (Router karar vermeden önce içeriği bilelim)
        if file_b64 and file_type:
            print(f"📦 Dosya algılandı: {file_type}. RAM'de işleniyor...")
            
            if file_type == 'text/plain':
                decoded_text = base64.b64decode(file_b64).decode('utf-8')
                file_context_for_router = f"[YÜKLENEN TXT DOSYASI]:\n{decoded_text[:3000]}\n"
            
            elif file_type == 'application/pdf':
                try:
                    pdf_bytes = base64.b64decode(file_b64)
                    pdf_file = io.BytesIO(pdf_bytes)
                    reader = PyPDF2.PdfReader(pdf_file)
                    pdf_text = "".join([page.extract_text() + "\n" for page in reader.pages[:5]])
                    file_context_for_router = f"[YÜKLENEN PDF DOSYASI]:\n{pdf_text[:3000]}\n"
                except Exception as e:
                    print(f"PDF Okuma Hatası: {e}")
                    file_context_for_router = "[UYARI: PDF okunamadı, şifreli veya bozuk olabilir.]\n"
            
            elif file_type.startswith('image/'):
                is_image = True 
                file_context_for_router = "[Kullanıcı bir görsel yükledi.]\n"

            context_text += file_context_for_router

        # 2. ADIM: YÖNLENDİRİCİYE SOR (Artık dosya içeriğini bilerek karar veriyor)
        needs_search = await should_search(query, history, file_context_for_router)

        # 3. ADIM: ARAMA GEREKİYORSA ARAMA YAP
        if needs_search:
            print("🔍 Arama motoru tetiklendi...")
            search_results = await asyncio.to_thread(search_pipeline, query, [])
            top_results = search_results[:4] 
            sources = top_results 
            
            context_text += "\n[ARAMA MOTORUNDAN GELEN YENİ KAYNAKLAR]:\n"
            for r in top_results:
                 if isinstance(r, dict):
                     context_text += f"- {r.get('title')}: {r.get('content')[:500]}\n"

        # 4. ADIM: YAPAY ZEKAYA GÖNDER
        chat_prompt = f"""Kullanıcı sana bir soru sordu. Dosya yüklenmişse veya arama yapılmışsa veriler aşağıdadır.
        
[VERİLER]
{context_text}

[ÖNCEKİ SOHBET]
{history}

Kullanıcı: {query}
Asistan:"""

        if is_image:
            print("📸 Görsel analizi için Llama 3.2 Vision modeli kullanılıyor...")
            message = HumanMessage(
                content=[
                    {"type": "text", "text": chat_prompt},
                    {"type": "image_url", "image_url": f"data:{file_type};base64,{file_b64}"}
                ]
            )
            #ai_response_obj = await asyncio.to_thread(vision_llm.invoke, [message])
            ai_response_obj = await vision_llm.ainvoke([message])
        else:
            print("💬 Standart model kullanılıyor...")
            #ai_response_obj = await asyncio.to_thread(chat_llm.invoke, chat_prompt)
            ai_response_obj = await chat_llm.ainvoke(chat_prompt)

        # 🚀 STR VS OBJECT HATASININ KESİN ÇÖZÜMÜ BURADA:
        if isinstance(ai_response_obj, str):
            ai_response = ai_response_obj
        else:
            ai_response = ai_response_obj.content

        # 5. ADIM: REACT'A GÖNDER
        response_payload = {
            "type": "AI_CHAT_REPLY",
            "message": ai_response,
            "sources": sources,
            "didSearch": needs_search
        }
        
        await redis_client.publish(f"job:{job_id}", json.dumps(response_payload, default=str))
        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "DONE"}))

    except Exception as e:
        print(f"❌ [AI CHAT ERROR] {e}")
        await redis_client.publish(f"job:{job_id}", json.dumps({"type": "ERROR", "message": str(e)}, default=str))