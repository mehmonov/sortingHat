from config import Config, load_config
from aiogram import Bot, Dispatcher
from models.database.sqlite import Database



config: Config = load_config()
bot: Bot = Bot(token="6371651493:AAHDDFwX6V-i16Cc1Lbi8uD3gwdyVMnW9VA", parse_mode="HTML")
db = Database(path_to_db="main.db")