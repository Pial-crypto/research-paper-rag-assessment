from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

qdrant_client = QdrantClient(
    url="https://61aadc77-8e8c-49a6-b633-f6f8aed79829.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.tSKkTqbC5sGvakuEpCNbCmZtC0V_sbGI55rMnPSwxSw",
)

# Create a collection
collection_name = "research_papers"

qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

print(qdrant_client.get_collections())
