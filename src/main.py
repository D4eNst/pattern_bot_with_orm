import asyncio
import logging

from aiogram.methods import DeleteWebhook

from bot import dp, bot
from content.handlers.routs import main_router
from content.middlewares.middleware import rg_middlewares
from utils import start_with, stop_with

logging.basicConfig(level=logging.INFO)


async def start_bot():
    # register handlers and start/stop functions
    rg_middlewares(dp)
    dp.include_router(main_router)

    dp.startup.register(start_with)
    dp.shutdown.register(stop_with)

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
