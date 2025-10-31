from fastapi import APIRouter
from src.services.connectMongoDB import queries_collection
from collections import Counter
router = APIRouter()

@router.get("/analytics/popular")
async def popular_queries():
    cursor = queries_collection.find()
    questions = [q["question"] async for q in cursor]
    counter = Counter(questions)
    return counter.most_common(10)
