import logging
import os

import aiohttp
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from fast_bot.bot.keyboards.user_keyboard import main_page_kb, home_page_kb

API_URL = os.getenv("API_URL", "http://localhost:8000")
logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Выберите действие:",
                         reply_markup=main_page_kb())


class Form(StatesGroup):
    waiting_for_message = State()


@user_router.message(F.text.contains('Назад'))
async def handle_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Выберите действие:",
                         reply_markup=main_page_kb())


@user_router.message(F.text == '📖 Список всех сообщений')
async def get_messages_command(message: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api/v1/messages/") as response:
                response_data = await response.json()
                if response.status == 200:
                    if not response_data:
                        await message.answer("Сообщений пока нет.",
                                             reply_markup=home_page_kb())
                        return
                    text = "\n\n".join(
                        [
                            f"Имя: {msg['user']['first_name']} {msg['user']['last_name']}\n"
                            f"Сообщение: {msg['content']['text']}\n"
                            f"Фото: {msg['content']['photo'] if msg['content']['photo'] else 'Отсутствует'}\n"
                            f"Видео: {msg['content']['video'] if msg['content']['video'] else 'Отсутствует'}"
                            for msg in response_data])
                    await message.answer(text, reply_markup=home_page_kb())
                else:
                    await message.answer(
                        f"Не удалось получить сообщения: {response_data['detail']}",
                        reply_markup=home_page_kb())
                    logger.error(f"Failed to get messages: {response_data}")
    except Exception as e:
        await message.answer(f"An error occurred: {str(e)}",
                             reply_markup=home_page_kb())
        logger.exception(f"An error occurred while getting messages: {str(e)}")


@user_router.message(F.text == '📝 Новое сообщение')
async def write_message_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Отправьте сообщение:")
    await state.set_state(Form.waiting_for_message)


@user_router.message(F.text, Form.waiting_for_message)
async def post_message_command(message: types.Message, state: FSMContext):
    first_name = message.from_user.first_name
    username = message.from_user.username
    content = message.text
    chat_id = message.chat.id

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/api/v1/message/",
                                    params={"first_name": first_name,
                                            "username": username,
                                            "content": content,
                                            "chat_id": chat_id, }) as response:
                response_data = await response.json()
                if response.status == 200:
                    await message.answer("Сообщение отправлено!",
                                         reply_markup=home_page_kb())
                    await state.clear()
                else:
                    await message.answer(
                        f"Не удалось отправить сообщение: {response_data}",
                        reply_markup=home_page_kb())
                    logger.error(f"Failed to send message:")
                    await state.clear()
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}",
                             reply_markup=home_page_kb())
        logger.exception(f"An error occurred while sending message: ")
        await state.clear()
