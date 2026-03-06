import os

# Sabit localhost yerine .env/docker-compose'dan gelen veriyi alıyoruz
DB_AYARLARI = {
    "host": os.getenv("DATABASE_HOST", "host.docker.internal"),
    "database": os.getenv("DATABASE_NAME", "arama_motoru_db"),
    "user": os.getenv("DATABASE_USER", "postgres"),
    "password": os.getenv("DATABASE_PASSWORD", "gizlisifrem"),
    "port": os.getenv("DATABASE_PORT", "5432")
}

QDRANT_URL = os.getenv("QDRANT_URL", "http://host.docker.internal:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "ollama_my_rag_collection")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
DIMENSION = int(os.getenv("DIMENSION"))  # embeddinggem


"""
DB_AYARLARI = {
    "host": "localhost",
    "database": "arama_motoru_db",
    "user": "postgres",
    "password": "gizlisifrem",
    "port": "5432"
}


QDRANT_URL="http://localhost:6333"
COLLECTION_NAME="ollama_my_rag_collection"


"""
