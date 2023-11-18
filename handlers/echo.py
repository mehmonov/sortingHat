from aiogram import Router
from aiogram.types import Message

from loader import bot
echo_router: Router = Router()


@echo_router.message()
async def process_any_message(message: Message):
   
    await message.answer(f"Salom {message.from_user.full_name}. Biror gap aytmoqchi bo'lsangiz: https://t.me/husniddin1213")