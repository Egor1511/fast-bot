from fastapi import UploadFile, File, \
    APIRouter

from messages.cache import set_cache, get_cache
from messages.crud import get_messages
from messages.models import Message
from messages.services.message_service import process_message

messages_router = APIRouter(
    prefix="/api/v1",
)


@messages_router.get("/messages/", response_model=list[Message])
async def read_messages(skip: int = 0, limit: int = 10):
    """
    Retrieves a list of messages from the database, with optional pagination.
    Args:
        skip (int, optional): The number of messages to skip. Defaults to 0.
        limit (int, optional): The maximum number of messages to retrieve. Defaults to 10.
    Returns:
        list[Message]: A list of Message objects representing the retrieved messages.
    """
    cache_key = f"messages_{skip}_{limit}"
    cached_messages = await get_cache(cache_key)
    if cached_messages:
        return cached_messages

    messages = await get_messages(skip=skip, limit=limit)
    await set_cache(cache_key, messages)
    return messages


@messages_router.post("/message/", response_model=Message)
async def write_message(first_name: str, username: str, content: str,
                        chat_id: int, image: UploadFile = File(None)):
    """
    Endpoint to write a new message to the database.
    Parameters:
        - first_name (str): The first name of the user sending the message.
        - username (str): The username of the user sending the message.
        - content (str): The content of the message.
        - chat_id (int): The ID of the chat where the message is being sent.
        - image (UploadFile, optional): The image file to be sent with the message. Defaults to None.
    Returns:
        - Message: The newly created message object.
    """
    new_message = await process_message(first_name, username, content, chat_id,
                                        image)
    return new_message
