from fastapi import APIRouter
from src.services.connectMongoDB import papers_collection


router = APIRouter()
@router.get("/papers")
async def list_papers():
    cursor = papers_collection.find({}, {"filename": 1})
    papers = [{"paper_id": str(doc["_id"]), "filename": doc["filename"]} async for doc in cursor]
    return papers
