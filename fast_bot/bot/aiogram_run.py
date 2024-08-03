import asyncio
import logging

from create_bot import bot, dp
from fast_bot.bot.hendlers.user_handler import user_router


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(user_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(),
                           skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
