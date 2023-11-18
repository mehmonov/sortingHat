from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from loader import bot, db

admin_router: Router = Router()

@admin_router.message(F.text == 'boshqaruv')
async def admin_panel(message: Message):
    if message.from_user.id == 6329800356:
        await message.answer('admin panelga xush kelibsiz aka :)')
        
        await message.answer(
            f"Ho'sh, bugungacha botdan ro'yhatdan o'tganlar soni {db.count_users()[0]} \n\n\n\n\n Fakultetlar bo'yicha: \n\n {db.count_users_by_facultet()}",
        )
    else:
        await message.answer('siz admin emassiz')
