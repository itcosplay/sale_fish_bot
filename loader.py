from environs import Env

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

env = Env()
env.read_env()

bot = Bot(token=env.str('TG_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
moltin_token = '0388c8fc1485a163ad70fe0a08d4bd4bf1104ce8'