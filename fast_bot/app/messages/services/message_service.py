import os
import shutil

from aiogram.types import Message
from fastapi import UploadFile

from messages.cache import clear_cache
from messages.crud import create_message
from messages.models import User, Content


async def save_file(file: UploadFile, directory: str) -> str:
    """
    Save an uploaded file to a specified directory.
    Args:
        file (UploadFile): The uploaded file to be saved.
        directory (str): The directory where the file will be saved.
    Returns:
        str: The URL of the saved file.
    """
    file_path = f"static/{directory}/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return f"/static/{directory}/{file.filename}"


async def process_message(first_name: str, username: str, content: str,
                          chat_id: int, image: UploadFile = None) -> Message:
    """
    Process a message by saving an uploaded image, creating a user and content object,
    and creating a new message.
    Args:
        first_name (str): The first name of the user.
        username (str): The username of the user.
        content (str): The content of the message.
        chat_id (int): The ID of the chat.
        image (UploadFile, optional): The uploaded image file. Defaults to None.
    Returns:
        Message: The newly created message.
    This function first checks if an image file is provided. If so, it saves the image
    to the "images" directory and retrieves the URL of the saved image. It then creates
    a user object with the provided first name and username, and a content object with
    the provided content and image URL. Finally, it creates a new message using the
    user, content, and chat ID, clears the cache, and returns the newly created message.
    """
    image_url = await save_file(image, "images") if image else None

    user_data = {"first_name": first_name, "last_name": username}
    content_data = {"text": content, "photo": image_url}

    new_message = await create_message(User(**user_data),
                                       Content(**content_data), chat_id)
    await clear_cache()
    return new_message
