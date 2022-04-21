from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardButton


def create_initial_keyboard():
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
        InlineKeyboardButton('buy 5 kg', callback_data='5'))

    keyboard.insert(
        InlineKeyboardButton('buy 10 kg', callback_data='10'))
    
    keyboard.insert(
        InlineKeyboardButton('buy 15 kg', callback_data='15'))

    keyboard.add(
        InlineKeyboardButton('корзина', callback_data='cart'))

    keyboard.add(
        InlineKeyboardButton('в меню', callback_data='to_menu'))

    return keyboard


def create_cart_keyboard(cart_data):
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
