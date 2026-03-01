import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from redis import Redis
from rq import Queue, Worker
from datetime import datetime
import sys
from pathlib import Path






import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from redis import Redis
from rq import Queue, Worker
from datetime import datetime
import sys
from pathlib import Path

# --- AYARLAR VE BAĞLANTI ---
DB_URL = "postgresql+psycopg2://postgres:gizlisifrem@127.0.0.1:5432/arama_motoru_db"
engine = create_engine(DB_URL)

st.set_page_config(page_title="RAG Komuta Merkezi", layout="wide")

# --- TABLO KONTROLÜ ---
def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS hedef_siteler (
                id SERIAL PRIMARY KEY,
                ana_url VARCHAR(2048) UNIQUE NOT NULL,
                max_sayfa INTEGER DEFAULT 10,
                durum VARCHAR(50) DEFAULT 'bekliyor',
                son_tarama_tarihi TIMESTAMP
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS taranan_linkler (
                id SERIAL PRIMARY KEY,
                url VARCHAR(2048) UNIQUE NOT NULL,
                baslik VARCHAR(500),
                aciklama TEXT,
                icerik_ozeti VARCHAR(1000), 
                erisim_tarihi TIMESTAMP
            );
        """))
        conn.commit()

init_db()

# --- VERİ FONKSİYONLARI ---

def get_target_sites():
    query = """
        SELECT 
            ana_url, max_sayfa, durum, 
            CASE 
                WHEN son_tarama_tarihi IS NULL THEN 'Hemen'
                ELSE TO_CHAR((son_tarama_tarihi + INTERVAL '5 hours') - NOW(), 'HH24:MI:SS')
            END as kalan_süre
        FROM hedef_siteler
        ORDER BY id DESC
    """
    return pd.read_sql(query, engine)

def get_db_stats():
    try:
        with engine.connect() as conn:
            total = conn.execute(text("SELECT COUNT(*) FROM taranan_linkler")).scalar()
            pending = conn.execute(text("SELECT COUNT(*) FROM taranan_linkler WHERE baslik = 'no_data'")).scalar()
            completed = total - pending
            recent = pd.read_sql("SELECT url, baslik, erisim_tarihi FROM taranan_linkler WHERE baslik != 'no_data' ORDER BY erisim_tarihi DESC LIMIT 10", engine)
        return {"total": total, "pending": pending, "completed": completed, "recent": recent}
    except: return None

# --- ARAYÜZ (GÖVDE) ---
st.title("🚀 RAG Search - Admin Komuta Merkezi")

stats = get_db_stats()
if stats:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Toplam Link", stats["total"])
    m2.metric("Bekleyen", stats["pending"], delta_color="inverse")
    
    # Redis Bilgileri
    try:
        r_conn = Redis(host='localhost', port=6379, decode_responses=True)

        queue_size = r_conn.llen("link_kuyrugu")

        failed_queue = r_conn.llen("hatali_linkler")

        success_jobs = r_conn.get("basarili_is") or 0
        failed_jobs = r_conn.get("basarisiz_is") or 0

        workers = r_conn.scard("aktif_workerlar")

        active_job = r_conn.get("aktif_is")

        c1,c2,c3,c4,c5 = st.columns(5)

        c1.metric("Bekleyen İş", queue_size)

        c2.metric("Başarılı İş", success_jobs)

        c3.metric("Başarısız İş", failed_jobs)

        c4.metric("Worker Sayısı", workers)

        if active_job:
            c5.metric("Aktif İş", "1")
        else:
            c5.metric("Aktif İş", "0")
    except:
        st.sidebar.error("Redis bağlantısı kurulamadı!")

st.divider()

col_l, col_r = st.columns([1.2, 0.8])

with col_l:
    st.subheader("🌐 Hedef Siteler (Düzenlenebilir)")
    df = get_target_sites()
    
    # --- CANLI EDİTÖR ---
    # Tabloyu düzenlenebilir hale getiriyoruz
    edited_df = st.data_editor(
        df,
        column_config={
            "ana_url": st.column_config.TextColumn("Site URL", disabled=True), # URL değiştirilemez (Key)
            "max_sayfa": st.column_config.NumberColumn("Maksimum Sayfa", min_value=1, max_value=2000, step=1),
            "durum": st.column_config.TextColumn("Durum", disabled=True),
            "kalan_süre": st.column_config.TextColumn("Kalan Süre", disabled=True),
        },
        use_container_width=True,
        hide_index=True,
        key="site_editor"
    )

    # Değişiklik varsa kaydet butonu çıkar
    if st.button("Değişiklikleri Veritabanına Kaydet"):
        with engine.connect() as conn:
            for index, row in edited_df.iterrows():
                conn.execute(
                    text("UPDATE hedef_siteler SET max_sayfa = :p WHERE ana_url = :u"),
                    {"p": row["max_sayfa"], "u": row["ana_url"]}
                )
            conn.commit()
        st.success("Tüm sayfa sayıları güncellendi!")
        st.rerun()

    # --- SİTE EKLEME ---
    with st.expander("➕ Yeni Site Ekle"):
        new_url = st.text_input("Site URL (https://...):")
        new_pages = st.number_input("Başlangıç Sayfa Sayısı:", 1, 1000, 50)
        if st.button("Listeye Ekle"):
            if new_url:
                with engine.connect() as conn:
                    try:
                        conn.execute(
                            text("INSERT INTO hedef_siteler (ana_url, max_sayfa) VALUES (:u, :p)"),
                            {"u": new_url, "p": new_pages}
                        )
                        conn.commit()
                        st.success(f"{new_url} eklendi!")
                        st.rerun()
                    except: st.error("Bu site zaten mevcut!")

with col_r:
    st.subheader("🕒 Son Tarananlar")
    if stats: st.table(stats["recent"])

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Sistem Kontrol")
    if st.button("🔄 Paneli Yenile"): st.rerun()
    
    st.divider()
    if st.button("♻️ Kurtarma Botunu Tetikle"):
        try:
            from postgresql_islem.redis_secure_bot import eksik_linkleri_kuyruga_at
            eksik_linkleri_kuyruga_at()
            st.success("Kurtarma başlatıldı!")
        except Exception as e: st.error(f"Hata: {e}")