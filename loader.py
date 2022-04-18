from environs import Env

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from moltin_api import get_access_token

env = Env()
env.read_env()

bot = Bot(token=env.str('TG_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)