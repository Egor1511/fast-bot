from datetime import datetime, timezone

from app.messages.database import message_collection
from app.messages.models import Message, User, Content


async def get_messages(skip: int = 0, limit: int = 10) -> list[Message]:
    messages = []
    cursor = message_collection.find().skip(skip).limit(limit)
    async for document in cursor:
        messages.append(Message(**document))
    return messages


async def create_message(user: User, content: Content,
                         chat_id: int) -> Message:
    user_dict = user.dict()
    content_dict = content.dict()

    message_dict = {
        "user": user_dict,
        "content": content_dict,
        "chat_id": chat_id,
        "created_at": datetime.now(timezone.utc)
    }

    result = await message_collection.insert_one(message_dict)
    new_message = await message_collection.find_one(
        {"_id": result.inserted_id})
    return Message(**new_message)
