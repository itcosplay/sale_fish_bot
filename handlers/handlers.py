from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from loader import moltin_token

from keyboards import create_default_keyboard
from keyboards import create_product_keyboard


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(
        text='Здравствуйте! Используйте кнопку меню «Ассортимент»',
        reply_markup=create_default_keyboard()
    )


@dp.message_handler(text='Ассортимент')
async def create_request(message:types.Message):
    await message.delete()

    await message.answer(
        text='Пожалуйста, выберите товар:',
        reply_markup=create_product_keyboard(moltin_token)
    )