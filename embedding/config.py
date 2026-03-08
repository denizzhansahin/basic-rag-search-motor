import os
from dotenv import load_dotenv

# Docker içindeysek, compose'dan gelen değişkenler zaten sistemdedir.
if not os.getenv("IS_DOCKER"):
    load_dotenv()
    print("🏠 Yerel .env yüklendi.")
else:
    print("🐳 Docker ortamı algılandı, ayarlar korunuyor.")

QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
DIMENSION = int(os.getenv("DIMENSION"))  # embeddinggem