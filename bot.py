from aiogram import executor
from handlers import dp


async def on_startup(dispatcher):
    print('Bot was started')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)