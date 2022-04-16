from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardButton

from moltin_api import get_products


def create_default_keyboard():
    keyboard = ReplyKeyboardMarkup()

    keyboard.add(KeyboardButton(text='Ассортимент'))

    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True

    return keyboard


def create_product_keyboard(moltin_token):
    products = get_products(moltin_token)
    keyboard = InlineKeyboardMarkup()
    
    for product in products:
        keyboard.add(
            InlineKeyboardButton (
                text=product['name'].lower(),
                callback_data=product['id']
            )
        )

    keyboard.add(
        InlineKeyboardButton (
            text='отмена',
            callback_data='cancel'
        )
    )

    return keyboard