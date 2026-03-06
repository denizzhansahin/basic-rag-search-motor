from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings
from search_core.config import COLLECTION_NAME, EMBEDDING_MODEL, OLLAMA_BASE_URL, QDRANT_URL



client=QdrantClient(url=QDRANT_URL)

embeddings=OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=OLLAMA_BASE_URL
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