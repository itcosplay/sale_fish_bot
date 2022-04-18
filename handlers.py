import pprint

from environs import Env

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from moltin_api import get_actual_token
from moltin_api import get_products
from moltin_api import get_product

from loader import dp

from user_state import UserState

from keyboards import create_default_keyboard
from keyboards import create_product_keyboard

from handle_data_lib import create_product_description_text


env = Env()
env.read_env()

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(
        text='Здравствуйте! Используйте кнопку меню «Ассортимент»',
        reply_markup=create_default_keyboard()
    )


@dp.message_handler(text='Ассортимент')
async def show_products(message:types.Message,  state:FSMContext):
    moltin_token = get_actual_token(
        env.str('CLIENT_ID'),
        env.str('CLIENT_SECRET')
    )
    print('ACTUAL TOKEN: ', moltin_token)
    products = get_products(moltin_token)
    
    await message.answer(
        text='Пожалуйста, выберите товар:',
        reply_markup=create_product_keyboard(products)
    )

    await UserState.select_product.set()


@dp.callback_query_handler(state=UserState.select_product)
async def show_selected_product(
    call:types.CallbackQuery,
    state:FSMContext
):
    if call.data == 'cancel':
        await call.message.answer(
            text='Вернуться к выбору можно через кнопку «Ассортимент»',
            reply_markup=create_default_keyboard()
        )
        await state.finish()

    else:
        moltin_token = get_actual_token(
            env.str('CLIENT_ID'),
            env.str('CLIENT_SECRET')
        )
        product_id = call.data
        product_data = get_product(moltin_token, product_id)['data']
        
        await call.message.answer(
            text=create_product_description_text(product_data),
            # reply_markup=create_default_keyboard()
        )

        await state.finish()