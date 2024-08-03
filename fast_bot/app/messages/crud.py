from datetime import datetime, timezone

from messages.database import message_collection
from messages.models import Message, User, Content


async def get_messages(skip: int = 0, limit: int = 10) -> list[Message]:
    """
    Retrieves a list of messages from the database.
    Args:
        skip (int, optional): The number of messages to skip. Defaults to 0.
        limit (int, optional): The maximum number of messages to retrieve. Defaults to 10.
    Returns:
        list[Message]: A list of Message objects.
    """

    messages = []
    cursor = message_collection.find().skip(skip).limit(limit)
    async for document in cursor:
        messages.append(Message(**document))
    return messages


async def create_message(user: User, content: Content,
                         chat_id: int) -> Message:
    """
    Create a new message with the given user, content, and chat ID.
    Args:
        user (User): The user who sent the message.
        content (Content): The content of the message.
        chat_id (int): The chat ID where the message was sent.
    Returns:
        Message: The newly created message.
    """
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
