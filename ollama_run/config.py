import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")