from fastapi import UploadFile, File, \
    APIRouter

from app.messages.cache import set_cache, get_cache
from app.messages.crud import get_messages
from app.messages.models import Message
from app.messages.services.message_service import process_message

messages_router = APIRouter(
    prefix="/api/v1",
)


@messages_router.get("/messages/", response_model=list[Message])
async def read_messages(skip: int = 0, limit: int = 10):
    cache_key = f"messages_{skip}_{limit}"
    cached_messages = await get_cache(cache_key)
    if cached_messages:
        return cached_messages

    messages = await get_messages(skip=skip, limit=limit)
    await set_cache(cache_key, messages)
    return messages


@messages_router.post("/message/", response_model=Message)
async def write_message(first_name: str, username: str, content: str,
                        chat_id: int, image: UploadFile = File(None),
                        video: UploadFile = File(None)):
    new_message = await process_message(first_name, username, content, chat_id,
                                        image, video)
    return new_message
