from fastapi import APIRouter
from src.services.rag_pipeline import answer_query
from src.Class.BaseQuery import QueryRequest
import time
from src.services.connectMongoDB import queries_collection
from src.Class.BaseQuery import QueryRequest
router = APIRouter()



@router.post("/query")
async def query_endpoint(req: QueryRequest):
    start_time = time.time()
    result = answer_query(
        question=req.question,
        top_k=req.top_k,
        paper_ids=req.paper_ids,
    )

    query_doc = {
        "question": req.question,
        "papers_referenced": req.paper_ids or "all",
        "response_time": round(time.time() - start_time, 2),
        "confidence": result.get("confidence", 0.0),
        "createdAt": time.time(),
    }
    await queries_collection.insert_one(query_doc)
    return result
