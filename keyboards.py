from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardButton


def create_default_keyboard():
    keyboard = ReplyKeyboardMarkup()

    keyboard.add(KeyboardButton(text='Ассортимент'))

    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True

    return keyboard


def create_product_keyboard(products):
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


def create_product_description_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text='добавить в корзину',
            callback_data='add_to_cart'
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text='назад',
            callback_data='back'
        )
    )

    return keyboard


def create_after_added_product_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(
            text='корзина',
            callback_data='show_cart'
        )
    )

    keyboard.add(
        InlineKeyboardButton(
            text='выбрать еще товар',
            callback_data='another_product'
        )
    )

    return keyboard