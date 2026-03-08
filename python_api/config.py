import os
from dotenv import load_dotenv


# Docker içindeysek, compose'dan gelen değişkenler zaten sistemdedir.
if not os.getenv("IS_DOCKER"):
    load_dotenv()
    print("🏠 Yerel .env yüklendi.")
else:
    print("🐳 Docker ortamı algılandı, ayarlar korunuyor.")


ACCEPT_URL = os.getenv("ACCEPT_URL").split(",")
SECRET_KEY = os.getenv("SECRET_KEY")




# 2. REDIS BAĞLANTISI (Docker üzerinden gelecek)
# 1. Önce ortam değişkenlerini al
REDIS_HOST = os.getenv("REDIS_HOST", "redis_broker")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_MODEL_VISION = os.getenv("OLLAMA_MODEL_VISION")
DIMENSION = int(os.getenv("DIMENSION"))  # embeddinggem


