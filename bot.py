import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config, load_config

from handlers.echo import echo_router
from handlers.menu import menu_router
from handlers.start import start_router
from handlers.admin import  admin_router
from loader import bot, db
logger = logging.getLogger(__name__)



async def main():
    logging.basicConfig(
        level=logging.INFO,
       
    )
        # Ma'lumotlar bazasini yaratamiz:
    try:
        db.create_table_users()
    except Exception as err:
        print(err)

    logger.info("Starting bot")


    dp: Dispatcher = Dispatcher()

    dp.include_routers(
        admin_router,
        menu_router,
        start_router,
        echo_router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
