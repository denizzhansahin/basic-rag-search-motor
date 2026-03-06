import json
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from search_core.config import OLLAMA_MODEL, OLLAMA_BASE_URL



# Sıcaklığı düşük tutuyoruz ki model yaratıcılık yerine formata sadık kalsın
llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0.1,
    base_url = OLLAMA_BASE_URL
)



def ai_answer(query, results):
    context_list = []
    for r in results[:5]:
        if isinstance(r, dict):
            title = r.get('title', 'Bilinmiyor')
            content = r.get('content', '')
            url = r.get('url', '#')
            context_list.append(f"Başlık: {title}\nİçerik: {content[:500]}\nURL: {url}")
        else:
            context_list.append(str(r))
    
    context = "\n\n".join(context_list)

    # Prompt'a kesin komutlar ve daha fazla öneri şablonu eklendi
    sys_prompt = """
Sen gelişmiş bir arama motoru asistanısın. Sana verilen dökümanlara göre kullanıcının sorusunu yanıtla.
Toplamda 5 öneri verebilirsin, eğer 5'ten azsa sadece mevcut kadar öneri ver.
DİKKAT: YANITINI SADECE AŞAĞIDAKİ JSON FORMATINDA VER! Hiçbir markdown etiketi (```json vb.) kullanma. Doğrudan süslü parantez '{' ile başla!
{
  "summary": "Buraya kısa ve detaylı özet yanıtını yaz (Markdown formatında kalın yazılar kullanabilirsin).",
  "suggestions": [
    {"title": "Öneri Başlığı 1", "url": "[https://ornek.com/1](https://ornek.com/1)"},
    {"title": "Öneri Başlığı 2", "url": "[https://ornek.com/2](https://ornek.com/2)"},
    {"title": "Öneri Başlığı 3", "url": "[https://ornek.com/3](https://ornek.com/3)"},
    {"title": "Öneri Başlığı 4", "url": "[https://ornek.com/4](https://ornek.com/4)"},
    {"title": "Öneri Başlığı 5", "url": "[https://ornek.com/5](https://ornek.com/5)"}
  ]
}
"""

    user_prompt = f"Soru:\n{query}\n\nDökümanlar:\n{context}"

    try:
        r = llm.invoke([
            SystemMessage(content=sys_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        # MODELİN GEVZE ÇIKTISINI TEMİZLEME ALANI
        raw_content = r.content.strip()
        # Eğer model inatla markdown etiketi koyduysa bunları kesip atıyoruz
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        if raw_content.startswith("```"):
            raw_content = raw_content[3:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
            
        raw_content = raw_content.strip()

        # Temizlenmiş stringi JSON'a çevir
        response_data = json.loads(raw_content)
        return {
            "summary": response_data.get("summary", "Özet oluşturulamadı."),
            "suggestions": response_data.get("suggestions", [])
        }
    except Exception as e:
        # Hata durumunda konsola modelin ne saçmaladığını yazdır (debug için faydalıdır)
        print(f"JSON Parse Hatası. LLM'in ham çıktısı: {r.content if hasattr(r, 'content') else 'Bilinmiyor'}")
        return {
            "summary": "Yapay zeka özeti oluşturulurken veriler derlenemedi. Lütfen tekrar deneyin.",
            "suggestions": []
        }