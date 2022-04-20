from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardButton


def create_default_keyboard():
    keyboard = ReplyKeyboardMarkup()

    keyboard.add(KeyboardButton('Ассортимент'))

    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True

    return keyboard


def create_menu_keyboard(products):
    keyboard = InlineKeyboardMarkup()

    for product in products:
        keyboard.add(
            InlineKeyboardButton(product['name'].lower(),
                                 callback_data=product['id']))

    keyboard.add(
        InlineKeyboardButton('корзина', callback_data='cart'))

    keyboard.add(
        InlineKeyboardButton('отмена', callback_data='cancel'))

    return keyboard


def create_product_description_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.insert(
        InlineKeyboardButton('5', callback_data='five_kg'))

    keyboard.insert(
        InlineKeyboardButton('10', callback_data='ten_kg'))
    
    keyboard.insert(
        InlineKeyboardButton('15', callback_data='fifteen_kg'))

    keyboard.add(
        InlineKeyboardButton('корзина', callback_data='cart'))

    keyboard.add(
        InlineKeyboardButton('в меню', callback_data='to_menu'))

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
