from pprint import pprint
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from user_state import UserState

from keyboards import create_initial_keyboard
from keyboards import create_menu_keyboard
from keyboards import create_product_description_keyboard
from keyboards import create_cart_keyboard

from handle_data_lib import fetch_caption
from handle_data_lib import fetch_img_url
from handle_data_lib import fetch_cart_description

from moltin_api import get_actual_token
from moltin_api import get_products
from moltin_api import get_product
from moltin_api import add_to_cart
from moltin_api import get_cart_items


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(
        'Здравствуйте! Используйте кнопку меню «Ассортимент»',
        reply_markup=create_initial_keyboard())


@dp.message_handler(text='Ассортимент')
async def show_menu(message: types.Message):
    moltin_token = get_actual_token()
    products = get_products(moltin_token)

    await message.answer('Выберите товар:',
                         reply_markup=create_menu_keyboard(products))

    await UserState.handle_menu.set()


@dp.callback_query_handler(state=UserState.handle_menu)
async def handle_menu(call: types.CallbackQuery,
                      state: FSMContext):
    await call.answer()
    moltin_token = get_actual_token()

    if call.data == 'cancel':
        await call.message.answer(
            'Вернуться к выбору можно через кнопку «Ассортимент»',
            reply_markup=create_initial_keyboard())
        await state.finish()

    elif call.data == 'cart':
        cart_id = call.message.from_user.id
        cart_items_data = get_cart_items(moltin_token, cart_id)
        # pprint(cart_items_data)
        # phone id: 1607547372
        print(call.message.from_user.id)
        if len(cart_items_data['data']) == 0:
            await call.message.answer('Ваша пуста...', reply_markup=create_initial_keyboard())

            await state.finish()

        cart_text = fetch_cart_description(cart_items_data)

        await call.message.answer(
            cart_text, reply_markup=create_cart_keyboard(cart_items_data))

        await state.finish()

    else:
        product_id = call.data
        await state.update_data(selected_product_id=product_id)
        product_data = get_product(moltin_token, product_id)

        caption = fetch_caption(product_data)
        img_url = fetch_img_url(product_data)
        reply_markup = create_product_description_keyboard()

        if img_url:
            await call.message.answer_photo(
                photo=img_url, caption=caption, reply_markup=reply_markup)

        else:
            await call.message.answer(
                caption, reply_markup=reply_markup)

        await UserState.handle_description.set()


@dp.callback_query_handler(state=UserState.handle_description)
async def handle_add_to_cart(call: types.CallbackQuery,
                             state: FSMContext):
    await call.answer()
    cart_id = call.message.from_user.id
    moltin_token = get_actual_token()

    if call.data == 'to_menu':
        products = get_products(moltin_token)

        await call.message.answer(
            'Выберите товар:', reply_markup=create_menu_keyboard(products))

        await UserState.handle_menu.set()

    elif call.data == 'cart':
        cart_data = get_or_create_cart(moltin_token, cart_id)

        pprint(cart_data)

        await call.message.answer(
            'Тут будет корзина... Стейт сброшен.',
            reply_markup=create_initial_keyboard())

        await state.finish()

    else:
        product_id = await state.get_data('selected_product_id')
        product_amount = int(call.data)

        add_to_cart(moltin_token, cart_id, product_id['selected_product_id'],
                    product_amount)

        await call.message.answer(
            text='Товар в корзине! State was reset',
            reply_markup=create_initial_keyboard()
        )

        await state.finish()
