import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

ACCEPT_URL = os.getenv("ACCEPT_URL").split(",")
SECRET_KEY = os.getenv("SECRET_KEY")




# 2. REDIS BAĞLANTISI (Docker üzerinden gelecek)
# 1. Önce ortam değişkenlerini al
REDIS_HOST = os.getenv("REDIS_HOST", "redis_broker")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

