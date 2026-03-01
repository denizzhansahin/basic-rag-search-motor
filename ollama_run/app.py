import sys
from pathlib import Path

# Şu anki dosyanın bulunduğu klasörü bul ve bir üst klasöre git
base_path = Path(__file__).resolve().parent.parent 
sys.path.append(str(base_path))

# Artık üst klasördeki veya yan klasördeki dosyaları görebilir
# Örneğin: from alt_klasor.embedding import embedding_pdf


from embedding.embedding_pdf import embedding_pdf
from embedding.embeddin_url_selenium import embedding_url
from embedding.embedding_save_qdrant import qdranta_kaydet
import streamlit as st # DOĞRU OLAN BU
import tempfile
import os

# Kendi yazdığın RAG okuma fonksiyonunu içe aktar
from ollama_rag_read import soru_sor

# EĞER kayıt (veri hazırlama) fonksiyonlarını da ayrı dosyalara yazdıysan, 
# buradaki yorum ( # ) işaretlerini kaldırıp kendi fonksiyonlarını bağlayabilirsin.
# from veri_hazirlama import pdf_oku_ve_bol, url_oku_ve_bol
# from veritabani_kayit import qdranta_kaydet

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Gemma RAG Asistanı", page_icon="🧠", layout="wide")

# --- 2. SESSİON STATE (BELLEK/HAFIZA) AYARLARI ---
# Ekranda görünecek mesaj geçmişi (İlk açıldığında asistanın selam vermesini sağlıyoruz)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Yüklediğin belgelere dayanarak sana nasıl yardımcı olabilirim?"}
    ]

# Arka planda modele gidecek Kayan Pencere (Sliding Window) hafızası
if "memory_window" not in st.session_state:
    st.session_state.memory_window = []

MAX_GECMIS_SAYISI = 30 

# --- 3. YAN MENÜ (SIDEBAR) KONTROL PANELİ ---
with st.sidebar:
    st.image("https://ollama.com/public/ollama.png", width=100) # Orijinal Ollama logosu
    st.title("⚙️ RAG Kontrol Paneli")
    st.markdown("Veritabanınızı (Qdrant) buradan besleyin.")
    
    # -- ÖZELLİK 1: PDF YÜKLEME --
    st.subheader("📄 PDF Dosyası Ekle")
    uploaded_file = st.file_uploader("Bir PDF dosyası seçin", type=["pdf"])
    
    if st.button("PDF'i Veritabanına Kaydet"):
        if uploaded_file is not None:
            with st.spinner("PDF işleniyor ve vektörlere çevriliyor..."):
                # Önemli: Streamlit'e yüklenen dosya RAM'de durur. 
                # PDF okuyucu kütüphaneler dosya yolu (path) ister. 
                # Bu yüzden geçici bir dosya (tempfile) oluşturup içine yazıyoruz.
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # ------ VERİ KAYDETME KODUN BURAYA GELECEK ------
                # Örnek Kullanım:
                parcalar = embedding_pdf(tmp_file_path)
                qdranta_kaydet(parcalar, collection_name="ollama_my_rag_collection")
                # ------------------------------------------------
                
                st.success(f"✅ '{uploaded_file.name}' başarıyla Qdrant'a eklendi!")
                os.unlink(tmp_file_path) # İşlem bitince geçici dosyayı çöpe at
        else:
            st.warning("Lütfen önce bir PDF dosyası sürükleyip bırakın.")

    st.divider() # Araya şık bir çizgi çeker

    # -- ÖZELLİK 2: WEB (URL) YÜKLEME --
    st.subheader("🌐 Web Sayfası Ekle")
    url_input = st.text_input("Bir web sayfası linki (URL) yapıştırın:")
    
    if st.button("URL'yi Veritabanına Kaydet"):
        if url_input:
            with st.spinner("Web sitesi okunuyor (Selenium)..."):
                
                # ------ VERİ KAYDETME KODUN BURAYA GELECEK ------
                # Örnek Kullanım:
                parcalar = embedding_url(url_input)
                qdranta_kaydet(parcalar, collection_name="ollama_my_rag_collection")
                # ------------------------------------------------
                
                st.success("✅ Web sayfası başarıyla vektörleştirildi!")
        else:
            st.warning("Lütfen geçerli bir URL girin.")

    st.divider()

    # -- ÖZELLİK 3: SOHBET HAFIZASINI SIFIRLAMA --
    st.subheader("🧹 Bellek Yönetimi")
    st.markdown("Modelin kafası karışırsa geçmişi temizleyin.")
    if st.button("Sohbet Geçmişini Temizle", type="primary"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Geçmiş temizlendi. Yepyeni bir konuya başlayabiliriz!"}
        ]
        st.session_state.memory_window = []
        st.rerun() # Sayfayı zorla yeniler, ekranı temizler

# --- 4. ANA EKRAN (SOHBET ARAYÜZÜ) ---
st.title("🧠 Gemma RAG Asistanı")
st.markdown("*Tamamen yerel, gizlilik odaklı ve Qdrant destekli asistanınız.*")

# Bellekteki mesajları sırayla ekrana çiz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Yeni soru alma (Walrus ':=' operatörü ile)
if prompt := st.chat_input("Veritabanındaki belgelerle ilgili bir soru sorun..."):
    
    # 1. Kullanıcı sorusunu ekrana bas
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Asistanın cevabını al ve ekrana bas
    with st.chat_message("assistant"):
        with st.spinner("Gemma belgeleri inceliyor..."):
            
            aktif_gecmis_metni = "".join(st.session_state.memory_window[-MAX_GECMIS_SAYISI:])
            
            # Kendi fonksiyonumuza soruyu ve hafızayı gönderiyoruz
            cevap = soru_sor(
                soru=prompt, 
                sohbet_gecmisi=aktif_gecmis_metni, 
                collection_name="ollama_my_rag_collection"
            )
            
            st.markdown(cevap)
            
    # 3. İlerisi için bu sohbeti belleğe kaydet
    st.session_state.messages.append({"role": "assistant", "content": cevap})
    st.session_state.memory_window.append(f"Kullanıcı: {prompt}\nAsistan: {cevap}\n\n")