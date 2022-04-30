import re

from environs import Env
from requests.exceptions import HTTPError

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

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
from moltin_api import remove_cart_item
from moltin_api import create_customer


env = Env()
env.read_env()

storage = MemoryStorage()
bot = Bot(token=env.str('TG_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    handle_menu = State()
    handle_description = State()
    handle_cart = State()
    handle_email = State()

    selected_product_id = State()


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(
        'Здравствуйте! Используйте кнопку меню «Ассортимент»',
        reply_markup=create_initial_keyboard())


@dp.message_handler(text='Ассортимент')
async def show_menu(message: types.Message):
    moltin_token = get_actual_token()
    products = get_products(moltin_token)

    await message.answer(
        'Выберите товар:', reply_markup=create_menu_keyboard(products))

    await UserState.handle_menu.set()


@dp.callback_query_handler(state=UserState.handle_menu)
async def handle_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    moltin_token = get_actual_token()

    if call.data == 'cancel':
        await call.message.delete()
        await call.message.answer(
            'Вернуться к выбору можно через кнопку «Ассортимент»',
            reply_markup=create_initial_keyboard())

        await state.finish()

    elif call.data == 'cart':
        cart_id = call.message.from_user.id
        cart_items_data = get_cart_items(moltin_token, cart_id)

        if len(cart_items_data['data']) == 0:
            await call.message.edit_text(
                'Ваша пуста...',
                reply_markup=create_cart_keyboard(cart_items_data))

            await UserState.handle_cart.set()
            return

        cart_text = fetch_cart_description(cart_items_data)

        await call.message.edit_text(
            cart_text, reply_markup=create_cart_keyboard(cart_items_data))

        await UserState.handle_cart.set()

    else:
        await call.message.delete()
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
            await call.message.answer(caption, reply_markup=reply_markup)

        await UserState.handle_description.set()


@dp.callback_query_handler(state=UserState.handle_description)
async def handle_description(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    cart_id = call.message.from_user.id
    moltin_token = get_actual_token()

    if call.data == 'to_menu':
        products = get_products(moltin_token)

        await call.message.answer(
            'Выберите товар:', reply_markup=create_menu_keyboard(products))

        await UserState.handle_menu.set()

    elif call.data == 'cart':
        cart_items_data = get_cart_items(moltin_token, cart_id)

        if len(cart_items_data['data']) == 0:
            await call.message.answer(
                'Ваша пуста...',
                reply_markup=create_cart_keyboard(cart_items_data))

            await UserState.handle_cart.set()
            return

        cart_text = fetch_cart_description(cart_items_data)

        await call.message.answer(
            cart_text, reply_markup=create_cart_keyboard(cart_items_data))

        await UserState.handle_cart.set()

    else:
        product_id = await state.get_data('selected_product_id')
        product_amount = int(call.data)

        add_to_cart(
            moltin_token, cart_id, product_id['selected_product_id'],
            product_amount)

        products = get_products(moltin_token)

        await call.message.answer(
            'Товар в корзине! Хотите выбрать что нибудь еще?',
            reply_markup=create_menu_keyboard(products))

        await UserState.handle_menu.set()


@dp.callback_query_handler(state=UserState.handle_cart)
async def handle_cart(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    moltin_token = get_actual_token()

    if call.data == 'to_menu':
        products = get_products(moltin_token)
        await call.message.edit_text(
            'Выберите товар:', reply_markup=create_menu_keyboard(products))

        await UserState.handle_menu.set()

    elif call.data == 'payment':
        await call.message.delete()
        await call.message.answer('введите ваш email')
        await UserState.handle_email.set()

    else:
        cart_id = call.message.from_user.id
        item_id = call.data
        remove_cart_item(moltin_token, cart_id, item_id)
        cart_items_data = get_cart_items(moltin_token, cart_id)

        if len(cart_items_data['data']) == 0:
            await call.message.edit_text(
                'Ваша пуста...',
                reply_markup=create_cart_keyboard(cart_items_data))

            await UserState.handle_cart.set()
            return

        cart_text = fetch_cart_description(cart_items_data)

        await call.message.edit_text(
            cart_text, reply_markup=create_cart_keyboard(cart_items_data))

        await UserState.handle_cart.set()


@dp.message_handler(state=UserState.handle_email)
async def handle_email(message: types.Message, state: FSMContext):
    user_answer = message.text
    email_mask = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    if not re.fullmatch(email_mask, user_answer):
        await message.answer(
            'Неккоректный формат email. Попробуйте ввести еще раз... '
            '\n(пример: thebestfish@mail.com)')
        await UserState.handle_email.set()
        return

    moltin_token = get_actual_token()

    try:
        status_code = create_customer(moltin_token, user_answer)

    except HTTPError:
        if status_code == 409:
            pass

    await message.answer('Спасибо, с вами свяжется наш менеджер :)')
    await state.finish()


async def on_startup(dispatcher):
    print('Bot was started')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
