from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# MongoDB connection URI
MONGO_DETAILS = f"mongodb://{settings.mongo_username}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}"

# Async MongoDB client
client = AsyncIOMotorClient(MONGO_DETAILS)

# Database reference
db = client[settings.mongo_db]

# Collection references
users_collection = db.get_collection("users")
assignments_collection = db.get_collection("assignments")
