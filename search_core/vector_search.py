from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings

QDRANT_URL="http://localhost:6333"
COLLECTION_NAME="ollama_my_rag_collection"

client=QdrantClient(url=QDRANT_URL)

embeddings=OllamaEmbeddings(
    model="embeddinggemma"
)


def vector_search(query,limit=40):

    vec=embeddings.embed_query(query)

    r=client.query_points(
        collection_name=COLLECTION_NAME,
        query=vec,
        limit=limit,
        with_payload=True
    )

    return r.points