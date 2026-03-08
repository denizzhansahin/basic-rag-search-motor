import os
from dotenv import load_dotenv


# Docker içindeysek, compose'dan gelen değişkenler zaten sistemdedir.
if not os.getenv("IS_DOCKER"):
    load_dotenv()
    print("🏠 Yerel .env yüklendi.")
else:
    print("🐳 Docker ortamı algılandı, ayarlar korunuyor.")
    HOST = os.getenv("DB_HOST", "rag_postgres_yeni")


DB_AYARLARI = {
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("PORT")
}

print("DB Ayarları")
print(DB_AYARLARI)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
