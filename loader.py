from config import Config, load_config
from aiogram import Bot, Dispatcher
from models.database.sqlite import Database



config: Config = load_config()
bot: Bot = Bot(token="6462565189:AAGWj75nUp4n97FDK-0WuTyLJb-Tn65kW84", parse_mode="HTML")
db = Database(path_to_db="main.db")