from fastapi import APIRouter, HTTPException
from src.services.connectMongoDB import papers_collection
from bson import ObjectId


router = APIRouter()
@router.get("/papers/{paper_id}/stats")
async def paper_stats(paper_id: str):
    try:
        paper = await papers_collection.find_one({"_id": ObjectId(paper_id)})
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")

        stats = {
            "filename": paper["filename"],
            "num_sections": len(paper["sections"]),
            "num_pages": max(s["page"] for s in paper["sections"]),
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
