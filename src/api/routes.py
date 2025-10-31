from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.pdf_processor import extract_text_with_sections
from src.services.embedding_service import get_embeddings
from src.services.rag_pipeline import answer_query
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from src.Class.BaseQuery import QueryRequest
from src.services.qdrant_client import ensure_collection, upsert_vectors, COLLECTION_NAME,qdrant_client
from qdrant_client import QdrantClient
import uuid, time, os
from collections import Counter
from src.services.connectMongoDB import mongo_client, papers_collection, queries_collection
from src.api.uploadPaper import router as upload_router
from src.api.paperList import router as paperlist_router
from src.api.paperDetails import router as paperdetails_router
from src.api.paperStats import router as paperstats_router
from src.api.deletePaper import router as deletepaper_router
from src.api.query import router as query_router
from src.api.queryHistory import router as queryhistory_router
from src.api.analyticsPopuler import router as analyticspopuler_router

from qdrant_client.models import Filter, FieldCondition, MatchValue
router = APIRouter()


# -----------------------------
# MongoDB Setup
# -----------------------------


try:
    mongo_client.admin.command("ping")
    print("MongoDB connected")
except Exception as e:
    print("MongoDB connection failed:", e)


ensure_collection()

router.include_router(upload_router)
router.include_router(paperlist_router)
router.include_router(paperdetails_router)
router.include_router(paperstats_router)
router.include_router(deletepaper_router)
router.include_router(query_router)
router.include_router(queryhistory_router)
router.include_router(analyticspopuler_router)












