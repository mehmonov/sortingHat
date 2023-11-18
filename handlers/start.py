from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from keyboards.keyboards import menu
start_router: Router = Router()
from loader import  db, bot
import sqlite3


@start_router.message(Command('start'))
async def start(message: Message):
    name = message.from_user.full_name
    try:
        db.add_user(id=message.from_user.id, Name=name)
    except :
        await bot.send_message(chat_id=6329800356, text="User bazaga qo'shilmadi.")

    await message.answer(
        "Assalomu alaykum. Fakultetingizni tanlang.", reply_markup=menu
    )

    count = db.count_users()[0]
    msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=6329800356, text=msg)
