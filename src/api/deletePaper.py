from fastapi import APIRouter, HTTPException
from src.services.connectMongoDB import papers_collection
from bson import ObjectId
from src.services.qdrant_client import qdrant_client, COLLECTION_NAME
from qdrant_client.models import Filter, FieldCondition, MatchValue
router = APIRouter()




@router.delete("/papers/{paper_id}")
async def delete_paper(paper_id: str):
    try:
        paper = await papers_collection.find_one({"_id": ObjectId(paper_id)})
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")

     
        result = await papers_collection.delete_one({"_id": ObjectId(paper_id)})

       
        try:
            qdrant_client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="paper_id",
                            match=MatchValue(value=paper_id)
                        )
                    ]
                ),
            )
            print(f" Deleted vectors for paper_id={paper_id} from Qdrant")
        except Exception as e:
            print(f"Qdrant vector delete failed for {paper_id}: {e}")

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Delete failed in MongoDB")

        return {"status": "deleted", "paper_id": paper_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
