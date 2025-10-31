from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from src.config import COLLECTION_NAME, QDRANT_URL, QDRANT_API_KEY

print(COLLECTION_NAME, QDRANT_URL, QDRANT_API_KEY)


if QDRANT_API_KEY:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    client = QdrantClient(url=QDRANT_URL)

qdrant_client = client

def ensure_collection():
    try:
        collections = [col.name for col in client.get_collections().collections]
        if COLLECTION_NAME not in collections:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)
            )
            print(f"Created new Qdrant collection: {COLLECTION_NAME}")
        else:
            print(f"Qdrant collection '{COLLECTION_NAME}' already exists.")
    except Exception as e:
        print(" Qdrant connection/setup failed:", e)


def upsert_vectors(points):
    try:
        qdrant_points = [
            PointStruct(id=p["id"], vector=p["vector"], payload=p["payload"])
            for p in points
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=qdrant_points)
        print(f" {len(points)} vectors upserted to Qdrant")
    except Exception as e:
        print(" Qdrant upsert failed:", e)
        raise


def search_vector(query_vector, top_k=5):
    try:
        result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        return result
    except Exception as e:
        print(" Qdrant search failed:", e)
        raise
