import os
from dotenv import load_dotenv


# Docker içindeysek, compose'dan gelen değişkenler zaten sistemdedir.
if not os.getenv("IS_DOCKER"):
    load_dotenv()
    print("🏠 Yerel .env yüklendi.")
else:
    print("🐳 Docker ortamı algılandı, ayarlar korunuyor.")




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


DB_AYARLARI = {
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("PORT")
}


COLLECTION_NAME = os.getenv("COLLECTION_NAME")