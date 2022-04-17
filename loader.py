from environs import Env

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from moltin_api import get_access_token

env = Env()
env.read_env()

bot = Bot(token=env.str('TG_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)

moltin_token = get_access_token(
    env.str('CLIENT_ID'), env.str('CLIENT_SECRET')
)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)