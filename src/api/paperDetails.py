
from fastapi import APIRouter, HTTPException
from src.services.connectMongoDB import papers_collection
from bson import ObjectId
router = APIRouter()
@router.get("/papers/{paper_id}")
async def get_paper(paper_id: str):
    try:
        paper = await papers_collection.find_one({"_id": ObjectId(paper_id)})
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        paper["_id"] = str(paper["_id"])
        return paper
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid paper ID")
