import motor.motor_asyncio

from app.config import get_mongo_url

MONGO_DETAILS = get_mongo_url()
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.messages_db
user_collection = database.get_collection("users")
content_collection = database.get_collection("contents")
message_collection = database.get_collection("messages")
