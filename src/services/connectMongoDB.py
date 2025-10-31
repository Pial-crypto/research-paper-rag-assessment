from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
MONGO_URI = "mongodb://localhost:27017/"
mongo_client = AsyncIOMotorClient(MONGO_URI, server_api=ServerApi("1"))
db = mongo_client["paper_database"]
papers_collection = db["papers"]
queries_collection = db["queries"]