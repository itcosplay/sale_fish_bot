from pprint import pprint
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from user_state import UserState

from keyboards import create_default_keyboard
from keyboards import create_menu_keyboard
from keyboards import create_product_description_keyboard

from handle_data_lib import fetch_caption
from handle_data_lib import fetch_img_url

from moltin_api import get_actual_token
from moltin_api import get_products
from moltin_api import get_product
from moltin_api import add_to_cart


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(
        'Здравствуйте! Используйте кнопку меню «Ассортимент»',
        reply_markup=create_default_keyboard())


@dp.message_handler(text='Ассортимент')
async def show_products(message:types.Message):
    moltin_token = get_actual_token()
    products = get_products(moltin_token)

    await message.answer('Выберите товар:',
                         reply_markup=create_menu_keyboard(products))

    await UserState.handle_menu.set()


@dp.callback_query_handler(state=UserState.handle_menu)
async def show_selected_product(call:types.CallbackQuery,
                                state:FSMContext):
    if call.data == 'cancel':
        await call.message.answer(
            text='Вернуться к выбору можно через кнопку «Ассортимент»',
            reply_markup=create_default_keyboard())
        await state.finish()

    elif call.data == 'cart':
        await call.message.answer(
            text='Тут будет корзина... Стейт сброшен.',
            reply_markup=create_default_keyboard())

    else:
        moltin_token = get_actual_token()
        product_id = call.data
        product_data = get_product(moltin_token, product_id)
        pprint(product_data)
        caption = fetch_caption(product_data)
        img_url = fetch_img_url(product_data)
        reply_markup=create_product_description_keyboard()

        if img_url:
            await call.message.answer_photo(
                photo=img_url, caption=caption, reply_markup=reply_markup)

        else:
            await call.message.answer(
                caption, reply_markup=reply_markup)

        await UserState.handle_description.set()


@dp.callback_query_handler(state=UserState.handle_description)
async def handle_add_to_cart(
    call:types.CallbackQuery,
    state:FSMContext
):
    if call.data == 'back':
        moltin_token = get_actual_token()
        print('ACTUAL TOKEN: ', moltin_token)
        products = get_products(moltin_token)
    
        await call.message.answer(
            text='Пожалуйста, выберите товар:',
            reply_markup=create_product_keyboard(products)
        )

        await UserState.selectig_product.set()

    elif call.data == 'add_to_cart':
        state_data = await state.get_data()
        selected_product = state_data['selectig_product']
        
        moltin_token = get_actual_token()
        cart_id = call.message.from_user.id
        # cart = get_or_create_cart(moltin_token, cart_id)
        added = add_to_cart(moltin_token, cart_id, selected_product, 1)
        pprint.pprint(added)

        await call.message.answer(
            text='Товар в корзине!',
            # reply_markup=create_product_keyboard(products)
        )