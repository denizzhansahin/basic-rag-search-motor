import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

DB_USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")

#DB_URL = "postgresql+psycopg2://postgres:gizlisifrem@127.0.0.1:5432/arama_motoru_db"
# F-string kullanarak temiz bir URL oluşturma
DB_URL = f"postgresql+psycopg2://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Kontrol için (Şifreyi gizleyerek yazdırmak güvenlidir)
print(f"Bağlantı adresi hazır: postgresql+psycopg2://{DB_USER}:***@{HOST}:{PORT}/{DATABASE}")
REDIS_HOST = os.getenv("REDIS_HOST", "redis_broker") 
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))