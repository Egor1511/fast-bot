import os
import shutil

from aiogram.types import Message
from fastapi import UploadFile

from app.messages.cache import clear_cache
from app.messages.crud import create_message
from app.messages.models import User, Content


async def save_file(file: UploadFile, directory: str) -> str:
    file_path = f"static/{directory}/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return f"/static/{directory}/{file.filename}"


async def process_message(first_name: str, username: str, content: str,
                          chat_id: int, image: UploadFile = None,
                          video: UploadFile = None) -> Message:
    image_url = await save_file(image, "images") if image else None
    video_url = await save_file(video, "videos") if video else None

    user_data = {"first_name": first_name, "last_name": username}
    content_data = {"text": content, "photo": image_url, "video": video_url}

    new_message = await create_message(User(**user_data),
                                       Content(**content_data), chat_id)
    await clear_cache()
    return new_message
