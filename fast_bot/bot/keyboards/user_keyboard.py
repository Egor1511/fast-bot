from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_page_kb() -> ReplyKeyboardMarkup:
    kb_list = [[KeyboardButton(text="📖 Список всех сообщений")],
               [KeyboardButton(text="📝 Новое сообщение")], ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )


def home_page_kb() -> ReplyKeyboardMarkup:
    kb_list = [[KeyboardButton(text="🔙 Назад")]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
