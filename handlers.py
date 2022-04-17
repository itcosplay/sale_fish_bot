from environs import Env

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from moltin_api import check_token
from moltin_api import get_products

from loader import dp
from loader import moltin_token

from user_state import UserState

from keyboards import create_default_keyboard
from keyboards import create_product_keyboard

env = Env()
env.read_env()

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(
        text='Здравствуйте! Используйте кнопку меню «Ассортимент»',
        reply_markup=create_default_keyboard()
    )


@dp.message_handler(text='Ассортимент')
async def create_request(message:types.Message,  state:FSMContext):
    token = check_token(
        moltin_token,
        env.str('CLIENT_ID'),
        env.str('CLIENT_SECRET')
    )

    products = get_products(token['access_token'])
    
    await message.answer(
        text='Пожалуйста, выберите товар:',
        reply_markup=create_product_keyboard(products)
    )

    await UserState.select_product.set()


@dp.callback_query_handler(state=UserState.select_product)
async def set_operation_type(
    call:types.CallbackQuery,
    state:FSMContext
):
    if call.data