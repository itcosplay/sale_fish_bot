from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

import pprint

from moltin_api import get_actual_token
from moltin_api import get_products
from moltin_api import get_product
from moltin_api import get_product_img_url
from moltin_api import add_to_cart

from loader import dp

from user_state import UserState

from keyboards import create_default_keyboard
from keyboards import create_product_keyboard
from keyboards import create_product_description_keyboard


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(
        'Здравствуйте! Используйте кнопку меню «Ассортимент»',
        reply_markup=create_default_keyboard())


@dp.message_handler(text='Ассортимент')
async def show_products(message:types.Message,  state:FSMContext):
    moltin_token = get_actual_token()
    user_id = message.from_user.id
    print('ACTUAL TOKEN: ', moltin_token)
    print('user_id: ', user_id)
    products = get_products(moltin_token)
    
    await message.answer(
        text='Пожалуйста, выберите товар:',
        reply_markup=create_product_keyboard(products)
    )
    
    await state.update_data(cart=[])
    await UserState.selectig_product.set()


@dp.callback_query_handler(state=UserState.selectig_product)
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
    
    elif call.data == 'cart':
        pass

    else:
        moltin_token = get_actual_token()
        product_id = call.data

        await state.update_data(selectig_product=product_id)

        product_data = get_product(moltin_token, product_id)['data']

        product_name = product_data['name']
        product_description = product_data['description']
        product_price = product_data[
            'meta']['display_price']['with_tax']['formatted']

        caption = f'{product_name}'
        caption += f'\n\n{product_description}'
        caption += f'\n\n{product_price}'

        img_data = product_data['relationships'].get('main_image')['data']

        if img_data:
            product_img_id = img_data['id']

        else:
            product_img_id = None

        if product_img_id:
            await call.message.answer_photo(
                photo=get_product_img_url(moltin_token, product_img_id),
                caption=caption,
                reply_markup=create_product_description_keyboard()
            )

        else:
            await call.message.answer(
                text=caption,
                reply_markup=create_product_description_keyboard()
            )

        await UserState.adding_cart.set()


@dp.callback_query_handler(state=UserState.adding_cart)
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