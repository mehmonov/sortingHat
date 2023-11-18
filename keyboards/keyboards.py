from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🍫 Fakultet tanlash", callback_data="facultcheck")
            
        ],
        [
            InlineKeyboardButton(text="☕️ Admin bilan gaplashish", callback_data="admincall")
            
        ],
        [
            InlineKeyboardButton(text="🎯 Ma'lumot", callback_data="info")
            
        ],

    ],
)