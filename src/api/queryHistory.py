from fastapi import APIRouter
from src.services.connectMongoDB import queries_collection
from collections import Counter
router = APIRouter()


@router.get("/queries/history")
async def get_query_history():
    cursor = queries_collection.find().sort("createdAt", -1)
    history = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        history.append(doc)
        if len(history) >= 5:
            break
    return history
